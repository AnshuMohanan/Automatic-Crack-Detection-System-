# data_processor.py

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from sklearn.preprocessing import StandardScaler
from collections import deque

# Import constants from the configuration file
import config

# ==============================================================================
# == ⚙️ STATEFUL REAL-TIME PROCESSOR
# ==============================================================================

class RealTimeProcessor:
    """
    Handles stateful processing of individual real-time data points using a
    pre-fitted, generalized scaler.
    """
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self.buffer = deque(maxlen=config.BUFFER_SIZE)

    def process_new_reading(self, load_kn, lvdt_mm):
        load_n = load_kn * 1000
        raw_stress = load_n / config.AREA
        raw_strain = lvdt_mm / config.LENGTH
        self.buffer.append({'stress': raw_stress, 'strain': raw_strain})

        if len(self.buffer) < config.SMOOTH_WINDOW_LENGTH:
            return raw_stress, raw_strain, -1  # Return default "waiting" status

        stress_history = np.array([p['stress'] for p in self.buffer])
        strain_history = np.array([p['strain'] for p in self.buffer])

        smoothed_stress_point = savgol_filter(stress_history, config.SMOOTH_WINDOW_LENGTH, config.SMOOTH_POLY_ORDER)[-1]
        smoothed_strain_point = savgol_filter(strain_history, config.SMOOTH_WINDOW_LENGTH, config.SMOOTH_POLY_ORDER)[-1]

        prev_raw_stress = self.buffer[-2]['stress']
        prev_raw_strain = self.buffer[-2]['strain']

        scaled_point = self.scaler.transform([[smoothed_stress_point, smoothed_strain_point]])
        prev_point_scaled = self.scaler.transform([[prev_raw_stress, prev_raw_strain]])

        scaled_stress = scaled_point[0, 0]
        scaled_strain = scaled_point[0, 1]
        stress_diff = scaled_stress - prev_point_scaled[0, 0]
        strain_diff = scaled_strain - prev_point_scaled[0, 1]

        slope = scaled_stress / (scaled_strain + 1e-6)
        sudden_drop_flag = 1 if stress_diff < config.STRESS_DROP_THRESHOLD else 0
        sudden_rise_flag = 1 if stress_diff > config.STRESS_RISE_THRESHOLD else 0
        stress_curve_score = scaled_stress * scaled_strain

        feature_vector = np.array([[
            scaled_stress, scaled_strain, slope, stress_diff, strain_diff,
            sudden_drop_flag, sudden_rise_flag, stress_curve_score
        ]])
        
        prediction = self.model.predict(feature_vector)[0]
        return raw_stress, raw_strain, prediction

# ==============================================================================
# == ⚙️ BATCH DATA PROCESSING FUNCTION (HIGH-ACCURACY MODE)
# ==============================================================================

def process_dataframe_for_batch_prediction(df):
    """
    Processes a full dataframe by creating a new, specialized scaler on-the-fly
    for maximum accuracy.
    """
    df.columns = [col.strip() for col in df.columns]
    if 'LVDT(mm)' not in df.columns or 'LOAD CELL(KN)' not in df.columns:
        raise ValueError("Required columns 'LVDT(mm)' and 'LOAD CELL(KN)' not found.")

    df = df[['LVDT(mm)', 'LOAD CELL(KN)']].copy()
    df.dropna(inplace=True)
    if df.empty:
        raise ValueError("DataFrame is empty after cleaning raw data.")

    df['Stress (N/mm²)'] = (df['LOAD CELL(KN)'] * 1000) / config.AREA
    df['Strain'] = df['LVDT(mm)'] / config.LENGTH

    original_stress = df['Stress (N/mm²)'].copy()
    original_strain = df['Strain'].copy()

    smoothed_stress = savgol_filter(df['Stress (N/mm²)'], config.SMOOTH_WINDOW_LENGTH, config.SMOOTH_POLY_ORDER)
    smoothed_strain = savgol_filter(df['Strain'], config.SMOOTH_WINDOW_LENGTH, config.SMOOTH_POLY_ORDER)

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array([smoothed_stress, smoothed_strain]).T)
    df['STRESS(SS)'] = scaled_data[:, 0]
    df['STRAIN(SS)'] = scaled_data[:, 1]

    df['SLOPE'] = df['STRESS(SS)'] / (df['STRAIN(SS)'] + 1e-6)
    df['STRESS DIFFERENCE'] = df['STRESS(SS)'].diff().fillna(0)
    df['STRAIN DIFFERENCE'] = df['STRAIN(SS)'].diff().fillna(0)
    df['SUDDEN DROP FLAG'] = (df['STRESS DIFFERENCE'] < config.STRESS_DROP_THRESHOLD).astype(int)
    df['SUDDEN RISE FLAG'] = (df['STRESS DIFFERENCE'] > config.STRESS_RISE_THRESHOLD).astype(int)
    df['STRESS CURVE'] = df['STRESS(SS)'] * df['STRAIN(SS)']

    df.rename(columns={'STRESS(SS)': 'STRESS', 'STRAIN(SS)': 'STRAIN'}, inplace=True)
    df['Original_Stress'] = original_stress
    df['Original_Strain'] = original_strain
    return df
# config.py

# ==============================================================================
# == ⚙️ APPLICATION CONFIGURATION
# ==============================================================================

# --- Model & Scaler Files ---
MODEL_PATH = "logistic_model.pkl"
SCALER_PATH = "scaler.pkl"

# --- Physical Properties ---
AREA = 22500  # Area in mm^2
LENGTH = 1000  # Length in mm

# --- Data Processing Parameters ---
BUFFER_SIZE = 20
SMOOTH_WINDOW_LENGTH = 7
SMOOTH_POLY_ORDER = 3

# --- Feature Engineering Thresholds ---
STRESS_DROP_THRESHOLD = -0.05
STRESS_RISE_THRESHOLD = 0.05

# --- GUI Mappings ---
# Status codes and their human-readable descriptions
CRACK_CONDITIONS = {
    -1: "Waiting for data...",
    0: "No Crack! Safe",
    1: "Minute Crack Forming!",
    2: "Minute Crack Formed!",
    3: "Large Crack Forming!",
    4: "Large Crack Formed!"
}

# Color coding for different statuses
COLOR_MAPPING = {
    -1: "grey",
    0: "blue",
    1: "green",
    2: "orange",
    3: "red",
    4: "purple"
}
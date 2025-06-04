import os
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from helper_functions import log_info, log_error

# Load environment variables
load_dotenv()

# Define base paths dynamically with default values
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, os.getenv('ARTIFACTS_DIR', 'artifacts'))
DATA_DIR = os.path.join(BASE_DIR, os.getenv('DATA_DIR', 'data'))

# Output file paths
TRAIN_PROCESSED_PATH = os.path.join(ARTIFACTS_DIR, "train_processed.csv")
VAL_PROCESSED_PATH = os.path.join(ARTIFACTS_DIR, "val_processed.csv")

# Ensure directories exist
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def load_and_process_data(csv_path, test_size=0.2, random_state=42):
    """
    Load and process the Social Network Ads dataset.
    
    Args:
        csv_path (str): Path to the input CSV file
        test_size (float): Proportion of the dataset to include in the validation split
        random_state (int): Random state for reproducibility
        
    Returns:
        tuple: ((X_train, y_train), (X_val, y_val))
    """
    try:
        log_info(f"Loading dataset from: {csv_path}")
        df = pd.read_csv(csv_path)

        # Select features and target
        X = df[['Age', 'EstimatedSalary']]  # Using Age and Salary as features
        y = df['Purchased']  # Target variable

        # Split into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=random_state,
            stratify=y  # Ensure balanced split
        )

        # Save processed data
        train_df = pd.concat([X_train, y_train], axis=1)
        val_df = pd.concat([X_val, y_val], axis=1)
        
        train_df.to_csv(TRAIN_PROCESSED_PATH, index=False)
        val_df.to_csv(VAL_PROCESSED_PATH, index=False)

        log_info("Processed data saved successfully.")
        return (X_train, y_train), (X_val, y_val)

    except Exception as e:
        log_error(f"Failed to load/process data: {str(e)}")
        raise

if __name__ == "__main__":
    sample_data_path = os.path.join(DATA_DIR, "Social_Network_Ads.csv")
    load_and_process_data(sample_data_path)

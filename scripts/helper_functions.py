import os
import logging
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

# Load environment variables with defaults
load_dotenv()

# Define data paths
DATA_PATH = os.getenv('DATA_PATH', 'data/raw/dataset.csv')
TRAIN_PROCESSED_PATH = os.getenv('TRAIN_PROCESSED_PATH', 'data/processed/train.csv')
VAL_PROCESSED_PATH = os.getenv('VAL_PROCESSED_PATH', 'data/processed/val.csv')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

def log_info(message: str) -> None:
    """Log information message."""
    logger.info(message)

def log_error(message: str) -> None:
    """Log error message."""
    logger.error(message)

def setup_logging(log_file: str = 'logs/mlops.log') -> None:
    """
    Set up logging configuration
    
    Args:
        log_file (str): Path to the log file
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

def evaluate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate evaluation metrics
    
    Args:
        y_true (np.ndarray): True labels
        y_pred (np.ndarray): Predicted labels
        
    Returns:
        dict: Dictionary containing evaluation metrics
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    try:
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted')
        }
        logger.info(f"Evaluation metrics: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        raise

def clean_text(text: str) -> str:
    """
    Clean and normalize text data.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    return str(text).strip()

def save_processed_data(
    data: pd.DataFrame,
    filepath: str,
    index: bool = False
) -> None:
    """
    Save processed data to CSV.
    
    Args:
        data (pd.DataFrame): Data to save
        filepath (str): Output file path
        index (bool): Whether to save index
    """
    try:
        data.to_csv(filepath, index=index)
        log_info(f"Data saved successfully to {filepath}")
    except Exception as e:
        log_error(f"Failed to save data to {filepath}: {str(e)}")
        raise

def validate_dataframe(
    df: pd.DataFrame,
    required_columns: list
) -> bool:
    """
    Validate DataFrame has required columns.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        required_columns (list): List of required column names
        
    Returns:
        bool: True if valid, False otherwise
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        log_error(f"Missing required columns: {missing_cols}")
        return False
    return True

def load_and_process_data(csv_path):
    try:
        log_info(f"Loading dataset from: {csv_path}")
        df = pd.read_csv(csv_path)

        # Ensure required columns exist
        if 'text' not in df.columns or 'summary' not in df.columns:
            log_error("Missing 'text' or 'summary' column in dataset.")
            return None, None

        # Clean text
        df['text'] = df['text'].apply(clean_text)
        df['summary'] = df['summary'].apply(clean_text)

        # Split into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            df['text'], df['summary'], test_size=0.2, random_state=42
        )

        # Save processed data
        pd.DataFrame({'text': X_train, 'summary': y_train}).to_csv(TRAIN_PROCESSED_PATH, index=False)
        pd.DataFrame({'text': X_val, 'summary': y_val}).to_csv(VAL_PROCESSED_PATH, index=False)

        log_info("Processed data saved successfully.")
        return (X_train, y_train), (X_val, y_val)

    except Exception as e:
        log_error(f"Failed to load/process data: {str(e)}")
        return None, None

if __name__ == "__main__":
    load_and_process_data(DATA_PATH)

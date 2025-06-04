# MLOps Data Processing Application 🤖

A streamlined data processing application built with Python and Streamlit for MLOps workflows. This application provides an intuitive interface for data preprocessing, splitting, and validation tasks.

## 🌟 Features

- Interactive web interface built with Streamlit
- CSV file upload and processing
- Configurable train-test split parameters
- Real-time data validation and processing
- Automatic artifact generation
- Comprehensive logging system
- Docker support for containerized deployment

## 🛠️ Project Structure

```
mlops/
├── scripts/
│   ├── app.py              # Streamlit web application
│   ├── data_processing.py  # Data processing logic
│   └── helper_functions.py # Utility functions
├── data/                   # Data directory for CSV files
├── artifacts/             # Processed data outputs
├── logs/                  # Application logs
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mlops
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Direct Execution
```bash
streamlit run scripts/app.py
```

#### Option 2: Docker Deployment
```bash
docker build -t mlops-app .
docker run -p 8501:8501 -v ${PWD}/data:/app/data -v ${PWD}/artifacts:/app/artifacts -v ${PWD}/logs:/app/logs mlops-app
```

The application will be available at `http://localhost:8501`

## 📊 Usage

1. Open the application in your web browser
2. Use the sidebar to configure processing parameters:
   - Test Split Size (0.1 to 0.4)
   - Random State (0 to 100)
3. Upload your CSV file using the file uploader
4. Click "Process Data" to start the processing
5. View the results:
   - Training and validation data samples
   - Dataset statistics
   - Processing logs

## 📁 Input Data Format

The application expects CSV files with the following columns:
- `text`: The input text data
- `summary`: The corresponding summary or target variable

## 📂 Output

Processed data is saved in the `artifacts` directory:
- `train_processed.csv`: Training dataset
- `val_processed.csv`: Validation dataset

Logs are stored in:
- `logs/mlops.log`: Application logs

## 🔧 Configuration

Environment variables can be set in a `.env` file:
```env
ARTIFACTS_DIR=artifacts
```

## 🐳 Docker Support

The included Dockerfile provides a containerized environment for the application. Build and run commands are provided above in the "Running the Application" section.

## 📝 Logging

The application includes comprehensive logging:
- Info level: General processing information
- Error level: Processing and validation errors
- Logs are saved to `logs/mlops.log`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 

> **An end-to-end machine learning solution to detect phishing websites with 95%+ accuracy using ensemble learning techniques.**

### **Base URL**
```
https://networksecurity-wjcj.onrender.com
```
---


## ✨ Key Features

### **🔍 Intelligent Detection**
- **30+ Feature Analysis**: URL structure, domain age, SSL status, DNS records, traffic patterns
- **Ensemble Learning**: Combines Random Forest, Gradient Boosting, and AdaBoost
- **High Accuracy**: 95%+ detection rate with minimal false positives

### **🚀 Production-Ready**
- **RESTful API**: FastAPI with auto-generated Swagger documentation
- **Containerized**: Docker support for consistent deployment
- **CI/CD Pipeline**: Automated testing and deployment
- **Experiment Tracking**: MLflow and DagsHub integration
- **Monitoring**: Comprehensive logging and error handling

### **📊 MLOps Excellence**
- **Modular Design**: Separate components for ingestion, transformation, training
- **Version Control**: Git + DVC for model and data versioning
- **Reproducibility**: Complete pipeline automation

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Data Source   │────▶│  Data Ingestion  │────▶│ Data Validation │
│  (PhishingData) │     │   Component      │     │   Component     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                           │
                                                           ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Prediction    │◀────│  Model Trainer   │◀────│ Data Transform  │
│   Pipeline      │     │   Component      │     │   Component     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐     
│   FastAPI Web   │   
│   Application   │  
└─────────────────┘     
```

### **Pipeline Workflow**

1. **Data Ingestion**: Load and split phishing dataset
2. **Data Validation**: Check schema, detect drift, validate quality
3. **Data Transformation**: Feature engineering, scaling, encoding
4. **Model Training**: Hyperparameter tuning, cross-validation
5. **Model Deployment**: Serialize and deploy best model
6. **Prediction Service**: REST API for real-time predictions

---

## 📈 Model Performance

### **Test Set Results**

| Metric | Score |
|--------|-------|
| **Precision** | 95.18% |
| **Recall** | 95.23% |
| **F1-Score** | 95.20% |

## 🛠️ Tech Stack

### **Machine Learning**
- **Scikit-learn**: Model training and evaluation
- **Pandas & NumPy**: Data manipulation
- **Imbalanced-learn**: Handling class imbalance

### **Model Training & Tracking**
- **MLflow**: Experiment tracking and model registry
- **DagsHub**: Collaborative ML platform

### **Web Framework & Deployment**
- **FastAPI**: High-performance async API
- **Uvicorn**: ASGI server

### **DevOps & Tools**
- **Docker**: Containerization
- **GitHub Actions**: CI/CD pipeline
- **MongoDB**: Data storage
- **Python 3.8+**: Core language

---

## 📂 Project Structure

```
networksecurity_ml/
│
├── NetworkSecurity/           # Main package
│   ├── components/           # Pipeline components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   
│   │
│   ├── entity/               # Data classes
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   │
│   ├── pipeline/             # Training & prediction pipelines
│   │   ├── training_pipeline.py
│   │   └── batch_prediction.py
│   │
│   ├── utils/                # Utility functions
│   │   ├── main_utils/
│   │   └── ml_utils/
│   │
│   ├── exception/            # Custom exceptions
│   ├── logging/              # Logging configuration
│   └── constants/            # Constants and configs
│
├── final_model/              # Saved models
│   ├── model.pkl
│   └── preprocessor.pkl
│
│
├── Network_Data/             # Dataset
│   └── phisingData.csv
│
├── .github/workflows/        # CI/CD workflows
│   └── main.yml
│
├── app.py                    # FastAPI application
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
└── README.md                 # This file
```

---

## 🚀 Installation

### **Prerequisites**
- Python 3.8 or higher
- pip package manager
- Git

### **Clone Repository**

```bash
git clone https://github.com/arpitverma108/networksecurity_ml.git
cd networksecurity_ml
```

### **Create Virtual Environment**

```bash
# Create environment
conda create -p networksecurity python=3.8 -y
conda activate networksecurtiy

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Environment Variables**

Create a `.env` file in the root directory:

```env
MONGODB_URL=your_mongodb_connection_string
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
DAGSHUB_TOKEN=your_dagshub_token
```

---

## 💻 Usage

### **1. Train the Model**

```bash
python main.py
```

This will:
- Load and preprocess data
- Train multiple models with hyperparameter tuning
- Track experiments in MLflow/DagsHub
- Save the best model

### **2. Run the API Server**

```bash
# Development
uvicorn app:app --reload

# Production
uvicorn app:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### **3. Access API Documentation**

Navigate to: `http://localhost:8000/docs`

Interactive Swagger UI for testing endpoints.

### **4. Make Predictions**

#### **Using Python:**

```python
import requests

url = "https://networksecurity-wjcj.onrender.com/predict"

# Sample website features
data = {
    "having_IP_Address": 1,
    "URL_Length": 1,
    "Shortining_Service": 1,
    "having_At_Symbol": 1,
    # ... all 30 features
}

response = requests.post(url, json=data)
print(response.json())


## 📚 API Documentation

### **Base URL**
```
https://networksecurityml.onrender.com
```

## 🧪 Experiments

The project uses **MLflow** and **DagsHub** for experiment tracking.

### **View Experiments**

```bash
mlflow ui
```

Navigate to: `http://localhost:5000`

### **Tracked Metrics**
- F1-Score
- Precision
- Recall
- Training time
- Model parameters
- Feature importance

### **DagsHub Integration**

All experiments are automatically synced to DagsHub:
- https://dagshub.com/arpitv0710/networksecurity_ml/experiments

**Experiment Summary:**
- 7+ experiments run
- Multiple model configurations tested
- Best model: **Random Forest with 256 estimators**
- F1-Score: 0.9920 (Training), 0.9893 (Test)

---

## 🎬 Demo

### **Live Application**
🔗 **URL**: https://networksecurity-wjcj.onrender.com/docs


#### Metrics Comparison
All metrics above 95%, demonstrating robust performance.

---

## 👤 Contact

**Arpit Verma**

- GitHub: [@arpitverma108](https://github.com/arpitverma108)
- LinkedIn: [Arpit Verma](https://www.linkedin.com/in/arpit-verma-871343283/)
- Email: arpitv0710@gmail.com
---
Made with ❤️ and ☕ by Arpit Verma


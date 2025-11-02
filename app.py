import os
import sys
import certifi
from NetworkSecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel
ca = certifi.where()
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(f"MongoDB URL: {mongo_db_url}")
from NetworkSecurity.pipeline.training_pipeline import TrainingPipeline
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import pymongo

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Form
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from NetworkSecurity.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Add this route to serve the CSV file for download
@app.get("/prediction_output/output.csv")
async def download_results():
    """Serve the prediction results CSV file for download"""
    file_path = "prediction_output/output.csv"
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="phishing_detection_results.csv",
            media_type='text/csv'
        )
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Results file not found. Please run a prediction first.")

# Alternative route with better name
@app.get("/download-results")
async def download_results_alt():
    """Alternative route to download results"""
    file_path = "prediction_output/output.csv"
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="phishing_detection_results.csv",
            media_type='text/csv'
        )
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Results file not found. Please run a prediction first.")

# Add static file serving for prediction_output directory
app.mount("/prediction_output", StaticFiles(directory="prediction_output"), name="prediction_output")

# Create templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("prediction_output", exist_ok=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(None)):
    try:
        # Check if it's a form submission (single prediction) or file upload
        form_data = await request.form()
        
        print(f"=== PREDICTION DEBUG START ===")
        print(f"Form data keys: {list(form_data.keys())}")
        print(f"File received: {file}")
        if file:
            print(f"File name: {file.filename}")
            print(f"File size: {file.size if hasattr(file, 'size') else 'N/A'}")
        
        df = None
        
        if file and file.filename and file.filename.endswith('.csv'):
            # CSV bulk prediction
            print("Processing CSV file...")
            df = pd.read_csv(file.file)
            print(f"CSV data shape: {df.shape}")
            print(f"CSV columns: {df.columns.tolist()}")
            print(f"First few rows:\n{df.head()}")
            
        elif form_data and any(key.startswith('having_') or key.startswith('URL_') for key in form_data.keys()):
            # Single prediction from form
            print("Processing form data...")
            feature_names = [
                "having_IP_Address", "URL_Length", "Shortining_Service", 
                "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix",
                "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length",
                "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor",
                "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL",
                "Redirect", "on_mouseover", "RightClick", "popUpWidnow",
                "Iframe", "age_of_domain", "DNSRecord", "web_traffic",
                "Page_Rank", "Google_Index", "Links_pointing_to_page", "Statistical_report"
            ]
            
            # Create single row DataFrame from form data
            data = {}
            missing_features = []
            for feature in feature_names:
                value = form_data.get(feature)
                if value is not None and value != '':
                    data[feature] = [int(value)]
                else:
                    missing_features.append(feature)
                    # Use default value for missing features
                    data[feature] = [1]  # Default to legitimate
            
            if missing_features:
                print(f"Missing features (using defaults): {missing_features}")
            
            df = pd.DataFrame(data)
            print(f"Form data DataFrame shape: {df.shape}")
            print(f"Form data values: {data}")
            
        else:
            print("No valid data provided")
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": "No data provided. Please fill the form or upload a CSV file."
            })
        
        # Check if model files exist
        if not os.path.exists("final_model/preprocessor.pkl"):
            raise FileNotFoundError("Preprocessor file not found at final_model/preprocessor.pkl")
        if not os.path.exists("final_model/model.pkl"):
            raise FileNotFoundError("Model file not found at final_model/model.pkl")
        
        # Your existing prediction logic
        print("Loading model and preprocessor...")
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        
        print("Making predictions...")
        y_pred = network_model.predict(df)
        print(f"Raw predictions: {y_pred}")
        
        df['predicted_column'] = y_pred
        
        # Convert -1 to 0 for better readability (phishing=0, legitimate=1)
        df['predicted_column'] = df['predicted_column'].replace(-1, 0)
        
        # Calculate summary statistics
        total_count = len(df)
        safe_count = (df['predicted_column'] == 1).sum()
        phishing_count = (df['predicted_column'] == 0).sum()
        
        print(f"Results - Total: {total_count}, Safe: {safe_count}, Phishing: {phishing_count}")
        print(f"Prediction distribution: {df['predicted_column'].value_counts().to_dict()}")
        
        # Save results
        df.to_csv('prediction_output/output.csv', index=False)
        print("Results saved to prediction_output/output.csv")
        
        # Convert to HTML table
        table_html = df.to_html(classes='data-table', index=False, escape=False)
        print(f"Table HTML generated: {len(table_html)} characters")
        print("=== PREDICTION DEBUG END ===")
        
        return templates.TemplateResponse("results.html", {
            "request": request, 
            "table": table_html,
            "total_count": total_count,
            "safe_count": safe_count,
            "phishing_count": phishing_count
        })
        
    except Exception as e:
        print(f"=== ERROR IN PREDICTION ===")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"=== ERROR END ===")
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": f"Prediction failed: {str(e)}"
        })

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Phishing Detection API is running"}

# Model info endpoint
@app.get("/model-info")
async def model_info():
    try:
        model_exists = os.path.exists("final_model/model.pkl")
        preprocessor_exists = os.path.exists("final_model/preprocessor.pkl")
        
        return {
            "model_loaded": model_exists,
            "preprocessor_loaded": preprocessor_exists,
            "model_path": "final_model/model.pkl",
            "preprocessor_path": "final_model/preprocessor.pkl"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting Phishing URL Detection Server...")
    print(f"Templates directory: {os.path.abspath('templates')}")
    print(f"Static directory: {os.path.abspath('static')}")
    print(f"Final model directory: {os.path.abspath('final_model')}")
    
    # Check if required directories exist
    if not os.path.exists("templates"):
        print("WARNING: templates directory does not exist!")
    if not os.path.exists("static"):
        print("WARNING: static directory does not exist!")
    if not os.path.exists("final_model"):
        print("WARNING: final_model directory does not exist!")
    
    app_run(app, host="0.0.0.0", port=8080)
#import library
from fastapi import FastAPI,Query

from fastapi.responses import JSONResponse
import pandas as pd 
import numpy as np 
import joblib

import sys
import os
sys.path.append(os.path.abspath("..")) 
from src.pydantic_model import Input_user,PredictionResponse
from src.shap import shap_model
from src.pipeline import Model_version



#import models
model=joblib.load('models/churn_pipeline.pkl')




#create Fastapi object
app=FastAPI()

#create end point
@app.get('/')
def hello():
    return {"message": "This API predicts whether a customer will churn or not"}


#endpoint
@app.get('/health')               
def health_check() -> dict :                #for machine visualisation
    return {
            'status':'ok',
            'version':Model_version,
            'model_loaded':model is not None}


#endpoint
@app.post('/predict',response_model=PredictionResponse)
def checking_customer_churn(data:Input_user):
    entry=pd.DataFrame([{
        'customerID':data.customerID,
        'gender':data.gender,
        'SeniorCitizen':data.SeniorCitizen,
        'Partner':data.Partner,
        'Dependents':data.Dependents,
       'tenure':data.tenure,
       'PhoneService':data.PhoneService,
       'MultipleLines':data.MultipleLines,
       'InternetService':data.InternetService,
       'OnlineSecurity':data.OnlineSecurity, 
       'OnlineBackup':data.OnlineBackup, 
       'DeviceProtection':data.DeviceProtection,
        'TechSupport':data.TechSupport,
       'StreamingTV':data.StreamingTV,
       'StreamingMovies':data.StreamingMovies,
       'Contract':data.Contract,
       'PaperlessBilling':data.PaperlessBilling,
       'PaymentMethod':data.PaymentMethod,
       'MonthlyCharges':data.MonthlyCharges,
       'TotalCharges':data.TotalCharges
    }])

    #prediction 
    prediction=int(model.predict(entry)[0])
    probs = model.predict_proba(entry)[0]
    #check confidance in percetage
    confidence = round(max(probs) * 100, 2)
    #classes
    class_labels=model.classes_.tolist()
    #diff probability
    #create mapping ({class name : probability})
    class_probs = dict(zip(class_labels, [round(p,2) for p in probs]))
    try:
        predicted_category = "Yes" if prediction == 1 else "No"
        return JSONResponse(status_code=200, content={"predicted_category":predicted_category,'Confidence' :confidence,
                                                          'Class Probabilities':class_probs})
        
        
    except Exception as e:
         return JSONResponse(status_code=500,content={"error": str(e)})


@app.post('/top-features')
def checking_top_feature(data: Input_user,top_n_feature: int = Query(..., description="Number of top contributing features")):
    
        
    entry=pd.DataFrame([{   
    'customerID':data.customerID,
    'gender':data.gender,
    'SeniorCitizen':data.SeniorCitizen,
    'Partner':data.Partner,
    'Dependents':data.Dependents,
    'tenure':data.tenure,
    'PhoneService':data.PhoneService,
    'MultipleLines':data.MultipleLines,
    'InternetService':data.InternetService,
    'OnlineSecurity':data.OnlineSecurity, 
    'OnlineBackup':data.OnlineBackup, 
    'DeviceProtection':data.DeviceProtection,
    'TechSupport':data.TechSupport,
    'StreamingTV':data.StreamingTV,
    'StreamingMovies':data.StreamingMovies,
    'Contract':data.Contract,
    'PaperlessBilling':data.PaperlessBilling,
    'PaymentMethod':data.PaymentMethod,
    'MonthlyCharges':data.MonthlyCharges,
    'TotalCharges':data.TotalCharges}])


    #checking prediction 
    prediction = int(model.predict(entry)[0])
    
    #checking shape values
    shaps=shap_model(entry,top_n_feature)

    
    return JSONResponse(
    status_code=200,
    content={"Checking shap values": shaps.to_dict(orient="records")}
)
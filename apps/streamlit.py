import streamlit as st 
import requests
import pandas as pd

#FastAPI end point for predict
#url="http://127.0.0.1:8000/predict"
#for docker when running image differently
#url="http://host.docker.internal:8000/predict"
#FastAPI for TopFeatures
#url_topfeatures="http://127.0.0.1:8000/top-features"
#url_topfeatures="http://host.docker.internal:8000/top-features"

#For compose file
#url = "http://fastapi:8000/predict"
#url_topfeatures = "http://fastapi:8000/top-features"

#for adjusting both syster and also docker file
import os

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000") 
#It dynamically decides which URL to use based on environment.
#Look for environment variable named API_URL
#If NOT found → use default:


url = f"{BASE_URL}/predict"
url_topfeatures = f"{BASE_URL}/top-features"



st.title('Predicting Customer Churn')


customerID=st.text_input("Enter customerID",'7590-VHVEG')      
gender= st.selectbox('Select gender ',['Male','Female'],0)     
SeniorCitizen=st.selectbox('if SeniorCitizen then 1 else 0',[1,0],1)
Partner=st.selectbox('do you have partner?',['Yes','No'],0)
Dependents= st.selectbox('Are you dependent?',['Yes','No'],1)    
tenure=st.number_input('Since when are you using ?',value=30)    
PhoneService=st.selectbox('do you have PhoneService?',['Yes','No'],1)    
MultipleLines=st.selectbox('is InternetService?',['Yes','No','No phone service'],1)    
InternetService=st.selectbox('Type of InternetService?',['Fiber optic','No','DSL'],1)   
OnlineSecurity=st.selectbox('is OnlineSecurity?',['No', 'Yes', 'No internet service'],1)   
OnlineBackup= st.selectbox('Is OnlineBackup?',['No', 'Yes', 'No internet service'],1)   
DeviceProtection=st.selectbox('DeviceProtection safety?',['No', 'Yes', 'No internet service'],1)      
TechSupport=st.selectbox('Are you getting techsupport?',['No', 'Yes', 'No internet service'],1)        
StreamingTV=st.selectbox('Is StreamingTV?',['No', 'Yes', 'No internet service'],1)      
StreamingMovies=st.selectbox('Is StreamingMovies?',['No', 'Yes', 'No internet service'],1)        
Contract=st.selectbox('What type of contract?',['Month-to-month', 'One year', 'Two year'],1)       
PaperlessBilling=st.selectbox('what about paperlessbilling?',['No','Yes'],1)     
PaymentMethod=st.selectbox('How do you pay?',['Electronic check','Mailed check','Bank transfer (automatic)', 'Credit card (automatic)'],2)     
MonthlyCharges=st.number_input('How much do you pay Monthly?',value=50.5)    
TotalCharges=st.number_input('Total Charges?',value=50.55)      

#input dict
entry={'customerID':customerID,
          'gender':gender,
          'SeniorCitizen':SeniorCitizen,
          'Partner':Partner,
          'Dependents':Dependents,
          'tenure':tenure,
          'PhoneService':PhoneService,
          'MultipleLines':MultipleLines,
          'InternetService':InternetService,
          'OnlineSecurity':OnlineSecurity,
          'OnlineBackup':OnlineBackup,
          'DeviceProtection':DeviceProtection,
          'TechSupport':TechSupport,
          'StreamingTV':StreamingTV,
          'StreamingMovies':StreamingMovies,
          'Contract':Contract,
          'PaperlessBilling':PaperlessBilling,
          'PaymentMethod':PaymentMethod,
          'MonthlyCharges':MonthlyCharges,
          'TotalCharges':TotalCharges
          }




if st.button('Predict'):
   
    response = requests.post(url, json=entry)

    if response.status_code == 200:
        result = response.json()
        #st.success(f"Churn Prediction : {result}")

        prediction = result["predicted_category"]
        confidence = result["Confidence"]
        prob = result["Class Probabilities"]

        st.success(f"Prediction: {prediction}")
        st.write(f"Confidence: {confidence}%")
        st.write("Class Probabilities:", prob)
    else:
        st.error("Error connecting to FastAPI backend") 

#------------------------------------------------------------------------------------


top_n_feature = st.number_input("How many do you want to see top contributing features for prediction?", value=5)

if st.button("Show Top Features"):
    
    response = requests.post(
        f"{url_topfeatures}?top_n_feature={top_n_feature}",
        json=entry
    )

    if response.status_code == 200:
        result = response.json()
        st.write("Top Feature Contributions")
        #st.write(result)
        #create pandas data frame
        df1 = pd.DataFrame(result["Checking shap values"])
        st.dataframe(df1)
    else:
        st.error("Error getting top features")



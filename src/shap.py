import shap
import os
import sys
sys.path.append(os.path.abspath("..")) 
from src.featureengineering import FeatureEngineering
from src.preprocessor import preprocessor
#from src.pipeline import pipeline
import joblib
import pandas as pd

def shap_model(entry,top_n_feature=5):
    #preprocessing data
    pipeline=joblib.load('models/churn_pipeline.pkl')
    X_fe = pipeline.named_steps["feature_engineering"].transform(entry)
    X_pre = pipeline.named_steps["preprocessing"].transform(X_fe)

    #saving model
    model = pipeline.named_steps["model"]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_pre)
    #to get feature name

    feature_names = pipeline.named_steps["preprocessing"].get_feature_names_out()
    
    #divide into 2 category
    import numpy as np
    shap_values_class1 = np.round(shap_values[0][:,1]*100,2)
    shap_values_class0 = np.round(shap_values[0][:,0]*100,2)

    
    model=joblib.load('models/churn_pipeline.pkl')
    prediction=int(model.predict(entry)[0])

    if prediction==1:
        shap_df = pd.DataFrame({
    "feature": feature_names,
    "shap_value_class1": shap_values_class1
    }).sort_values('shap_value_class1',ascending=False).head(top_n_feature)

    else:

        shap_df = pd.DataFrame({
        "feature": feature_names,
        "shap_value_class0": shap_values_class0
        }).sort_values('shap_value_class0',ascending=False).head(top_n_feature)

    return shap_df
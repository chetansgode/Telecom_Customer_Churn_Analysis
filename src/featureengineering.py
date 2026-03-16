#import library
from sklearn.base import BaseEstimator,TransformerMixin
import pandas as pd

class FeatureEngineering(BaseEstimator,TransformerMixin):
    def fit(self,X,y=None):
        return self
    
    def transform(self, X):
        X=X.copy()

        #droping customerID
        X = X.drop(columns=['customerID'])

        #convert text data 
        # convert TotalCharges
        X['TotalCharges'] = pd.to_numeric(X['TotalCharges'], errors='coerce')
        X['TotalCharges'] = X['TotalCharges'].fillna(X['MonthlyCharges'])


        # MonthlyCharges category
        def cal_MonthlyCharges(val):

            if val <= 30:
                return 0
            elif val <= 60:
                return 1
            elif val <= 90:
                return 2
            else:
                return 3
        

          # binary mapping
        binary_map = {'Yes':1,'No':0}

        for col in ['Partner','Dependents']:
            X[col] = X[col].map(binary_map)

        X['gender'] = X['gender'].map({'Male':1,'Female':0})

        # 3-category mapping
        X['MultipleLines'] = X['MultipleLines'].map({'Yes':1,'No':0,'No phone service':2})
        X['TechSupport'] = X['TechSupport'].map({'Yes':1,'No':0,'No internet service':2})
        X['OnlineSecurity'] = X['OnlineSecurity'].map({'Yes':1,'No':0,'No internet service':2})
        X['OnlineBackup'] = X['OnlineBackup'].map({'Yes':1,'No':0,'No internet service':2})
        X['DeviceProtection'] = X['DeviceProtection'].map({'Yes':1,'No':0,'No internet service':2})
        X['StreamingTV'] = X['StreamingTV'].map({'Yes':1,'No':0,'No internet service':2})
        X['StreamingMovies'] = X['StreamingMovies'].map({'Yes':1,'No':0,'No internet service':2})


        X['MonthlyCharges_category'] = X['MonthlyCharges'].apply(cal_MonthlyCharges)

        return X
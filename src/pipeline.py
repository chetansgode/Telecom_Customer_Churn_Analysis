#import function and class
from src.featureengineering import FeatureEngineering
from src.preprocessor import preprocessor
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

#import pipeline
from imblearn.pipeline import Pipeline

Model_version= "1.0.0"
#create pipeline


pipeline = Pipeline(steps=[

    ('feature_engineering', FeatureEngineering()),

    ('preprocessing', preprocessor),

    ('smote', SMOTE(sampling_strategy={1:3300}, random_state=5)),

    ('model', RandomForestClassifier(
        n_estimators=80,
        max_depth=7,
        random_state=5295
    ))

])





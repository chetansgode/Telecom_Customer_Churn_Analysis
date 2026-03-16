#import library
from sklearn.preprocessing import MinMaxScaler,PowerTransformer,OrdinalEncoder,OneHotEncoder
from sklearn.compose import ColumnTransformer

#step2-— Column Preprocessing

num_cols = ['MonthlyCharges','tenure']
power_cols = ['TotalCharges']
binary_cols = ['PhoneService','PaperlessBilling']
cat_cols = ['InternetService','Contract','PaymentMethod']

preprocessor = ColumnTransformer(

    transformers=[

        ('power', PowerTransformer(), power_cols),
        ('scale', MinMaxScaler(), num_cols),
        ('binary', OrdinalEncoder(), binary_cols),
        ('onehot', OneHotEncoder(handle_unknown='ignore'), cat_cols)

    ],

    remainder='passthrough'

)
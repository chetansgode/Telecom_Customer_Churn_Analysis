#import library
from pydantic import BaseModel,Field
from typing import Annotated,Literal,Dict

#pydantic model creation


class Input_user(BaseModel):

    customerID:Annotated[str,Field(...,description='Enter CustomerID')]
    gender:Annotated[Literal['Male','Female'],Field(...,description='Gender of Users')]
    SeniorCitizen:Annotated[Literal[1,0],Field(...,description='if SeniorCitizen then 1 else 0')]
    Partner:Annotated[Literal['Yes','No'],Field(...,description='do you have partner?')]
    Dependents:Annotated[Literal['Yes','No'],Field(...,description='do you have Dependents?')]
    tenure:Annotated[int,Field(...,description='Since when are you using ?')]
    PhoneService:Annotated[Literal['Yes','No'],Field(...,description='do you have PhoneService?')]
    MultipleLines:Annotated[Literal['Yes','No','No phone service'],Field(...,description='is InternetService?')]
    InternetService:Annotated[Literal['Fiber optic','No','DSL'],Field(...,description='Type of InternetService?')]
    OnlineSecurity:Annotated[Literal['No', 'Yes', 'No internet service'],Field(...,description='is OnlineSecurity?')]
    OnlineBackup:Annotated[Literal['No', 'Yes', 'No internet service'],Field(...,description='Is OnlineBackup?')]
    DeviceProtection:Annotated[Literal['No', 'Yes', 'No internet service'],Field(...,description='DeviceProtection safety?')]
    TechSupport:Annotated[Literal['No', 'Yes', 'No internet service'],Field(...,description='Are you getting techsupport?')]
    StreamingTV:Annotated[Literal['No', 'Yes', 'No internet service'],Field(...,description='Is StreamingTV?')]
    StreamingMovies:Annotated[Literal['No', 'Yes', 'No internet service'],Field(...,description='Is StreamingMovies?')]
    Contract:Annotated[Literal['Month-to-month', 'One year', 'Two year'],Field(...,description='What type of contract?')]
    PaperlessBilling:Annotated[Literal['No','Yes'],Field(...,description='what about paperlessbilling?')]
    PaymentMethod:Annotated[Literal['Electronic check','Mailed check','Bank transfer (automatic)', 'Credit card (automatic)'],Field(...,description='How do you pay?')]
    MonthlyCharges:Annotated[float,Field(...,description='How much do you pay Monthly?')]
    TotalCharges:Annotated[float,Field(...,description='Total Charges?')]



class PredictionResponse(BaseModel):

    predicted_category: str = Field(
        ...,
        description="Predicted churn category",
        example="Yes"
    )

    confidence: float = Field(
        ...,
        description="Model confidence score (0 to 1)",
        example=0.78
    )

    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probability distribution across all classes",
        example={"0": 0.21, "1": 0.79}
    )


from pydantic import BaseModel
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib
from fastapi import FastAPI
import pandas as pd
import secrets
from fastapi import Depends, FastAPI, HTTPException, status,Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import numpy as np
import uvicorn
from fonctions import *
from fastapi import File, UploadFile
import io
from fastapi.responses import StreamingResponse
import os

app = FastAPI(title='Churn Prediction')

security = HTTPBasic()


# si on deploy l'api dans kubernetes on recuperes les usernames et passwords à partir des variables d'environnement(secrets)
###########################################################################################################################
usernames = []
passwords = []

i=1

while i <= 3:

    usernames.append(encode(os.getenv("username"+str(i))))
    passwords.append(encode(os.getenv("password"+str(i))))
    i+=1

access = [1,0,0]


#####################################################################################################################

# si on lance une istance de l'api avec la commande python3 main.py ou comme un container Docker ou dans les test

#credentials = pd.read_csv('credentials.csv')

#usernames = list(credentials['usernames'])
#passwords = list(credentials['passwords'])
#access = list(credentials['access'])

######################################################################################################################


user_pass = dict(zip(usernames,passwords)) # dict of users and password




def Authentication (credentials: HTTPBasicCredentials = Depends(security)):

    for user, password in user_pass.items():

        if (secrets.compare_digest(credentials.username, decode_64(user)) and secrets.compare_digest(credentials.password, decode_64(password))):

            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
        )



def Authorization (credentials: HTTPBasicCredentials = Depends(security)):

    for i, (user, password) in enumerate(user_pass.items()):

        if access[i] == 1 and (secrets.compare_digest(credentials.username, decode_64(user)) and secrets.compare_digest(credentials.password, decode_64(password))):

            return credentials.username
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
        )

@app.get('/status')
def get_status():
    return 1

# Using FastAPI instance
@app.get("/permissions",dependencies=[Depends(Authentication)])
async def permissions(username: str = Depends(Authentication)):

    url_list = [route.path for route in app.routes]

    rm = ['/openapi.json','/docs/oauth2-redirect','/redoc']

    for el in rm:
        url_list.remove(el)

    if access[usernames.index(encode(username))] == 1 :
        return ' Hello '+ username + ' you have access to the following services: ' +  str(url_list).replace('[','').replace(']','').replace("'",'')
    else:
        url_list.remove('/predict/RFC')
        
        return ' Hello '+ username+ ' you have access to the following services: ' +  str(url_list).replace('[','').replace(']','').replace("'",'')


class request_body(BaseModel):

    gender: str
    SeniorCitizen: str
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines:str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.post('/predict/KNC',dependencies=[Depends(Authentication)],tags = ['Predict'])
async def predict_KNC(data : request_body, username: str = Depends(Authentication)):

    """KNeighborsClassifier Model 
    
    Input: 

    a json data like the one in Request body

    Example:

    {"gender":"Male","SeniorCitizen":"0","Partner":"Yes","Dependents":"Yes","tenure":72,"PhoneService":"Yes","MultipleLines":"Yes","InternetService":"DSL","OnlineSecurity":"Yes","OnlineBackup":"No","DeviceProtection":"Yes","TechSupport":"Yes","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"Two year","PaperlessBilling":"Yes","PaymentMethod":"Credit card (automatic)","MonthlyCharges":83.55,"TotalCharges":6093.3}
    

    Output:

    Predict churn: Yes or No 
    
    """

    model = joblib.load('KNC.joblib')

    test_data = return_df(data)

    class_idx = model.predict(test_data)
    #probability = model.predict_proba(test_data).max()

    return { 'Hello ' + username + '! ' + ' Here your prediction for your data' : 'Yes' if class_idx==1 else 'No'} #,'probability': probability }


@app.post('/predict/RFC',dependencies=[Depends(Authorization)],tags = ['Predict'])
async def predict_RFC(data : request_body, username: str = Depends(Authorization)):

    """RandomForestClassifier Model 
    
    Input: 

    a json data like the one in Request body

    Example:

    {"gender":"Male","SeniorCitizen":"0","Partner":"Yes","Dependents":"Yes","tenure":72,"PhoneService":"Yes","MultipleLines":"Yes","InternetService":"DSL","OnlineSecurity":"Yes","OnlineBackup":"No","DeviceProtection":"Yes","TechSupport":"Yes","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"Two year","PaperlessBilling":"Yes","PaymentMethod":"Credit card (automatic)","MonthlyCharges":83.55,"TotalCharges":6093.3}
    

    Output:

    Predict churn: {Yes or No} and its probability 
    
    """

    model = joblib.load('RFC.joblib')

    test_data = return_df(data)

    class_idx = model.predict(test_data)
    probability = model.predict_proba(test_data).max()

    return { 'Hello ' + username + '! ' + ' Here your prediction for your data' : 'Yes' if class_idx==1 else 'No' ,'probability': probability }



@app.post('/predict/LR',dependencies=[Depends(Authentication)],tags = ['Predict'])
async def predict_LR(data : request_body, username: str = Depends(Authentication)):

    """LogisticRegression Model 

    Input: 

    a json data like the one in Request body

    Example:

    {"gender":"Male","SeniorCitizen":"0","Partner":"Yes","Dependents":"Yes","tenure":72,"PhoneService":"Yes","MultipleLines":"Yes","InternetService":"DSL","OnlineSecurity":"Yes","OnlineBackup":"No","DeviceProtection":"Yes","TechSupport":"Yes","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"Two year","PaperlessBilling":"Yes","PaymentMethod":"Credit card (automatic)","MonthlyCharges":83.55,"TotalCharges":6093.3}
    

    Output:

    Predict churn: {Yes or No} and its probability 
    
    """

    model = joblib.load('LR.joblib')

    test_data = return_df(data)

    class_idx = model.predict(test_data)
    probability = model.predict_proba(test_data).max()

    return { 'Hello ' + username + '! ' + ' Here your prediction for your data' : 'Yes' if class_idx==1 else 'No' ,'probability': probability }



@app.post('/predict/GBC',dependencies=[Depends(Authentication)],tags = ['Predict'])
async def predict_GBC(data : request_body, username: str = Depends(Authentication)):

    """GradientBoostingClassifier Model 

    Input: 

    a json data like the one in Request body

    Example:

    {"gender":"Male","SeniorCitizen":"0","Partner":"Yes","Dependents":"Yes","tenure":72,"PhoneService":"Yes","MultipleLines":"Yes","InternetService":"DSL","OnlineSecurity":"Yes","OnlineBackup":"No","DeviceProtection":"Yes","TechSupport":"Yes","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"Two year","PaperlessBilling":"Yes","PaymentMethod":"Credit card (automatic)","MonthlyCharges":83.55,"TotalCharges":6093.3}
    

    Output:

    Predict churn: {Yes or No} and its probability    
    
    """

    model = joblib.load('GBC.joblib')

    test_data = return_df(data)

    class_idx = model.predict(test_data)
    probability = model.predict_proba(test_data).max()

    return { 'Hello ' + username + '! ' + ' Here your prediction for your data' : 'Yes' if class_idx==1 else 'No' ,'probability': probability }




@app.get('/scores/{modele_type}',tags = ['Score Test data'])
async def get_scores(modele_type:str, Authentication=Header("username:password")):

    stat_authent = 0
    #On récupéer les données d'authentification du headers
    username, password = Authentication.split(":",2)

    for user, passw in user_pass.items():  
        if decode_64(user) == username :
            if decode_64(passw) == password:
                stat_authent = 1
                break
    #On vérifie l'authetification
    if stat_authent == 0 :
        raise HTTPException(status_code=403, detail="Erreur d'autentification")
        result = None


    if modele_type not in ['KNC','LR','GBC','RFC']:
        raise HTTPException(status_code=404, detail ="Le modele doit être : 'KNC','LR','GBC','RFC'")
    else :
        return scores_modele(modele_type)


@app.post('/predict/csv/{modele_type}',tags = ['Predict'])
async def predict_csv(modele_type:str, Authentication=Header("username:password"),csv_file: UploadFile = File(...)):
    '''

    Input:

    Please authenticate using your username and password 

    Insert one of machine learning model available: KNC, LR, GBC, RFC

    KNC: KNeighborsClassifier
    LR : LogisticRegression
    GBC: GradientBoostingClassifier
    RFC: RandomForestClassifier

    Upload a csv file of dataframe with columns:

    gender: str
    SeniorCitizen: str
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines:str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


    Output:

    Churn.csv with churn prediction column added to the dataframe
    
    '''

    stat_authent = 0
    #On récupéer les données d'authentification du headers
    username, password = Authentication.split(":",2)

    for user, passw in user_pass.items():  
        if decode_64(user) == username :
            if decode_64(passw) == password:
                stat_authent = 1
                break
    #On vérifie l'authetification
    if stat_authent == 0 :
        raise HTTPException(status_code=403, detail="Erreur d'autentification")
        result = None

    

    if modele_type not in ['KNC','LR','GBC','RFC']:
        raise HTTPException(status_code=404, detail ="Le modele doit être : 'KNC','LR','GBC','RFC'")
    else :
        df = pd.read_csv(io.StringIO(str(csv_file.file.read(), 'utf8')), encoding='utf8', sep = ',', header = 0)

        X_test=pd.read_csv("X_test.csv", sep = ',', header = 0)

        columns = X_test.columns

        if len(df.columns) != len(columns) or (df.columns != X_test.columns).any() or (df.dtypes != X_test.dtypes).any():
            
            raise HTTPException(status_code=422, detail="Unprocessable Entity: types or names of columns don't match or missing ones")

        df = predict_csv_modele(modele_type,df)

        stream = io.StringIO()
    
        df.to_csv(stream)
    
        response = StreamingResponse(iter([stream.getvalue()]),
                            media_type="text/csv"
        )
    
    response.headers["Content-Disposition"] = "attachment; filename=Churn.csv"

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)










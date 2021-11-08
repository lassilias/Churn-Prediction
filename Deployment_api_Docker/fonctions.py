import base64,joblib
import pandas as pd
import numpy as np
from sklearn.metrics import balanced_accuracy_score,log_loss, precision_score, recall_score, f1_score


def decode_64(base64_message):

    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message

def encode(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def scores_modele(modele_type : str):

    X_test=pd.read_csv("X_test.csv", sep = ',', header = 0)

    X_test = X_test.astype('str')
    X_test.tenure = X_test.tenure.astype('int')
    X_test.MonthlyCharges = X_test.MonthlyCharges.astype('float')
    X_test.TotalCharges = X_test.TotalCharges.astype('float')

    modele = joblib.load(modele_type + '.joblib')

    test_predictions = modele.predict(X_test) # calcul des predictions sur le jeu de test

    y_test = pd.read_csv("y_test.csv", sep = ',', header = 0)

    bac = np.round(balanced_accuracy_score(y_test.to_numpy(), test_predictions),2)
    f1 = np.round(f1_score(y_test.to_numpy(), test_predictions),2)
    pr = np.round(precision_score(y_test.to_numpy(), test_predictions),2)
    ll = np.round(log_loss(y_test.to_numpy(), test_predictions),2)

    result = {'Balanced Accuracy':bac,
                'F1 Score': f1,
                'Précision': pr,
                'Log Loss': ll}

    return result


def predict_csv_modele(modele_type : str,df):

    df = df.astype('str')
    df.tenure = df.tenure.astype('int')
    df.MonthlyCharges = df.MonthlyCharges.astype('float')
    df.TotalCharges = df.TotalCharges.astype('float')

    modele = joblib.load(modele_type + '.joblib')

    test_predictions = modele.predict(df) # calcul des predictions sur le jeu de test

    df['Churn'] = pd.Series(test_predictions).replace(0,'No').replace(1,'Yes')

    return df

def return_df(data):

    test_data = pd.DataFrame([[
        data.gender
        ,data.SeniorCitizen
        ,data.Partner
        ,data.Dependents
        ,data.tenure
        ,data.PhoneService
        ,data.MultipleLines
        ,data.InternetService
        ,data.OnlineSecurity
        ,data.OnlineBackup
        ,data.DeviceProtection
        ,data.TechSupport
        ,data.StreamingTV
        ,data.StreamingMovies
        ,data.Contract
        ,data.PaperlessBilling
        ,data.PaymentMethod
        ,data.MonthlyCharges
        ,data.TotalCharges
        ]],columns=['gender','SeniorCitizen','Partner','Dependents','tenure','PhoneService','MultipleLines','InternetService','OnlineSecurity','OnlineBackup',
                    'DeviceProtection','TechSupport','StreamingTV','StreamingMovies','Contract','PaperlessBilling','PaymentMethod','MonthlyCharges','TotalCharges'])
    
    return test_data
    

    




import os
import requests

os.environ['LOG_CONTENT']="0"

r = requests.post(
   url='http://api_churn:8000/predict/RFC',auth=('alice', 'wonderland'),
   #url='http://0.0.0.0:8000/predict/RFC',auth=('alice', 'wonderland'),
    json={"gender":"Male","SeniorCitizen":"0","Partner":"Yes","Dependents":"Yes","tenure":72,"PhoneService":"Yes","MultipleLines":"Yes","InternetService":"DSL",
    "OnlineSecurity":"Yes","OnlineBackup":"No","DeviceProtection":"Yes","TechSupport":"Yes","StreamingTV":"Yes","StreamingMovies":"Yes","Contract":"Two year",
    "PaperlessBilling":"Yes","PaymentMethod":"Credit card (automatic)","MonthlyCharges":83.55,"TotalCharges":6093.3}
)

output = '''
============================
    Content test
============================

request done at "/predict/RFC"
| username="alice"
| password="wonderland"
| a good json input data

expected result = 200
actual restult = {status_code}

==>  {test_status}

'''


# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))
os.environ['LOG_CONTENT']="1"

# impression dans un fichier
if os.environ.get('LOG_CONTENT') == '1':
    with open('/LOG/api_test.log', 'a') as file:
        file.write(output)

#######################################################################################################################################################################

os.environ['LOG_CONTENT']="0"

r = requests.post(
    #url='http://0.0.0.0:8000/predict/RFC',auth=('alice', 'wonderland'),
    url='http://api_churn:8000/predict/RFC',auth=('alice', 'wonderland'),
    json={}
)

output = '''
============================
    Content test
============================

request done at "/predict/RFC"
| username="alice"
| password="wonderland"
| an empty json data

expected result = 422
actual restult = {status_code}

==>  {test_status}

'''


# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 422:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))

os.environ['LOG_CONTENT']="1"

# impression dans un fichier
if os.environ.get('LOG_CONTENT') == '1':
    with open('/LOG/api_test.log', 'a') as file:
        file.write(output)

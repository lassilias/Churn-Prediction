import os
import requests

os.environ['LOG_AUTHENTIFICATION']="0" #initialisation de la variable environnement avant le tests

r = requests.get(
    # url='http://127.0.0.1:8000/permissions',auth=('alice', 'wonderland')
    url='http://api_churn:8000/permissions', auth=('alice','wonderland')
)

output = '''
============================
    Authentication test
============================

request done at "/permissions"
| username="alice"
| password="wonderland"

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

os.environ['LOG_AUTHENTIFICATION']="1"
print (output.format(status_code=status_code, test_status=test_status))
# impression dans un fichier
if os.environ.get('LOG_AUTHENTIFICATION') == '1':
    with open('/LOG/api_test.log', 'a') as file:
#    with open('/LOG/api_test.log', 'a') as file:
        file.write(output)
###################################################################################################################################################################

os.environ['LOG_AUTHENTIFICATION']="0"

r = requests.get(
    #url='http://127.0.0.1:8000/permissions',auth=('bob', 'builder')
    url='http://api_churn:8000/permissions', auth=('bob', 'builder')
)

output = '''
============================
    Authentication test
============================

request done at "/permissions"
| username="bob"
| password="builder"

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
print (output.format(status_code=status_code, test_status=test_status))
os.environ['LOG_AUTHENTIFICATION']="1"

# impression dans un fichier
if os.environ.get('LOG_AUTHENTIFICATION') == '1':
    with open('/LOG/api_test.log', 'a') as file:
    #with open('/LOG/api_test.log', 'a') as file:
        file.write(output)

###################################################################################################################################################################
os.environ['LOG_AUTHENTIFICATION']="0"

r = requests.get(
    #url='http://127.0.0.1:8000/permissions',auth=('alice', 'builder')
    url='http://api_churn:8000/permissions', auth=('alice', 'builder')
)

output = '''
============================
    Authentication test
============================

request done at "/permissions"
| username="alice"
| password="builder"

expected result = 401
actual restult = {status_code}

==>  {test_status}

'''


# statut de la requête
status_code = r.status_code

# affichage des résultats
if status_code == 401:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print (output.format(status_code=status_code, test_status=test_status))
os.environ['LOG_AUTHENTIFICATION']="1"

# impression dans un fichier
if os.environ.get('LOG_AUTHENTIFICATION') == '1':
    with open('/LOG/api_test.log', 'a') as file:
   # with open('/LOG/api_test.log', 'a') as file:
        file.write(output)


import os
import requests
from requests.auth import HTTPBasicAuth


user_list_authorization=[
    {'nom':'alice','pwd':'wonderland','authorization':['oui']},
    {'nom':'bob','pwd':'builder','authorization':['oui']},
	{'nom':'tof','pwd':'tof','authorization':['non']}
]

# définition de l'adresse de l'API
api_address = os.environ.get('HOSTNAME')
# port de l'API
api_port = 8000
# requête

def autorisation(user,password,attendu):
    url='http://{address}:{port}/users/me'.format(address=api_address, port=api_port)
    print(url)
    r = requests.get(url, auth=HTTPBasicAuth(user, password))

#requests.get('https://www.instapaper.com/api/authenticate', auth=HTTPBasicAuth('username', 'password'))
    output = '''
============================
    Authorization test
============================

request done at "/users/me"
| username={username}
| password={pwd}

expected result = {test_attendu}
actual restult = {status_code}

==>  {test_status}

'''


# statut de la requête
    status_code = r.status_code

# affichage des résultats
    if status_code == attendu:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'


    mon_log=output.format(username=user,pwd=password,test_attendu=attendu,status_code=status_code, test_status=test_status)
    #print(output.format(username=user,pwd=password,test_attendu=attendu,status_code=status_code, test_status=test_status))
    print(mon_log)


# impression dans un fichier
    if os.environ.get('LOG') == '1':
        with open('api_test.log', 'a') as file:
            #file.write(output)
            file.write(mon_log)
			
		

def list_api(user,password,attendu):
    url='http://{address}:{port}/model/list'.format(address=api_address, port=api_port)
    print(url)
    r = requests.get(url, auth=HTTPBasicAuth(user, password))

#requests.get('https://www.instapaper.com/api/authenticate', auth=HTTPBasicAuth('username', 'password'))
    output = '''
============================
    Model List test
============================

request done at "/model/list"
| username={username}
| password={pwd}

expected result = {test_attendu}
actual restult = {status_code}

==>  {test_status}

'''


# statut de la requête
    status_code = r.status_code

# affichage des résultats
    if status_code == attendu:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'


    mon_log=output.format(username=user,pwd=password,test_attendu=attendu,status_code=status_code, test_status=test_status)
    #print(output.format(username=user,pwd=password,test_attendu=attendu,status_code=status_code, test_status=test_status))
    print(mon_log)


# impression dans un fichier
    if os.environ.get('LOG') == '1':
        with open('api_test.log', 'a') as file:
            #file.write(output)
            file.write(mon_log)

def test_api_score(user,password,mon_model,attendu):
    url='http://{address}:{port}/model/{mm}/score'.format(address=api_address, port=api_port,mm=mon_model)
    print(url)
    r = requests.get(url, auth=HTTPBasicAuth(user, password))

#requests.get('https://www.instapaper.com/api/authenticate', auth=HTTPBasicAuth('username', 'password'))
    output = '''
============================
    Model List test
============================

request done at "/model/{mmodel}/score
| username={username}
| password={pwd}

expected result = {test_attendu}
actual restult = {test_score}

==>  {test_status}

'''


# statut de la requête
    if r.status_code==200:
        test_score = r.json()['score']
    else:
        test_score=r.status_code
		

# affichage des résultats
    if test_score == attendu:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'


    mon_log=output.format(username=user,pwd=password,mmodel=mon_model,test_attendu=attendu,test_score=test_score, test_status=test_status)
    #print(output.format(username=user,pwd=password,test_attendu=attendu,status_code=status_code, test_status=test_status))
    print(mon_log)


# impression dans un fichier
    if os.environ.get('LOG') == '1':
        with open('api_test.log', 'a') as file:
            #file.write(output)
            file.write(mon_log)


for i in user_list_authorization:
    if 'oui' in i["authorization"]:
    
        autorisation(i["nom"],i["pwd"],200)
    else:
        autorisation(i["nom"],i["pwd"],403)


for i in user_list_authorization:
    if 'oui' in i["authorization"]:
    
        list_api(i["nom"],i["pwd"],200)
    else:
        list_api(i["nom"],i["pwd"],403)


for i in user_list_authorization:
    if 'oui' in i["authorization"]:
        test_api_score(i["nom"],i["pwd"],'knn',0.7724484104852203)
    else:
        test_api_score(i["nom"],i["pwd"],'knn',403)




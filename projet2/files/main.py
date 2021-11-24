# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 19:49:19 2021

@author: Christophe
"""

from fastapi import Depends, FastAPI, Response, HTTPException
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np
import json

import pickle


app = FastAPI()

security=HTTPBasic()


users = {
    'alice': 'wonderland',
    'bob': 'builder',
	'clementine':'mandarine',
	'tof':'taf'
	
}

docs_tags=[
	{
        'name': 'Modele',
        'description': 'Fonction d\'analyse des modèles'
    },
    {
        'name': 'Info_user',
        'description': 'Controle les droits d\'utilisation'
    },
    {
        'name': 'System',
        'description': 'Fonctions système pour l\'API'
    }
	
]


model_df=pd.DataFrame(np.array([
    ['knn','Knn','knn.model'],
    ['reglin','Regression Lineaire','RegressionLogistic.model'],
    ['svm','SVM', 'svm.model'],
    ['dt','DecisionTree', 'DecisionTree.model'],
    ['gb','GradientBoost', 'GradientBoost.model']
]),columns=['nom_court','nom', 'model'])



def authenticate_user(username, password):
    authenticated_user = False
    if username in users.keys():
        if users[username] == password:
            authenticated_user = True
    return authenticated_user





def prepa_data():
	myChurn=pd.read_csv("churn.csv")
	myChurn['TotalCharges'] = pd.to_numeric(myChurn.TotalCharges, errors='coerce')
	myChurn.dropna(subset = ["TotalCharges"], inplace=True)
	myChurn = pd.get_dummies(myChurn,columns=['gender','SeniorCitizen','Partner','Dependents','InternetService',
       'DeviceProtection', 
       'StreamingTV',
       'Contract','PhoneService',
        'MultipleLines','OnlineSecurity','OnlineBackup','TechSupport','StreamingMovies',
       'PaymentMethod','PaperlessBilling'],drop_first=True)
	myData=myChurn.drop(columns=['customerID'])
	X = myData.drop(columns = ['Churn'])
	y = myData['Churn'].values
	return X,y





@app.get("/",tags=['System'])
async def root():
    return {"message": "Hello World"}


@app.get("/users/me",tags=['info_user'])
def read_current_user(credentials: HTTPBasicCredentials= Depends(security)):
#def read_current_user(username:str=Depends(get_current_username)):
	"""
	Info dans la fonction

	Parameters
	----------
	credentials : HTTPBasicCredentials, optional
		DESCRIPTION. The default is Depends(security).

	Returns
	-------
	dict
		DESCRIPTION.

	"""
	droit=authenticate_user(credentials.username,credentials.password)
	if droit==False:
		HTTPException(status_code=403, detail="Non Autorisé")
	return {"username":credentials.username,"password":credentials.password,'droit':droit }

@app.get("/users/logout",tags=['info_user'])
def logout(response : Response):
	"""
	Fonction dé déconnexion de l\'utilisateur. La fonctionest non fonctionnelle pour le moment
	
	"""
  #response = RedirectResponse('*your login page*', status_code= 302)
#	response.delete_cookie("Authorization", domain="localtest.me")
	return {"message": "Deconnecté"}



@app.get('/status',tags=['System'])
async def return_status(credentials: HTTPBasicCredentials= Depends(security)):
    '''
    returns 1 if the app is up
    '''
    return 1

@app.get('/model/list',tags=['Modele'])
async def list_models(credentials: HTTPBasicCredentials= Depends(security)):
	"""
	Donne la liste des modèles disponibles

	Returns
	-------
	TYPE
		DESCRIPTION.

	"""
	droit=authenticate_user(credentials.username,credentials.password)
	if droit==False:
		raise HTTPException(status_code=403, detail="Non Autorisé")
#	if not authenticate_user(username=username, password=password):
#        raise HTTPException(status_code=403, detail='Authentication failed')
		
		
	r1=model_df.to_json(orient="records")
	r2=r1[1:-1]
	r3='{'+r2+'}'
	#parsed = json.loads(r2)
	result=json.dumps(r3)
	#json_compatible_item_data = jsonable_encoder(result)
	#return {r2}
	return Response(content=r1, media_type="application/json")


@app.get('/model/{nom_model}',tags=['Modele'])
async def get_model_info(nom_model,credentials: HTTPBasicCredentials= Depends(security)):
	"""
	Retourn des informations sur lemodèle

	Parameters
	----------
	nom_model : TYPE
		Nom court du modèle obtenu via la liste des modèles.

	Returns
	-------
	dict
		DESCRIPTION.

	"""
	droit=authenticate_user(credentials.username,credentials.password)
	if droit==False:
		raise HTTPException(status_code=403, detail="Non Autorisé")
	for index, row in model_df.iterrows():
		if row['nom_court']==nom_model:
			#result=row['nom']
			return {'nom modele':row['nom'],'nom court':row['nom_court'],'fichier de modele':row['model']}
	return None



@app.get('/model/{nom_model}/score',tags=['Modele'])

async def get_model_score(nom_model,credentials: HTTPBasicCredentials= Depends(security)):
	"""
	Retourne le score du modèledont le nom court est fourni dans l'URL'

	Parameters
	----------
	nom_model : TYPE
		Nom court du modèle obtenu via la liste des modèles.

	Returns
	-------
	score
		Score du modèle obtenu sur les données exemple.

	"""
	droit=authenticate_user(credentials.username,credentials.password)
	if droit==False:
		raise HTTPException(status_code=403, detail="Non Autorisé")
	result=""
	for index, row in model_df.iterrows():
		if row['nom_court']==nom_model:
			
			X,y=prepa_data()
			
			X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.30, random_state = 40, stratify=y)
			filename = row['model']
			loaded_model = pickle.load(open(filename, 'rb'))
			result = loaded_model.score(X_test, y_test)
			
	return {'modele':nom_model,'score':result}



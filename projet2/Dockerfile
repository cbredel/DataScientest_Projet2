FROM ubuntu:20.04

ADD files/requirements.txt files/main.py files/svm.model files/ada.model files/DecisionTree.model files/GradientBoost.model files/knn.model files/RandomForest.model files/RegressionLogistic.model files/churn.csv ./

RUN apt update && apt install python3-pip -y && pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0

Contains all files necessary to start Fastapi Churn Prediction: 

1) main.py contains api code.


2) fonctions.py contains functions used in main.py .


3) X_test.csv and y_test.csv are the Test Data.


4) joblib files are the trained models:

  KNC: KNeighborsClassifier
  RFC: RandomForestClassifier
  LR: LogisticRegression
  GB: GradientBoostingClassifier

5) credentials.csv contains credentials to authenticate in api.

6) start.sh is a script that create and activate a python environment, install requirements python packages and run api.

# -*- coding: utf-8 -*-
"""pulsares.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F41xou1Xocmh4jcKFOIqGGvjjXCXPR2h
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Basad en
 #https://www.kaggle.com/code/nguyenn95/playground-series-season-3-episode-10#Playground-Series---Season-3,-Episode-10---Solution
 #https://www.kaggle.com/code/iqbalsyahakbar/ps3e10-first-attempt-at-playground-competition
train_data_original = pd.read_csv("train.csv")
test_data_original = pd.read_csv("test.csv")
original = pd.read_csv("Pulsar.csv")

train_data = train_data_original.drop(columns=["id"])
test_data = test_data_original.drop(columns=["id"])

#Se necesita hacer la correcion
#segun https://www.kaggle.com/competitions/playground-series-s3e10/discussion/393588
train_data[['EK','Skewness','EK_DMSNR_Curve','Skewness_DMSNR_Curve']] = train_data[['Skewness','EK','Skewness_DMSNR_Curve','EK_DMSNR_Curve']]
original[['EK','Skewness','EK_DMSNR_Curve','Skewness_DMSNR_Curve']] = original[['Skewness','EK','Skewness_DMSNR_Curve','EK_DMSNR_Curve']]
test_data[['EK','Skewness','EK_DMSNR_Curve','Skewness_DMSNR_Curve']] = test_data[['Skewness','EK','Skewness_DMSNR_Curve','EK_DMSNR_Curve']]

train_data.drop(columns=['Class']).describe()

test_data.describe()

#Imprime la cantidad de valores faltantes
def get_missing_values(data):
    missing_values = data.isna().sum()
    return len(missing_values[missing_values > 0].sort_values() )
get_missing_values(train_data)

get_missing_values(test_data)

"""#Preprocesamiento"""

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score

X_train, X_valid, y_train, y_valid = train_test_split(train_data.drop(columns=["Class"]), train_data.Class, test_size=0.1)
skew_cols = X_train.columns[2: 6].to_list() + [X_train.columns[-1]]

def transform_to_normal_using_log(x):
    min_values = np.min(x)
    base_values = np.ceil(np.abs(min_values)) # prevent 0 or negative
    return np.log(x + base_values)


log_pipeline = make_pipeline(
    FunctionTransformer(transform_to_normal_using_log)
)
preprocessing = ColumnTransformer([
    ("log", log_pipeline, skew_cols)
], remainder=StandardScaler())
df = pd.DataFrame(preprocessing.fit_transform(X_train), columns=X_train.columns)

"""#Entrenamiento"""

X_train = pd.DataFrame(preprocessing.fit_transform(X_train), columns=X_train.columns)
X_valid = pd.DataFrame(preprocessing.transform(X_valid), columns=X_valid.columns)
def score_dataset(X_train, X_valid, y_train, y_valid, model):
    model.fit(X_train, y_train)
    return model.score(X_valid, y_valid)
default_models = {
    "Logistic Reg": LogisticRegression(),
    "Random Forest": RandomForestClassifier(),
    "SVC": SVC()
}
acc_scores = {}
for model_name, model in default_models.items():
    acc_scores[model_name] = {"mean accuracy": score_dataset(X_train, X_valid, y_train, y_valid, model)}

acc_scores

predictions = LogisticRegression().fit(X_train, y_train).predict(X_valid)
ConfusionMatrixDisplay(confusion_matrix(y_valid, predictions)).plot(cmap="Blues");
plt.show()

import pickle

# Supongamos que 'modelo' es tu modelo entrenado
modelo_entrenado = model

# Guardar el modelo en un archivo
with open('modelo_entrenado.pkl', 'wb') as archivo:
    pickle.dump(modelo_entrenado, archivo)


import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

data = pd.read_csv("../data/fraud_data.csv")

X = data[['amount']]
y = data['fraud']

model = DecisionTreeClassifier()
model.fit(X, y)

pickle.dump(model, open("fraud_model.pkl", "wb"))

print("Model trained successfully")
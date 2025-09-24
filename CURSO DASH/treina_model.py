from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score
import joblib

heart_disease = fetch_ucirepo(id=45)
dados = heart_disease.data.features

dados["doenca"] = (heart_disease.data.targets > 0) * 1

X = dados.drop(columns='doenca')
y = dados['doenca']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=432, stratify=y)

modelo = xgb.XGBClassifier(objective='binary:logistic')

modelo.fit(X_train, y_train)

preds = modelo.predict(X_test)

acuracia = accuracy_score(y_test, preds)
print(f'A acurácia do modelo é {acuracia:.2%}')

joblib.dump(modelo, 'modelo_xgboost.pkl')
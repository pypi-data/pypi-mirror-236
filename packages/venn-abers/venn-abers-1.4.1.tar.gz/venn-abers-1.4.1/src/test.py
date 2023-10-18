import pandas as pd
from src.venn_abers import VennAbersCalibrator
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier

data = {'X1':[7, 6, 5, 2, 5, 7, 3, 7, 2, 1, 5],
        'X2':[20, 21, 19, 18, 7, 12, 4, 12, 8, 3, 7],
        'X3' : [6.1, 5.9, 6.0, 6.1, 5, 23, 5.5, 6.1, 4.5, 5.1, 5.5],
        'X4' : ['a', 'b', 'a', 'c', 'a', 'b', 'b', 'a', 'c', 'b', 'a'],
        'y_label': ['M','N', 'F', 'F', 'N', 'F', 'F', 'M', 'N', 'N', 'F']
        }

df = pd.DataFrame(data)
X = df.iloc[:, :-1]
y = df.y_label.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)
clf = CatBoostClassifier(verbose=False)
va = VennAbersCalibrator(estimator=clf, inductive=True, cal_size=0.5, random_state=101)
va.fit(X_train, y_train)
p_prime = va.predict_proba(X_test)
y_prime = va.predict(X_test, one_hot=False)
print(X)
print(p_prime)

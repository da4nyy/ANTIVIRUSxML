# -*- coding: utf-8 -*-
"""antivirus-learning-phase.ipynb
"""

import numpy as np
import pandas as pd
import seaborn as sns
import sklearn.ensemble as ske
from sklearn.feature_selection import SelectFromModel
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn import utils
import joblib
import sys
import pickle
sys.modules['sklearn.externals.joblib'] = joblib



data = pd.read_csv('data.csv',sep="|")
data.head()


data.isnull().sum()

colomuns = ["LoaderFlags","NumberOfRvaAndSizes","SectionsNb","SectionsMeanEntropy","SectionsMinEntropy","SectionsMaxEntropy","SectionsMeanRawsize","SectionMaxRawsize","SectionsMeanVirtualsize","SectionsMinVirtualsize","SectionMaxVirtualsize","ImportsNbDLL","ImportsNb","ImportsNbOrdinal","ExportNb","ResourcesNb","ResourcesMeanEntropy","ResourcesMinEntropy","ResourcesMaxEntropy","ResourcesMeanSize","ResourcesMinSize","ResourcesMaxSize","LoadConfigurationSize","VersionInformationSize","legitimate"]
for c in colomuns:  
  m=round(data[c].mean(),2)
  data= data.fillna(m)

X = data.drop(['Name', 'md5', 'legitimate'], axis=1).values
y = data['legitimate'].values

data.dtypes

sns.countplot(x='legitimate', data=data);

ex = ExtraTreesClassifier()
lab = preprocessing.LabelEncoder()
y_transformed = lab.fit_transform(y)

fsel = ex.fit(X,y_transformed)
model = SelectFromModel(fsel, prefit=True)
X_new = model.transform(X)
nb_features = X_new.shape[1]

X_train, X_test, y_train, y_test = train_test_split(X_new, y ,test_size=0.2)

features = []

print('%i features identified as important:' % nb_features)

indices = np.argsort(fsel.feature_importances_)[::-1][:nb_features]
for f in range(nb_features):
    print("%d. feature %s (%f)" % (f + 1, data.columns[2+indices[f]], fsel.feature_importances_[indices[f]]))

for f in sorted(np.argsort(fsel.feature_importances_)[::-1][:nb_features]):
    features.append(data.columns[2+f])

algorithms = {
        "DecisionTree": DecisionTreeClassifier(max_depth=10),
        "RandomForest": RandomForestClassifier(n_estimators=50),
        "AdaBoost": AdaBoostClassifier(n_estimators=100),
        "GNB": GaussianNB()
    }

results = {}
accuracy_test = []
model = []
print("\nNow testing algorithms")
for algo in algorithms:
    clf = algorithms[algo]
    lab = preprocessing.LabelEncoder()
    y_transformed = lab.fit_transform(y_train)
    clf.fit(X_train, y_transformed)
    pred = clf.predict(X_test)
    score = clf.score(X_test, y_test)
    results[algo] = score
    print("%s : %f %%" % (algo, score*100))
    acc = accuracy_score(pred, y_test)
    accuracy_test.append(acc)
    print('Test Accuracy :\033[32m \033[01m {:.5f}% \033[30m \033[0m'.format(acc*100))
    print('\033[01m              Classification_report \033[0m')
    print(classification_report(y_test, pred))
    print('\033[01m             Confusion_matrix \033[0m')
    cf_matrix = confusion_matrix(y_test, pred)
    plot_ = sns.heatmap(cf_matrix/np.sum(cf_matrix), annot=True,fmt= '0.2%')
    plt.show()
    print('\033[31m###################- End -###################\033[0m')

winner = max(results, key=results.get)
print('\nWinner algorithm is %s with a %f %% success' % (winner, results[winner]*100))

# Save the algorithm and the feature list for later predictions
print('Saving algorithm and feature list in classifier directory...')
joblib.dump(algorithms[winner], 'classifier.pkl')
open('features.pkl', 'bw').write(pickle.dumps(features))
print('Saved')

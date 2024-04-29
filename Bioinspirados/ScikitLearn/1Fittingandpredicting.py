#Fitting and predicting: estimator basics
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(random_state =0 )
X = [[1,2,3],[11,12,13]]
Y = [0,1]
clf.fit(X,Y)
predict = clf.predict(X)
print(predict)
predictNewData = clf.predict([[4,5,6],[14,15,16]])
print(predictNewData)



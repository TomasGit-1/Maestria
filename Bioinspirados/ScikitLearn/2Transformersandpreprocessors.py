from sklearn.preprocessing import StandardScaler

X = [[0,15], [1,-10]]
#Scale date according t computed scaling values 
predict = StandardScaler().fit(X).transform(X)
print(predict)

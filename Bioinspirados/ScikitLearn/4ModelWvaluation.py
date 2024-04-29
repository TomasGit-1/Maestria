from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate


X, y = make_regression(n_samples=100, random_state=0)
lr = LinearRegression()
result = cross_validate(lr, X, y) 
test = result['test_score']
print(test)
import numpy as np

class LinearRegression:
    def __init__(self, lr=0.01, num_iters=1000):
        self.lr = lr
        self.num_iters = num_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        # Initialize weights and bias to zeros
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        # Gradient descent
        for _ in range(self.num_iters):
            y_pred = np.dot(X, self.weights) + self.bias
            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        y_pred = np.dot(X, self.weights) + self.bias
        return y_pred
    
    #MSE AND RMSE   
    def mse(self, y_true, y_pred):
        return np.mean((y_true - y_pred)**2)
    
    def rmse(self, y_true, y_pred):
        return np.sqrt(np.mean((y_true - y_pred)**2))


    
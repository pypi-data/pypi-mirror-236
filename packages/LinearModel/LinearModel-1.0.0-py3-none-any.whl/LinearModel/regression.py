import numpy as np

class LinearModel:

    def __init__(self,instruction_count: int=1000,learning_rate: int=0.001,regularization_parameter: int=0):
        self.ic = instruction_count
        self.alpha = learning_rate
        self.lamda = regularization_parameter
        self.w = None
        self.b = None

    def cost(w:np.ndarray, b:float, x:np.ndarray, y:np.ndarray) -> float:
        """
            - #### computes the root mean squared error

            w: one by n matrix represents the weights
            b: a number represents the bias
            x: an m by n matrix,represents a dataset with m examples and n features
            y: a one by m matrix,represents the target vector
        """
        y_hat = np.dot(w, x.T) + b
        diff = np.power(y_hat - y, 2)
        mean = diff.mean()
        rmse = np.sqrt(mean)
        return rmse
    
    def __gradient__(w:np.ndarray, b:np.float64, x:np.ndarray, y:np.ndarray, lamda:float = 0) -> tuple[np.ndarray, float]:
        """
            - #### computes the derivatives of the squared error with respect to w and b

            w: one by n matrix represents the weights
            b: a number represents the bias
            x: an m by n matrix,represents a dataset with m examples and n features
            y: a one by m matrix,represents the target vector
            lamda: the regularization parameter
        """
        m = x.shape[0]
        dj_db = np.dot(w, x.T) + b - y # this is now a one by m matrix
        dj_dw = np.dot(dj_db, x) - lamda * w # one by n matrix
        dj_db = dj_db.mean()
        dj_dw = dj_dw / m
        return dj_dw, dj_db
    
    def fit(self, x:np.ndarray,y:np.ndarray,w_in: np.ndarray=None,b_in: float=0) -> tuple[np.ndarray, float]:
        """
            - #### computes the weights vector w and the bias b

            w_in: one by n matrix represents the weights
            b_in: a number represents the bias
            x: an m by n matrix,represents a dataset with m examples and n features
            y: a one by m matrix,represents the target vector
        """
        n = x.shape[1]

        if w_in is None:
            w_in = np.zeros(shape=(1,n))

        w = w_in
        b = b_in
        
        for _ in range(self.ic):
            dj_dw, dj_db = LinearModel.__gradient__(w, b, x, y)
            w = w - dj_dw
            b = b - dj_db

        self.w = w
        self.b = b

        return w,b
    
    def predict(self, x):
        if self.w is None or self.b is None:
            raise Exception("fit was not called")
        return np.dot(self.w, x.T) + self.b
    
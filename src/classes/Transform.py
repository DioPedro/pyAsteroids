import numpy as np

class Transform:
    def __init__(self):
        pass

    @staticmethod
    def translate(t_x, t_y):
        return np.array([1.0, 0.0, 0.0, t_x, 
                         0.0, 1.0, 0.0, t_y, 
                         0.0, 0.0, 1.0, 0.0, 
                         0.0, 0.0, 0.0, 1.0], np.float32)

    @staticmethod
    def rotate(angle):
        cos = np.cos(angle)
        sin = np.sin(angle)
        return  np.array([cos, -sin, 0.0, 0.0, 
                          sin,  cos, 0.0, 0.0, 
                          0.0, 0.0, 1.0, 0.0, 
                          0.0, 0.0, 0.0, 1.0], np.float32)

    @staticmethod
    def scale(s_x, s_y):
        return np.array([s_x, 0.0, 0.0, 0.0,
                         0.0, s_y, 0.0, 0.0,
                         0.0, 0.0, 1.0, 0.0,
                         0.0, 0.0, 0.0, 1.0], np.float32)
    @staticmethod
    def stack(tranformations):
        tranformations = reversed(tranformations)

        finalTransformation = tranformations[0].reshape(4, 4)
        for i in range(1, len(tranformations)):
            finalTransformation = np.dot(finalTransformation, tranformations[i].reshape(4, 4))

        return finalTransformation

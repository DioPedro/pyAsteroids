from typing import List, Tuple, Callable
import numpy as np    

def NAV_PATH(amplitude: float, x: float):
    return amplitude * (np.sin(2 * x) + (np.sin(6 * x) / 4))

def AMONG_PATH(a: int, b: int, x: float):
    return (a * b / np.sqrt((b * np.cos(x)) ** 2 + (a * np.sin(x) ** 2)))

def curvePath(equation: Callable[[Tuple[int, ...]], int], args: Tuple[float, ...]):
    rads = np.arange(0, (2 * np.pi), 0.005)
    amplitude = 10
    points = []
    for rad in rads:
        r = equation(*args, rad)
        points.append([r * np.cos(rad), r * np.sin(rad)])
    return points

class Path:
    def __init__(self, 
                 points: List[Tuple[float, float]], 
                 start: int):
        self.points = points
        self.position = start
    
    def increment(self):
        self.position = (self.position + 1) % len(self.points)
    
    def atPosition(self):
        return self.points[self.position]
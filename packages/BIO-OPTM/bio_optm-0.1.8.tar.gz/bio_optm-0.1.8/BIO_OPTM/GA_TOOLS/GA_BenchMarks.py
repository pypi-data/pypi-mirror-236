""" Collection of functions and visualizers for optimal solution testing testing
    See this link for some of the functions detailed here: 
    * https://en.wikipedia.org/wiki/Test_functions_for_optimization#Test_functions_for_constrained_optimization
"""

import numpy as np 
import matplotlib.pyplot as plt

#######################################################
# 
#      Optimization Functions
# 
#######################################################
class OptimizationTester:
    def __init__(self, Function, optimalInput, optimalValue, **kwargs):
        self.Function=Function
        self.optimalInput=optimalInput
        self.optimalValue=optimalValue
    

    def Function(self, solution, **kwargs):
        return solution

    def getOptimalInput(self, ):
        return self.optimalInput
    
    def getOptimalValue(self, ):
        return self.optimalValue


class BoothFunction(OptimizationTester):
    def __init__(self, Function, optimalInput=[0,1], optimalValue={"min":0, "max":1200}, **kwargs):
        super().__init__(Function, optimalInput, optimalValue, **kwargs)

    def solve(self, solution):
        return self.Function(boothFunction(solution))


def boothFunction(XY):
    x = XY[0]
    y = XY[1]
    return (x+2*y-7)**2 + (2*x+y-5)**2



#######################################################
# 
#      Visualizers
# 
#######################################################
def  FunctionVisualizer( Function=BoothFunction, optima=[-10, 10], verbose=False, Title="Title",
                            window=[200, 200], dimensions=2, labelsize=80, fontsize=80, fontdict={"size":60}):
    """Visualizes the solution space"""
    vs = np.linspace(-10, 10, window[0])
    vs = list(range(-10, 11))
    imgArray = np.zeros([len(vs), len(vs)])
    
    optima = -np.inf
    print(vs)
    for r in range(window[0]):
        for c in range(window[1]):
            x = vs[r]
            y = vs[c]
            # imgArray[r,c] = BoothFunction([x,y])
            imgArray[r,c] = Function.solve([x,y])
            
    data = imgArray
    if verbose:
        try:
            display(data)
        except Exception as ex:
            print(data)

    fig, ax = plt.subplots(1, figsize=window)
    im = ax.imshow(data, interpolation='nearest')
    ax.set_title(Title)
    cbar = ax.figure.colorbar(im, ax = ax)
    cbar.ax.set_ylabel("Color bar", rotation = -90, va = "bottom")
    
#     cbar.set_xticklabels(cbar.get_xticks(), fontdict={"size":20})
#     cbar.set_label(label='a label',weight='bold', fontsize=200)
    
    # plt.show() 
    cbar.ax.tick_params(labelsize=labelsize) 
    cbar.ax.set_title('Your Label',fontsize=fontsize)

    
    ax.set_xticks([v for v in range(len(vs))])
    ax.set_xticklabels([str(v) for v in vs], fontdict={"size":60})
    plt.show()
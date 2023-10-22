"""Collection of environment managers to test different optimization algorithms on. 
   They will utilize a given OptimizerAgent manager and call their solve and other relevant functions
"""
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt


class ENV_Manager:
    """Runs the game/environment that the Optimizer agents will have to exist in. 
    It is the framework through with the GA agent will go through the algorithm and store performance metrics and such 
    """
    def __init__(self, agentManager, epochs, **kwargs) -> None:
        self.agentManager=agentManager            # managers the population/optimizer agent(s)
        self.epochs=epochs
        self.kwargs=kwargs
        self.bestSolution= None
        self.bestScore = None
        self.avgScores = list()
        self.scores = list()       # stores each generations scores to be averaged and stored in the above
        self.probs = dict()         # key=chromosome number, value=probability of selection for pairing 


    def performTask(self, ):
        self.evaluateSolutions()
        self.improveSolutions()

    def evaluateSolutions(self,):
        return    
        
    def improveSolutions(self,):
        return
    
    
    


class GA_ENV(ENV_Manager):
    def __init__(self, agentManager, generations: int, 
                 patienceLimit=np.inf, 
                 **kwargs) -> None:
        super().__init__(agentManager, generations, **kwargs)
        
        self.generations=generations
        self.bestGeneration = 0
        self.generation=0
        self.endEarly = False
        self.patience=0
        self.patienceLimit = patienceLimit


    def Solve(self, verbose=False, interval=0):
        self.endEarly = False
        self.generation = 0
        self.agentManager.init()
        print(f"Generations: {self.generations}")
        while self.generation < self.generations and not self.endEarly:
            self.TestSolutions()          # get scores for each solution
            self.SurvivalOfTheFittest()
            self.RecordPerformance()       # rank, adjust them as needed, and sort
            self.generation += 1
            if verbose and self.generation%interval == 0:
                print(f"Generation: {self.generation}/{self.generations}")
                self.getBest()
                
            

    def TestSolutions(self,):
        self.scores.clear()
        # generate scores for each agents solutions
        for c in range(self.agentManager.population_size):
            score = self.agentManager.objective_function(self.agentManager.chromosomes[c])
            self.agentManager.observePerformance(c, score)  # store this score related to this agent in the manger
            self.scores.append(score)
        self.avgScores.append(np.max(self.scores))
    
    def SurvivalOfTheFittest(self,):
        # perform the score ranking/adjustment, and sorting. then do the pair section and breeding
        self.agentManager.survivalOfTheFittest()  


    def RecordPerformance(self,):
        # after the above the best current score and solution is stored
        if np.array_equal(self.bestSolution, self.agentManager.best_performance):
            self.patients += 1
        else:
            self.patients = 0

        if self.bestScore is not None and self.bestScore != self.agentManager.assessor(self.bestScore, self.agentManager.best_performance):
            self.bestGeneration = self.generation
        
        self.bestScore = self.agentManager.best_performance
        self.bestSolution = self.agentManager.best_solution

        

        # logic to stop at convergence
        if self.patience > self.patienceLimit:
            self.endEarly = True
            print(f"Ending due to convergence at {self.patience} repeated best solutions")

    def getBest(self, verbose=True):
        print(f"\t\tBest Solution: {self.bestSolution}\n\t\tGeneration: {self.bestGeneration}\n\t\tScore:{self.bestScore}")
        return self.bestScore, self.bestScore
    
    def plot_scores(self, title="Title", figsize=(10, 10), fontdictT={"size":10}, fontdictY={}, fontdictX={}):
        f, ax = plt.subplots(1, figsize=figsize)
        ax.plot(self.avgScores)
        ax.set_title(title, fontdict=fontdictT)
        ax.set_xticklabels(ax.get_xticks(), fontdict=fontdictX)
        ax.set_yticklabels(ax.get_yticks(), fontdict=fontdictY)
        ax.set_xlabel("Generations", fontdict=fontdictT)
        ax.set_ylabel("Average Objective", fontdict=fontdictT)


class GA_TSP_ENV(GA_ENV):
    def __init__(self, agentManager, generations: int, patienceLimit=np.inf, **kwargs) -> None:
        super().__init__(agentManager, generations, patienceLimit, **kwargs)

    def TestSolutions(self,):
        self.scores.clear()
        # generate scores for each agents solutions
        for c in range(self.agentManager.population_size):
            score = self.agentManager.objective_function(self.agentManager.chromosomes[c], self.agentManager.adjacencyMat)
            self.agentManager.observePerformance(c, score)  # store this score related to this agent in the manger
            self.scores.append(score)
        self.avgScores.append(np.max(self.scores))
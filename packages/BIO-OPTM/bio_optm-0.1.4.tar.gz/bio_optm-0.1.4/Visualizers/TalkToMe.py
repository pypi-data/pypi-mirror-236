import  numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class TheHand:
    def __init__(self, name="", **kwargs) -> None:
        self.name = name
        self.kwargs = kwargs
        self.imagePath, self.imageList = self.processKwargs()

        
    def processKwargs(self, ):
        return self.kwargs['path'], self.kwargs["images"]
        
    
    def grabHold(self):
        say = ""
        while say.lower() != "talk to me":
            say = input("Say it!")
        
        # intialize spirit link
        img = np.random.randint(0, len(self.ImageList), 1)[0]
        ghostImage = self.imageList[img]
        
        # show spirit:
        ghostImage = mpimg.imread(ghostImage)
        imgplot = plt.imshow(ghostImage)
        plt.show()
        
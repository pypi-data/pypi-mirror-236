import pandas as pd
import numpy as np 



class PandasTool:
    def __init__(self, ) -> None:
        pass

    def smartOpener(filepath, **kwargs):
        if filepath.endswith(".csv"):
            print("csv")
            return pd.read_csv(filepath, **kwargs)
        return

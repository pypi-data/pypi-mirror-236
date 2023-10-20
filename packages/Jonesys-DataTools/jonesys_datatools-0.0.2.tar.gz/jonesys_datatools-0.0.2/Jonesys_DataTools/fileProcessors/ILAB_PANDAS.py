import pandas as pd
import numpy as np 

def smartOpener(filepath, **kwargs):
        if filepath.endswith(".csv"):
            print("csv")
            return pd.read_csv(filepath, **kwargs)
        elif filepath.endswith("xlsx") or filepath.endswith("xlsx"):
            return pd.read_excel(filepath, **kwargs)
        return

class PandasTool:
    def __init__(self, ) -> None:
        pass

    def smartOpener(self, filepath, **kwargs):
        if filepath.endswith(".csv"):
            print("csv")
            return pd.read_csv(filepath, **kwargs)
        elif filepath.endswith("xlsx") or filepath.endswith("xlsx"):
            return pd.read_excel(filepath, **kwargs)
        return

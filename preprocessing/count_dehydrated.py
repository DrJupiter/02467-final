
import os

import matplotlib.pyplot as plt
from glob import glob
from pathlib import Path

code_path = Path(os.getcwd())
path = code_path.joinpath('./data/complete/')

def dehydrated(path):

    subfolders = [ f.path for f in os.scandir(path) if f.is_dir() ]

    total = []
    for path in subfolders:
        total.append(0)
        for filename in os.listdir(path):
            with open(path+ "\\" + filename, 'r', encoding="latin-1") as fileObj:
                # -1 to exclude the header
                total[-1] += len(fileObj.readlines()) #not -1 since no header
                #print("Rows Counted {} in the csv {}:".format(len(fileObj.readlines()) - 1, filename))  
    return total
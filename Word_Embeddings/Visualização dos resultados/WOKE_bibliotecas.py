import time
import joblib
import os
from random import randint, random
import sys
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from google.colab import output
from google.colab import drive
drive.mount('/content/drive')
import pandas as pd
from animate_plot_example import create_graph_video
import matplotlib.pyplot as plt
import os

from numpy import arange

aluminum_data = pd.read_csv('Datasets/aluminum.csv')
ptfe_data = pd.read_csv('Datasets/ptfe.csv')
brass_data = pd.read_csv('Datasets/brass.csv')
lowcarbon_data = pd.read_csv('Datasets/lowcarbon.csv')
stainless_steel_data = pd.read_csv('Datasets/stainless_steel.csv')

brass_force_data = pd.to_numeric(brass_data['Force'][2:]).values
print(max(brass_force_data))


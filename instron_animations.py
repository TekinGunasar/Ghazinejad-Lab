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

force_ss_steel = pd.to_numeric(stainless_steel_data['Force'][2:])
displacement_ss_steel = pd.to_numeric(stainless_steel_data['Displacement'][2:])
strain_ss_steel = pd.to_numeric(stainless_steel_data['Strain 1'][2:])
stress_ss_steel = force_ss_steel*21

plt.scatter(strain_ss_steel,stress_ss_steel)
plt.show()

#displacement_lc_steel= list(pd.to_numeric(lowcarbon_data['Displacement'][2:]))
#force_lc_steel = pd.to_numeric(lowcarbon_data['Force'][2:])
#strain_lc_steel = pd.to_numeric(lowcarbon_data['Strain 1'][2:])
#stress_lc_steel = force_lc_steel*20

#plt.scatter(strain_lc_steel,stress_lc_steel)
#plt.show()

#displacement_polymer = list(list(pd.to_numeric(polymer_data['Displacement'][2:])))
#displacement_polymer = list(list(pd.to_numeric(polymer_data['Displacement'][2:])))
#strain_polymer = list(list(pd.to_numeric(polymer_data['Strain 1'][2:])))

#stress_polymer = force_polymer*10
#plt.scatter(strain_polymer,stress_polymer,c='g')
#plt.show()

#plt.xlabel('Displacement[mm]')
#plt.ylabel('Force[kN]')
#plt.scatter(displacement_polymer,force_polymer)
#plt.show()


#aluminum_data = pd.read_csv('Datasets/aluminum.csv')

#force = pd.to_numeric(aluminum_data['Force'][10:])
#displacement = list(list(pd.to_numeric(aluminum_data['Displacement'][10:])))
#strain = pd.to_numeric(aluminum_data['Strain 1'][10:])

#stress = force*26.204564666103128

#plt.scatter(displacement,force)
#plt.xlabel('Displacement[mm]')
#plt.ylabel('Force[kN]')
#plt.show()

#plt.scatter(strain,stress)
#plt.xlim(-0.005,max(strain)+0.005)
#plt.show()

#num_frames_per = 1
#frames_directory = 'Animation Frames/Aluminum'
#final_directory = './'

#create_graph_video(strain,stress,num_frames_per,frames_directory,final_directory)

import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import pandas as pd

from math import floor
import json


def create_graph_video(settings_file):

    settings = json.loads(open(settings_file,'r').read())['plot settings']
    data = pd.read_csv(settings['csv_file_path'])

    if not os.path.exists(settings['frames directory']):
        os.mkdir(settings['frames directory'])

    if not os.path.exists(settings['movie directory']):
        os.mkdir(settings['movie directory'])

    for frame in os.listdir(settings['frames directory']):
        os.remove(os.path.join(settings['frames directory'],frame))

    force_data = pd.to_numeric(data['Force'][2:]).values
    displacement_data = pd.to_numeric(data['Displacement'][2:]).values

    strain_data = pd.to_numeric(data['Strain 1'][2:]).values
    stress_data = force_data * float(settings['stress conversion factor'])

    max_force = max(force_data) + int(max(force_data)/6)
    max_stress = max(stress_data) + 40

    num_data_points = len(force_data)
    with imageio.get_writer(os.path.join(settings['movie directory'],settings['movie name']), mode='?') as writer:
        for i in range(num_data_points):

            fig, axs = plt.subplots(3, 1)
            fig.suptitle(settings['material'])

            axs[0].scatter(displacement_data[0:i], force_data[0:i], c='g')
            axs[0].set_title('Force v.s Displacement')
            axs[0].set_xlabel('Displacement(mm)')
            axs[0].set_ylabel('Force (kN)')
            axs[0].set_ylim(0,max_force)

            axs[2].scatter(strain_data[0:i], stress_data[0:i], c='b')
            axs[2].set_title('Stress v.s Strain')
            axs[2].set_xlabel('Strain')
            axs[2].set_ylabel('Stress (MPa)')
            axs[2].set_ylim(0,max_stress)

            fig.delaxes(axs[1])

            plt.subplots_adjust(hspace= -0.05)
            plt.savefig(os.path.join(settings['frames directory'],f'frame-{i}.png'))
            plt.close()

            image = imageio.imread(os.path.join(settings['frames directory'],f'frame-{i}.png'))
            [writer.append_data(image) for iter in range(int(settings['num frames per']))]

if __name__ == '__main__':
    settings = 'settings_files/hcs_settings.json'
    create_graph_video(settings)



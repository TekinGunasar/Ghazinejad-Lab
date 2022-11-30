import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

from math import floor

def create_graph_video(x,y,num_frames_per,frames_directory,final_directory):

    y_max = max(y+30)
    x_max = max(x+0.1)
    for i in range(2, len(x)+1):
        plt.scatter(x[0:i],y[0:i],c='purple')
        plt.xlim(0,x_max)
        plt.ylim(0, y_max)
        plt.title('Tensile Stress v.s Tensile Strain - Aluminum')
        plt.xlabel('Tensile Strain (Displacement) [%]')
        plt.ylabel('Tensile Stress [MPa]')
        plt.savefig(f'{frames_directory}\line-{i}.png')
        plt.close()

    with imageio.get_writer('line.mov', mode='?') as writer:
        for i in range(2, len(x)+1):
            image = imageio.imread(f'{frames_directory}\line-{i}.png')
            [writer.append_data(image) for iter in range(num_frames_per)]

if __name__ == '__main__':
    size = 100

    x = np.arange(0,10,step=0.05)
    y = [x_i**2 for x_i in x]
    num_frames_per = 1
    final_directory ='./'
    frames_directory = 'Animation Frames\Aluminum'
    create_graph_video(x,y,num_frames_per,frames_directory,final_directory)

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


def get_force_data(data_path):
    data = pd.read_csv(data_path)
    force_data = pd.to_numeric(data['Force'][2:]).values

    return force_data

def get_strain_data(data_path):
    data = pd.read_csv(data_path)
    force_data = pd.to_numeric(data['Strain 1'][2:]).values

    return force_data

def get_displacement_data(data_path):
    data = pd.read_csv(data_path)
    force_data = pd.to_numeric(data['Displacement'][2:]).values

    return force_data

def get_stress_conversion_factor(data_path,uts):

    data = pd.read_csv(data_path)
    force_data = get_force_data(data_path)

    return uts/max(force_data)

def plot_force_displacement(data_path,material):
    force_data = get_force_data(data_path)
    displacement_data = get_displacement_data(data_path)

    plt.xlabel('Displacement(mm)')
    plt.ylabel('Force(kN)')
    plt.title(f'Force v.s Displacement: {material}')
    plt.scatter(displacement_data,force_data)
    plt.show()

def plot_strain_displacement(data_path,material):
    strain_data = get_strain_data(data_path)
    displacement_data = get_displacement_data(data_path)

    plt.xlabel('Displacement(mm)')
    plt.ylabel('Strain(kN)')
    plt.title(f'Strain v.s Displacement: {material}')
    plt.scatter(displacement_data,strain_data)
    plt.show()

def plot_stress_strain(data_path,material,uts):
    force_data = get_force_data(data_path)
    strain_data = get_strain_data(data_path)

    stress_conversion_factor = get_stress_conversion_factor(data_path,uts)
    stress_data = force_data * stress_conversion_factor

    plt.xlabel('Strain')
    plt.ylabel('Stress(MPa)')
    plt.title(f'Stress v.s Strain: {material}')
    plt.scatter(strain_data, stress_data)
    plt.show()

def plot_both(data_path,material,uts):
    force_data = get_force_data(data_path)
    displacement_data = get_displacement_data(data_path)
    strain_data = get_strain_data(data_path)

    stress_conversion_factor = get_stress_conversion_factor(data_path,uts)
    stress_data = force_data * stress_conversion_factor

    fig, axs = plt.subplots(3, 1)
    fig.suptitle(material)

    axs[0].set_title('Force v.s Displacement')
    axs[0].set_xlabel('Displacement (mm)')
    axs[0].set_ylabel('Force (kN)')
    axs[0].scatter(displacement_data,force_data,c='b')

    axs[2].set_title('Stress v.s Strain')
    axs[2].set_xlabel('Strain')
    axs[2].set_ylabel('Stress (MPa)')
    axs[2].scatter(strain_data,stress_data,c='g')

    fig.delaxes(axs[1])

    plt.subplots_adjust(hspace= -0.05)
    plt.show()


if __name__ == '__main__':

    data_hcs = 'Datasets/brass.csv'
    uts_abs = 400

    print(get_stress_conversion_factor(data_hcs,uts_abs))




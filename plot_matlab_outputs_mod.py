# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 11:48:31 2025

@author: Rutvija
"""

import os

import pandas as pd

import matplotlib.pyplot as plt

from matplotlib.cm import viridis

import matplotlib as mpl

import numpy as np

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

mpl.use('SVG')

mpl.rcParams['svg.fonttype'] = 'none'  # Do not convert fonts to paths

 

 

# Define the path to the datasets folder

folder_path = r"E:\07012025\changing the discharge gap\21kV"

base_plot_directory = folder_path

pca_plots_directory = os.path.join(base_plot_directory, "PCA plots")

 

# Create "PCA plots" subfolder if it doesn't exist

if not os.path.exists(pca_plots_directory):

    os.mkdir(pca_plots_directory)

 

 

cmap = viridis

num_colors = 11  # Number of colors needed

colors = cmap(np.linspace(0, 1, num_colors))

 

color_map = {f'PC {i}': colors[i - 1] for i in range(1, num_colors + 1)}

 

 

def create_variance_plot(df, title, subsubfolder_path):

    fig, ax = plt.subplots(figsize=(6, 4.5))

    df.iloc[:16].plot(y="% Variance", legend=False, ax=ax, marker='o', linestyle='-', markersize=4)

    ax.set_xlabel("PCs")

    ax.set_ylabel("% Variance")

    plt.xticks([0, 2, 4])

    plt.xlim(0, 11)

    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)

  

    # Add an inset

    inset_ax = inset_axes(ax, width="70%", height="60%", loc='center right', borderpad=0.5)

    inset_ax.plot(df.iloc[2:11].index, df.iloc[2:11]["% Variance"], marker='o', linestyle='-', markersize=4)

    inset_ax.set_xlim(2, 11)

    save_plots(title, subsubfolder_path)

 

def create_score_plot(df, title, subsubfolder_path, range_start, range_end, start_index, fontsize=18):

    columns_to_plot = df.columns[range_start:range_end]

    legend_labels = [f"PC {i}" for i in range(start_index, start_index + len(columns_to_plot))]

 

    fig, ax = plt.subplots(figsize=(8.3, 11.7))

    y_axis_separation = 0.5

    for i, (column, label) in enumerate(zip(columns_to_plot, legend_labels)):

        if i < 11:  # Only plot the first 10 PCs

            plt.plot(df.index, df[column] - (i * y_axis_separation), color=color_map[label], label=label)

    plt.yticks(fontsize=18)

    plt.xlabel("Time (s)", fontsize=18)

    plt.ylabel("Score (a.u.)", fontsize=18)

    plt.legend(fontsize=18)

    plt.tick_params(axis='both', labelsize=18)

    plt.title(title, fontsize=18)  # Add this line to set the title font size

#    plt.xlim(0, 4500)

    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)

    # # Add an inset

    # inset_ax = inset_axes(ax, width="50%", height="40%", loc='center right', borderpad=0.5)

    # inset_ax.plot(df.index, df[column] - (i * y_axis_separation), color=color_map[label], label=label)

    # inset_ax.set_xlim(0, 160)

   

    save_plots(title, subsubfolder_path)

 

def create_eigenspectra_plot(df, title, subsubfolder_path, range_start, range_end, start_index, fontsize=18):

    columns_to_plot = df.columns[range_start:range_end]

    legend_labels = [f"PC {i}" for i in range(start_index, start_index + len(columns_to_plot))]

 

    fig, ax = plt.subplots(figsize=(8.3, 11.7))

    for i, (column, label) in enumerate(zip(columns_to_plot, legend_labels)):

        if i < 11:  # Only plot the first 10 PCs

            plt.plot(df.iloc[:, 0], df[column] - (i * 0.1), color=color_map[label], label=label)

    plt.yticks(fontsize=18)

    plt.xlabel("Wavenumbers (cm$^{-1}$)", fontsize=18)

    plt.ylabel("Loading (a.u.)", fontsize=18)

    plt.legend(fontsize=18)

    plt.tick_params(axis='both', labelsize=18)

    plt.title(title, fontsize=18)  # Add this line to set the title font size

#    plt.xlim(4000, 650)

    save_plots(title, subsubfolder_path)

 

 

 

def save_plots(title, subsubfolder_path):

    figure_path = os.path.join(subsubfolder_path, title + ".png")

    #eps_path = os.path.join(subsubfolder_path, title + ".eps")

    svg_path = os.path.join(subsubfolder_path, title + ".svg")

 

    plt.savefig(figure_path, dpi=300)

    #plt.savefig(eps_path, format='eps')

    plt.savefig(svg_path, format='svg', transparent=True)

    plt.close()

 

 

 

# Iterate through each subfolder

for root, dirs, files in os.walk(folder_path):

    for file in files:

        if file == "PCA_CVE.txt":

            file_path = os.path.join(root, file)

            df = pd.read_csv(file_path, header=None, names=["% Variance"])

            zero_row = pd.DataFrame([[0]], columns=["% Variance"])

            df = pd.concat([zero_row, df], ignore_index=True)

            title = os.path.splitext(file)[0]

            subsubfolder = os.path.basename(root)

            subsubfolder_path = os.path.join(pca_plots_directory, subsubfolder)

            if not os.path.exists(subsubfolder_path):

                os.mkdir(subsubfolder_path)

            create_variance_plot(df, title + f"1_to_{num_colors}", subsubfolder_path)

    for file in files:

        if file == "PCA_scores.txt":

            file_path = os.path.join(root, file)

            df = pd.read_csv(file_path, delimiter="\t")

            title = os.path.splitext(file)[0]

            subsubfolder = os.path.basename(root)

            subsubfolder_path = os.path.join(pca_plots_directory, subsubfolder)

            if not os.path.exists(subsubfolder_path):

                os.mkdir(subsubfolder_path)

            #create_score_plot(df, title + "1_to_3", subsubfolder_path, 1, 4, 1)

            #create_score_plot(df, title + "4_to_20", subsubfolder_path, 5, 22, 4)

            create_score_plot(df, title + f"1_to_{num_colors}", subsubfolder_path, 1, 11, 1)

          

    for file in files:

        if file == "PCA_eigenspectra.txt":

            file_path = os.path.join(root, file)

            df = pd.read_csv(file_path, delimiter="\t")

            title = os.path.splitext(file)[0]

            subsubfolder = os.path.basename(root)

            subsubfolder_path = os.path.join(pca_plots_directory, subsubfolder)

            if not os.path.exists(subsubfolder_path):

                os.mkdir(subsubfolder_path)

            #create_eigenspectra_plot(df, title + "1_to_3", subsubfolder_path, 1, 4, 1)

            #create_eigenspectra_plot(df, title + "4_to_20", subsubfolder_path, 5, 22, 4)

            create_eigenspectra_plot(df, title + f"1_to_{num_colors}", subsubfolder_path, 1, 11, 1)

           

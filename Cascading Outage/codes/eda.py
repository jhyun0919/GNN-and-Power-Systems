from datetime import time
import pandas as pd
from os import path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob
import networkx as nx


def show_ps_graph(case_name, save_fig=False):
    bus = pd.read_csv("../datasets/ps/" + case_name + "/bus.csv", header=None)
    branch = pd.read_csv("../datasets/ps/" + case_name + "/branch.csv", header=None)
    gen = pd.read_csv("../datasets/ps/" + case_name + "/gen.csv", header=None)
    #     mac = pd.read_csv("../datasets/" + case_name + "/mac.csv", header=None)
    #     shunt = pd.read_csv("../datasets/" + case_name + "/shunt.csv", header=None)
    #     exc = pd.read_csv("../datasets/" + case_name + "/exc.csv", header=None)
    #     gov = pd.read_csv("../datasets/" + case_name + "/gov.csv", header=None)

    bus_id = list(bus[0])
    branch_from = list(branch[0])
    branch_to = list(branch[1])
    try:
        branch_id = list(branch[23])
    except KeyError:
        branch_id = list(branch[22])
    gen_bus = list(gen[0])
    #     gen_id = gen[-1]
    #     mac_bus = mac[0]
    #     shunt_bus = shunt[0]
    #     exc_bus = exc[0]
    #     gov_bus = gov[0]

    print("> Red Node: Bus with Gen")
    print("> Green Node: Bus without Gen")

    node_list = []
    color_map = []
    G = nx.Graph()
    for bus_i in bus_id:
        node_list.append(bus_i)
        if bus_i in gen_bus:
            color_map.append("red")
        else:
            color_map.append("green")
    G.add_nodes_from(node_list)
    for f, t, i in zip(branch_from, branch_to, branch_id):
        G.add_edge(f, t, key=i)

    pos = nx.kamada_kawai_layout(G)
    nx.draw_networkx(G, pos=pos, node_color=color_map)
    if save_fig:
        plt.savefig(case_name + ".png")  # save as png
    plt.show()  # display


def show_plot(case_name, data_time_stamp, i, ref=True):

    data_types = [
        "delta",
        "omega",
        "Pm",
        "Eap",
        "Vmag",
        "theta",
        "E1",
        "Efd",
        "P3",
        "Temperature",
    ]

    print("> Data type: {}".format(data_types[i]))

    # set file_name
    if ref:
        file_dir = path.join("../datasets/ref/", case_name)
    else:
        file_dir = path.join("../datasets/", case_name)
    file_name = data_types[i] + "_sim_" + case_name + "_" + data_time_stamp + ".csv"
    file_name = path.join(file_dir, file_name)

    # upload the data
    data = pd.read_csv(file_name, index_col=0, header=None)
    print("> Data shape: {}".format(data.shape))

    # check convergence
    print("> Converged? {}".format(not data.isnull().values.any()))

    # plot the data
    data.plot(xlabel="time", ylabel=data_types[i], figsize=(12, 8), legend=True)


def show_dist(case_name, i, time_at=0):
    data_types = [
        "delta",
        "omega",
        "Pm",
        "Eap",
        "Vmag",
        "theta",
        "E1",
        "Efd",
        "P3",
        "Temperature",
    ]

    print("> Data type: {}".format(data_types[i]))

    file_names = glob.glob("../datasets/" + case_name + "/" + data_types[i] + "*")
    data_at_t = []
    for file_name in file_names:
        data = pd.read_csv(file_name, index_col=0, header=None)
        data_at_t.append(list(data.iloc[time_at]))
    data_at_t = np.array(data_at_t)
    print(np.linalg.matrix_rank(data_at_t))

    for i in range(data_at_t.shape[1]):
        sns.boxplot(data=data_at_t[:, i])
        # sns.histplot(data_t0[:, i])


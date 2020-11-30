import pandas as pd
import numpy as np
import matlab


def bus_converter(opf_data):
    data = {}
    for col_idx in range(len(opf_data[0, :])):
        if col_idx == 0:
            data["bus_i"] = opf_data[:, col_idx]
        elif col_idx == 1:
            data["type"] = opf_data[:, col_idx]
        elif col_idx == 2:
            data["Pd"] = opf_data[:, col_idx]
        elif col_idx == 3:
            data["Qd"] = opf_data[:, col_idx]
        elif col_idx == 4:
            data["Gs"] = opf_data[:, col_idx]
        elif col_idx == 5:
            data["Bs"] = opf_data[:, col_idx]
        elif col_idx == 6:
            data["area"] = opf_data[:, col_idx]
        elif col_idx == 7:
            data["Vm"] = opf_data[:, col_idx]
        elif col_idx == 8:
            data["Va"] = opf_data[:, col_idx]
        elif col_idx == 9:
            data["baseKV"] = opf_data[:, col_idx]
        elif col_idx == 10:
            data["zone"] = opf_data[:, col_idx]
        elif col_idx == 11:
            data["Vmax"] = opf_data[:, col_idx]
        elif col_idx == 12:
            data["Vmin"] = opf_data[:, col_idx]
        else:
            print("bus error occured at col {}".format(col_idx))

    data = pd.DataFrame.from_dict(data)
    return data


def gen_converter(opf_data):
    data = {}
    for col_idx in range(len(opf_data[0, :])):
        if col_idx == 0:
            data["bus"] = opf_data[:, col_idx]
        elif col_idx == 1:
            data["Pg"] = opf_data[:, col_idx]
        elif col_idx == 2:
            data["Qg"] = opf_data[:, col_idx]
        elif col_idx == 3:
            data["Qmax"] = opf_data[:, col_idx]
        elif col_idx == 4:
            data["Qmin"] = opf_data[:, col_idx]
        elif col_idx == 5:
            data["Vg"] = opf_data[:, col_idx]
        elif col_idx == 6:
            data["mBase"] = opf_data[:, col_idx]
        elif col_idx == 7:
            data["status"] = opf_data[:, col_idx]
        elif col_idx == 8:
            data["Pmax"] = opf_data[:, col_idx]
        elif col_idx == 9:
            data["Pmin"] = opf_data[:, col_idx]
        elif col_idx == 10:
            data["Pc1"] = opf_data[:, col_idx]
        elif col_idx == 11:
            data["Pc2"] = opf_data[:, col_idx]
        elif col_idx == 12:
            data["Qc1min"] = opf_data[:, col_idx]
        elif col_idx == 13:
            data["Qc1max"] = opf_data[:, col_idx]
        elif col_idx == 14:
            data["Qc2min"] = opf_data[:, col_idx]
        elif col_idx == 15:
            data["Qc2max"] = opf_data[:, col_idx]
        elif col_idx == 16:
            data["ramp_agc"] = opf_data[:, col_idx]
        elif col_idx == 17:
            data["ramp_10"] = opf_data[:, col_idx]
        elif col_idx == 18:
            data["ramp_30"] = opf_data[:, col_idx]
        elif col_idx == 19:
            data["ramp_q"] = opf_data[:, col_idx]
        elif col_idx == 20:
            data["apf"] = opf_data[:, col_idx]
        else:
            print("gen error occured at col {}".format(col_idx))

    data = pd.DataFrame.from_dict(data)
    return data


def gencost_converter(opf_data):
    data = {}
    n = int(opf_data[0][3])
    for col_idx in range(len(opf_data[0, :])):
        if col_idx == 0:
            data["2"] = opf_data[:, col_idx]
        elif col_idx == 1:
            data["startup"] = opf_data[:, col_idx]
        elif col_idx == 2:
            data["shutdown"] = opf_data[:, col_idx]
        elif col_idx == 3:
            data["n"] = opf_data[:, col_idx]
        else:
            col_name = "c" + str(n + 3 - col_idx)
            data[col_name] = opf_data[:, col_idx]

    data = pd.DataFrame.from_dict(data)
    return data


def branch_converter(opf_data):
    data = {}
    for col_idx in range(len(opf_data[0, :])):
        if col_idx == 0:
            data["fbus"] = opf_data[:, col_idx]
        elif col_idx == 1:
            data["tbus"] = opf_data[:, col_idx]
        elif col_idx == 2:
            data["r"] = opf_data[:, col_idx]
        elif col_idx == 3:
            data["x"] = opf_data[:, col_idx]
        elif col_idx == 4:
            data["b"] = opf_data[:, col_idx]
        elif col_idx == 5:
            data["rateA"] = opf_data[:, col_idx]
        elif col_idx == 6:
            data["rateB"] = opf_data[:, col_idx]
        elif col_idx == 7:
            data["rateC"] = opf_data[:, col_idx]
        elif col_idx == 8:
            data["ratio"] = opf_data[:, col_idx]
        elif col_idx == 9:
            data["angle"] = opf_data[:, col_idx]
        elif col_idx == 10:
            data["status"] = opf_data[:, col_idx]
        elif col_idx == 11:
            data["angmin"] = opf_data[:, col_idx]
        elif col_idx == 12:
            data["angmax"] = opf_data[:, col_idx]
        else:
            print("branch error occured at col {}".format(col_idx))

    data = pd.DataFrame.from_dict(data)
    return data


def read_m_data(mpc):
    for key in mpc.keys():
        if type(mpc[key]) == matlab.double:
            mpc[key] = np.asarray(mpc[key])

        if key in ["bus", "gen", "gencost", "branch"]:
            if key == "bus":
                mpc[key] = bus_converter(mpc[key])
            elif key == "gen":
                mpc[key] = gen_converter(mpc[key])
            elif key == "gencost":
                mpc[key] = gencost_converter(mpc[key])
            elif key == "branch":
                mpc[key] = branch_converter(mpc[key])
            else:
                print("read_m error")

    return mpc

import os
import matlab.engine
import argparse
from tqdm import trange
import numpy as np
import pickle

my_parser = argparse.ArgumentParser()
my_parser.add_argument("-i", action="store", help="input mat file name")
my_parser.add_argument(
    "-n", action="store", type=int, help="the number of generated samples"
)
my_parser.add_argument(
    "-d",
    action="store",
    type=float,
    default=0.01,
    help="the scaling coefficent of uncertainty distributions",
)


args = my_parser.parse_args()

case_name = vars(args)["i"]
sample_num = vars(args)["n"]
dist_scale = vars(args)["d"]

print("> case_name: {}".format(case_name))
print("> number of samples: {}".format(sample_num))
print("> uncertainty distribution scaling coeff: {}".format(dist_scale))

current_dir = os.getcwd()
os.chdir("./matpower7.1/")

print("> start generating dastaset")

eng = matlab.engine.start_matlab()

features = []
labels = []

for i in trange(sample_num):
    # solve opf with perturbed data
    data = eng.run_opf_ac(case_name, dist_scale)

    # feature data
    feature = np.hstack(
        (
            np.asarray(data["Pg"]).squeeze(),
            np.asarray(data["Pd"]).squeeze(),
            np.asarray(data["Qd"]).squeeze(),
        )
    )
    feature = np.expand_dims(feature, axis=1)
    features.append(feature)

    # label data
    F_act = np.asarray(data["F_act"])
    F_max = np.asarray(data["F_max"])
    label = (F_act / F_max) * 100
    labels.append(label)

dataset = {"feature": np.array(features), "label": np.array(labels)}

os.chdir(current_dir)

dataset_dir = os.path.join("../data", "GCN_datasets")
dataset_name = case_name.split(".")[0]
dataset_path = os.path.join(dataset_dir, dataset_name)

outfile = open(dataset_path + ".pickle", "wb")
pickle.dump(dataset, outfile)
outfile.close()

print("> the dataset is saved at /'{}/'".format(dataset_path))

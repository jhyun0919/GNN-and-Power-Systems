import os
import matlab.engine
import argparse
from tqdm import trange
import numpy as np
import pickle
import time
from datetime import timedelta
from datetime import datetime
from sys import exit

start_time = time.time()

my_parser = argparse.ArgumentParser()
my_parser.add_argument("-i", action="store", help="input mat file name")
my_parser.add_argument(
    "-n", action="store", type=int, help="the number of generated samples"
)


args = my_parser.parse_args()

case_name = vars(args)["i"]
sample_num = vars(args)["n"]

print("> input args")
print("  - case_name: {}".format(case_name))
print("  - number of samples = {}".format(sample_num))

THRESHOLD = False
THRESHOLD_1 = 100
THRESHOLD_2 = int(0.1 * (sample_num))

# generate the dataset by Matpower
print("> start generating dastaset")

current_dir = os.getcwd()
os.chdir("./matpower7.1/")

eng = matlab.engine.start_matlab()

features = []
labels = []

threshold_tick = 0
for i in trange(sample_num):
    # solve opf with perturbed data
    data = eng.run_opf_ac(case_name)

    # feature data
    feature = np.hstack(
        (
            np.asarray(data["Pg"]).squeeze(),
            np.asarray(data["Pd"]).squeeze(),
            np.asarray(data["Qd"]).squeeze(),
        )
    )
    feature = np.expand_dims(feature, axis=1)

    # label data
    F_act = np.asarray(data["F_act"])
    F_max = np.asarray(data["F_max"])
    del_idx = []
    for idx, (f_act, f_max) in enumerate(zip(F_act, F_max)):
        if f_max == 0:
            del_idx.append(idx)
    F_act = np.delete(F_act, del_idx)
    F_max = np.delete(F_max, del_idx)
    label = (F_act / F_max) * 100
    label = np.expand_dims(label, axis=1)

    # append a sample
    # ... if Fmax is not ZERO
    if len(label) == 0:
        threshold_tick += 1
        if threshold_tick > THRESHOLD_1:
            THRESHOLD = True
        elif threshold_tick > THRESHOLD_2:
            THRESHOLD = True
        if THRESHOLD:
            print("-------- terminate the iteration --------")
            exit()
    else:
        features.append(feature)
        labels.append(label)


dataset = {"feature": np.array(features), "label": np.array(labels)}

# save the generated dataset
os.chdir(current_dir)
dataset_dir = os.path.join("../data", "GCN_datasets")
dataset_name = case_name.split(".")[0]
dt = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
dataset_path = (
    os.path.join(dataset_dir, dataset_name)
    + "_"
    + str(sample_num)
    + "_"
    + dt
    + ".pickle"
)

outfile = open(dataset_path, "wb")
pickle.dump(dataset, outfile)
outfile.close()

print("> the dataset is saved as '{}'".format(dataset_path))
print("> execution time: {}".format(str(timedelta(seconds=time.time() - start_time))))

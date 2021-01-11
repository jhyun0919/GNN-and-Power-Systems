import matlab.engine
import os, glob
from tqdm import trange
import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument(
    "-n",
    action="store",
    type=int,
    help="the number of generated samples for each outage pair",
)

args = my_parser.parse_args()
num_samples = vars(args)["n"]

num_branches = 46
failure_pairs = [(2, 9), (2, 29), (8, 29), (9, 13), (23, 25), (23, 26), (23, 32)]

num_outage_pairs = (num_branches * (num_branches - 1) / 2) - len(failure_pairs)

# print info
print("> Contingency: N-2")
print("> Case Name: case39")
print("> Number of Branches: {}".format(num_branches))
print("> Number of Generated Samples for each Outage Pair: {}".format(num_samples))
print(
    "> Total Number of Generated Samples: {}".format(num_samples * (num_outage_pairs))
)

# generate the dataset by COSMIC
current_dir = os.getcwd()
os.chdir("../cosmic/matlab/")

eng = matlab.engine.start_matlab()

eng.write_ps_csv("../../datasets/case39", 39)

for i in range(23, num_branches + 1):
    for j in range(i, num_branches + 1):
        if i == j:
            pass
        elif (i, j) in failure_pairs:
            pass
        else:
            print()
            print("> tripped branch index: {} & {}".format(i, j))
            print()
            for k in range(num_samples):
                eng.sim_case39_n_2(i, j, "../../datasets/case39", k, True, False)

                for filename in glob.glob("../../datasets/case39/sim*"):
                    os.remove(filename)
                for filename in glob.glob("../../datasets/case39/trace*"):
                    os.remove(filename)

os.chdir(current_dir)

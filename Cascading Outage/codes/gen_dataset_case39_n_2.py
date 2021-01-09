import matlab.engine
import os, glob
from tqdm import trange

# generate the dataset by COSMIC
print("> Contingency: N-2")
print("> Case Name: case39")

current_dir = os.getcwd()
os.chdir("../cosmic/matlab/")

eng = matlab.engine.start_matlab()

num_branches = 46

print("> Number of Branches: {}".format(num_branches))

for i in trange(1, num_branches + 1):
    for j in range(1, num_branches + 1):
        if i == j:
            pass
        else:
            print()
            print("- tripped branch index: {} & {}".format(i, j))
            print()
            eng.sim_case39_n_2(i, j, "../../datasets/case39", False)

            for filename in glob.glob("../../datasets/case39/sim*"):
                os.remove(filename)
            for filename in glob.glob("../../datasets/case39/trace*"):
                os.remove(filename)

os.chdir(current_dir)

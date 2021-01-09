import matlab.engine
import os, glob
from tqdm import trange

# generate the dataset by COSMIC
print("> Contingency: N-2")
print("> Case Name: case2383")

current_dir = os.getcwd()
os.chdir("../cosmic/matlab/")

eng = matlab.engine.start_matlab()

num_branches = 2896

print("> Number of Branches: {}".format(num_branches))

for i in trange(1, num_branches + 1):
    for j in range(1, num_branches + 1):
        if i == j:
            pass
        else:
            print()
            print("- tripped branch index: {} & {}".format(i, j))
            print()
            eng.sim_case2383_n_2(i, j, "../../datasets/case2383", False)

            for filename in glob.glob("../../datasets/case2383/sim*"):
                os.remove(filename)
            for filename in glob.glob("../../datasets/case2383/trace*"):
                os.remove(filename)

os.chdir(current_dir)

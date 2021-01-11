import matlab.engine
import os, glob
from tqdm import trange
import argparse
from sys import exit


def run_mat_code(
    eng,
    trip_i,
    trip_j,
    case_num,
    case_name,
    num_samples,
    verbose=False,
    print_opt=False,
):
    print()
    print("> tripped branch index: ({}, {})".format(trip_i, trip_j))
    print()
    for k in trange(num_samples):
        if case_num == 9:
            eng.sim_case9_n_2(
                trip_i, trip_j, "../../datasets/" + case_name, k, verbose, print_opt
            )
        elif case_num == 39:
            eng.sim_case39_n_2(
                trip_i, trip_j, "../../datasets/" + case_name, k, verbose, print_opt
            )
        else:
            eng.sim_case2383_n_2(
                trip_i, trip_j, "../../datasets/" + case_name, k, verbose, print_opt
            )

        for filename in glob.glob("../../datasets/" + case_name + "/sim*"):
            os.remove(filename)
        for filename in glob.glob("../../datasets/" + case_name + "/trace*"):
            os.remove(filename)


def get_num_failure_pairs(trip_i, trip_j, failure_pairs, num_branches):
    if trip_i is None and trip_j is None:
        num_failure_pairs = len(failure_pairs)
    elif trip_i is not None and trip_j is None:
        num_failure_pairs = 0
        for j in range(1, num_branches + 1):
            if (trip_i, j) in failure_pairs:
                num_failure_pairs += 1
    else:
        num_failure_pairs = 0

    return num_failure_pairs


def main():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument(
        "-c", action="store", type=int, help="case number",
    )
    my_parser.add_argument(
        "-i", action="store", type=int, help="trip branch index i",
    )

    my_parser.add_argument(
        "-j", action="store", type=int, help="trip branch index j",
    )

    my_parser.add_argument(
        "-n",
        action="store",
        type=int,
        help="the number of generated samples for each outage pair",
    )

    args = my_parser.parse_args()
    case_num = vars(args)["c"]
    trip_i = vars(args)["i"]
    trip_j = vars(args)["j"]
    num_samples = vars(args)["n"]

    verbose = False
    print_opt = False

    if case_num not in [9, 39, 2383]:
        print("wrong case num input arg")
        exit()

    if trip_i == trip_j:
        if trip_i is not None or trip_i is not None:
            print("i and j should be different two numbers")
            exit()
    if trip_i is None and trip_j is not None:
        trip_i, trip_j = trip_j, trip_i

    if case_num == 9:
        case_name = "case9"
        num_branches = 9
        failure_pairs = []
    elif case_num == 39:
        case_name = "case39"
        num_branches = 46
        failure_pairs = [
            (2, 9),
            (2, 29),
            (8, 29),
            (9, 13),
            (23, 25),
            (23, 26),
            (23, 32),
            (29, 30),
        ]
    else:
        case_name = "case2383"
        num_branches = 2896
        failure_pairs = []

    if (trip_i, trip_j) in failure_pairs:
        print(
            "pair ({}, {}) is unable to finish the computation.".format(trip_i, trip_j)
        )
        exit()

    num_failure_pairs = get_num_failure_pairs(
        trip_i=trip_i,
        trip_j=trip_j,
        failure_pairs=failure_pairs,
        num_branches=num_branches,
    )

    if trip_i is None and trip_j is None:
        num_outage_pairs = (num_branches * (num_branches - 1) / 2) - num_failure_pairs
    elif trip_i is not None and trip_j is None:
        num_outage_pairs = num_branches - num_failure_pairs
    else:
        num_outage_pairs = 1 - num_failure_pairs

    # print info
    print("> Contingency: N-2")
    print("> Case Name: {}".format(case_name))
    print("> Number of Branches: {}".format(num_branches))
    print("> Number of Outage Pairs: {}".format(num_outage_pairs))
    print("> Number of Generated Samples per Outage Pair: {}".format(num_samples))
    print(
        "> Total Number of Generated Samples: {}".format(num_samples * num_outage_pairs)
    )

    # generate the dataset by COSMIC
    current_dir = os.getcwd()
    os.chdir("../cosmic/matlab/")

    eng = matlab.engine.start_matlab()

    if num_outage_pairs == 1:
        run_mat_code(
            eng=eng,
            trip_i=trip_i,
            trip_j=trip_j,
            case_num=case_num,
            case_name=case_name,
            num_samples=num_samples,
            verbose=verbose,
            print_opt=print_opt,
        )
    elif num_outage_pairs == num_branches - 1:
        for trip_j in range(1, num_branches + 1):
            if trip_i == trip_j:
                pass
            elif (trip_i, trip_j) in failure_pairs:
                pass
            else:
                run_mat_code(
                    eng=eng,
                    trip_i=trip_i,
                    trip_j=trip_j,
                    case_num=case_num,
                    case_name=case_name,
                    num_samples=num_samples,
                    verbose=verbose,
                    print_opt=print_opt,
                )
    else:
        for trip_i in range(1, num_branches + 1):
            for trip_j in range(trip_i, num_branches + 1):
                if trip_i == trip_j:
                    pass
                elif (trip_i, trip_j) in failure_pairs:
                    pass
                else:
                    run_mat_code(
                        eng=eng,
                        trip_i=trip_i,
                        trip_j=trip_j,
                        case_num=case_num,
                        case_name=case_name,
                        num_samples=num_samples,
                        verbose=verbose,
                        print_opt=print_opt,
                    )

    os.chdir(current_dir)


if __name__ == "__main__":
    main()

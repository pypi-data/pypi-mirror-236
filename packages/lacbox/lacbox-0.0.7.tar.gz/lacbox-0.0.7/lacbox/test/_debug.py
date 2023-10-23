import argparse

parser = argparse.ArgumentParser(description="Debugging AESOpt.aerodynamics")
parser.add_argument("run", nargs="?", help="Number for the test to run", type=int, default=True)
parser.add_argument("--verbose", action="store_false", help="Flag for NOT printing verbose output")
parser.add_argument("--plot", action="store_false", help="Flag for NOT plotting the output")
args = parser.parse_args().__dict__
run = args["run"] 
verbose = args["verbose"] 
plot = args["plot"]


def run_flag(run, flag):
    if isinstance(run, bool):
        return run
    elif isinstance(run, int):
        return run == flag
    elif isinstance(run, list):
        return any([run_flag(_run, flag) for _run in run])


from test_io import test_load_save_pc, test_load_save_st, test_load_save_oper

if run_flag(run, 1):
    test_load_save_pc()
if run_flag(run, 2):
    test_load_save_st()
if run_flag(run, 3):
    test_load_save_oper()

from test_aero import test_smooth_root
if run_flag(run, 10):
    test_smooth_root()



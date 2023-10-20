import json
import pandas as pd

from .lib import *

class Logger:
    # Folders
    RUNS = "runs/"

    # Files
    BEST_FILE = "best.json"
    PROGRESS_REPORT_FILE = "progress_report.csv"

    def run(i, seed):
        return f"run_{i}_{seed}/"
    
    def error_experiment_exists():
        print("User Warning: There is already an experiment with that name.\nPlease delete/change the name of the experiment (SGE parameters file)")

    def get_progress_reports(experiment):
        # Fitness
        BEST, MEAN, STD  = "Best", "Mean", "Std"
        bests, means, stds = [], [], []
        
        for seed in range(30):
            df = pd.read_csv(Logger.get_progress_report_file(experiment, seed), sep="\t", index_col=0, names=["index", BEST, MEAN, STD])
            
            bests.append(df[BEST])
            means.append(df[MEAN])
            stds.append(df[STD])
            
        # Fitness
        bests = pd.concat(bests, axis=1)
        means = pd.concat(means, axis=1)
        stds = pd.concat(stds, axis=1)

        return bests, means, stds

    def save_json(json_data, path):
        with open(path, "w") as f:
            json.dump(json_data, f)

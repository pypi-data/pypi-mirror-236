import os
from .. import sge 

from .utilities.lib import *
from .utilities.logger import Logger

class Fedora(sge.EngineSGE):

    def __init__(
            self,
            data,
            seeds,
            model,
            error_metric,
            sge_parameters_path,
            grammar_path,
            logging_dir,
            penalty = None
        ):  
        
        # SGE setup
        super().__init__(sge_parameters_path)

        # Get Data
        self.data = data

        # Set the seed
        self.seeds = seeds

        # Set model
        self.model = model

        # Error Metric
        self.error_metric = error_metric

        # Define Grammar Path
        self.grammar_path = grammar_path

        # Define Logging Directory
        self.logging_dir = logging_dir

        # Define fitness penalty function
        self.penalty = penalty

    # def evaluate(self, phenotype: str) -> tuple[float, dict]:
    def evaluate(self, phenotype):
        """ Structured Grammatical Evolution (SGE) Evaluate Function """

        # Applying the Individual Phenotype to the dataset
        engineered_train = engineer_dataset(phenotype, self.train_data)
        engineered_validation = engineer_dataset(phenotype, self.validation_data)
        
        # Fitness
        fitness = score(self.model, engineered_train, engineered_validation, self.error_metric)

        if self.penalty:
            fitness += self.penalty(self.model)

        # Info
        self.individuals_information.append({PHENOTYPE: phenotype, FITNESS: fitness})

        return fitness, None

    def evolution_progress(self, population):
        # phenotypes = [individual["phenotype"] for individual in population]
        return ""

    def save_best(self, current_run):
        best_validation_info = sorted(self.individuals_information, key=lambda x: x[FITNESS])[0]
        Logger.save_json({PHENOTYPE: best_validation_info[PHENOTYPE]}, current_run + Logger.BEST_FILE)
        

    def run(self):
        experience_dir = self.logging_dir + sge.params["EXPERIMENT_NAME"]

        if os.path.exists(experience_dir): 
            return Logger.error_experiment_exists()

        for i in range(len(self.seeds)):
            # Individuals Information
            self.individuals_information = []
            
            # Run Seed
            self.seed = self.seeds[i]

            # Setup SGE PARAMS                                 
            sge.params["RUN"] = i
            sge.params["SEED"] = self.seed
            sge.params["GRAMMAR"] = self.grammar_path
            sge.params["EXPERIMENT_NAME"] = experience_dir + Logger.RUNS

            self.current_run = sge.params["EXPERIMENT_NAME"] + Logger.run(i, self.seed)

            # Create Current Run Folder if not exists
            if not os.path.exists(self.current_run): 
                os.makedirs(self.current_run)
            
            # Set Model Seed
            self.model.random_state = self.seed
                 
            # Split Data
            self.train_data, self.test_data, self.validation_data, self.train_validation_data = split_data(self.data, self.seed)
            
            # Run Structured Grammatical Evolution
            self.evolutionary_algorithm()
            
            # Save the phenotype of the best validation individual
            self.save_best(self.current_run)
            
        return self
    
"""! @brief Get Data stage, for obtaining data from a generic source, such as a database."""
import os
import sys
from typing import Any
from json import loads as json_loads

from dsframework.base.batch.pipeline_stage_base import ZIDS_BatchPipelineStage
from trainer.main import Main
from trainer.config import config as trainer_config

##
# @file
# @brief Stage main class, implements ZIDS_Stage base class.
class RunTrainerStage(ZIDS_BatchPipelineStage):
    """! Stage class

    Implement a stage that will later be converted to an executable job in a specific workflow.
    """

    def __init__(self, stage_config):
        """! The Stage class (generatedStageName) initializer.
        Base class will load basic configuration parameters, additional fields should be added here

            Args:
                stage_config : Configuration dictionary, loaded from configuration file.
        """

        ##
        # @hidecallgraph @hidecallergraph
        print(f"Initializing Stage: {self.get_name()}")
        super().__init__(stage_config)

    def get_name(self):
        """! Get the stage name
        """
        return self.__class__.__name__

    def main(self, **kwargs: Any):
        """! Executes the main functionality of the stage.

            Args:
                **kwargs : Whatever is needed for the stage to run properly.
        """
        trainer_main_class = Main(cfg=trainer_config, training_path=os.getcwd() + '/datasets',
                          validation_path=os.getcwd() + '/datasets')
        trainer_main_class.execute_trainer(force_save_path='/trainer_tmp')
        trainer_main_class.copy_to_gs(self.bucket_name, self.folder_path, self.project_id)

        print('Trainer stage completed.')


if __name__ == "__main__":
    """! Executes the stage by instantiating it and calling the main function.
    Set up argument condition according to the usage of the written stage

        Args:
            System argument 1 - Configuration file
            System argument 2 - Start date
    """
    if sys.argv and len(sys.argv) > 1:
        config = json_loads(sys.argv[1])
        stage = RunTrainerStage(config)
        try:
            start_date = sys.argv[2]
            end_date = sys.argv[3]
            params = sys.argv[4]
            stage.update_stage_params(start_date, end_date, params)
            stage.main()
        except Exception as e:
            raise Exception(f" Stage failed with error: {e}")
    else:
        raise Exception(f"Stage configuration not provided, Can't run stage")

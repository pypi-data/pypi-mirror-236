"""! @brief Get Data stage, for obtaining data from a generic source, such as a database."""
import sys
import logging
from json import loads as json_loads
from dsframework.base.batch.pipeline_stage_base import ZIDS_BatchPipelineStage

logger = logging.getLogger(__name__)

##
# @file
# @brief Stage main class, implements ZIDS_Stage base class.
class ExampleStage(ZIDS_BatchPipelineStage):
    """! Example Stage class
    Implement a stage that will later be converted to an executable job in a specific workflow.
    """

    def __init__(self, stage_config):
        """! The Stage class (ExampleStage) initializer.
        Base class will load basic configuration parameters, additional fields should be added here

            Args:
                stage_config : Configuration dictionary, loaded from configuration file.
        """

        ##
        # @hidecallgraph @hidecallergraph
        logger.info(f"Initializing Stage: {self.get_name()}")
        self.highest_price_unit_df = None
        self.df = None
        super().__init__(stage_config, logger)
        self.spark = self.load_spark()
        logger.info(f"Stage {self.get_name()} Initialized")

    def get_name(self):
        """! Get the stage name
        """
        return self.__class__.__name__

    def load(self):
        """! The \'load\' phase is for loading input dataframes and running input data tests if needed
        """
        self.df = self.spark.read. \
            options(header='true', inferSchema='true').csv(f"gs://{self.bucket_name}/example_data/retail_day.csv")

    def run(self):
        """! The \'run\' phase is for the transform logic
        """
        self.df.printSchema()
        self.df.createOrReplaceTempView("sales")
        self.highest_price_unit_df = self.spark.sql("select * from sales where UnitPrice >= 3.0")

    def finish(self):
        """! The \'finish\' phase is for saving output dataframes and running output data tests if needed
        """
        self.highest_price_unit_df.write.mode("overwrite").parquet(f"{self.bucket_path}"
                                                                   f"/example_data/highest_prices_{self.project_id}.parquet")


if __name__ == "__main__":
    """! Executes the stage by instantiating it and calling the __call__ function of the base class.

        Args:
            System argument 1 - Configuration file
            System argument 2 - Start date, received from Airflow
            System argument 3 - End date, received from Airflow
            System argument 4 - Placeholder for future parameters
    """
    if sys.argv and len(sys.argv) > 1:
        config = json_loads(sys.argv[1])
        stage = ExampleStage(config)
        try:
            start_date = sys.argv[2]
            end_date = sys.argv[3]
            params = sys.argv[4]
            stage.update_stage_params(start_date, end_date, params)
            stage()
        except Exception as e:
            raise Exception(f" Stage failed with error: {e}")
    else:
        raise Exception(f"Stage configuration not provided, Can't run stage")

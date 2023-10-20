import os
import pendulum
import pandas as pd

# BigQuery API
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from .transform import Transform


class BigQuery:

    """
    Pass in a service account file path and query data stored in BigQuery
    Example: BigQuery().query("SELECT * FROM `jinlee.dbt.fct_receive` LIMIT 10")
    """
    
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("BIGQUERY_SERVICE_ACCOUNT"), scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        self.project = self.client.project

    def query(self, sql):
        """
        Returns results of SQL Query as a pandas DataFrame
        """
        return self.client.query(sql).to_dataframe()

    @staticmethod
    def prepare_df(df):
        # Lower case columns, replace spaces with underscore
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Add a UTC timestamp
        df['updated_at'] = pendulum.now().strftime('%Y-%m-%d %H:%M:%S %p')
        df['updated_at'] = df['updated_at'].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S %p', utc=True)
        
        return df

    def list_datasets(self):
    
        """
        Datasets in project jinlee:
            accounts
            dbo
            dbt_bigquery
            dev
            gsheets
            jinlee
            spareparts
        """
    
        datasets = list(self.client.list_datasets())  # Make an API request.
        project = self.client.project

        if datasets:
            
            dataset_list = []
            
            print("Datasets in project {}:".format(project))
            for dataset in datasets:
                print("\t{}".format(dataset.dataset_id))
                dataset_list.append(dataset.dataset_id)
                
            return dataset_list
            
        else:
            print("{} project does not contain any datasets.".format(project))
    
    def list_tables_in_dataset(self, dataset):
        
        # TODO(developer): Set dataset_id to the ID of the dataset that contains
        #                  the tables you are listing.
        # dataset_id = 'jinlee.dbo'

        tables = self.client.list_tables(f"{self.project}.{dataset}")  # Make an API request.
        table_names = []
        print("Tables contained in '{}':".format(dataset))
        for table in tables:
            table_name = "{}.{}.{}".format(table.project, table.dataset_id, table.table_id)
            table_names.append(table_name)
            print(table_name)
        return table_names
    
    # READ
    
    def select(self, sql, query_config=None):
        
        """
        Pass in a SQL Query and query_config
        and return the results as a DataFrame        
        """

        # self.client.query(sql).to_dataframe()
        
#         sql = """
#             SELECT * 
#             FROM `jinlee.dbo.weighbridge_PMF_MASTER`
#             WHERE DATE(date) >= @date
#             LIMIT @limit
#         """

#         query_config = bigquery.QueryJobConfig(
#             query_parameters=[
#                 bigquery.ScalarQueryParameter('date', 'DATE', '2021-01-01'),
#                 bigquery.ScalarQueryParameter('limit', 'INTEGER', 1000)
#             ]
#         )
    
        return self.client.query(sql, job_config=query_config).to_dataframe()
    
    # CREATE

    def updated_count(self, table_id):

        """
        Checks how many times a script has run
        """

        update_counter = 0

        # Query distinct count and add to counter
        query_job = self.client.query(
            f"""
            SELECT count(distinct(updated_at)) as updated_count
            FROM {table_id}
            """
        )

        print(f"[ Read  ] Checking if {table_id} has been updated before ...")

        # Query will only run if table is found
        try:
            results = query_job.result() 
            for row in results:
                update_counter += row.updated_count
            print(f"[ Read  ] Table {table_id} has been updated {update_counter} time(s).")

        except NotFound:
            print(f"[ Read  ] Table {table_id} does not exist. This will be the first time writing to BQ.")

        return update_counter

    def check_if_dataset_exists(self, dataset_id):

        """
        Checks if the dataset {project_name}.{schema} exists
        Create it if it does not
        """

        try:
            self.client.get_dataset(dataset_id) # Make an API request
            print(f"[ Read  ] Dataset {dataset_id} found! Proceeding to write data ...")

        except NotFound:
            print(f"[ Read  ] {dataset_id} not found, attempting to create the requested dataset now ...")
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "asia-southeast1"
            dataset = self.client.create_dataset(dataset, timeout=30)
            print(f"[ Write ] {self.client.project}.{dataset.dataset_id} created in {dataset.location}.")

    def create_table(self, df, source, schema, table, write_behavior=None, job_config=None):

        # table_id = 'jinlee.stocks'

        # Since string columns use the "object" dtype, pass in a (partial) schema
        # to ensure the correct BigQuery data type.
        # job_config = bigquery.LoadJobConfig(schema=[
        #     bigquery.SchemaField("my_string", "STRING"),
        # ])

        """
        `WRITE_TRUNCATE`: If the table already exists, BigQuery overwrites the table data and uses the schema from the query result.
        `WRITE_APPEND`: If the table already exists, BigQuery appends the data to the table.
        `WRITE_EMPTY`: If the table already exists and contains data, a 'duplicate' error is returned in the job result.

        The default value is `WRITE_EMPTY`. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. 
        Creation, truncation and append actions occur as one atomic update upon job completion.
        """
        
        dataset_id = f"{self.project}.{schema}"
        table_id = f"{dataset_id}.{table}"

        # Default behavior is append
        if write_behavior is None:
            write_behavior = "WRITE_APPEND"

        # Check for empty frame
        if df is not None:

            self.check_if_dataset_exists(dataset_id=dataset_id)
            
            # Identify where the data came from
            df['data_source'] = source

            # Prepare the df to be written to BigQuery
            transformed_df = Transform(df).lower_case_columns()\
                                          .add_updated_timestamp().df

            # Keep track of how many times the data has been inserted
            df['updated_count'] = self.updated_count(table_id=table_id)

            # Allow user to pass in job_config manually
            if job_config is None:                                     
                # Proceed to write the data to the dataset
                job_config = bigquery.LoadJobConfig(
                    write_disposition=write_behavior
                )
            print(f"[ Write ] BigQuery.{table_id} using {write_behavior}.")
            
            job = self.client.load_table_from_dataframe(
                df, table_id, job_config=job_config
            )
            
            print(f"[ Done  ] BigQuery.{table_id} Wrote {len(transformed_df)} rows.")

            # Wait for the load job to complete.
            return job.result()

        else:
            print(f"No data was written to BigQuery - Empty data.")
        
    # DELETE
    
    def delete_dataset(self, dataset_id):
        
        # TODO(developer): Set model_id to the ID of the model to fetch.
        # Example: dataset_id = 'jinlee'

        # Use the delete_contents parameter to delete a dataset and its contents.
        # Use the not_found_ok parameter to not receive an error if the dataset has already been deleted.
        self.client.delete_dataset(
            dataset_id, delete_contents=True, not_found_ok=True
        )  # Make an API request.

        print("Deleted dataset '{}'.".format(dataset_id))
        
    # DELETE TABLE
    
    def delete_table(self, table_id):
        
        # TODO(developer): Set table_id to the ID of the table to fetch.
        # table_id = 'your-project.your_dataset.your_table'

        # If the table does not exist, delete_table raises
        # google.api_core.exceptions.NotFound unless not_found_ok is True.
        self.client.delete_table(table_id, not_found_ok=True)  # Make an API request.
        
        print("Deleted table '{}'.".format(table_id))                
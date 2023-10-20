import os
from google.cloud import bigquery
import logging
logging.basicConfig(format='%(name)s - %(levelname)s -%(asctime)s- %(message)s', level=logging.INFO)


class BigQuery():
    def __int__(self, credential_json):
        self.client = bigquery.Client()
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_json

    def write_insights_to_bq_table(self, dataframe=None, schema=None, table_id=None):
        common_schema = [
            bigquery.SchemaField("date_range_start", bigquery.enums.SqlTypeNames.DATE),
            bigquery.SchemaField("date_range_end", bigquery.enums.SqlTypeNames.DATE)]
        schema.extend(common_schema)
        job_config = bigquery.LoadJobConfig(
            # Specify a (partial) schema. All columns are always written to the
            # table. The schema is used to assist in data type definitions.
            schema=schema,
            # Optionally, set the write disposition. BigQuery appends loaded rows
            # to an existing table by default, but with WRITE_TRUNCATE write
            # disposition it replaces the table with the loaded data.
            # write_disposition="WRITE_TRUNCATE",
        )

        load_job = None
        retry_count = 0
        exception = None
        while load_job is None and retry_count < 5:
            try:
                load_job = self.client.load_table_from_dataframe(
                    dataframe, table_id, job_config=job_config
                )  # Make an API request.
                load_job.result()  # Wait for the job to complete.

                table = self.client.get_table(table_id)  # Make an API request.
                message = "Loaded {} rows and {} columns to {} ".format(load_job.output_rows,
                                                                        len(table.schema),
                                                                        table_id)
                logging.info(message)
                return message
            except Exception as e:
                exception = e
                retry_count += 1
        raise Exception(f"BigQuery load job given exception in all the {retry_count} retries:  {exception}")
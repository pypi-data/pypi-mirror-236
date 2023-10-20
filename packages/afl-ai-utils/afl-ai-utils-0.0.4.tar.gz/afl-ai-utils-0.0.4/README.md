# afl-ai-utils
    rm -rf build dist 
    python3 setup.py sdist bdist_wheel
    twine upload --repository pypi dist/* 


# Usage

    
        """Send a Slack message to a channel via a webhook.

        Args:
            dataframe(pandas dataframe): for dataframe to be dumped to bigquery
            schema(BigQuery.Schema ): ex:
                schema = [
                            bigquery.SchemaField("date_range_start", bigquery.enums.SqlTypeNames.DATE),
                            bigquery.SchemaField("date_range_end", bigquery.enums.SqlTypeNames.DATE)
                        ]

            table_id (list): table_id in which dataframe need to be inserted e.g project_id.dataset.table_name = table_id
            mode(str): To append or replace the table - e.g mode = "append"  or mode="replace"
        Returns:
            returns as success message with number of inserted rows and table name
        """
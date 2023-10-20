# afl-ai-utils
    rm -rf build dist 
    python3 setup.py sdist bdist_wheel
    twine upload --repository pypi dist/* 


# Usage

### Slack Alerting

        """Send a Slack message to a channel via a webhook.

    Args:
        info_alert_slack_webhook_url(str): Infor slack channel url
        red_alert_slack_webhook_url(str): red alert channel url
        slack_red_alert_userids (list): userid's to mention in slack for red alert notification
        payload (dict): Dictionary containing Slack message, i.e. {"text": "This is a test"}
        is_red_alert (bool): Full Slack webhook URL for your chosen channel.

    Returns:
        HTTP response code, i.e. <Response [503]>
    """


### BigQuery Dataframe to BigQuery    
    
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



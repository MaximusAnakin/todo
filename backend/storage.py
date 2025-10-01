from azure.data.tables import TableServiceClient
import os
import logging

connection_string = os.environ["AzureWebJobsStorage"]
table_name = "tasks"

client = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = client.get_table_client(table_name)

try:
    table_client.create_table()
    logging.info("Table 'tasks' created or already exists")
except Exception as e:
    logging.error(f"Table creation failed: {e}")
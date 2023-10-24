from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
import json
from datetime import datetime


class LoggerOpenSearch:
    def __init__(self, host, region):
        credentials = boto3.Session().get_credentials()
        auth = AWSV4SignerAuth(credentials, region, "es")

        self.client = OpenSearch(
            hosts=[{"host": host, "port": 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            pool_maxsize=20,
        )

    def create_index(self, index_name):
        # Create an index with non-default settings.
        index_body = {"settings": {"index": {"number_of_shards": 4}}}

        response = self.client.indices.create(index_name, body=index_body)
        print("\nCreating index:")
        print(response)

    def log(self, index_name, json_data):
        json_data["date"] = datetime.utcnow().isoformat()

        # # Print the JSON-formatted string
        # print(json.dumps(json_data, indent=4))

        # Send to OpenSearch
        response = self.client.index(index=index_name, body=json_data, refresh=True)
        # print("\nAdding document:")
        # print(response)

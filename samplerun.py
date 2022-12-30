from azure.cosmos import CosmosClient, exceptions, PartitionKey
import os
import json

#load custom variables
varfile = open('custom_vars.json')
var = json.load(varfile)
varfile.close()
CONSISTENCY_LEVEL = var['variables']['CONSISTENCY_LEVEL']
DATABASE_NAME = var['variables']['DATABASE_NAME']
CONTAINER_NAME = var['variables']['CONTAINER_NAME']
URL = var['variables']['URL']
KEY = var['variables']['KEY']

#load sample data
print("Opening json file to load sample data...")   
f = open('users.json')
data = json.load(f)
f.close()

def create_items(container):
    try:
        for i in data['users']:
            container.create_item(body=i)
            print(f'Successfully created item: {i}')
    except exceptions.CosmosResourceExistsError as e:
        print("Oops! This item already exists in the container")


def delete_items(container):
    for i in data['users']:
        container.delete_item(item=i['id'], partition_key=i['userId'])
        print(f"Successfully deleted item with id: {i['id']} and userId: {i['userId']}")

def run_sample():
    client = CosmosClient(URL, credential=KEY, consistency_level=CONSISTENCY_LEVEL)
    try:
        #setup database for sample run
        database = client.create_database_if_not_exists(DATABASE_NAME)

        #setup container for sample run
        container = database.create_container_if_not_exists(id=CONTAINER_NAME, partition_key=PartitionKey(path="/userId"))
        
        create_items(container)
        response = input(f"The database => {DATABASE_NAME}, container => {CONTAINER_NAME}, and items have been successfully created! Are you ready to delete them (yes/no)?")
        if response == "yes" or "y":
            delete_items(container)
        else:
            pass

        #cleanup database
        try:
            client.delete_database(database)
            print("clean up is complete - provisioned resources have been successfully deleted.")
        except exception.CosmosResourceNotFoundError:
            pass
    
    except exceptions.CosmosHttpResponseError as e:
        print(f"Oops! Encountered an error: {e.message}")

if __name__ == '__main__':
    run_sample()
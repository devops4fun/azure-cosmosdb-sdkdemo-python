from azure.cosmos import CosmosClient, exceptions, PartitionKey
import os
import json
import time

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


def delete_items(container, database, client):
    for i in data['users']:
        container.delete_item(item=i['id'], partition_key=i['userId'])
        print(f"Successfully deleted item with id: {i['id']} and userId: {i['userId']}")
    delete_database(database, client)

def delete_database(database, client):
    #cleanup database
    try:
        client.delete_database(database)
        print("Demo is complete - provisioned resources have been successfully deleted.")
    except exceptions.CosmosResourceNotFoundError:
        pass        

def end():
    print("Demo complete. The provisioned resources have been left untouched per your request.")
    pass 

def run_sample():
    response = 'yes'
    client = CosmosClient(URL, credential=KEY, consistency_level=CONSISTENCY_LEVEL)
    try:
        #setup database for sample run
        database = client.create_database_if_not_exists(DATABASE_NAME)

        #setup container for sample run
        container = database.create_container_if_not_exists(id=CONTAINER_NAME, partition_key=PartitionKey(path="/userId"))
        
        create_items(container)

        response = input(f"The database => {DATABASE_NAME}, container => {CONTAINER_NAME}, and items have been successfully created! Are you ready to delete them (yes/no)?")
        if response in ("no", "n"):
            end()
        elif response in ("yes", "y"):
            delete_items(container, database, client)
        else:
            print("***Invalid option entered - Yes or No expected***")
   
    except exceptions.CosmosHttpResponseError as e:
        print(f"Oops! Encountered an error: {e.message}")

if __name__ == '__main__':
    run_sample()
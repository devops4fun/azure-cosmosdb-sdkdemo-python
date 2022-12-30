# azure-cosmosdb-sdkdemo-python
Interact with Azure CosmosDB via sdk for Python

Azure provides several SDKs to interact with the CosmosDB service. Here is a demo script leveraging the SDK to accomplish the following activities:
1. Instantiate the [CosmosClient](https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos.cosmosclient?view=azure-python) class create a client object. 
2. Use the client object to create a new new database, container within CosmosDB.
3. Populate the CosmosDB container the items stored in the `users.json` file within this rep. to Azure via the `Python SDK` (samplerun.py).
4. Clean-up (i.e. delete) the resources created during the demo.

### Pre-requisites
1. An [Azure Resource group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal) must exist within a valid azure account.
2. A [CosmosDB Account](https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-database-account) must exist within the Azure Resource group in step 1.
3. Update the `custom_vars.json` file with the relevant variables for your environment.

## Instructions
1. Complete Pre-requisites above

2. Run the samplerun.py
```
python samplerun.py
```
3. Verify resources (database, container, items) have been deployed.

4. Consent to Clean-up
```
The database => mydatabasename, container => mycontainername, and items have been successfully created! Are you ready to delete them (yes/no)? yes
```



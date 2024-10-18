import time
import sys
import json
from jsonpath_ng.ext import parse
import cursor
from CheckLabs import *
import random
from Sentences import *
import ntnx_networking_py_client.models.networking.v4.config as v4NetConfig
import ntnx_networking_py_client.models.networking.v4.config 
import ntnx_iam_py_client
import ntnx_iam_py_client.configuration as iamConfig

# ========================================================================
# = retrieveUserId
# ========================================================================
# Function to retrieve the extId of a specific subnet
def retrieveUserId(userName, variables):

    # Configure the client
    sdkConfig = ntnx_networking_py_client.Configuration()
    sdkConfig.host = variables['PC']
    sdkConfig.port = 9440
    sdkConfig.maxRetryAttempts = 3
    sdkConfig.backoffFactor = 3
    sdkConfig.username = variables['PCUser']
    sdkConfig.password = variables['PCPassword']
    sdkConfig.verify_ssl = False

    client = ntnx_iam_py_client.ApiClient(configuration=sdkConfig)
    usersApi = ntnx_iam_py_client.UsersApi(api_client=client)

    response = usersApi.list_users(_filter="username eq '" + str(userName) + "'")
    myData = response.to_dict()

    if myData['data']:
        return myData['data'][0]['ext_id']
    else:
        return None
    
# ========================================================================
# = getUserById
# ========================================================================    
# Function to retrieve the extId of a specific subnet
def getUserById(extId, variables):

    # Configure the client
    sdkConfig = ntnx_networking_py_client.Configuration()
    sdkConfig.host = variables['PC']
    sdkConfig.port = 9440
    sdkConfig.maxRetryAttempts = 3
    sdkConfig.backoffFactor = 3
    sdkConfig.username = variables['PCUser']
    sdkConfig.password = variables['PCPassword']
    sdkConfig.verify_ssl = False

    client = ntnx_iam_py_client.ApiClient(configuration=sdkConfig)
    usersApi = ntnx_iam_py_client.UsersApi(api_client=client)

    response = usersApi.get_user_by_id(extId=extId)
    myData = response.to_dict()

    if myData['data']:
        return myData['data'][0]
    else:
        return None
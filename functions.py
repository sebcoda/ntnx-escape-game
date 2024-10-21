from CheckLabs import *
from Sentences import *
import ntnx_networking_py_client.models.networking.v4.config 
import ntnx_iam_py_client

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
# = retrieveUserId
# ========================================================================
# Function to retrieve the extId of a specific subnet
def retrieveRoleId(roleName, variables):

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
    roleApi = ntnx_iam_py_client.RolesApi(api_client=client)

    response = roleApi.list_roles(_filter="displayName eq '" + str(roleName) + "'")
    myData = response.to_dict()

    if myData['data']:
        return myData['data'][0]['ext_id']
    else:
        return None
    
# ========================================================================
# = retrieveAuthorizationPolicyId
# ========================================================================
# Function to retrieve the extId of a specific authorization policy
def retrieveAuthorizationPolicyId(policyName, variables):

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
    authorizationPoliciesApi = ntnx_iam_py_client.AuthorizationPoliciesApi(api_client=client)

    response = authorizationPoliciesApi.list_authorization_policies(_filter="displayName eq '" + str(policyName) + "'")
    myData = response.to_dict()

    if myData['data']:
        return myData['data'][0]['ext_id']
    else:
        return None
    

# ========================================================================
# = checkAuthorizationPolicyAssignement
# ========================================================================
# Function to check if the assignment is correct
def checkAuthorizationPolicyAssignement(authorizationPolicyId, roleId, userId, variables):

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
    authorizationPoliciesApi = ntnx_iam_py_client.AuthorizationPoliciesApi(api_client=client)

    response = authorizationPoliciesApi.get_authorization_policy_by_id(extId=authorizationPolicyId)
    myData = response.to_dict()

    # Check if the correct role is assigned
    if myData['data']['role'] != roleId:
        return False
    
    # Check if the correct user is assigned in any of the identities
    user_assigned = any(identity['_reserved']['user']['uuid']['anyof'][0] == userId for identity in myData['data']['identities'])
    if not user_assigned:
        return False
    
    # If everything is correct, return True
    return True
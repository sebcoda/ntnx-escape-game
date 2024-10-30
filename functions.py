from CheckLabs import *
from Sentences import *
import ntnx_networking_py_client.models.networking.v4.config 
import ntnx_iam_py_client
import ntnx_networking_py_client
import ntnx_vmm_py_client
import ntnx_prism_py_client
import requests
import json

# ========================================================================
# = configSdkClient
# ========================================================================
def confSDKClient(host, user, password, ssl=False):
    
    # Configure the client
    sdkConfig = ntnx_networking_py_client.Configuration()
    sdkConfig.host = host
    sdkConfig.port = 9440
    sdkConfig.maxRetryAttempts = 3
    sdkConfig.backoffFactor = 3
    sdkConfig.username = user
    sdkConfig.password = password
    sdkConfig.verify_ssl = ssl

    return sdkConfig

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
# = retrieveRoleId
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

# ========================================================================
# = retrieveProjectInfo
# ========================================================================
# Function that is returning the extId of a project
def retrieveProjectInfo(projectName, variables):

    url = "https://%s:9440/api/nutanix/v3/projects/list" % variables['PC']
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload={}

    response = requests.post(url, json=payload, headers=headers, verify=False, auth=(variables['PCUser'], variables['PCPassword']))
    response_data = response.json()

    if len(response_data['entities']) != 0:
        for project in response_data['entities']:
            if project['status']['name'] == projectName:
                return project
    
    return None


# ========================================================================
# = retrieveSubnetID
# ========================================================================
# Function that is returning the extId of a subnet
def retrieveSubnetID(subnet_name, variables):

    # Configure the client
    sdkConfig = confSDKClient(variables['PC'], variables['PCUser'], variables['PCPassword'])

    client = ntnx_networking_py_client.ApiClient(configuration=sdkConfig)
    subnets_api = ntnx_networking_py_client.SubnetsApi(api_client=client)

    response=subnets_api.list_subnets(_filter="name eq '" + subnet_name + "'")
    myData = response.to_dict()

    # Check if we got an id
    if myData['data']==None or len(myData['data']) != 1:
        return None
        
    # If everything is correct, return True
    return True 

# ========================================================================
# = retrieveImageID
# ========================================================================
# Function that is returning the extId of an image
# Note : developped in v3 API because Python SDK seems to be broken (list_images URL is not found, 404 error)
# SDK Ref : https://developers.nutanix.com/sdk-reference?namespace=vmm&version=v4.0.b1&language=python
def retrieveImageID(image_name, variables):

    url = "https://%s:9440/api/nutanix/v3/images/list" % variables['PC']
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload={
        "kind": "image",
        "length": 100,
        }

    response = requests.post(url, json=payload, headers=headers, verify=False, auth=(variables['PCUser'], variables['PCPassword']))
    response_data = response.json()

    for image in response_data['entities']:
        if image['status']['name'] == image_name:
            return image['metadata']['uuid']
        
    return None

# ========================================================================
# = retrieveVMInfo
# ========================================================================
def retrieveVMInfo(vm_name, variables):

    # Configure the client
    sdkConfig = confSDKClient(variables['PC'], variables['PCUser'], variables['PCPassword'])

    client = ntnx_vmm_py_client.ApiClient(configuration=sdkConfig)
    vms_api = ntnx_vmm_py_client.VmApi(api_client=client)

    response=vms_api.list_vms(_filter="name eq '" + vm_name + "'")
    myData = response.to_dict()

    # Check if we got an id
    if myData['data']==None or len(myData['data']) != 1:
        return False, {}
    
    vmUUID=myData['data'][0]['ext_id']
    
    response=vms_api.get_vm_by_ext_id(vmUUID)
    myData=response.to_dict()

    # If everything is correct, return True
    return True, myData['data']

# ========================================================================
# = getVMProjectUUID
# ========================================================================
# GL Todo : write with SDK when available
def getVMProjectUUID(vmuuid, pc, user, password):
    url = "https://%s:9440/api/nutanix/v3/vms/%s"% (pc,vmuuid)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, verify=False, auth=(user, password))
    response_data = response.json()

    return response_data['metadata']['project_reference']['uuid']

# ========================================================================
# = hasVMCloudinit
# ========================================================================
# GL Todo : write with SDK when available
def hasVMCloudinit(vmuuid, pc, user, password):
    url = "https://%s:9440/api/nutanix/v3/vms/%s"% (pc,vmuuid)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, verify=False, auth=(user, password))
    response_data = response.json()

    if response_data['spec']['resources']['guest_customization'] == None:
        return False
    
    return True

# ========================================================================
# = retrieveCatID
# ========================================================================
def retrieveCatID( key, value, variables):
    
    sdkConfig = confSDKClient(variables['PC'], variables['PCUser'], variables['PCPassword'])
    page = 0
    limit = 50

    client = ntnx_prism_py_client.ApiClient(configuration=sdkConfig)
    categories_api = ntnx_prism_py_client.CategoriesApi(api_client=client)

    if value == None:
        try:
            api_response = categories_api.get_all_categories(_page=page, _limit=limit,_filter="key eq '" + key + "'")
            myData=api_response.to_dict()

            if myData['data'] == None:
                return False, None
            else:
                return True, myData['data'][0]['ext_id']

        except ntnx_prism_py_client.rest.ApiException as e:
            print(e)
    else:
        try:
            api_response = categories_api.get_all_categories(_page=page, _limit=limit,_filter="key eq '" + key + "' and value eq '" + value + "'")
            myData=api_response.to_dict()
            
            if myData['data'] == None:
                return False, None
            else:
                return True, myData['data'][0]['ext_id']

        except ntnx_prism_py_client.rest.ApiException as e:
            print(e)            

# ========================================================================
# = retrieveStoragePolicyID
# ========================================================================
# Function that is returning the extId of a storage policy
# GL Todo : write with SDK when available

def retrieveStoragePolicyID(policy_name, variables):

    url = "https://%s:9440/api/nutanix/v3/storage_policies/list" % variables['PC']
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {}

    response = requests.post(url, json=payload, headers=headers, verify=False, auth=(variables['PCUser'], variables['PCPassword']))
    response_data = response.json()

    for policy in response_data['entities']:
        if policy['status']['name'] == policy_name:
            return policy['metadata']['uuid']

    return None

# ========================================================================
# = retrieveSecurityPolicyID
# ========================================================================
# Function that is returning the extId of a security policy
def retrieveSecurityPolicyID(policy_name, variables):

    url = "https://%s:9440/api/microseg/v4.0.b1/config/policies?((type eq Schema.Enums.SecurityPolicyType'APPLICATION'))" % variables['PC']
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, verify=False, auth=(variables['PCUser'], variables['PCPassword']))
    response_data = response.json()

    for policy in response_data['data']:
        if policy['name'] == policy_name:
            return policy['extId']

    return None

# ========================================================================
# = retrieveProtectionPolicyInfo
# ========================================================================
# Function that is returning the info of a protection policy
def retrieveProtectionPolicyInfo(policy_name, variables):

    url = "https://%s:9440/api/nutanix/v3/protection_rules/list" % variables['PC']
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {}

    response = requests.post(url, json=payload, headers=headers, verify=False, auth=(variables['PCUser'], variables['PCPassword']))
    response_data = response.json()

    for policy in response_data['entities']:
        if policy['status']['name'] == policy_name:
            
            # We found the policy, let's return the details
            poluuid=policy['metadata']['uuid']

            url = "https://%s:9440/api/nutanix/v3/protection_rules/%s" % (variables['PC'], poluuid)

            response2 = requests.get(url, json=payload, headers=headers, verify=False, auth=(variables['PCUser'], variables['PCPassword']))

            return response2.json()

    return None

# ========================================================================
# = retrieveApprovalPolicyInfo
# ========================================================================
# Function that is returning the info of a Approval policy
# GL ToDo : write with SDK when available
def retrieveApprovalPolicyInfo( policy_name, variables):

    url = "https://%s:9440/api/security/v4.0.a1/dashboard/approval-policies" % variables['PC']
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {}

    response = requests.get(url, json=payload, headers=headers, verify=False, auth=(variables['PCUser'], variables['PCPassword']))
    response_data = json.loads(response.text)

    if response_data['data'][0]['name'] == variables['ApprovalPolicy']:
        return response_data['data'][0]
    else:
        return None


    

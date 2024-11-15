# Put here all the actions that can be used by the #>A:<action name>#" calls
    
import ntnx_vmm_py_client
from functions import *
import requests
from base64 import b64encode


# ====================================================================================================
# lowercaseTrigram - Done
# ====================================================================================================
# This fonction store trigram in lowercase

def lowercaseTrigram(variables):
    variables['Trigram'] = variables['Trigram'].lower()
    return True

# ====================================================================================================
# lowercaseTrigram - Done
# ====================================================================================================
# This function delete VM identified in the variables
def DeleteVM(variables):

    # Configure the client
    sdkConfig = confSDKClient(variables['PC'], variables['PCUser'], variables['PCPassword'])
    client = ntnx_vmm_py_client.ApiClient(configuration=sdkConfig)
    vm_api = ntnx_vmm_py_client.VmApi(api_client=client)
  

    try:
        api_response = vm_api.get_vm_by_ext_id(extId=variables['VMUUID'])
    except ntnx_vmm_py_client.rest.ApiException as e:
        print(e)

    # Extract E-Tag Header
    etag_value = ntnx_vmm_py_client.ApiClient.get_etag(api_response)

    try:
        api_response = vm_api.delete_vm(extId=variables['VMUUID'], if_match=etag_value)
    except ntnx_vmm_py_client.rest.ApiException as e:
        print(e)

    return True

# ====================================================================================================
# DeployBP - WIP
# ====================================================================================================
# To Do : Migrate to v4 API/SDK when available
def DeployBP( variables ):
    
    # Get BP from github
    url = "https://raw.githubusercontent.com/Golgautier/ntnx-escape-game/refs/heads/main/blueprint/NewVM.json?token=GHSAT0AAAAAACWL3ED3FL3LF2LCFKPFT5MEZZTGOBA"
    response = requests.get(url)

    with open("newvm.json", "wb") as file:
        #GL file.write(response.content)
        print("GL")

    with open("newvm.json", "r") as file:
        content=file.read()

    url = "https://%s:9440/api/nutanix/v3/blueprints/import_json" % variables['PC']


    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = content

    response = requests.post(url, json=payload, headers=headers, verify=False, auth=(variables['PCUser'], variables['PCPassword']))

    return True


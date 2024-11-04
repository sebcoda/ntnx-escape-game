# Put here all the actions that can be used by the #>A:<action name>#" calls
    
import ntnx_vmm_py_client
from functions import *


# ====================================================================================================
# lowercaseTrigram - Done
# ====================================================================================================
# This fonction store trigram in lowercase

def lowercaseTrigram(variables):
    variables['Trigram'] = variables['Trigram'].lower()
    return True

# ====================================================================================================
# lowercaseTrigram - To be done
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

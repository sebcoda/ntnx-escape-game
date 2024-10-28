from functions import *

# =============================================================================
# CheckUSer - Done
# =============================================================================
def CheckUser(variables):
    from functions import retrieveUserId, retrieveRoleId, retrieveAuthorizationPolicyId, checkAuthorizationPolicyAssignement

    result = True
    clue = ''

    #retrieve the user by filtering by name
    userId = retrieveUserId(userName=variables['Trigram'] + "-adm", variables=variables) #non existing user
    if userId is None:
        result=False
        clue="The user " + variables['Trigram'] + "-adm hasn't been found. Are you sure you've created it with the correct name?"
        
        return result, clue
    
    # Store UserUUID in the variables
    variables['UserUUID'] = userId

    #retrieve the Super Admin role ID
    roleId = retrieveRoleId(roleName="Super Admin", variables=variables)

    #retrieve the authorization policy ID
    authorizationPolicyId = retrieveAuthorizationPolicyId(policyName=variables['Trigram'] + "-auth", variables=variables)

    if authorizationPolicyId is None:
        result=False
        clue="The authorization policy  " + variables['Trigram'] + "-auth is not created as requested. Are you sure you've created it with the correct name?"
        
        return result, clue
    
    #check if the authorization policy is associated to the correct role and user
    response = checkAuthorizationPolicyAssignement(authorizationPolicyId=authorizationPolicyId, roleId=roleId, userId=userId, variables=variables)

    if response is False: 
        result=False
        clue="The authorization policy  " + variables['Trigram'] + "-auth exist, but is not correctly assigning the role to the user. Are you sure you've assigned the correct ressources?"
        
        return result, clue
        
    return result, clue

# =============================================================================
# CheckProject - Done
# =============================================================================
def CheckProject(variables):
    from functions import retrieveProjectId

    result = True
    clue = ''

    response = retrieveProjectId(projectName=variables['Trigram'] + "-proj", variables=variables)

    if response is None: 
        result=False
        clue="The project " + variables['Trigram'] + "-proj doesn't exist. Are you sure you named it correctly?"
        
        return result, clue

    # We store ProjectUUID in the variables to be used later
    variables['ProjectUUID'] = response
    return result, clue
    
# =============================================================================
# CheckNetwork - Done
# =============================================================================
# Notes : We only verify if subnet, we do not really care of the configuration, as
# it is not used later in the game
def CheckNetwork(variables):
    
    clue=''
    result=True

    response = retrieveSubnetID(subnet_name=variables['Trigram'] + "-subnet", variables=variables)

    if response is None: 
        result=False
        clue="The subnet " + variables['Trigram'] + "-subnet is not on the cluster. Are you sure you named it correctly?"
        
        return result, clue
    
    # We store networkUUID in the variables to be used later
    variables['NetworkUUID'] = response

    return result, clue

# =============================================================================
# CheckImage - Done
# =============================================================================
def CheckImage(variables):

    clue=''
    result=True

    response = retrieveImageID(image_name=variables['Trigram'] + "-ubuntu", variables=variables)

    if response is None: 
        result=False
        clue="Are you sure you created the image " + variables['Trigram'] + "-ubuntu ? I do not see it?"
        
        return result, clue

    # We store ImageUUID in the variables to be used later
    variables['ImageUUID'] = response

    return result, clue

# =============================================================================
# CheckImage - WIP
# =============================================================================
def CheckVM(variables):

    clue=''
    result=True

    found,response = retrieveVMInfo(vm_name=variables['Trigram'] + "-vm", variables=variables)

    if found == False: 
        result=False
        clue="The VM " + variables['Trigram'] + "-vm is not on the cluster. Are you sure you named it correctly?"
        
        return result, clue
    else:
        # Check all other information

        # Check owner
        if response['ownership_info']['owner']['ext_id'] != variables['UserUUID']:
            result=False
            clue="The VM is not owned by the user " + variables['Trigram'] + "-adm. Can you fix it ?"
            
            return result, clue

        # Number of NICS
        if len(response['nics']) != 2:
            result=False
            clue="The VM " + variables['Trigram'] + "-vm should have 2 NICs. Are you sure you've configured it properly?"
            
            return result, clue

        # Check network connection on our subnet
        if ( response['nics'][0]['network_info']['subnet']['ext_id'] != variables['NetworkUUID']) and (response['nics'][1]['network_info']['subnet']['ext_id'] != variables['NetworkUUID'] ):
            result=False
            clue="The VM " + variables['Trigram'] + "-vm should be connected to the network " + variables['Trigram'] + "-subnet. It looks like it is not done. Can you check ?"
            
            return result, clue
        
        # Check image used
        if response['disks'][0]['backing_info']['data_source']['reference']['image_ext_id'] != variables['ImageUUID']:
            result=False
            clue="The VM " + variables['Trigram'] + "-vm should be based on the image " + variables['Trigram'] + "-ubuntu. It seems not to be the case. Can you fix it ?"
            
            return result, clue

        # Check owner
        if response['disks'][0]['backing_info']['data_source']['reference']['image_ext_id'] != variables['ImageUUID']:
            result=False
            clue="The VM " + variables['Trigram'] + "-vm should be based on the image " + variables['Trigram'] + "-ubuntu. It seems not to be the case. Can you fix it ?"
            
            return result, clue

        # Project
        # GL ToDo : Migrate to v4/SDK when project will be available in SDK
        if getVMProjectUUID(response['ext_id'],pc=variables['PC'], user=variables['PCUser'],password=variables['PCPassword']) != variables['ProjectUUID']:
            result=False
            clue="The VM " + variables['Trigram'] + "-vm should be in the project " + variables['Trigram'] + "-proj. It seems not to be the case. Can you fix it ?"
            
            return result, clue
        
        # Cloud Init
        # GL ToDo : Migrate to v4/SDK when guest-customization will be available in SDK
        if hasVMCloudinit(response['ext_id'],pc=variables['PC'], user=variables['PCUser'],password=variables['PCPassword']) == False:
            result=False
            clue="Your should have cloud-init configured. It seems not to be the case. Can you fix it or I won't able to connect on ? You'll have to recreate it, unfortunately."
            
            return result, clue

        # Power State
        if response['power_state'] != 'ON':
            result=False
            clue="The VM " + variables['Trigram'] + "-vm is not powered on. Are you sure you started it?"
            
            return result, clue

    # Store VMUUID and HostUUID in the variables to be used later
    variables['VMUUID'] = response['ext_id']
    variables['HostUUID'] = response['host']['ext_id']

    return result, clue

def CheckCat(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckStoragePolicy(variables):
    clue=''
    result=True

    response = retrieveStoragePolicyID(policy_name=variables['Trigram'] + "-policy", variables=variables)

    if response is None: 
        result=False
        clue="Are you sure you created the storage policy " + variables['Trigram'] + "-policy ? I did not find it?"
        
        return result, clue

    # We store ImageUUID in the variables to be used later
    variables['StoragePolicyUUID'] = response

    return result, clue

def CheckSecurityPolicy(variables):
    clue=''
    result=True

    response = retrieveSecurityPolicyID(policy_name=variables['Trigram'] + "-policy", variables=variables)

    if response is None: 
        result=False
        clue="Are you sure you created the security policy " + variables['Trigram'] + "-policy ? I guess you should double check ;-) ?"
        
        return result, clue

    # We store ImageUUID in the variables to be used later
    variables['SecurityPolicyUUID'] = response

    return result, clue

def CheckSecurityPolicy2(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckProtectionPolicy(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckApprovalPolicy(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckRestoreVM(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckReport(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckNewNode(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckRunway(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue
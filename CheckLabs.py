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


    result = True
    clue = ''

    response = retrieveProjectInfo(projectName=variables['Trigram'] + "-proj", variables=variables)

    if response is None: 
        result=False
        clue="The project " + variables['Trigram'] + "-proj doesn't exist. Are you sure you named it correctly?"
        
        return result, clue
    else:
        # We check if infrastructure is correctly set
        if len(response['spec']['resources']['account_reference_list']) == 0:
            result=False
            clue="The project " + variables['Trigram'] + "-proj doesn't have any cluster associated. Can you fix it ?"
            
            return result, clue
        
        # We check users
        if len(response['spec']['resources']['external_user_group_reference_list']) == 0:
            result=False
            clue="The project " + variables['Trigram'] + "-proj doesn't have any user associated. Can you fix it ?"
            
            return result, clue

        # We store ProjectUUID in the variables to be used later
        variables['ProjectUUID'] = response['metadata']['uuid']
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
# CheckImage - Done
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
        # GL : Currently disabled because user must be in an IDP to be associated to a project.
        #      User <Trigram>-adm is local
        #
        # if response['ownership_info']['owner']['ext_id'] != variables['UserUUID']:
        #     result=False
        #     clue="The VM is not owned by the user " + variables['Trigram'] + "-adm. Can you fix it ?"
            
        #     return result, clue

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

# =============================================================================
# CheckCat - Done
# =============================================================================
def CheckCat(variables):
    clue=''
    result=True

    found,_ = retrieveCatID(variables['Trigram'] + "-cat", None, variables=variables)

    # Check for category key first
    if not found: 
        result=False
        clue="The category " + variables['Trigram'] + "-cat doesn't exist. Are you sure you named it correctly?"
        
        return result, clue
    
    # Check for Value "Test"
    found,_ = retrieveCatID(variables['Trigram'] + "-cat", "Test", variables=variables)
    if not found: 
        result=False
        clue="The category " + variables['Trigram'] + "-cat exists, But I do not see the 'Test' value..."
        
        return result, clue
    

    # Check for Value "Critical"
    found,uuid = retrieveCatID(variables['Trigram'] + "-cat", "Critical", variables=variables)
    if not found: 
        result=False
        clue="The category " + variables['Trigram'] + "-cat exists, But I do not see the 'Critical' value..."
        
        return result, clue
    else:
        variables['CatUUID'] = uuid        

    return result, clue

# =============================================================================
# CheckStoragePolicy - Done
# =============================================================================
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

# =============================================================================
# CheckSecurityPolicy - WIP
# =============================================================================
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

# =============================================================================
# CheckProtectionPolicy - Done
# =============================================================================
def CheckProtectionPolicy(variables):
    clue=''
    result=True
    
    info = retrieveProtectionPolicyInfo(variables['Trigram'] + "-policy", variables=variables)

    if info == None:
        clue="Are you sure you created the protection policy " + variables['Trigram'] + "-policy ? I did not find it?"
        
        return False, clue
    else:
        # We check policy details

        # Schedule
        if info['spec']['resources']['availability_zone_connectivity_list'][0]['snapshot_schedule_list'][0]['recovery_point_objective_secs'] != 3600:
            clue="It looks like the snapshot schedule is not set to 1 hour. Can you fix it ?"            
            return False, clue

        # Retention
        if info['spec']['resources']['availability_zone_connectivity_list'][0]['snapshot_schedule_list'][0]['local_snapshot_retention_policy']['rollup_retention_policy']['multiple'] != 1 or info['spec']['resources']['availability_zone_connectivity_list'][0]['snapshot_schedule_list'][0]['local_snapshot_retention_policy']['rollup_retention_policy']['snapshot_interval_type'] != 'DAILY':
            clue="It looks like the snapshot retention is not set to 1 day. Can you fix it ?"            
            return False, clue

        # Categories
        cat=variables['Trigram']+"-cat"

        if cat not in info['status']['resources']['category_filter']['params'].keys():
            clue="It looks like the category filter is not set correctly. Can you fix it ?"            
            return False, clue
        
        # Category value
        if info['status']['resources']['category_filter']['params'][cat] == 'Critical':
            clue="It looks like the category value is not set correctly. Can you fix it ?"
            return False, clue

        variables['ProtectionPolicyUUID'] = info['metadata']['uuid']


    return True, clue


# =============================================================================
# CheckApprovalPolicy - Done
# =============================================================================
def CheckApprovalPolicy(variables):
    clue=''
    result=True

    response = retrieveApprovalPolicyInfo(variables['ApprovalPolicy'], variables=variables)

    # We check if policy is created
    if response is None: 
        result=False
        clue="Are you sure you created the approval policy " + variables['ApprovalPolicy'] + " ? I did not see it?"
        
        return result, clue
    else:
        # We check policy details

        # Approvers
        # Not tested, because of useless for next steps

        # targeted protection policy
        if 'securedPolicies' in response.keys(): 
            for item in response['securedPolicies']:
                if item['policyUuid'] == variables['ProtectionPolicyUUID']:
                    return True, ""
            
        return False, "The approval policy is not linked to the protection policy. Can you fix it ?"

# =============================================================================
# CheckRestoreVM - Done
# =============================================================================
def CheckRestoreVM(variables):
    clue=''
    result=True

    found,response = retrieveVMInfo(vm_name=variables['Trigram'] + "-vm", variables=variables)

    if found == False: 
        result=False
        clue="The VM " + variables['Trigram'] + "-vm is not on the cluster. Are you sure you named it correctly?"
        
        return result, clue

    return result, clue

# =============================================================================
# CheckLiveMigration - Done
# =============================================================================
def CheckLiveMigration(variables):
   
    found,response = retrieveVMInfo(vm_name=variables['Trigram'] + "-vm", variables=variables)

    if found and variables['HostUUID'] != response['host']['ext_id']:
        return True,""
    else:
        return False, "The VM is still on the same host, move it right now please !"
    
# =============================================================================
# CheckLiveMigration - WIP
# =============================================================================
def CheckReport(variables):
    clue=''
    result=True

    found, info = retrieveReportInfo(variables['Trigram'] + "-report", variables=variables)

    if not found:
        result=False
        clue="The report " + variables['Trigram'] + "-report is not on the cluster. Are you sure you named it correctly?"
        
        return result, clue
    else:
        # We check report config

        # Schedule
        if info['spec']['resources']['schedule']['interval_type'] != 'DAILY':
            clue="The report " + variables['Trigram'] + "-report should be scheduled daily. Can you fix it ?"
            
            return False, clue

        # Recipients
        if not (len(info['spec']['resources']['notification_policy']['email_config']['recipient_list'])!=0 and info['spec']['resources']['notification_policy']['email_config']['recipient_list'][0]['email_address']==variables['EmailReport']):
            clue="The report does not have te good recipient. Can you check that ?"
            return False, clue

        # Content
        listvm=False
        for elt in info['spec']['resources']['template']['template_rows']:
            if elt['row_element_list'][0]['widget_config']['entity_type'] == 'vm':
                listvm=True

        if listvm == False:
            clue="The report " + variables['Trigram'] + "-report should list VMs. Can you fix it ?"
            
            return False, clue

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
from functions import *
from jsonpath_ng.ext import parse

scoreFile="score.json"

# Here are all the functions called by the game content to check labs
# Each function returns a tuple (result, clue, variable name)
# - result is a boolean (True if the check is OK, False otherwise)
# - clue is a string that will be displayed to the user why the check is not OK
# - variable name is the name of the dictionary key containing the value we check to validate the exercise. This value will be reasked by the engine if check is false



# =============================================================================
# NeedRecovery - Done
# =============================================================================
def NeedRecovery(variables,recoveryMode):
    with open(scoreFile, 'r') as file:
        data = json.load(file)
        
    jsonpath_expr=parse("score[?(@.player=="+variables['Trigram']+")].value")

    for match in jsonpath_expr.find(data):
        if match.value > 1:
            variables['RecoveryUntilStage']=match.value
            print("\n\nSpecial event : Entering in recovery mode....\n\n")

    return True, '', None


# =============================================================================
# CheckUSer - Done
# =============================================================================
def CheckUser(variables,recoveryMode):
    from functions import retrieveUserId, retrieveRoleId, retrieveAuthorizationPolicyId, checkAuthorizationPolicyAssignement

    result = True
    clue = ''

    #retrieve the user by filtering by name
    userId = retrieveUserId(userName=variables['Trigram'] + "-adm", variables=variables) #non existing user
    if userId is None:
        result=False
        clue="The user " + variables['Trigram'] + "-adm hasn't been found. Are you sure you've created it with the correct name?"
        
        return result, clue, None
    
    # Store UserUUID in the variables
    variables['UserUUID'] = userId

    #retrieve the Super Admin role ID
    roleId = retrieveRoleId(roleName="Super Admin", variables=variables)

    #retrieve the authorization policy ID
    authorizationPolicyId = retrieveAuthorizationPolicyId(policyName=variables['Trigram'] + "-auth", variables=variables)

    if authorizationPolicyId is None:
        result=False
        clue="The authorization policy  " + variables['Trigram'] + "-auth is not created as requested. Are you sure you've created it with the correct name?"
        
        return result, clue, None
    
    #check if the authorization policy is associated to the correct role and user
    response = checkAuthorizationPolicyAssignement(authorizationPolicyId=authorizationPolicyId, roleId=roleId, userId=userId, variables=variables)

    if response is False: 
        result=False
        clue="The authorization policy  " + variables['Trigram'] + "-auth exist, but is not correctly assigning the role to the user. Are you sure you've assigned the correct ressources?"
        
        return result, clue, None
        
    return result, clue, None

# =============================================================================
# CheckProject - Done
# =============================================================================
def CheckProject(variables,recoveryMode):


    result = True
    clue = ''

    response = retrieveProjectInfo(projectName=variables['Trigram'] + "-proj", variables=variables)

    if response is None: 
        result=False
        clue="The project " + variables['Trigram'] + "-proj doesn't exist. Are you sure you named it correctly?"
        
        return result, clue, None
    else:
        # We check if infrastructure is correctly set
        if len(response['spec']['resources']['account_reference_list']) == 0:
            result=False
            clue="The project " + variables['Trigram'] + "-proj doesn't have any cluster associated. Can you fix it ?"
            
            return result, clue, None
        
        # We check users
        if len(response['spec']['resources']['external_user_group_reference_list']) + len(response['spec']['resources']['account_reference_list']) == 0:
            result=False
            clue="The project " + variables['Trigram'] + "-proj doesn't have any user associated. Can you fix it ?"
            
            return result, clue, None

        # We store ProjectUUID in the variables to be used later
        variables['ProjectUUID'] = response['metadata']['uuid']
        return result, clue, None
    
# =============================================================================
# CheckNetwork - Done
# =============================================================================
# Notes : We only verify if subnet, we do not really care of the configuration, as
# it is not used later in the game
def CheckNetwork(variables,recoveryMode):
    
    clue=''
    result=True

    response = retrieveSubnetID(subnet_name=variables['Trigram'] + "-subnet", variables=variables)

    if response is None: 
        result=False
        clue="The subnet " + variables['Trigram'] + "-subnet is not on the cluster. Are you sure you named it correctly?"
        
        return result, clue, None
    
    # We store networkUUID in the variables to be used later
    variables['NetworkUUID'] = response

    return result, clue, None

# =============================================================================
# CheckImage - Done
# =============================================================================
def CheckImage(variables,recoveryMode):

    clue=''
    result=True

    response = retrieveImageID(image_name=variables['Trigram'] + "-ubuntu", variables=variables)

    if response is None: 
        result=False
        clue="Are you sure you created the image " + variables['Trigram'] + "-ubuntu ? I do not see it?"
        
        return result, clue, None

    # We store ImageUUID in the variables to be used later
    variables['ImageUUID'] = response

    return result, clue, None

# =============================================================================
# CheckImage - Done
# =============================================================================
def CheckVM(variables,recoveryMode):

    clue=''
    result=True

    found,response = retrieveVMInfo(vm_name=variables['Trigram'] + "-vm", variables=variables)

    if found == False: 
        result=False
        clue="The VM " + variables['Trigram'] + "-vm is not on the cluster. Are you sure you named it correctly?"
        
        return result, clue, None
    elif recoveryMode == False:
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
            
            return result, clue, None

        # Check network connection on our subnet
        if ( response['nics'][0]['network_info']['subnet']['ext_id'] != variables['NetworkUUID']) and (response['nics'][1]['network_info']['subnet']['ext_id'] != variables['NetworkUUID'] ):
            result=False
            clue="The VM " + variables['Trigram'] + "-vm should be connected to the network " + variables['Trigram'] + "-subnet. It looks like it is not done. Can you check ?"
            
            return result, clue, None
        
        # Check image used
        if response['disks'][0]['backing_info']['data_source']['reference']['image_ext_id'] != variables['ImageUUID']:
            result=False
            clue="The VM " + variables['Trigram'] + "-vm should be based on the image " + variables['Trigram'] + "-ubuntu. It seems not to be the case. Can you fix it ?"
            
            return result, clue, None

        # Check owner
        if response['disks'][0]['backing_info']['data_source']['reference']['image_ext_id'] != variables['ImageUUID']:
            result=False
            clue="The VM " + variables['Trigram'] + "-vm should be based on the image " + variables['Trigram'] + "-ubuntu. It seems not to be the case. Can you fix it ?"
            
            return result, clue, None

        # Project
        # GL ToDo : Migrate to v4/SDK when project will be available in SDK
        if getVMProjectUUID(response['ext_id'],pc=variables['PC'], user=variables['PCUser'],password=variables['PCPassword']) != variables['ProjectUUID']:
            result=False
            clue="The VM " + variables['Trigram'] + "-vm should be in the project " + variables['Trigram'] + "-proj. It seems not to be the case. Can you fix it ?"
            
            return result, clue, None
        
        # Cloud Init
        # GL ToDo : Migrate to v4/SDK when guest-customization will be available in SDK
        if hasVMCloudinit(response['ext_id'],pc=variables['PC'], user=variables['PCUser'],password=variables['PCPassword']) == False:
            result=False
            clue="Your should have cloud-init configured. It seems not to be the case. Can you fix it or I won't able to connect on ? You'll have to recreate it, unfortunately."
            
            return result, clue, None

        # Power State
        if response['power_state'] != 'ON':
            result=False
            clue="The VM " + variables['Trigram'] + "-vm is not powered on. Are you sure you started it?"
            
            return result, clue, None

    # Store VMUUID and HostUUID in the variables to be used later
    variables['VMUUID'] = response['ext_id']
    variables['HostUUID'] = response['host']['ext_id']

    return result, clue, None

# =============================================================================
# CheckCat - Done
# =============================================================================
def CheckCat(variables,recoveryMode):
    clue=''
    result=True     

    found,_ = retrieveCatID(variables['Trigram'] + "-cat", None, variables=variables)

    # Check for category key first
    if not found: 
        result=False
        clue="The category " + variables['Trigram'] + "-cat doesn't exist. Are you sure you named it correctly?"
        
        return result, clue, None
    
    # Check for Value "Test"
    found,_ = retrieveCatID(variables['Trigram'] + "-cat", "Test", variables=variables)
    if not found: 
        result=False
        clue="The category " + variables['Trigram'] + "-cat exists, But I do not see the 'Test' value..."
        
        return result, clue, None
    

    # Check for Value "Critical"
    found,uuid = retrieveCatID(variables['Trigram'] + "-cat", "Critical", variables=variables)
    if not found: 
        result=False
        clue="The category " + variables['Trigram'] + "-cat exists, But I do not see the 'Critical' value..."
        
        return result, clue, None
    else:
        variables['CatUUID'] = uuid        

    return result, clue, None

# =============================================================================
# CheckCatVM - Done
# =============================================================================
def CheckCatVM(variables,recoveryMode):
    clue=''
    result=True
    
    if recoveryMode:
        return True, '', None

    found,response = retrieveVMInfo(vm_name=variables['Trigram'] + "-vm", variables=variables)

    for tmp in response['categories']:
        if variables['CatUUID'] == tmp['ext_id']:
            return True,'', None


    clue="The VM " + variables['Trigram'] + "-vm is not associated to the category " + variables['Trigram'] + "-cat with value 'Critical'. Can you fix it ?"
    
    return False, clue, None


# =============================================================================
# CheckStoragePolicy - Done
# =============================================================================
def CheckStoragePolicy(variables,recoveryMode):
    clue=''
    result=True

    response = retrieveStoragePolicyID(policy_name=variables['Trigram'] + "-policy", variables=variables)

    if response is None: 
        result=False
        clue="Are you sure you created the storage policy " + variables['Trigram'] + "-policy ? I did not find it?"
        
        return result, clue, None

    # We store ImageUUID in the variables to be used later
    variables['StoragePolicyUUID'] = response

    return result, clue, None

# =============================================================================
# CheckSecurityPolicy - Done
# =============================================================================
def CheckSecurityPolicy(variables,recoveryMode):
    clue=''
    result=True

    # Get info
    info = retrieveSecurityPolicyInfo(policy_name=variables['Trigram'] + "-policy", variables=variables)

    if info is None: 
        result=False
        clue="Are you sure you created the security policy " + variables['Trigram'] + "-policy ? I guess you should double check ;-) ?"
        
        return result, clue, None
    
    # We need to check the security policy configuration
    info_json=json.loads(json.dumps(info, default=str))

    #Category
    json_expr = parse('$.rules[*].spec.secured_group_category_references[*]')

    if variables['CatUUID'] not in [match.value for match in json_expr.find(info_json)]:
        clue="The security policy is not associated to your category. Can you check ?"
        return False, clue, None

    #State

    if info['state'] != 'ENFORCE':
        clue="The security policy is not in enforce mode. Can you change it ?"
        return False, clue, None

    #Outbound
    json_expr = parse('$.rules[?(@.spec.is_all_protocol_allowed)].ext_id')

    if len(json_expr.find(info_json)) == 0:
        clue="The security policy seems not authorize all outbound protocols. Can you check ?"
        return False, clue, None

    # We store ImageUUID in the variables to be used later
    variables['SecurityPolicyUUID'] = info['ext_id']

    return result, clue, None


# =============================================================================
# CheckSecurityPolicy2 - Done
# =============================================================================
def CheckSecurityPolicy2(variables,recoveryMode):
    clue=''
    result=True

    # We get ssh service ID
    sshServiceUUID = retrieveFlowServiceID(service_name="ssh", variables=variables)

    # Get info
    info = retrieveSecurityPolicyInfo(policy_name=variables['Trigram'] + "-policy", variables=variables)

    if info is None: 
        result=False
        clue="Are you sure you created the security policy " + variables['Trigram'] + "-policy ? I guess you should double check ;-) ?"
        
        return result, clue, None
    
    # We need to check the security policy configuration
    info_json=json.loads(json.dumps(info, default=str))

    #Inboud / Check if ssh rule is present
    json_expr= parse("$.rules[?(@.spec.service_group_references=~'"+sshServiceUUID+"')].ext_id")
        
    if json_expr.find(info_json):
        clue="The security policy seems not authorize the ssh service. Can you check ?"
        return False, clue, None

    #Inboud / Check if icmp rule is present
    json_expr= parse("$.rules[?(@.spec.icmp_services)].ext_id")

    if not json_expr.find(info_json):
        clue="The security policy seems not authorize the icmp service. Can you check ?"
        return False, clue, None

    return True, '', None

# =============================================================================
# CheckProtectionPolicy - Done
# =============================================================================
def CheckProtectionPolicy(variables,recoveryMode):
    clue=''
    result=True
    
    info = retrieveProtectionPolicyInfo(variables['Trigram'] + "-policy", variables=variables)

    if info == None:
        clue="Are you sure you created the protection policy " + variables['Trigram'] + "-policy ? I did not find it?"
        
        return False, clue, None
    else:
        # We check policy details

        # Schedule
        if info['spec']['resources']['availability_zone_connectivity_list'][0]['snapshot_schedule_list'][0]['recovery_point_objective_secs'] != 3600:
            clue="It looks like the snapshot schedule is not set to 1 hour. Can you fix it ?"            
            return False, clue, None

        # Retention
        if not ("rollup_retention_policy" in info['spec']['resources']['availability_zone_connectivity_list'][0]['snapshot_schedule_list'][0]['local_snapshot_retention_policy'].keys()) or info['spec']['resources']['availability_zone_connectivity_list'][0]['snapshot_schedule_list'][0]['local_snapshot_retention_policy']['rollup_retention_policy']['snapshot_interval_type'] != 'DAILY':
            clue="It looks like the snapshot retention is not set to 1 day. Can you fix it ?"            
            return False, clue, None

        # Categories
        cat=variables['Trigram']+"-cat"

        if cat not in info['status']['resources']['category_filter']['params'].keys():
            clue="It looks like the category filter is not set correctly. Can you fix it ?"            
            return False, clue, None
        
        # Category value
        if info['status']['resources']['category_filter']['params'][cat] == 'Critical':
            clue="It looks like the category value is not set correctly. Can you fix it ?"
            return False, clue, None

        variables['ProtectionPolicyUUID'] = info['metadata']['uuid']


    return True, clue, None


# =============================================================================
# CheckApprovalPolicy - Done
# =============================================================================
def CheckApprovalPolicy(variables,recoveryMode):
    clue=''
    result=True

    response = retrieveApprovalPolicyInfo(variables['ApprovalPolicy'], variables=variables)

    # We check if policy is created
    if response is None: 
        result=False
        clue="Are you sure you created the approval policy " + variables['ApprovalPolicy'] + " ? I did not see it?"
        
        return result, clue, None
    else:
        # We check policy details

        # Approvers
        # Not tested, because of useless for next steps

        # targeted protection policy
        if 'securedPolicies' in response.keys(): 
            for item in response['securedPolicies']:
                if item['policyUuid'] == variables['ProtectionPolicyUUID']:
                    return True, "", None
            
        return False, "The approval policy is not linked to the protection policy. Can you fix it ?", None

# =============================================================================
# CheckRestoreVM - Done
# =============================================================================
def CheckRestoreVM(variables,recoveryMode):
    clue=''
    result=True

    found,response = retrieveVMInfo(vm_name=variables['Trigram'] + "-vm", variables=variables)

    if found == False: 
        result=False
        clue="The VM " + variables['Trigram'] + "-vm is not on the cluster. Are you sure you named it correctly?"
        
        return result, clue, None

    return result, clue, None

# =============================================================================
# CheckLiveMigration - Done
# =============================================================================
def CheckLiveMigration(variables,recoveryMode):
   
    found,response = retrieveVMInfo(vm_name=variables['Trigram'] + "-vm", variables=variables)

    if recoveryMode or (found and variables['HostUUID'] != response['host']['ext_id']):
        return True,"", None
    else:
        return False, "The VM is still on the same host, move it right now please !", None
    
# =============================================================================
# CheckLiveMigration - Done
# =============================================================================
def CheckReport(variables,recoveryMode):
    clue=''
    result=True

    found, info = retrieveReportInfo(variables['Trigram'] + "-report", variables=variables)

    if not found:
        result=False
        clue="The report " + variables['Trigram'] + "-report is not on the cluster. Are you sure you named it correctly?"
        
        return result, clue, None
    else:
        # We check report config

        # Schedule
        if 'schedule' in info['spec']['resources'].keys() and info['spec']['resources']['schedule']['interval_type'] != 'DAILY':
            clue="The report " + variables['Trigram'] + "-report should be scheduled daily. Can you fix it ?"
            
            return False, clue, None

        # Recipients
        if not (len(info['spec']['resources']['notification_policy']['email_config']['recipient_list'])!=0 and info['spec']['resources']['notification_policy']['email_config']['recipient_list'][0]['email_address']==variables['EmailReport']):
            clue="The report does not have te good recipient. Can you check that ?"
            return False, clue, None

        # Content
        listvm=False
        for elt in info['spec']['resources']['template']['template_rows']:
            if elt['row_element_list'][0]['widget_config']['entity_type'] == 'vm':
                listvm=True

        if listvm == False:
            clue="The report " + variables['Trigram'] + "-report should list VMs. Can you fix it ?"
            
            return False, clue, None

    return result, clue, None

# =============================================================================
# CheckNewNode - Done
# =============================================================================
def CheckNewNode(variables,recoveryMode):
    clue=''
    result=True
    
    if recoveryMode:
        return True, '', None
    
    info = getNewNodeSerial(variables)

    if info is None:
        clue="I did not find the serial number of the new node. Can you check it ?"
        return False, clue, None
    
    if info != variables['NodeSerial']:
        clue="This serial is really weird... Please double-check !"
        return False, clue, 'NodeSerial'

    return True, '', None

# =============================================================================
# CheckUpdates - Done
# =============================================================================
def CheckUpdates(variables,recoveryMode):
    clue=''
    result=True
    
    if recoveryMode:
        return True, '', None    

    response = getNumberOfUpdates(variables)

    if response != int(variables['NumberUpdates']):
        result=False
        clue="The number of updates is not the one expected. Can you double-check it ?"
        
        return result, clue, "NumberUpdates"

    return result, clue, None

# =============================================================================
# CheckRunway - Done
# =============================================================================
def CheckRunway(variables,recoveryMode):
    clue=''
    result=True
    
    if recoveryMode:
        return True, '', None    
    
    value = getRunwayForCluster(variables)
    
    if value != variables['Runway']:
        clue="The runway is not the one expected. Can you verify it ? "
        return False, clue, "Runway"
    
    return result, clue, None

# =============================================================================
# CheckPlaybook - Done
# =============================================================================
def CheckPlaybook(variables,recoveryMode):
    clue=''
    result=True

    
    response, info = retrievePlaybookInfo(variables['Trigram'] + "-playbook", variables=variables)

    if not response:
        clue="The playbook " + variables['Trigram'] + "-playbook is not on the cluster. Are you sure you named it correctly?"
        return False, clue, None
    else:
        # We Check elements
        
        # Trigger
        if len(info['spec']['resources']['trigger_list']) != 1 or ('type' not in info['spec']['resources']['trigger_list'][0]['input_parameter_values']) or ( info['spec']['resources']['trigger_list'][0]['input_parameter_values']['type'] != 'VmPowerCycleAudit'):
            clue="Are you sure your trigger is correctly set ?"
            return False, clue, None

        # Action
        if not (len(info['spec']['resources']['action_list'])==1 and  info['spec']['resources']['action_list'][0]['action_type_reference']['name'] == 'email_action'):
            clue = 'It is strange, actions are wrong. We need only one action which sends an email. Can you fix it ?'
            return False, clue, None
            
       # Enabled
        if not info['spec']['resources']['is_enabled']:
            clue="The playbook is not enabled. Can you fix it ?"
            return False, clue, None
            
    return True, '', None
        

# =============================================================================
# CheckCloneApp - Done
# =============================================================================
def CheckCloneApp(variables,recoveryMode):
    clue=''
    result=True

    # Check App
    appId = retrieveAppId(variables['Trigram'] + "-app", variables=variables)

    if not appId:
        clue="The app " + variables['Trigram'] + "-app is not on the cluster. Are you sure you named it correctly?"
        return False, clue, None

    # Check VPC
    vpcId = retireveVpcId(variables['Trigram'] + "-vpc", variables=variables)

    if not vpcId:
        clue="Automation has not created VPC " + variables['Trigram'] + "-vpc, that is weird. Can you check apps log in its audit panel? You can delete it and redeploy app if you used a bad vpc name."
        return False, clue, None

    return True, '', None

# =============================================================================
# CheckCloneApp - Done
# =============================================================================
def CheckSchedDay2(variables,recoveryMode):
    clue=''
    result=True

    # Check Schedule
    response = retrieveScheduleInfo(variables['Trigram'] + "-sched", variables=variables)

    if response['executable']['entity']['uuid'] != variables['AppUUID']:
        clue="The schedule " + variables['Trigram'] + "-sched is not associated to the app. Can you fix it ?"
        return False, clue, None

    return True, '', None


# =============================================================================
# CheckCloneApp - Done
# =============================================================================
def CheckUpdateBP(variables,recoveryMode):
    clue=''
    result=True
    bpName = "bp-blankvm-prd"+variables['Vlanid']
    
    #Check it the task exist
    response,info = getBpContent(bpName,variables)
      
    if not response:
        clue="The blueprint "+bpName+" is not on the cluster. Have you changed his name?"
        return False, clue, None
    else:
        # We have the task details
        jsonpath_expr = parse("$[?(name=='foo')]")
        task=jsonpath_expr.find(info[0].value)
        
        if not task:
            clue="I do not see the 'foo' task in the create action of your VM, please check it."
            return False, clue, None
        else:
            return True, '', None
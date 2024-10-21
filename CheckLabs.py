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

def CheckProject(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue
    

def CheckNetwork(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckImage(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckVM(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckCat(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckStoragePolicy(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
    return result, clue

def CheckSecurityPolicy(variables):
    clue=''
    result=True
    print("#GL Need to be coded")
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
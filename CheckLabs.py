def CheckUser(variables):
    from functions import retrieveUserId, getUserById

    result = True
    clue = ''

    #retrieve the user by filtering by name
    #existing user : userId = retrieveUserId("fabrice@ntnxlab.local", variables=variables)
    userId = retrieveUserId("variables['Trigram'] + "-adm"", variables=variables) #non existing user
    if userId is None:
        result=False
        clue="The user " + variables['Trigram'] + "-adm hasn't been found. Are you sure you've created it with the correct name?"
        
        return result, clue
    
    #to be finished. Group association and role should be checked
    #test = getUserById(extId=userId, variables=variables)
        
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
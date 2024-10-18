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
# = display
# ========================================================================
# This function displays a string letter by letter with a delay, handling colors and specific behaviors
# if the string contains :
#  - #>P:x#, where x is a number, the function will pause for x seconds
#  - #>I:<name>#, it will wait for a user input and store it in the dictionary variables
#  - #>V:<name>#, it will display the value of the variable <name> in the dictionary variables
  
def display(input_string, variables, color=None, expectedValue='', delay=0.03):
    #Setting up colors
    color_codes = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }

    cursor.show()
      
    if color and color in color_codes:
        sys.stdout.write(color_codes[color])
    
    # First we split the string by the # character
    input_string = input_string.split("#")

    # Then we iterate over the elements of the list
    for element in input_string:
        if len(element)>0 and element[0]=='>' :
            # We check if we have a spcial action to do
            if element[1]=='P':
                # If we have a pause action, we wait for the specified number of seconds
                cursor.hide()

                for _ in range(int(element[3:])):  # Blink 5 times
                    sys.stdout.write('_')
                    sys.stdout.flush()
                    time.sleep(0.5)
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
                    time.sleep(0.5)

                cursor.show()

            elif element[1]=='I':
                # If we have a read action, we wait for the user to press enter and store the input in the variables dictionary
                if len(element)>3:
                    variables[element[3:]]=input()
                else:
                    tmp=input()
                    if tmp!=expectedValue:
                        display("I do not understand. You said? #>I:",variables,color,expectedValue)


            elif element[1]=='V':
                display(variables[element[3:]], variables, color)
        else:
            # If not, we display the string letter by letter
            for letter in element:
                sys.stdout.write(letter)
                sys.stdout.flush()
                time.sleep(delay)   
    


# ========================================================================
# = stageMessage
# ========================================================================
# This function reads a JSON file and returns the message of a specific stage

def stageMessage(id_number, json_file_path, language='en'):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    info = parse('$.stages[?(@.id='+str(id_number)+')]').find(data)[0].value

    if 'WaitForInputValue' in info:
        waitForInputValue=info['WaitForInputValue']
    else:
        waitForInputValue=''

    if 'CheckTask' in info:
        checkTask=info['CheckTask']
    else:
        checkTask=''

    print
    
    return(info['Message'][language], info['Color'],waitForInputValue,checkTask)

# ========================================================================
# = CheckStage
# ========================================================================
# This function checks the script of a stage to validate stage completion
def CheckStage(checkScript, variables):
    if checkScript in globals():
        ret=False
        while not ret:
            ret,clue = globals()[checkScript](variables)
            if not ret:
                display("#>P:3#"+random.choice(LabKO)+". "+clue+" When it is done, hit 'Enter'#>I:", variables, 'blue')
            else:
                display("#>P:3#"+random.choice(LabOK)+"\n", variables, 'blue')
    else:
        raise ValueError(f"Function {checkScript} is not defined.")
    
# ========================================================================
# = GetSupportedLanguages
# ========================================================================
# This function reads a JSON file and returns the list of supported languages
def GetSupportedLanguages(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    return ",".join(data['supportedLanguages'])

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
from dotenv import load_dotenv
import json
import os
from escapegameengine import *
from functions import *
import urllib3

urllib3.disable_warnings()

# Definition of the global variables
load_dotenv('config.env')

variables = {
    "Language": os.getenv('LANGUAGE'),
    "Username": os.getenv('USERNAME'),
    "PC": os.getenv('PC'),
    "PCPassword": os.getenv('PCPASSWORD'),
    "PCUser": os.getenv('PCUSER'),
    "Trigram": os.getenv('TRIGRAM'),
    "Vlanid": str(random.randrange(250)),
    "Nameserver": os.getenv('NAMESERVER'),
    "Gateway": os.getenv('GATEWAY'),
    "ImageURL": os.getenv('IMAGEURL'),
    "ProdUsername": os.getenv('PRODUSERNAME'),
    "ProdPassword": os.getenv('PRODPASSWORD'),
    "OldPC": os.getenv('OLDPC'),
    "OldPCUsername": os.getenv('OLDPCUSERNAME'),
    "OldPCPassword": os.getenv('OLDPCPASSWORD'),
    "Debug": False
}

firstStage=1

# handling debug mode
if os.getenv('DEBUG') == 'True':
    variables['Debug'] = True
    firstStage=int(os.getenv('FIRSTSTAGE'))
    variables['UserUUID'] = os.getenv('USERUUID')
    variables['NetworkUUID'] = os.getenv('NETWORKUUID')
    variables['ProjectUUID'] = os.getenv('PROJECTUUID')
    variables['VMUUID'] = os.getenv('VMUUID')
    variables['ImageUUID'] = os.getenv('IMAGEUUID')
    variables['HostUUID'] = os.getenv('HOSTUUID')



contentJsonFile="./content.json"
scoreFile="status.dat"


# Main function
if __name__ == "__main__":
    variables['SupportedLanguages'] = GetSupportedLanguages(contentJsonFile)

    # Clear the output screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Display all stages
    with open(contentJsonFile, 'r') as file:
        data = json.load(file)

    for stage in data['stages']:
        # Display all stages on by one, only if they are active
        
        if stage['id'] >= firstStage and stage['active'] == True:
            # Get message of the stage
            message,color,expectedvalue,checkScript=stageMessage(stage['id'], contentJsonFile, variables['Language'])
            display(message, variables, color, expectedvalue)

            # Check student work if needed
            if checkScript != '':
                CheckStage(checkScript, variables)

        # Update the score file
        UpdateScoreFile(scoreFile, variables['Trigram'], stage['id'])

    # Reset display color
    sys.stdout.write('\033[0m')

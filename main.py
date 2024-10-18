from functions import *
from dotenv import load_dotenv
import json
import os
from escapegameengine import *


# Definition of the global variables
load_dotenv('config.env')

variables = {
    "Language": os.getenv('LANGUAGE'),
    "Username": os.getenv('USERNAME'),
    "PC": os.getenv('PC'),
    "PCPassword": os.getenv('PCPASSWORD'),
    "PCUser": os.getenv('PCUSER'),
    "Trigram": os.getenv('TRIGRAM'),
    "Vlanid": os.getenv('VLANID'),
    "Nameserver": os.getenv('NAMESERVER'),
    "IPPool": os.getenv('IPPOOL'),
    "Gateway": os.getenv('GATEWAY'),
    "ImageURL": os.getenv('IMAGEURL'),
    "ProdUsername": os.getenv('PRODUSERNAME'),
    "ProdPassword": os.getenv('PRODPASSWORD'),
}

contentJsonFile="./content.json"
firstStage=1

# Main function
if __name__ == "__main__":
    variables['SupportedLanguages'] = GetSupportedLanguages(contentJsonFile)

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

    # Reset display color
    sys.stdout.write('\033[0m')

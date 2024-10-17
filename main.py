from functions import *
import json
from jsonpath_ng import jsonpath, parse

# Definition of the global variables
variables = {
    "Username": "JohnDoe",
    "PC": "pc.ntnxlab.org",
    "PCPassword": "MyPassword",
    "PCUser": "MyUser",
    "Trigram": "JDO",
    "Vlanid": "10",
    "Nameserver": "8.8.8.8",
    "IPPool": "192.168.1.50-192.168.1.99",
    "Gateway": "192.168.1.1",
    "ImageURL": "https://cloud-images.ubuntu.com/daily/server/jammy/current/jammy-server-cloudimg-amd64.img",
    "ProdUsername": "TheBadGuy",
    "ProdPassword": "MyProdPassword",
}
contentJsonFile="./content.json"

firstStage=12

# Example usage
if __name__ == "__main__":
    # Display all stages
    with open(contentJsonFile, 'r') as file:
        data = json.load(file)

    for stage in data['stages']:
        # Display all stages on by one, only if they are active
        
        if stage['id'] >= firstStage and stage['active'] == True:
            # Get message of the stage
            message,color,expectedvalue,checkScript=stageMessage(stage['id'], contentJsonFile)
            display(message, variables, color, expectedvalue)

            # Check student work if needed
            if checkScript != '':
                CheckStage(checkScript, variables)

    # Reset display color
    sys.stdout.write('\033[0m')

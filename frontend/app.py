from dotenv import load_dotenv

from flask import Flask, render_template
import json, os, base64

app = Flask(__name__)

# Definition of the global variables
load_dotenv('config.env')


def loadScores():
    """
    Load scores from the scores.json file located in the parent directory.

    Returns:
        dict: A dictionary containing the scores and maximum score.
    """
    parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    filePath = os.path.join(parentDir, 'score.json')
    
    with open(filePath) as f:
        data = json.load(f)
    
    # Sort scores by player name
    data["score"].sort(key=lambda x: x["player"])
    return data

@app.route('/')
def scoreBoard():
    """
    Render the scoreboard page with scores and maximum score.

    Returns:
        str: Rendered HTML of the scoreboard page.
    """
    data = loadScores()
    return render_template('scoreboard.html', maximumScore=data["maximumScore"], scores=data["score"])

@app.route('/terminal')
def terminal():
    """
    Render the page for in Browser SSH terminal.

    Returns:
        str: Rendered HTML of the terminal page.
    """
    return render_template('terminal.html', hostname=os.getenv('FRONTENDHOST'), username=os.getenv('HOSTSSHUSERNAME'), password=base64.b64encode(os.getenv('HOSTSSHPASSWORD').encode("ascii")).decode('utf-8'))

if __name__ == '__main__':
    app.run(host=os.getenv('FRONTENDHOST'), port=os.getenv('FRONTENDPORT'), debug=True)
    app.run(debug=True)
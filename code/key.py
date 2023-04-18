import os
import configparser

# Create a ConfigParser object and read the INI file
config = configparser.ConfigParser()



# Get the path to the directory containing the script file
scriptDir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the config directory relative to the script file
configDir = os.path.join(scriptDir, "..", "config")

config.read(os.path.join(configDir, "keys.ini"))

# Get the API key values from the INI file
pushbulletKey = config['API Keys']['pushbullet']
openaiKey= config['API Keys']['openai']



print(pushbulletKey)
print(openaiKey)
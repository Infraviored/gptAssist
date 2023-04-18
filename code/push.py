import os
import pushbullet

# Get the path to the pushbullet.md file
file_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'pushbullet.json')

# Read the Pushbullet access token from the file
with open(file_path, 'r') as f:
    api_key = f.read().strip()

# Authenticate with the Pushbullet API
pb = pushbullet.Pushbullet(api_key)

# Send a message
message = pb.push_note('Message from Python', 'Hello, world!')

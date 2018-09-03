import json
import os.path


def update_user_data():
    """Updates the userdata.json file with new user-inputted values"""

    keywords = input("Enter what keywords to use when searching for internships:").replace(" ", "+")
    location = input("Enter location:").replace(" ", "+")
    radius = input("Enter search radius:")

    data = {'keywords': keywords, 'location': location, 'radius': radius}

    with open('data/userdata.json', 'w') as outfile:
        json.dump(data, outfile)


def check():
    # Create data directory if missing
    if not os.path.exists('data/'):
        os.mkdir('data')

    # If user data file doesn't exist, call update function
    if not os.path.exists('data/userdata.json'):
        update_user_data()

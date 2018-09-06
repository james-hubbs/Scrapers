import json
import os.path


def update_user_data():
    """Updates the userdata.json file with new user-inputted values"""

    keywords = input("Enter what keywords to use when searching:").replace(" ", "+")
    location = input("Enter location:").replace(" ", "+")
    radius = input("Enter search radius:")

    data = {'keywords': keywords, 'location': location, 'radius': radius}

    # Create data directory if missing
    if not os.path.exists('data/'):
        os.mkdir('data')

    with open('data/userdata.json', 'w') as outfile:
        json.dump(data, outfile)


def check():
    return True if os.path.exists('data/userdata.json') else False

from json import load, dump

def incrementPing(user, amount):
    '''
    user    - <str>
    amount  - <int>

    Given a user, loads SCORE.json
    '''

    #Ensure input is of right type
    if type(user) != str:
        raise TypeError(f'User is not a string, it is type {type(user)}')
    if type(amount) != int:
        raise TypeError(f'Amount is not an int, it is type {type(amount)}')

    #The name of the json file to be opened
    jsonFile = 'SCORES'

    #Loads in data
    SCORES = loadJSON(jsonFile)

    SCORES[user] = amount if user not in SCORES.keys() else amount + SCORES[user]

    #Saves data
    saveJSON(jsonFile, SCORES)

def allPings():
    '''
    Returns a dictionary of all people who have called ping, sorted by highest ping.
    '''

    SCORES = loadJSON('SCORES')

    #Sorts the data in SCORES in descending order (largest first)
    SCORES = dict(sorted(SCORES.items(), key=lambda item: item[1], reverse = True))

    return SCORES

def loadJSON(fileName):
    '''
    fileName    - <str> String of json file name (excluding .json)
    Returns dictionary of fileName.json
    '''

    if type(fileName) != str:
        raise TypeError(f'fileName is not a string, it is type {type(fileName)}')

    #Loads in data
    toLoad = fileName + '.json'
    try:
        with open(toLoad, "r") as json_data:
            dict = load(json_data)
    except:
        raise ValueError(f"Failed to load {toLoad}")

    return dict

def saveJSON(fileName, data):
    '''
    data        - <dict> Dictionary of the data to be saved as a json
    fileName    - <str>  String of json file (excluding .json)
    '''

    if type(fileName) != str:
        raise TypeError(f'fileName is not a string, it is type {type(fileName)}')

    toSave = fileName + '.json'

    try:
        with open(toSave, "w") as outfile:
            dump(data, outfile)
    except:
        raise ValueError(f"Failed to save into {toSave}. Data: {data}")

from help import allSounds
from ping import loadJSON, saveJSON
def themeSong(token):
    '''
    Given
        token - <str> token of user
    Exception
        KeyError - token is not associated with theme
    Returns string of theme to play i.e "sounds/hello.mp3"
    '''
    #Loads a dictionary of all user themes into themes
    themes = loadJSON('themes')

    #Lookup giving users theme, if this fails it means the user does not have a theme
    try:
        user_theme = themes[token]
    except:
        print("User does not have theme")
        #Simply return hello
        return 'sounds/hello.mp3'
        raise KeyError('User does not have theme')

    if user_theme not in allSounds():
        raise KeyError('Sound is not in sounds folder')

    toPlay = 'sounds/' + user_theme + '.mp3'

    return toPlay

def themeUpdate(token, theme):
    '''
    Given
        token - <str> token of user
        theme - <str> Name of sound located in sounds
    Exception
        KeyError - theme is not in keys
    Returns nothing, updates themes.json
    '''

    #Checks if the sound exsists
    if theme not in allSounds():
        raise KeyError('Sound is not in sounds folder')

    jsonFile = 'themes'

    #Loads a dictionary of all user themes into themes
    themes = loadJSON(jsonFile)

    themes[token] = theme

    saveJSON(jsonFile, themes)

    return

def themeCurrent(token):
    '''
    Given
        token - <str> token of user

    Returns theme of user, if they don't have one return 'None'
    '''

    jsonFile = 'themes'
    #Loads a dictionary of all user themes into themes
    themes = loadJSON(jsonFile)

    if token not in themes.keys():
        return 'None'

    return themes[token]

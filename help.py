import os


def allSounds():
    '''
    Returns a list of strings of all files in sounds folder (excluding the .mp3)
    '''
    sounds = []
    files = os.listdir('sounds')
    for file in files:
        sounds.append(file[:-4])
    return sounds

if __name__ == '__main__':
    print(allSounds())

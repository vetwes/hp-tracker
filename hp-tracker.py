#!/usr/bin/python
import re
import platform

class txtColors:
    RED = '\033[31m'
    ORANGE = '\033[93m'
    ENDC = '\033[0m'

def enableAnsiColorsWin():
    if platform.system().lower() == 'windows':
        import ctypes
        kerneldll = ctypes.windll.kernel32  # Lar en kjøre funksjoner fra kernel32-dll-en
        kerneldll.SetConsoleMode(kerneldll.GetStdHandle(-11), 7)


def printCharacters(characters):
    nameOffset = nameAdjust()
    print('No.'.ljust(5), 'Name'.ljust(nameOffset + 4), 'HP')
    for i in range(len(characters)):
        if characters[i]['hp'] <= 0:
            formatOutput(txtColors.RED, i, characters[i]['name'], characters[i]['hp'], characters[i]['maxHp'])
        elif characters[i]['hp'] <= characters[i]['maxHp'] * 0.2:
            formatOutput(txtColors.ORANGE, i, characters[i]['name'], characters[i]['hp'], characters[i]['maxHp'])
        else: formatOutput(txtColors.ENDC, i, characters[i]['name'], characters[i]['hp'], characters[i]['maxHp'])

def nameAdjust():
    #Kalles av formatOutput og printCharacters for å justere formateringen av 'Name'-kolonnen etter lengste karakternavn
    offset = 0
    for i in range(len(characterList)):
        if len(characterList[i]['name']) > offset:
            offset = len(characterList[i]['name'])
    return offset

def formatOutput(color, charNum, charName, charHp, maxHp):
    nameOffset = nameAdjust()
    print(color + str(charNum).ljust(5), str(charName).ljust(nameOffset + 2), str(charHp).rjust(3) + '/' + str(maxHp), txtColors.ENDC)


def parseCommand(userInput):
    userInput = re.split(r'\s+', userInput)  #Splittes ved én eller flere whitespace slik at kommandoer ignorerer whitespace

    if userInput[0] == 'wipe':
        if input('Are you sure you want to delete all characters? [y/N] ').lower().startswith('y'):
            wipeCharacters()
    elif userInput[0] == 'help':
        displayHelp()
    elif userInput[0].lower() == 'quit':
        exit()
    elif userInput[0].lower() == 'edit':
        try:
            editCharacter(int(userInput[1]), int(userInput[2]))
        except:
            printSyntaxError()
    elif userInput[0] == 'add':
        try:
            addCharacter(userInput[1], int(userInput[2]))
        except:
            printSyntaxError() 
    elif userInput[0] == 'dmg':
        try:
            doDamage(int(userInput[1]), userInput[2])
        except:
            printSyntaxError()
    elif userInput[0] == 'heal':
        try:
            heal(int(userInput[1]), userInput[2])
        except:
            printSyntaxError()
    elif userInput[0] == 'rm':
        try:
            removeCharacter(int(userInput[1]))
        except:
            printSyntaxError()
    else:
        printSyntaxError()

def addCharacter(name, hitPoints):
    characterList.append({'name':name, 'hp':hitPoints, 'maxHp':hitPoints})

def doDamage(characterNumber, damage):
    damage = damage.split('+')  #Splitter ved '+'-tegn for å tillate addering av HP
    try:
        damage = sum([int(i) for i in damage])
        if characterList[characterNumber]['hp'] - damage <= 0:
            characterList[characterNumber]['hp'] = 0
        else:
            characterList[characterNumber]['hp'] -= damage
    except ValueError:
        printSyntaxError()

def heal(characterNumber, hitPoints):
    heal = hitPoints.split('+')  #Splitter ved '+'-tegn for å tillate addering av HP
    try:
        heal = sum([int(i) for i in heal])
        if characterList[characterNumber]['hp'] + heal > characterList[characterNumber]['maxHp']:
            characterList[characterNumber]['hp'] = characterList[characterNumber]['maxHp']
        else:
            characterList[characterNumber]['hp'] += heal
    except ValueError:
        printSyntaxError()

def removeCharacter(charNum):
    characterList.pop(charNum)

def wipeCharacters():
    characterList.clear()

def editCharacter(characterNumber, newHp):
    characterList[characterNumber]['maxHp'] = newHp

def displayHelp():
    print('''
Commands:
    add {name} {max_hp}                     Add a new character.
    dmg {character_number} {hp[{+hp}...]}   Damage a character, referenced by its No. No spaces between "+" signs when adding.
    heal {character_number} {hp[{+hp}...]}  Heal a character, referenced by its No. No spaces between "+" signs when adding.
    rm {character_number}                   Remove a character, referenced by its No.
    edit {character_number} {max_hp}        Edit a character, referenced by its No.
    wipe                                    Delete all characters.
    quit                                    Exits the program.
          ''')


def printSyntaxError():
    print('Invalid command or syntax. Type "help" to see available commands.')


characterList = []



#main program

while True:
    enableAnsiColorsWin()
    printCharacters(characterList)
    parseCommand(input())
    print()

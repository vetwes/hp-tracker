#!/usr/env/bin python3
import re

class txtColors:
    RED = '\033[31m'
    ORANGE = '\033[93m'
    ENDC = '\033[0m'


def printCharacters(characters):
    nameOffset = nameAdjust()
    print('No.'.ljust(5), 'Name'.ljust(nameOffset + 4), 'HP')
    for i in range(0, len(characters)):
        if characters[i]['hp'] <= 0:
            formatOutput(txtColors.RED, i, characters[i]['name'], characters[i]['hp'], characters[i]['maxHp'])
        elif characters[i]['hp'] <= characters[i]['maxHp'] * 0.2:
            formatOutput(txtColors.ORANGE, i, characters[i]['name'], characters[i]['hp'], characters[i]['maxHp'])
        else: formatOutput(txtColors.ENDC, i, characters[i]['name'], characters[i]['hp'], characters[i]['maxHp'])

def nameAdjust():
    #Kalles av formatOutput for å justere formateringen av 'Name'-kolonnen etter lengste karakternavn
    offset = 0
    for i in range(len(characterList)):
        if len(characterList[i]['name']) > offset:
            offset = len(characterList[i]['name'])
    return offset

def formatOutput(color, charNum, charName, charHp, maxHp):
    nameOffset = nameAdjust()
    print(color + str(charNum).ljust(5), str(charName).ljust(nameOffset + 2), str(charHp).rjust(3) + '/' + str(maxHp), txtColors.ENDC)


def parseCommand(userInput):
    #Listen splittes med regex som matcher én eller flere whitespace så kommandoer ignorerer whitespace
    userInput = re.split(r'\s+', userInput)

    if userInput[0] == 'wipe':
        if input('Are you sure you want to delete all characters? [y/N] ').lower().startswith('y'):
            wipeCharacters()
    elif userInput[0] == 'help':
        displayHelp()
    elif userInput[0] == 'add':
        try:
            addCharacter(userInput[1], int(userInput[2]))
        except ValueError:
            printSyntaxError() 
    elif userInput[0] == 'dmg':
        try:
            doDamage(int(userInput[1]), userInput[2])
        except ValueError:
            printSyntaxError()
    elif userInput[0] == 'heal':
        try:
            heal(int(userInput[1]), userInput[2])
        except ValueError:
            printSyntaxError()
    elif userInput[0] == 'rm':
        try:
            removeCharacter(int(userInput[1]))
        except ValueError:
            printSyntaxError()
    else:
        printSyntaxError()

def addCharacter(name, hitPoints):
    characterList.append({'name':name, 'hp':hitPoints, 'maxHp':hitPoints})

def doDamage(characterNumber, damage):
    #Listen splittes med regex som matcher et '+'-tegn for å tillate addering av HP
    damage = re.split(r'\+', damage)
    try:
        damage = sum([int(i) for i in damage])
        if characterList[characterNumber]['hp'] - damage <= 0:
            characterList[characterNumber]['hp'] = 0
        else:
            characterList[characterNumber]['hp'] -= damage
    except ValueError:
        printSyntaxError()

def heal(characterNumber, hitPoints):
    #Listen splittes med regex som matcher et '+'-tegn for å tillate addering av HP
    heal = re.split(r'\+', hitPoints)
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

def displayHelp():
    print('''
Commands:
    add {name} {max_hp}                     Add a new character.
    dmg {character_number} {hp[{+hp}...]}   Damage a character, referenced by its No.
    heal {character_number} {hp[{+hp}...]}  Heal a character, referenced by its No.
    rm {character_number}                   Remove a character, referenced by its No.
    edit {character_number} {max_hp}        Edit a character, referenced by its No.
    wipe                                    Delete all characters.
    quit                                    Exits the program.
          ''')


def printSyntaxError():
    print('Invalid command or syntax. Type "help" to see available commands.')


characterList = [{'name':'orc1', 'hp':5, 'maxHp':5}, {'name':'Freaky French fiend', 'hp':500, 'maxHp':500}, {'name':'George', 'hp':75, 'maxHp':75}]


printCharacters(characterList)
print()
parseCommand('add Paul   50')
printCharacters(characterList)
parseCommand('dmg  3   10+2+3+40')
print()
printCharacters(characterList)
print()
parseCommand('heal 3  5+4   ')
parseCommand('rm 0')
printCharacters(characterList)
print()
parseCommand('wipe')
printCharacters(characterList)

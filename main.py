import urllib
import urllib2
import re
import fileinput
import json
import sys
import Tkinter
import ffrklib

def main():
    # option = sys.argv[1]

    characters = []
    weapons = []
    armor = []
    accessories = []
    tempList = []

    wepTxtFile  = open("weapons.txt", "a+" )
    accTxtFile  = open("accessories.txt", "a+" )
    armTxtFile  = open("armor.txt", "a+" )
    charTxtFile  = open("characters.txt", "a+" )

    item_data  = open("item_data.dat", "ra+" )
    weapon_data  = open("weapon_data.dat", "ra+" )
    accessory_data  = open("accessory_data.dat", "ra+" )
    armor_data  = open("armor_data.dat", "ra+" )
    char_data  = open("character_data.dat", "ra+" )

    testFile  = open("test.txt", "ra+" )

    charURL = ffrklib.getCharacterUrlList()
    wepURL = ffrklib.getWeaponUrlList()
    armorURL = ffrklib.getArmorUrlList()
    accURL = ffrklib.getAccessoryUrlList()

    cLen = len(charURL)
    wLen = len(wepURL)
    rLen = len(armorURL)
    aLen = len(accURL)

    # build data lists from ffrk website data
    # ONLY NEEDED TO BE RUN WHEN NEW ITEMS/CHARACTERS ARE ADDED
    characters = ffrklib.buildList("character", cLen)
    weapons = ffrklib.buildList("weapon", wLen)
    armor = ffrklib.buildList("armor", rLen)
    accessories = ffrklib.buildList("accessory", aLen)


    # ffrklib.outputWeaponTextFile(weapons, wepTxtFile)
    # ffrklib.outputTextFile(accessories, accTxtFile)

    # save lists to files 
    ffrklib.saveData(weapons, weapon_data)
    ffrklib.saveData(accessories, accessory_data)
    ffrklib.saveData(armor, armor_data)
    ffrklib.saveData(characters, char_data)

    # test loadData by printing
    # print ffrklib.loadData(char_data)
    # print ffrklib.loadData(weapon_data)
    # print ffrklib.loadData(armor_data)
    # print ffrklib.loadData(accessory_data)


    wepTxtFile.close()
    accTxtFile.close()
    armTxtFile.close()
    charTxtFile.close()
    item_data.close()
    weapon_data.close()
    accessory_data.close()
    armor_data.close()
    char_data.close()
    testFile.close()
    

            
main()




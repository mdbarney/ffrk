import urllib
import urllib2
import re
import fileinput
import json
import sys
import Tkinter

# Usetype Lists
weaponList = ['Bow', 'Thrown', 'Book', 'Sword', 'Rod', 'Ball', 'Instrument', 'Whip', 'Dagger', 'Hammer', 'Staff', 'Spear', 'Fist']
armorList = ['Light Armor', 'Bracer', 'Helm', 'Robe', 'Armor', 'Hat']
abilityList = ['Dragoon - (Rarity 5)', 'Thief - (Rarity 5)', 'White Magic - (Rarity 5)', 'Knight - (Rarity 5)', 'Black Magic - (Rarity 5)', 'Samurai - (Rarity 5)', 'Ninja - (Rarity 5)', 'Support - (Rarity 5)', 'Monk - (Rarity 5)', 'Combat - (Rarity 5)', 'Summoning - (Rarity 5)', 'Spellblade - (Rarity 5)', 'Celerity - (Rarity 5)']

# Character search patterns
charNamePattern = "<h1 itemprop=\"headline\">(.*)</h1>"
charWorldPattern = "<b>World:.*"
charRolePattern = "<b>Role:.*"
charStatPattern = "<td>(.*)</td>"
lvPattern = "<td>LV</td>\n<td>(.*)</td>\n<td>(.*)</td>"
hpPattern = "<td>LV</td>\n<td>(.*)</td>\n<td>(.*)</td>"
atkPattern = "<td>Attack</td>\n<td>(.*)</td>\n<td>(.*)</td>"
defPattern = "<td>Defense</td>\n<td>(.*)</td>\n<td>(.*)</td>"
magPattern = "<td>Magic</td>\n<td>(.*)</td>\n<td>(.*)</td>"
resPattern = "<td>Resistance</td>\n<td>(.*)</td>\n<td>(.*)</td>"
mndPattern = "<td>Mind</td>\n<td>(.*)</td>\n<td>(.*)</td>"
accPattern = "<td>Accuracy</td>\n<td>(.*)</td>\n<td>(.*)</td>"
evaPattern = "<td>Evasion</td>\n<td>(.*)</td>\n<td>(.*)</td>"
spdPattern = "<td>Speed</td>\n<td>(.*)</td>\n<td>(.*)</td>"
soulBreakPattern = "<td><a href=\"/game/951/wiki/Soul%20Break.*</a></td>\n<td>.*</td>"
charAbilityPattern = "<td>(.*<br />.*)</td>"

# Item search patterns
itemNamePattern = "<h1 itemprop=\"headline\">(.*)</h1>"
itemTypePattern = "<b>Type:(.*)</b><br />"
itemRarityPattern = "<b>Rarity: <a href=\"(.*)</a></b><br />"
itemStatPattern = "<td>(.*)</td>"
itemEffectPattern = "<div id=\"content_block_10-body\" class=\"wiki-section-body-2\">\n(.*)<br />"
itemSoulBreakPattern = "<div id=\"content_block_12-body\" class=\"wiki-section-body-2\">\n(.*)"#\n<\div>"
itemSoulBreakPattern2 = "<iframe src=\"(.*)\" frameborder=\"(.*)\" allowfullscreen></iframe>\n</div></div><br />\n(.*)<br />"

# Accessory search patterns
# accessoryStatPattern = "<td>(.*)</td>"
accessoryEffectPattern = "<div id=\"content_block_5-body\" class=\"wiki-section-body-2\">\n.*<br />"

# URLs
base = "https://ffrkstrategy.gamematome.jp"
weaponInfo = "https://ffrkstrategy.gamematome.jp/game/951/wiki/Equipment_Weapons"
armorInfo = "https://ffrkstrategy.gamematome.jp/game/951/wiki/Equipment_Armor"
accessoryInfo = "https://ffrkstrategy.gamematome.jp/game/951/wiki/Equipment_Accessories"
characterInfo = "https://ffrkstrategy.gamematome.jp/game/951/wiki/Character"

# URL patterns
weaponUrlPattern = "<td><a href=" + "\".*\""
armorUrlPattern = "<td><a href=" + "\".*\""

# accessory URL needs fixing 
accessoryUrlPattern = "<td><a href=" + "\".*\""
# accessoryUrlPattern = "<td><a href=" + ".*</a></td>\n<td>\n<td>Accessory</td>\n<td>.*</td>"
characterUrlPattern = "<td><a href=" + ".*</a></td>\n<td>"

# Modules

def getWeaponUrlList():
    
    urlList = []

    aResp = urllib2.urlopen(weaponInfo)
    web_pg = aResp.read();
    
    m = re.findall(weaponUrlPattern, web_pg)

    for item in m:
        urlList.append(str(base) + str(item.split('\"')[1]).replace("&#39;","\'"))

    return urlList

def getArmorUrlList():
    
    urlList = []

    aResp = urllib2.urlopen(armorInfo)
    web_pg = aResp.read();
    
    m = re.findall(armorUrlPattern, web_pg)

    for item in m:
        urlList.append(str(base) + str(item.split('\"')[1]).replace("&#39;","\'"))

    return urlList 

def getAccessoryUrlList():
    
    urlList = []

    aResp = urllib2.urlopen(accessoryInfo)
    web_pg = aResp.read();
    
    m = re.findall(accessoryUrlPattern, web_pg)

    for item in m:
        urlList.append(str(base) + str(item.split('\"')[1]).replace("&#39;","\'"))

    return urlList 

def getCharacterUrlList():
    
    urlList = []

    aResp = urllib2.urlopen(characterInfo)
    web_pg = aResp.read();
    
    m = re.findall(characterUrlPattern, web_pg)

    for item in m:
        urlList.append(str(base) + str(item.split('\"')[1]).replace("&#39;","\'"))

    return urlList 

def getWeaponInfo(urlList, index):

    weaponInfoList = []

    aResp = urllib2.urlopen(str(urlList[index]).rstrip('\n'));
    web_pg = aResp.read();
    name = re.search(itemNamePattern, web_pg)
    itemType = re.search(itemTypePattern, web_pg)
    rarity = re.search(itemRarityPattern, web_pg)
    effect = re.search(itemEffectPattern, web_pg)
    soulBreak = re.search(itemSoulBreakPattern, web_pg)
    soulBreakInfo = re.search(itemSoulBreakPattern2, web_pg)

    if soulBreakInfo is not None:
        soulBreakInfo1 = re.split('<|>|\n',str(soulBreakInfo.group()))
    else:
        soulBreakInfo1 = ""

    m = re.findall(itemStatPattern, web_pg)

    name1 = re.split('<|>',str(name.group()))
    type1 = re.split('<|>|: ',str(itemType.group()))
    rarity1 = re.split('<|>',str(rarity.group()))
    effect1 = re.split('<|>|\n',str(effect.group()))
    soulBreak1 = re.split('<|>|\n',str(soulBreak.group()))

    weaponInfoList.append("Name: " + str(name1[2]).replace("&#39;","\'"))
    weaponInfoList.append("Type: " + str(type1[3]))
    weaponInfoList.append("Rarity: " + str(rarity1[4]).rstrip())

    for i, j, k, in zip(m,m[1::],m[2::]):
        if i == "Attack":
            weaponInfoList.append(str(i) + ": " + str(k))
        if i == "Magic":
            weaponInfoList.append(str(i) + ": " + str(k))
        if i == "Accuracy":
            weaponInfoList.append(str(i) + ": " + str(k))
        if i == "Defense":
            weaponInfoList.append(str(i) + ": " + str(k))
        if i == "Resistance":
            weaponInfoList.append(str(i) + ": " + str(k))
        if i == "Evasion":
            weaponInfoList.append(str(i) + ": " + str(k))
        if i == "Mind":
            weaponInfoList.append(str(i) + ": " + str(k))
        if i == "Speed":
            weaponInfoList.append(str(i) + ": " + str(k))

    weaponInfoList.append("Effect: " + str(effect1[3]).replace("&#39;","\'"))

    # needs fine tuning for soul break descriptions to not break it
    if str(soulBreak1[3]) == "None":
        weaponInfoList.append("Soul Break: " + str(soulBreak1[3]).replace("&#39;","\'"))
    else:
        weaponInfoList.append("Soul Break: " + str(soulBreak1[5]).replace("&#39;","\'"))

    # print weaponInfoList
    return weaponInfoList

def getArmorInfo(urlList, index):

    armorInfoList = []

    aResp = urllib2.urlopen(str(urlList[index]).rstrip('\n'));
    web_pg = aResp.read();
    name = re.search(itemNamePattern, web_pg)
    itemType = re.search(itemTypePattern, web_pg)
    rarity = re.search(itemRarityPattern, web_pg)
    effect = re.search(itemEffectPattern, web_pg)
    soulBreak = re.search(itemSoulBreakPattern, web_pg)
    soulBreakInfo = re.search(itemSoulBreakPattern2, web_pg)

    if soulBreakInfo is not None:
        soulBreakInfo1 = re.split('<|>|\n',str(soulBreakInfo.group()))
    else:
        soulBreakInfo1 = ""

    m = re.findall(itemStatPattern, web_pg)

    name1 = re.split('<|>',str(name.group()))
    type1 = re.split('<|>|: ',str(itemType.group()))
    rarity1 = re.split('<|>',str(rarity.group()))
    effect1 = re.split('<|>|\n',str(effect.group()))
    soulBreak1 = re.split('<|>|\n',str(soulBreak.group()))

    armorInfoList.append("Name: " + str(name1[2]).replace("&#39;","\'"))
    armorInfoList.append("Type: " + str(type1[3]))
    armorInfoList.append("Rarity: " + str(rarity1[4]).rstrip())

    for i, j, k, in zip(m,m[1::],m[2::]):
        if i == "Attack":
            armorInfoList.append(str(i) + ": " + str(k))
        if i == "Magic":
            armorInfoList.append(str(i) + ": " + str(k))
        if i == "Accuracy":
            armorInfoList.append(str(i) + ": " + str(k))
        if i == "Defense":
            armorInfoList.append(str(i) + ": " + str(k))
        if i == "Resistance":
            armorInfoList.append(str(i) + ": " + str(k))
        if i == "Evasion":
            armorInfoList.append(str(i) + ": " + str(k))
        if i == "Mind":
            armorInfoList.append(str(i) + ": " + str(k))
        if i == "Speed":
            armorInfoList.append(str(i) + ": " + str(k))

    armorInfoList.append("Effect: " + str(effect1[3]).replace("&#39;","\'"))

    # needs fine tuning for soul break descriptions to not break it
    if str(soulBreak1[3]) == "None":
        armorInfoList.append("Soul Break: " + str(soulBreak1[3]).replace("&#39;","\'"))
    else:
        armorInfoList.append("Soul Break: " + str(soulBreak1[5]).replace("&#39;","\'"))

    return armorInfoList

def getAccessoryInfo(urlList, index):

    accessoryInfoList = []

    aResp = urllib2.urlopen(str(urlList[index]).rstrip('\n'));
    web_pg = aResp.read();
    name = re.search(itemNamePattern, web_pg)
    itemType = re.search(itemTypePattern, web_pg)
    rarity = re.search(itemRarityPattern, web_pg)
    effect = re.search(accessoryEffectPattern, web_pg)
    # soulBreak = re.search(itemSoulBreakPattern, web_pg)
    # soulBreakInfo = re.search(itemSoulBreakPattern2, web_pg)

    m = re.findall(itemStatPattern, web_pg)

    # Validity checks
    if effect is not None:
        # print str(effect.group())
        effect1 = re.split('<|>|\n',str(effect.group()))
        effect2 = str(effect1[3]).replace("&#39;","\'")
    else:
        effect2 = "None"

    # if soulBreakInfo is not None:
    #     soulBreakInfo1 = re.split('<|>|\n',str(soulBreakInfo.group()))
    # else:
    #     soulBreakInfo1 = ""


    name1 = re.split('<|>',str(name.group()))
    rarity1 = re.split('<|>',str(rarity.group()))
    # effect1 = re.split('<|>|\n',str(effect.group()))
    # soulBreak1 = re.split('<|>|\n',str(soulBreak.group()))

    accessoryInfoList.append("Name: " + str(name1[2]).replace("&#39;","\'"))
    accessoryInfoList.append("Type: Accessory")
    accessoryInfoList.append("Rarity: " + str(rarity1[4]).rstrip())

    if m is not None:
        for i, j, k, in zip(m,m[1::],m[2::]):
            if i == "Attack":
                accessoryInfoList.append(str(i) + ": " + str(k))
            elif i == "Magic":
                accessoryInfoList.append(str(i) + ": " + str(k))
            elif i == "Accuracy":
                accessoryInfoList.append(str(i) + ": " + str(k))
            elif i == "Defense":
                accessoryInfoList.append(str(i) + ": " + str(k))
            elif i == "Resistance":
                accessoryInfoList.append(str(i) + ": " + str(k))
            elif i == "Evasion":
                accessoryInfoList.append(str(i) + ": " + str(k))
            elif i == "Mind":
                accessoryInfoList.append(str(i) + ": " + str(k))
            elif i == "Speed":
                accessoryInfoList.append(str(i) + ": " + str(k))

    accessoryInfoList.append("Effect: " + str(effect2))

    # # needs fine tuning for soul break descriptions to not break it
    # if str(soulBreak1[3]) == "None":
    #     accessoryInfoList.append("Soul Break: " + str(soulBreak1[3]).replace("&#39;","\'"))
    # else:
    #     accessoryInfoList.append("Soul Break: " + str(soulBreak1[5]).replace("&#39;","\'"))

    return accessoryInfoList

def getCharacterInfo(urlList, index):

    character = []

    aResp = urllib2.urlopen(str(urlList[index]).rstrip('\n'));
    web_pg = aResp.read();
    name = re.search(charNamePattern, web_pg)
    world = re.search(charWorldPattern, web_pg)
    role = re.search(charRolePattern, web_pg)
    
    m = re.findall(charStatPattern, web_pg)
    n = re.findall(charAbilityPattern, web_pg)

    useTypes = []
    abilityTypes = []

    length = len(m)
    i = 35
    while True:
        if i == length:
            break
        else:
            useTypes.append(str(m[i]).replace("<br />"," - "))
            i = i + 1

    length = len(n)
    i = 0
    while True:
        if i == length:
            break
        else:
            abilityTypes.append(str(n[i]).replace("<br />"," - "))
            i = i + 1

    name1 = re.split('<|>',str(name.group()).replace("&#39;","\'"))
    world1 = re.split('<|>',str(world.group()).replace("&#39;","\'"))
    role1 = re.split('<|>|: ',str(role.group()).replace("&#39;","\'"))

    lvl =  m[3]
    hp = m[6]
    attack = m[9]
    defense = m[12]
    magic = m[15]
    resistance = m[18]
    mind = m[21]
    accuracy = m[24]
    evasion = m[27]
    speed = m[30]
    soulBreak = re.split('<|>',str(m[33]))
    soulBreakDesc = m[34]

    # loading stats into list
    character.append(str(name1[2]))
    character.append(str(world1[4]))
    character.append(str(role1[3]))
    character.append(str(hp))
    character.append(str(attack))
    character.append(str(defense))
    character.append(str(magic))
    character.append(str(resistance))
    character.append(str(mind))
    character.append(str(accuracy))
    character.append(str(evasion))
    character.append(str(speed))
    character.append(str(soulBreak[2]).replace("&#39;","\'") + " - " + str(soulBreakDesc).replace("&#39;","\'"))


    nlen = len(useTypes)
    wlen = len(weaponList)
    arlen = len(armorList)

    tempWepList = []
    tempArmorList = []

    # weapon types
    i = 0
    j = 0
    while(i < nlen):
        j = 0
        while(j < wlen):
            if useTypes[i] == weaponList[j]:
                tempWepList.append(str(useTypes[i]))
            j = j + 1
        i = i + 1

    # armor types
    i = 0
    j = 0
    while(i < nlen):
        j = 0
        while(j < arlen):
            if useTypes[i] == armorList[j]:
                tempArmorList.append(str(useTypes[i]))
            j = j + 1
        i = i + 1

    character.append(tempWepList)
    character.append(tempArmorList)
    character.append(abilityTypes)

    return character

# TODO
def outputJsonFile(info, dataType, outFile):

    atk = 0
    matk = 0
    acc = 0
    deff = 0
    res = 0
    eva = 0
    mnd = 0
    spd = 0
    
    atk1 = ""
    matk1 = ""
    acc1 = ""
    def1 = ""
    res1 = ""
    eva1 = ""
    mnd1 = ""
    spd1 = ""
    
    atk2 = ""
    matk2 = ""
    acc2 = ""
    def2 = ""
    res2 = ""
    eva2 = ""
    mnd2 = ""
    spd2 = ""

    atk3 = ""
    matk3 = ""
    acc3 = ""
    def3 = ""
    res3 = ""
    eva3 = ""
    mnd3 = ""
    spd3 = ""

    # {
    # "weapons": [
    # {
    #     "name":"Knife (II)",
    #     "id":"",
    #     "type":"Dagger",
    #     "origin":"II",
    #     "rarity":"1",
    #     "attack":"19",
    #     "defense":"0",
    #     "magic":"0",
    #     "resistance":"0",
    #     "mind":"0",
    #     "accuracy":"83",
    #     "evasion":"0",
    #     "effect":"None",
    #     "soul_break":"None",
    #     "obtained":"",
    #     "record_synergy_bonus":
    #     {
    #         "base":
    #         {
    #             "attack":"",
    #             "defense":"",
    #             "magic":"",
    #             "resistance":"",
    #             "mind":"",
    #             "accuracy":"",
    #             "evasion":""
    #         },
    #         "base+":
    #         {
    #             "attack":"",
    #             "defense":"",
    #             "magic":"",
    #             "resistance":"",
    #             "mind":"",
    #             "accuracy":"",
    #             "evasion":""
    #         },
    #         "base++":
    #         {
    #             "attack":"",
    #             "defense":"",
    #             "magic":"",
    #             "resistance":"",
    #             "mind":"",
    #             "accuracy":"",
    #             "evasion":""
    #         }
    #     }
    # },

    print >> outFile, "{\n\t\"" + str(dataType) + "\": ["

    for i in infoList:
        print >> outFile, "\t{\n\t\t\"name\":\"" + str(name2) + "\","

    if index == (len(urlList) - 1):
        print >> outFile, "\t{\n\t\t\"name\":\"" + str(name2) + "\",\n\t\t\"id\":\"" + str(id2) + "\",\n\t\t\"type\":\"" + str(type2) + "\",\n\t\t\"origin\":\"" + str(origin2) + "\",\n\t\t\"rarity\":\"" + str(rarity2) + "\",\n\t\t\"attack\":\"" + str(atk) + "\",\n\t\t\"defense\":\"" + str(deff) + "\",\n\t\t\"magic\":\"" + str(matk) + "\",\n\t\t\"resistance\":\"" + str(res) + "\",\n\t\t\"mind\":\"" + str(mnd) + "\",\n\t\t\"accuracy\":\"" + str(acc) + "\",\n\t\t\"evasion\":\"" + str(eva) + "\",\n\t\t\"effect\":\"" + str(effect2) + "\",\n\t\t\"soul_break\":\"" + str(soulBreak2) + "\",\n\t\t\"obtained\":\"" + str(obtained) + "\",\n\t\t\"record_synergy_bonus\":\n\t\t{\n\t\t\t\"base\":\n\t\t\t{\n\t\t\t\t\"attack\":\"" + str(atk1) + "\",\n\t\t\t\t\"defense\":\"" + str(def1) + "\",\n\t\t\t\t\"magic\":\"" + str(matk1) + "\",\n\t\t\t\t\"resistance\":\"" + str(res1) + "\",\n\t\t\t\t\"mind\":\"" + str(mnd1) + "\",\n\t\t\t\t\"accuracy\":\"" + str(acc1) + "\",\n\t\t\t\t\"evasion\":\"" + str(eva1) + "\"\n\t\t\t},\n\t\t\t\"base+\":\n\t\t\t{\n\t\t\t\t\"attack\":\"" + str(atk2) + "\",\n\t\t\t\t\"defense\":\"" + str(def2) + "\",\n\t\t\t\t\"magic\":\"" + str(matk2) + "\",\n\t\t\t\t\"resistance\":\"" + str(res2) + "\",\n\t\t\t\t\"mind\":\"" + str(mnd2) + "\",\n\t\t\t\t\"accuracy\":\"" + str(acc2) + "\",\n\t\t\t\t\"evasion\":\"" + str(eva2) + "\"\n\t\t\t},\n\t\t\t\"base++\":\n\t\t\t{\n\t\t\t\t\"attack\":\"" + str(atk3) + "\",\n\t\t\t\t\"defense\":\"" + str(def3) + "\",\n\t\t\t\t\"magic\":\"" + str(matk3) + "\",\n\t\t\t\t\"resistance\":\"" + str(res3) + "\",\n\t\t\t\t\"mind\":\"" + str(mnd3) + "\",\n\t\t\t\t\"accuracy\":\"" + str(acc3) + "\",\n\t\t\t\t\"evasion\":\"" + str(eva3) + "\"\n\t\t\t}\n\t\t}\n\t}\n]}"
    else:
        print >> outFile, "\t{\n\t\t\"name\":\"" + str(name2) + "\",\n\t\t\"id\":\"" + str(id2) + "\",\n\t\t\"type\":\"" + str(type2) + "\",\n\t\t\"origin\":\"" + str(origin2) + "\",\n\t\t\"rarity\":\"" + str(rarity2) + "\",\n\t\t\"attack\":\"" + str(atk) + "\",\n\t\t\"defense\":\"" + str(deff) + "\",\n\t\t\"magic\":\"" + str(matk) + "\",\n\t\t\"resistance\":\"" + str(res) + "\",\n\t\t\"mind\":\"" + str(mnd) + "\",\n\t\t\"accuracy\":\"" + str(acc) + "\",\n\t\t\"evasion\":\"" + str(eva) + "\",\n\t\t\"effect\":\"" + str(effect2) + "\",\n\t\t\"soul_break\":\"" + str(soulBreak2) + "\",\n\t\t\"obtained\":\"" + str(obtained) + "\",\n\t\t\"record_synergy_bonus\":\n\t\t{\n\t\t\t\"base\":\n\t\t\t{\n\t\t\t\t\"attack\":\"" + str(atk1) + "\",\n\t\t\t\t\"defense\":\"" + str(def1) + "\",\n\t\t\t\t\"magic\":\"" + str(matk1) + "\",\n\t\t\t\t\"resistance\":\"" + str(res1) + "\",\n\t\t\t\t\"mind\":\"" + str(mnd1) + "\",\n\t\t\t\t\"accuracy\":\"" + str(acc1) + "\",\n\t\t\t\t\"evasion\":\"" + str(eva1) + "\"\n\t\t\t},\n\t\t\t\"base+\":\n\t\t\t{\n\t\t\t\t\"attack\":\"" + str(atk2) + "\",\n\t\t\t\t\"defense\":\"" + str(def2) + "\",\n\t\t\t\t\"magic\":\"" + str(matk2) + "\",\n\t\t\t\t\"resistance\":\"" + str(res2) + "\",\n\t\t\t\t\"mind\":\"" + str(mnd2) + "\",\n\t\t\t\t\"accuracy\":\"" + str(acc2) + "\",\n\t\t\t\t\"evasion\":\"" + str(eva2) + "\"\n\t\t\t},\n\t\t\t\"base++\":\n\t\t\t{\n\t\t\t\t\"attack\":\"" + str(atk3) + "\",\n\t\t\t\t\"defense\":\"" + str(def3) + "\",\n\t\t\t\t\"magic\":\"" + str(matk3) + "\",\n\t\t\t\t\"resistance\":\"" + str(res3) + "\",\n\t\t\t\t\"mind\":\"" + str(mnd3) + "\",\n\t\t\t\t\"accuracy\":\"" + str(acc3) + "\",\n\t\t\t\t\"evasion\":\"" + str(eva3) + "\"\n\t\t\t}\n\t\t}\n\t},"

    print >> outFile, "\n"

# TODO
def outputCsvFile(infoList, outFile):

    for item in infoList:
        for e in item:
            if e.find("Name") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Type") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Rarity") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Attack") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Magic") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Accuracy") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Defense") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Resistance") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Evasion") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Mind") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Speed") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Effect") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Soul Break") != -1:
                print >> outFile, e.replace(": ", ":\t")
        print >> outFile, "\n"

# TODO
def outputTabbedTxtFileWithSynergy(infoList, outFile):

    # Equipment Name  Origin Rarity Attack Magic Accuracy Defense Resistance Evasion Mind Speed Special Effect   RS Attack RS Magic RS Accuracy RS Defense RS Resistance RS Evasion RS Mind RS Speed   RS Attack+ RS Magic+ RS Accuracy+ RS Defense+ RS Resistance+ RS Evasion+ RS Mind+ RS Speed+  RS Attack++ RS Magic++ RS Accuracy++ RS Defense++ RS Resistance++ RS Evasion++ RS Mind++ RS Speed++ 
    print >> outFile, "Equipment Name\tOrigin\tRarity\tAttack\tMagic\tAccuracy\tDefense\tResistance\tEvasion\tMind\tSpeed\tSpecial Effect\tRS Attack\tRS Magic\tRS Accuracy\tRS Defense\tRS Resistance\tRS Evasion\tRS Mind\tRS Speed\tRS Attack+\tRS Magic+\tRS Accuracy+\tRS Defense+\tRS Resistance+\tRS Evasion+\tRS Mind+\tRS Speed+\tRS Attack++\tRS Magic++\tRS Accuracy++\tRS Defense++\tRS Resistance++\tRS Evasion++\tRS Mind++\tRS Speed++"

    for item in infoList:
        for e in item:
            if e.find("Name") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Type") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Rarity") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Attack") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Magic") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Accuracy") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Defense") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Resistance") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Evasion") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Mind") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Speed") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Effect") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Soul Break") != -1:
                print >> outFile, e.replace(": ", ":\t")
        print >> outFile, "\n"

# TODO
def outputTabbedTxtFile(infoList, outFile):

    # Equipment Name  Origin Rarity Attack Magic Accuracy Defense Resistance Evasion Mind Speed Special Effect   RS Attack RS Magic RS Accuracy RS Defense RS Resistance RS Evasion RS Mind RS Speed   RS Attack+ RS Magic+ RS Accuracy+ RS Defense+ RS Resistance+ RS Evasion+ RS Mind+ RS Speed+  RS Attack++ RS Magic++ RS Accuracy++ RS Defense++ RS Resistance++ RS Evasion++ RS Mind++ RS Speed++ 
    print >> outFile, "Equipment Name\tOrigin\tRarity\tAttack\tMagic\tAccuracy\tDefense\tResistance\tEvasion\tMind\tSpeed\tSpecial Effect"

    for item in infoList:
        for e in item:
            if e.find("Name") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Type") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Rarity") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Attack") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Magic") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Accuracy") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Defense") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Resistance") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Evasion") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Mind") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Speed") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Effect") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Soul Break") != -1:
                print >> outFile, e.replace(": ", ":\t")
        print >> outFile, "\n"

def outputTextFile(infoList, outFile):

    for item in infoList:
        for e in item:
            if e.find("Name") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Type") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Rarity") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Attack") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Magic") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Accuracy") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Defense") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Resistance") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Evasion") != -1:
                print >> outFile, e.replace(": ", ":\t")
            elif e.find("Mind") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Speed") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Effect") != -1:
                print >> outFile, e.replace(": ", ":\t\t")
            elif e.find("Soul Break") != -1:
                print >> outFile, e.replace(": ", ":\t")
        print >> outFile, "\n"

    # WORKS BUT USES SPACES, NOT TABS
    # for item in infoList:
    #     print >> outFile, item[0] + "\n", '\n'.join(map(str, item[1:]))
    #     print >> outFile, "\n"

def saveData(infoList, dataFile):

    for item in infoList:
        print >> dataFile, item[0] + ',', ', '.join(map(str, item[1:]))

def loadData(dataFile):

    infoList = []

    # for line in dataFle:

    #     temp = dataFile.readline().rstrip('\n')
    #     re.split(',',str())

    line = dataFile.readline().rstrip('\n')
    line1 = re.split(', ',str(line))

    infoList.append(line1)

    while line:
        # print line
        line = dataFile.readline().rstrip('\n')
        line1 = re.split(', ',str(line))
    
        infoList.append(line1)

    # remove empty element at the end of the list
    infoList.pop()

    return infoList

def buildList(dataType, length):

    infoList = []
    i = 0

    while True:
        if i == length:
            break
        else:
            if dataType == "weapon":
                infoList.append(getWeaponInfo(getWeaponUrlList(), i))
            elif dataType == "armor":
                infoList.append(getArmorInfo(getArmorUrlList(), i))
            elif dataType == "accessory":
                infoList.append(getAccessoryInfo(getAccessoryUrlList(), i))
            elif dataType == "character":
                infoList.append(getCharacterInfo(getCharacterUrlList(), i))
            i = i + 1

    return infoList

def findStat(infoList, stat):
    # potentially make a new list and return new list for further processing
    temp = []
    for item in infoList:
        for e in item:
            if e.find(stat) != -1:
                # print item
                temp.append(item)
                break
    return temp

# def sortList(infoList, sort):
#     for item in infoList:
#         for e in item:
#             if e.find(stat) != -1:
#                 # print item
#                 break


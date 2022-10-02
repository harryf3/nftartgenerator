from PIL import Image
import os
import random

partdirs = ['eyes','heads','horns','mouths','shirts']

#secondaryToChange = 'ff0000'
#primaryToChange = '000fff'

randHEX = lambda: ('#%02X%02X%02X' % (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
print(randHEX())

primaryToChange = (0,15,255,255)
secondaryToChange = (255,0,0,255)


primaryColors = 'primary.png'
secondaryColors = 'secondary.png'

def colorSetup(file):
    imgFile = Image.open(file)
    priDict = {}
    for x in range(imgFile.size[0]):
        for y in range(imgFile.size[1]):
            priDict[x] = (imgFile.getpixel((x,y)))
    return priDict

primaryColorsDict = colorSetup(primaryColors)
secondaryColorsDict = colorSetup(secondaryColors)

def partSetup():
    allparts = {}
    for pd in partdirs:
        partdic = {}
        partsin = os.listdir(pd)
        for i,p in enumerate(partsin):
            partdic[i] = (Image.open(f'{pd}/{p}'))
        allparts[pd] = partdic
    return allparts

parts = partSetup()


def changeColor(img,primaryColor,secondaryColor,replacePrimary,replaceSecondary):
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if(img.getpixel((x,y)) == primaryColor):
                img.putpixel((x,y), replacePrimary)
            elif(img.getpixel((x,y)) == secondaryColor):
                img.putpixel((x,y), replaceSecondary)
    return img

def overlay(parts,backgroundColor = (0,0,0,0)):
    overlayed = Image.new(mode='RGBA',size = (64,64),color=backgroundColor)
    for part in parts:
        overlayed.paste(part,(0,0),part)
    return overlayed

def quickPartChange(partType):
    attr = [random.choice(list(parts[partType].keys())), random.choice(list(primaryColorsDict.keys())), random.choice(list(secondaryColorsDict.keys()))]
    part = changeColor(parts[partType][attr[0]], primaryToChange, secondaryToChange, primaryColorsDict[attr[1]], secondaryColorsDict[attr[2]])
    return [attr,part]

def createCharacter(parts):
    partChosen = []
    ids = []

    shirt = quickPartChange('shirts')
    partChosen.append(shirt[1])
    ids += (shirt[0])

    head = quickPartChange('heads')
    partChosen.append(head[1])
    ids += (head[0])

    horn = quickPartChange('horns')
    partChosen.append(horn[1])
    ids += (horn[0])

    eye = quickPartChange('eyes')
    partChosen.append(eye[1])
    ids += (eye[0])

    mouth = quickPartChange('mouths')
    partChosen.append(mouth[1])
    ids += (mouth[0])

    return (''.join([str(i) for i in ids]),overlay(partChosen))

def createMult(path,tries):
    made = []
    for i in range(tries):
        ch = createCharacter(parts)
        if ch[0] not in made:
            made.append(ch[0])
            ch[1].save(f'{path}/{ch[0]}.png','PNG')
            print(f'Created {len(made)}')
createMult('created',1000)
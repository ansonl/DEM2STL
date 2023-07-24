from sourceDEM import *
from hydrographicMask import *

print('Available Steps:')
print('1 - Generate Source DEM commands')
print()

savedValues = {}

modelResolution = 250
targetSRS = 'ESRI:102004'

while 1:
    choiceNum = 0
    print('Enter the step numbers (ex:1) to run in order. Enter negative number or letter to exit.')
    print('1. Source DEM')
    print('2. Coastline Mask')
    print('3. Coastline Mask')
    print('2. Coastline Mask')
    print('2. Coastline Mask')
    print('2. Coastline Mask')
    print('2. Coastline Mask')
    print('2. Coastline Mask')



    print()
    print('Saved values:')
    print(savedValues)
    
    cancel = False

    choices = input('>').split(' ')
    for c in choices:
        if c.isdigit():
            choiceNum = int(choice)
            if choiceNum == 1:
                savedValues['sourceDEMOutputHighestResFilename'], savedValues['sourceDEMOutputPrintedResFilename'] = generateSourceDEMCommands(modelResolution)
                continue
            if choiceNum == 2:
                savedValues['coastlinesRasterFilename'] = generateCoastlineDEMCommands(savedValues['sourceDEMOutputHighestResFilename'])
                continue
            if choiceNum == 3:
                savedValues['hydrographicMaskRasterFilename'] = generateHydrographicMaskFinalCommands(savedValues['coastlinesRasterFilename'], 'xxx', 'xxx', targetSRS, modelResolution)
                continue
            elif choiceNum < 0:
                cancel = True
                break
            else:
                print('Invalid step number')
        else:
            print('Invalid input')
            cancel = True
            break
    
    if cancel == True:
        break
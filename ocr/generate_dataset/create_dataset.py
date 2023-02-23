from PIL import Image
import os
import random
import numpy as np
import cv2
import imutils
import csv
from tqdm import tqdm

fonts = ['roya_bold']
# templates = [os.path.basename(os.path.splitext(template)[0]) for template in os.listdir('Templates') if template.endswith('.png') and template not in ['tashrifat.png', 'template-sepah.png', 'template-police.png']]
templates = ['template-base']

# Noises
noises = os.listdir('Noises')
# transformations 
transformations = ['zoom_in']
#transformations = []
# Count of permutations
permutations = 5

numbers_code = [i for i in range(10, 100)]
numbers_2 = [i for i in range(10, 100) if i%10]
numbers_3 = [j*10 + i for i in range(1, 10) for j in numbers_2 if i%10]
letters = ['ALEF', 'BE', 'PE', 'TE', 'SE', 'JIM', 'CHE', 'HE', 'KHE', 'DAL', 'ZAL', 'RE', 'ZE', 'ZHE', 'SIN','SHIN', 'SAD', 'ZAD', 'TA', 'ZA', 'EIN', 'GHEIN', 'FE', 'GHAF', 'KAF', 'GAF', 'LAM', 'MIM', 'NON', 'VAV', 'HA', 'YE']
places = [95, 155, 230, 315, 365, 420, 495, 555]


# Returns a plate as a string
def getPlateName(n1, n2, l, n3, n4, n5, n6, n7):
    return f'{n1}{n2}{l}{n3}{n4}{n5}{n6}{n7}'

# Returns Address of a glyph image given font, and glyph name
def getGlyphAddress(font, glyphName):
    return f'Glyphs/{font}/{glyphName}_trim.png'
    # return f'Glyphs/{font}/{glyphName}.png'

# Returns an array containing a plate's letter and numbers:
# [number1, number2 , letter, number3, number4, number5]

def getNewPlate ():
    selected_2 = random.choice(numbers_2)
    selected_3 = random.choice(numbers_3)
    selected_letter = '0'
    while selected_letter.isdigit():
      selected_letter = random.choice(letters)
    selected_code = random.choice(numbers_code)
    return [selected_2//10, selected_2 % 10, selected_letter, selected_3//100, (selected_3 % 100) // 10, selected_3%10, selected_code // 10, selected_code % 10]

# Genrate Noise
def applyNoise (plate, repeat=3):
    background = plate.convert("RGBA")
    noisyTemplates = []
    [random.choice(noises) for _ in range(repeat)]
    for noise in noises:
        newPlate = Image.new('RGBA', (600,132), (0, 0, 0, 0))
        newPlate.paste(background, (0,0))
        noise = Image.open(os.path.join('Noises/', noise)).convert("RGBA")
        newPlate.paste(noise, (0, 0), mask=noise)
        noisyTemplates.append(newPlate)
    return noisyTemplates

# Generate Transformations of plates
def applyTransforms (plate, repeat=3):
    transformedTemplates = []
    plate = np.array(plate)
    
    # Rotating to clockwise
    for _ in range(repeat):
        result = imutils.rotate_bound(plate, random.randint(2,7))
        result = Image.fromarray(result)
        transformedTemplates.append(result)

    # Rotating to anticlockwise
    for _ in range(repeat):
        result = imutils.rotate_bound(plate, random.randint(-7,-2))
        result = Image.fromarray(result)
        transformedTemplates.append(result)
    
    # Scaling up
    for _ in range(repeat):
        height, width, _ = plate.shape
        randScale = random.uniform(1.1, 1.3)
        result = cv2.resize(plate, None, fx=randScale, fy=randScale, interpolation = cv2.INTER_CUBIC)
        result = Image.fromarray(result)
        transformedTemplates.append(result)
    
    # Scaling down
    for _ in range(repeat):
        height, width, _ = plate.shape
        randScale = random.uniform(0.2, 0.6)
        result = cv2.resize(plate, None, fx=randScale, fy=randScale, interpolation = cv2.INTER_CUBIC)
        result = Image.fromarray(result)
        transformedTemplates.append(result)

    # # Adding perspective transformations
    # for _ in range(3):
    #     rows,cols,ch = plate.shape
    #     background = Image.fromarray(np.zeros(cols + 100, rows + 100, 3))
    #     pts1 = np.float32([[50,50],[200,50],[50,200]])
    #     pts2 = np.float32([[10,100],[200,50],[100,250]])
    #     M = cv2.getAffineTransform(pts1,pts2)
    #     result = cv2.warpAffine(plate,M,(cols,rows))
    #     result = Image.fromarray(result)
    #     transformedTemplates.append(result)
    
    return transformedTemplates


idCounter = 0
fontsProgBar = tqdm(total=len(fonts)*len(templates)*permutations*len(noises)*(len(transformations)-1)*3, desc='Generating Plate...')
for font in fonts:
    # Create font directory if not exists
    if not os.path.exists(font): os.mkdir(font)
    # time.sleep(0.1)

    # Getting the letters list from nameMap csv
    letters = []
    with open(f'Fonts/{font}_namesMap.csv') as nameMapCsv:
        reader = csv.reader(nameMapCsv)
        next(reader) # Skipping header
        letters = [rows[1] for rows in reader]

    for template in templates:
        for i in range(permutations):
            idCounter += 1

            # Generate a plate as an array
            # e.g. ['3', '7', 'GAF', '8', '5', '3']
            plate = getNewPlate()
            # print(plate)
            # Get the plate name as string
            # e.g. 37_GAF_853
            plateName = label = getPlateName(*plate)

            # Get Glyph images of plate characters
            glyphImages = []
            for glyph in plate:
                glyphImage = Image.open(getGlyphAddress(font, glyph)).convert("RGBA")
                # number.putalpha(255)
                glyphImages.append(glyphImage)

            # Create a blank image with size of templates 
            # and add the background and glyph images
            newPlate = Image.new('RGBA', (600,132), (0, 0, 0, 0))
            background = Image.open(f'Templates/{template}.png').convert("RGBA")
            newPlate.paste(background, (0,0))
            # adding glyph images with 11 pixel margin
            w = 0
            for i, glyph in enumerate(glyphImages):
                glyph_x = places[i] - (glyph.size[0])//2
                glyph_y = 66 - (glyph.size[1])//2
                newPlate.paste(glyph, (glyph_x, glyph_y), mask=glyph)
            
            idCounter += 1
            # Save Simple Plate
            _newPlate = newPlate.resize((312,70), Image.ANTIALIAS)
            fontsProgBar.update(1)
            _newPlate.save(f"{font}/{plateName}_{template.split('-')[1]}{random.randint(0,20)}{idCounter}.png")
            # newPlate.show(f"{font}/{plateName}_{template.split('-')[1]}.png")
            
            idCounter += 1
            
            noisyTemplates = applyNoise(newPlate)
            for noisyTemplate in noisyTemplates[:1]:
                idCounter += 1
                fontsProgBar.update(1)
                _noisyTemplate = noisyTemplate.resize((312,70), Image.ANTIALIAS)
                _noisyTemplate.save(f"{font}/{plateName}_{template.split('-')[1]}{random.randint(0,20)}{idCounter}.png")
                transformedTemplates = applyTransforms(noisyTemplate)
                for transformedTemplate in transformedTemplates[:1]:
                    idCounter += 1
                    _transformedTemplate = transformedTemplate.resize((312,70), Image.ANTIALIAS)
                    fontsProgBar.update(1)
                    _transformedTemplate.save(f"{font}/{plateName}_{template.split('-')[1]}{random.randint(0,20)}{idCounter}.png")
            """"""
        fontsProgBar.update(1)
    fontsProgBar.update(1)
fontsProgBar.update(1)


fontsProgBar.close()



# Creating annotation file for generated plates
generated = [os.path.basename(os.path.splitext(plate)[0]) for plate in os.listdir('roya_bold') ]
plate_annotation = [f'{p}.png, "{p.split("_")[0]}"' for p in generated]
plate_annotation.sort()
print('Number of generated plates:', len(plate_annotation))
with open(f'annotation_{font}.txt', 'w') as f:
  f.write('\n'.join(plate_annotation))


# Creating character dictionary
char_dictionary = '\n'.join(letters)+'\n'
with open('persian_dict.txt', 'w') as f:
  f.write(char_dictionary)

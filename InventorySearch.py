import os
import re
import shutil

######### CONFIG ##########

inventoryPath = '' # Path to the inventory folder (Needs to use / instead of \)
corePath = '' # QB ONLY # Path to the core folder (Needs to use / instead of \)

#### DO NOT EDIT BELOW ####

inventoryType = inventoryPath.split('/')[-1]
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

itemsPath = inventoryPath+'/data/items.lua' if inventoryType == 'ox_inventory' else corePath+'/shared/items.lua' # Path to the items folder
weaponsPath = inventoryPath+'/data/weapons.lua' if inventoryType == 'ox_inventory' else corePath+'/shared/weapons.lua' # Path to the weapons folder
imagePath = inventoryPath+'/web/images' if inventoryType == 'ox_inventory' else inventoryPath+'/html/images' # Path to the images folder
missingPath = desktop+'/missing.txt' # Path to the missing txt file
extrasPath = desktop+'/extras' # Path to the new extra images folder

missingPath = missingPath.replace('\\', '/')
extrasPath = extrasPath.replace('\\', '/')

image_list = []
item_list = []
weapon_list = []

if not os.path.exists(extrasPath):
    os.makedirs(extrasPath)

if not os.path.exists(missingPath):
    with open(missingPath, 'w') as f:
        pass

if inventoryType == 'ox_inventory':
    # Images
    for _, _, files in os.walk(imagePath):
        for file in files:
          filename = os.path.splitext(file)[0]
          image_list.append(filename)

    # Items
        with open(itemsPath, 'r') as file:
            content = file.read()

        double_quote_pattern = r'\["(.*?)"\]'
        single_quote_pattern = r"\['(.*?)'\]"

        double_quoted_texts = re.findall(double_quote_pattern, content)
        single_quoted_texts = re.findall(single_quote_pattern, content)
        for text in double_quoted_texts:
            item_list.append(text)

        for text in single_quoted_texts:
            item_list.append(text)


    # Weapons

        with open(weaponsPath, 'r') as file:
            content = file.read()

        double_quote_pattern = r'\["(.*?)"\]'
        single_quote_pattern = r"\['(.*?)'\]"

        double_quoted_texts = re.findall(double_quote_pattern, content)
        single_quoted_texts = re.findall(single_quote_pattern, content)
        for text in double_quoted_texts:
            weapon_list.append(text)

        for text in single_quoted_texts:
            weapon_list.append(text)
else:
    # Images
    for _, _, files in os.walk(imagePath):
        for file in files:
          filename = os.path.splitext(file)[0]
          image_list.append(filename)

    # Items
    count = 0
    with open(itemsPath, 'r') as file:
        for line in file:
            count += 1
            line = line.strip()
            if line and not line.startswith('-') and count >2: 
                item = line.split()[0]  
                item_list.append(item)

# Check for missing images

open(missingPath, 'w').close()
for item in item_list and weapon_list:
    if item not in image_list:
        with open(missingPath, 'a') as file:
            file.write(item + '\n')

# Move the extra images to the new folder

for image in image_list:
  if image not in item_list and image not in weapon_list:
    shutil.copy(imagePath + '/' + image + '.png', extrasPath + '/' + image + '.png')
    os.remove(imagePath + '/' + image + '.png')

print('Done!')

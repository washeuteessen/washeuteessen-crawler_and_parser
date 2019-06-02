import json
from jsonmerge import merge

with open('recipes/items_chefkoch_79k.txt', "r") as json_file:  
    json_file = json_file.read()
    recipes = json.load(json_file)

with open('recipes/src_img_73k.txt', "r") as json_file:  
    json_file = json_file.read()
    src_img = json.load(json_file)

print(recipes)
print(src_img)

# merged = merge(src_img, recipes)

# print(merged)

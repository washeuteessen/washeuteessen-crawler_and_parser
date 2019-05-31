import json
from jsonmerge import merge

# with open('recipes/items_chefkoch_80k.json', "r") as json_file:  
#     recipes = json.load(json_file)

# with open('recipes/scr_img_300.json', "r") as json_file:  
#     src_img = json.load(json_file)

input_file = open('recipes/scr_img_300.json')
json_array = json.load(input_file)
print(json_array)

# merged = merge(src_img, recipes)

# print(merged)

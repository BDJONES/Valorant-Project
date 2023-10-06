import json
import urllib.request
import requests
import os
import bs4
from matplotlib import pyplot as plt
from PIL import Image

def ranking_json_generator(obj):
    # create a formatted string of the Python JSON object
    result = os.path.exists('valorant_rankings.json')
    if result == False:
        f = open('valorant_rankings.json', 'w')  # Open file
        fileSize = os.path.getsize('valorant_rankings.json')
        if fileSize == 0:
            text = json.dumps(obj, sort_keys=True, indent=4)
            f.write(text)  # Write string
            f.close()  # Close the file
            print('Successfully created the json')

def weapon_json_generator(obj):
    # create a formatted string of the Python JSON object
    result = os.path.exists('valorant_weapons.json')
    if result == False:
        f = open('valorant_weapons.json', 'w')  # Open file
        fileSize = os.path.getsize('valorant_weapons.json')
        if fileSize == 0:
            text = json.dumps(obj, sort_keys=True, indent=4)
            f.write(text)  # Write string
            f.close()  # Close the file
            print('Successfully created the json')
            return True
    return False

def print_weapon_names(json_object):
    my_list = json_object['data']
    for i in range(len(my_list)):
        if i < len(my_list) - 1:
            print(my_list[i]['displayName'], end=', ')
        else:
            print(my_list[i]['displayName'])

def print_weapon_skin_names(json_object, weapon_name):
    my_list = json_object['data']
    skin_list = list()
    #print(len(my_list[0]['skins']))
    for i in range(len(my_list)):
        if my_list[i]['displayName'] == weapon_name:
            for j in range(len(my_list[i]['skins'])):
                if 'Standard' not in my_list[i]['skins'][j]['displayName']:
                    skin_list.append(my_list[i]['skins'][j]['displayName'])
    skin_list.sort()
    for i in range(len(skin_list)):
        if (i == len(skin_list) - 1):
            print(skin_list[i])
        else:
            print(skin_list[i],end=', ')

def display_skin_img(json_object, weapon_name, skin_name):
    my_list = json_object['data']
    img_url = ''
    for i in range(len(my_list)):
        if my_list[i]['displayName'] == weapon_name:
            for j in range(len(my_list[i]['skins'])):
                if my_list[i]['skins'][j]['chromas'][0]['displayName'] == skin_name:
                    img_url = my_list[i]['skins'][j]['chromas'][0]['fullRender']
    urllib.request.urlretrieve(img_url, f'{skin_name}.png')
    im1 = Image.open(f'{skin_name}.png')
    im1.show()

def load_ranked_dict(list1, list2, obj_json):
    my_dict = dict()
    rank_list = list()
    index = 0
    unaccepted_ranks = ['UNRANKED', 'Unused1', 'Unused2']
    for i in obj_json['data'][0]['tiers']:
        if (i['tierName'] not in unaccepted_ranks):
            rank_list.append(i['tierName'])
    #print(rank_list)
    for i in list1:
        my_dict[rank_list[index]] = i
        index += 1
    for i in list2:
        my_dict[rank_list[index]] = i
        index += 1
    for i in range(len(rank_list)):
        if (i == len(rank_list) - 1):
            print(rank_list[i])
        else:
            print(rank_list[i],end=', ')
    return my_dict

def display_rank_percentage(rank_choice, obj_json, my_dict):
    unaccepted_ranks = ['UNRANKED', 'Unused1', 'Unused2']
    for i in obj_json['data'][0]['tiers']:
        if (rank_choice in unaccepted_ranks):
            print('Type an accpeted rank')
            break
        elif((i['tierName'] not in unaccepted_ranks) and (i['tierName'] == rank_choice)):
            img_url = i['largeIcon']
            urllib.request.urlretrieve(img_url, f'{rank_choice}.png')
            im1 = Image.open(f'{rank_choice}.png')
            im1.show()
            print(f'{my_dict[rank_choice]} of players are in the {rank_choice} rank')

if __name__ == "__main__": 
    counter = 0
    print('Would you like to look at Valorant weapons or competitive tiers')
    user_input = ''
    while 1:
        try:
            user_input = input('Type either a \'w\' or a \'c\'\n')
            acceptable_input = ['w', 'c']
            if user_input not in acceptable_input:
                raise ValueError('Invalid input')
            break
        except ValueError as excpt:
            print(excpt)
        except:
            print('An error has occured')

    while 1:
        if user_input == 'w':
            url = 'https://valorant-api.com/v1/weapons'
            request_weapons = requests.get(url)
            weapons_json = request_weapons.json()
            print(request_weapons.status_code)
            weapon_json_generator(weapons_json)
            print_weapon_names(weapons_json)
            weapon_choice = input('Pick a weapon that you would like to look at\n')
            print_weapon_skin_names(weapons_json, weapon_choice)
            skin_choice = input('Which skin would you like to see? Type the name as displayed above\n')
            display_skin_img(weapons_json, weapon_choice, skin_choice)
        elif user_input == 'c':
            rank_pic_url = 'https://valorant-api.com/v1/competitivetiers'
            rank_stats_url = 'https://www.esportstales.com/valorant/rank-distribution-and-percentage-of-players-by-tier'
            request_tiers = requests.get(rank_pic_url)
            request_stats = requests.get(rank_stats_url)
            print(request_tiers.status_code)
            print(request_stats.status_code)
            soup = bs4.BeautifulSoup(request_stats.content)
            rank_table = soup.find(id = 'block-yui_3_17_2_1_1649943349040_82044')
            rank_cell = rank_table.find(class_ = 'tg')
            rank_distribution = rank_cell.find_all(class_ = 'tg-shjz')
            distribution_left_list = list()
            distribution_right_list = list()
            count = 0
            for i in  rank_distribution:
                if (i.get_text() != '') and (count % 2 == 0):
                    distribution_left_list.append(i.get_text())
                elif (i.get_text() != '') and (count % 2 == 1):
                    distribution_right_list.append(i.get_text())
                count += 1
                
            # print(distribution_left_list)
            # print(distribution_right_list)
            rank_json = request_tiers.json()
            ranking_json_generator(rank_json)
            rank_dict = load_ranked_dict(distribution_left_list, distribution_right_list, rank_json)
            rank_choice = input(f'Which rank would you like to look at?\nType the name as displayed above\n')
            display_rank_percentage(rank_choice, rank_json, rank_dict)
            #print(rank_dict)
            #print(my_api_json['data'][0]['tiers'][3]['tierName'])
            
        elif counter > 0 and user_input == 'q':
            print('Thank You')
            break
        else:
            print('Type a valid character')
        counter += 1

        print('Would you like to look at Valorant weapons or competitive tiers')
        print('If you would like to quit type \'q\'')
        user_input = input('Type either a \'w\', \'c\', \'q\'\n')
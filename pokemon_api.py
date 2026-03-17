import random
import requests

BASE_URL = "https://pokeapi.co/api/v2/"

def pokemon_data(id):
    id_str = str(id)
    url = f"{BASE_URL}pokemon/{id_str}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        english_name = data['name']
        jp_name = get_pokemon_japanese_name(english_name)
        type = data['types'][0]['type']['name']
        image_url = data['sprites']['front_default']
    return {
        'english_name': english_name,
        'jp_name': jp_name,
        'type': type,
        'image_url': image_url,
    }

def get_pokemon_japanese_name(english_name):
    response = requests.get(BASE_URL + f'pokemon-species/{english_name.lower()}')
    if response.ok:
        data = response.json()
        
        for name_info in data['names']:
            if name_info['language']['name'] == 'ja-hrkt':
                return name_info['name']
        return "日本語名が見つかりません。"
    else:
        return "ポケモンの情報を取得できませんでした。"

def get_pokemon_types():
    return [
        "normal",
        "fighting",
        "flying",
        "poison",
        "ground",
        "rock",
        "bug",
        "ghost",
        "steel",
        "fire",
        "water",
        "grass",
        "electric",
        "psychic",
        "ice",
        "dragon",
        "dark",
        "fairy",
    ]

def get_batsugun_tyeps(type):
    batsugun = {
        "fighting": ["normal", "ice", "rock", "dark", "steel"],
        "flying": ["grass", "fighting", "bug"],
        "poison": ["grass", "fairy"],
        "ground": ["fire", "electric", "poison", "rock", "steel"],
        "rock": ["fire", "ice", "flying", "bug"],
        "bug": ["grass", "psychic", "dark"],
        "ghost": ["psychic", "ghost"],
        "steel": ["ice", "rock", "fairy"],
        "fire": ["grass", "ice", "bug", "steel"],
        "water": ["fire", "ground", "rock"],
        "grass": ["water", "ground", "rock"],
        "electric": ["water", "flying"],
        "psychic": ["fighting", "poison"],
        "ice": ["grass", "ground", "flying", "dragon"],
        "dragon": ["dragon"],
        "dark": ["psychic", "ghost"],
        "fairy": ["fighting", "dragon", "dark"],
        "normal": ["nothing"],
    }
    return batsugun[type]

def make_choices_answer(type):
    batsugun = get_batsugun_tyeps(type)
    answer = random.sample(batsugun, 1)[0]
    types = get_pokemon_types()
    choices = list(set(batsugun) ^ set(types))
    if type in choices:
        choices.remove(type)
    choices = random.sample(choices, 3)
    choices.insert(random.randint(0,len(choices)), answer)
    return choices, answer

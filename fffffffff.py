# from faker import Faker
#
# faker = Faker()
#
# def generate_random_word():
#     return faker.word()
#
# print(type(generate_random_word()))
#
import requests

import json

json_string = '{"name": "Soldier face", "imageUrl": "https://www.wiggins.com/", "price": 10120, "description": "This movie about such traditional plan tree.", "location": "SPB", "published": false, "genreId": 7}'

movie_dict = json.loads(json_string)
print(movie_dict)
print(type(movie_dict))  # <class 'dict'>
from faker import Faker

faker = Faker()

def generate_random_word():
    return faker.word()

print(type(generate_random_word()))


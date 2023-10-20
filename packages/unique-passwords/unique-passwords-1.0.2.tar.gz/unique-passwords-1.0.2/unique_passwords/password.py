import random
import string

capitalLetters = string.ascii_uppercase
smallLetters = string.ascii_lowercase
numbers = string.digits
specialChar = "!@#$%^&?><|_-"


def generate_password(password_length):

    essential = [
        random.choice(smallLetters),
        random.choice(specialChar),
        random.choice(capitalLetters),
        random.choice(numbers)
    ]

    random_characters = [
        random.choice(random.choice([smallLetters, specialChar, capitalLetters, numbers]))
        for _ in range(password_length - len(essential))
    ]

    password_characters = essential + random_characters
    random.shuffle(password_characters)

    password = ''.join(password_characters)
    
    return password

def generate_multiple(password_length, password_number):
    return [generate_password(password_length) for _ in range(password_number)]
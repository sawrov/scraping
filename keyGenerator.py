import random


class Key:

    def __init__(self, key=''):
        if key == '':
            self.key = self.generate()
        else:
            self.key = key.lower()

    def verify(self):
        score = 0
        check_digit = self.key[2]
        check_digit_count = 0
        chunks = self.key.split('-')
        for chunk in chunks:
            if len(chunk) != 4:
                return False
            for char in chunk:
                if char == check_digit:
                    check_digit_count += 1
                score += ord(char)
        if score == 1392 and check_digit_count == 5:
            return True
        return False

    def generate(self):
        key = ''
        chunk = ''
        check_digit_count = 0
        alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
        while True:
            while len(key) < 25:
                char = random.choice(alphabet)
                key += char
                chunk += char
                if len(chunk) == 4:
                    key += '-'
                    chunk = ''
            key = key[:-1]
            if Key(key).verify():
                return key
            else:
                key = ''

    def __str__(self):
        valid = 'Invalid'
        if self.verify():
            valid = 'Valid'
        return self.key.upper() + ':' + valid


keys = []
no=int(input("How many keys do you want to generate: "))
while len(keys) < no:
    temp = Key()
    if temp in keys:
        pass
    else:
        print(temp)
        keys.append(temp)

print("THE LIST OF GENERATED KEYS ARE: \n")

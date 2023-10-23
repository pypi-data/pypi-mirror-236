import string
import random

class Crypto:
    def __init__(self, text, key):
        self.text = text
        self.key = key

    def encrypt(self):
        shift = self.key
        key_range = 10
        plain_text = self.text
        shift %= key_range
        alphabet = string.ascii_lowercase
        shifted = alphabet[shift:] + alphabet[:shift]
        table = str.maketrans(alphabet, shifted)
        encrypted = plain_text.translate(table)
        return '/V1_CRYPTO ' + encrypted

    def decrypt(self):
        shift = self.key
        key_range = 10
        plain_text = self.text
        shift = key_range - shift
        shift %= key_range
        if '/V1_CRYPTO ' in plain_text:
            alphabet = string.ascii_lowercase
            shifted = alphabet[shift:] + alphabet[:shift]
            table = str.maketrans(alphabet, shifted)
            decrypted = plain_text.translate(table)
            decrypted = decrypted.replace('/V1_CRYPTO ', '')
            return decrypted
        else:
            return 'Padding error! /V1_CRYPTO not found in the text'

    def substitution_encrypt(self):
        key = list(KeyVariable.key_var_all)
        random.shuffle(key)
        table = str.maketrans(string.ascii_letters + string.digits + string.punctuation, ''.join(key))
        encrypted = self.text.translate(table)
        return '/SUBSTITUTION_CRYPTO ' + encrypted

    def substitution_decrypt(self):
        key = list(KeyVariable.key_var_all)
        random.shuffle(key)
        table = str.maketrans(''.join(key), string.ascii_letters + string.digits + string.punctuation)
        decrypted = self.text.translate(table)
        decrypted = decrypted.replace('/SUBSTITUTION_CRYPTO ', '')
        return decrypted


class KeyGenerator:
    @staticmethod
    def key_generator_num_v1(min_val, max_val):
        key = random.randint(min_val, max_val)
        return key + 8

    @staticmethod
    def key_generator_num_v1_1(string_lowercase, key):
        out = int(string_lowercase, base=key)
        return out

    @staticmethod
    def key_generator_num_v2(size, chars=string.ascii_letters + string.digits + '@#£_.&-+()/*:;!? \n\n~`|•√π÷×¶∆€¥$¢^°={}"%()©®™+✓[]<>'):
        return ''.join(random.choice(chars) for _ in range(size))


class CryptoV2:
    def __init__(self, string, key):
        self.string = string
        self.key = key

    def encrypt(self):
        keys = self.key
        value = keys[-1] + keys[:-1]
        encrypt = dict(zip(keys, value))
        string = self.string
        encrypt_new = ''.join([encrypt[letter] for letter in string.lower()])
        return '/V2_CRYPTO ' + encrypt_new

    def decrypt(self):
        keys = self.key
        string = self.string
        if '/V2_CRYPTO ' in string:
            value = keys[-1] + keys[:-1]
            decrypt = dict(zip(value, keys))
            decrypt_new = ''.join([decrypt[letter] for letter in string.lower()])
            decrypt_new = decrypt_new.replace('/V2_CRYPTO ', '')
            return decrypt_new
        else:
            return 'Padding error! /V2_CRYPTO not found in the text'

    def caesar_variation_encrypt(self):
        shift = self.key
        plain_text = self.string
        encrypted = ''.join(chr((ord(char) + shift) % 256) for char in plain_text)
        return '/CAESAR_VARIATION_CRYPTO ' + encrypted

    def caesar_variation_decrypt(self):
        shift = self.key
        cipher_text = self.string
        decrypted = ''.join(chr((ord(char) - shift) % 256) for char in cipher_text)
        decrypted = decrypted.replace('/CAESAR_VARIATION_CRYPTO ', '')
        return decrypted


class CryptoV3Num:
    def __init__(self, number, key):
        self.number = number
        self.key = key

    def encrypt(self):
        shift = self.key
        plain_text = str(self.number)
        encrypted = ''.join(chr((ord(char) + shift) % 10 + ord('0')) for char in plain_text)
        return '/V3_NUM_CRYPTO ' + encrypted

    def decrypt(self):
        shift = self.key
        cipher_text = str(self.number)
        decrypted = ''.join(chr((ord(char) - shift) % 10 + ord('0')) for char in cipher_text)
        decrypted = decrypted.replace('/V3_NUM_CRYPTO ', '')
        return decrypted

    def rail_fence_encrypt(self):
        rails = self.key
        text = str(self.number)

        def encrypt(text, rails):
            rail_dict = {i: [] for i in range(rails)}
            rail = 0
            direction = 1

            for char in text:
                rail_dict[rail].append(char)
                rail += direction

                if rail == rails - 1 or rail == 0:
                    direction = -direction

            encrypted = ''
            for i in range(rails):
                encrypted += ''.join(rail_dict[i])
            return encrypted

        encrypted = encrypt(text, rails)
        return '/RAIL_FENCE_CRYPTO ' + encrypted

    def rail_fence_decrypt(self):
        rails = self.key
        text = self.number

        def decrypt(text, rails):
            rail_dict = {i: [] for i in range(rails)}
            rail = 0
            direction = 1

            for i in range(len(text)):
                rail_dict[rail].append(None)
                rail += direction

                if rail == rails - 1 or rail == 0:
                    direction = -direction

            index = 0
            for i in range(rails):
                for j in range(len(rail_dict[i])):
                    rail_dict[i][j] = text[index]
                    index += 1

            rail = 0
            direction = 1
            decrypted = ''
            for i in range(len(text)):
                decrypted += rail_dict[rail].pop(0)
                rail += direction

                if rail == rails - 1 or rail == 0:
                    direction = -direction

            return decrypted

        text = text.replace('/RAIL_FENCE_CRYPTO ', '')
        decrypted = decrypt(text, rails)
        return decrypted


class KeyVariable:
    key_var_all = string.ascii_letters + string.digits + '@#£_.&-+()/*:;!? \n\n~`|•√π÷×¶∆€¥$¢^°={}"%()©®™+✓[]<>'
    key_var_alp_number = string.ascii_letters + string.digits
    key_var_number = string.digits
    key_var_sim = '@#£_"&-+()/*:;!?~`|•√π÷×¶∆€¥$¢^°={}"%©®™✓[]<>' + " '"
    key_var_more = 'àáâäæãåāqwêéèëērtyūüúûùìīïíîõōøœòöôópßdfghjklzxçvbñmqwertyuioplkjhgfdsazxcvbnm1234567890රු'

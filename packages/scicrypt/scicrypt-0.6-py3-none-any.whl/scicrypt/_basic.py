
from  __future__  import annotations
import base64
import random
import numpy as np

__all__ = ['reverse', 'a1z26', 'affine', 'atbash',  'baconian', 'base16', 'base32', 'base64_crypto',  'base85', 'beaufort',
           'bifid', 'onepad', 'morse', 'polybius', 'porta', 'trifid', 'transpose',  'vigenere', 'xor']
def gcd(a: int, b: int) -> int:
    while a != 0:
        a, b = b % a, a
    return b


def find_mod_inverse(a: int, m: int) -> int:
    if gcd(a, m) != 1:
        raise ValueError(f"mod inverse of {a!r} and {m!r} does not exist")
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m



def reverse(message):
    """
    This is program to explain reverse cipher.
    >>> import crypto as crypt
    >>> crypt.reverse("reverse")
        'esrever'
    >>> crypt.reverse('esrever')
        'reverse'
        
    """
    translated = ''
    i = len(message) -1
    
    while i>=0:
        translated = translated +message[i]
        i = i-1
    return translated
    
    



"""
Convert a string of characters to a sequence of numbers
corresponding to the character's position in the alphabet.

https://www.dcode.fr/letter-number-cipher
http://bestcodes.weebly.com/a1z26.html
"""

class a1z26:
    
    def encode(self, plain: str) -> list[int]:
        """
        >>> x = crypt.a1z26.encode("a1z26")
        >>> crypt.a1z26.decode(x)
            'a1z26'
        >>> encode("crypto")
            [3, 18, 25, 16, 20, 15]
        
    
        """
        return [ord(elem) - 96 for elem in plain]


    def decode(self, encoded: list[int]) -> str:
        """
        >>> decode([3, 18, 25, 16, 20, 15])
            'crypto'
        """
        return "".join(chr(elem + 96) for elem in encoded)


a1z26 = a1z26()

# https://scanftree.com/
class Affine(object):
    DIE =  128
    KEY = (7, 3, 55)
    
    def __init__(self):
        pass
    
    def encryptChar(self, char):
        K1, K2, kI = self.KEY
        return chr((K1 * ord(char) + K2) % self.DIE)
    
    def encrypt(self, string):
        return "".join(map(self.encryptChar, string))
    
    def decryptChar(self, char):
        K1, K2, KI = self.KEY
        return chr(KI * (ord(char) - K2) % self.DIE)
    
    def decrypt(self, string):
        return "".join(map(self.decryptChar, string))
    
affine = Affine()



""" https://en.wikipedia.org/wiki/Atbash """
def atbash(self, sequence: str) -> str:
        """
        >>> atbash("crypto")
            'xibkgl'
        """
        output = ""
        for i in sequence:
            extract = ord(i)
            if 65 <= extract <= 90:
                output += chr(155 - extract)
            elif 97 <= extract <= 122:
                output += chr(219 - extract)
            else:
                output += i
        return output
    
    


"""
Program to encode and decode Baconian or Bacon's Cipher
Wikipedia reference : https://en.wikipedia.org/wiki/Bacon%27s_cipher
"""
encode_dict = {
    "a": "AAAAA",
    "b": "AAAAB",
    "c": "AAABA",
    "d": "AAABB",
    "e": "AABAA",
    "f": "AABAB",
    "g": "AABBA",
    "h": "AABBB",
    "i": "ABAAA",
    "j": "BBBAA",
    "k": "ABAAB",
    "l": "ABABA",
    "m": "ABABB",
    "n": "ABBAA",
    "o": "ABBAB",
    "p": "ABBBA",
    "q": "ABBBB",
    "r": "BAAAA",
    "s": "BAAAB",
    "t": "BAABA",
    "u": "BAABB",
    "v": "BBBAB",
    "w": "BABAA",
    "x": "BABAB",
    "y": "BABBA",
    "z": "BABBB",
    " ": " ",
}


decode_dict = {value: key for key, value in encode_dict.items()}


class baconian:
    
    def encode(self, word: str) -> str:
        """
        Encodes to Baconian cipher

        >>> encode("crypto")
            'AAABABAAAABABBAABBBABAABAABBAB'
        
        >>> encode("hello world!")
        Traceback (most recent call last):
        ...
        Exception: encode() accepts only letters of the alphabet and spaces
        """
        encoded = ""
        for letter in word.lower():
            if letter.isalpha() or letter == " ":
                encoded += encode_dict[letter]
            else:
                raise Exception("encode() accepts only letters of the alphabet and spaces")
        return encoded
    
    

    def decode(self, coded: str) -> str:
        """
        Decodes from Baconian cipher

        >>> decode('AAABABAAAABABBAABBBABAABAABBAB')
            'crypto'
       
        >>> decode("AABBBAABAAABABAABABAABBAB BABAAABBABBAAAAABABAAAABB!")
        Traceback (most recent call last):
        ...
        Exception: decode() accepts only 'A', 'B' and spaces
        """
        if set(coded) - {"A", "B", " "} != set():
            raise Exception("decode() accepts only 'A', 'B' and spaces")
        decoded = ""
        for word in coded.split():
            while len(word) != 0:
                decoded += decode_dict[word[:5]]
                word = word[5:]
            decoded += " "
        return decoded.strip()
    
baconian = baconian()




class base16:
    def encode(self, inp: str) -> bytes:
        """
        Encodes a given utf-8 string into base-16.

        >>> base16_encode('Hello World!')
        b'48656C6C6F20576F726C6421'
        >>> base16_encode('HELLO WORLD!')
        b'48454C4C4F20574F524C4421'
        >>> base16_encode('')
        b''
        """
        # encode the input into a bytes-like object and then encode b16encode that
        return base64.b16encode(inp.encode("utf-8"))
    
    
    def decode(self, b16encoded: bytes) -> str:
        """
        Decodes from base-16 to a utf-8 string.

        >>> base16_decode(b'48656C6C6F20576F726C6421')
        'Hello World!'
        >>> base16_decode(b'48454C4C4F20574F524C4421')
        'HELLO WORLD!'
        >>> base16_decode(b'')
        ''
        """
        # b16decode the input into bytes and decode that into a human readable string
        return base64.b16decode(b16encoded).decode("utf-8")
    
base16 = base16()
    
    


class base32:
    def encode(self, string: str) -> bytes:
        """
        Encodes a given string to base32, returning a bytes-like object
        >>> base32_encode("Hello World!")
        b'JBSWY3DPEBLW64TMMQQQ===='
        >>> base32_encode("123456")
        b'GEZDGNBVGY======'
        >>> base32_encode("some long complex string")
        b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY='
        """

        # encoded the input (we need a bytes like object)
        # then, b32encoded the bytes-like object
        return base64.b32encode(string.encode("utf-8"))

    def decode(self, encoded_bytes: bytes) -> str:
        """
        Decodes a given bytes-like object to a string, returning a string
        >>> base32_decode(b'JBSWY3DPEBLW64TMMQQQ====')
        'Hello World!'
        >>> base32_decode(b'GEZDGNBVGY======')
        '123456'
        >>> base32_decode(b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY=')
        'some long complex string'
        """

        # decode the bytes from base32
        # then, decode the bytes-like object to return as a string
        return base64.b32decode(encoded_bytes).decode("utf-8")


base32 = base32()



class Base64Cryptography:
    @staticmethod
    def encode(data):
        """
        Encode the input data using Base64 encoding.

        Args:
            data (bytes or str): The data to be encoded.

        Returns:
            str: The Base64-encoded data as a string.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        encoded_data = base64.b64encode(data).decode('utf-8')
        return encoded_data

    @staticmethod
    def decode(encoded_data):
        """
        Decode Base64-encoded data.

        Args:
            encoded_data (str): The Base64-encoded data as a string.

        Returns:
            bytes: The decoded data as bytes.
        """
        decoded_data = base64.b64decode(encoded_data.encode('utf-8'))
        return decoded_data
    
    
    
base64_crypto = Base64Cryptography()


class base85:
    def encode(self, string: str) -> bytes:
        """
        >>> base85_encode("")
        b''
        >>> base85_encode("12345")
        b'0etOA2#'
        >>> base85_encode("base 85")
        b'@UX=h+?24'
        """
        # encoded the input to a bytes-like object and then a85encode that
        return base64.a85encode(string.encode("utf-8"))

    def decode(self, a85encoded: bytes) -> str:
        """
        >>> base85_decode(b"")
        ''
        >>> base85_decode(b"0etOA2#")
        '12345'
        >>> base85_decode(b"@UX=h+?24")
        'base 85'
        """
        # a85decode the input into bytes and decode that into a human readable string
        return base64.a85decode(a85encoded).decode("utf-8")
    
    
base85 = base85()




class BeaufortCipher:
    def __init__(self):
        pass

    def encrypt(self, plaintext, keyword):
        plaintext = plaintext.upper()
        keyword = keyword.upper()
        encrypted_text = ""

        for i in range(len(plaintext)):
            if plaintext[i].isalpha():
                key_char = keyword[i % len(keyword)]
                shift = ord(key_char) - ord('A')
                encrypted_char = chr(((ord(plaintext[i]) - ord('A') + shift) % 26) + ord('A'))
                encrypted_text += encrypted_char
            else:
                encrypted_text += plaintext[i]

        return encrypted_text

    def decrypt(self, ciphertext, keyword):
        ciphertext = ciphertext.upper()
        keyword = keyword.upper()
        decrypted_text = ""

        for i in range(len(ciphertext)):
            if ciphertext[i].isalpha():
                key_char = keyword[i % len(keyword)]
                shift = ord(key_char) - ord('A')
                decrypted_char = chr(((ord(ciphertext[i]) - ord('A') - shift) % 26) + ord('A'))
                decrypted_text += decrypted_char
            else:
                decrypted_text += ciphertext[i]

        return decrypted_text

    
beaufort = BeaufortCipher()




class BifidCipher:
    """
    The Bifid Cipher uses a Polybius Square to encipher a message in a way that
    makes it fairly difficult to decipher without knowing the secret.
    
    https://www.braingle.com/brainteasers/codes/bifid.php
    """
    def __init__(self) -> None:
        SQUARE = [
            ["a", "b", "c", "d", "e"],
            ["f", "g", "h", "i", "k"],
            ["l", "m", "n", "o", "p"],
            ["q", "r", "s", "t", "u"],
            ["v", "w", "x", "y", "z"],
        ]
        self.SQUARE = np.array(SQUARE)
        
    def letter_to_numbers(self, letter: str) -> np.ndarray:
        """
        Return the pair of numbers that represents the given letter in the
        polybius square
        >>> np.array_equal(BifidCipher().letter_to_numbers('a'), [1,1])
        True
        >>> np.array_equal(BifidCipher().letter_to_numbers('u'), [4,5])
        True
        """
        index1, index2 = np.where(self.SQUARE == letter)
        indexes = np.concatenate([index1 + 1, index2 + 1])
        return indexes

    def numbers_to_letter(self, index1: int, index2: int) -> str:
        """
        Return the letter corresponding to the position [index1, index2] in
        the polybius square
        >>> BifidCipher().numbers_to_letter(4, 5) == "u"
        True
        >>> BifidCipher().numbers_to_letter(1, 1) == "a"
        True
        """
        letter = self.SQUARE[index1 - 1, index2 - 1]
        return letter
    
    
    def encode(self, message: str) -> str:
        """
        Return the encoded version of message according to the polybius cipher
        >>> BifidCipher().encode('testmessage') == 'qtltbdxrxlk'
        True
        >>> BifidCipher().encode('Test Message') == 'qtltbdxrxlk'
        True
        >>> BifidCipher().encode('test j') == BifidCipher().encode('test i')
        True
        """
        message = message.lower()
        message = message.replace(" ", "")
        message = message.replace("j", "i")
        first_step = np.empty((2, len(message)))
        for letter_index in range(len(message)):
            numbers = self.letter_to_numbers(message[letter_index])
            first_step[0, letter_index] = numbers[0]
            first_step[1, letter_index] = numbers[1]
        second_step = first_step.reshape(2 * len(message))
        encoded_message = ""
        for numbers_index in range(len(message)):
            index1 = int(second_step[numbers_index * 2])
            index2 = int(second_step[(numbers_index * 2) + 1])
            letter = self.numbers_to_letter(index1, index2)
            encoded_message = encoded_message + letter
        return encoded_message
    
    def decode(self, message: str) -> str:
        """
        Return the decoded version of message according to the polybius cipher
        >>> BifidCipher().decode('qtltbdxrxlk') == 'testmessage'
        True
        """
        message = message.lower()
        message.replace(" ", "")
        first_step = np.empty(2 * len(message))
        for letter_index in range(len(message)):
            numbers = self.letter_to_numbers(message[letter_index])
            first_step[letter_index * 2] = numbers[0]
            first_step[letter_index * 2 + 1] = numbers[1]
        second_step = first_step.reshape((2, len(message)))
        decoded_message = ""
        for numbers_index in range(len(message)):
            index1 = int(second_step[0, numbers_index])
            index2 = int(second_step[1, numbers_index])
            letter = self.numbers_to_letter(index1, index2)
            decoded_message = decoded_message + letter
        return decoded_message
    
    
bifid = BifidCipher()




class MorseCodeConverter:
    def __init__(self):
        self.morse_code_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
            '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
            ' ': ' '
        }

    def encrypt(self, text):
        text = text.upper()
        morse_code = []
        for char in text:
            if char in self.morse_code_dict:
                morse_code.append(self.morse_code_dict[char])
            else:
                morse_code.append(char)
        return ' '.join(morse_code)

    def decrypt(self, morse_code):
        morse_code = morse_code.split(' ')
        text = []
        for symbol in morse_code:
            if symbol in self.morse_code_dict.values():
                text.append([key for key, value in self.morse_code_dict.items() if value == symbol][0])
            else:
                text.append(symbol)
        return ''.join(text).lower()

morse  = MorseCodeConverter()





class Onepad:
    def encrypt(self, text: str) -> tuple[list[int], list[int]]:
        """Function to encrypt text using pseudo-random numbers"""
        plain = [ord(i) for i in text]
        key = []
        cipher = []
        for i in plain:
            k = random.randint(1, 300)
            c = (i + k) * k
            cipher.append(c)
            key.append(k)
        return cipher, key

   
    def decrypt(self, cipher: list[int], key: list[int]) -> str:
        """Function to decrypt text using pseudo-random numbers."""
        plain = []
        for i in range(len(key)):
            p = int((cipher[i] - (key[i]) ** 2) / key[i])
            plain.append(chr(p))
        return "".join([i for i in plain])

onepad = Onepad()


class PolybiusCipher:
    def __init__(self) -> None:
        SQUARE = [
            ["a", "b", "c", "d", "e"],
            ["f", "g", "h", "i", "k"],
            ["l", "m", "n", "o", "p"],
            ["q", "r", "s", "t", "u"],
            ["v", "w", "x", "y", "z"],
        ]
        self.SQUARE = np.array(SQUARE)

    def letter_to_numbers(self, letter: str) -> np.ndarray:
        """
        Return the pair of numbers that represents the given letter in the
        polybius square
        >>> np.array_equal(PolybiusCipher().letter_to_numbers('a'), [1,1])
        True

        >>> np.array_equal(PolybiusCipher().letter_to_numbers('u'), [4,5])
        True
        """
        index1, index2 = np.where(self.SQUARE == letter)
        indexes = np.concatenate([index1 + 1, index2 + 1])
        return indexes

    def numbers_to_letter(self, index1: int, index2: int) -> str:
        """
        Return the letter corresponding to the position [index1, index2] in
        the polybius square

        >>> PolybiusCipher().numbers_to_letter(4, 5) == "u"
        True

        >>> PolybiusCipher().numbers_to_letter(1, 1) == "a"
        True
        """
        return self.SQUARE[index1 - 1, index2 - 1]

    def encode(self, message: str) -> str:
        """
        Return the encoded version of message according to the polybius cipher

        >>> PolybiusCipher().encode("test message") == "44154344 32154343112215"
        True

        >>> PolybiusCipher().encode("Test Message") == "44154344 32154343112215"
        True
        """
        message = message.lower()
        message = message.replace("j", "i")

        encoded_message = ""
        for letter_index in range(len(message)):
            if message[letter_index] != " ":
                numbers = self.letter_to_numbers(message[letter_index])
                encoded_message = encoded_message + str(numbers[0]) + str(numbers[1])
            elif message[letter_index] == " ":
                encoded_message = encoded_message + " "

        return encoded_message

    def decode(self, message: str) -> str:
        """
        Return the decoded version of message according to the polybius cipher

        >>> PolybiusCipher().decode("44154344 32154343112215") == "test message"
        True

        >>> PolybiusCipher().decode("4415434432154343112215") == "testmessage"
        True
        """
        message = message.replace(" ", "  ")
        decoded_message = ""
        for numbers_index in range(int(len(message) / 2)):
            if message[numbers_index * 2] != " ":
                index1 = message[numbers_index * 2]
                index2 = message[numbers_index * 2 + 1]

                letter = self.numbers_to_letter(int(index1), int(index2))
                decoded_message = decoded_message + letter
            elif message[numbers_index * 2] == " ":
                decoded_message = decoded_message + " "

        return decoded_message

polybius =   PolybiusCipher()








class PortaCipher:
    """ 
    # Usage example
    keyword = "KEYWORD"
    text = "HELLO WORLD"

    cipher = PortaCipher()
    encrypted_text = cipher.encrypt(text, keyword)
    print(f'Encrypted: {encrypted_text}')

    decrypted_text = cipher.decrypt(encrypted_text, keyword)
    print(f'Decrypted: {decrypted_text}')

    
    """
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    def generate_key_square(self, keyword):
        keyword = keyword.upper()
        key_square = []

        for char in keyword:
            if char not in key_square:
                key_square.append(char)

        for char in self.alphabet:
            if char not in key_square:
                key_square.append(char)

        return ''.join(key_square)

    def encrypt(self, plaintext, keyword):
        plaintext = plaintext.upper()
        key_square = self.generate_key_square(keyword)
        ciphertext = []

        for char in plaintext:
            if char in self.alphabet:
                index = self.alphabet.index(char)
                key_char = key_square[index]
                ciphertext.append(key_char)
            else:
                ciphertext.append(char)

        return ''.join(ciphertext)

    def decrypt(self, ciphertext, keyword):
        ciphertext = ciphertext.upper()
        key_square = self.generate_key_square(keyword)
        plaintext = []

        for char in ciphertext:
            if char in self.alphabet:
                index = key_square.index(char)
                plain_char = self.alphabet[index]
                plaintext.append(plain_char)
            else:
                plaintext.append(char)

        return ''.join(plaintext)


porta = PortaCipher()




class TrifidCipher:
    """
    # https://en.wikipedia.org/wiki/Trifid_cipher
    """
    def _generate_trifid_grid(self, key):
        key = key.upper()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        key_set = set(key)
        remaining_chars = [char for char in alphabet if char not in key_set]
        key += "".join(remaining_chars)
        key = key.replace("J", "I")  # Remove J (or replace with I)
        trifid_grid = [[0] * 3 for _ in range(3)]

        k = 0
        for i in range(3):
            for j in range(3):
                trifid_grid[i][j] = key[k]
                k += 1

        return trifid_grid

    def encrypt(self, plaintext, key):
        plaintext = plaintext.upper()
        key = key.upper()
        trifid_grid = self._generate_trifid_grid(key)
        encoded_text = ""

        for char in plaintext:
            if char == " ":
                encoded_text += " "
            else:
                for i in range(3):
                    for j in range(3):
                        if trifid_grid[i][j] == char:
                            encoded_text += str(i + 1) + str(j + 1)

        return encoded_text

    def decrypt(self, ciphertext, key):
        ciphertext = ciphertext.replace(" ", "")
        key = key.upper()
        trifid_grid = self._generate_trifid_grid(key)
        decoded_text = ""

        for i in range(0, len(ciphertext), 2):
            row = int(ciphertext[i]) - 1
            col = int(ciphertext[i + 1]) - 1
            decoded_text += trifid_grid[row][col]

        return decoded_text


trifid = TrifidCipher()




class TranspositionCipher:
    def _pad_message(self, message, key):
        message_len = len(message)
        padding = (key - (message_len % key)) % key
        return message + 'X' * padding

    def encrypt(self, plaintext, key):
        plaintext = plaintext.upper().replace(' ', '')
        plaintext = self._pad_message(plaintext, key)
        num_cols = key
        num_rows = len(plaintext) // num_cols
        matrix = [['' for _ in range(num_cols)] for _ in range(num_rows)]

        index = 0
        for row in range(num_rows):
            for col in range(num_cols):
                matrix[row][col] = plaintext[index]
                index += 1

        ciphertext = ''
        for col in range(num_cols):
            for row in range(num_rows):
                ciphertext += matrix[row][col]

        return ciphertext

    def decrypt(self, ciphertext, key):
        num_cols = key
        num_rows = len(ciphertext) // num_cols
        matrix = [['' for _ in range(num_cols)] for _ in range(num_rows)]

        index = 0
        for col in range(num_cols):
            for row in range(num_rows):
                matrix[row][col] = ciphertext[index]
                index += 1

        plaintext = ''
        for row in range(num_rows):
            for col in range(num_cols):
                plaintext += matrix[row][col]

        return plaintext


transpose = TranspositionCipher()



class VigenereCipher:
    def _extend_key(self, text, key):
        extended_key = key
        while len(extended_key) < len(text):
            extended_key += key
        return extended_key[:len(text)]

    def encrypt(self, plaintext, key):
        plaintext = plaintext.upper()
        key = key.upper()
        extended_key = self._extend_key(plaintext, key)
        ciphertext = ""

        for i in range(len(plaintext)):
            if plaintext[i].isalpha():
                shift = ord(extended_key[i]) - ord('A')
                encrypted_char = chr(((ord(plaintext[i]) - ord('A') + shift) % 26) + ord('A'))
                ciphertext += encrypted_char
            else:
                ciphertext += plaintext[i]

        return ciphertext

    def decrypt(self, ciphertext, key):
        ciphertext = ciphertext.upper()
        key = key.upper()
        extended_key = self._extend_key(ciphertext, key)
        plaintext = ""

        for i in range(len(ciphertext)):
            if ciphertext[i].isalpha():
                shift = ord(extended_key[i]) - ord('A')
                decrypted_char = chr(((ord(ciphertext[i]) - ord('A') - shift) % 26) + ord('A'))
                plaintext += decrypted_char
            else:
                plaintext += ciphertext[i]

        return plaintext

vigenere = VigenereCipher()




class XORCipher:
    """ 

        author: 
        date:
        class: XORCipher

        This class implements the XOR-cipher algorithm and provides
        some useful methods for encrypting and decrypting strings and
        files.

        Overview about methods

        - encrypt : list of char
        - decrypt : list of char
        - encrypt_string : str
        - decrypt_string : str
        - encrypt_file : boolean
        - decrypt_file : boolean
   
    
    
    """
    def __init__(self, key: int = 0):
        """
        simple constructor that receives a key or uses
        default key = 0
        """

        # private field
        self.__key = key

    def encrypt(self, content: str, key: int) -> list[str]:
        """
        input: 'content' of type string and 'key' of type int
        output: encrypted string 'content' as a list of chars
        if key not passed the method uses the key by the constructor.
        otherwise key = 1
        """

        # precondition
        assert isinstance(key, int) and isinstance(content, str)

        key = key or self.__key or 1

        # make sure key is an appropriate size
        key %= 255

        return [chr(ord(ch) ^ key) for ch in content]

    def decrypt(self, content: str, key: int) -> list[str]:
        """
        input: 'content' of type list and 'key' of type int
        output: decrypted string 'content' as a list of chars
        if key not passed the method uses the key by the constructor.
        otherwise key = 1
        """

        # precondition
        assert isinstance(key, int) and isinstance(content, list)

        key = key or self.__key or 1

        # make sure key is an appropriate size
        key %= 255

        return [chr(ord(ch) ^ key) for ch in content]

    def encrypt_string(self, content: str, key: int = 0) -> str:
        """
        input: 'content' of type string and 'key' of type int
        output: encrypted string 'content'
        if key not passed the method uses the key by the constructor.
        otherwise key = 1
        """

        # precondition
        assert isinstance(key, int) and isinstance(content, str)

        key = key or self.__key or 1

        # make sure key can be any size
        while key > 255:
            key -= 255

        # This will be returned
        ans = ""

        for ch in content:
            ans += chr(ord(ch) ^ key)

        return ans

    def decrypt_string(self, content: str, key: int = 0) -> str:
        """
        input: 'content' of type string and 'key' of type int
        output: decrypted string 'content'
        if key not passed the method uses the key by the constructor.
        otherwise key = 1
        """

        # precondition
        assert isinstance(key, int) and isinstance(content, str)

        key = key or self.__key or 1

        # make sure key can be any size
        while key > 255:
            key -= 255

        # This will be returned
        ans = ""

        for ch in content:
            ans += chr(ord(ch) ^ key)

        return ans

    def encrypt_file(self, file: str, key: int = 0) -> bool:
        """
        input: filename (str) and a key (int)
        output: returns true if encrypt process was
        successful otherwise false
        if key not passed the method uses the key by the constructor.
        otherwise key = 1
        """

        # precondition
        assert isinstance(file, str) and isinstance(key, int)

        try:
            with open(file) as fin:
                with open("encrypt.out", "w+") as fout:

                    # actual encrypt-process
                    for line in fin:
                        fout.write(self.encrypt_string(line, key))

        except OSError:
            return False

        return True

    def decrypt_file(self, file: str, key: int) -> bool:
        """
        input: filename (str) and a key (int)
        output: returns true if decrypt process was
        successful otherwise false
        if key not passed the method uses the key by the constructor.
        otherwise key = 1
        """

        # precondition
        assert isinstance(file, str) and isinstance(key, int)

        try:
            with open(file) as fin:
                with open("decrypt.out", "w+") as fout:

                    # actual encrypt-process
                    for line in fin:
                        fout.write(self.decrypt_string(line, key))

        except OSError:
            return False

        return True


xor= XORCipher()
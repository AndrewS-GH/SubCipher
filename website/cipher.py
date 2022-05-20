"""
Cipher class housing the methods that interact with the ciphertext and plaintext
"""

import re
from operator import itemgetter
from collections import Counter, defaultdict
from typing import Union
from .cipher_key import CipherKey


class Cipher:
    ENG_FREQ = "etaoinsrhdlucmfywgpbvkxqjz"
    max_common_strings = 25

    def __init__(self, cipher_text: str) -> None:
        """
        init
        """
        self._original = cipher_text.lower()  # never gets modified
        self._mod = cipher_text.lower()
        self._cipher_key = CipherKey(cipher_text)

    def update_text(self) -> None:
        """
        Updates the cipher text based on the key
        itereates over original
        """
        print(self._mod)
        self._mod = ""
        for char in self._original:
            temp = self._cipher_key.get(char, char)
            if temp != '_' or char == "_":
                self._mod += temp
        print(self._mod)

    def get_cipher(self) -> str:
        """
        returns the updated cipher text
        """
        return self._mod

    def get_original(self) -> str:
        """
        returns the original cipher text gotten from the user
        """
        return self._original

    def get_key(self, *, as_str: bool = False) -> Union[str, dict]:
        """
        returns the original cipher text gotten from the user
        """
        if as_str is True:
            return "\n".join([f"{key} {val}" for key, val in self._cipher_key.items()]) + "\n"

        return self._cipher_key

    def modify_key_from_dict(self, key: dict) -> None:
        """
        modifies the cipher_key from a dictionary
        """
        self._cipher_key = CipherKey(self._original, key)
        self.update_text()

    def modify_key_by_element(self, key: str, value: str) -> None:
        """
        modifies single element in the cipher key
        """
        self._cipher_key[key] = value

    def swap_by_frequency(self) -> None:
        """
        Updates the key and cipher based on english letter freuquency
        """
        temp_cipher_key = {char: self.ENG_FREQ[i] for i, char in enumerate(self._cipher_key)}
        self._cipher_key = CipherKey(self._original, temp_cipher_key)
        self.update_text()

    def get_common_substrings(self, size: int) -> dict:
        """
        Prints the top x substrings of size `size`
        """
        if size <= 0:
            raise AttributeError("size must be greater than 0")

        substrings = defaultdict(int)
        l, r = 0, size  # left and right pointers

        cleaned_text = self.clean_text(self._original)
        while r <= len(cleaned_text):
            substring = cleaned_text[l:r]
            if " " not in substring:  # only add substrings without whitespace
                substrings[substring] += 1

            # increment pointers
            l += 1
            r += 1

        # return top `max_common_strings` as a dict
        return dict(sorted(substrings.items(), key=itemgetter(1), reverse=True)[:self.max_common_strings])

    def get_common_words(self, length: int) -> dict:
        """
        Prints the top x words of length `length`
        """
        if length <= 0:
            raise AttributeError("length must be greater than 0")

        cleaned_text = self.clean_text(self._original)
        counter = Counter(cleaned_text.split(" "))
        return {k: v for k, v in counter.most_common() if len(k) == length}

    def get_duplicate_substrings(self) -> dict:
        """
        Prints out all two letter duplicate substrings
        """
        substrings = defaultdict(int)
        cleaned_text = self.clean_text(self._original)

        for index, char in enumerate(cleaned_text[:-1]):  # ignore last character
            if char == cleaned_text[index + 1] and char != " ":
                substrings[char * 2] += 1

        return dict(sorted(substrings.items(), key=itemgetter(1), reverse=True)[:self.max_common_strings])

        """
        Resets the key and sets the modified cipher back to the original
        """
        self._cipher_key = CipherKey(self.original)
        self.mod = self.original

    def reset(self) -> None:
        """
        resets _cipher_key
        """
        self._cipher_key.reset()
        self.update_text()

    @staticmethod
    def clean_text(text: str) -> str:
        return re.sub(r"[^a-zA-Z0-9 ]", '', text)


if __name__ == "__main__":

    a = Cipher("a wfkaw fa wo kfpoo aw awld fa jakKwdkawk djlawkdjlkawjdkklja lwdjkljsklajwkdljalkwjdlkasldkjawf")
    print(a.get_duplicate_substrings())

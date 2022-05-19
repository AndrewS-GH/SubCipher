"""
Cipher class housing the methods that interact with the ciphertext and plaintext
"""

import re
from operator import itemgetter
from collections import Counter, defaultdict
from typing import Union
from cipher_key import CipherKey


class Cipher:
    ENG_FREQ = "etaoinsrhdlucmfywgpbvkxqjz"
    max_common_strings = 25
    
    def __init__(self, cipher: str) -> None:
        """
        init
        """
        self._original = cipher.lower()  # never gets modified
        self._mod = cipher.lower()
        self._cipher_key = CipherKey(cipher)


    def update_text(self) -> None:
        """
        Updates the cipher text based on the key
        itereates over original
        """
        self._mod = ""
        for char in self._original:
            temp = key[char]
            if temp != '_':
                self_.mod += temp

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
        self._cipher_key = CipherKey(key)
        self.update_text()
    
    def modify_key_from_element(self, key: str, value: str) -> None:
        """
        modifies single element in the cipher key
        """
        self._cipher_key[key] = value


    def swap_by_frequency(self) -> None:
        """
        Updates the key and cipher based on english letter freuquency
        """
        for index, key in enumerate(self.key):
            self.cipher_key[key] = ENG_FREQ[index]
        self.update_text()

    def get_common_substrings(self, size: int) -> dict:
        """
        Prints the top x substrings of size `size`
        """
        assert size > 0, "size must be greater than 0"

        substrings = defaultdict(int)
        l, r = 0, size  # left and right pointers

        cleaned_text = re.sub(r"[^a-zA-Z0-9 ]", '', self._original)
        while r <= len(cleaned_text):
            substring = cleaned_text[l:r]
            if " " not in substring:  # only add substrings without whitespace
                substrings[substring] += 1

            # increment pointers
            l += 1
            r += 1

        # return top `max_common_strings` as a dict
        return dict(sorted(substrings.items(), key=itemgetter(1), reverse=True)[:self.max_common_strings])


    def get_common_words(self, size: int) -> dict:
        """
        Prints the top x words of size `size`
        """
        counter = Counter()


        dictSS = {}
        copyCipher = re.sub(r"[^a-zA-Z0-9 ]", '', self.original)
        copyCipher = copyCipher.split()
        defVals = 25
        for word in copyCipher:
            if len(word) == numWord:
                if word in dictSS.keys():
                    dictSS[word] += 1
                else:
                    dictSS[word] = 1
        if len(dictSS) < defVals:
            defVals = len(dictSS)
        res = dict(sorted(dictSS.items(), key=itemgetter(1),
                        reverse=True)[:defVals])
        return res
        # end getCommWords


        # -----------\
        # getDupSS()  \
        # -----------------------------------------------------------
    def getDupSS(self) -> dict:
        """
        Prints out all two letter duplicate substrings
        """
        dictSS = {}
        cleaned_cipher_text = re.sub(r"[^a-zA-Z0-9 ]", '', self.original)
        defVals = 25
        while copyCipher:
            vals = copyCipher[0:2]
            if len(vals) == 2:
                if vals[0] == vals[1]:
                    if vals in dictSS.keys():
                        dictSS[vals] += 1
                    else:
                        dictSS[vals] = 1
            copyCipher = copyCipher[1:]
        if len(dictSS) < defVals:
            defVals = len(dictSS)
        if "  " in dictSS:
            dictSS.pop("  ")
        res = dict(sorted(dictSS.items(), key=itemgetter(1),
                          reverse=True)[:defVals])
        return res
    # end getDupSS

    # --------\
    # reset()  \
    # -----------------------------------------------------------
    def reset(self) -> None:
        """
        Resets the key and sets the modified cipher back to the original
        """
        self.key = {}
        self.generateKey()
        self.mod = self.original
    # end rest          


if __name__ == "__main__":

    a = Cipher("awfkaw fawokfpoawawldjakwdkawk djlawkdjlkawjdklja lwdjkljsklajwkdljalkwjdlkasldkjawf")
    print(a.get_common_substrings(2))
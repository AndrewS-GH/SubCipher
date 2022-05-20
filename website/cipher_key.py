"""
CipherKey class

Extends dictionary to generate items from the cipher text, and guards __setitem__ data

"""
from collections import Counter
from typing import Optional


class CipherKey(dict):

    def __init__(self, cipher_text: str, optional_key: Optional[dict] = None):
        self._cipher_text = cipher_text  # original cipher text
        self._valid_chars = set([char for char in cipher_text.lower() if char.isalpha()])  # set of all characters in cipher text

        if optional_key:
            super().__init__(optional_key)

            if set(self.keys()) != self._valid_chars:  # verify the optional key is good
                raise AttributeError("Cipher key must have the same dictionary keys as unique chars in the cipher text")
        else:  # if no key submitted generate one from the cipher_text
            super().__init__(self.generate_default_key(cipher_text))

    def __setitem__(self, k, v):
        """
        k -> must be an alpha character in the cipher text
        v -> must be an alpha character or an `_`
        """

        if k not in self._valid_chars:
            raise AttributeError(f"{k} is not a valid character in the Cipher Text")

        if not isinstance(v, str):
            raise TypeError(f"Second argument must be of type str")

        if not len(v) == 1:
            raise AttributeError(f"Second argument must be a str of length 1")

        if not v.isalpha() and v != "_":
            raise AttributeError(f"Value must be alpha or `_`")

        super().__setitem__(k, v.lower())

    def reset(self, cipher_text=None):
        if cipher_text is None:
            cipher_text = self._cipher_text
        self.__init__(cipher_text=cipher_text)

    @staticmethod
    def generate_default_key(cipher_text: str):
        """
        Generates a key for the cipher text, elements are ordered based on
        their frequency
        """
        count = Counter([char for char in cipher_text if char.isalpha()])  # we only want to count alpha characters
        return {char: char for char, _ in count.most_common()}

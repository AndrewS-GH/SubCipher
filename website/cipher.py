"""
Cipher class housing the methods that interact with the ciphertext and plaintext
"""

import re
from operator import itemgetter

# ------ CONSTANTS ----------
ENG_FREQ = "etaoinsrhdlucmfywgpbvkxqjz"


class Cipher:
    """
    Cipher class
    """

    # -----------\
    # __init__()  \
    # -----------------------------------------------------------
    def __init__(self, cipher: str) -> None:
        """
        init
        """
        self.original = cipher
        self.mod = cipher
        self.key = {}
        self.generateKey()
    # end init

    # --------------\
    # generateKey()  \
    # -----------------------------------------------------------
    def generateKey(self) -> None:
        """
        Generates a key for the cipher text, elements are ordered based on
        their frequency
        """
        letterFreq = {}
        for char in self.original:
            if char.isalpha():  # filters out whitespace and any non characters
                if char in letterFreq:  # if the character already in dict
                    letterFreq[char] += 1
                else:  # if character not already in dict
                    letterFreq[char] = 1
        sortFreq = sorted(letterFreq.items(), key=lambda x: x[1],
                           reverse=True)
        for pair in sortFreq:
            self.key[pair[0]] = pair[0]
    # end generateKey

    # -------------\
    # updateText()  \
    # -----------------------------------------------------------
    def updateText(self) -> None:
        """
        Updates the cipher text based on the key
        """
        self.mod = ""
        tempOne = self.original
        tempTwo = ""

        for item in self.key.items():
            valOld = item[0]
            valNew = item[1]
            for char in tempOne:
                if char == valOld:
                    if valNew != "0":
                        tempTwo += valNew.upper()
                else:
                    tempTwo += char
            tempOne = tempTwo
            tempTwo = ""
        self.mod = tempOne.lower()
    # end updateText

    # ------------\
    # getCipher()  \
    # -----------------------------------------------------------
    def getCipher(self) -> str:
        """
        returns the updated cipher text
        """
        return self.mod
    # end getCipher

    # ----------\
    # getOrig()  \
    # -----------------------------------------------------------
    def getOrig(self) -> str:
        """
        returns the original cipher text gotten from the user
        """
        return self.original
    # end getOrig

    # ---------\
    # getKey()  \
    # -----------------------------------------------------------
    def getKey(self) -> str:
        """
        returns the original cipher text gotten from the user
        """
        strKey = ""
        for key in self.key:
            strKey += (key + " " + self.key[key] + "\n")
        return strKey
    # end getOrig

    # ------------\
    # modifyKey()  \
    # -----------------------------------------------------------
    def modifyKey(self, key) -> None:
        """
        Creates a guiObj object to let the user modify the key in a GUI
        """
        self.key = key
        self.updateText()
    # end modifyKey

    # ----------\
    # saveKey()  \
    # -----------------------------------------------------------
    def saveKey(self, filePath: str) -> None:
        """
        Writes the current key to a file
        """
        keyFile = open(filePath, "w")
        for item in self.key.items():
            keyFile.write(item[0] + " " + item[1] + "\n")
        keyFile.close()
    # end saveKey

    # ----------\
    # loadKey()  \
    # -----------------------------------------------------------
    def loadKey(self) -> None:
        """
        Opens a key file and updates the key and cipher
        """
        keyFileName = input("Enter the path for the key file: ")
        keyFile = open(keyFileFame, "r")
        for line in keyFile:
            vals = line.split()
            self.key[vals[0]] = vals[1]
        self.updateText()

    # -------------\
    # saveCipher()  \
    # -----------------------------------------------------------
    def saveCipher(self, filePath: str) -> None:
        """
        Writes the cipher to a file
        """
        cipherFile = open(filePath, "w")
        cipherFile.write(self.mod)
        cipherFile.close()
    # end saveCipher

    # -------------\
    # swapByFreq()  \
    # -----------------------------------------------------------
    def swapByFreq(self) -> None:
        """
        Updates the key and cipher based on english letter freuquency
        """
        index = 0
        for key in self.key:
            self.key[key] = ENG_FREQ[index]
            index += 1
        self.updateText()
    # end swapByFreq

    # ------------\
    # getCommSS()  \
    # -----------------------------------------------------------
    def getCommSS(self, numSS: int) -> dict:
        """
        Prints the top x substrings of size numSS
        Param numSS: an integer representing the size of substrings the
                      user wants printed
        """
        dictSS = {}
        copyCipher = re.sub(r"[^a-zA-Z0-9 ]", '', self.original)
        defVals = 30
        while copyCipher:
            vals = copyCipher[0:numSS]
            if len(vals) == numSS and " " not in vals:
                if vals in dictSS.keys():
                    dictSS[vals] += 1
                else:
                    dictSS[vals] = 1
            copyCipher = copyCipher[1:]
        if len(dictSS) < defVals:
            defVals = len(dictSS)
        res = dict(sorted(dictSS.items(), key=itemgetter(1),
                          reverse=True)[:defVals])
        return res
    # end showCommSS

        # -----------\
        # getDupSS()  \
        # -----------------------------------------------------------
    def getDupSS(self) -> dict:
        """
        Prints out all two letter duplicate substrings
        """
        dictSS = {}
        copyCipher = re.sub(r"[^a-zA-Z0-9 ]", '', self.original)
        defVals = 30
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
    # end showDupSS

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

import unittest
import random
import string
from substitutioncipher import *

class SubstitutionCipherTests(unittest.TestCase):
    def test_caesar_shift_key(self):
        self.assertTrue(SubstitutionCipher.caesar_shift_key(1)==list("BCDEFGHIJKLMNOPQRSTUVWXYZA"))
        self.assertTrue(SubstitutionCipher.caesar_shift_key(2)==list("CDEFGHIJKLMNOPQRSTUVWXYZAB"))
        self.assertTrue(SubstitutionCipher.caesar_shift_key(-1)==list("ZABCDEFGHIJKLMNOPQRSTUVWXY"))
        self.assertTrue(SubstitutionCipher.caesar_shift_key(-2)==list("YZABCDEFGHIJKLMNOPQRSTUVWX"))

    def test_encrypt(self):
        plaintext = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = list("BCDEFGHIJKLMNOPQRSTUVWXYZA")
        ciphertext = SubstitutionCipher.encrypt(key, plaintext)
        self.assertTrue(ciphertext=="BCDEFGHIJKLMNOPQRSTUVWXYZA")

    def test_next_keys(self):
        next_keys = SubstitutionCipher.next_keys(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), 1, seed=0)
        self.assertTrue(next_keys==[list("ABCDEFGHIJKLYNOPQRSTUVWXMZ")])

def main():
    unittest.main()

if __name__ == '__main__':
    main()

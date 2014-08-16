import unittest
from enigma import *

class EnigmaTests(unittest.TestCase):
    def test_step_rotors(self):
        enigma = Enigma("123", "AAA")
        self.failUnless(enigma.rotor_pos==list("AAA"))
        enigma.step_rotors_explicit("D", "C")
        self.failUnless(enigma.rotor_pos==list("AAB"))
        enigma.step_rotors_explicit("D", "C")
        self.failUnless(enigma.rotor_pos==list("AAC"))
        enigma.step_rotors_explicit("D", "C")
        self.failUnless(enigma.rotor_pos==list("ABD"))

        enigma.step_rotors_explicit("B", "F")
        self.failUnless(enigma.rotor_pos==list("BCE"))
        enigma.step_rotors_explicit("B", "F")
        self.failUnless(enigma.rotor_pos==list("BCF"))
        enigma.step_rotors_explicit("B", "F")
        self.failUnless(enigma.rotor_pos==list("BDG"))
        enigma.step_rotors_explicit("B", "F")
        self.failUnless(enigma.rotor_pos==list("BDH"))

    def test_double_step(self):
        enigma = Enigma("321", "KER")
        enigma.step_rotors_explicit("E", "Q")
        self.failUnless(enigma.rotor_pos==list("LFS"))

    def test_step_rotor_double(self):
        enigma = Enigma("321", "KDO")
        expected_rotors = [list("KDP"), list("KDQ"), list("KER"), list("LFS"), list("LFT")]
        for i in range(5):
            enigma.step_rotors()
            self.failUnless(enigma.rotor_pos==expected_rotors[i])

    def test_increment_letter(self):
        enigma = Enigma("123", "AAA")
        self.failUnless(enigma.increment_letter("A")=="B")
        self.failUnless(enigma.increment_letter("B")=="C")
        self.failUnless(enigma.increment_letter("C")=="D")
        self.failUnless(enigma.increment_letter("Y")=="Z")
        self.failUnless(enigma.increment_letter("Z")=="A")

    def test_add_to_letter(self):
        enigma = Enigma("123", "AAA")
        self.failUnless(enigma.add_to_letter("A",5)=="F")
        self.failUnless(enigma.add_to_letter("B",5)=="G")
        self.failUnless(enigma.add_to_letter("C",5)=="H")
        self.failUnless(enigma.add_to_letter("Y",5)=="D")
        self.failUnless(enigma.add_to_letter("Z",5)=="E")

        self.failUnless(enigma.add_to_letter("A",9)=="J")
        self.failUnless(enigma.add_to_letter("B",9)=="K")
        self.failUnless(enigma.add_to_letter("C",9)=="L")
        self.failUnless(enigma.add_to_letter("Y",9)=="H")
        self.failUnless(enigma.add_to_letter("Z",9)=="I")

    def test_apply_rotors(self):
        enigma = Enigma("123", "AAA")
        self.failUnless(enigma.apply_rotors(1,2,3,"A")=="U")

    def test_cipher(self):
        enigma = Enigma("123", "AAA", ["AB", "CD"])
        self.failUnless(enigma.cipher("B")=="U")

        enigma = Enigma("123", "AAA", ["AB", "CD", "UV"])
        self.failUnless(enigma.cipher("B")=="V")

def main():
    unittest.main()

if __name__ == '__main__':
    main()

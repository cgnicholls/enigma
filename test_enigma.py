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

def main():
    unittest.main()

if __name__ == '__main__':
    main()

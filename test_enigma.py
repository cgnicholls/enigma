import unittest
from enigma import *

class EnigmaTests(unittest.TestCase):
    def test_step_rotors(self):
        enigma = Enigma(rotor_order="123", rotor_pos="AAA")
        self.assertTrue(enigma.rotor_pos==list("AAA"))
        enigma.step_rotors_explicit("D", "C")
        self.assertTrue(enigma.rotor_pos==list("AAB"))
        enigma.step_rotors_explicit("D", "C")
        self.assertTrue(enigma.rotor_pos==list("AAC"))
        enigma.step_rotors_explicit("D", "C")
        self.assertTrue(enigma.rotor_pos==list("ABD"))

        enigma.step_rotors_explicit("B", "F")
        self.assertTrue(enigma.rotor_pos==list("BCE"))
        enigma.step_rotors_explicit("B", "F")
        self.assertTrue(enigma.rotor_pos==list("BCF"))
        enigma.step_rotors_explicit("B", "F")
        self.assertTrue(enigma.rotor_pos==list("BDG"))
        enigma.step_rotors_explicit("B", "F")
        self.assertTrue(enigma.rotor_pos==list("BDH"))

    def test_double_step(self):
        enigma = Enigma(rotor_order="321", rotor_pos="KER")
        enigma.step_rotors_explicit("E", "Q")
        self.assertTrue(enigma.rotor_pos==list("LFS"))

    def test_step_rotor_double(self):
        enigma = Enigma(rotor_order="321", rotor_pos="KDO")
        expected_rotors = [list("KDP"), list("KDQ"), list("KER"), list("LFS"), list("LFT")]
        for i in range(5):
            enigma.step_rotors()
            self.assertTrue(enigma.rotor_pos==expected_rotors[i])

    def test_increment_letter(self):
        enigma = Enigma(rotor_order="123", rotor_pos="AAA")
        self.assertTrue(enigma.increment_letter("A")=="B")
        self.assertTrue(enigma.increment_letter("B")=="C")
        self.assertTrue(enigma.increment_letter("C")=="D")
        self.assertTrue(enigma.increment_letter("Y")=="Z")
        self.assertTrue(enigma.increment_letter("Z")=="A")

    def test_add_to_letter(self):
        enigma = Enigma(rotor_order="123", rotor_pos="AAA")
        self.assertTrue(enigma.add_to_letter("A",5)=="F")
        self.assertTrue(enigma.add_to_letter("B",5)=="G")
        self.assertTrue(enigma.add_to_letter("C",5)=="H")
        self.assertTrue(enigma.add_to_letter("Y",5)=="D")
        self.assertTrue(enigma.add_to_letter("Z",5)=="E")

        self.assertTrue(enigma.add_to_letter("A",9)=="J")
        self.assertTrue(enigma.add_to_letter("B",9)=="K")
        self.assertTrue(enigma.add_to_letter("C",9)=="L")
        self.assertTrue(enigma.add_to_letter("Y",9)=="H")
        self.assertTrue(enigma.add_to_letter("Z",9)=="I")

    def test_apply_rotor(self):
        enigma = Enigma(rotor_order="123", ring_setting="CSW", rotor_pos="AAA")
        self.assertTrue(enigma.apply_rotor(3, "E", "A", "C")=="Q")
        
        enigma = Enigma(rotor_order="123", ring_setting="AAA", rotor_pos="GBN")
        self.assertTrue(enigma.apply_rotor(2, "A", "B", "X")=="O")

        enigma = Enigma(rotor_order="234", ring_setting="BSK", rotor_pos="SXC")
        self.assertTrue(enigma.apply_rotor(4, "K", "C", "D")=="D")

    def test_apply_rotors(self):
        enigma = Enigma(rotor_order="123", rotor_pos="AAA")
        self.assertTrue(enigma.apply_rotors(1,2,3,"A")=="U")

    def test_cipher(self):
        enigma = Enigma(rotor_order="123", rotor_pos="AAA", plugs=["AB", "CD"])
        self.assertTrue(enigma.cipher("B")=="U")

        enigma = Enigma(rotor_order="123", rotor_pos="AAA", plugs=["AB", "CD", "UV"])
        self.assertTrue(enigma.cipher("B")=="V")

def main():
    unittest.main()

if __name__ == '__main__':
    main()

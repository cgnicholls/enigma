import string

rotorlist1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
rotorlist2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
rotorlist3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
rotorlist4 = list("ESOVPZJAYQUIRHXLNFTGKDCMWB")
rotorlist5 = list("VZBRGITYUPSDNHLXAWMJQOFECK")
rotorlist6 = list("JPGVOUMFYQBENHZRDKASXLICTW")
rotorlist7 = list("NZJHGRCXMYSWBOUFAIVLPEKQDT")
rotorlist8 = list("FKQHTLXOCBJSPDZRAMEWNIUYGV")

alphabet = list(string.ascii_uppercase)
rotor = dict()
rotor[1] = {a:x for (a,x) in zip(alphabet, rotorlist1)}
rotor[2] = {a:x for (a,x) in zip(alphabet, rotorlist2)}
rotor[3] = {a:x for (a,x) in zip(alphabet, rotorlist3)}
rotor[4] = {a:x for (a,x) in zip(alphabet, rotorlist4)}
rotor[5] = {a:x for (a,x) in zip(alphabet, rotorlist5)}
#rotor[6] = {a:x for (a,x) in zip(alphabet, rotorlist6)}
#rotor[7] = {a:x for (a,x) in zip(alphabet, rotorlist7)}
#rotor[8] = {a:x for (a,x) in zip(alphabet, rotorlist8)}

# Create the inverse dictionaries
inv_rotor = dict()
for i in range(1, 6):
    inv_rotor[i] = {v:k for k, v in rotor[i].items()}

stepping = dict()
stepping[1] = "Q"
stepping[2] = "E"
stepping[3] = "V"
stepping[4] = "J"
stepping[5] = "Z"

reflectorlist = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")
reflector = {a:x for (a,x) in zip(alphabet, reflectorlist)}

class Enigma:
    def __init__(self, rotor_order, ring_setting = "AAA", rotor_pos = "AAA", plugs = []):
        # note that rotor_pos should be of the form "GJD" 
        # and ring_setting should be of the form "SNK"
        self.rotor_order = [int(x) for x in rotor_order]
        self.rotor_pos = list(rotor_pos)
        self.ring_setting = list(ring_setting)
        self.stecker_dict = {a:a for a in alphabet}
        for plug in plugs:
            self.stecker_dict[plug[0]] = plug[1]
            self.stecker_dict[plug[1]] = plug[0]

    # Cycles through capital letters in ascii.
    # i.e. A -> B, ..., Z -> A
    def increment_letter(self, letter):
        return chr((ord(letter)-65+1)%26+65)

    def add_to_letter(self, letter, increase):
        return chr((ord(letter)-65+increase)%26+65)

    def step_rotors_explicit(self, middle_notch, right_notch):
        # Increment right rotor
        step_middle = (self.rotor_pos[2] == right_notch)
        step_left = (self.rotor_pos[1] == middle_notch)

        # Always step the fast rotor
        self.rotor_pos[2] = self.increment_letter(self.rotor_pos[2])

        # Account for the double step. Middle rotor steps if the right rotor
        # is at the notch position, or if the left rotor steps, i.e. if the
        # middle rotor is at its notch position
        if step_middle or step_left:
            self.rotor_pos[1] = self.increment_letter(self.rotor_pos[1])
        if step_left:
            self.rotor_pos[0] = self.increment_letter(self.rotor_pos[0])

    def step_rotors(self):
        self.step_rotors_explicit(stepping[self.rotor_order[1]], stepping[self.rotor_order[2]])

    # Applies the given rotors
    def apply_rotors(self, left_rotor, middle_rotor, right_rotor, plaintext_character):
        # Letter passes through the rotors right to left
        ciphered = self.apply_rotor(right_rotor, self.ring_setting[2], self.rotor_pos[2], plaintext_character)
        ciphered = self.apply_rotor(middle_rotor, self.ring_setting[1], self.rotor_pos[1], ciphered)
        ciphered = self.apply_rotor(left_rotor, self.ring_setting[0], self.rotor_pos[0], ciphered)
        # Passes through reflector
        ciphered = reflector[ciphered]
        # Passes through rotors left to right
        ciphered = self.apply_inverse_rotor(left_rotor, self.ring_setting[0], self.rotor_pos[0], ciphered)
        ciphered = self.apply_inverse_rotor(middle_rotor, self.ring_setting[1], self.rotor_pos[1], ciphered)
        ciphered = self.apply_inverse_rotor(right_rotor, self.ring_setting[2], self.rotor_pos[2], ciphered)  
        return ciphered

    def apply_rotor(self, rotor_num, ring_setting, rotor_pos, plaintext_character):
        # calculate change thanks to rotor position
        change_pos = ord(rotor_pos)-65
        # calculate change thanks to ring setting
        change_setting = ord(ring_setting)-65
        increase = (change_pos - change_setting)%26

        ciphered = self.add_to_letter(plaintext_character, increase)
        ciphered = rotor[rotor_num][ciphered]
        return ciphered

    def apply_inverse_rotor(self, rotor_num, ring_setting, rotor_pos, plaintext_character):
        # calculate change thanks to rotor position
        change_pos = ord(rotor_pos)-65
        # calculate change thanks to ring setting
        change_setting = ord(ring_setting)-65
        increase = (change_pos - change_setting)%26
        
        ciphered = self.add_to_letter(plaintext_character, increase)
        ciphered = inv_rotor[rotor_num][ciphered]
        return ciphered

    def apply_steckerboard(self, stecker_dict, plaintext_character):
        return stecker_dict[plaintext_character]

    def cipher(self, letter):
        ciphered = self.apply_steckerboard(self.stecker_dict, letter)
        ciphered = self.apply_rotors(self.rotor_order[0], self.rotor_order[1], self.rotor_order[2], ciphered)
        ciphered = self.apply_steckerboard(self.stecker_dict, ciphered)
        return ciphered

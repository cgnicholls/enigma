import string
from enigma import *

class Cryptanalysis:
    @staticmethod
    def monograph_frequencies(text):
        if len(text) == 0:
            return None

        frequencies = dict()
        alphabet = string.ascii_uppercase
        for a in alphabet:
            frequencies[a] = 0
        for i in range(len(text)):
            a = text[i]
            frequencies[a] += 1

        for a in alphabet:
            frequencies[a] = frequencies[a] / float(len(text))
        return frequencies

    @staticmethod
    def digraph_frequencies(text):
        if len(text) == 0:
            return None

        frequencies = dict()
        alphabet = string.ascii_uppercase
        for a in alphabet:
            for b in alphabet:
                frequencies[(a,b)] = 0
        for i in range(len(text)-1):
            a = text[i].upper()
            b = text[i+1].upper()
            if Cryptanalysis.is_upper_alpha(a) and Cryptanalysis.is_upper_alpha(b):
                frequencies[(a,b)] += 1

        for a in alphabet:
            for b in alphabet:
                frequencies[(a,b)] = frequencies[(a,b)] / float(len(text))
        return frequencies

    @staticmethod
    def is_upper_alpha(c):
        if ord(c) >= 65 and ord(c) <= 90:
            return True
        else:
            return False

    @staticmethod
    def score_key(ciphertext, key="AAA"):
        enigma = Enigma(rotor_order="123", rotor_pos=key)
        putative_plaintext = enigma.encrypt(ciphertext)
        ct_monographs = crypt.monograph_frequencies(ciphertext)
        ct_digraphs = crypt.digraph_frequencies(ciphertext)
        return crypt.squared_difference_frequencies(ct_monographs, monographs)

    @staticmethod
    def solve_with_rotor_order(ciphertext, monographs_model, digraphs_model, rotor_order):
        middle_step = Enigma.stepping_point(int(rotor_order[1]))
        right_step = Enigma.stepping_point(int(rotor_order[2]))
        key = list("AAA")
        best_key = None
        best_mono = float("infinity")
        while key != list("AAA") or best_key == None:
            enigma = Enigma(rotor_order, ring_setting="".join(key))
            putative_plaintext = enigma.encrypt(ciphertext)
            #digraphs_ppt = Cryptanalysis.digraph_frequencies(putative_plaintext)
            monographs_ppt = Cryptanalysis.monograph_frequencies(putative_plaintext)
            #squared_diff_di = Cryptanalysis.squared_difference_frequencies(digraphs_ppt, digraphs_model)
            squared_diff_mono = Cryptanalysis.squared_difference_frequencies(monographs_ppt, monographs_model)

            if squared_diff_mono < best_mono:
                best_key = list("".join(key))
                best_mono = squared_diff_mono

            #print(key, squared_diff_mono)
            #print("BEST KEY", best_key, best_mono)
            key = Enigma.step_rotors_explicit(key, middle_step, right_step)
        return best_key

    @staticmethod
    def all_rotor_orders():
        rotor_orders = []
        count = 0
        for i in range(1, 6):
            for j in range(1, 6):
                for k in range(1, 6):
                    if i == j or i == k or j == k:
                        continue
                    rotor_orders.append(str(i)+str(j)+str(k))
        return rotor_orders

    @staticmethod
    def solve(ciphertext, monographs_model, digraphs_model):
        rotor_orders = Cryptanalysis.all_rotor_orders()
        for rotor_order in rotor_orders:
            print(rotor_order, Cryptanalysis.solve_with_rotor_order(ciphertext, monographs_model, digraphs_model, rotor_order))

    @staticmethod
    def solve_with_rotor_order_unknown_plugs(ciphertext, monographs_model, rotor_order):
        key_scores = dict()
        middle_step = Enigma.stepping_point(int(rotor_order[1]))
        right_step = Enigma.stepping_point(int(rotor_order[2]))
        key = list("AAA")
        best_key = None
        best_mono = float("infinity")
        while key != list("AAA") or best_key == None:
            enigma = Enigma(rotor_order, ring_setting="".join(key))
            putative_plaintext = enigma.encrypt(ciphertext)
            monographs_ppt = Cryptanalysis.monograph_frequencies(putative_plaintext)
            sorted_monographs_model = sorted(monographs_model.values())
            sorted_monographs_ppt = sorted(monographs_ppt.values())
            squared_diff_mono = Cryptanalysis.squared_difference_lists(sorted_monographs_ppt, sorted_monographs_model)

            key_scores["".join(key)] = squared_diff_mono

            if squared_diff_mono < best_mono:
                best_key = list("".join(key))
                best_mono = squared_diff_mono

            #print(key, squared_diff_mono)
            #print("BEST KEY", best_key, best_mono)
            key = Enigma.step_rotors_explicit(key, middle_step, right_step)

        sorted_keys = sorted(key_scores, key=key_scores.get)
        print(sorted_keys[0:20])
        return list(sorted_keys[0])

    @staticmethod
    def solve_with_unknown_plugs(ciphertext, monographs_model):
        best_rotors = []
        rotor_orders = Cryptanalysis.all_rotor_orders()
        for rotor_order in rotor_orders:
            best_rotor = Cryptanalysis.solve_with_rotor_order_unknown_plugs(ciphertext, monographs_model, rotor_order)
            best_rotors.append((rotor_order, best_rotor))
            print(rotor_order, best_rotor)
        return best_rotors

    @staticmethod
    def squared_difference_lists(list1, list2):
        squared_diff = 0
        for i in range(len(list1)):
            squared_diff += (list1[i] - list2[i]) ** 2
        return squared_diff / float(len(list1))

    @staticmethod
    def squared_difference_frequencies(dict1, dict2):
        squared_diff = 0
        for key in dict1.keys():
            squared_diff += (dict1[key] - dict2[key]) ** 2
        return squared_diff / float(len(dict1.keys()))

def sample_plaintext(length=500):
    text = open("animal-farm.txt")
    text_str = ""
    count = 0
    while True:
        c = text.read(1)
        if not c or count >= length:
            break
        c = c.upper()
        if ord(c) >= 65 and ord(c) <= 90:
            text_str += c
        count += 1
    return text_str

def build_text_string_from_file(file_name):
    text = open(file_name)
    text_str = ""
    while True:
        c = text.read(1)
        if not c:
            break
        c = c.upper()
        if ord(c) >= 65 and ord(c) <= 90:
            text_str += c
    return text_str

def compute_language_model(file_name):
    text_str = build_text_string_from_file("animal-farm.txt")
    crypt = Cryptanalysis()
    digraphs = crypt.digraph_frequencies(text_str)
    monographs = crypt.monograph_frequencies(text_str)
    return (monographs, digraphs)

def main():
    (monographs_model, digraphs_model) = compute_language_model("animal-farm.txt")

    plaintext = sample_plaintext(200)
    crypt = Cryptanalysis()
    pt_monographs = crypt.monograph_frequencies(plaintext)
    pt_digraphs = crypt.digraph_frequencies(plaintext)
    print(crypt.squared_difference_frequencies(pt_monographs, monographs_model))
    print(crypt.squared_difference_frequencies(pt_digraphs, digraphs_model))

    enigma = Enigma(rotor_order="321", ring_setting="AAB", plugs=["AB", "CD", "EF"])
    ciphertext = enigma.encrypt(plaintext)
    ct_monographs = crypt.monograph_frequencies(ciphertext)
    ct_digraphs = crypt.digraph_frequencies(ciphertext)
    print(crypt.squared_difference_frequencies(ct_monographs, monographs_model))
    print(crypt.squared_difference_frequencies(ct_digraphs, digraphs_model))

    #best_key = Cryptanalysis.solve_with_rotor_order_unknown_plugs(ciphertext, monographs_model, "321")
    best_key = Cryptanalysis.solve_with_unknown_plugs(ciphertext, monographs_model)
    #best_key = Cryptanalysis.solve(ciphertext, monographs_model, digraphs_model)
    print("BEST KEY", best_key)

if __name__ == "__main__":
    main()

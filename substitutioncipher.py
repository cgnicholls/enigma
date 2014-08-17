import string
import random
from cryptanalysis import *
class SubstitutionCipher:
    @staticmethod
    def swap_two_letters(key):
        # Choose 2 letters at random and switch
        alphabet = list(string.ascii_uppercase)
        swap = random.sample(alphabet, 2)
        index0 = key.index(swap[0])
        index1 = key.index(swap[1])
        key[index0] = swap[1]
        key[index1] = swap[0]
        return key

    @staticmethod
    def next_keys(key, num_keys, seed=None):
        if seed != None:
            random.seed(seed)
        next_keys = []
        for i in range(num_keys):
            next_key = key.copy()
            num_swaps = random.randint(1, 4)
            for j in range(num_swaps):
                SubstitutionCipher.swap_two_letters(next_key)
            next_keys.append(next_key)
        return next_keys

    @staticmethod
    def best_n_keys(ciphertext, monographs_model, digraphs_model, keys, n):
        key_scores = dict()
        for key in keys:
            putative_plaintext = SubstitutionCipher.decrypt(key, ciphertext)
            monographs_pt = Cryptanalysis.monograph_frequencies(putative_plaintext)
            digraphs_pt = Cryptanalysis.digraph_frequencies(putative_plaintext)
            mono_score = Cryptanalysis.squared_difference_frequencies(monographs_pt, monographs_model)
            di_score = Cryptanalysis.squared_difference_frequencies(digraphs_pt, digraphs_model)
            #print("KEY", key)
            #print(putative_plaintext)
            #print(di_score)
            key_scores["".join(key)] = di_score
        return sorted(key_scores, key=key_scores.get)[0:n]

    @staticmethod
    def solve_from_putative_key(ciphertext, monographs_model, digraphs_model, p_key):
        start_keys = [p_key]
        while True:
            test_keys = []
            for key in start_keys:
                test_keys += SubstitutionCipher.next_keys(key, 10)
                test_keys += [key]
            best_keys = SubstitutionCipher.best_n_keys(ciphertext, monographs_model, digraphs_model, test_keys, 20)
            print("BEST KEY", best_keys[0])
            start_keys = [list(key_str) for key_str in best_keys]

    @staticmethod
    def solve(ciphertext):
        # Start with any key
        key = string.ascii_uppercase

    @staticmethod
    def score_key(ciphertext, monographs_model, digraphs_model, key):
        putative_plaintext = SubstitutionCipher.decrypt(key, ciphertext)
        monographs_pt = Cryptanalysis.monograph_frequencies(putative_plaintext)
        digraphs_pt = Cryptanalysis.digraph_frequencies(putative_plaintext)
        mono_score = Cryptanalysis.squared_difference_frequencies(monographs_pt, monographs_model)
        di_score = Cryptanalysis.squared_difference_frequencies(digraphs_pt, digraphs_model)
        return di_score

    @staticmethod
    def encrypt(key, plaintext):
        map_key = {a:k for (a,k) in zip(list(string.ascii_uppercase), key)}
        ciphertext = ""
        for c in plaintext:
            ciphertext += map_key[c]
        return ciphertext
        
    @staticmethod
    def decrypt(key, ciphertext):
        map_key = {k:a for (a,k) in zip(list(string.ascii_uppercase), key)}
        plaintext = ""
        for c in ciphertext:
            plaintext += map_key[c]
        return plaintext

    @staticmethod
    def caesar_shift_key(shift):
        shift = shift % 26
        key = list(string.ascii_uppercase)
        key = key[shift:len(key)] + key[0:shift]
        return key

    @staticmethod
    def random_key():
        alphabet = list(string.ascii_uppercase)
        random.shuffle(alphabet)
        return alphabet

    @staticmethod
    def search_for_key(ciphertext, monographs_model, digraphs_model, start_key):
        while True:
            key_scores = dict()
            for i in range(1000):
                next_key = start_key.copy()
                num_swaps = random.randint(1, 10)
                for j in range(num_swaps):
                    SubstitutionCipher.swap_two_letters(next_key)
                next_key_score = SubstitutionCipher.score_key(ciphertext, monographs_model, digraphs_model, next_key)
                key_scores["".join(next_key)] = next_key_score
            best_key_scores = sorted(key_scores, key=key_scores.get)
            print(best_key_scores[0:20])
            start_key = list(best_key_scores[0])

def main():
    (monographs_model, digraphs_model) = compute_language_model("animal-farm.txt")

    plaintext = sample_plaintext(500)
    print(plaintext)
    key = SubstitutionCipher.caesar_shift_key(3)
    ciphertext = SubstitutionCipher.encrypt(key, plaintext)

    #SubstitutionCipher.solve_from_putative_key(ciphertext, monographs_model, digraphs_model, list(string.ascii_uppercase))
    SubstitutionCipher.search_for_key(ciphertext, monographs_model, digraphs_model, list(string.ascii_uppercase))

if __name__ == "__main__":
    main()

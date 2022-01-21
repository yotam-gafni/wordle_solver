from functools import lru_cache
from collections import defaultdict
import math

class FullScan(object):
    def __init__(self, all_lines_words, file_lines_words, histo, hard_mode = False, Verbose = False):
        self.histo = histo
        self.hard_mode = hard_mode
        self.Verbose = Verbose
        self.hit_count = 0
        self.miss_count = 0
        self.all_lines_words = all_lines_words
        self.file_lines_words = file_lines_words

        self.all_lines = range(len(all_lines_words))
        self.file_lines = [all_lines_words.index(x) for x in file_lines_words]
        if Verbose:
            print("Prepopulation start!")
        self.responseCache = {}  # numpy.zeros((len(all_lines_words),len(all_lines_words)),dtype=numpy.uint8)
        for i in self.all_lines:
            for j in self.file_lines:
                self.responseCache[(i, j)] = self.calc_response_vector_slow(i, j)
        if Verbose:
            print("Prepopulation done!")


    #@lru_cache(maxsize=None)
    def calc_response_vector_slow(self, w1,w2):
        #print(w1)
        #print(w2)
        w1 = self.all_lines_words[w1]
        w2 = self.all_lines_words[w2]
        tw2 = str(w2)
        msum_int = 0
        msum = [0 for i in range(5)]
        for c_ind in range(5):
            if w1[c_ind] == tw2[c_ind]:
                msum[c_ind] = 2
                msum_int += 2 * (3**c_ind)
                tw2 = tw2[:c_ind] + "*" + tw2[c_ind+1:]
        for c_ind in range(5):
            if w1[c_ind] in tw2 and msum[c_ind] == 0:
                #msum[c_ind] = 1
                msum_int += 1 * (3**c_ind)
                ind_app = tw2.find(w1[c_ind])
                tw2 = tw2[:ind_app] + "*" + tw2[ind_app+1:]
        return msum_int #msum_to_int(tuple(msum))

    def check_lines(self, guess_lines, lines, depth, start_word):
        if len(lines) == 1:
            self.histo[depth + 1] += 1
            return (depth + 1, depth + 1)
        min_wc = 100000
        max_entropy = 0
        chosen_word = ""
        srmat = {}
        if depth != 0 or start_word is None:
            all_it = guess_lines
        else:
            # all_it = guess_lines
            all_it = [start_word]

        for w1 in all_it:
            rmat = {}
            for w2 in lines:
                if (w1, w2) in self.responseCache:
                    msum = self.responseCache[(w1, w2)]
                    self.hit_count += 1
                else:
                    self.miss_count += 1
                    w1_s = self.all_lines_words[w1]
                    w2_s = self.all_lines_words[w2]
                    tw2 = str(w2_s)
                    msum_int = 0
                    msum_vec = [0 for i in range(5)]
                    for c_ind in range(5):
                        if w1_s[c_ind] == tw2[c_ind]:
                            msum_vec[c_ind] = 2
                            msum_int += 2 * (3 ** c_ind)
                            tw2 = tw2[:c_ind] + "*" + tw2[c_ind + 1:]
                    for c_ind in range(5):
                        if w1_s[c_ind] in tw2 and msum_vec[c_ind] == 0:
                            # msum[c_ind] = 1
                            msum_int += 1 * (3 ** c_ind)
                            ind_app = tw2.find(w1_s[c_ind])
                            tw2 = tw2[:ind_app] + "*" + tw2[ind_app + 1:]
                    self.responseCache[(w1, w2)] = msum_int  # msum_to_int(tuple(msum))
                    msum = msum_int

                if msum not in rmat:
                    rmat[msum] = [w2]
                else:
                    rmat[msum].append(w2)

            M = max([len(val) for val in rmat.values()])
            dict_len = float(len(lines))
            Entropy = -1 * sum([len(val) / dict_len * math.log(len(val) / dict_len) for val in rmat.values()])
            if Entropy > max_entropy:
                # if M < min_wc:
                if self.Verbose:
                    print("M:{},Entropy:{}".format(M, Entropy))
                min_wc = M
                max_entropy = Entropy
                chosen_word = w1
                srmat = rmat
        if self.Verbose:
            print("Min wc: {}, chosen word: {}, depth: {}".format(min_wc, chosen_word, depth))
        newsmat = srmat
        # for sr in srmat:
        #	if len(srmat[sr]) > 5 - depth:
        #		newsmat[sr] = srmat[sr]
        m = depth
        total_steps = 0
        possible_words_mat = {}
        if self.hard_mode:
            w1 = chosen_word
            for w2 in guess_lines:
                if (w1, w2) in self.responseCache:
                    msum = self.responseCache[(w1, w2)]
                    self.hit_count += 1
                else:
                    self.miss_count += 1
                    w1_s = self.all_lines_words[w1]
                    w2_s = self.all_lines_words[w2]
                    tw2 = str(w2_s)
                    msum_int = 0
                    msum_vec = [0 for i in range(5)]
                    for c_ind in range(5):
                        if w1_s[c_ind] == tw2[c_ind]:
                            msum_vec[c_ind] = 2
                            msum_int += 2 * (3 ** c_ind)
                            tw2 = tw2[:c_ind] + "*" + tw2[c_ind + 1:]
                    for c_ind in range(5):
                        if w1_s[c_ind] in tw2 and msum_vec[c_ind] == 0:
                            # msum[c_ind] = 1
                            msum_int += 1 * (3 ** c_ind)
                            ind_app = tw2.find(w1_s[c_ind])
                            tw2 = tw2[:ind_app] + "*" + tw2[ind_app + 1:]
                    self.responseCache[(w1, w2)] = msum_int  # msum_to_int(tuple(msum))
                    msum = msum_int

                if msum not in possible_words_mat:
                    possible_words_mat[msum] = [w2]
                else:
                    possible_words_mat[msum].append(w2)
        it_keys = newsmat.keys()
        for key in it_keys:
            elem = newsmat[key]
            if self.hard_mode:
                max_depth, total_steps_sub = self.check_lines(possible_words_mat[key], elem, depth + 1, None)
            else:
                max_depth, total_steps_sub = self.check_lines(guess_lines, elem, depth + 1, None)
            if self.Verbose and max_depth > 5 and depth in [2, 3]:
                print("Key: {}, depth: {}".format(key, depth))
            m = max(m, max_depth)
            total_steps += total_steps_sub
        return (m, total_steps)



def msum_to_int(msum):
    total = 0
    for i in msum:
        total = total*3 + i
    return total

if __name__ == '__main__':

    all_w = open("words.txt", "r")
    all_lines_words = [x.strip() for x in all_w.readlines()]

    from word_list import poss_words as file_lines_words
    histo = defaultdict(int)
    for start_w in range(len(all_lines_words)):
        fs = FullScan(all_lines_words, file_lines_words, histo)
        m = fs.check_lines(fs.all_lines, fs.file_lines, 0,start_w)
        print("For word {}: Max depth encountered: {}".format(all_lines_words[start_w],m))
        print("Hits: {}, Misses: {}".format(fs.hit_count, fs.miss_count))
        print(histo)
        histo.clear()

from functools import lru_cache
from collections import defaultdict
import math
#import numpy

#f = open("2500.txt","r")
#file_lines = f.readlines()
from word_list import poss_words as file_lines_words

all_w = open("words.txt","r")
all_lines_words = [x.strip() for x in all_w.readlines()]

all_lines = range(len(all_lines_words))
file_lines = [all_lines_words.index(x) for x in file_lines_words]


hard_mode = False

how_deep = 0



def msum_to_int(msum):
    total = 0
    for i in msum:
        total = total*3 + i
    return total

#@lru_cache(maxsize=None)
def calc_response_vector_slow(w1,w2):
    #print(w1)
    #print(w2)
    w1 = all_lines_words[w1]
    w2 = all_lines_words[w2]
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


print("Prepopulation start!")
responseCache = {} #numpy.zeros((len(all_lines_words),len(all_lines_words)),dtype=numpy.uint8)
#for i in all_lines:
#    for j in file_lines:
#        responseCache[(i,j)] = calc_response_vector_slow(i,j)
print("Prepopulation done!")
def calc_response_vector(w1,w2):
    return responseCache[(w1,w2)]

global hit_count
global miss_count
hit_count = 0
miss_count = 0

def check_lines(guess_lines, lines, depth, histogram):
    global hit_count
    global miss_count
    if len(lines) == 1:
        histo[depth+1] += 1
        return (depth+1,depth+1)
    min_wc = 100000
    max_entropy = 0
    chosen_word = ""
    srmat = {}
    if depth != 0:
        all_it = guess_lines
    else:
        all_it = guess_lines
        #all_it = ["snare"]

    for w1 in all_it:
        rmat = {}
        for w2 in lines:
            if (w1,w2) in responseCache:
                msum = responseCache[(w1,w2)]
                hit_count += 1
            else:
                miss_count += 1
                w1_s = all_lines_words[w1]
                w2_s = all_lines_words[w2]
                tw2 = str(w2_s)
                msum_int = 0
                msum_vec = [0 for i in range(5)]
                for c_ind in range(5):
                    if w1_s[c_ind] == tw2[c_ind]:
                        msum_vec[c_ind] = 2
                        msum_int += 2 * (3**c_ind)
                        tw2 = tw2[:c_ind] + "*" + tw2[c_ind+1:]
                for c_ind in range(5):
                    if w1_s[c_ind] in tw2 and msum_vec[c_ind] == 0:
                        #msum[c_ind] = 1
                        msum_int += 1 * (3**c_ind)
                        ind_app = tw2.find(w1_s[c_ind])
                        tw2 = tw2[:ind_app] + "*" + tw2[ind_app+1:]
                responseCache[(w1,w2)] = msum_int #msum_to_int(tuple(msum))
                msum = msum_int


            if msum not in rmat:
                rmat[msum] = [w2]
            else:
                rmat[msum].append(w2)

        M = max([len(val) for val in rmat.values()])
        dict_len = float(len(lines))
        Entropy = -1 * sum([len(val)/dict_len*math.log(len(val)/dict_len) for val in rmat.values()])
        if Entropy > max_entropy:
        #if M < min_wc:
            print("M:{},Entropy:{}".format(M, Entropy))
            min_wc = M
            max_entropy = Entropy
            chosen_word = w1
            srmat = rmat
    print("Min wc: {}, chosen word: {}, depth: {}".format(min_wc, chosen_word,depth))
    newsmat = srmat
    #for sr in srmat:
    #	if len(srmat[sr]) > 5 - depth:
    #		newsmat[sr] = srmat[sr]
    m = depth
    total_steps = 0
    it_keys = newsmat.keys()
    for key in it_keys:
        elem = newsmat[key]
        if hard_mode:
            max_depth,total_steps_sub = check_lines(elem, elem, depth+1, histo)
        else:
            max_depth,total_steps_sub = check_lines(guess_lines, elem, depth+1, histo)
        if max_depth > 5 and depth in [2,3]:
            print("Key: {}, depth: {}".format(key,depth))
        m = max(m,max_depth)
        total_steps += total_steps_sub
    return (m, total_steps)

histo = defaultdict(int)
m = check_lines(all_lines, file_lines, 0, histo)
print("Max depth encountered: {}".format(m))
print("Hits: {}, Misses: {}".format(hit_count, miss_count))
print(histo)

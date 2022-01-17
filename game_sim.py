from functools import lru_cache

counter_example_words = set(["bills","cills","dills","fills","gills","hills", "jills", "kills","lills","mills","nills","pills","rills","sills","tills","vills","wills","yills","zills"])

def msum_to_int(msum):
    total = 0
    for i in msum:
        total = total*3 + i
    return total

@lru_cache(maxsize=None)
def calc_response_vector(w1,w2):
    #print(w1)
    #print(w2)
    w1 = all_lines_words[w1]
    w2 = all_lines_words[w2]
    tw2 = str(w2)
    msum = [0 for i in range(5)]
    for c_ind in range(5):
        if w1[c_ind] == tw2[c_ind]:
            msum[c_ind] = 2
            tw2 = tw2[:c_ind] + "*" + tw2[c_ind+1:]
    for c_ind in range(5):
        if w1[c_ind] in tw2 and msum[c_ind] == 0:
            msum[c_ind] = 1
            ind_app = tw2.find(w1[c_ind])
            tw2 = tw2[:ind_app] + "*" + tw2[ind_app+1:]
    return msum_to_int(tuple(msum))

def calc_response_vector_no_int(w1,w2):
    #print(w1)
    #print(w2)
    w1 = all_lines_words[w1]
    w2 = all_lines_words[w2]
    tw2 = str(w2)
    msum = [0 for i in range(5)]
    for c_ind in range(5):
        if w1[c_ind] == tw2[c_ind]:
            msum[c_ind] = 2
            tw2 = tw2[:c_ind] + "*" + tw2[c_ind+1:]
    for c_ind in range(5):
        if w1[c_ind] in tw2 and msum[c_ind] == 0:
            msum[c_ind] = 1
            ind_app = tw2.find(w1[c_ind])
            tw2 = tw2[:ind_app] + "*" + tw2[ind_app+1:]
    return tuple(msum)

all_w = open("words.txt","r")
all_lines_words = [x.strip() for x in all_w.readlines()]
snare_idx = all_lines_words.index("snare")

srmat_memoize_cache = {}
def calc_srmat(all_lines, lines, past_guesses_feedbacks):
    if past_guesses_feedbacks in srmat_memoize_cache:
        return srmat_memoize_cache[past_guesses_feedbacks]
    min_wc = 100000
    chosen_word = -1
    srmat = {}
    if len(past_guesses_feedbacks) != 0:
        all_it = all_lines
    else:
        all_it = [snare_idx]
    for w1 in all_it:
        rmat = {}
        for w2 in lines:
            msum = calc_response_vector(w1,w2)
            if msum not in rmat:
                rmat[msum] = [w2]
            else:
                rmat[msum].append(w2)
        M = max([len(val) for val in rmat.values()])
        if M < min_wc:
            min_wc = M
            chosen_word = w1
            srmat = rmat
    srmat_memoize_cache[past_guesses_feedbacks] = (srmat, chosen_word)
    return (srmat,chosen_word)

def run_game(target):
    all_lines = range(len(all_lines_words))
    lines = range(len(all_lines_words))
    target_idx = all_lines_words.index(target)
    guess_trace = []
    for round in range(10):
        (srmat,chosen_word) = calc_srmat(all_lines,lines,tuple(guess_trace))
        print(all_lines_words[chosen_word])
        #inp = input()
        #print(inp)
        inp = calc_response_vector_no_int(chosen_word,target_idx)
        print(inp)
        feedback = msum_to_int(tuple([int(el) for el in inp]))
        if feedback not in srmat:
            print("Unexpected feedback {}, srmat: {}".format(feedback,srmat))
        guess_trace.append((chosen_word,feedback))
        lines = srmat[feedback]
        if len(lines) == 1:
            print("Done. Final word is {}".format(all_lines_words[lines[0]]))
            return True
        if round > 4:
            print("Beyond limit, option set:{}".format([all_lines_words[x] for x in lines]))
    print("Failed. Did not find word after 6 attempts")
    return False


def main():
    #print(calc_response_vector("fills","snare"))
    #print(calc_response_vector("fills","moult"))
    for w in counter_example_words:
        print("Playing for {}:".format(w))
        if not run_game(w):
            exit(0)

if __name__ == "__main__":
    main()

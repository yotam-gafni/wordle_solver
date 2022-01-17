from functools import lru_cache

counter_example_words = set(["bills","cills","dills","fills","gills","hills", "jills", "kills","lills","mills","nills","pills","rills","sills","tills","vills","wills","yills","zills"])


@lru_cache(maxsize=None)
def calc_response_vector(target,guess):
    w1 = guess.strip()
    w2 = target.strip()
    tw2 = w2
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
    return msum

def run_game(target):
    f = open("words.txt","r")
    all_w = open("words.txt","r")
    lines = f.readlines()
    all_lines = all_w.readlines()
    for round in range(10):
        min_wc = 100000
        chosen_word = ""
        srmat = {}
        if round != 0:
            all_it = all_lines
        else:
            all_it = ["snare"]
        for w1 in all_it:
            w1 = w1.strip()
            rmat = {}
            for w2 in lines:
                w2 = w2.strip()
                tw2 = w2
                msum = calc_response_vector(w2,w1)
                if tuple(msum) not in rmat:
                    rmat[tuple(msum)] = [w2]
                else:
                    rmat[tuple(msum)].append(w2)
            M = max([len(val) for val in rmat.values()])
            if M < min_wc:
                min_wc = M
                chosen_word = w1
                srmat = rmat
        print(chosen_word)
        #inp = input()
        #print(inp)
        inp = calc_response_vector(target,chosen_word)
        print(inp)
        feedback = tuple([int(el) for el in inp])
        lines = srmat[feedback]
        if len(lines) == 1:
            print("Done. Final word is {}".format(lines[0]))
            return True
        if round > 4:
            print("Beyond limit, option set:{}".format(lines))
    print("Failed. Did not find word after 6 attempts")
    return False


def main():
    print(calc_response_vector("fills","snare"))
    print(calc_response_vector("fills","moult"))
    for w in counter_example_words:
        print("Playing for {}:".format(w))
        if not run_game(w):
            exit(0)

if __name__ == "__main__":
    main()

f = open("words.txt","r")
all_w = open("words.txt","r")

lines = f.readlines()
all_lines = all_w.readlines()


count = 0

from functools import lru_cache

@lru_cache(maxsize=None)
def calc_response_vector(w1,w2):
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



for round in range(6):
	min_wc = 100000
	chosen_word = ""
	srmat = {}
	if round != 0:
		all_it = all_lines
	else:
		all_it = ["aesir"]

	for w1 in all_it:
		w1 = w1.strip()
		mat = {}
		rmat = {}
		for w2 in lines:
			w2 = w2.strip()
			msum = calc_response_vector(w1,w2)
			if tuple(msum) not in rmat:
				rmat[tuple(msum)] = [w2]
			else:
				rmat[tuple(msum)].append(w2)
			mat[tuple([w1,w2])] = msum

		M = max([len(val) for val in rmat.values()])
		if M < min_wc:
			min_wc = M
			chosen_word = w1
			srmat = rmat
		
	print(chosen_word)
	inp = input()
	feedback = tuple([int(el) for el in inp.split(",")])
	lines = srmat[feedback]
	if len(lines) == 1:
		print("Done. Final word is {}".format(lines[0]))
		exit(0)

print("Failed. Did not find word after 6 attempts")


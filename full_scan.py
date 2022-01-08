#f = open("2500.txt","r")
#file_lines = f.readlines()
from word_list import poss_words as file_lines

all_w = open("words.txt","r")

all_lines = all_w.readlines()


hard_mode = False

how_deep = 0


def check_lines(guess_lines, lines, depth): 
	if len(lines) == 1:
		return depth
	min_wc = 100000
	chosen_word = ""
	srmat = {}
	if depth != 0:
		all_it = guess_lines
	else:
		all_it = guess_lines
		#all_it = ["snare"]

	for w1 in all_it:
		w1 = w1.strip()
		mat = {}
		rmat = {}
		for w2 in lines:
			w2 = w2.strip()
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
	print("Min wc: {}, chosen word: {}, depth: {}".format(min_wc, chosen_word,depth))
	newsmat = srmat	
	#for sr in srmat:
	#	if len(srmat[sr]) > 5 - depth:
	#		newsmat[sr] = srmat[sr]
	m = depth
	it_keys = newsmat.keys()
	for key in it_keys:
		elem = newsmat[key]
		if hard_mode:
			curr = check_lines(elem, elem, depth+1)
		else:
			curr = check_lines(guess_lines, elem, depth+1)
		if curr > 5 and depth in [2,3]:
			print("Key: {}, depth: {}".format(key,depth))
		m = max(m,curr)
	return m
		
m = check_lines(all_lines, file_lines, 0)
print("Max depth encountered: {}".format(m))

#f = open("2500.txt","r")
#file_lines = f.readlines()
from word_list import poss_words as file_lines

all_lines = open("words.txt","r").readlines()
hard_mode = False
how_deep = 0

def check_lines(guess_lines, lines, depth): 
	if len(lines) == 1:
		return depth
	
	max_wc = 0
	chosen_word = ""
	srmat = {}
	
	all_it = guess_lines
	# if depth== 0:
	#	all_it = ["snare"]

	for w1 in all_it:
		w1 = w1.strip()
		mat = {}
		rmat = {}
		
		for w2 in lines:
			tw2 = w2 = w2.strip()
			msum = [0 for i in range(5)]
						
			for c_ind in range(5):
				if w1[c_ind] == tw2[c_ind]:
					msum[c_ind] = 2
					tw2 = f"{tw2[:c_ind]}*{tw2[c_ind+1:]}"
			for c_ind in range(5):
				if w1[c_ind] in tw2:
					msum[c_ind] = 1
					ind_app = tw2.find(w1[c_ind])
					tw2 = f"{tw2[:ind_app]}*{tw2[ind_app+1:]}"
					
			pre = [] if tuple(msum) in rmat else rmat[tuple(msum)]
			rmat[tuple(msum)] = pre.append(w2)
			mat[tuple([w1,w2])] = msum

		M = len(rmat)
		if M > max_wc:
			max_wc = M
			chosen_word = w1
			srmat = rmat
			
	print(f"Min wc: {max_wc}, chosen word: {chosen_word}, depth: {depth}"))
	newsmat = srmat	
	m = depth
	it_keys = newsmat.keys()
	
	for key in it_keys:
		elem = newsmat[key]
		curr = check_lines(elem if hard_mode else guess_lines, elem, depth+1)
		if curr > 5 and depth in [2,3]:
			print(f"Key: {key}, depth: {depth}")
		m = max(m,curr)
		
	return m
		
m = check_lines(all_lines, file_lines, 0)
print("Max depth reached: {m}")

from math import sqrt 
from full_scan import FullScan
from collections import defaultdict

Verbose = True

def printv(st):
	if Verbose:
		print(st)

def is_prime(num):
	for div in range(2,int(sqrt(num))):
		if num % div == 0:
			return False
	return True

all_primes = []
for num in range(10 * 1000, 100 * 1000):
	if is_prime(num):
		all_primes.append(num)
printv(all_primes)

max_unq = 0

for p1 in all_primes:
	for p2 in all_primes:
		app = "{}{}".format(p1,p2)
		curr_unq = len(set(list(app)))
		if curr_unq > max_unq:
			max_unq = curr_unq
			argmax_unq = [p1,p2]
		if max_unq == 10:
			break
printv(max_unq)
printv(argmax_unq)

perm_dic = {}
guess_dic = {}
for p1 in all_primes:
	l1 = list(str(p1))
	l1.sort()
	t1 = tuple(l1)
	if t1 in perm_dic:
		perm_dic[t1] += 1
	else:
		perm_dic[t1] = 1
	if t1 in guess_dic:
		guess_dic[t1].append(str(p1))
	else:
		guess_dic[t1] = [str(p1)]

count = 0
all_over_top = []
success = True
for elem in perm_dic:
	if perm_dic[elem] > 4:
		count += 1
		all_over_top.append(perm_dic[elem])
		histo = defaultdict(int)
		fs = FullScan(guess_dic[elem], guess_dic[elem], histo)
		res = fs.check_lines(fs.all_lines, fs.file_lines, 0, None)
		if res[0] > 4:
			printv("Failure. res: {}, guess_dic: {}".format(res, guess_dic[elem]))
			success = False
			break

argmax_perm = max(perm_dic, key=perm_dic.get)
max_perm = perm_dic[argmax_perm]

printv(max_perm)
printv(argmax_perm)
printv(count)
printv(all_over_top)
if success:
	print("Success: Can solve primel in at most 6 guesses")

#histo = defaultdict(int)
#fs = FullScan(["hello"], ["hello"], histo)
#res = fs.check_lines(fs.all_lines, fs.file_lines, 0, None)
#print(res)


	

from math import sqrt 
from full_scan import check_lines

def is_prime(num):
	for div in range(2,int(sqrt(num))):
		if num % div == 0:
			return False
	return True

all_primes = []
for num in range(10 * 1000, 100 * 1000):
	if is_prime(num):
		all_primes.append(num)
print(all_primes)

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
print(max_unq)
print(argmax_unq)

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
		res = check_lines(guess_dic[elem], guess_dic[elem], 0)
		if res > 3:
			print("Failure. res: {}, guess_dic: {}".format(res, guess_dic[elem]))
			success = False
			break

argmax_perm = max(perm_dic, key=perm_dic.get)
max_perm = perm_dic[argmax_perm]

print(max_perm)
print(argmax_perm)
print(count)
print(all_over_top)
if success:
	print("Success: Can solve primel in at most 6 guesses")




	

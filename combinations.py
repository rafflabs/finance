# Combinazioni semplici (senza ripetizione) di n oggetti su p posizioni
# Basato sulla numerazione binaria

n = 9
p = 4
s = 2 ** n - 1

ncomb = 0
i = 0
while i < s:
	d = i
	k = 0
	id = 0
	res = ""
	lowid =0
	is_lowid = True
	while True:
		r = d % 2
		if r == 1:
			k = k + 1
			if k > p:
				break
			else:
				if is_lowid:
					is_lowid = False
					lowid = id
				if id < 10:
					res = res + " " + str(id) + ", "
				else:
					res = res + str(id) + ", "
		id = id + 1
		d = d // 2
		if d == 0:
			break
	# print(i, bin(i), k, res)
	if k == p:
		ncomb = ncomb + 1
		print("[", res, "]", i, bin(i), lowid, ncomb)
		i = i + 2 ** lowid
	else:
		i = i + 1

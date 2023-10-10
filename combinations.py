# k-combinations of n elements
# Calculation and printing of all actual K-COMBINATIONS
# the number of k-combinations of n elements is C(n,k)
# the number of k-element subsets of a n-element set
# C(n,k) is also named binomial coefficient
# C(n,k) = n!/(k! * (n - k)!)
# ======================================================

# The program calculates all the k-element subsets of a n-element set
# The algorithm is based on the binary coding of natural numbers

# For Steiner systems we could use this algorithm to find and list all the blocks
# Steiner System S(t, k, n).
# Number of blocks b:          b = (n t) / (k t)      is an Integer
# (n t) is the number of combinations of n objects on t places
# This is a necessary condition for the existence of the Steiner System S(t, h, N)
# =================================================================================

# ==============================================
# TO DO: Convert to a function in Rust language
# ==============================================

# Number of elements
n = 9

# Number of positions (k-combinations)
p = 4

# Number of subsets not empty
s = 2 ** n - 1

ncomb = 0
i = 0
while i < s:
	d = i
	k = 0
	id = 0
	res = ""
	lowid = 0
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
		
		# print("old i = ", bin(i))
		# print("        ", bin(2 ** lowid))
		# Optimization by skipping (2 ** lowid) loops
		i = i + 2 ** lowid
		print("new i = ", bin(i))
	else:
		i = i + 1

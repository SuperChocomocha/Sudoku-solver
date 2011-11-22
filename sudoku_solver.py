import copy

class sudoku_solver():
	def __init__(self, file):
		self.filename = file
		f = open(file, "r")
		
		#initialize domains of all variables
		self.domain = {}
		var_count = 0
		for line in f:
			for char in line:
				if char == "*":
					self.domain[var_count] = range(1, 10)
					var_count += 1
				else:
					if not char == "\n":
						self.domain[var_count] = [int(char)]
						var_count += 1

		self.constraints = []
		#adding all row constraint arcs
		for i in xrange(9):
			for j in xrange(9*i, 9*i + 9):
				for k in xrange(9*i, 9*i + 9):
					if not j == k and not (j, k, "r") in self.constraints:
						self.constraints.append((j, k, "r"))

		#adding all column constraint arcs
		for i in xrange(9):
			for j in xrange(9):
				for k in xrange(9*i + j, 81, 9):
					for l in xrange(9*i + j, 81, 9):
						if not k == l and not (k, l, "c") in self.constraints:
							self.constraints.append((k, l, "c"))

		#adding all block constraint arcs
		const = [0, 3, 6, 27, 30, 33, 54, 57, 60]
		for num in const:
			for i in xrange(3):
				for j in xrange(3):
					for k in xrange(3):
						for l in xrange(3):
							if not i + 9*j == k + 9*l and not (i + 9*j + num, k + 9*l + num, "b") in self.constraints:
								self.constraints.append((i + 9*j + num, k + 9*l + num, "b"))
		f.close()

	#ac-3 algorithm that eliminates values from the domains based on constraints, eventually solving the constraint satisfaction problem
	def ac_3(self, domain):
		queue = []
		for constraint in self.constraints:
			queue.append(constraint)

		#the ac-3 algorithm
		while queue:
			(xi, xj, cons) = queue.pop(0)
			if self.ac_3_helper(xi, xj, domain):
				for (a, b, c) in self.constraints:
					if b == xi and not a == xj:
						queue.append((a, b, c))
			if not domain[xi]:
				return 0
		
		for key in domain:
			if not len(domain[key]) == 1:
				return 1
		return 2

	#ac-3 helper method, checks the domains of two variables
	def ac_3_helper(self, a, b, domain):
		if len(domain[b]) == 1 and domain[b][0] in domain[a]:
			domain[a].remove(domain[b][0])
			return True
		return False
	
	#assign values using only logic
	def logic_solve(self):
		temp = copy.deepcopy(self.domain)

		for i in xrange(81):
			row = [i]
			col = [i]
			block = [i]
			for (a, b, c) in self.constraints:
				if a == i:
					if c == "r":
						row.append(b)
					elif c == "c":
						col.append(b)
					else:
						block.append(b)

			d1 = {}
			for var in row:
				if len(temp[var]) > 1:
					for val in temp[var]:
						if not val in d1:
							d1[val] = [var]
						else:
							d1[val].append(var)

			for key in d1:
				if len(d1[key]) == 1:
					temp[d1[key][0]] = [key]
			self.ac_3(temp)

			d2 = {}
			for var in col:
				if len(temp[var]) > 1:
					for val in temp[var]:
						if not val in d2:
							d2[val] = [var]
						else:
							d2[val].append(var)

			for key in d2:
				if len(d2[key]) == 1:
					temp[d2[key][0]] = [key]
			self.ac_3(temp)

			d3 = {}
			for var in block:
				if len(temp[var]) > 1:
					for val in temp[var]:
						if not val in d3:
							d3[val] = [var]
						else:
							d3[val].append(var)

			for key in d3:
				if len(d3[key]) == 1:
					temp[d3[key][0]] = [key]
			self.ac_3(temp)

		self.domain = copy.deepcopy(temp)

	#backtrack algorithm that calls ac-3 as a subroutine
	def backtrack(self):
		self.logic_solve()
		if self.ac_3(self.domain) == 2:
			return 2

		temp = copy.deepcopy(self.domain)
		temp2 = copy.deepcopy(self.domain)

		for var in temp2:
			if len(temp2[var]) > 1:
				t = []
				for val in temp2[var]:
					t.append(val)
				for val in t:
					temp2[var] = [val]
					result = self.ac_3(temp2)
					if result == 2:
						self.domain = copy.deepcopy(temp2)
						return 2
					else:
						temp2 = copy.deepcopy(temp)
		return 0

	#output solution to file
	def output_solution(self):
		f = open(self.filename + "_solution.txt", "w")
		f.write(self.filename + "\n")
		if self.backtrack() == 2:
			string = ""
			count = 0
			for key in self.domain:
				string += str(self.domain[key][0])
				count += 1
				if count == 9:
					count = 0
					string += "\n"
			f.write(string)
		else:
			f.write("No Solution. Domains of variables:\n")
			for key in self.domain:
				f.write(str(key) + ": " + str(self.domain[key]) + "\n")
		f.close()

sudoku_solver("ac3solvable_example").output_solution()
sudoku_solver("dp_puzzle").output_solution()
sudoku_solver("gentle_sudoku").output_solution()
sudoku_solver("moderate_sudoku").output_solution()
sudoku_solver("diabolical_sudoku").output_solution()
sudoku_solver("guessing_puzzle").output_solution()


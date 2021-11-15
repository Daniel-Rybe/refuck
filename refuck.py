#!/usr/bin/python3

import re
from rule_classes import *


class ReFuckInterpreter:

	def __init__(self, filename):
		self.program = []
		self.done = False 
		self.rules = [
			BuiltinOpRule('+'),
			BuiltinOpRule('-'),
			BuiltinOpRule('*'),
			BuiltinOpRule('/'),
			BuiltinPrintRule(),
			BuiltinInputRule()
		]

		with open(filename, 'r') as file:
			self.program = self.parse(file)

	def parse(self, file):
		program = []
		line = file.readline()
		while len(line) > 0:
			if line.find('#') != -1:
				line = line[:line.find('#')]
			program.extend(re.findall(r'([^\s]+)', line));
			line = file.readline()
		return program

	def step(self):
		self.rules = self.rules[:6]
		index = 0
		mode = 'normal'
		looking_for_arrow = True
		looking_for_semicollon = True
		rule_match_list = []
		rule_replace_list = []
		self.done = True

		while (index < len(self.program)):
			token = self.program[index]

			offset = 0
			rules_reset = [0] * len(self.rules)
			for rule in self.rules:
				rule.reset()

			while not all(rules_reset) and index + offset < len(self.program):
				for i in range(len(self.rules)):
					if rules_reset[i]: continue
					rule = self.rules[i]
					result = rule.step(self.program[index + offset])
					if result == 1:
						self.program[index : index + offset + 1] = rule.getReplacementList()
						self.done = False
						return;
					if result == -1:
						rules_reset[i] = 1;
				offset += 1

			if mode == 'normal':
				if token == ':':
					mode = 'rule1'
					rule_match_list = []
					rule_replace_list = []
					looking_for_arrow = True

			elif mode == 'rule1':
				if token == '>' and looking_for_arrow:
					mode = 'rule2'
					looking_for_semicollon = True
				else:
					if token == ':':
						looking_for_arrow = False
					elif token == ';':
						looking_for_arrow = True
					rule_match_list.append(token)

			elif mode == 'rule2':
				if token == ';' and looking_for_semicollon:
					mode = 'normal'
					self.rules.append(CustomRule(rule_match_list, rule_replace_list))
				else:
					if token == ':':
						looking_for_semicollon = False
					elif token == ';':
						looking_for_semicollon = True
					rule_replace_list.append(token)

			index += 1



if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--stepbystep', help = 'step by step mode', action='store_true')
	parser.add_argument('-l', '--log', help ='log intermediate state to console', action='store_true')
	parser.add_argument('input', help = 'specify input file')
	args = parser.parse_args()

	interpreter = ReFuckInterpreter(args.input)

	while not interpreter.done:
		if args.stepbystep:
			input()
			
		if args.stepbystep or args.log:
			for token in interpreter.program:
				print(token, end=' ')
			print()

		interpreter.step()

	print()




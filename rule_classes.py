class RuleInterface:

	def step(self, token):
		#return 1 if matched, -1 if not matche, 0 otherwise
		pass

	def getReplacementList(self):
		#returns replacement list if step returned 1
		pass

	def reset(self):
		#reset everything and get ready to match again
		pass


class CustomRule(RuleInterface):

	def __init__(self, match_list, repl_list):
		self.match_list = match_list
		self.repl_list = repl_list;
		self.index = 0
		self.tokens = {}

	def step(self, token):
		if self.match_list[self.index].isupper():
			if not self.match_list[self.index] in self.tokens:
				self.tokens[self.match_list[self.index]] = token;
			elif self.tokens[self.match_list[self.index]] != token:
				return -1

			self.index += 1
			if (self.index == len(self.match_list)):
				return 1
			return 0

		elif token == self.match_list[self.index]:
			self.index += 1
			if (self.index == len(self.match_list)):
				return 1
			return 0
		else:
			return -1

	def getReplacementList(self):
		return [self.tokens[token] if token in self.tokens else token for token in self.repl_list]

	def reset(self):
		self.index = 0
		self.tokens = {}


def is_number(token):
	return token.replace('.','',1).isdigit()

class BuiltinOpRule(RuleInterface):
	def __init__(self, operator):
		self.operator = operator;
		self.stage = 0;
		self.a = 0;
		self.b = 0;

	def step(self, token):
		if self.stage == 0 or self.stage == 1:
			if is_number(token):
				if self.stage == 0:
					if token.isdigit():
						self.a = int(token)
					else:
						self.a = float(token)
				elif self.stage == 1:
					if token.isdigit():
						self.b = int(token)
					else:
						self.b = float(token)
				self.stage += 1
				return 0
			else:
				return -1
		else:
			if token == self.operator:
				return 1
			else:
				return -1

	def getReplacementList(self):
		result = 0
		if self.operator == '+':
			result = self.a + self.b;
		if self.operator == '-':
			result = self.a - self.b;
		if self.operator == '*':
			result = self.a * self.b;
		if self.operator == '/':
			result = self.a / self.b;
			
		if type(result) == float and result.is_integer():
			result = int(result)
		return [str(result)]

	def reset(self):
		self.stage = 0;


class BuiltinPrintRule(RuleInterface):

	def __init__(self):
		self.stage = 0
		self.token = ''

	def step(self, token):
		if self.stage == 0:
			self.stage = 1
			self.token = token
			return 0
		else:
			if token.endswith('!'):
				if len(token) > 1:
					print(token[:-1] + ' ', end = '')
				print(self.token)
				return 1
			else:
				return -1

	def getReplacementList(self):
		return [self.token]

	def reset(self):
		self.stage = 0

class BuiltinInputRule(RuleInterface):

	def __init__(self):
		self.token = ''

	def step(self, token):
		if token.endswith('?'):
			prompt = token[:-1] + ' ' if len(token) > 1 else ''
			self.token = input(prompt)
			return 1
		else:
			return -1

	def getReplacementList(self):
		return [self.token]

	def reset(self):
		pass
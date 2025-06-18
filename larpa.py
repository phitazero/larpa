# Lighter ARgPArse v1.0

ARG_FLAG = 0
ARG_POSITIONAL = 1

SELECT_FROM_ALL = 0
SELECT_FROM_FLAGS = 1
SELECT_FROM_OPTIONS = 2

def _indexget(iterable, i):
	if i < 0: return None
	if i >= len(iterable): return None
	return iterable[i]

class ArgumentParser:
	def __init__(self, argv=None, flags=None, options=None):
		if argv is None:
			argv = __import__("sys").argv

		self.argv = argv
		self.flags = []
		self.positional = []
		self.options = {}

		if flags is None: flags = []
		if options is None: options = []

		self.tempArgv = argv.copy()
		self.parseFlags = True

		while (arg := self._eat()) is not None:
			arg, type = arg

			if type == ARG_FLAG:
				if arg in flags:
					self.flags.append(arg)

				elif arg in options:
					nextArg = self._eat()
					if nextArg is None:
						print(f"fatal: flag {arg} requires an option")
						exit(1)

					self.options[arg] = nextArg[0]

				else:
					print(f"fatal: unknown flag: {arg}")
					exit(1)

			else:
				self.positional.append(arg)

		del self.tempArgv
		del self.parseFlags

	def _eat(self):
		arg = _indexget(self.tempArgv, 0)

		if arg is None: return None

		if not self.parseFlags:
			self.tempArgv = self.tempArgv[1:]
			return arg, ARG_POSITIONAL

		if arg == "--":
			self.parseFlags = False
			self.tempArgv = self.tempArgv[1:]
			return self._eat()

		if arg.startswith("--"):
			self.tempArgv = self.tempArgv[1:]
			return arg, ARG_FLAG

		if _indexget(arg, 0) == "-" and _indexget(arg, 1) is not None:
			if len(arg) == 2:
				self.tempArgv = self.tempArgv[1:]
				return arg, ARG_FLAG
			else:
				flag = f"-{arg[1]}"
				self.tempArgv[0] = f"-{arg[2:]}"
				return flag, ARG_FLAG

		self.tempArgv = self.tempArgv[1:]
		return arg, ARG_POSITIONAL


	def getPositional(self, index):
		return _indexget(self.positional, index)

	def whichSet(self, *flags, selectFrom=SELECT_FROM_ALL):
		if selectFrom == SELECT_FROM_ALL:
			selectFrom = self.flags + list(self.options.keys())
		elif selectFrom == SELECT_FROM_FLAGS:
			selectFrom = self.flags
		elif selectFrom == SELECT_FROM_OPTIONS:
			selectFrom = self.options.keys()
		else:
			raise ValueError("Invalid selectFrom provided")

		for arg in selectFrom:
			if arg in flags:
				return arg

		return None

	def isSet(self, *flags):
		return self.whichSet(*flags) is not None

	def getOption(self, *flags, default=None):
		flag = self.whichSet(*flags, SELECT_FROM_OPTIONS)
		
		if flag is None: return default

		return self.options[flag]

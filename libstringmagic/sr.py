#!/usr/bin/python

import types

class CmdManager:
	"""Manages execution of several StringModifier commands."""
	def __init__(self):
		self.cmdChain = []

	def add(self, cmd):
		"""Adds the given command to the command chain.
		   It must be derived from StringModifier."""	
		if not isinstance(cmd, StringModifier):
			raise TypeError("Only objects of classes which are derived from StringModifier may be given.")
		self.cmdChain.append(cmd)

	def execute(self, string):
		"""Executes the command chain on the given string and returns the result."""
		
		# Reset all command objects.
		for cmd in self.cmdChain:
			cmd.reset()

		# Run the commands.
		previousCmd = None
		for cmd in self.cmdChain:
			string = cmd.execute(string, previousCmd)
			previousCmd = cmd
		if string == None:
			raise TypeError("Result ended up to be None.")
		return string

class Result:
	"""Represents that an action has been performed to an index in a string and what have been done."""
	def __init__(self, startindex, endindex, value = None):
		"""startindex is the beginning index of the "current" version of the string and
		   value is the old value, e.g. what was deleted. endindex is the end index of the
		   string, and e.g. for a deletion it should be the same as startindex."""
		if type(startindex) != types.IntType:
			raise TypeError("Start index is not an int: " + str(startindex))
		if type(endindex) != types.IntType:
			raise TypeError("End index is not an int: " + str(endindex))
		self.startindex = startindex
		self.endindex = endindex
		self.value = value
	def getStartindex(self):
		return self.startindex
	def getEndindex(self):
		return self.endindex
	def getValue(self):
		return self.value

class StringModifier:
	"""Base class for all classes which wants to alter a string."""
	def __init__(self):
		self.reset()

	def execute(self, string, previous = None):
		"""Executes the command and returns the result based on the given argument."""
		raise NotImplementedError()
	def reset(self):
		"""Resets the command to a stage where it can be run again.
		   If an implementation requires additional reset, it must overwrite
		   this method but remember to call it."""
		self.results = []
		
class MarkedPartsModifier(StringModifier):
	"""Feeds implementing classes the parts of a string which has been marked, and
	   takes care of reinserting those parts into the original string."""
	def __init__(self):
		StringModifier.__init__(self)

	def modifyPart(self, part):
		"""For each marked part in the current string this method is called.
		   It must return the altered version of the string. The reset method
		   is not called between invocations of this method."""
		raise NotImplementedError()

	def execute(self, string, previous = None):
		"""Executes the command and returns the result based on the given argument."""
		if previous == None:
			previous = StringModifier()
		prevIndex = 0
		prevRes = None
		addindex = 0 # How much the new string grows.
		newstring = ""
		for res in previous.results:
			strBefore = string[:res.startindex]
			strMarked = string[res.startindex : res.endindex]
			strAfter  = string[res.endindex:]
			latestUnmidified = ""
			if prevRes == None:
				latestUnmidified = string[:res.startindex]
			else:
				latestUnmidified = string[prevRes.endindex:res.startindex]
			strModified = self.modifyPart(strMarked)
			# Insert the string at the proper location.
			newstring = newstring + latestUnmidified + strModified

			# Save what we did and where we did it.
			prevIndex = res.endindex
			prevRes = Result(res.startindex + addindex,
			          res.startindex + addindex + len(strModified), strModified) 
			self.results.append(prevRes)
			addindex = addindex + len(strModified)
		newstring = newstring + string[prevIndex:]
		return newstring
	
class Everything(StringModifier):
	"""Marks the entire string."""
	def __init__(self):
		StringModifier.__init__(self)
		
	def execute(self, string, previous = None):
		"""Executes the command and returns the result based on the given argument."""
		self.results.append(Result(0, len(string), string))
		return string
class Search(StringModifier):
	"""Searches for the string given as parameter."""
	search = ""
	def __init__(self, search):
		StringModifier.__init__(self)
		self.search = search

	def execute(self, string, previous = None):
		"""Executes the command and returns the result based on the given argument."""
		index = string.find(self.search)
		while index >= 0:
			# Save the current finds.
			self.results.append(Result(index, index + len(self.search), self.search))
			# Find again: Is there more?
			index = string.find(self.search, index + 1)
		return string

class Delete(StringModifier):
	"""Deletes the strings marked by the previous StringModifier."""
	def __init__(self):
		StringModifier.__init__(self)
	
	def execute(self, string, previous = None):
		"""Executes the command and returns the result based on the given argument."""
		if previous == None:
			previous = StringModifier()
		addindex = 0
		for res in previous.results:
			# Remove the current finds from the work string.
			string = string[0 : res.startindex + addindex] + string[res.endindex + addindex :]
			self.results.append(Result(res.startindex + addindex, res.startindex + addindex, res.value))
			addindex = addindex - len(res.value)
		return string
			
		
class Insert(StringModifier):
	"""Inserts a given string at the locations marked by e.g. a search."""
	def __init__(self, insert):
		StringModifier.__init__(self)
		self.insert = insert

	def execute(self, string, previous = None):
		"""Executes the command and returns the result based on the given argument."""
		if previous == None:
			previous = StringModifier()
		prevIndex = 0
		addindex = 0 # How much the new string grows.
		newstring = ""
		for res in previous.results:
			# Insert the string at the proper location.
			newstring = newstring + string[prevIndex:res.endindex]  + self.insert

			# Save what we did and where we did it.
			prevIndex = res.endindex
			self.results.append(Result(res.startindex + addindex,
			                       res.startindex + addindex + len(self.insert), self.insert))
			addindex = addindex + len(self.insert)
		newstring = newstring + string[prevIndex:]
		return newstring
class Append(StringModifier):
	"""Marks where a string to the end of the file name, not altering the extension."""
	def __init__(self):
		StringModifier.__init__(self)
		self.appendExtension = False # Append to the extension?

	def execute(self, string, previous = None):
		"""Executes the command and returns the result based on the given argument."""
                rdot = string.find(".")
                if rdot > -1 and self.appendExtension == False:
			self.results.append(Result(rdot, rdot, ""))
                        return string
                else:
			self.results.append(Result(len(string), len(string), ""))
                        return string
	def setAppendExtension(self, appendExtension):
		"""Sets if appending must always be done to the file extension (value True)
		   or just to the file name (value False)."""
		self.appendExtension = appendExtension

class Prefix(StringModifier):
	"""Marks the string in the beginning of each string."""
	def __init__(self):
		StringModifier.__init__(self)
		
	def execute(self, string, previous = None):
		"""Executes the command and returns the result based on the given argument."""
		self.results.append(Result(0, 0, ""))
		return string
class Lowercase(MarkedPartsModifier):
	"""Makes the marked text lower case."""
	def __init__(self):
		MarkedPartsModifier.__init__(self)
	def modifyPart(self, part):
		"""For each marked part in the current string this method is called.
		   It must return the altered version of the string. The reset method
		   is not called between invocations of this method."""
		return part.lower()
class Uppercase(MarkedPartsModifier):
	"""Makes the marked text lower case."""
	def __init__(self):
		MarkedPartsModifier.__init__(self)
	def modifyPart(self, part):
		"""For each marked part in the current string this method is called.
		   It must return the altered version of the string. The reset method
		   is not called between invocations of this method."""
		return part.upper()
class Numbering(MarkedPartsModifier):
	BEFORE = 1
	AFTER = 2
	"""Inserts numbers before or after marked parts."""
	def __init__(self, start = 1, interval = 1, insert = None):
		MarkedPartsModifier.__init__(self)
		if insert == self.AFTER or insert == None:
			self.format = '%(str)s%(num)d'
		elif insert == self.BEFORE:
			self.format = '%(num)d%(str)s'
		else:
			# TODO better error handling.
			print "Error: Unknown insertion mode."
		self.start = start
		self.current = self.start
		self.interval = interval
		
	def modifyPart(self, part):
		"""For each marked part in the current string this method is called.
		   It must return the altered version of the string. The reset method
		   is not called between invocations of this method."""
		res = self.format % {'str' : part, 'num' : self.current}
		self.current = self.current + self.interval	
		return res
	

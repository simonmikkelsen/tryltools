import unittest, sr

class SearchTest(unittest.TestCase):
	def testSearch(self):
		search = sr.Search("needle")
		search.execute("needle in a haystack with needleneedles in it.")
		self.assertEqual(search.results[0].startindex, 0)
		self.assertEqual(search.results[1].startindex, 26)
		self.assertEqual(search.results[2].startindex, 32)
		self.assertEqual(search.results[0].value, "needle")
		self.assertEqual(search.results[1].value, "needle")
		self.assertEqual(search.results[2].value, "needle")

class ReplaceTest(unittest.TestCase):
	def testReplace(self):
		search = sr.StringModifier()
		search.results = [sr.Result(4, 4, "needle"), sr.Result(7, 7, "needle")]
		repl = sr.Insert(".")
		self.assertEqual(repl.execute("findthedots", search), "find.the.dots")

class SRTest(unittest.TestCase):
	def testCombinedWithManager(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Search(" "))
		cmdMgr.add(sr.Delete())
		cmdMgr.add(sr.Insert("--"))
		self.assertEqual(cmdMgr.execute("This is text too  "), "This--is--text--too----")
	def testCombinedWithDoubleReplace(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Search(" "))
		cmdMgr.add(sr.Delete())
		cmdMgr.add(sr.Insert("--"))
		cmdMgr.add(sr.Insert(".."))
		self.assertEqual(cmdMgr.execute("This is text too  "), "This--..is--..text--..too--..--..")

	def testCombinedManually(self):
		search = sr.Search(" ")
		searchRes = search.execute("This is text too")

		delete = sr.Delete()
		deleteRes = delete.execute(searchRes, search)
		self.assertEqual(delete.results[0].startindex, 4)
		self.assertEqual(delete.results[1].startindex, 6)
		self.assertEqual(delete.results[2].startindex, 10)
		self.assertEqual(deleteRes, "Thisistexttoo")

		replace = sr.Insert(".")
		self.assertEqual(replace.execute(deleteRes, delete), "This.is.text.too")
class AppendTest(unittest.TestCase):
	def testAppend(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Append())
		cmdMgr.add(sr.Insert("-more"))
		self.assertEqual(cmdMgr.execute("Text.txt"), "Text-more.txt")
	def testAppendWithReplace(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Append())
		cmdMgr.add(sr.Insert("-more"))
		cmdMgr.add(sr.Insert("-stuff"))
		self.assertEqual(cmdMgr.execute("Text.txt"), "Text-more-stuff.txt")

	def testAppendExtension(self):
		cmdMgr = sr.CmdManager()
		appender = sr.Append()
		appender.setAppendExtension(True)
		cmdMgr.add(appender)
		cmdMgr.add(sr.Insert("-more"))
		self.assertEqual(cmdMgr.execute("Text.txt"), "Text.txt-more")
class IndirectPartModifierTest(unittest.TestCase):
	"""Tests classes that uses the part modifier."""
	def testLower(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Search("M"))
		cmdMgr.add(sr.Lowercase())
		self.assertEqual(cmdMgr.execute("I Love my Mom"), "I Love my mom")
	def testLowerEverything(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Everything())
		cmdMgr.add(sr.Lowercase())
		self.assertEqual(cmdMgr.execute("I Love my Mom"), "i love my mom")

	def testLowerMore(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Search("MAN"))
		cmdMgr.add(sr.Lowercase())
		self.assertEqual(cmdMgr.execute("MAN, I Love my Mom"), "man, I Love my Mom")
	def testUpperWithInsert(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Search("man"))
		cmdMgr.add(sr.Uppercase())
		cmdMgr.add(sr.Insert(" dude"))
		self.assertEqual(cmdMgr.execute("man, I Love my Mom"), "MAN dude, I Love my Mom")
		
class NumberingTest(unittest.TestCase):
	def testAfter(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Search("MAN "))
		cmdMgr.add(sr.Numbering(1, 1, sr.Numbering.AFTER))
		self.assertEqual(cmdMgr.execute("Counted MAN "), "Counted MAN 1")
		self.assertEqual(cmdMgr.execute("Counted MAN "), "Counted MAN 2")
		
	def testBefore(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Search(" MAN"))
		cmdMgr.add(sr.Numbering(1, 1, sr.Numbering.BEFORE))
		self.assertEqual(cmdMgr.execute("Counted  MAN"), "Counted 1 MAN")
		self.assertEqual(cmdMgr.execute("Counted  MAN"), "Counted 2 MAN")
	def testNegative(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Search(" MAN"))
		cmdMgr.add(sr.Numbering(1, -2, sr.Numbering.BEFORE))
		self.assertEqual(cmdMgr.execute("Counted  MAN"), "Counted 1 MAN")
		self.assertEqual(cmdMgr.execute("Counted  MAN"), "Counted -1 MAN")
	def testMultiNegative(self):
		cmdMgr = sr.CmdManager()
		cmdMgr.add(sr.Search(" MAN"))
		cmdMgr.add(sr.Numbering(3, -4, sr.Numbering.BEFORE))
		self.assertEqual(cmdMgr.execute("Counted  MAN"), "Counted 3 MAN")
		self.assertEqual(cmdMgr.execute("Counted  MAN"), "Counted -1 MAN")
		self.assertEqual(cmdMgr.execute("Counted  MAN"), "Counted -5 MAN")
		self.assertEqual(cmdMgr.execute("Counted  MAN"), "Counted -9 MAN")
if __name__ == "__main__":
	unittest.main()

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
		
if __name__ == "__main__":
	unittest.main()

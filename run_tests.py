from camelCase import camelCase
import unittest

class TestCamelCase(unittest.TestCase):
    def test_normal(self):
        tstStr = "plugin-packager"
        print "Testing \'%s\'"%tstStr
        self.assertEqual(camelCase(tstStr,'-'),"pluginPackager")
    def test_beginging(self):
        tstStr = "----plugin-packager"
        print "Testing \'%s\'"%tstStr
        self.assertEqual(camelCase(tstStr,'-'),"pluginPackager")
    def test_endinging(self):
        tstStr = "plugin-packager---"
        print "Testing \'%s\'"%tstStr
        self.assertEqual(camelCase(tstStr,'-'),"pluginPackager")
    def test_heads(self):
        tstStr = "-plugin-packager---"
        print "Testing \'%s\'"%tstStr
        self.assertEqual(camelCase(tstStr,'-'),"pluginPackager")
    def test_hole(self):
        tstStr = "-plugin- packager---"
        print "Testing \'%s\'"%tstStr
        self.assertEqual(camelCase(tstStr,'-'),"pluginPackager")

if __name__=="__main__":
    unittest.main()

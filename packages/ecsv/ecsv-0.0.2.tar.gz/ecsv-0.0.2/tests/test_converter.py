import unittest
import sys
import os
sys.path.append(os.path.join('/', os.path.relpath('src', '/')))
input_files_dir = os.path.join('/', os.path.relpath('tests/input_files', '/'))
from ecsv.Converter import Converter

class testIntoHtmlForm(unittest.TestCase):
    def test_1(self):
        result = Converter(input_files_dir + "/test1.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Title</th></tr></form></table>"
        self.assertEqual(result, expected)
    def test_2(self):
        result = Converter(input_files_dir + "/test2.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Title</th></tr><tr><td><label for='Name' name='Name'>Name</label></td><td><input id='Name' type='text'/></td></tr></form></table>"
        self.assertEqual(result, expected)
    def test_3(self):
        result = Converter(input_files_dir + "/test3.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Title</th></tr><tr><td><label for='Name' name='Name'>Name</label></td><td><input id='Name' type='text'/></td><td><label for='Age' name='Age'>Age</label></td><td><input id='Age' type='text'/></td></tr></form></table>"
        self.assertEqual(result, expected)
    def test_4(self):
        result = Converter(input_files_dir + "/test4.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Title</th></tr><tr><td><label for='Temperature' name='Temperature'>Temperature</label></td><td><input id='Temperature' type='text'/></td><td><label for='°C' name='°C'>°C</label></td></tr></form></table>"
        self.assertEqual(result, expected)
    def test_5(self):
        result = Converter(input_files_dir + "/test5.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Title</th></tr><tr><td><label for='Test No.' name='Test No.'>Test No.</label></td><td><label for='Tests' name='Tests'>Tests</label></td></tr><tr><td><label for='1' name='1'>1</label></td><td><input id='1' type='text'/></td></tr><tr><td><label for='2' name='2'>2</label></td><td><input id='2' type='text'/></td></tr><tr><td><label for='3' name='3'>3</label></td><td><input id='3' type='text'/></td></tr><tr><td><label for='4' name='4'>4</label></td><td><input id='4' type='text'/></td></tr><tr><td><label for='5' name='5'>5</label></td><td><input id='5' type='text'/></td></tr></form></table>"
        self.assertEqual(result, expected)
    def test_6(self):
        result = Converter(input_files_dir + "/test6.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Title</th></tr><tr><td><label for='Comments' name='Comments'>Comments</label></td></tr><tr><td><input id='Comments' type='text'/></td></tr></form></table>"
        self.assertEqual(result, expected)
    def test_7(self):
        result = Converter(input_files_dir + "/test7.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Title</th></tr><tr><td></td><td><label for='Notes' name='Notes'>Notes</label></td></tr><tr><td></td><td><input id='Notes' type='text'/></td></tr></form></table>"
        self.assertEqual(result, expected)
    def test_8(self):
        result = Converter(input_files_dir + "/test8.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Title</th></tr><tr><td><label for='Address' name='Address'>Address</label></td><td><label for='City' name='City'>City</label></td><td><label for='State' name='State'>State</label></td><td><label for='Country' name='Country'>Country</label></td><td><label for='Zip' name='Zip'>Zip</label></td></tr><tr><td><input id='Address' type='text'/></td><td><input id='City' type='text'/></td><td><input id='State' type='text'/></td><td><input id='Country' type='text'/></td><td><input id='Zip' type='text'/></td></tr></form></table>"
        self.assertEqual(result, expected)
    def test_9(self):
        result = Converter(input_files_dir + "/test9.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Hanging Around</th></tr></form></table>"
        self.assertEqual(result, expected)
    def test_10(self):
        result = Converter(input_files_dir + "/test10.csv").into_HTML_Form()
        expected = "<table><form><tr><th>Title</th></tr><tr><td><label for='Name' name='Name'>Name</label></td><td><label for='Age' name='Age'>Age</label></td><td></td></tr><tr><td><input id='Name' type='text'/></td><td><input id='Age' type='text'/></td><td></td></tr><tr><td><label for='Played' name='Played'>Played</label></td><td><input id='Played' type='text'/></td><td><label for='games' name='games'>games</label></td></tr><tr><td><label for='Height' name='Height'>Height</label></td><td><input id='Height' type='text'/></td><td><label for='meters' name='meters'>meters</label></td></tr><tr><td><label for='Blocks Per Game' name='Blocks Per Game'>Blocks Per Game</label></td><td><input id='Blocks Per Game' type='text'/></td><td></td></tr></form></table>"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()


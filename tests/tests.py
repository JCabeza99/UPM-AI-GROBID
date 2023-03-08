import unittest
from upm_ai_grobid import mama_papers
import xml.etree.ElementTree as ET


class TestProject(unittest.TestCase):
    def test_getAbstract(self):
        with open("test.xml") as test:
            self.assertNotEqual(mama_papers.getAbstract(ET.parse(test).getroot()),"")
    def test_getFigures(self):
        with open("test.xml") as test:
            self.assertEqual(mama_papers.getFigures(ET.parse(test).getroot()),0)
    def test_getLinks(self):
        with open("test.xml") as test:
            self.assertEqual(mama_papers.getLinks(ET.parse(test).getroot()),"") 
    def test_getAbstract2(self):
        with open("test1.xml") as test:
            self.assertEqual(mama_papers.getAbstract(ET.parse(test).getroot()),"")
    def test_getFigures2(self):
        with open("test1.xml") as test:
            self.assertEqual(mama_papers.getFigures(ET.parse(test).getroot()),0)
    def test_getLinks2(self):
        with open("test1.xml") as test:
            self.assertEqual(mama_papers.getLinks(ET.parse(test).getroot()),"") 
        
        
if __name__ == '__main__':
    unittest.main()
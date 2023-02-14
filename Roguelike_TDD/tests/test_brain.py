import unittest
from unittest.mock import patch
from Roguelike_TDD.src.brain import *
from Roguelike_TDD.src.options import *


class BrainTetCase(unittest.TestCase):
    
    def test_make_brain_object(self):
        brain = Brain()
        self.assertIsNotNone(brain)
    
    def test_generate_object_by_char(self):
        brain = Brain()
        self.assertIsInstance(brain.recognize(EMPTY), Empty)
        self.assertIsInstance(brain.recognize(TREE), Tree)
        self.assertIsInstance(brain.recognize(STONE), Stone)
        self.assertIsInstance(brain.recognize(LETTER), Letter)
        self.assertIsInstance(brain.recognize(TREASURE), Treasure)
    
    def test_empty_object(self):
        object = Empty()
        self.assertIsInstance(object, KnowledgeAbout)
        self.assertEqual(object.message(), MESSAGE_EMPTY)
        self.assertEqual(object.can_do(), [])
        self.assertFalse(object.it_barier())
    
    def test_tree_object(self):
        object = Tree()
        self.assertIsInstance(object, KnowledgeAbout)
        self.assertEqual(object.message(), MESSAGE_TREE)
        self.assertEqual(object.can_do(), [HACK])
        self.assertTrue(object.it_barier())
    def test_stone_object(self):
        object = Stone()
        self.assertIsInstance(object, KnowledgeAbout)
        self.assertIsInstance(object, KnowledgeAbout)
        self.assertEqual(object.message(), MESSAGE_STONE)
        self.assertEqual(object.can_do(), [])
        self.assertTrue(object.it_barier())
    
    def test_letter_object(self):
        object = Letter()
        self.assertIsInstance(object, KnowledgeAbout)
        self.assertEqual(object.message(), MESSAGE_LETTER)
        self.assertEqual(object.can_do(), [READ])
        self.assertTrue(object.it_barier())
    
    def test_treasure_object(self):
        object = Treasure()
        self.assertIsInstance(object, KnowledgeAbout)
        self.assertEqual(object.message(), MESSAGE_TREASURE)
        self.assertEqual(object.can_do(), [PICK_UP])
        self.assertTrue(object.it_barier())


if __name__ == "__main__":
    unittest.main()

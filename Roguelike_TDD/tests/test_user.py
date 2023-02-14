import unittest
from random import randint
from unittest.mock import patch

import src.user
from src.brain import *
from src.options import *
from src.user import User


class UserTestCase(unittest.TestCase):
    
    def tests_make_user_object(self):
        name = "UserName"
        user = User(name)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, name)
        self.assertEqual(user.action, '')
    
    def test_user_has_inventory(self):
        user = User("UserName")
        self.assertIsInstance(user.inventory, list)
        self.assertEqual(len(user.inventory), 0)
    
    def test_user_has_health(self):
        user = User("UserName")
        self.assertEqual(user.health, MAX_USER_HEALTH)
    
    def test_user_has_barain(self):
        user = User("TestUser_Name")
        self.assertIsInstance(user.brain, Brain)
    
    def test_get_user_default_position(self):
        user = User("TestUser_Name")
        position = user.get_position()
        self.assertIsInstance(position, list)
        self.assertEqual(len(position), 2)
        self.assertEqual(position, [-1, -1])
        self.assertEqual(user.direction, DIRECTION_UP)
    
    def test_user_put_item_to_inventory(self):
        user = User("TestUser_Name")
        self.assertEqual(user.inventory.count(TREASURE), 0)
        user.to_inventory(TREASURE)
        self.assertEqual(user.inventory.count(TREASURE), 1)
    
    def test_user_has_items(self):
        user = User("TestUser_Name")
        self.assertTrue(user.has(0, TREASURE))
        self.assertEqual(user.inventory.count(TREASURE), 0)
        
        self.assertFalse(user.has(1, TREASURE))
        user.to_inventory(TREASURE)
        self.assertTrue(user.has(1, TREASURE))
    
    def test_user_is_dead(self):
        user = User("TestUser_Name")
        self.assertFalse(user.is_dead())
        
        user.health = 0
        self.assertTrue(user.is_dead())
    
    @patch("src.map.Map")
    def test_user_see(self, MockMap):
        user = User("TestUser_Name")
        attrs = {"get_in_direction.return_value": TREE}
        MockMap.configure_mock(**attrs)
        self.assertEqual(user.see(MockMap), TREE)
    
    @patch("src.map.Map")
    def test_place_on_map(self, MockMap):
        x, y = randint(0, 10), randint(0, 20)
        user = User("TestUser_Name")
        attrs = {"get_empty_random_position.return_value": (x, y)}
        MockMap.configure_mock(**attrs)
        user.place_on(MockMap)
        self.assertEqual(user.position, [x, y])
        MockMap.put.assert_called_with(x, y, USER)
    
    def test_can_walk_to(self):
        user = User("TestUser_Name")
        knowledge_about = Empty()
        self.assertEqual(user.can_walk_to(DIRECTION_UP, knowledge_about),
                         [DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT])
        
        knowledge_about = Stone()
        self.assertEqual(user.can_walk_to(DIRECTION_UP, knowledge_about),
                         [DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT])
    
    # @unittest.skip('Рефакторинг')
    @patch("src.user.User")
    def test_user_do(self, user):
        # user = User("TestUser_Name")
        knowledge_about = Treasure()
        user.action = DIRECTION_UP  # knowledge_about.can_do()[0]
        user.can_walk_to.return_value = [DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT]
        user.do(map, knowledge_about)
        self.assertIn(user.action, user.can_walk_to(user.action, knowledge_about))
        user.move.assert_called_once()


if __name__ == "__main__":
    unittest.main()

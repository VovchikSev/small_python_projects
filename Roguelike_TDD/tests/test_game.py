import unittest
from unittest.mock import patch

import src.map
from src.game import Game, GameOverException
from src.map import Map
from src.options import *
from src.user import User


class GameTetCase(unittest.TestCase):
    def test_make_game_object(self):
        game = Game()
        self.assertIsNotNone(game)
        self.assertIsInstance(game.user, User)
    
    def test_init_map(self):
        game = Game()
        self.assertIsNotNone(game.map)
        self.assertIsInstance(game.map, Map)
    
    @patch("src.map.Map")
    def test_map_generation(self, MockMap):
        game = Game()
        game.map = MockMap
        game.generate_map(20, 10, EMPTY)
        game.map.generate.assert_called_with(20, 10, EMPTY)
    
    @patch("src.map.Map")
    def tests_place_items_on_map(self, MockMap):
        game = Game()
        game.map = MockMap
        game.generate_map(20, 10, EMPTY)
        game.place_on_map(20, TREE)
        game.map.place.assert_called_with(20, TREE)
    
    @patch("src.user.User")
    @patch("src.map.Map")
    def test_game_turn(self, MockUser, MockMap):
        game = Game()
        game.map = MockMap
        game.user = MockUser
        attrs = {"is_dead.return_value": False, "has.return_value": False}
        game.user.configure_mock(**attrs)
        game.turn()
        game.map.show.assert_called_once()
        game.user.show_info.assert_called_with(game.map)
    
    @patch("src.map.Map")
    @patch("src.user.User")
    def test_game_turn_raise_exception_if_user_dead(self, MockUser, MockMap):
        game = Game()
        game.map = MockMap
        game.user = MockUser
        attrs = {"is_dead.return_value": True, "has.return_value": False}
        game.user.configure_mock(**attrs)
        with self.assertRaises(GameOverException):
            game.turn()
    
    @patch("src.map.Map")
    @patch("src.user.User")
    def test_game_turn_raise_exception_if_users_inventory_full(self, MockUser, MockMap):
        game = Game()
        game.map = MockMap
        game.user = MockUser
        attrs = {"is_dead.return_value": False, "has.return_value": True}
        game.user.configure_mock(**attrs)
        with self.assertRaises(GameOverException):
            game.turn()

    @patch("src.user.User")
    def test_game_not_over_if_user_live_and_inventory_empty(self, MockUser):
        game = Game()
        game.user = MockUser
        attrs = {"is_dead.return_value": False, "has.return_value": False}
        game.user.configure_mock(**attrs)
        self.assertFalse(game.user.is_dead())
    
    @patch("src.user.User")
    def test_game_is_over_if_user_dead(self, MockUser):
        game = Game()
        game.user = MockUser
        attrs = {"is_dead.return_value": True, "has.return_value": False}
        game.user.configure_mock(**attrs)
        self.assertTrue(game.is_over())

    @patch("src.user.User")
    def test_game_is_over_if_inventory_full(self, MockUser):
        game = Game()
        game.user = MockUser
        attrs = {"is_dead.return_value": False, "has.return_value": True}
        game.user.configure_mock(**attrs)
        self.assertTrue(game.is_over())

    # @patch("src.user.User")
    # def test_place_user_on_map(self, MockUser):
    #     x, y = 10, 20
    #     game = Game()
    #     game.user = MockUser
    #     game.user.place_on_map()
    #     game.user.move.assert_called(x, y)
    #
if __name__ == "__main__":
    unittest.main()

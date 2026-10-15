import unittest
from card_table.structure import GameTable

class GameTableTests(unittest.TestCase):
    def setUp(self):
        self.table = GameTable()

    def test_single_player_links_to_itself(self):
        player = self.table.insert_at_start("Luna")
        self.assertIs(player.right_neighbor, player)
        self.assertIs(player.left_neighbor, player)
        self.assertTrue(self.table.validate_integrity())

    def test_insert_and_traverse_both_directions(self):
        for name in ["Ana", "Beto", "Cami"]:
            self.table.insert_at_end(name)
        self.assertEqual(self.table.traverse_right(), ["Ana", "Beto", "Cami"])
        self.assertEqual(self.table.traverse_left(), ["Ana", "Cami", "Beto"])

    def test_insert_at_middle(self):
        self.table.insert_at_end("Ana")
        self.table.insert_at_end("Cami")
        self.table.insert_at_position(2, "Beto")
        self.assertEqual(self.table.traverse_right(), ["Ana", "Beto", "Cami"])

    def test_turns_reverse_and_skip(self):
        for name in ["Ana", "Beto", "Cami", "Dani"]:
            self.table.insert_at_end(name)
        self.assertEqual(self.table.next_turn().name, "Beto")
        self.assertEqual(self.table.previous_turn().name, "Ana")
        self.assertEqual(self.table.skip_turns(2).name, "Cami")
        self.assertEqual(self.table.skip_turns(-1).name, "Beto")

    def test_remove_players(self):
        self.table.insert_at_end("Ana")
        self.table.insert_at_end("Beto")
        self.table.remove_player("Ana")
        self.assertEqual(self.table.traverse_right(), ["Beto"])
        self.assertIs(self.table.current_player.right_neighbor, self.table.current_player)
        self.table.remove_player("Beto")
        self.assertEqual(self.table.player_count, 0)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            self.table.insert_at_start(" ")
        self.table.insert_at_end("Ana")
        with self.assertRaises(ValueError):
            self.table.insert_at_end("ana")
        with self.assertRaises(ValueError):
            self.table.insert_at_position(3, "Beto")

if __name__ == "__main__":
    unittest.main()

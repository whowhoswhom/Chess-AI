import os
import sys
import types
import unittest

# Ensure modules from the src directory can be imported when running as a module
SRC_DIR = os.path.dirname(__file__)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Provide a minimal pygame stub so that sound.py can be imported without the
# real pygame dependency installed.
if 'pygame' not in sys.modules:
    class _DummySound:
        def __init__(self, *args, **kwargs):
            pass

        def play(self, *args, **kwargs):
            pass

    dummy_mixer = types.SimpleNamespace(Sound=_DummySound)
    sys.modules['pygame'] = types.SimpleNamespace(mixer=dummy_mixer)

from board import Board
from move import Move
from square import Square


class TestBoardUndoMove(unittest.TestCase):
    """Test undo_move restores board state."""

    def test_undo_restores_piece_positions(self):
        board = Board()

        piece = board.squares[6][4].piece
        initial_square = board.squares[6][4]
        final_square = board.squares[4][4]
        move = Move(initial_square, final_square)

        board.move(piece, move, testing=True)

        self.assertIs(board.squares[6][4].piece, None)
        self.assertIs(board.squares[4][4].piece, piece)
        self.assertEqual(len(board.move_history), 1)
        self.assertTrue(piece.moved)

        board.undo_move()

        self.assertIs(board.squares[6][4].piece, piece)
        self.assertIs(board.squares[4][4].piece, None)
        self.assertEqual(len(board.move_history), 0)
        self.assertFalse(piece.moved)
        self.assertIsNone(board.last_move)


if __name__ == '__main__':
    unittest.main()

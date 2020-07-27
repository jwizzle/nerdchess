from nerdchess import pieces


class BoardRules():
    """Applies different boardrules.

    Parameters:
        move: The move to check against
        board: The board to check against

    Attributes:
        move: The move we're checking
        board: The board we're checking
        valid: Is the checked move valid?
        origin: The origin square of the move
        destination: The destination square of the move
        piece: The piece being moved
    """

    def __init__(self, move, board):
        self.move = move
        self.board = board
        self.valid = True
        (self.origin,
         self.destination) = self.move.get_origin_destination(self.board)
        self.piece = self.origin.occupant
        self.apply()

    def apply(self):
        """ Apply boardrules based on the moved piece. """
        if isinstance(self.piece, pieces.Pawn):
            self.__pawn_rules()
        if not isinstance(self.piece, pieces.Knight):
            self.__blocking_pieces()
        self.__self_checking()

    def __pawn_rules(self):
        """ Rules to apply to pawns only. """
        if self.move.horizontal == 1:
            # If we're going horizontal, are we at least capturing?
            if not self.destination.occupant:
                d_letter = self.move.destination[0]
                o_number = int(self.move.origin[1])
                # If not, is it at least en passant?
                if not isinstance(
                        self.board.squares[d_letter][o_number].occupant,
                        pieces.Pawn):
                    self.valid = False

    def __blocking_pieces(self):
        """ Check if the move is being blocked. """
        for square in self.move.squares_between():
            c = square[0]
            i = int(square[1])
            if self.board.squares[c][i].occupant:
                self.valid = False

    def __self_checking(self):
        """ Check if the move puts the player itself in check. """
        newboard = self.move.new_board(self.board)
        if newboard.is_check() == self.piece.color:
            self.valid = False

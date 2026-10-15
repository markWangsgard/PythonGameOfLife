from __future__ import annotations


class Cell:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Board:
    living_cells: dict[tuple[int, int], Cell]

    def __init__(self, alive_cells: list[Cell]):
        self.living_cells = {}
        for c in alive_cells:
            self.living_cells[(c.x, c.y)] = c

    def print(self) -> None:
        for c in self.living_cells.values():
            print(f"{{{c.x},{c.y}}}")

    def get_or_make_cell(self, x: int, y: int) -> Cell:
        if (x, y) in self.living_cells:
            return self.living_cells[(x, y)]
        else:
            return Cell(x, y)

    def get_cell_neighbors(self, cell: Cell) -> list[Cell]:
        return [
            self.get_or_make_cell(cell.x + 1, cell.y + 1),
            self.get_or_make_cell(cell.x + 1, cell.y),
            self.get_or_make_cell(cell.x + 1, cell.y - 1),
            self.get_or_make_cell(cell.x - 1, cell.y + 1),
            self.get_or_make_cell(cell.x - 1, cell.y),
            self.get_or_make_cell(cell.x - 1, cell.y - 1),
            self.get_or_make_cell(cell.x, cell.y + 1),
            self.get_or_make_cell(cell.x, cell.y - 1),
        ]

    def count_alive_cell_neighbors(self, cell: Cell) -> int:
        return sum(
            1 for c in self.get_cell_neighbors(cell)
            if (c.x, c.y) in self.living_cells
        )

    def cell_lives(self, cell: Cell) -> bool:
        if ((cell.x, cell.y) in self.living_cells and self.count_alive_cell_neighbors(cell) == 2) or self.count_alive_cell_neighbors(cell) == 3:
            return True
        else:
            return False

    def advance_next_gen(self) -> None:
        potential_cells = {}
        for cell in self.living_cells.values():
            for c in self.get_cell_neighbors(cell):
                potential_cells[(c.x, c.y)] = c
        self.living_cells = {
            key: c for key, c in potential_cells.items() if self.cell_lives(c)
        }

def simulate(b: Board, iterations: int) -> Board:
    for i in range(iterations):
        b.advance_next_gen()
    return b

def main() -> None:
    print("Hello from pythongameoflife!")


    print("Original Board")
    my_board = Board([Cell(1, 0), Cell(2, 1), Cell(0, 2), Cell(1, 2), Cell(2, 2)])
    my_board.print()
    simulate(my_board, 100000)
    my_board.print()


if __name__ == "__main__":
    main()
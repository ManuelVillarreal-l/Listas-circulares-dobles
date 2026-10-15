"""Circular doubly linked list specialized for a card-game table."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass(eq=False)
class Player:
    """A participant connected to the player on either side."""
    name: str
    favorite_card: str = "Sin preferencia"
    right_neighbor: Optional["Player"] = None
    left_neighbor: Optional["Player"] = None

    def __post_init__(self):
        self.name = self.name.strip()
        self.favorite_card = self.favorite_card.strip() or "Sin preferencia"
        if not self.name:
            raise ValueError("El nombre del jugador no puede estar vacío.")

class GameTable:
    """Manage players in a circular structure with links in both directions."""
    def __init__(self):
        self.current_player: Optional[Player] = None
        self.player_count = 0

    def _validate_new_name(self, name: str) -> str:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Escribe un nombre válido.")
        if self.find_player(clean_name):
            raise ValueError(f"Ya existe un jugador llamado '{clean_name}'.")
        return clean_name

    def insert_at_start(self, name: str, favorite_card: str = "Sin preferencia") -> Player:
        new_player = Player(self._validate_new_name(name), favorite_card)
        if self.current_player is None:
            new_player.right_neighbor = new_player
            new_player.left_neighbor = new_player
            self.current_player = new_player
        else:
            last_player = self.current_player.left_neighbor
            new_player.right_neighbor = self.current_player
            new_player.left_neighbor = last_player
            last_player.right_neighbor = new_player
            self.current_player.left_neighbor = new_player
            self.current_player = new_player
        self.player_count += 1
        self.validate_integrity()
        return new_player

    def insert_at_end(self, name: str, favorite_card: str = "Sin preferencia") -> Player:
        if self.current_player is None:
            return self.insert_at_start(name, favorite_card)
        new_player = Player(self._validate_new_name(name), favorite_card)
        last_player = self.current_player.left_neighbor
        new_player.right_neighbor = self.current_player
        new_player.left_neighbor = last_player
        last_player.right_neighbor = new_player
        self.current_player.left_neighbor = new_player
        self.player_count += 1
        self.validate_integrity()
        return new_player

    def insert_at_position(self, position: int, name: str, favorite_card: str = "Sin preferencia") -> Player:
        if not isinstance(position, int) or position < 1 or position > self.player_count + 1:
            raise ValueError(f"La posición debe estar entre 1 y {self.player_count + 1}.")
        if position == 1:
            return self.insert_at_start(name, favorite_card)
        if position == self.player_count + 1:
            return self.insert_at_end(name, favorite_card)
        new_player = Player(self._validate_new_name(name), favorite_card)
        target = self.current_player
        for _ in range(position - 1):
            target = target.right_neighbor
        previous_player = target.left_neighbor
        new_player.left_neighbor = previous_player
        new_player.right_neighbor = target
        previous_player.right_neighbor = new_player
        target.left_neighbor = new_player
        self.player_count += 1
        self.validate_integrity()
        return new_player

    def remove_player(self, name: str) -> Player:
        target = self.find_player(name)
        if target is None:
            raise KeyError(f"No existe el jugador '{name}'.")
        if self.player_count == 1:
            self.current_player = None
        else:
            target.left_neighbor.right_neighbor = target.right_neighbor
            target.right_neighbor.left_neighbor = target.left_neighbor
            if target is self.current_player:
                self.current_player = target.right_neighbor
        target.right_neighbor = None
        target.left_neighbor = None
        self.player_count -= 1
        self.validate_integrity()
        return target

    def find_player(self, name: str) -> Optional[Player]:
        if self.current_player is None:
            return None
        search_name = name.strip().casefold()
        cursor = self.current_player
        for _ in range(self.player_count):
            if cursor.name.casefold() == search_name:
                return cursor
            cursor = cursor.right_neighbor
        return None

    def _traverse(self, direction: str) -> list[str]:
        names = []
        if self.current_player is None:
            return names
        cursor = self.current_player
        for _ in range(self.player_count):
            names.append(cursor.name)
            cursor = getattr(cursor, direction)
        return names

    def traverse_right(self) -> list[str]:
        return self._traverse("right_neighbor")

    def traverse_left(self) -> list[str]:
        return self._traverse("left_neighbor")

    def next_turn(self) -> Player:
        if self.current_player is None:
            raise ValueError("Agrega al menos un jugador para iniciar la partida.")
        self.current_player = self.current_player.right_neighbor
        return self.current_player

    def previous_turn(self) -> Player:
        if self.current_player is None:
            raise ValueError("Agrega al menos un jugador para iniciar la partida.")
        self.current_player = self.current_player.left_neighbor
        return self.current_player

    def skip_turns(self, steps: int) -> Player:
        if self.current_player is None:
            raise ValueError("Agrega al menos un jugador para iniciar la partida.")
        if not isinstance(steps, int):
            raise ValueError("El salto debe ser un número entero.")
        direction = "right_neighbor" if steps >= 0 else "left_neighbor"
        for _ in range(abs(steps) % max(self.player_count, 1)):
            self.current_player = getattr(self.current_player, direction)
        return self.current_player

    def get_summary(self) -> str:
        if self.player_count == 0:
            return "La mesa está vacía."
        return "  ↔  ".join(self.traverse_right()) + "  ↻"

    def validate_integrity(self) -> bool:
        """Raise AssertionError if any active player has broken links."""
        if self.player_count == 0:
            if self.current_player is not None:
                raise AssertionError("La mesa vacía no debe tener jugador actual.")
            return True
        if self.current_player is None:
            raise AssertionError("Hay jugadores registrados pero no hay turno actual.")
        cursor = self.current_player
        visited = set()
        for _ in range(self.player_count):
            if cursor is None or cursor.right_neighbor is None or cursor.left_neighbor is None:
                raise AssertionError("Se encontró un enlace vacío dentro de la mesa.")
            if cursor.right_neighbor.left_neighbor is not cursor:
                raise AssertionError("Los enlaces derecha/izquierda no son recíprocos.")
            if cursor.left_neighbor.right_neighbor is not cursor:
                raise AssertionError("Los enlaces izquierda/derecha no son recíprocos.")
            visited.add(id(cursor))
            cursor = cursor.right_neighbor
        if cursor is not self.current_player or len(visited) != self.player_count:
            raise AssertionError("El círculo no cierra o la cantidad no coincide.")
        return True

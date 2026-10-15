"""Alternative command-line menu; all prompts are displayed in Spanish."""
from card_table.structure import GameTable

def run_console():
    table = GameTable()
    while True:
        print("""
========== MESA ARCANA ==========
1. Insertar jugador al inicio
2. Insertar jugador al final
3. Insertar jugador en posición
4. Eliminar jugador
5. Buscar jugador
6. Recorrer hacia la derecha
7. Recorrer hacia la izquierda
8. Avanzar turno
9. Reversa de turno
10. Saltar turnos
11. Mostrar mesa
0. Salir
""")
        option = input("Selecciona una opción: ").strip()
        try:
            if option == "1":
                table.insert_at_start(input("Nombre: "), input("Carta favorita / alias: "))
            elif option == "2":
                table.insert_at_end(input("Nombre: "), input("Carta favorita / alias: "))
            elif option == "3":
                position = int(input("Posición (1 = inicio): "))
                table.insert_at_position(position, input("Nombre: "), input("Carta favorita / alias: "))
            elif option == "4":
                table.remove_player(input("Nombre a eliminar: "))
            elif option == "5":
                player = table.find_player(input("Nombre a buscar: "))
                print(f"Encontrado: {player.name} | Carta favorita: {player.favorite_card}" if player else "Jugador no encontrado.")
            elif option == "6":
                print(" → ".join(table.traverse_right()))
            elif option == "7":
                print(" ← ".join(table.traverse_left()))
            elif option == "8":
                print("Turno actual:", table.next_turn().name)
            elif option == "9":
                print("Turno actual:", table.previous_turn().name)
            elif option == "10":
                print("Turno tras el salto:", table.skip_turns(int(input("Cantidad (+ derecha / - izquierda): "))).name)
            elif option == "11":
                print(table.get_summary())
            elif option == "0":
                print("¡Buena partida!")
                break
            else:
                print("Opción no válida.")
        except (ValueError, KeyError) as error:
            print(f"No se pudo completar: {error}")

if __name__ == "__main__":
    run_console()

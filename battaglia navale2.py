import random
from colorama import Fore, Back, Style, init
import time
import pygame

init(autoreset=True)
pygame.mixer.init()

def create_grid(size):
    grid = []
    for _ in range(size):
        grid.append([Fore.BLUE + "O" + Style.RESET_ALL] * size)
    return grid

def print_grid(grid):
    for row in grid:
        print(" ".join(row))

def place_ships(grid, ship_lengths):
    size = len(grid)
    ships = []
    for length in ship_lengths:
        while True:
            orientation = random.choice(["horizontal", "vertical"])
            if orientation == "horizontal":
                ship_row = random.randint(0, size - 1)
                ship_col = random.randint(0, size - length)
            else:
                ship_row = random.randint(0, size - length)
                ship_col = random.randint(0, size - 1)
            
            is_collision = False
            coords = []

            for i in range(length):
                if orientation == "horizontal":
                    if grid[ship_row][ship_col + i] != Fore.BLUE + "O" + Style.RESET_ALL:
                        is_collision = True
                        break
                    coords.append((ship_row, ship_col + i))
                else:
                    if grid[ship_row + i][ship_col] != Fore.BLUE + "O" + Style.RESET_ALL:
                        is_collision = True
                        break
                    coords.append((ship_row + i, ship_col))
            
            if not is_collision:
                break
        
        ships.append({
            "coords":coords,
            "length": length,
            "hits": 0
        })
        
        for coord in coords:
            grid[coord[0]][coord[1]] = Fore.GREEN + "X" + Style.RESET_ALL
    
    return ships

def computer_turn(grid, previous_guesses):
    size = len(grid)
    while True:
        guess_row = random.randint(0, size - 1)
        guess_col = random.randint(0, size - 1)
        if (guess_row, guess_col) not in previous_guesses:
            previous_guesses.add((guess_row, guess_col))
            return guess_row, guess_col

def main():
    size = 10
    ship_lengths = [2, 2, 2, 2, 3, 3, 3, 4, 4, 6]
    ship_name = ["Nave d\'assalto", "Sottomarino", "Crociere", "Corazzata", "Portaerei"]
    computer_grid = create_grid(size)
    player_grid = create_grid(size)

    def print_player_grid_with_coordinates(grid):
        # Etichette personalizzate per le colonne
        column_labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        print("    " + " ".join(column_labels))  # Stampa le etichette delle colonne

        for i, row in enumerate(grid):
            # Formatta le etichette delle righe aggiungendo uno zero iniziale se necessario
            row_label = str(i + 1).rjust(2, "0")
            print(row_label + "  " + " ".join(row))  # Stampa il contenuto della riga

    print("Benvenuto a Battaglia Navale!")
    print("Posiziono le tue navi e del computer casualmente")
    #print_grid(player_grid)
    # Conto alla rovescia da 2 a 1
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)  # Pausa di 1 secondo
    
    pygame.mixer.music.load("battle.mp3")
    pygame.mixer.music.play(-1)

    player_ships = place_ships(player_grid, ship_lengths)
    print("Le tue navi sono posizionate!")

    computer_ships = place_ships(computer_grid, ship_lengths)
    print("Il computer ha posizionato le sue navi!")

    ship_lengths_remaining = [ship["length"] for ship in player_ships]
    computer_previous_guesses = set()
    num_guesses = 0

    computer_ships_remaining = len(ship_lengths)
    player_ships_remaining = len(ship_lengths)
    
    while len(ship_lengths_remaining) > 0:
        guess_row = int(input("Indovina la riga: ")) - 1
        guess_col = int(input("Indovina la colonna: ")) - 1

        if 0 <= guess_row < size and 0 <= guess_col < size:
            if computer_grid[guess_row][guess_col] == Fore.GREEN + "X" + Style.RESET_ALL:
                print("Congratulazioni! Hai colpito una nave del computer!")
                computer_grid[guess_row][guess_col] = Fore.RED + "!" + Style.RESET_ALL
                for ship in computer_ships: # è nuovo da qui
                                if (guess_row, guess_col) in ship["coords"]:
                                    ship["hits"] += 1
                                    if ship["hits"] == ship["length"]:
                                        print("Hai affondato una nave da", ship["length"], "del computer!")
                                        ship_lengths_remaining.remove(ship["length"])
                                        computer_ships_remaining -= 1  # Decrementa solo quando una nave viene affondata
                                        print("Al computer rimangono", computer_ships_remaining, "navi.")
                                        break
                num_guesses += 1
            else:
                print("Spiacente, hai colpito l'acqua.")
                num_guesses += 1

            #print("Griglia del computer:")
            #print_grid(computer_grid)

            print("La tua griglia:")
            print_player_grid_with_coordinates(player_grid)

            if len(ship_lengths_remaining) == 0:
                break

            computer_guess_row, computer_guess_col = computer_turn(player_grid, computer_previous_guesses)

            if player_grid[computer_guess_row][computer_guess_col] == Fore.GREEN + "X" + Style.RESET_ALL:
                print("Il computer ha colpito una tua nave!")
                player_grid[computer_guess_row][computer_guess_col] = Fore.RED + "!" + Style.RESET_ALL

                for ship in player_ships:
                     if (guess_row, guess_col) in ship["coords"]:
                        ship["hits"] += 1
                        if ship["hits"] == ship["length"]:
                            print("Il computer ha affondato una tua nave da", ship["length"], "!")
                            ship_lengths_remaining.remove(ship["length"])
                            player_ships_remaining -= 1  # Decrementa solo quando una nave viene affondata
                            print("Al computer rimangono", player_ships_remaining, "navi.")
                            break
            else:
                print("Il computer ha colpito l'acqua.")

            # Mostra solo le posizioni colpite e nell'acqua nella griglia del computer
            computer_display_grid = []
            for row in computer_grid:
                display_row = []
                for cell in row:
                    if cell == Fore.RED + "!" + Style.RESET_ALL or cell == Fore.BLUE + "O" + Style.RESET_ALL:
                        display_row.append(cell)
                    else:
                        display_row.append(Fore.BLUE + "O" + Style.RESET_ALL)
                computer_display_grid.append(display_row)

            print("Griglia del computer:")
            print_player_grid_with_coordinates(computer_display_grid)

            input("Premi invio per continuare...")  # Attendi l'input per procedere
        else:
            print("Coordinate non valide. Inserisci coordinate tra 1 e", size)

    print("Hai affondato tutte le navi del computer in " + str(num_guesses) + " tentativi!")
    pygame.mixer.music.stop()
if __name__ == "__main__":
    main()
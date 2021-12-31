# -*- coding: utf-8 -*-

import random
from collections import deque


# The BattleshipGame class establishes the basics of the game, such as the number of players, how the turns will play
# out, and the winning condition.
class BattleshipGame:

    # We create the game based on the number of players.
    def __init__(self, nop):
        # If there is one player we initialize the game with a computer as his opponent.
        if nop == 1:
            self.p = [Player("Player"), Computer("The Computer")]
        # Otherwise, we create two player objects.
        else:
            self.p = [Player("Player 1"), Player("Player 2")]

        # We establish the players as opponents so that they are able to attack each other when the game starts.
        self.p[0].set_rival(self.p[1])
        self.p[1].set_rival(self.p[0])

    # This method defines how the game will run.
    def play(self):
        # Both players start by positioning their boats on the board.
        self.p[0].position_ships()
        self.p[1].position_ships()

        # Once that's done, we output a message to signal the beggining of the game.
        input("Both admirals are ready for battle. Press enter to play... ")
        winner = False
        # We create a queue to store the turns.
        turn = deque()
        # We create an accumulator for the while loop.
        r = 0
        while r <= 100:
            # We append the players to our turns queue until we reach the maximum number of turns possible (100).
            turn.append("p1")
            turn.append("p2")
            r += 1
        # We create another while loop to change turns and verify the winner.
        while not winner:
            # Take a turn for the next player.
            if turn.pop() == "p1":
                winner = self.p[0].take_turn()
                # Check to see if Player 1 won.
                if winner:
                    print("Game over!", self.p[0].pname, "is the winner!")
            else:
                winner = self.p[1].take_turn()
                # Check to see if Player 2 won.
                if winner:
                    print("Game over!", self.p[1].pname, "is the winner!")

# The Board class is a 10*10 grid for both players.  The board has cells, each of which
# is set to one of four values:
# Your board view:
# Boat: A position with a boat. " B".
# Empty: A position with no boat. " _".
# Your opponents board view:
# Hit: A position has been attacked and a boat has been hit. "X"
# Miss: A position has been attacked but no ship was in that position."_O"

class Board:

    # Initialize the 10*10 grid.
    def __init__(self):
        self.grid = [[" _"] * 10 for i in range(10)]
        # The hit_shipcount counts the number of successful attacks. When it reaches 17 = gameover. 
        self.hit_shipcount = 0

    # Print the grid.
    def __str__(self):
        str_value = "  A B C D E F G H I J\n"  # "  0 1 2 3 4 5 6 7 8 9\n"
        for i in range(10):
            str_value += str(i)
            for j in range(10):
                str_value += self.grid[i][j]
            if i != 9:
                str_value += "\n"
        return str_value

    # Print your opponent's grid with boats hidden.
    def get_public_view(self):
        str_value = "  A B C D E F G H I J\n"  # "  0 1 2 3 4 5 6 7 8 9\n"
        for i in range(10):
            str_value += str(i)
            for j in range(10):
                if self.grid[i][j] == " B":
                    str_value += " _"
                else:
                    str_value += self.grid[i][j]
            if i != 9:
                str_value += "\n"
        return str_value

    # Adds a ship to the board. If that posotion is not available returns false.
    # A position must be inside the board and must not overlap with the other boats.
    def add_ship(self, boat):
        # Check the position is within range.
        width = 1
        height = 1
        if boat.direction == "v":
            height = boat.size
        else:
            width = boat.size

        # Computer
        if (boat.x < 0) or (boat.y < 0) or (boat.x + width > 10) or (boat.y + height > 10):
            return False

        # Check if the position is already occupied. 
        for x in range(width):
            for y in range(height):
                if self.grid[boat.y + y][boat.x + x] != " _":
                    return False

        # If board does not fit returns False. Position is valid.
        # Now update board with " B" to show boat.
        for x in range(width):
            for y in range(height):
                self.grid[boat.y + y][boat.x + x] = " B"
        return True

    # attack method records the attack in one precise position (x,y).
    def attack(self, x, y):
        # Check what is in that position.
        current_attack = self.grid[y][x]
        # Hit if there is a boat in the position selected.
        if current_attack == " B":
            self.grid[y][x] = " X"
            self.hit_shipcount += 1
            return True
        # Miss if there was not boat in that position.
        elif current_attack == " _":
            self.grid[y][x] = " O"
            return False
        # Ignore attack if the position has previously been attacked.
        else:
            return False

    # Checks all the boats have been sunk; hit_shipcount = 17.
    def loose(self):
        if self.hit_shipcount == 17:
            return True
        else:
            return False


# Boat class
class Boat:
    # Initialize the boat with a (boat_name, size).
    def __init__(self, boat_name, size):
        self.boat_name = boat_name
        self.size = size
        self.x = None
        self.y = None
        self.direction = None

    # (x,y) Top-left position of the boat. Depending on direction it extends down(v), right(h).
    def boat_position(self, x, y):
        self.x = x
        self.y = y

    # Boat direction vertical(v), horizontal(h).
    def set_direction(self, direction):
        self.direction = direction


# Player class
class Player:
    # Initialize the player with a (name).

    def __init__(self, pname):
        self.pname = pname
        self.board = Board()
        self.ships = [Boat("Aircraft Carrier", 5), Boat("Battleship", 4), Boat("Submarine", 3), Boat("Destroyer", 3),
                      Boat("Patrol Boat", 2)]
        self.rival = None
        self.log = [0, 0, 0]
        self.bulletsAvailable = self.game_difficulty()

    # Set the game difficulty; from (1 to 4). The smaller the easier!
    def game_difficulty(self):
        difficulty = ["1", "2", "3", "4"]
        selectLevel = input("Select the difficulty of the game (1, 2, 3, 4).Trust me start with an easy level if you"
                            " have not played before!. Note: Both players need to select the same difficulty!! ")
        while selectLevel not in difficulty:
            print("There are only four levels from 1 to 4")
        if selectLevel == "1":
            return 81
        elif selectLevel == "2":
            return 61
        elif selectLevel == "3":
            return 49
        else:
            return 34

    # Link player and opponent.
    def set_rival(self, rival):
        self.rival = rival

    # Position ships.
    def position_ships(self):
        input(self.pname + ": Time to position your fleet. Press enter to continue. ")

        # Position ships.
        for boat in self.ships:
            self.position_boat(boat)

        # Show the board after ships have been positioned.
        print("Your fleet is ready. This is your complete board:")
        print(self.board)

    # Positions one ship. Helper method for positionShips
    def position_boat(self, boat):
        # Show board before single ship positioned.
        print(self.board)
        print("Position a ", boat.boat_name, "of length", boat.size, "on the board.")
        # Ask user for direction of boat.
        direction = None
        while direction is None:
            direction = input("Select the direction of your ship? (v/h) ")
            if (direction != "v") and (direction != "h"):
                print("You must enter a 'v' or a 'h'.  Try again.")
                direction = None
        # Ask user for the position of the boat.
        shipLocation = None
        while shipLocation is None:
            try:
                shipLocation = input("Please enter the shipLocation. " +
                                     " In the form x,y (e.g., A,4): ")
                coordinates = shipLocation.split(",")
                changeValue = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
                x = changeValue[coordinates[0]]
                y = int(coordinates[1])
                boat.set_direction(direction)
                boat.boat_position(x, y)
                # Add the ship to the board.
                if not self.board.add_ship(boat):
                    # The boat was not succesfully added. Raise an exception to force the user try another position.
                    raise Exception
            except ValueError:
                print("You need to introduce a valid shipLocation. Try again.")
                shipLocation = None
            except:
                print("You must choose a shipLocation that is (a) on the board and (b) doesn't intersect" +
                      "with any other boats.")
                shipLocation = None

    # Single turn of the player.
    def take_turn(self):
        # Display both yours and opponent board.
        print(self.pname + "'s board:")
        print(self.board)
        print()
        print("Your view of " + self.rival.pname + "'s board:")
        print(self.rival.board.get_public_view())
        # Statistics for player.
        print(self.pname, "Statistics\nAttacks: ", self.log[0], "\tHits: ", self.log[1], "\tMisses: ",
              self.log[2], "\tMissilesLeft: ", self.bulletsAvailable)
        # Attack position.
        attackLocation = None
        while attackLocation is None:
            try:
                attackLocation = input("Enter your attack position.  Use the form x,y (e.g., B,3): ")
                coordinates = attackLocation.split(",")
                changeValue = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
                c1 = changeValue[coordinates[0]]
                c2 = int(coordinates[1])
                if (c1 < 0) or (c1 > 9) or (c2 < 0) or (c2 > 9):
                    raise Exception
                else:
                    break
            except:
                print("You need to enter a valid position in the form x,y where both x and y are integers in the range of " +
                      "0-9. Try again.")
                attackLocation = None

        # Make an attack.
        hit_flag = self.rival.board.attack(c1, c2)
        self.log[0] += 1
        self.bulletsAvailable -= 1
        if hit_flag:
            self.log[1] += 1
            print("You hit a boat!")
        else:
            self.log[2] += 1
            print("You missed.")
        # True is opponent has defeated, otherwise False.
        if self.rival.board.loose() or self.loose_by_ammo():
            return True
        else:
            return False

    def loose_by_ammo(self):
        if self.bulletsAvailable == 0:
            return True
            print("You run out of bullets!")
        else:
            return False


# Computer class
class Computer:
    # Initialize computer player with (name).
    def __init__(self, pname):
        self.pname = pname
        self.board = Board()
        self.ships = [Boat("Aircraft Carrier", 5), Boat("Battleship", 4), Boat("Submarine", 3), Boat("Destroyer", 3),
                      Boat("Patrol Boat", 2)]
        self.rival = None
        self.log = [0, 0, 0]

    # Link computer player and opponent.
    def set_rival(self, rival):
        self.rival = rival

    # Computer positions ships.
    def position_ships(self):
        for boat in self.ships:
            self.position_boat(boat)

        # Computer has succesfully positioned ships.
        input("The Computer's ships is ready to play.  Press enter to continue...")

    # Positions one ship. Helper method for positionShips.
    def position_boat(self, boat):
        CshipLocation = False
        while CshipLocation == False:
            # Randomize direction of computer's ship.
            o = random.randint(0, 1)
            if o == 0:
                direction = "v"
            else:
                direction = "h"

            # Randomized top-left position of computer's ship.
            # Loop.
            x = random.randint(1, 10) - 1
            y = random.randint(1, 10) - 1

            boat.set_direction(direction)
            boat.boat_position(x, y)

            # Add a ship.
            result = self.board.add_ship(boat)
            # If position not available.
            if result == True:
                CshipLocation = True

    # Single turn of computer player.
    def take_turn(self):
        # Randomize attack of Computer.
        x = random.randint(1, 10) - 1
        y = random.randint(1, 10) - 1

        # Statistics for computer player.
        print(self.pname, "Statistics\nAttacks: ", self.log[0], "\tHits: ", self.log[1], "\tMisses: ",
              self.log[2])

        # Perform attack
        hit_flag = self.rival.board.attack(x, y)
        self.log[0] += 1
        if hit_flag:
            self.log[1] += 1
            print("\nThe Computer hit a boat!")
        else:
            self.log[2] += 1
            print("\nThe Computer missed.")

        # True if opponent has been defeated. Otherwise False.
        if self.rival.board.loose():
            return True
        else:
            return False


# How many player are playing the game?
print("*************** Welcome to BATTLESHIP! ***************")
players_num = None
while players_num is None:
    players_num = int(input("Please enter the number of players. (1 or 2) "))
    if (players_num != 1) and (players_num != 2):
        print("Invalid input. You must enter either 1 or 2.  Please try again.")
        players_num = None
while True:
    game = BattleshipGame(players_num)
    game.play()
    replay = input("Do you want to play another match? (YES OR NO) ")
    if replay == 'NO':
        break
    elif replay == 'YES':
        continue
# Create new game.


# -----------------------------------------------------------------------------------------------------------------------------------------------------------

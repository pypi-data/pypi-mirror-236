'''

#bfs
graph={
    'A':['B','C'],
    'B':['D','E'],
    'C':['F'],
    'D':[],
    'E':['F'],
    'F':[]
    }

visited=[]
queue=[]


def BFS(visited,graph,node):
    visited.append(node)
    queue.append(node)
    while queue:
        m=queue.pop(0)
        print(m,end=" ")
        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

def DFS(visited,graph,node):
    if node not in visited:
        print(node)
        visited1.add(node)
        for neighbour in graph[node]:
            DFS(visited,graph,neighbour)
        
    
DFS(visited,graph,'A')
print("\n")
BFS(visited,graph,'A')
        
------------------------------------------------------------------------------------------
#DFS
# Define a simple graph as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

visited = {}  # Dictionary to keep track of visited nodes

# Recursive DFS function
def dfs(node):
    if node not in visited:
        print(node, end=' ')
        visited[node] = True
        for neighbor in graph[node]:
            dfs(neighbor)

# Call DFS starting from a specific node
dfs('A')
#BFS

from collections import deque

# Define the same graph as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# BFS function
def bfs(start):
    visited = {}  # Dictionary to keep track of visited nodes
    queue = deque()  # Queue for BFS traversal

    # Initialize with the start node
    queue.append(start)
    visited[start] = True

    while queue:
        node = queue.popleft()
        print(node, end=' ')

        # Visit all neighbors of the current node
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited[neighbor] = True

# Call BFS starting from node 'A'
bfs('A')
# Distributive law
a=5
b=3
c=2
Alhs=a*(b+c)
Arhs=(a+b)*(a+c)
if Alhs==Arhs:
    print("Distributive law holds for addition")
else:
    print("Distributive law doesn't hold for addition")

Mlhs=a+(b*c)
Mrhs=(a*b)+(a*c)
if Mlhs==Mrhs:
    print("Distributive law holds for multiplication")
else:
    print("Distributive law doesn't hold for multiplication")
# Associative law
a=5
b=3
c=2
Alhs=(a+b)+c
Arhs=a+(b+c)
if Alhs==Arhs:
    print("Associative law holds for addition")
else:
    print("Associative law doesn't hold for addition")

Mlhs=(a*b)*c
Mrhs=a*(b*c)
if Mlhs==Mrhs:
    print("Associative law holds for multiplication")
else:
    print("Associative law doesn't hold for multiplication")
--------------------------------------------------------------------------------------------------------------------------------------
#card shuffle
import random

# Define a deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]

# Shuffle the deck
random.shuffle(deck)

# Print the shuffled deck
for card in deck:
    print(f"{card['rank']} of {card['suit']}")
------------------------------------------------------------------------------------------------------------------------------------
#Travelling Sales man
from itertools import permutations

def tsp(graph):
    num_cities = len(graph)
    all_cities = list(range(num_cities))
    min_cost = float('inf')

    for tour in permutations(all_cities):
        tour_cost = sum(graph[tour[i - 1]][tour[i]] for i in range(num_cities))
        min_cost = min(min_cost, tour_cost)

    return min_cost

graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

print(tsp(graph))
---------------------------------------------------------------------------------------------------------
#waterjug
from collections import defaultdict
jug1, jug2, goal = 4, 3, 2

visited = defaultdict(lambda: False)

def WJS(amt1, amt2):

	if (amt1 == goal and amt2 == 0) or (amt2 == goal and amt1 == 0):
		print(amt1,"    ",amt2)
		return True

	if visited[(amt1, amt2)] == False:
		print(amt1,"    ",amt2)
		visited[(amt1,  amt2)] = True
		return (WJS(0, amt2) or
				WJS(amt1, 0) or
				WJS(jug1, amt2) or
				WJS(amt1, jug2) or
				WJS(amt1 + min(amt2, (jug1-amt1)),
				amt2 - min(amt2, (jug1-amt1))) or
				WJS(amt1 - min(amt1, (jug2-amt2)),
				amt2 + min(amt1, (jug2-amt2))))
	else:
		return False

print("Steps: \njug1  jug2")
WJS(0,0)
---------------------------------------------------------------------------------------------------
#A*
import networkx as net

# Create a graph
G = net.Graph()

# Add nodes and edges to the graph (customize as per your problem)
G.add_node('A', pos=(0, 0))
G.add_node('B', pos=(1, 1))
G.add_node('C', pos=(2, 2))
G.add_node('D', pos=(3, 3))
G.add_node('E', pos=(4, 4))

G.add_edge('A', 'B', weight=1)
G.add_edge('A', 'C', weight=3)
G.add_edge('B', 'D', weight=2)
G.add_edge('C', 'D', weight=1)
G.add_edge('D', 'E', weight=2)

# Define the start and goal nodes
start = 'A'
goal = 'E'

# Find the shortest path using A* algorithm
path = net.astar_path(G, start, goal, weight='weight')

path_cost = net.astar_path_length(G, start, goal, weight='weight')

print("Shortest path:",path)
print("Path cost:",path_cost)
------------------------------------------------------------------------------------------------------------------------
#N queen
class Solution:
    def solveNQueen(self, n: int) -> list[list[str]]:
        # Initialize sets to keep track of occupied columns and diagonal positions
        col = set()
        posDiag = set()
        negDiag = set()

        res = []

        board = [["."] * n for i in range(n)]

        def backtrack(r):
            # If all queens are placed successfully (r == n), add the current board configuration to the solutions
            if r == n:
                # Create a copy of the board as a list of strings
                copy = ["".join(row) for row in board]
                res.append(copy)
                return
            
            for c in range(n):
                if c in col or (r + c) in posDiag or (r - c) in negDiag:
                    continue

                col.add(c)
                posDiag.add(r + c)
                negDiag.add(r - c)
                board[r][c] = "Q"

                backtrack(r + 1)

                col.remove(c)
                posDiag.remove(r + c)
                negDiag.remove(r - c)
                board[r][c] = "."

        backtrack(0)
        return res

solution = Solution()
n = 4
solutions = solution.solveNQueen(n)
for i in solutions:
    for row in i:
        print(row)
    print()
-------------------------------------------------------------------------------------------------------------------------------------
# Hill climbing
from scipy.optimize import minimize
import numpy as np

# Define the objective function to be optimized
def objective_function(x):
    return sum(x ** 2)

# Hill climbing using SciPy's minimize function
problem_size = 5  # Change this to the size of your problem
initial_solution = np.random.uniform(-5, 5, problem_size)
result = minimize(objective_function, initial_solution, method='Powell', options={'disp': True})

best_solution = result.x
best_value = result.fun

print("Best Solution:", best_solution)
print("Best Value:",best_value)
------------------------------------------------------------------------------------------------------------
#Predicate 10A
# Define a dictionary to represent the rules or facts
rules = {
    "Sachin": "batsman",
    "batsman": "cricketer",
}

# Function to derive the predicate
def derive_pre(entity, rules):
    if entity in rules:
        return rules[entity]
    else:
        return "Unknown"

# Input entity you want to derive the predicate for
inputE= "Sachin"

# Derive the predicate
predicate = derive_pre(inputE, rules)

# Print the result
print(f"{inputE} is {predicate}")
---------------------------------------------------------------------------------------------------------------------------------
#family tree
from ete3 import Tree
t=Tree('(male, female,(((((ME, Brother,sister)Father  Mother))Grandfather  Grandmother))parent)Tree;',format=1)
print( t.get_ascii(show_internal=True)) 
-------------------------------------------------------------------------------------------------------------------------------
#cannibals & missionaries
from collections import deque

# Define the initial state and the goal state
initial_state = (3, 3, 1)  # (Missionaries on the left, Cannibals on the left, Boat position)
goal_state = (0, 0, 0)

# Function to check if a state is valid
def is_valid(state):
    m, c, b = state
    return 0 <= m <= 3 and 0 <= c <= 3 and (m >= c or m == 0) and (3 - m >= 3 - c or 3 - m == 0)

# Function to generate valid successor states
def successors(state):
    m, c, b = state
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    if b == 1:
        moves = [(-m, -c) for m, c in moves]
    return [(m + dm, c + dc, 1 - b) for dm, dc in moves if is_valid((m + dm, c + dc, 1 - b))]

# Breadth-First Search
def bfs():
    visited = set()
    queue = deque([(initial_state, [])])

    while queue:
        state, path = queue.popleft()
        if state == goal_state:
            return path + [state]
        if state not in visited:
            visited.add(state)
            for successor in successors(state):
                if successor not in visited:
                    queue.append((successor, path + [state]))

    return None  # No solution found

# Solve the problem
solution = bfs()

if solution:
    for state in solution:
        m, c, b = state
        print(f"{m} Missionaries, {c} Cannibals | Boat: {'Left' if b == 1 else 'Right'}")
else:
    print("No solution found.")
------------------------------------------------------------------------------------------------------------------------------
#tic tac toe
import random

# Define the Tic-Tac-Toe board
board = [" " for _ in range(9)]

# Function to print the board
def print_board():
    print("   |   |")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("___|___|___")
    print("   |   |")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("___|___|___")
    print("   |   |")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("   |   |")

# Function to check for a win
def check_win(board, player):
    # Check rows, columns, and diagonals for a win
    return ((board[0] == board[1] == board[2] == player) or
            (board[3] == board[4] == board[5] == player) or
            (board[6] == board[7] == board[8] == player) or
            (board[0] == board[3] == board[6] == player) or
            (board[1] == board[4] == board[7] == player) or
            (board[2] == board[5] == board[8] == player) or
            (board[0] == board[4] == board[8] == player) or
            (board[2] == board[4] == board[6] == player))

# Function to check if the board is full
def is_board_full(board):
    return " " not in board

# Minimax algorithm for AI player
def minimax(board, depth, maximizing):
    scores = {
        "X": 1,
        "O": -1,
        "Tie": 0
    }

    if check_win(board, "X"):
        return scores["X"]
    if check_win(board, "O"):
        return scores["O"]
    if is_board_full(board):
        return scores["Tie"]

    if maximizing:
        max_eval = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                eval = minimax(board, depth + 1, False)
                board[i] = " "
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                eval = minimax(board, depth + 1, True)
                board[i] = " "
                min_eval = min(min_eval, eval)
        return min_eval

# AI player makes a move
def ai_move():
    best_move = -1
    best_eval = -float("inf")

    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            eval = minimax(board, 0, False)
            board[i] = " "
            if eval > best_eval:
                best_eval = eval
                best_move = i

    return best_move

# Main game loop
while True:
    print_board()
    
    # Player's turn
    player_move = int(input("Enter your move (1-9): ")) - 1
    if 0 <= player_move < 9 and board[player_move] == " ":
        board[player_move] = "O"
    else:
        print("Invalid move. Try again.")
        continue

    if check_win(board, "O"):
        print_board()
        print("Congratulations! You win!")
        break

    if is_board_full(board):
        print_board()
        print("It's a tie!")
        break

    # AI's turn
    ai = ai_move()
    board[ai] = "X"

    if check_win(board, "X"):
        print_board()
        print("AI wins! You lose.")
        break

    if is_board_full(board):
        print_board()
        print("It's a tie!")
        break
--------------------------------------------------------------------------------------------------------------------------------------
def TOH(n, source, auxiliary, target):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    TOH(n-1, source, target, auxiliary)
    print(f"Move disk {n} from {source} to {target}")
    TOH(n-1, auxiliary, source, target)

# Usage
TOH(3, 'A', 'B', 'C')  
--------------------------------------------------------------------------------------------------------------------------------------










 '''

def sum(n1,n2):
    c=n1+n2
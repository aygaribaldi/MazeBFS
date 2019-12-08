import time

class Maze():
    """A pathfinding problem."""

    def __init__(self, grid, location):
        """Instances differ by their current agent locations."""
        self.grid = grid
        self.location = location

    def display(self):
        """Print the maze, marking the current agent location."""
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if (r, c) == self.location:
                    print('*', end=' ')
                else:
                    print(self.grid[r][c], end=' ')
            print()
        print()

    def moves(self):
        """Return a list of possible moves given the current agent location."""
        moves_list = []
        rows, cols = self.location
        if self.grid[rows+1][cols] != 'X':
            moves_list.append('S')
        if self.grid[rows-1][cols] != 'X':
            moves_list.append('N')
        if self.grid[rows][cols+1] != 'X':
            moves_list.append('E')
        if self.grid[rows][cols-1] != 'X':
            moves_list.append('W')
        return moves_list

    def neighbor(self, move):
        """Return another Maze instance with a move made."""
        current_location = list(self.location)
        location = ()
        if move == 'N':
            current_location[0] -= 1
            location = tuple(current_location)
        if move == 'S':
            current_location[0] += 1
            location = tuple(current_location)
        if move == 'E':
            current_location[1] += 1
            location = tuple(current_location)
        if move == 'W':
            current_location[1] -= 1
            location = tuple(current_location)

        m1 = Maze(self.grid, location)
        return m1


class Agent():

    def bfs(self, maze, goal):
        """Return an ordered list of moves to get the maze to match the goal."""
        # make the frontier and empty queue
        frontier = []
        final_moves = []
        visited_locations = []
        finished = False
        parent_in_list = False
        current_parent = ()
        # list of tuples with parent and list of moves
        parents_moves = []

        # enqueue the start onto the frontier
        frontier.append(maze.location)
        visited_locations.append(maze.location)
        parents_moves.append((maze.location, []))

        # until the frontier is empty
        while frontier and not finished:
            # dequeue the parent off frontier
            popped_node = frontier.pop(0)
            m1 = Maze(maze.grid, popped_node)

            if not finished:
                # for each child of parent
                for move in m1.moves():
                    visited = False
                    child = m1.neighbor(move)
                    child = child.location

                    # figure out if location has been visited
                    for loc in visited_locations:
                        if child == loc:
                            visited = True

                    # enqueue child onto frontier if undiscovered
                    if not visited:
                        visited_locations.append(child)
                        frontier.append(child)
                        # go through parents_moves list and see if the first element of the tuple is equal to parent of child
                        for m in parents_moves:
                            if popped_node == m[0]:
                                current_parent = m
                                parent_in_list = True
                                # add the child, and list of moves
                                parents_moves.append((child, current_parent[1] + [move]))

                    # stop if child is the goal
                    if child == goal.location:
                        final_moves = current_parent[1] + [move]
                        finished = True
                        frontier.clear()
                        break;

            # if the parent was in the list remove it
            if parent_in_list:
                try:
                    parents_moves.remove(current_parent)
                except:
                    pass

        return final_moves


def main():
    """Create a maze, solve it with BFS, and console-animate."""
    grid = ["XXXXXXXXXXXXXXXXXXXX",
            "X     X    X       X",
            "X XXXXX XXXX XXX XXX",
            "X       X      X X X",
            "X XXXXX XXXXXX X X X",
            "X X   X        X X X",
            "X XXX XXXXXX XXXXX X",
            "X XXX    X X X     X",
            "X    XXX       XXXXX",
            "XXXXX   XXXXXX     X",
            "X   XXX X X    X X X",
            "XXX XXX X X XXXX X X",
            "X     X X   XX X X X",
            "XXXXX     XXXX X XXX",
            "X     X XXX    X   X",
            "X XXXXX X XXXX XXX X",
            "X X     X  X X     X",
            "X X XXXXXX X XXXXX X",
            "X X                X",
            "XXXXXXXXXXXXXXXXXX X"]

    maze = Maze(grid, (1, 1))
    maze.display()

    agent = Agent()
    goal = Maze(grid, (19, 18))
    t1 = time.perf_counter()
    path = agent.bfs(maze, goal)
    t2 = time.perf_counter()
    t3 = t2-t1
    print(t3)
    while path:
        move = path.pop(0)
        maze = maze.neighbor(move)
        time.sleep(0.25)
        maze.display()

if __name__ == '__main__':
    main()
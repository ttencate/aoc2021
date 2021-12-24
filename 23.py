import heapq

import aoc


EXAMPLE1 = '''
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
'''


COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


class State:
    def __init__(self, data, room_size, destinations):
        self.data = data
        self.room_size = room_size
        self.destinations = destinations
        n = 0
        for d in self.data:
            if isinstance(d, str):
                n += 1
            elif isinstance(d, list):
                n += len(d)
        if not (n == len(self.destinations) * self.room_size):
            assert False, str(self)

    @classmethod
    def parse(cls, input):
        lines = input.strip().splitlines()
        room_size = len(lines) - 3
        data = []
        destinations = {}
        next_dest = 'A'
        for x, char in enumerate(lines[1]):
            if char == '.':
                if lines[2][x] == '#':
                    # No room below this cell.
                    data.append(None)
                else:
                    # Room exists below this cell.
                    destinations[next_dest] = len(data)
                    next_dest = chr(ord(next_dest) + 1)
                    data.append([lines[y][x] for y in range(1 + room_size, 1, -1) if lines[y][x].isalpha()])
            elif char.isalpha():
                data.append(char)
        return State(data, room_size, destinations)

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return self.data == other.data

    def __lt__(self, other):
        return False

    def __hash__(self):
        return hash(repr(self.data))

    def clone(self):
        data = [d[:] if isinstance(d, list) else d for d in self.data]
        return State(data, self.room_size, self.destinations)

    def moves(self):
        '''
        >>> state = State.parse(EXAMPLE1)
        >>> moves = list(state.moves())
        >>> len(moves)
        28
        >>> moves[0][0]
        30
        >>> print(moves[0][1])
        #############
        #B..........#
        ###.#C#B#D###
          #A#D#C#A#
          #########
        >>> moves[-1][0]
        3000
        >>> print(moves[-1][1])
        #############
        #..........D#
        ###B#C#B#.###
          #A#D#C#A#
          #########
        >>> state = State.parse("""
        ... #############
        ... #.B.....A.D.#
        ... ###.#C#B#.###
        ...   #A#D#C#.#
        ...   #########
        ... """)
        >>> moves = list(state.moves())
        >>> len(moves)
        1
        >>> moves[0][0]
        6
        >>> print(moves[0][1])
        #############
        #.B.......D.#
        ###A#C#B#.###
          #A#D#C#.#
          #########
        '''
        # If we can move into a room, do that and don't yield any other moves.
        # There is never any reason not to do this immediately.
        for i, d in enumerate(self.data):
            if isinstance(d, str):
                # Move into destination room if possible.
                dest = self.destinations[d]
                # Is destination room empty or only of our own type?
                if all(a == d for a in self.data[dest]):
                    # Is path clear?
                    # Start and end indices need not be checked: start is never
                    # clear (it contains our arthropod under consideration) and
                    # end is always clear (outside a room).
                    if all(not isinstance(self.data[j], str) for j in range(min(i, dest) + 1, max(i, dest))):
                        next_state = self.clone()
                        next_state.data[i] = None
                        next_state.data[dest].append(d)
                        num_steps = abs(dest - i) + 1 + self.room_size - len(next_state.data[dest])
                        cost = num_steps * COSTS[d]
                        yield cost, next_state
                        return

        # Move out of rooms.
        for i, d in enumerate(self.data):
            if isinstance(d, list) and d:
                # Move topmost arthropod out of the room.
                min_dest = i
                while min_dest > 0 and not isinstance(self.data[min_dest - 1], str):
                    min_dest -= 1
                max_dest = i
                while max_dest < len(self.data) - 1 and not isinstance(self.data[max_dest + 1], str):
                    max_dest += 1
                for dest in range(min_dest, max_dest + 1):
                    if isinstance(self.data[dest], list):
                        # Prohibited to linger just outside a room. And
                        # there's never any reason to, anyway.
                        continue
                    next_state = self.clone()
                    arthropod = next_state.data[i].pop()
                    next_state.data[dest] = arthropod
                    num_steps = abs(dest - i) + 1 + self.room_size - len(d)
                    cost = num_steps * COSTS[arthropod]
                    yield cost, next_state

    def is_done(self):
        for i, d in enumerate(self.data):
            if isinstance(d, str):
                # Someone is still in the hallway.
                return False
            elif isinstance(d, list):
                for a in d:
                    if i != self.destinations[a]:
                        # Someone is still in the wrong room.
                        return False
        return True

    def __str__(self):
        '''
        >>> state = State.parse(EXAMPLE1)
        >>> print(state)
        #############
        #...........#
        ###B#C#B#D###
          #A#D#C#A#
          #########
        >>> state.data[1] = state.data[2].pop()
        >>> print(state)
        #############
        #.B.........#
        ###.#C#B#D###
          #A#D#C#A#
          #########
        '''
        l = len(self.data)
        lines = [
            list('#############'),
            list('#...........#'),
            list('###.#.#.#.###'),
        ]
        for _ in range(self.room_size - 1):
            lines.append(list('  #.#.#.#.#'))
        lines.append(list('  #########'))
        for i, d in zip(range(1, l + 1), self.data):
            if isinstance(d, str):
                lines[1][i] = d
            elif isinstance(d, list):
                for j, a in zip(range(1 + self.room_size, 1, -1), d):
                    lines[j][i] = a
        return '\n'.join(''.join(line) for line in lines)


def augment(input):
    '''
    >>> print(augment(EXAMPLE1))
    #############
    #...........#
    ###B#C#B#D###
      #D#C#B#A#
      #D#B#A#C#
      #A#D#C#A#
      #########
    '''
    lines = input.strip().splitlines()
    lines.insert(3, '  #D#C#B#A#')
    lines.insert(4, '  #D#B#A#C#')
    return '\n'.join(lines)


def solve(input):
    '''
    >>> solve(EXAMPLE1)
    (12521, 44169)
    '''
    return min_cost(input), min_cost(augment(input))


def min_cost(input):
    start = State.parse(input)
    queue = [(0, start)]
    visited = set()
    while queue:
        cost, state = heapq.heappop(queue)
        if state.is_done():
            return cost
        if state in visited:
            continue
        visited.add(state)
        for move_cost, next_state in state.moves():
            next_cost = cost + move_cost
            heapq.heappush(queue, (next_cost, next_state))

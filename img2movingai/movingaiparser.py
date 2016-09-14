import itertools
import random


class MovingAIMap(object):

    def __init__(self, header, map_matrix):
        self.matrix = map_matrix
        self.height = len(map_matrix)
        self.width = len(map_matrix[0])
        self.type = 'unknown'
        self.doors = {}
        self._parse_header(header)

    def _parse_header(self, header):
        parsed_header = [(h.split(' ')[0], h.split(' ')[1:]) for h in header]
        for command, values in parsed_header:
            if command == "height":
                self.height = int(values[0])
            elif command == "width":
                self.width = int(values[0])
            elif command == "type":
                self.type = values[0]
            elif command == "key":
                self._parse_keys(values)

    def _parse_keys(self, values):
        if values[0] == '$key$':
            # Template, skip it.
            return
        values = [int(v) for v in values]  # Convert all to integers.
        pairs = list(pairwise(values))
        self.doors[pairs[0]] = pairs[1:]

    def is_door(self, r, c=None):
        if c is None:
            r, c = r
        return any(((r, c) in doors for doors in self.doors.values()))

    def is_key(self, r, c=None):
        if c is None:
            r, c = r
        return (r, c) in self.doors.keys()

    def is_free(self, r, c=None):
        if c is None:
            r, c = r
        return self.matrix[r][c] != '@' and not self.is_door(r, c)

    def find_key(self, r, c=None):
        if c is None:
            r, c = r
        if self.is_door(r, c):
            for k, v in self.doors.items():
                if (r, c) in v:
                    return k

    def all_free(self):
        lis = [(c, r) for c in range(self.width)
               for r in range(self.height) if self.is_free(r, c)]
        return lis

    def random_free(self):
        """
        Return a random free tile in the map.
        """
        return random.sample(list(self.all_free()), 1)  # TODO: Very inefficient.

    def __str__(self):
        result = "Moving AI Map\n"
        result += "\ttype = {}".format(self.type)
        result += "\theight = {}".format(self.height)
        result += "\twidth = {}".format(self.height)
        result += "\tkey-doors = {}".format(self.doors)
        return result


def parse_map(map_path):
    map_file = open(map_path, 'r')
    raw_map = map_file.read()
    raw_map_lines = raw_map.split('\n')
    header = list(itertools.takewhile(lambda l: l != "map", raw_map_lines))
    map_matrix = list(itertools.dropwhile(
        lambda l: l != "map", raw_map_lines))[1:]
    return MovingAIMap(header, map_matrix)


def pairwise(iterable):
    return zip(iterable[::2], iterable[1::2])

#######################################################

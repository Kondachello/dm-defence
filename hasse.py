import matplotlib.pyplot as plt
from itertools import combinations


class Poset:
    def __init__(self, elements, relations):
        self.elements = elements
        self.relations = relations
        self.hasse_relations = []
        self.levels = {}
        self.build_hasse_diagram()
        if self.check_for_cycles():
            raise ValueError("Error: cycle found. Relation must create a poset.")
        self.assign_levels()

    def dfs(self, v, visited, stack):
        visited[v] = stack[v] = True
        for a, b in self.hasse_relations:
            if a == v:
                if not visited[b]:
                    if self.dfs(b, visited, stack):
                        return True
                elif stack[b]:
                    return True
        stack[v] = False
        return False

    def build_hasse_diagram(self):
        self.hasse_relations = list(self.relations)
        to_remove = set()
        for a, b in self.relations:
            for c, d in self.relations:
                if b == c and (a, d) in self.hasse_relations:
                    to_remove.add((a, d))
        self.hasse_relations = [rel for rel in self.hasse_relations if rel not in to_remove]

    def check_for_cycles(self):
        visited = {elem: False for elem in self.elements}
        stack = {elem: False for elem in self.elements}
        for elem in self.elements:
            if not visited[elem]:
                if self.dfs(elem, visited, stack):
                    return True
        return False

    def assign_levels(self):
        levels = {elem: 0 for elem in self.elements}
        changed = True
        while changed:
            changed = False
            for a, b in self.hasse_relations:
                if levels[b] <= levels[a]:
                    levels[b] = levels[a] + 1
                    changed = True
        self.levels = {}
        for elem, level in levels.items():
            if level not in self.levels:
                self.levels[level] = []
            self.levels[level].append(elem)

    def is_lattice(self):
        for x, y in combinations(self.elements, 2):
            if not self.upper_bound(x, y) or not self.lower_bound(x, y):
                return False
        return True

    def upper_bound(self, x, y):
        upper_bounds = [z for z in self.elements if self.has_path(x, z) and self.has_path(y, z)]
        ub_candidates = [z for z in upper_bounds if all(self.has_path(u, z) for u in upper_bounds)]
        return ub_candidates[0] if len(ub_candidates) == 1 else None

    def lower_bound(self, x, y):
        lower_bounds = [z for z in self.elements if self.has_path(z, x) and self.has_path(z, y)]
        lb_candidates = [z for z in lower_bounds if all(self.has_path(z, u) for u in lower_bounds)]
        return lb_candidates[0] if len(lb_candidates) == 1 else None

    def has_path(self, start, end):
        if start == end:
            return True
        visited = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for a, b in self.hasse_relations:
                if a == node and b not in visited:
                    if b == end:
                        return True
                    visited.add(b)
                    stack.append(b)
        return False

    def draw_hasse_diagram(self):
        plt.figure(figsize=(8, 6))
        positions = {}
        for level, elements in self.levels.items():
            num_elements = len(elements)
            x_offset = -(num_elements - 1) / 2

            for i, elem in enumerate(elements):
                positions[elem] = (x_offset + i, level)
        for elem, (x, y) in positions.items():
            plt.plot(x, y, 'o', markersize=10, label=str(elem))
            xy_offset = 0.05
            plt.text(x + xy_offset, y + xy_offset, str(elem), ha='center', va='bottom', fontsize=14)
        for a, b in self.hasse_relations:
            x1, y1 = positions[a]
            x2, y2 = positions[b]
            dx = x2 - x1
            dy = y2 - y1
            arrow_offset = 0.1
            plt.arrow(x1, y1, dx * (1 - arrow_offset), dy * (1 - arrow_offset),
                      head_width=0.03, head_length=0.05, fc='k', ec='k', length_includes_head=True)
        plt.title("Hasse Diagram")
        plt.axis('off')
        plt.show()


elements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
relations = [(1, 2), (1, 3), (1, 6), (2, 4), (3, 4), (5, 1), (6, 4), (1, 7), (4, 8), (4, 9), (1, 4)]

poset = Poset(elements, relations)
print("Is lattice:", poset.is_lattice())
poset.draw_hasse_diagram()
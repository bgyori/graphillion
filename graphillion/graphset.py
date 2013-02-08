from graphillion import setset

def _hook_args(func):
    def wrapper(self, *args, **kwds):
        if args:
            obj = args[0]
            args = [None] + list(args)[1:]
            if obj is None:
                args[0] = None
            elif isinstance(obj, (set, frozenset)):
                args[0] = set([_do_hook_args(e) for e in obj])
            elif isinstance(obj, dict):
                args[0] = {}
                for k, l in obj.iteritems():
                    args[0][k] = [_do_hook_args(e) for e in l]
            elif isinstance(obj, list):
                args[0] = []
                for s in obj:
                    args[0].append([_do_hook_args(e) for e in s])
            else:
                args[0] = _do_hook_args(obj)
        return func(self, *args, **kwds)
    return wrapper

def _do_hook_args(e):
    if not isinstance(e, tuple):
        raise KeyError, e
    if e in setset._obj2int:
        return e
    elif (e[1], e[0]) in setset._obj2int:
        return (e[1], e[0])
    raise KeyError, e


class GraphSet(setset):

    @_hook_args
    def __init__(self, obj=None):
        setset.__init__(self, obj)

    @_hook_args
    def __contains__(self, s):
        return setset.__contains__(self, s)

    def include(self, obj):
        try:  # if obj is edge
            return setset.include(self, _do_hook_args(obj))
        except KeyError:  # else obj is vertex
            gs = GraphSet()
            for edge in [e for e in setset.universe() if obj in e]:
                gs |= setset.include(self, edge)
            return gs & self

    def exclude(self, obj):
        try:  # if obj is edge
            return setset.exclude(self, _do_hook_args(obj))
        except KeyError:  # else obj is vertex
            return self - self.include(obj)

    @_hook_args
    def add(self, obj):
        return setset.add(self, obj)

    @_hook_args
    def remove(self, obj):
        return setset.remove(self, obj)

    @_hook_args
    def discard(self, obj):
        return setset.discard(self, obj)

    def maximize(self):
        for s in setset.maximize(self, GraphSet._weights):
            yield s

    def minimize(self):
        for s in setset.minimize(self, GraphSet._weights):
            yield s

    @staticmethod
    def universe(universe=None, traversal=None, source=None):
        if universe is not None:
            edges = []
            GraphSet._weights = {}
            for e in universe:
                edges.append(e[:2])
                if len(e) > 2:
                    GraphSet._weights[e[:2]] = e[2]
            if traversal:
                if not source:
                    source = edges[0][0]
                    for e in edges:
                        source = min(e[0], e[1], source)
                edges = GraphSet._traverse(edges, traversal, source)
            setset.universe(edges)
        else:
            edges = []
            for e in setset.universe():
                if e in GraphSet._weights:
                    edges.append((e[0], e[1], GraphSet._weights[e]))
                else:
                    edges.append(e)
            return edges

    @staticmethod
    def _traverse(edges, traversal, source):
        neighbors = {}
        for u, v in edges:
            if u not in neighbors:
                neighbors[u] = set([v])
            else:
                neighbors[u].add(v)
            if v not in neighbors:
                neighbors[v] = set([u])
            else:
                neighbors[v].add(u)
        assert source in neighbors

        sorted_edges = []
        queue_or_stack = []
        visited_vertices = set()
        u = source
        while True:
            if u in visited_vertices:
                continue
            visited_vertices.add(u)
            for v in sorted(neighbors[u]):
                if v in visited_vertices:
                    e = (u, v) if (u, v) in edges else (v, u)
                    sorted_edges.append(e)
            new_vertices = neighbors[u] - visited_vertices - set(queue_or_stack)
            queue_or_stack.extend(new_vertices)
            if not queue_or_stack:
                break
            if traversal == 'bfs':
                u, queue_or_stack = queue_or_stack[0], queue_or_stack[1:]
            else:
                queue_or_stack, u = queue_or_stack[:-1], queue_or_stack[-1]
        assert set(edges) == set(sorted_edges)
        return sorted_edges

    _weights = {}
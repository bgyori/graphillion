import _illion


def add_elem(e):
    if e in setset._obj2int:
        return
    i = len(setset._int2obj)
    _illion.setset(set([i]))
    setset._obj2int[e] = i
    setset._int2obj.append(e)
    assert len(setset._int2obj) == len(_illion.universe()) + 1
    assert setset._int2obj[i] == e
    assert setset._obj2int[e] == i

def conv_arg(e):
    add_elem(e)
    return setset._obj2int[e]

def hook_arg(func):
    def wrapper(self, *args, **kwds):
        if not args:
            return func(self, *args, **kwds)
        else:
            obj = args[0]
            args = [None] + list(args)[1:]
            if isinstance(obj, list):
                l = []
                for s in obj:
                    l.append(set([conv_arg(e) for e in s]))
                args[0] = l
            elif isinstance(obj, dict):
                d = {}
                for k, l in obj.iteritems():
                    d[k] = [conv_arg(e) for e in l]
                args[0] = d
            elif isinstance(obj, (set, frozenset, tuple)):
                args[0] = set([conv_arg(e) for e in obj])
            else:
                args[0] = conv_arg(obj)
            return func(self, *args, **kwds)
    return wrapper

def conv_ret(s):
    if isinstance(s, (set, frozenset, tuple, list)):
        ret = set()
        for e in s:
            ret.add(setset._int2obj[e])
        return ret
    else:
        return setset._int2obj[e]

def hook_ret(func):
    def wrapper(self, *args, **kwds):
        return conv_ret(func(self, *args, **kwds))
    return wrapper


class setset_iterator(object):

    def __init__(self, it):
        self.it = it

    def __iter__(self):
        return self

    @hook_ret
    def next(self):
        return self.it.next()


class setset(_illion.setset):

    @hook_arg
    def __init__(self, *args, **kwds):
        _illion.setset.__init__(self, *args, **kwds);

    @hook_arg
    def __contains__(self, *args, **kwds):
        return _illion.setset.__contains__(self, *args, **kwds);

    @hook_arg
    def include(self, *args, **kwds):
        return _illion.setset.include(self, *args, **kwds);

    @hook_arg
    def exclude(self, *args, **kwds):
        return _illion.setset.exclude(self, *args, **kwds);

    @hook_arg
    def add(self, *args, **kwds):
        return _illion.setset.add(self, *args, **kwds)

    @hook_arg
    def remove(self, *args, **kwds):
        return _illion.setset.remove(self, *args, **kwds)

    @hook_arg
    def discard(self, *args, **kwds):
        return _illion.setset.discard(self, *args, **kwds)

    @hook_ret
    def pop(self, *args, **kwds):
        return _illion.setset.pop(self, *args, **kwds)

    def __iter__(self):
        return setset_iterator(self.rand_iter())

    def randomize(self):
        i = self.rand_iter()
        while (True):
            yield conv_ret(i.next())

    def optimize(self, weights_arg):
        weights = [0] * (len(setset.universe()) + 1)
        for o, w in weights_arg.iteritems():
            i = setset._obj2int[o]
            weights[i] = w
        i = self.opt_iter(weights)
        while (True):
            yield conv_ret(i.next())

    @staticmethod
    def universe(*args):
        if args:
            _illion.universe([])
            setset._obj2int = {}
            setset._int2obj = [None]
            for e in args[0]:
                add_elem(e)
            _illion.universe(xrange(1, len(*args) + 1))
        else:
            assert len(setset._int2obj) == len(_illion.universe()) + 1
            for e, i in setset._obj2int.iteritems():
                assert e == setset._int2obj[i]
            for i in xrange(1, len(setset._int2obj)):
                e = setset._int2obj[i]
                assert i == setset._obj2int[e]
            return setset._int2obj[1:]

    _obj2int = {}
    _int2obj = [None]


#class graphset(setset):
#    pass

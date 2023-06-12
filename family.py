from logpy import run, conde, var, eq
import rel

def father(name):
    x = var()
    return run(0, x, father(x, name))

def children(name):
    x = var()
    res = run(0, x, conde([rel.father(name,x)], [rel.mother(name,x)]))
    return res

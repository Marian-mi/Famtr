from logpy import run, conde, var, eq
import rel

def father(name):
    x = var()
    return run(0, x, rel.father(x, name))[0]

def mother(name):
    x = var()
    return run(0, x, rel.mother(x, name))[0]

def parent_rule_named(name, y):
    return conde([rel.father(y, name)], [rel.mother(y, name)])

def parent_rule(x, y):
    return conde([rel.father(y, x)], [rel.mother(y, x)])

def spouse(name):
    x, y = var(), var()
    return run(0, y, conde([rel.father(name, x), rel.mother(y, x)], [rel.mother(name, x), rel.father(y, x)]))[0]

def children(name):
    x = var()
    res = run(0, x, conde([rel.father(name,x)], [rel.mother(name,x)]))
    return res

def siblings(name): 
    x, y = var(), var()
    return remove_from_tup(run(0, y, conde([rel.father(x, name), rel.father(x, y)])), name)

def sibling_rule(x, y):
    z = var()
    return conde([rel.father(z, x), rel.father(z, y)])

def grandparents(name):
    x, y = var(), var()
    return run(0, y, conde([parent_rule_named(name, x), parent_rule(x, y)]))

def brother_rule(x, y):
    return conde([sibling_rule(x, y), rel.male(y)])

def sister_rule(x, y):
    return conde([sibling_rule(x, y), rel.female(y)])

def uncles(name):
    x, y = var(), var()
    return remove_from_tup(run(0, y, conde([parent_rule_named(name, x), brother_rule(x, y)])), father(name))

def aunts(name):
    x, y = var(), var()
    return remove_from_tup(run(0, y, conde([parent_rule_named(name, x), sister_rule(x, y)])), mother(name))

def remove_from_tup(tup, name):
    arr = list(tup)
    if name in arr:
        arr.remove(name)
    return arr
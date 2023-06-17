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

def spouse_rule_named(name, y):
    x = var()
    return conde([rel.father(name, x), rel.mother(y, x)], [rel.mother(name, x), rel.father(y, x)])

def children(name):
    x = var()
    res = run(0, x, conde([rel.father(name,x)], [rel.mother(name,x)]))
    return res

def children_rule(x, y):
    return conde([rel.father(x, y)], [rel.mother(x, y)])

def siblings(name): 
    x, y = var(), var()
    return remove_from_tup(run(0, y, conde([rel.father(x, name), rel.father(x, y)])), name)

def sibling_rule(x, y):
    z = var()
    return conde([rel.father(z, x), rel.father(z, y)])

def sibling_rule_named(name, y):
    z = var()
    return conde([rel.father(z, name), rel.father(z, y)])

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

def nephews(name):
    x, y, z = var(), var(), var()
    res = run(0, y, conde([sibling_rule_named(name, x), rel.male(x), children_rule(x, y)],
                          [spouse_rule_named(name, z), sibling_rule(z, x), rel.male(x), children_rule(x, y)]))
    for c in children(name):
        res = remove_from_tup(res, c)

    for c in children(spouse(name)):
        res = remove_from_tup(res, c)

    return res

def nieces (name):
    x, y, z = var(), var(), var()
    res = run(0, y, conde([sibling_rule_named(name, x), rel.female(x), children_rule(x, y)],
                          [spouse_rule_named(name, z), sibling_rule(z, x), rel.female(x), children_rule(x, y)]))
    for c in children(name):
        res = remove_from_tup(res, c)

    for c in children(spouse(name)):
        res = remove_from_tup(res, c)
        
    return res

def remove_from_tup(tup, name):
    arr = list(tup)
    if name in arr:
        arr.remove(name)
    return arr
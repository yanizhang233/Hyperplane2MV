import pickle
from nonlinearity import sigma
from config import Symbols
import math

with open('lib.p', 'rb') as fp:
    lib = pickle.load(fp)


with open('lib_aguzzoli.p', 'rb') as fp:
    lib_aguzzoli = pickle.load(fp)

def sigmaConstruct(w, b):
    if (w,b) in lib:
        return lib[(w,b)]
    if w < 0:
        return f"{Symbols.NOT}{sigmaConstruct_agu(-1 * w, -1 * b + 1)}"
    if w == 0:
        return f"{sigma(b)}"
    wl = w
    wr = w
    wl -= 1  # wl[idx] -= 1
    wr -= 1  # wr[idx] -= 1
    left = sigmaConstruct(wl, b)
    right = sigmaConstruct(wr, b + 1)
    if right == '0' or right == '¬ (1)':
        return '0'
    if left == '1' or left == '¬ (0)':
        return right
    if right == '1' or right == '¬ (0)':
        if left == '0' or left == '¬ (1)':
            return 'x'
        else:
            return f"({left} {Symbols.OR} x)"

    if left == '0' or left == '¬ (1)':
        if right == '1' or right == '¬ (0)':
            return 'x'
        else:
            return f"(x {Symbols.AND} {right})"
            # return '(' +'x' +str(idx+1) + ' ⊙ ' + str(right)+ ')'
    return f"(({left} {Symbols.OR} x) {Symbols.AND} {right})"




def sigmaConstruct_agu(w, b):
    if (w,b) in lib:
        return lib[(w,b)]
    if w < 0:
        return f"{Symbols.NOT}{sigmaConstruct_agu(-1*w, -1*b+1)}"
    if w == 0:
        return f"{sigma(b)}"
    # case 1
    if b==0 or b==-1*w+1:
        if b==0:
            return Symbols.OR.join(['x']*w)
        if b==-1*w+1:
            return Symbols.AND.join(['x']*w)
    # case 2
    if w % (-1*b+1) == 0 or w % (w+b) == 0:
        if w % (-1*b+1) == 0:
            return  Symbols.AND.join([f"({Symbols.OR.join(['x']*(w//(-1*b+1)))})"]*(-1*b+1))
        if w % (w+b) == 0:
            return Symbols.OR.join([f"({Symbols.AND.join(['x'] * (w // (w+b)))})"] * (w+b))
    # case 3
    if math.gcd(w, -1*b) > 1 or math.gcd(w, -1*b+1) > 1:
        if math.gcd(w, -1*b) > 1:
            d = math.gcd(w, -1*b)
            return Symbols.OR.join([sigmaConstruct_agu(w//d, b//d)] * d)
        if math.gcd(w, -1*b+1) > 1:
            d = math.gcd(w, -1*b+1)
            return Symbols.AND.join([sigmaConstruct_agu(w//d, (b+d-1)//d)]*d)
    # case 4
    wl = w
    wr = w
    wl -= 1  # wl[idx] -= 1
    wr -= 1  # wr[idx] -= 1
    left = sigmaConstruct_agu(wl, b)
    right = sigmaConstruct_agu(wr, b + 1)
    if right == '0' or right == '¬ (1)':
        return '0'
    if left == '1' or left == '¬ (0)':
        return right
    if right == '1' or right == '¬ (0)':
        if left == '0' or left == '¬ (1)':
            return 'x'
        else:
            return f"({left} {Symbols.OR} x)"

    if left == '0' or left == '¬ (1)':
        if right == '1' or right == '¬ (0)':
            return 'x'
        else:
            return f"(x {Symbols.AND} {right})"
            # return '(' +'x' +str(idx+1) + ' ⊙ ' + str(right)+ ')'
    return f"(({left}) {Symbols.OR} x) {Symbols.AND} ({right})"




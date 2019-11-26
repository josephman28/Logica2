from copy import deepcopy

def enFNC(A):
    assert(len(A)==4 or len(A)==7), u"Fórmula incorrecta!"
    B = ''
    p = A[0]

    if "-" in A:
        q = A[-1]

        B = "-"+p+"O-"+q+"Y"+p+"O"+q
    elif "Y" in A:
        q = A[3]

        r = A[5]

        B = q+"O-"+p+"Y"+r+"O-"+p+"Y-"+q+"O-"+r+"O"+p
    elif "O" in A:
        q = A[3]

        r = A[5]

        B = q+"O"+p+"Y-"+r+"O"+p+"Y"+q+"O"+r+"O-"+p
    elif ">" in A:
        q = A[3]

        r = A[5]

        B = q+"O"+p+"Y-"+r+"O"+p+"Y-"+q+"O"+r+"O-"+p
    else:
        print(u'Error enENC(): Fórmula incorrecta!')

    return B


def Tseitin(A, letrasProposicionalesA):
    letrasProposicionalesB = [chr(x) for x in range(256, 300)]
    assert(not bool(set(letrasProposicionalesA) & set(letrasProposicionalesB))), u"¡Hay letras proposicionales en común!"
    l = []
    pila = []
    i = -1
    s = A[0]
    while len(A)>0:
        if s in letrasProposicionalesA and len(pila)> 0 and pila[-1]=="-":
            i += 1
            atomo = letrasProposicionalesB[i]
            pila = pila[:-1]
            pila.append(atomo)
            l.append(atomo + "=-" + s)
            A = A[1:]
            if len(A)>0:
                s = A[0]
        elif s == ")":
            w = pila[-1]
            o = pila[-2]
            v = pila[-3]
            pila = pila[:len(pila)-4]
            i+=1
            atomo = letrasProposicionalesB[i]
            f = atomo + "=" + "(" + v + o + w + ")"
            l.append(f)
            s = atomo
        else:
            pila.append(s)
            A = A[1:]
            if len(A)>0:
                s = A[0]
    B = ""
    if i < 0:
        atomo = pila[-1]
    else:
        atomo = letrasProposicionalesB[i]
    for x in l:
        y = enFNC(x)
        B += "Y" + y
    B = atomo + B
    return B


def Clausula(C):
    l = []
    while len(C)>0:
        s = C[0]
        if s == "O":
            C = C[1:]
        elif s == "-":
            literal = s + C[1]
            l.append(literal)
            C = C[2:]
        else:
            l.append(s)
            C = C[1:]
    return l

def formaClausal(A):
    l = []
    i = 0
    while len(A)> 0:
        if i >= len(A):
            l.append(Clausula(A))
            A = []
        else:
            if A[i] == 'Y':
                l.append(Clausula(A[:i]))
                A = A[i+1:]
                i = 0
            else:
                i+=1
    return l

def clausula_u(S):
    for x in S:
        if len(x) == 1:
            return x
    return None

def complemento(l):
    x = l[0]
    if len(x) == 1:
        lc = "-"+x
        return lc
    else:
        lc = x[-1]
        return lc

def clausula_v(S):
    for x in S:
        if len(x) == 0:
            return True
    return False

def unitProp(S, I):

    P = True

    while(P):

        i = clausula_u(S)

        if i == None:
            P = False
        else:
            i_c = complemento(i)
            S = [x for x in S if i[0] not in x]
            for x in S:
                if i_c in x:
                    x.remove(i_c)

            if len(i[0]) == 2:
                I[i_c] = 0
            else:
                I[i[0]] = 1

    return S, I

def DPLL(S, I):
    S, I=unitProp(S,I)
    clausulavacia=[]
    if clausulavacia in S:
        return "Insatisfacible", {}
    elif len(S)==0:
        return "Satisfacible", I
    l=""
    for x in S:
       for p in x:
           if p not in I.keys():
               l=p
    Sp=deepcopy(S)
    for m in S:
        if l in m:
            Sp.remove(m)
        elif complemento(l) in m:
            m.remove(complemento(l))
    Ip=deepcopy(I)
    if l[0] == '-':
            Ip[l[1]] = 0
    else:
        Ip[l] = 1
    S1, I1 = DPLL(Sp, Ip)
    if S1 == "Satisfacible":
        return S1,I1
    else:
        Spp=deepcopy(S)
        for a in Spp:
            if complemento(l) in a:
                Spp.remove(a)
        for b in Spp:
            if l in b:
                b.remove(l)
        Ipp=deepcopy(I)
        if l[0]=='-':
            Ipp[l[1]]=0
        else:
            Ipp[l]=1
        return DPLL(Spp,Ipp)
# Test enFNC()
# Descomente el siguiente código y corra el presente archivo
# formula = "p=(qYr)"
# print(enFNC(formula)) # Debe obtener qO-pYrO-pY-qO-rOp

# Test Tseitin()
# Descomente el siguiente código y corra el presente archivo
# formula = "(p>q)"
# print(Tseitin(formula, ['p','q'])) # Debe obtener AYpO-AYqO-AY-pO-qOA (la A tiene una raya encima)

# Test Clausula()
# Descomente el siguiente código y corra el presente archivo
# c = "pO-qOr"
# print(Clausula(c)) # Debe obtener ['p', '-q', 'r']

# Test formaClausal()
# Descomente el siguiente código y corra el presente archivo
letras=["A","G","P","B","b","N","D","H","T","t","S","C","F"]
f = "((((((A>(GYP))Y((B>b)Y(b>B)))Y(N>(((-DYb)YH)OT)))Y(G>-b))Y(F>(HY-S)))Y(S>(AYC)))Y((t>((bYF)YH))Y((bYF)YH)>t)"
S = formaClausal(Tseitin(f, letras))
#print(Tseitin(f, letras)) # Debe obtener [['p', '-q', 'r'], ['-s', 't']]
I={}
# formula = "((((((A>(GYP))Y((B>b)Y(b>B)))Y(N>(((-DYb)YH)OT)))Y(G>-b))Y(F>(HY-S)))Y(S>(AYC)))Y((t>((bYF)YH))Y((bYF)YH)>t)"
# letras=["A","G","P","B","b","N","D","H","T","t","S","C","F"]

#S = Tseitin(f, letras) # Debe obtener AYpO-AYqO-AY-pO-qOA (la A tiene una raya encima)
print(DPLL(S,I))

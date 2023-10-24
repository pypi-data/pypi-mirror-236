import math
import random as rd

from QElephant.Matrix import *

I = complex(0, 1)

## Classes

class MuBit:
    def __init__(self, n: int=2) -> None:
        if type(n) is not int:
            raise TypeError(f"number of state must be an intergers, not {type(n)}")
        if not n >= 2:
            raise ValueError("a MuBit must have at least two intricated QuBit")

        self.__n = n
        self.__state: list[complex] = [0]*(2**self.__n)
        self.__state[0] = 1
    
    def get_size(self) -> int:
        return self.__n
    
    def __str__(self) -> str:
        def next(N: str) -> str:
            if N == "":
                return ""
            if N[-1] == "0":
                return N[:-1]+"1"
            else:
                return (next(N[:-1]))+"0"
        
        txt = ""
        N = "0"*self.__n
        for i in range(2**self.__n):
            txt += f"{round(self.__state[i], 3)} |{N}>\n"
            N = next(N)
        return txt
    
    def __set(self, i: int, value: int) -> None:
        """Set the nth QuBit into value"""
        if type(i) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(i)}")
        if i > self.__n:
            raise IndexError("MuBit index out of range")
        if not value in {0, 1}:
            raise ValueError(f"QuBit state must be 0 or 1, not {value}")

        i = i%self.__n
        M = Matrix([[1]])
        for j in range(self.__n):
            if j == i:
                M *= Matrix([[1-value, 0], [0, value]])
            else:
                M *= Matrix([[1, 0], [0, 1]])
        self.__state = M._Matrix__apply(self.__state)
        norm = math.sqrt(sum([abs(x)**2 for x in self.__state]))
        self.__state = [x/norm for x in self.__state]
    
    def __iter__(self):
        return iter([IQuBit(i, self) for i in range(self.__n)])
    
    def __getitem__(self, item: int) -> "QuBit":
        if type(item) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(item)}")
        if item > self.__n:
            raise IndexError("MuBit index out of range")

        item = item%self.__n
        return IQuBit(item, self)

    def __apply(self, i: int, matrix: Matrix) -> None:
        if type(i) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(i)}")
        if i > self.__n:
            raise IndexError("MuBit index out of range")
        if type(matrix) is not Matrix:
            raise TypeError(f"can only manipulate MuBit with Matrix, not {type(matrix)}")
        i = i%self.__n

        M = Matrix([[1]])

        for j in range(self.__n):
            if j == i:
                M *= matrix
            else:
                M *= Matrix.I()
        
        self.__state = M._Matrix__apply(self.__state)
    
    def __mapply(self, matrix: Matrix, i: int) -> None:
        if type(i) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(i)}")
        if i > self.__n:
            raise IndexError("MuBit index out of range")
        if type(matrix) is not Matrix:
            raise TypeError(f"can only manipulate MuBit with Matrix, not {type(matrix)}")
        i = i%self.__n

        M = Matrix([[1]])
        j = 0
        while j < self.__n:
            if j == i:
                M *= matrix
                j += 2
            else:
                M *= Matrix.I()
                j += 1
        self.__state = M._Matrix__apply(self.__state)
    
    def __getProb(self, i: int) -> float:
        """Probs for i to be zero"""
        if type(i) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(i)}")
        if i > self.__n:
            raise IndexError("MuBit index out of range")
        i = i%self.__n

        M = Matrix([[1]])

        for j in range(self.__n):
            if j == i:
                M *= Matrix([[1, 0], [0, 0]])
            else:
                M *= Matrix.I()
        
        l = M._Matrix__apply(self.__state)
        return sum([abs(x)**2 for x in l])

    def observe(self) -> list[int]:
        l = []
        for i in range(self.__n):
            l.append(IQuBit(i, self).observe())
        return l
    
    @staticmethod
    def intricateThem(*args: "QuBit") -> "MuBit":
        for q in args:
            if type(q) is IQuBit:
                raise TypeError("cannot intricate QuBit that are already intricated")
            if type(q) is not QuBit:
                raise TypeError(f"cannot intricate QuBit and {type(q)}")
        if len(args) < 2:
            raise ValueError("cannot intricate less than two QuBits")

        S = Matrix([[1]])
        for q in args:
            S *= Matrix([q._QuBit__state])

        mq = MuBit(len(args))
        mq._MuBit__state = S._Matrix__m[0]
        return mq
    
class QuBit:
    def __init__(self, alpha: complex=1, beta: complex=0):
        if type(alpha) not in {int, float, complex}:
            TypeError(f"QuBit state must be int, float or complex, not {type(alpha)}")
        if type(beta) not in {int, float, complex}:
            TypeError(f"QuBit state must be int, float or complex, not {type(alpha)}")
        if abs(alpha)**2 + abs(beta)**2 != 1:
            raise ValueError(f"the initial state must be normalized. Here, |alpha|**2+|beta|**2={abs(alpha)**2 + abs(beta)**2}")
        
        self.__state = [alpha, beta]
        self.__intricated = False
    
    def is_intricated(self) -> bool:
        return self.__intricated
    
    def get_Mubit(self) -> None:
        return None
    
    def __str__(self) -> str:
        return f"{round(self.__state[0], 3)} |0> + {round(self.__state[1], 3)} |1>"
    
    def __apply(self, matrix: Matrix) -> None:
        if type(matrix) is not Matrix:
            raise TypeError(f"can only manipulate QuBit with Matrix, not {type(matrix)}")

        self.__state = matrix._Matrix__apply(self.__state)
    
    def observe(self) -> list[int]:
        r = rd.random()
        if r < abs(self.__state[0])**2:
            self.__state = [1, 0]
            return 0
        self.__state = [0, 1]
        return 1

class IQuBit(QuBit):
    def __init__(self, n: int, mb: MuBit) -> None:
        if type(n) is not int:
            raise TypeError(f"MuBit indices must be interger, not {type(n)}")
        if n > mb._MuBit__n:
            raise ValueError(f"MuBit index out of range")
        if type(mb) is not MuBit:
            TypeError(f"an intricate QuBit should be associated with a MuBit, not a {type(mb)}")
        n = n%mb._MuBit__n

        super().__init__()
        self.__n = n
        self.__muBit = mb
        self.__intricated = True
    
    def is_intricated(self) -> bool:
        return self.__intricated
    
    def get_Mubit(self) -> tuple[MuBit, int]:
        return (self.__muBit, self.__n)
    
    def __str__(self) -> str:
        p = self.__muBit._MuBit__getProb(self.__n)
        return str(QuBit(math.sqrt(p), math.sqrt(1-p)))
    
    def __apply(self, matrix: Matrix) -> None:
        if type(matrix) is not Matrix:
            raise TypeError(f"can only manipulate QuBit with Matrix, not {type(matrix)}")

        self.__muBit._MuBit__apply(self.__n, matrix)
    
    def observe(self) -> int:
        r = rd.random()
        if r < self.__muBit._MuBit__getProb(self.__n):
            self.__muBit._MuBit__set(self.__n, 0)
            return 0
        self.__muBit._MuBit__set(self.__n, 1)
        return 1





## Fonctions

def H(q: QuBit) -> None:
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.H())
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.H())
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def X(q: QuBit) -> None:
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.X())
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.X())
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def Y(q: QuBit) -> None:
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Y())
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.Y())
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def Z(q: QuBit) -> None:
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Z())
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.Z())
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def S(q: QuBit) -> None:
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.S())
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.S())
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def T(q: QuBit) -> None:
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.T())
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.T())
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def Rx(q: QuBit, phi: float) -> None:
    if type(phi) not in {int, float}:
        TypeError(f"an angle must be integer or float, not {type(phi)}")

    if type(q) == QuBit:
        q._QuBit__apply(Matrix.Rx(phi))
    elif type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Rx(phi))
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def Ry(q: QuBit, phi: float) -> None:
    if type(phi) not in {int, float}:
        TypeError(f"an angle must be integer or float, not {type(phi)}")

    if type(q) == QuBit:
        q._QuBit__apply(Matrix.Ry(phi))
    elif type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Ry(phi))
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def Rz(q: QuBit, phi: float) -> None:
    if type(phi) not in {int, float}:
        TypeError(f"an angle must be integer or float, not {type(phi)}")

    if type(q) == QuBit:
        q._QuBit__apply(Matrix.Rz(phi))
    elif type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Rz(phi))
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def R1(q: QuBit, phi: float) -> None:
    if type(phi) not in {int, float}:
        TypeError(f"an angle must be integer or float, not {type(phi)}")

    if type(q) == QuBit:
        q._QuBit__apply(Matrix.R1(phi))
    elif type(q) == IQuBit:
        q._IQuBit__apply(Matrix.R1(phi))
    else:
        raise TypeError(f"a QuBit was expected, but a {type(q)} was given")

def CNOT(q: MuBit, n1: int, n2: int) -> None:
    if type(q) is not MuBit:
        TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(n1) is not int:
        TypeError(f"MuBit indices must be intergers, not {type(n1)}")
    if type(n2) is not int:
        TypeError(f"MuBit indices must be intergers, not {type(n2)}")
    if n1 > q._MuBit__n or n2 > q._MuBit__n:
        ValueError("Mubit index out of range")
    n1 = n1%q._MuBit__n
    n2 = n2%q._MuBit__n
    if n1==n2:
        ValueError("the CNOT gate must be applied on two differents QuBits")

    SWAP(q, 0, n1)
    SWAP(q, 1, n2)
    q._MuBit__mapply(Matrix.CNOT(), 0)
    SWAP(q, 0, n1)
    SWAP(q, 1, n2)

def SWAP(q: MuBit, n1: int, n2: int) -> None:
    if type(q) is not MuBit:
        TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(n1) is not int:
        TypeError(f"MuBit indices must be intergers, not {type(n1)}")
    if type(n2) is not int:
        TypeError(f"MuBit indices must be intergers, not {type(n2)}")
    if n1 > q._MuBit__n or n2 > q._MuBit__n:
        ValueError("Mubit index out of range")
    n1 = n1%q._MuBit__n
    n2 = n2%q._MuBit__n
    if n1==n2:
        ValueError("the SWAP gate must be applied on two differents QuBits")

    nmin = min(n1, n2)
    nmax = max(n1, n2)
    for i in range(nmin, nmax):
        q._MuBit__mapply(Matrix.SWAP(), i)
    for i in range(nmax-2, nmin-1, -1):
        q._MuBit__mapply(Matrix.SWAP(), i)

def Cu(q: MuBit, u: list[list[complex]], n1: int, n2: int) -> None:
    if type(q) is not MuBit:
        TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(n1) is not int:
        TypeError(f"MuBit indices must be intergers, not {type(n1)}")
    if type(n2) is not int:
        TypeError(f"MuBit indices must be intergers, not {type(n2)}")
    if n1 > q._MuBit__n or n2 > q._MuBit__n:
        ValueError("Mubit index out of range")
    n1 = n1%q._MuBit__n
    n2 = n2%q._MuBit__n
    if n1==n2:
        ValueError("the Cu gate must be applied on two differents QuBits")
    if type(u) is not list:
        raise ValueError(f"u was expected to be list[list[complex]], not {type(u)}")
    for u_ in u:
        if type(u_) is not list:
            raise ValueError(f"u was expected to be list[list[complex]]. A {type(u_)} has been found")
    for l in u:
        for x in l:
            if type(x) not in {int, float, complex}:
                raise ValueError(f"u was expected to be list[list[complex]]. A {type(x)} has been found")
    if len(u) != 2 or len(u[0]) != 2:
        if len(u) == 0:
            ValueError(f"the size of the matrix was expected to be (2, 2). A matrix of size (0, .) has been given")
        ValueError(f"the size of the matrix was expected to be (2, 2). A matrix of size ({len(u)}, {u[0]}) has been given")

    SWAP(q, 0, n1)
    SWAP(q, 1, n2)
    q._MuBit__mapply(Matrix.Cu(u), 0)
    SWAP(q, 0, n1)
    SWAP(q, 1, n2)

if __name__=="__main__":
    q = MuBit(2)
    H(q[0])
    Cu(q, [[0, 1], [1, 0]], 0, 1)

    print(q)
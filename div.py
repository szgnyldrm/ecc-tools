from fastecdsa import curve
from fastecdsa.point import Point
import bit
import sys

G = curve.secp256k1.G
N = curve.secp256k1.q

def pub2point(pub_hex):
    x = int(pub_hex[2:66],16)
    if len(pub_hex) < 70:
        y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
    else:
        y = int(pub_hex[66:], 16)
    return Point(x,y,curve=curve.secp256k1)

def point2compress(A):
    prefix = "03"
    if int(A.y) % 2 == 0:
        prefix = "02"
    return f"{prefix}{hex(A.x)[2:].zfill(64)}"
    
pubkey = "022f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a01"
total_keys = 2

Q = pub2point(pubkey)

k = pow(2, N-2, N)

for i in range(total_keys):
    try:
        Q = Q - (i*G)
        compress = point2compress(k*Q)
        print(compress, i)
    except:
        print("END", i)
        sys.exit()


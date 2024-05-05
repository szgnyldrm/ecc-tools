from fastecdsa import curve
from fastecdsa.point import Point
import bit
import sys

G = curve.secp256k1.G
N = curve.secp256k1.q


def pub2point(pub_hex):
    x = int(pub_hex[2:66], 16)
    if len(pub_hex) < 70:
        y = bit.format.x_to_y(x, int(pub_hex[:2], 16) % 2)
    else:
        y = int(pub_hex[66:], 16)
    return Point(x, y, curve=curve.secp256k1)


def point2compress(A):
    prefix = "03"
    if int(A.y) % 2 == 0:
        prefix = "02"
    return f"{prefix}{hex(A.x)[2:].zfill(64)}"


def sub_point(Q, S):
    x = Q - (S * G)
    return x


def add_point(Q, S):
    x = Q + (S * G)
    return x


def div_point(Q):
    k = pow(2, N-2, N)
    x = Q - (0 * G)
    return k * x


pubkey = "02e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd13"

xy_point = pub2point(pubkey)

div = div_point(xy_point)
div_public_key = point2compress(div)
print(div_public_key)


# add = add_point(xy_point, 6)
# add_public_key = point2compress(add)
# print(add_public_key)
# sub = sub_point(xy_point, 3)
# sub_public_key = point2compress(sub)
# print(sub_public_key)

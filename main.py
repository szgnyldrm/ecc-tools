from fastecdsa import curve
from fastecdsa.point import Point
import bit
import sys

G = curve.secp256k1.G
N = curve.secp256k1.q
Q = "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"


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


def is_zero(xy_point, key):
    if key % 2 != 0:
        key -= 1
        xy_point = sub_point(xy_point, 1)
    return xy_point, key


def is_rest(xy_point):
    return int(xy_point.x) % 2


def show(pubkey, key, xy_point):
    print(f"{pubkey} - Priv: {key} - Mod: {is_rest(xy_point)}")


pubkey = "033c4a45cbd643ff97d77f41ea37e843648d50fd894b864b0d52febc62f6454f7c"
private_key = "0xD2C55"
total_range = 20

xy_point, key = is_zero(pub2point(pubkey), int(private_key, 16))

show(pubkey, key, xy_point)

for i in range(total_range):
    key /= 2
    xy_point = div_point(xy_point)

    compress = point2compress(xy_point)
    show(compress, key, xy_point)

    xy_point, key = is_zero(xy_point, key)

    if compress == Q:
        break

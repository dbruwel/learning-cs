import json
import math


class EllipticCurve:
    def __init__(self, curve_coords: tuple[int, int], p: int, base: tuple[int, int]):
        self.curve: tuple = curve_coords  # (a, b) in y^2 = x^3 + ax^2 + bx
        self.order: int = p  # must be a prime number for this instance
        self.base = base

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as f:
            data = json.load(f)

        p = data["p"]
        a = data["a"]
        b = data["b"]
        base_x = data["base_x"]
        base_y = data["base_y"]

        return cls((a, b), p, (base_x, base_y))

    def _intersect_line_reflect(self, grad: int, x1: int, x2: int, y1: int):
        a = self.curve[0]
        x3 = (pow(grad, 2, self.order) - a - x1 - x2) % self.order
        y3 = (grad * (x1 - x3) - y1) % self.order
        return (x3, y3)

    def double(self, p1: tuple[int, int]):
        a = self.curve[0]
        b = self.curve[1]

        x1, y1 = p1
        x2 = x1

        grad = (3 * x1**2) % self.order
        grad = (grad + 2 * a * x1) % self.order
        grad = (grad + b) % self.order
        grad = (grad * pow(2 * y1, -1, self.order)) % self.order

        return self._intersect_line_reflect(grad, x1, x2, y1)

    def add(self, p1: tuple[int, int], p2: tuple[int, int]):
        x1, y1 = p1
        x2, y2 = p2

        if (x1 == x2) and (y1 == y2):
            return self.double(p1)

        grad = (y2 - y1) % self.order
        grad = (grad * pow(x2 - x1, -1, self.order)) % self.order

        return self._intersect_line_reflect(grad, x1, x2, y1)

    def multiply(self, p1: tuple[int, int], n: int):
        num_dubs = int(math.log2(n))
        powers = [p1]
        for _ in range(num_dubs):
            powers.append(self.double(powers[-1]))

        bits = [int(b) for b in bin(n)[3:]]

        running_total = powers.pop()

        for b in bits:
            next_power = powers.pop()
            if b == 1:
                running_total = self.add(running_total, next_power)

        return running_total


def get_pub(curve, priv):
    return curve.multiply(curve.base, priv)


def get_shared_key(curve, my_priv, their_pub):
    return curve.multiply(their_pub, my_priv)


def encrypt(shared, pt_message):
    return pt_message ^ shared[0]


def decrypt(shared, e_message):
    return e_message ^ shared[0]

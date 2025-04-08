import math

def main():
    R = toOhms(1, "k")
    C = toFarads(71, "nF")
    F = 1/(2*math.pi*R*C)

    Xc = 1/(2*math.pi*F*C)
    # Xl = 2*math.pi*F*L

    C1 = C * 1.414 * (10 ** 9)
    C2 = C * 0.7071 * (10 ** 9)

    print("F: {}\nR: {:.3f}\nC: {:.6f}\nXc: {:.3f}".format(int(F), R, C, Xc))
    print("\nFor II order Butterworth Response:\nC1: {:.2f}nF\nC2: {:.2f}nF".format(C1, C2))

def toFarads(value: float, units: str):
    """
    :param value: value in units
    :param units: F, uF, mkF
    :return:
    """
    multiplier = {
        "": 1,
        "F": 1,
        "uF": (10 ** -6),
        "nF": (10 ** -9),
        "pF": (10 ** -12)
    }
    return value * multiplier[units]

def toOhms(value: float, units: str):
    """
    :param value: value in units
    :param units: F, uF, mkF
    :return:
    """
    multiplier = {
        "": 1,
        "k": 1000,
        "m": 1000000
    }
    return value * multiplier[units.lower()]

if __name__ == "__main__":
    main()

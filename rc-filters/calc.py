import math

class AppError(Exception):

    pass

class SuperError(AppError):

    pass

def main():
    """
    F=300
    C=100
    Cfarrad=C*(10**-6)
    Xc=int(1/(2*math.pi*F*Cfarrad))
    Xl=2*math.pi*F*L
    R=4
    Uin=12
    U = (Uin * R) / (Xc + R)
    print("U: {}".format(U))
    """

    R1=40
    R2=20
    Uin=10
    U1 = (Uin * R1) / (R1 + R2)
    U2 = (Uin * R2) / (R1 + R2)

    I2 = U2/R2
    P2 = U2 * I2 # P2 = U2 ** 2 / R2

    print("U1: {:.3f}, U2: {:.3f}, I2: {:.3f}, P2: {:.3f}".format(U1, U2, I2, P2))


if __name__ == "__main__":
    main()

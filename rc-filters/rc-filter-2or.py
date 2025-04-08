import math
from webbrowser import Error


def main():
    # Maximum Pass-band Ripple [dB]
    Amax = 1.5
    # Minimum Stop-band Attenuation [dB]
    Amin = 16
    # Cutoff Frequency
    Fc = 500

    Fs = Fc * 4

    # Calculate necessary filter order
    Ep = math.sqrt(10**(Amax / 10) - 1)
    Es = math.sqrt(10**(Amin / 10) - 1)
    n = math.log(Es / Ep) / math.log(Fs / Fc)
    n = math.ceil(n)
    wc = 2 * math.pi * Fc

    # Component values
    R1 = R2 = 1000  # Ohm
    C1 = (1 / (R1 * wc)) * 1.414
    C2 = (1 / (R2 * wc)) * 0.7071

    Fc1 = int(1 / (2 * math.pi * R1 * C1))
    Fc2 = int(1 / (2 * math.pi * R2 * C2))

    # Actual Stop-band Attenuation
    Fp = Fc * (Ep ** (1/n))
    Amin_test_1 = math.floor(10 * math.log10( 1 + Ep**2 * (Fs/Fp)**(2*n) ))
    Amin_test_2 = math.floor(10 * math.log10( 1 + (Fs/Fc)**(2*n) ))

    print("Cut-off Frequency: {} Hz".format(Fc))
    print("Stop-band Frequency: {} Hz".format(Fs))
    print("Pass-band Frequency where gain is [-{} dB]: {} Hz".format(Amax, int(Fp)))
    print("Actual Stop-band Attenuation: {} dB"
          .format(Amin_test_1 if Amin_test_1 == Amin_test_2 else "!!! Test failed {} != {}".format(Amin_test_1,
                                                                                                   Amin_test_2)))
    print("Filter order: {}".format(n))

    print("\n-- 1-st RC figure setup [{} Hz] --".format(Fc1))
    print("R1: {} Ohm".format(R1))
    print("C1: {:.2f} nF".format(C1 * (10 ** 9)))
    print("\n-- 2-st RC figure setup [{} Hz]--".format(Fc2))
    print("R2: {} Ohm".format(R2))
    print("C2: {:.2f} nF".format(C2 * (10 ** 9)))


if __name__ == "__main__":
    main()

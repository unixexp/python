import scipy.signal as sig

sample_rate = 44100
taps = 256
step_hz = 500
freq_min = 2000
freq_max = 6000

def main():
    freq_r = get_frequencies()
    frequencies = freq_r['frequencies']
    steps = freq_r['steps']
    filename = "fir_tables.h"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header(steps))
        f.write( get_c_formated_fir_tables(frequencies, steps) )
        f.write(footer())

    # print(header(steps))
    # print(tables_s)
    # print(footer())

def get_frequencies() -> dict:
    frequencies = list(range(freq_min, freq_max + step_hz, step_hz))
    return {'frequencies': frequencies, 'steps': len(frequencies)}

def get_c_formated_fir_tables(frequencies, steps) -> str:
    lpf_table = []
    hpf_table = []
    symetrical_center = (taps - 1) // 2
    for num, freq in enumerate(frequencies):
        coeffs_lpf = sig.firwin(taps, freq, pass_zero='lowpass', window='hamming', fs=sample_rate)
        coeffs_hpf = [1.0 - x if n == symetrical_center else -x for n, x in enumerate(coeffs_lpf)]

        lpf_gen = _format_table(num, freq, coeffs_lpf, steps, "fir_lpf_table")
        hpf_gen = _format_table(num, freq, coeffs_hpf, steps, "fir_hpf_table")

        lpf_table.extend(lpf_gen)
        hpf_table.extend(hpf_gen)

    return "".join(lpf_table) + "\n" + "".join(hpf_table)

def header(steps: int):
    return (
        "// FIR Look-Up Table (range: {0:d} - {1:d} Hz, step: {2:d}Hz)\n"
        "// Sample rate: {3:d}\n\n"
        "#ifndef FIR_TABLES_H\n"
        "#define FIR_TABLES_H\n\n"
        "#define FIR_TAPS {4:d}\n"
        "#define FILTER_STEPS {5:d}\n"
        "#define FREQ_MIN {6:d}\n"
        "#define FREQ_MAX {7:d}\n"
        "#define STEP_HZ {8:d}\n\n".format(
            freq_min,
            freq_max,
            int(step_hz),
            int(sample_rate),
            taps,
            steps,
            freq_min,
            freq_max,
            step_hz
        )
    )

def footer():
    return "\n\n#endif // FIR_TABLES_H\n"

def _format_table(num: int, freq: int, coeffs_aref: list, steps: int, table: str):
    if num == 0:
        yield "const float {}[FILTER_STEPS][FIR_TAPS] = {{\n".format(table)

    coeffs_str = ", ".join(["{0:.8e}f".format(x) for x in coeffs_aref])

    if num < steps - 1:
        yield "    {{ {0} }},\t// Step {1}: {2} Hz\n".format(coeffs_str, num, freq)
    else:
        yield "    {{ {0} }}\t// Step {1}: {2} Hz\n}};\n".format(coeffs_str, num, freq)

if __name__ == '__main__':
    main()


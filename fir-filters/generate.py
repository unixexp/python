import numpy as np
import sys

def generate_lr4_linear_phase(fs, fc, num_taps):
    taps = 128
    try:
        taps = sys.argv[1]
    except IndexError:
        pass

    # Используем высокую сетку БПФ для точного построения кривой
    n_fft = 16384
    freqs = np.fft.rfftfreq(n_fft, d=1.0/fs)

    # Формула АЧХ фильтра Линквица-Райли 4-го порядка (24 дБ/окт)
    # На частоте fc ослабление ровно 0.5 (-6 дБ)
    with np.errstate(divide='ignore'):
        mag_lpf = 1.0 / (1.0 + (freqs / fc)**4)
        mag_hpf = 1.0 - mag_lpf # Комплементарный ВЧ-фильтр

    # Переводим АЧХ во временную область (нулевая фаза)
    ir_lpf = np.fft.irfft(mag_lpf, n=n_fft)
    ir_hpf = np.fft.irfft(mag_hpf, n=n_fft)

    # Сдвигаем центр импульса в середину массива (делаем фазу линейной)
    ir_lpf = np.fft.fftshift(ir_lpf)
    ir_hpf = np.fft.fftshift(ir_hpf)

    # Вырезаем нужное количество коэффициентов (num_taps) из центра
    center = n_fft // 2
    half = num_taps // 2

    # Берем нечетное окно или симметричный срез и накладываем окно Блэкмана
    taps_lpf = ir_lpf[center - half : center - half + num_taps]
    taps_hpf = ir_hpf[center - half : center - half + num_taps]

    window = np.blackman(num_taps)
    taps_lpf *= window
    taps_hpf *= window

    # Нормировка усиления на постоянном токе (0 Гц) и Найквисте
    taps_lpf /= np.sum(taps_lpf)

    return taps_lpf, taps_hpf

taps = 128
try:
    taps = int(sys.argv[1])
except IndexError:
    pass

lpf, hpf = generate_lr4_linear_phase(fs=44100, fc=3000, num_taps=taps)

print("const float fir_lpf[{}] = {{".format(taps))
print(", ".join(f"{x:.8f}f" for x in lpf))
print("};\n")

print("const float fir_hpf[{}] = {{".format(taps))
print(", ".join(f"{x:.8f}f" for x in hpf))
print("};")


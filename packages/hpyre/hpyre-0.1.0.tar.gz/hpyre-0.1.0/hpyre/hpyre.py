import numpy as np
from itertools import repeat
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import re 
from lecroyscope import Trace
import isfreader 
from itertools import groupby

['numpy', 'pandas', 'scipy', 'matplotlib', 'tkinter', 'lecroyscope', 'isfreader']

def find_nearest(array, value):
  return (np.abs(array - value)).argmin()

def fft_d(timee):
  return (timee[1]-timee[0])

def Z_Series_peaks(arr_v, arr_i, freq, i = -1, peak_number = 10, m = 'n', height = 0.1):

    if m == 'f':
        height = (np.abs(arr_v)).max()*height
        peak_number = 1000
        
    if m == 'n':
        height = (np.abs(arr_v)).max()*height

    peaks, _ = find_peaks(np.abs(arr_v), height = height)

    pk = pd.DataFrame(
        {
            "F": freq[peaks][:peak_number],
            "Z": np.abs(arr_v[peaks])[:peak_number]/np.abs(arr_i[peaks])[:peak_number],
        }
    )

    if i >= 0:
        pk = pk.add_suffix(f' Burst {i}')

    return pk

def VA_Series_peaks(arr_v, arr_i, freq, i = -1, peak_number = 10, m = 'n', height = 0.1):

    if m == 'f':
        height = (np.abs(arr_v)).max()*height
        peak_number = 1000
        
    if m == 'n':
        height = (np.abs(arr_v)).max()*height

    peaks, _ = find_peaks(np.abs(arr_v), height = height)

    pk = pd.DataFrame(
        {
            "F": freq[peaks][:peak_number],
            "V": np.abs(arr_v[peaks])[:peak_number],
            "A": np.abs(arr_i[peaks])[:peak_number],
        }
    )

    if i >= 0:
        pk = pk.add_suffix(f' Burst {i}')

    return pk

def RC_Series_peaks(arr_v, arr_i, freq, i = -1, peak_number = 10, m = 'n', height = 0.1):

    if m == 'f':
        height = (np.abs(arr_v)).max()*height
        peak_number = 1000
        
    if m == 'n':
        height = (np.abs(arr_v)).max()*height

    peaks, _ = find_peaks(np.abs(arr_v), height = height)

    pk = pd.DataFrame(
        {
            "F": freq[peaks][:peak_number],
            "R": np.real(arr_v[peaks][:peak_number]/arr_i[peaks][:peak_number]),
            "C": np.imag(arr_v[peaks][:peak_number]/arr_i[peaks][:peak_number]),
        }
    )

    if i >= 0:
        pk = pk.add_suffix(f' Burst {i}')

    return pk

def Z_peaks(arr_v, arr_i, freq, peak_number = 10, m = 2, height = 0.1):
    Z = Z_Series_peaks(arr_v, arr_i, freq, peak_number, m, height)
    
    f = Z['F'].to_numpy()
    z = Z['Z'].to_numpy()

    return f, z

def VA_peaks(arr_v, arr_i, freq, peak_number = 10, m = 2, height = 0.1):
    VA = VA_Series_peaks(arr_v, arr_i, freq, peak_number, m, height)

    f = VA['F'].to_numpy()
    v = VA['V'].to_numpy()
    a = VA['A'].to_numpy()

    return f, v, a

def RC_peaks(arr_v, arr_i, freq, peak_number = 10, m = 2, height = 0.1):
    RC = RC_Series_peaks(arr_v, arr_i, freq, peak_number, m, height)
    
    f = RC['F'].to_numpy()
    r = RC['R'].to_numpy()
    c = RC['C'].to_numpy()

    return f, r, c

def filter_name(arr, name):
    
    temp = [re.search(name, s) for s in arr]

    if not any(temp):
        raise Exception(f"Didn't find any {name}!")
    
    temp = [False if v is None else True for v in temp]
    t = []
    idx = np.where(temp)[0]
    for k in range(len(idx)):
        t.append(arr[idx[k]])
    return t

def trim(arr_v, arr_i = None, t = None, h = 1/10, m = 'o', p = 5):
    
    mask = np.where(np.abs(arr_v) < np.max(arr_v)*h, 0, arr_v)
    front = len(arr_v) - len(np.trim_zeros(mask, 'f'))
    back = len(arr_v) - len(np.trim_zeros(mask, 'b'))    
    
    if arr_i is None:
        if t is None:
            if m == 'o':
                return arr_v[int((100-p)*front/100):-int((100-p)*back/100)]
            elif m == 'b':
                return arr_v[:-back]
            elif m == 'f':
                return arr_v[front:]
            elif m == 'fb':
                return arr_v[front:-back]
            else:
                raise Exception(f"Wrong trim mode! Expected 'o','f', 'b' or 'fb'. Received '{m}'")
        else:
            if m == 'o':
                return arr_v[int((100-p)*front/100):-int((100-p)*back/100)], t[int((100-p)*front/100):-int((100-p)*back/100)]
            elif m == 'b':
                return arr_v[:-back], t[:-back]
            elif m == 'f':
                return arr_v[front:], t[front:]
            elif m == 'fb':
                return arr_v[front:-back], t[front:-back]
            else:
                raise Exception(f"Wrong trim mode! Expected 'o','f', 'b' or 'fb'. Received '{m}'")
    else:
        if t is None:
            if m == 'o':
                return arr_v[int((100-p)*front/100):-int((100-p)*back/100)], arr_i[int((100-p)*front/100):-int((100-p)*back/100)]
            elif m == 'b':
                return arr_v[:-back], arr_i[:-back]
            elif m == 'f':
                return arr_v[front:], arr_i[front:]
            elif m == 'fb':
                return arr_v[front:-back], arr_i[front:-back]
            else:
                raise Exception(f"Wrong trim mode! Expected 'o','f', 'b' or 'fb'. Received '{m}'")
        else:
            if m == 'o':
                return arr_v[int((100-p)*front/100):-int((100-p)*back/100)], arr_i[int((100-p)*front/100):-int((100-p)*back/100)], t[int((100-p)*front/100):-int((100-p)*back/100)]
            elif m == 'b':
                return arr_v[:-back], arr_i[:-back], t[:-back]
            elif m == 'f':
                return arr_v[front:], arr_i[front:], t[front:]
            elif m == 'fb':
                return arr_v[front:-back], arr_i[front:-back], t[front:-back]
            else:
                raise Exception(f"Wrong trim mode! Expected 'o','f', 'b' or 'fb'. Received '{m}'")

def norm_fft(arr):
    return arr/arr.shape[-1]

def norm_fft_abs(arr):
    return np.abs(arr)/arr.shape[-1]

def ideal_HFIRE(shape, voltage, lenn = 1000, count = 100, m = 'f'):
    
    if len(shape) != 4:
        raise Exception(f"Wrong shape lenghth! Expected 4, received {len(shape)}")

    v_temp = []
    
    for i in np.arange(count):
        v_temp.extend(repeat(voltage,lenn*shape[0]))
        v_temp.extend(repeat(0,lenn*shape[1]))
        v_temp.extend(repeat((-voltage),lenn*shape[2]))
        v_temp.extend(repeat(0,lenn*shape[3]))

    if m == 'b':
         v_temp = np.trim_zeros(v_temp, 'b')
    
    t = np.linspace(0, shape[0]*lenn*1e6*len(v_temp), len(v_temp))

    return t, v_temp

def ideal_IRE(shape, voltage, lenn = 5000, count = 8, m = 'o'):
    
    if len(shape) != 2:
        raise Exception(f"Wrong shape lenghth! Expected 2, received {len(shape)}")

    v_temp = []
    
    for i in np.arange(count):
        v_temp.extend(repeat(voltage,lenn*shape[0]))
        v_temp.extend(repeat(0,lenn*shape[1]))

    if m == 'b':
         v_temp = np.trim_zeros(v_temp, 'b')
    
    t = np.linspace(0, shape[0]*lenn*1e6*len(v_temp), len(v_temp))

    return t, v_temp

def open_single_Lecroy(j = 0):
    filename = fd.askopenfilenames(
        title='Open a file',
        filetypes=(("TRC files", "*.trc"),
                   ("All files", "*.*")))

    return open_path_Lecroy(filename, j = 0)

def open_path_Lecroy(filename, j = 0):
    
    if type(filename)  == str:
        trace_v = Trace(filename)
        
        v = trace_v.voltage
        t = trace_v.time

        return t, v
    
    if len(filename) == 1:

        trace_v = Trace(filename[0])
        
        v = trace_v.voltage
        t = trace_v.time

        return t, v
    
    else:

        a_c1 = filter_name(filename, "C1")
        a_c2 = filter_name(filename, "C2")

        trace_v = Trace(a_c1[j])
        trace_i = Trace(a_c2[j])
        
        v = trace_v.voltage
        i = trace_i.voltage
        t = trace_i.time

        return t, v, i
    
def open_single_Tek(j = 0):
    filename = fd.askopenfilenames(
        title='Open a file',
        filetypes=(("ISF files", "*.isf"),
                   ("All files", "*.*")))

    return open_path_Lecroy(filename, j = 0)

def open_path_Tek(filename, j = 0):

    if type(filename)  == str:
        trace_v = isfreader.read_file(filename)

        t = trace_v[:, 0] 
        v = trace_v[:, 1]  

        return t, v
    
    if len(filename) == 1:

        trace_v = isfreader.read_file(filename[0])

        t = trace_v[:, 0] 
        v = trace_v[:, 1]  

        return t, v
    
    else:

        a_c1 = filter_name(filename, "CH1")
        a_c2 = filter_name(filename, "CH2")

        trace_v = isfreader.read_file(a_c1[j])
        trace_i = isfreader.read_file(a_c2[j])
        
        t = trace_v[:, 0] 
        v = trace_v[:, 1]  
        i = trace_i[:, 1]  

        return t, v, i

def norm_time(arr):
    return arr - np.mean(arr)

def fft_full(arr_v, arr_i = None, t = None):

    fft_v = norm_fft(np.fft.rfft(arr_v))

    if arr_i == None:
        if t == None:
            return fft_v
        else:
            fft_freq = np.fft.rfftfreq(t.shape[-1], d = fft_d(t))
            return fft_freq, fft_v
    else:
        fft_i = norm_fft(np.fft.rfft(arr_i))
        if t == None:
            return fft_v, fft_i
        else:
             return fft_freq, fft_v, fft_i
        
def fft_abs(arr_v, arr_i = None, t = None):

    fft_v = norm_fft_abs(np.fft.rfft(arr_v))

    if arr_i == None:
        if t == None:
            return fft_v
        else:
            fft_freq = np.fft.rfftfreq(t.shape[-1], d = fft_d(t))
            return fft_freq, fft_v
    else:
        fft_i = norm_fft_abs(np.fft.rfft(arr_i))
        if t == None:
            return fft_v, fft_i
        else:
             return fft_freq, fft_v, fft_i
        
def FAST_split(v, i, t, a, b):
    return np.split(v, [a, b]), np.split(i, [a, b]), np.split(t, [a, b])

def FAST_split_single(v, a, b):
    return np.split(v, [a, b])

def FAST_split_values(filename_FAST):

    print(filename_FAST[0])
    voltage, timee = open_path_Lecroy(filename_FAST)

    print("\n\n")

    plt.figure(figsize=(10,6))
    plt.plot(1e3*timee, voltage)
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude (V)")
    plt.grid()
    plt.show()

    print("\n\n")

    pa = float(input("First break point (in ms):"))
    pb = float(input("Second break point (in ms):"))

    return pa, pb

def time_multiple_Lecroy(filename = None):

    if filename == None:
        filename = fd.askopenfilenames(
            title='Open a file',
            filetypes=(("TRC files", "*.trc"),
                    ("All files", "*.*")))
    
    trace = Trace(filename[0])
    v = trace.voltage

    voltage = np.zeros(len(v))
    current = np.zeros(len(v))
    time = np.zeros(len(v))

    for j in range(len(filename)):

        a_c1 = filter_name(filename, "C1")
        a_c2 = filter_name(filename, "C2")

        trace_v = Trace(a_c1[j])
        trace_i = Trace(a_c2[j])
        
        v = trace_v.voltage
        i = trace_i.voltage
        t = trace_i.time
        
        voltage = np.vstack((voltage, v))
        current = np.vstack((current, i))
        time = np.vstack((time, t)) 

    voltage = voltage[1:]
    current = current[1:]
    time = time[1:]

    return time, voltage, current

def freq_multiple_Lecroy(filename = None, m = 'abs'):

    if filename == None:
        filename = fd.askopenfilenames(
            title='Open a file',
            filetypes=(("TRC files", "*.trc"),
                    ("All files", "*.*")))
    
    trace = Trace(filename[0])
    v = trace.voltage

    lfftv = len(np.rfft(v))

    voltage = np.zeros(lfftv)
    current = np.zeros(lfftv)
    freq = np.zeros(lfftv)

    for j in range(len(filename)):

        a_c1 = filter_name(filename, "C1")
        a_c2 = filter_name(filename, "C2")

        trace_v = Trace(a_c1[j])
        trace_i = Trace(a_c2[j])
        
        v = trace_v.voltage
        i = trace_i.voltage
        t = trace_i.time
        
        if m == 'abs':
            F, V, I = fft_abs(v, i, t)
        elif m == 'full':
            F, V, I = fft_full(v, i, t)
        else:
            raise Exception(f"Wrong FFT mode! Expected 'abs' or 'full', received {m}.")

        voltage = np.vstack((voltage, V))
        current = np.vstack((current, I))
        freq = np.vstack((freq, F))

    voltage = voltage[1:]
    current = current[1:]
    freq = freq[1:]

    return freq, voltage, current

def Circuit_response(voltage, current, time, R_V, R_I, C):

    h_V = np.exp(-time/(R_V*C))
    h_I = np.exp(-time/(R_I*C))
    out_V = signal.fftconvolve(h_V, voltage, mode='full', axes=None)/R_V
    out_I = signal.fftconvolve(h_I, current, mode='full', axes=None)/R_I

    return time, out_V[:len(time)], out_I[:len(time)]

def Circuit_final_value(voltage, current, time, R_V, R_I, C, h = 0.9, m = 'mean'):
    
    _, out_V, out_I = Circuit_response(voltage, current, time, R_V, R_I, C)
    
    if m == 'mean':
        mask_V = np.where(np.abs(out_V) < np.max(out_V)*h, 0, np.abs(out_V))
        mask_I = np.where(np.abs(out_I) < np.max(out_I)*h, 0, np.abs(out_I))
        
        a_V = [list(g) for k, g in groupby(mask_V, key=lambda x:x!=0) if k]
        a_I = [list(g) for k, g in groupby(mask_I, key=lambda x:x!=0) if k]
        
        max_V = []
        max_I = []
        
        for k in range(len(a_V) - 1):
            max_V.append(np.max(a_V[k]))
            max_I.append(np.max(a_I[k]))

        return np.mean(max_V), np.mean(max_I)
    
    elif m == 'max':
        return np.max(out_V), np.max(out_I)
    
    else:
        raise Exception(f"Wrong Circuit mode! Expected 'mean' or 'max', received {m}.")

def time_multiple_Tek(filename = None):

    if filename == None:
        filename = fd.askopenfilenames(
            title='Open a file',
            filetypes=(("TRC files", "*.trc"),
                    ("All files", "*.*")))
        
    trace_v = isfreader.read_file(filename[0])
    v = trace_v[:, 1]

    voltage = np.zeros(len(v))
    current = np.zeros(len(v))
    time = np.zeros(len(v))

    for j in range(len(filename)):

        a_c1 = filter_name(filename, "C1")
        a_c2 = filter_name(filename, "C2")

        trace_v = isfreader.read_file(a_c1[j])
        trace_i = isfreader.read_file(a_c2[j])
        
        v = trace_v[:, 1]
        i = trace_i[:, 1]
        t = trace_i[:, 0]
        
        voltage = np.vstack((voltage, v))
        current = np.vstack((current, i))
        time = np.vstack((time, t)) 

    voltage = voltage[1:]
    current = current[1:]
    time = time[1:]

    return time, voltage, current

def freq_multiple_Tek(filename = None, m = 'abs'):

    if filename == None:
        filename = fd.askopenfilenames(
            title='Open a file',
            filetypes=(("TRC files", "*.trc"),
                    ("All files", "*.*")))
    
    trace_v = isfreader.read_file(filename[0])
    v = trace_v[:, 1]

    lfftv = len(np.rfft(v))

    voltage = np.zeros(lfftv)
    current = np.zeros(lfftv)
    freq = np.zeros(lfftv)

    for j in range(len(filename)):

        a_c1 = filter_name(filename, "C1")
        a_c2 = filter_name(filename, "C2")

        trace_v = isfreader.read_file(a_c1[j])
        trace_i = isfreader.read_file(a_c2[j])
        
        v = trace_v[:, 1]
        i = trace_i[:, 1]
        t = trace_i[:, 0]
        
        if m == 'abs':
            F, V, I = fft_abs(v, i, t)
        elif m == 'full':
            F, V, I = fft_full(v, i, t)
        else:
            raise Exception(f"Wrong FFT mode! Expected 'abs' or 'full', received {m}.")

        voltage = np.vstack((voltage, V))
        current = np.vstack((current, I))
        freq = np.vstack((freq, F))

    voltage = voltage[1:]
    current = current[1:]
    freq = freq[1:]

    return freq, voltage, current
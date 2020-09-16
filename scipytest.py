from scipy import zeros, signal, random, fft, arange
import matplotlib.pyplot as plt
from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot

def plotSpectrum(y,Fs):
 """
 Plots a Single-Sided Amplitude Spectrum of y(t)
 """
 n = len(y) # length of the signal
 k = arange(n)
 T = n/Fs
 frq = k/T # two sides frequency range
 frq = frq[range(int(n/2))] # one side frequency range

 Y = fft(y)/n # fft computing and normalization
 Y = Y[range(int(n/2))]
 
 plot(frq,abs(Y),'r') # plotting the spectrum
 xlabel('Freq (Hz)')
 ylabel('|Y(freq)|')


def filter_sbs():
    data = random.random(2000)
    #fig, (ax1, ax2) = plt.subplots(2)
    #fig.suptitle('Vertically stacked subplots')
    
    #ax1.plot(data)
    b, a = signal.iirnotch(10.0, 1.0, 200.0)
    z = signal.lfilter_zi(b, a)
    result = zeros(data.size)
    for i, x in enumerate(data):
        result[i], z = signal.lfilter(b, a, [x], zi=z)
    #ax2.plot(result)
    
    plotSpectrum(result,100)

    plt.show()


    return result

if __name__ == '__main__':
    result = filter_sbs()
    
import numpy as np
import math
from scipy.special import erfcinv
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
from PIL import Image

SHORT_TO_FLOAT_FACTOR = 1 << 15

N_INTERVALS = 300

BEACON_MIN_FREQUENCY = 900
BEACON_MAX_FREQUENCY = 1400
BEACON_FIND_HALF_RANGE_FREQUENCY = 5
BEACON_FIT_HALF_RANGE_FREQUENCY = 2
BEACON_FIT_MAX_EVALUATIONS = 3000
FFT_POINTS = 16384
OVERLAP = 0.9

class Signal:

    def __init__(self, beacon_frequency = None):
        
        self.beacon_frequency = beacon_frequency

    def __eq__(self, other):
        
        if isinstance(other, Signal):

            return (
                self.beacon_frequency == other.beacon_frequency and
                (self.signal_short == other.signal_short).all() and
                (self.signal_float == other.signal_float).all() and
                self.sample_rate == other.sample_rate and
                self.nfft == other.nfft and
                (self.fft == other.fft).all() and
                (self.real_fft_freq == other.real_fft_freq).all() and
                (self.real_fft == other.real_fft).all()
            )

        return False

    def __add__(self, other):

        # todo
        new_signal = Signal()

        return new_signal

    def set(self, signal_short, sample_rate):

        self.signal_short = signal_short
        self.signal_float = self.signal_short.astype(np.float32) / SHORT_TO_FLOAT_FACTOR

        self.sample_rate = sample_rate
        self.nfft = len(self.signal_float)
        self.fft = np.fft.fft(self.signal_float, self.nfft) / self.nfft
        self.real_fft_freq = np.fft.rfftfreq(self.nfft, d = 1 / sample_rate)
        self.real_fft = np.fft.rfft(self.signal_float, self.nfft) / self.nfft

    def process(self, clean=True):

        self.compute_beacon_frequency()
        
        if clean:

            self.clean()

        self.set(self.signal_short, self.sample_rate)
    
    def compute_beacon_frequency(self):

        indices_beacon_range = np.argwhere((self.real_fft_freq >= BEACON_MIN_FREQUENCY) & 
                                             (self.real_fft_freq <= BEACON_MAX_FREQUENCY))
        reduced_real_fft = self.real_fft[indices_beacon_range]
        reduced_real_fft_freq = self.real_fft_freq[indices_beacon_range]
        beacon_index = np.argmax(abs(reduced_real_fft))
        
        self.beacon_frequency = reduced_real_fft_freq[beacon_index][0]
        
    def clean(self):

        """ Remove direct beacon signal from ramplitude_correction signal """

        number_of_samples = len(self.signal_float) 
        
        start_indices = np.zeros(N_INTERVALS, dtype=int)
        end_indices = np.zeros(N_INTERVALS, dtype=int)

        total_time = len(self.signal_float)/self.sample_rate 
        t = np.arange(0, total_time, total_time/len(self.signal_float)) 
        
        number_of_samples_per_interval = np.floor(number_of_samples/N_INTERVALS) 

        for i in range(N_INTERVALS):

            start_indices[i] = i * number_of_samples_per_interval
            end_indices[i] = start_indices[i] + number_of_samples_per_interval - 1

        start_time = t[start_indices]
        end_time = t[end_indices] 
        average_time = (start_time+end_time)/2 
        
        # Extract beacon parameters
        beacon_parameters = self.fit_beacon(start_time, end_time, start_indices, end_indices)
        beacon_frequency = beacon_parameters[:,0] 
        beacon_amplitude = beacon_parameters[:,1] 
        beacon_continuous_phase = beacon_parameters[:,2] 
        fit_residual = beacon_parameters[:,3]
        
        # Interpolate when the residuals are not good enough (just for the selected window)
        median_absolute_deviation_scale = -1 / (math.sqrt(2)*erfcinv(3/2))  
        median_residual = np.median(fit_residual)
        median_absolute_deviation_residual = median_absolute_deviation_scale * np.median(np.abs(fit_residual-median_residual))
        median_absolute_deviation_limit = median_residual + 3*median_absolute_deviation_residual
    
        good_fit_indices = np.where(fit_residual < median_absolute_deviation_limit)[0]  # Correct fit indices
        bad_fit_indices = np.setdiff1d(np.arange(N_INTERVALS), good_fit_indices)
    
        good_fit_amplitude = beacon_amplitude[good_fit_indices]
        good_fit_frequency = beacon_frequency[good_fit_indices]
        good_fit_beacon_continuous_phase = beacon_continuous_phase[good_fit_indices]
    
        good_fit_average_time = average_time[good_fit_indices]
    
        corrected_beacon_amplitude = interp1d(good_fit_average_time, good_fit_amplitude, kind = 'linear', fill_value = 'extrapolate')(average_time)
        corrected_beacon_frequency = interp1d(good_fit_average_time, good_fit_frequency, kind = 'linear', fill_value = 'extrapolate')(average_time)
    
        corrected_beacon_continuous_phase = np.zeros(N_INTERVALS)
        corrected_beacon_continuous_phase[good_fit_indices] = good_fit_beacon_continuous_phase
    
        # Phase interpolation -
        # We move all the phases with reference to the badly fitted interval and then interpolate linearly
        for bad_fit_index in bad_fit_indices:
            
            greater_indices = good_fit_indices[good_fit_indices > bad_fit_index]
            smaller_indices = good_fit_indices[good_fit_indices < bad_fit_index]

            if greater_indices.any():
                closest_greater_index = np.argmin(np.abs(greater_indices - bad_fit_index))
                closest_greater = greater_indices[closest_greater_index]
                closest_greater_phase = beacon_continuous_phase[closest_greater]
                closest_greater_phase_shifted = closest_greater_phase - 2 * np.pi * (start_time[closest_greater]-start_time[bad_fit_index]) * corrected_beacon_frequency[bad_fit_index]
                
            if smaller_indices.any():
                closest_smaller_index = np.argmin(np.abs(smaller_indices - bad_fit_index))
                closest_smaller = smaller_indices[closest_smaller_index]
                closest_smaller_phase = beacon_continuous_phase[closest_smaller]
                closest_smaller_phase_shifted = closest_smaller_phase - 2 * np.pi * (start_time[closest_smaller]-start_time[bad_fit_index]) * corrected_beacon_frequency[bad_fit_index]
                
            if not smaller_indices.any():           
                corrected_beacon_continuous_phase[bad_fit_index] = closest_greater_phase_shifted
                
            elif not greater_indices.any():
                corrected_beacon_continuous_phase[bad_fit_index] = closest_smaller_phase_shifted
                
            else:     
                closest_indices = [closest_smaller, closest_greater]
                closest_phases = np.unwrap([closest_smaller_phase_shifted, closest_greater_phase_shifted])  # Avoid shift greater than pi
                corrected_beacon_continuous_phase[bad_fit_index] = np.interp(bad_fit_index, closest_indices, closest_phases)
        
        # Corrected beacon signal after interpolation
        
        corrected_beacon = np.zeros(len(self.signal_float))
        for j in range(N_INTERVALS):
            corrected_beacon[start_indices[j]:end_indices[j]] = corrected_beacon_amplitude[j] * np.cos(2*np.pi*corrected_beacon_frequency[j]*(t[start_indices[j]:end_indices[j]]-start_time[j]) + corrected_beacon_continuous_phase[j])
        
        self.signal_float = np.clip(self.signal_float - corrected_beacon, -1, 1)
        self.signal_short = (self.signal_float * (SHORT_TO_FLOAT_FACTOR - 1)).astype(np.int32)
             
    def fit_beacon(self, start_time, end_time, start_indices, end_indices):
        """ Fit the amplitude, frequency and phase of the beacon signal """
        
        beacon_min_frequency = self.beacon_frequency - BEACON_FIND_HALF_RANGE_FREQUENCY  # Minimum frequency for the beacon reconstruction
        beacon_max_frequency = self.beacon_frequency + BEACON_FIND_HALF_RANGE_FREQUENCY  # Maximum frequency for the beacon reconstruction
        
        beacon_parameters = np.zeros((N_INTERVALS, 4))

        for j in range(N_INTERVALS):

            # Fit initialization
            start_index = int(start_indices[j])
            end_index = int(end_indices[j])

            signal_interval = self.signal_float[start_index:end_index+1]
            signal_length = len(signal_interval)

            hanning_window = np.hanning(signal_length)
            amplitude_correction = len(hanning_window) / (sum(hanning_window))
            corrected_hanning_window = hanning_window * amplitude_correction
            corrected_signal_interval = signal_interval * corrected_hanning_window
           
            # Fft computation
            complex_fft_interval = np.fft.fft(corrected_signal_interval, signal_length) / signal_length
            real_fft_interval = np.fft.rfft(corrected_signal_interval, signal_length) / signal_length
            magn_fft_interval = abs(real_fft_interval)
            magn_fft_interval[1 : -1] = 2*abs(magn_fft_interval[1 : -1])
            real_fft_freq_interval = np.fft.rfftfreq(signal_length, d = 1 / self.sample_rate)

            # Look for the Fft peak inside interval around beacon frequency
            min_frequency_index = np.argmin(np.abs(real_fft_freq_interval - beacon_min_frequency))
            max_frequency_index = np.argmin(np.abs(real_fft_freq_interval - beacon_max_frequency))
            local_peak_frequency_index = np.argmax(magn_fft_interval[min_frequency_index:max_frequency_index+1])
            peak_frequency_index = local_peak_frequency_index + min_frequency_index

            # Set-up of beacon fit
            number_of_points_beacon_fit = round(BEACON_FIT_HALF_RANGE_FREQUENCY * signal_length / self.sample_rate)
            frequency_indices_to_fit = np.arange(peak_frequency_index - number_of_points_beacon_fit, peak_frequency_index + number_of_points_beacon_fit + 1)
            signal_to_fit = magn_fft_interval[peak_frequency_index - number_of_points_beacon_fit:peak_frequency_index + number_of_points_beacon_fit + 1]

            # Initial guess determination
            if magn_fft_interval[peak_frequency_index-1]>magn_fft_interval[peak_frequency_index+1]:
                initial_guess_fit = np.array([magn_fft_interval[peak_frequency_index], peak_frequency_index-0.01])
            else:
                initial_guess_fit = np.array([magn_fft_interval[peak_frequency_index], peak_frequency_index+0.01])
                        
            # Fit
            fit_parameters, _  = curve_fit(self.hanning_window_function, frequency_indices_to_fit, signal_to_fit, initial_guess_fit, method = 'trf', maxfev = BEACON_FIT_MAX_EVALUATIONS)
            fit_residuals = signal_to_fit - self.hanning_window_function(frequency_indices_to_fit, *fit_parameters)
            fit_residuals_norm = np.sum(fit_residuals**2)
             
            # Frequency and amplitude retrieval
            beacon_amplitude = fit_parameters[0]
            beacon_frequency = fit_parameters[1]*self.sample_rate/signal_length  # Retrieve the frequency from the best freq index
            
            # Phase computation
            beacon_discrete_phase = np.angle(complex_fft_interval[peak_frequency_index])
            beacon_continuous_phase = beacon_discrete_phase - (fit_parameters[1] - peak_frequency_index)*np.pi*(signal_length-1)/signal_length  # Correction to have phase at continuous max
            
            # Set output values
            beacon_parameters[j,0] = beacon_frequency
            beacon_parameters[j,1] = beacon_amplitude
            beacon_parameters[j,2] = beacon_continuous_phase
            beacon_parameters[j,3] = fit_residuals_norm

        return beacon_parameters
    
    def hanning_window_function(self, freq_index, ampl, freq):
        return ampl * np.abs(np.sinc(freq - freq_index) / (1 - (freq - freq_index)**2))
    
    def plot_spectrogram(self, half_range_spect = 100, export=False, filename=None):
    
        # Compute spectrogram
        freq_vector, time_vector, spect = spectrogram(self.signal_float, fs=self.sample_rate, window='hann', nperseg=FFT_POINTS, noverlap=OVERLAP * FFT_POINTS, mode='magnitude')

        spect = np.abs(spect)
        df = self.sample_rate / self.nfft

        filter = np.logical_and(freq_vector >= (self.beacon_frequency - half_range_spect), freq_vector <= (self.beacon_frequency + half_range_spect))
        freq_vector = freq_vector[filter]
        spect = spect[filter,:]

        # Compute spectrogram stats
        spect_max = np.max(spect)
        spect_mu = np.mean(spect)

        # Display spectrogram in dB.
        plt.figure()
        plt.pcolormesh(time_vector, freq_vector, 10 * np.log10(spect / spect_max), cmap='jet')
        plt.axis('tight')

        # Set colorbar limits and display it.
        cmin, cmax = plt.gci().get_clim()
        plt.clim(10 * np.log10(spect_mu / spect_max), cmax)
        plt.colorbar()

        # Set figure title and labels
        plt.title("Spectrogram")
        plt.xlabel('Time [s]')
        plt.ylabel('Freq [Hz]')

        if export:

            save_path = filename if filename else "spectrogram.png"
            plt.savefig(save_path)

        else:
        
            plt.show() 

        plt.close()   
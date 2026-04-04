# ================================================================
# Active Noise Cancellation (ANC) Software for Headphones
# Implementation using Filtered-x Least Mean Squares (FxLMS) Algorithm
# ================================================================

import numpy as np
import pyaudio
from scipy import signal
import matplotlib.pyplot as plt



class FxLMSFilter:
    """
    Filtered-x Least Mean Squares (FxLMS) adaptive filter for Active Noise Cancellation (ANC)
    """

    def __init__(self, filter_length=256, step_size=0.01, secondary_path_length=128):
        """
        Initialize the FxLMS filter
        
        Parameters:
        - filter_length: Length of the adaptive filter (control filter)
        - step_size: Learning rate (mu), controls convergence speed
        - secondary_path_length: Length of secondary path estimate
        """
        self.filter_length = filter_length
        self.step_size = step_size

        # Adaptive filter coefficients
        self.w = np.zeros(filter_length)

        # Secondary path estimate (impulse response)
        self.secondary_path = np.zeros(secondary_path_length)

        # Reference signal buffers
        self.x_buffer = np.zeros(filter_length)
        self.x_filtered_buffer = np.zeros(filter_length)

    def estimate_secondary_path(self, training_signal, training_response):
        """
        Estimate the secondary path using cross-correlation method.
        """
        # Use normalized cross-correlation to estimate impulse response
        corr = signal.correlate(training_response, training_signal, mode='full')
        mid = len(corr) // 2
        estimate = corr[mid : mid + len(self.secondary_path)]
        self.secondary_path = estimate / (np.max(np.abs(estimate)) + 1e-8)

    def update(self, reference_signal, error_signal):
        """
        Update filter coefficients using FxLMS algorithm
        
        Parameters:
        - reference_signal: Current reference signal sample
        - error_signal: Current error signal sample
        
        Returns:
        - anti_noise: Generated anti-noise signal
        """
        # Shift reference buffer
        self.x_buffer = np.roll(self.x_buffer, 1)
        self.x_buffer[0] = reference_signal

        # Generate anti-noise signal
        anti_noise = np.dot(self.w, self.x_buffer)

        # Filter reference signal through secondary path estimate
        x_filtered = np.convolve(self.x_buffer, self.secondary_path, mode='same')

        # Update buffer for filtered reference
        self.x_filtered_buffer = np.roll(self.x_filtered_buffer, 1)
        self.x_filtered_buffer[0] = x_filtered[0]

        # Update adaptive filter weights (FxLMS rule)
        self.w = self.w + self.step_size * error_signal * self.x_filtered_buffer

        return anti_noise



class LMSFilter:
    """
    Standard Least Mean Squares (LMS) adaptive filter
    """

    def __init__(self, filter_length=256, step_size=0.01):
        self.filter_length = filter_length
        self.step_size = step_size
        self.w = np.zeros(filter_length)
        self.x_buffer = np.zeros(filter_length)

    def update(self, input_signal, desired_signal):
        """
        Update LMS filter and return output + error
        """
        self.x_buffer = np.roll(self.x_buffer, 1)
        self.x_buffer[0] = input_signal

        output = np.dot(self.w, self.x_buffer)
        error = desired_signal - output
        self.w = self.w + self.step_size * error * self.x_buffer

        return output, error



class RealtimeANC:
    """
    Real-time Active Noise Cancellation System
    """

    def __init__(self, mode='feedforward', sample_rate=48000, chunk_size=256):
        self.mode = mode
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()

        # Initialize adaptive filters
        if mode in ['feedforward', 'hybrid']:
            self.feedforward_filter = FxLMSFilter(filter_length=256, step_size=0.001)

        if mode in ['feedback', 'hybrid']:
            self.feedback_filter = LMSFilter(filter_length=128, step_size=0.005)

        self.error_history = []

    def start_anc(self, duration=10):
        """
        Start ANC in real time
        """
        print(f"Starting {self.mode} ANC for {duration} seconds...")

        # Input/output streams
        if self.mode in ['feedforward', 'hybrid']:
            stream_ref = self.p.open(
                format=pyaudio.paFloat32,
                channels=2,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                input_device_index=7  # Change to specific mic if needed
            )

        stream_error = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            input_device_index=8
        )

        stream_output = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            output=True,
            frames_per_buffer=self.chunk_size,
             output_device_index=10
        )

        num_frames = int(duration * self.sample_rate / self.chunk_size)

        for frame_idx in range(num_frames):
            if self.mode in ['feedforward', 'hybrid']:
                ref_data = np.frombuffer(stream_ref.read(self.chunk_size), dtype=np.float32)

            error_data = np.frombuffer(stream_error.read(self.chunk_size), dtype=np.float32)
            anti_noise_chunk = np.zeros(self.chunk_size, dtype=np.float32)

            for i in range(self.chunk_size):
                if self.mode == 'feedforward':
                    anti_noise = self.feedforward_filter.update(ref_data[i], error_data[i])
                elif self.mode == 'feedback':
                    anti_noise, _ = self.feedback_filter.update(error_data[i], 0)
                elif self.mode == 'hybrid':
                    anti_noise_ff = self.feedforward_filter.update(ref_data[i], error_data[i])
                    anti_noise_fb, _ = self.feedback_filter.update(error_data[i], 0)
                    anti_noise = 0.6 * anti_noise_ff + 0.4 * anti_noise_fb

                anti_noise_chunk[i] = anti_noise

            self.error_history.extend(error_data.tolist())
            stream_output.write(anti_noise_chunk.tobytes())

            if frame_idx % 50 == 0:
                avg_error = np.mean(np.abs(error_data))
                print(f"Frame {frame_idx}/{num_frames}, Avg Error: {avg_error:.6f}")

        # Close all streams
        if self.mode in ['feedforward', 'hybrid']:
            stream_ref.stop_stream()
            stream_ref.close()
        stream_error.stop_stream()
        stream_error.close()
        stream_output.stop_stream()
        stream_output.close()
        print("ANC stopped.")

    def plot_performance(self):
        """
        Plot error signal performance
        """
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(self.error_history[:5000])
        plt.title('Error Signal Over Time')
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.grid(True)

        plt.subplot(2, 1, 2)
        frequencies = np.fft.rfftfreq(len(self.error_history[:5000]), 1/self.sample_rate)
        fft_vals = np.abs(np.fft.rfft(self.error_history[:5000]))
        plt.plot(frequencies, 20 * np.log10(fft_vals + 1e-10))
        plt.title('Error Signal Frequency Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude (dB)')
        plt.grid(True)
        plt.xlim(0, 2000)

        plt.tight_layout()
        plt.savefig('anc_performance.png', dpi=150)
        plt.close()

    def cleanup(self):
        self.p.terminate()


# ================================================================
# Simulation Mode (no hardware required)
# ================================================================
class SimulatedANC:
    """
    Simulated ANC system for algorithm testing without hardware
    """

    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.filter = FxLMSFilter(filter_length=128, step_size=0.01)

    def simulate(self, duration=2.0):
        """
        Run ANC simulation with synthetic noise
        """
        t = np.linspace(0, duration, int(duration * self.sample_rate))

        # Primary noise (what we want to cancel)
        primary_noise = (
            0.5 * np.sin(2 * np.pi * 100 * t) +
            0.3 * np.sin(2 * np.pi * 250 * t) +
            0.2 * np.sin(2 * np.pi * 500 * t) +
            0.1 * np.random.randn(len(t))
        )

        # Secondary path (speaker-to-ear transfer function)
        secondary_path_ir = signal.firwin(64, 0.5)
        self.filter.secondary_path = secondary_path_ir

        anti_noise = np.zeros_like(primary_noise)
        error_signal = np.zeros_like(primary_noise)

        for i in range(len(primary_noise)):
            anti_noise[i] = self.filter.update(primary_noise[i], error_signal[i])
            if i > 0:
                anti_noise_delayed = np.convolve(anti_noise[:i+1], secondary_path_ir, mode='same')[-1]
            else:
                anti_noise_delayed = 0
            error_signal[i] = primary_noise[i] + anti_noise_delayed

        noise_reduction_db = 20 * np.log10(
            np.std(primary_noise) / (np.std(error_signal[-1000:]) + 1e-10)
        )

        print(f"Noise Reduction: {noise_reduction_db:.2f} dB")
        return primary_noise, anti_noise, error_signal


# ================================================================
# Main Execution
# ================================================================
if __name__ == "__main__":
    print("ANC Software for Headphones")
    print("=" * 50)

    # Run simulation mode
    print("\nRunning Simulation...")
    sim_anc = SimulatedANC(sample_rate=48000)
    primary, anti, error = sim_anc.simulate(duration=2.0)

    print(f"Primary noise RMS: {np.std(primary):.4f}")
    print(f"Error signal RMS: {np.std(error[-1000:]):.4f}")

    # Uncomment for real-time testing (requires hardware)
    # anc_system = RealtimeANC(mode='feedforward', sample_rate=48000, chunk_size=256)
    # anc_system.start_anc(duration=10)
    # anc_system.plot_performance()
    # anc_system.cleanup()

    print("\nANC software ready!")

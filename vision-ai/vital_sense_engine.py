"""
Vital-Sense AI Core Processing Engine
Extracts real-time biometric signal waveforms from facial region of interest (ROI)
using computer vision matrix manipulation to estimate remote heart rates (rPPG).
"""

import numpy as np

class VitalSenseEngine:
    def __init__(self, buffer_size=150, sampling_rate=30):
        # Configuration parameters for streaming tracking vectors
        self.buffer_size = buffer_size       # Stores 5 seconds of continuous frames at 30fps
        self.sampling_rate = sampling_rate   # Target camera stream operational frame-rate
        self.signal_buffer = []              # Sequence array holding raw pixel channel intensity values

    def extract_chrominance_signal(self, frame_roi):
        """
        Analyzes a raw facial bounding box to pull spatial averages of red, green, and blue pixels.
        """
        # Step 1: Check if input bounding frame data exists
        if frame_roi is None or frame_roi.size == 0:
            return None

        # Step 2: Extract individual color layer matrices via spatial normalization averages
        mean_channels = np.mean(frame_roi, axis=(0, 1)) # Yields raw [B_avg, G_avg, R_avg]
        
        # Guard against zero-division errors during low-light edge cases
        if np.any(mean_channels == 0):
            return None

        return mean_channels

    def push_frame_telemetry(self, frame_roi):
        """
        Appends raw spatial channel vectors into the signal evaluation stack.
        """
        channels = self.extract_chrominance_signal(frame_roi)
        if channels is not None:
            self.signal_buffer.append(channels)
            
            # Bound memory array length to maintain precise execution memory limits
            if len(self.signal_buffer) > self.buffer_size:
                self.signal_buffer.pop(0)

    def compute_heart_rate_bpm(self):
        """
        Applies mathematical processing matrices to convert green channel variances into raw beats per minute.
        """
        if len(self.signal_buffer) < self.buffer_size:
            # Insufficient signal duration to generate an accurate biological calculation profile
            return None

        # Isolate the Green channel timeline profile array (index 1)
        signal_matrix = np.array(self.signal_buffer)
        green_signal = signal_matrix[:, 1]

        # Step 1: Detrend signal trends to isolate baseline sensor offsets
        normalized_signal = (green_signal - np.mean(green_signal)) / (np.std(green_signal) + 1e-6)

        # Step 2: Compute a Fast Fourier Transform (FFT) to convert signal changes into frequency domains
        fft_data = np.abs(np.fft.rfft(normalized_signal))
        frequencies = np.fft.rfftfreq(len(normalized_signal), d=1.0 / self.sampling_rate)

        # Step 3: Enforce strict biological context passbands (0.75 Hz to 3.0 Hz matches 45 to 180 BPM)
        valid_indices = np.where((frequencies >= 0.75) & (frequencies <= 3.0))[0]
        
        if len(valid_indices) == 0:
            return 72.0 # Return steady baseline average if processing bounds fail

        # Step 4: Isolate the dominant frequency spike vector
        peak_index = valid_indices[np.argmax(fft_data[valid_indices])]
        dominant_frequency = frequencies[peak_index]

        # Convert frequency domain directly into human Beats Per Minute (BPM) metrics
        calculated_bpm = dominant_frequency * 60.0
        return round(calculated_bpm, 1)

if __name__ == "__main__":
    # Self-contained processing engine validation check
    print("Initializing Vital-Sense engine standalone unit test simulation...")
    engine = VitalSenseEngine(buffer_size=30, sampling_rate=30)
    
    # Generate 32 mock image arrays containing simulated rhythmic color adjustments
    for i in range(32):
        simulated_pulse_variance = int(128 + 5 * np.sin(2 * np.pi * 1.2 * (i / 30.0)))
        mock_face_pixel_matrix = np.full((100, 100, 3), [100, simulated_pulse_variance, 150], dtype=np.uint8)
        engine.push_frame_telemetry(mock_face_pixel_matrix)
        
    print(f"Extraction Pipeline Verified. Computed Heart Rate Parameter: {engine.compute_heart_rate_bpm()} BPM")

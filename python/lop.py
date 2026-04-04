import pyaudio
import numpy as np

CHUNK = 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream_in = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)

stream_out = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

try:
    while True:
        input_bytes = stream_in.read(CHUNK)
        input_signal = np.frombuffer(input_bytes, dtype=np.int16)

        # Simple anti-phase
        anti_signal = -input_signal

        output_bytes = anti_signal.astype(np.int16).tobytes()
        stream_out.write(output_bytes)
except KeyboardInterrupt:
    pass

stream_in.stop_stream()
stream_in.close()
stream_out.stop_stream()
stream_out.close()
p.terminate()

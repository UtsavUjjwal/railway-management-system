import pyaudio

p = pyaudio.PyAudio()
print("=== Available Audio Devices ===\n")

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")
    print(f"  Input Channels: {info['maxInputChannels']}")
    print(f"  Output Channels: {info['maxOutputChannels']}")
    print(f"  Sample Rate: {int(info['defaultSampleRate'])} Hz")
    print()

p.terminate()
print("Write down the device numbers for your microphones and speakers!")

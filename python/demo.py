from anc_software_implementation import RealtimeANC

anc = RealtimeANC(mode='feedforward', sample_rate=48000, chunk_size=256)
anc.start_anc(duration=10)
anc.plot_performance()
anc.cleanup()

from anc_software_implementation import RealtimeANC

# Create ANC system in feedback mode (easier, needs only error mic)
print("Starting ANC in Feedback Mode...")
print("This uses only the internal error microphone")
print("\n Starting at low volume for safety...")

anc_system = RealtimeANC(
    mode='feedback',
    sample_rate=48000,
    chunk_size=256
)

# Run for 10 seconds
anc_system.start_anc(duration=10)

# Show performance
anc_system.plot_performance()

# Clean up
anc_system.cleanup()

print("\nANC test complete!")

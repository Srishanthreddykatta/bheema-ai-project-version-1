def fatigue_score(rep_times, rom_values):
    """Calculate fatigue score based on rep times and range of motion."""
    if not rep_times or not rom_values:
        return 0
    
    import statistics
    
    # Average rep time (slower reps = more fatigue)
    avg_time = statistics.mean(rep_times) if rep_times else 1.0
    time_fatigue = min(100, (avg_time / 2.0) * 100)  # Normalized to ~2 sec/rep
    
    # Average ROM (lower ROM = more fatigue)
    avg_rom = statistics.mean(rom_values) if rom_values else 90
    rom_fatigue = max(0, 100 - (avg_rom / 120.0) * 100)  # Normalized to 120 degrees max
    
    # Combined fatigue score
    fatigue = (time_fatigue + rom_fatigue) / 2.0
    return min(100, fatigue)

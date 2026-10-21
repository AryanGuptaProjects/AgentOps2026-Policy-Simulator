import numpy as np

def initialize_city_grid() -> np.ndarray:
    """Initializes a 10x10 city grid filled with baseline pollution levels (0.0)."""
    # 32-bit floats for reduced memory footprint and faster cache alignment
    return np.zeros((10, 10), dtype=np.float32)

def _apply_diffusion_and_decay(grid: np.ndarray, diffusion_rate: float = 0.15, decay_rate: float = 0.02) -> np.ndarray:
    """
    Applies spatial diffusion using a 4-neighbor finite difference stencil in pure NumPy.
    Pollution organically spreads to adjacent cells and slowly dissipates over time.
    """
    # Pad array edges to handle boundary conditions without loops
    padded = np.pad(grid, pad_width=1, mode='edge')
    
    # Calculate 4-neighbor spatial average via vector slicing (Up, Down, Left, Right)
    neighbors_avg = (
        padded[:-2, 1:-1] +  # Up
        padded[2:, 1:-1]  +  # Down
        padded[1:-1, :-2] +  # Left
        padded[1:-1, 2:]     # Right
    ) / 4.0

    # Smooth pollution across cells and apply natural atmospheric decay
    diffused_grid = (1.0 - diffusion_rate) * grid + diffusion_rate * neighbors_avg
    diffused_grid *= (1.0 - decay_rate)
    
    return diffused_grid

def update_grid_emissions(current_grid: np.ndarray, demographic_actions: list) -> np.ndarray:
    """
    Takes agent JSON outputs, updates spatial pollution matrices deterministically,
    and calculates atmospheric diffusion across the city grid.
    """
    updated_grid = current_grid.copy()
    
    # Define boolean spatial masks
    city_center_mask = np.zeros((10, 10), dtype=bool)
    city_center_mask[3:7, 3:7] = True
    suburbs_mask = ~city_center_mask

    # Aggregate total impact scores to minimize array writes
    total_suburb_impact = 0.0
    total_center_impact = 0.0

    for action in demographic_actions:
        target_zone = action.get("targeted_zone", "Suburbs")
        multiplier = float(action.get("emissions_multiplier", 1.0))
        vehicle_count = int(action.get("rerouted_vehicles", 10))
        
        impact = multiplier * (vehicle_count / 10.0)
        
        if target_zone == "Suburbs":
            total_suburb_impact += impact
        elif target_zone == "City Center":
            total_center_impact += impact

    # Apply vectorized impacts
    updated_grid[suburbs_mask] += total_suburb_impact
    updated_grid[city_center_mask] += total_center_impact

    # Run the pure NumPy spatial diffusion pass
    final_grid = _apply_diffusion_and_decay(updated_grid)

    return np.round(final_grid, 2)

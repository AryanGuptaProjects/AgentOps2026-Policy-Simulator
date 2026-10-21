import numpy as np

def initialize_city_grid() -> np.ndarray:
    """Initializes a 10x10 city grid filled with baseline pollution levels (0.0)."""
    # The matrix starts initialized to zeros, representing baseline air quality.
    return np.zeros((10, 10), dtype=float)

def update_grid_emissions(current_grid: np.ndarray, demographic_actions: list) -> np.ndarray:
    """
    Takes the agent JSON outputs and deterministically updates pollution values on the matrix.
    """
    updated_grid = current_grid.copy()
    
    # Define spatial masks[cite: 1]
    city_center_mask = np.zeros((10, 10), dtype=bool)
    # City Center (Indices [3:7, 3:7]) represents the downtown regulated zone[cite: 1].
    city_center_mask[3:7, 3:7] = True
    # Suburbs / Outer Ring represents the unregulated periphery[cite: 1].
    suburbs_mask = ~city_center_mask

    # Reads Agent JSON: Loops through each agent's action object[cite: 1].
    for action in demographic_actions:
        target_zone = action.get("targeted_zone", "Suburbs")
        multiplier = float(action.get("emissions_multiplier", 1.0))
        vehicle_count = int(action.get("rerouted_vehicles", 10))
        
        # Calculate impact score[cite: 1]
        impact = multiplier * (vehicle_count / 10.0)
        
        # Apply deterministic math based on targeted geography[cite: 1]
        if target_zone == "Suburbs":
            # Add pollution evenly across outer suburb cells[cite: 1]
            updated_grid[suburbs_mask] += impact
        elif target_zone == "City Center":
            # Add pollution to inner city cells[cite: 1]
            updated_grid[city_center_mask] += impact

    return np.round(updated_grid, 2)

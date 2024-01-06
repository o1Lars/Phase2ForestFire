import random
import matplotlib.pyplot as plt

def generate_mock_data(steps: int) -> tuple[list[int], list[int], list[int], list[int]]:
    """Generate mock test data for tree patches, rock patches, forest fires, and firefighters over time"""

    # Define initial values for the metrics
    initial_tree_patches = 70
    initial_rock_patches = 30
    initial_forest_fires = 10
    initial_firefighters = 8

    # Create lists to store the metrics' values over time
    tree_patches_values = [initial_tree_patches]
    rock_patches_values = [initial_rock_patches]
    forest_fires_values = [initial_forest_fires]
    firefighters_values = [initial_firefighters]

    # Simulate the metrics changing over steps/time
    for _ in range(steps):
        # Generate random changes for each metric value
        tree_change = random.randint(-5, 5)
        rock_change = random.randint(-3, 3)
        fire_change = random.randint(-2, 2)
        firefighters_change = random.randint(-8, 8)

        # Calculate new values for the metrics
        new_tree_value = tree_patches_values[-1] + tree_change
        new_rock_value = rock_patches_values[-1] + rock_change
        new_fire_value = forest_fires_values[-1] + fire_change
        new_firefighters_value = firefighters_values[-1] + firefighters_change

        # Ensure the metric values stay within defined ranges
        new_tree_value = max(0, min(new_tree_value, 100))
        new_rock_value = max(0, min(new_rock_value, 100))
        new_fire_value = max(0, min(new_fire_value, 50))
        new_firefighters_value = max(0, min(new_firefighters_value, 50))

        # Append the new metric values to their respective lists
        tree_patches_values.append(new_tree_value)
        rock_patches_values.append(new_rock_value)
        forest_fires_values.append(new_fire_value)
        firefighters_values.append(new_firefighters_value)

    return tree_patches_values, rock_patches_values, forest_fires_values, firefighters_values

def plot_simulation(steps: int) -> None:
    """Plot the simulation of tree patches, rock patches, forest fires, and firefighters over time"""

    # Generate mock test data
    tree_patches, rock_patches, forest_fires, firefighters = generate_mock_data(steps)

    # Create a list of steps for the x-axis
    step_list = list(range(steps + 1))

    # Create a figure and axis for the plot
    plt.figure(figsize=(10, 6))

    # Plot individual lines for each metric
    plt.plot(step_list, tree_patches, color='r', label='Trees Population')
    plt.plot(step_list, rock_patches, color='b', label='Non-combustible Land')
    plt.plot(step_list, forest_fires, color='g', label='Wildfires')
    plt.plot(step_list, firefighters, color='orange', label='Firefighters')

    # Labels, title, legend, and grid
    plt.xlabel("Simulation Steps")
    plt.ylabel("Count")
    plt.title("Evolution of Wildfire")
    plt.legend(loc="upper right")
    plt.grid(True)

    # Show the plot
    plt.show()

# Define the number of simulation steps
simulation_steps = 100

# Plot the simulation
plot_simulation(steps=simulation_steps)

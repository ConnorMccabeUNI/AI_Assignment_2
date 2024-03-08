import matplotlib.pyplot as plt
import networkx as nx
import random

import numpy as np


# Function to check if there are no conflicts in node coloring
def no_conflicts(G, node_colors, num_colors):
    color_map = [plt.cm.viridis(i / num_colors) for i in range(num_colors)]
    updated_colors = list(node_colors)  # Create a copy of node_colors to update
    for edge in G.edges:
        u, v = edge
        if node_colors[u - 1] == node_colors[v - 1]:
            return False # Conflict found, nodes with same color are connected
    return True # No conflicts found


# Function to check and update colors if two nodes of the same color are connected
def check_same_color_edges(G, node_colors, num_colors):
    color_map = [plt.cm.viridis(i / num_colors) for i in range(num_colors)]
    updated_colors = list(node_colors)  # Create a copy of node_colors to update
    for edge in G.edges:
        u, v = edge
        if node_colors[u - 1] == node_colors[v - 1]:
            # If nodes are of the same color, change the color of one of them
            # print("u-1", updated_colors[u - 1])
            # print("u", updated_colors[u])
            new_color = (random.choice(range(num_colors)) + 1) % num_colors  # Choose a new color
            # print("old Color", updated_colors[new_color])
            if updated_colors[new_color] == updated_colors[u]:
                new_color = (new_color + 1) % num_colors
            # print("new Color", updated_colors[new_color])
            updated_colors[u - 1] = color_map[new_color]
    return updated_colors


# Global variable to determine the number of colors
num_colors = 10
random.seed(2)  # For reproducibility
conflict_count = 0  # Initialize conflict counter

G = nx.Graph()
G.add_nodes_from(range(1, 101))

# Randomly add edges between nodes with a probability of 0.05
for node in G.nodes():
    for potential_neighbor in G.nodes():
        if node != potential_neighbor:
            if np.random.rand() < 0.05:  # Adjust probability to control edge density
                G.add_edge(node, potential_neighbor)

# Use a layout algorithm to position the nodes (spring_layout in this case)
iterative = 1
pos = {}  # This is a dictionary, not a list
for x in range(1, 11):
    for y in range(1, 11):
        pos[iterative] = (x, y)  # Adjusting x and y to start from 0 to match your example
        iterative += 1  # Increment the key for the next iteration

# pos = nx.spring_layout(G, seed=42)

# Generate distinct colors for nodes based on num_colors
color_map = [plt.cm.viridis(i / num_colors) for i in range(num_colors)]
node_colors = [color_map[i % num_colors] for i in range(len(G.nodes))]
print(node_colors)

# other shapes
nx.draw(G, pos, with_labels=True, node_color=node_colors)
# nx.draw(G, with_labels=True, node_color=node_colors)
plt.show()

# Initialize conflict counter
total_conflicts = 0
conflict_list = []

# Iterate to check for conflicts and update colors if necessary
for iteration in range(1, 51):  # Change the range to adjust the number of iterations
    conflicts = 0  # Counter for conflicts in the current iteration
    print(f"Iteration {iteration}:")

    # Check for conflicts and update colors if necessary
    if not no_conflicts(G, node_colors, num_colors):
        # Increment total conflict count
        total_conflicts += 1

        # Check if two nodes of the same color are connected and update colors if necessary
        node_colors = check_same_color_edges(G, node_colors, num_colors)

        # Count the number of conflicts in the current iteration
        for edge in G.edges:
            u, v = edge
            if node_colors[u - 1] == node_colors[v - 1]:
                conflicts += 1

        # Display conflicts in the current iteration
        print(f" - Conflicts in current iteration: {conflicts}")
        print(f" - Total conflicts so far: {total_conflicts}")
        conflict_list.append(conflicts)

        plt.clf()
        # Draw the graph with updated node colors
        nx.draw(G, pos, with_labels=True, node_color=node_colors)
        # plt.show()
    else:
        print(" - No conflicts in current iteration")
        break  # No conflicts found, exit loop

# Display total number of conflicts
print("Total number of conflicts:", total_conflicts)
ypoints = np.array(conflict_list)
plt.clf()
plt.plot(ypoints, color='r')
plt.title("Conflicts per Generation")
plt.xlabel("Generations")
plt.ylabel("Conflicts")
plt.show()

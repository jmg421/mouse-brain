import json
import random
from datetime import datetime

def distance(pos1, pos2):
    """Calculate Euclidean distance between two positions."""
    return ((pos1["x"] - pos2["x"]) ** 2 + (pos1["y"] - pos2["y"]) ** 2) ** 0.5

def generate_tbi_simulation(num_inflammation_nodes, num_damaged_neurons):
    simulation = {
        "metadata": {
            "title": "Mouse Brain TBI Simulation for Nasal Spray Research",
            "description": (
                "Synthetic data simulating TBI effects in a mouse brain, "
                "including inflammation and neuronal damage, to support nasal spray development."
            ),
            "author": "Your Name",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "version": "2.0",
            "investment_goal": "Synthetic data for $8M TBI nasal spray investment"
        },
        "elements": {
            "nodes": [],
            "edges": []
        }
    }

    # Base nodes
    base_nodes = [
        {"data": {"id": "mouse_brain", "label": "Mouse Brain", "node_type": "organ"}, "position": {"x": 0, "y": 0}},
        {
            "data": {
                "id": "tbi_zone",
                "label": "TBI Zone",
                "node_type": "injury",
                "description": "Primary region of traumatic brain injury."
            },
            "position": {"x": 300, "y": 150}
        },
        {"data": {"id": "cortex", "label": "Cortex", "node_type": "brain_region"}, "position": {"x": 100, "y": 100}},
        {"data": {"id": "hippocampus", "label": "Hippocampus", "node_type": "brain_region"}, "position": {"x": 200, "y": 100}}
    ]

    # Neuronal populations
    neuronal_populations = [
        {"data": {"id": "neurons_cortex", "label": "Neurons (Cortex)", "node_type": "neuronal_population"}, "position": {"x": 90, "y": 90}},
        {"data": {"id": "neurons_hippocampus", "label": "Neurons (Hippocampus)", "node_type": "neuronal_population"}, "position": {"x": 190, "y": 90}}
    ]

    simulation["elements"]["nodes"].extend(base_nodes + neuronal_populations)

    # Inflammation nodes (e.g., cytokines, proxies for nasal spray targets)
    for i in range(num_inflammation_nodes):
        x = random.uniform(250, 350)  # Near TBI zone
        y = random.uniform(100, 200)
        inflam_node = {
            "data": {
                "id": f"inflammation_{i}",
                "label": "Inflammation Marker",
                "node_type": "inflammatory",
                "level": random.uniform(0.5, 2.0),  # Synthetic severity metric
                "description": "Elevated inflammation due to TBI, target for nasal spray."
            },
            "position": {"x": x, "y": y}
        }
        simulation["elements"]["nodes"].append(inflam_node)

    # Damaged neuron nodes
    tbi_pos = {"x": 300, "y": 150}
    for i in range(num_damaged_neurons):
        x = random.uniform(200, 400)
        y = random.uniform(50, 250)
        damage_level = 2.0 if distance({"x": x, "y": y}, tbi_pos) < 100 else 1.0
        neuron_node = {
            "data": {
                "id": f"damaged_neuron_{i}",
                "label": "Damaged Neuron",
                "node_type": "neuron",
                "damage_level": damage_level,
                "description": "Neuron affected by TBI, measurable for recovery."
            },
            "position": {"x": x, "y": y}
        }
        simulation["elements"]["nodes"].append(neuron_node)

    # Edges: TBI zone impacts inflammation and neurons
    for i in range(num_inflammation_nodes):
        simulation["elements"]["edges"].append({
            "data": {
                "id": f"tbi_to_inflam_{i}",
                "source": "tbi_zone",
                "target": f"inflammation_{i}",
                "label": "Induces",
                "edge_type": "activates",
                "strength": random.uniform(1.0, 3.0)
            }
        })

    for i in range(num_damaged_neurons):
        simulation["elements"]["edges"].append({
            "data": {
                "id": f"tbi_to_neuron_{i}",
                "source": "tbi_zone",
                "target": f"damaged_neuron_{i}",
                "label": "Damages",
                "edge_type": "damages",
                "strength": random.uniform(1.0, 2.5)
            }
        })

    return simulation

if __name__ == "__main__":
    num_inflammation_nodes = 5000  # Reduced for manageability, adjust as needed
    num_damaged_neurons = 3000
    simulation_data = generate_tbi_simulation(num_inflammation_nodes, num_damaged_neurons)
    
    filename = f"data/synthetic/mouse_brain_tbi_simulation_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(filename, "w") as outfile:
        json.dump(simulation_data, outfile, indent=2)
    
    print(f"TBI simulation with {num_inflammation_nodes} inflammation nodes and "
          f"{num_damaged_neurons} damaged neurons saved to '{filename}'")

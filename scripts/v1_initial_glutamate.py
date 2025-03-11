import json
import random

def distance(pos1, pos2):
    """Calculate Euclidean distance between two positions."""
    return ((pos1["x"] - pos2["x"]) ** 2 + (pos1["y"] - pos2["y"]) ** 2) ** 0.5

def generate_simulated_brain(num_glutamate_nodes):
    simulation = {
        "metadata": {
            "title": "Expanded Mouse Brain Neural Network Simulation with Many Glutamate Nodes",
            "description": (
                "A comprehensive simulation of the mouse brain showing major brain regions, "
                "neural circuit components, and molecular interactions—emphasizing TBI-induced excessive glutamate release."
            ),
            "author": "Your Name",
            "date": "2025-03-11",
            "version": "3.0"
        },
        "elements": {
            "nodes": [],
            "edges": []
        }
    }

    # Base nodes
    base_nodes = [
        {
            "data": {"id": "mouse_brain", "label": "Mouse Brain", "node_type": "organ"},
            "position": {"x": 0, "y": 0}
        },
        {
            "data": {
                "id": "tbi_injury_zone",
                "label": "TBI Injury Zone",
                "node_type": "injury",
                "description": "Region affected by traumatic brain injury, leading to disrupted connectivity and excessive glutamate release."
            },
            "position": {"x": 300, "y": 150}
        }
    ]

    # Brain region nodes
    brain_regions = [
        {
            "data": {"id": "cortex", "label": "Cortex", "node_type": "brain_region"},
            "position": {"x": 100, "y": 100}
        },
        {
            "data": {"id": "hippocampus", "label": "Hippocampus", "node_type": "brain_region"},
            "position": {"x": 200, "y": 100}
        }
    ]

    # Neuronal population nodes
    neuronal_populations = [
        {
            "data": {
                "id": "excitatory_neurons_cortex",
                "label": "Excitatory Neurons (Cortex)",
                "node_type": "neuronal_population",
                "neurotransmitter": "glutamate"
            },
            "position": {"x": 90, "y": 90}
        },
        {
            "data": {
                "id": "inhibitory_neurons_cortex",
                "label": "Inhibitory Neurons (Cortex)",
                "node_type": "neuronal_population",
                "neurotransmitter": "GABA"
            },
            "position": {"x": 110, "y": 110}
        },
        {
            "data": {
                "id": "excitatory_neurons_hippocampus",
                "label": "Excitatory Neurons (Hippocampus)",
                "node_type": "neuronal_population",
                "neurotransmitter": "glutamate"
            },
            "position": {"x": 190, "y": 90}
        },
        {
            "data": {
                "id": "inhibitory_neurons_hippocampus",
                "label": "Inhibitory Neurons (Hippocampus)",
                "node_type": "neuronal_population",
                "neurotransmitter": "GABA"
            },
            "position": {"x": 210, "y": 110}
        }
    ]

    simulation["elements"]["nodes"].extend(base_nodes + brain_regions + neuronal_populations)

    # Generate glutamate nodes around the injury zone
    for i in range(num_glutamate_nodes):
        x = random.uniform(250, 350)  # Within 50-100 units of injury zone x=300
        y = random.uniform(100, 200)  # Within 50 units of injury zone y=150
        glutamate_node = {
            "data": {
                "id": f"glutamate_{i}",
                "label": "Glutamate",
                "node_type": "ligand",
                "description": "Major excitatory neurotransmitter elevated in TBI, contributing to excitotoxicity."
            },
            "position": {"x": x, "y": y}
        }
        simulation["elements"]["nodes"].append(glutamate_node)

    # Determine affected neuronal populations (distance < 150 from injury zone)
    injury_pos = {"x": 300, "y": 150}
    affected_populations = []
    for node in neuronal_populations:
        pos = node["position"]
        if distance(pos, injury_pos) < 150:
            affected_populations.append(node["data"]["id"])

    # Synaptic connections between neuronal populations
    synaptic_edges = [
        {
            "data": {
                "id": "synapse_cortex_to_hippocampus_ex",
                "source": "excitatory_neurons_cortex",
                "target": "excitatory_neurons_hippocampus",
                "label": "Glutamatergic Synapse",
                "edge_type": "synapse",
                "neurotransmitter": "glutamate"
            }
        },
        {
            "data": {
                "id": "synapse_cortex_to_hippocampus_in",
                "source": "excitatory_neurons_cortex",
                "target": "inhibitory_neurons_hippocampus",
                "label": "Glutamatergic Synapse",
                "edge_type": "synapse",
                "neurotransmitter": "glutamate"
            }
        }
    ]
    simulation["elements"]["edges"].extend(synaptic_edges)

    # Edges from TBI injury zone to glutamate nodes (direct release due to injury)
    for i in range(num_glutamate_nodes):
        edge = {
            "data": {
                "id": f"edge_injury_glutamate_{i}",
                "source": "tbi_injury_zone",
                "target": f"glutamate_{i}",
                "label": "Elevates",
                "edge_type": "activates",
                "strength": 1,
                "description": "TBI increases glutamate release due to cell damage."
            }
        }
        simulation["elements"]["edges"].append(edge)

    # Edges from excitatory neurons to glutamate nodes (release)
    release_distance = 50
    for node in simulation["elements"]["nodes"]:
        if node["data"]["node_type"] == "neuronal_population" and node["data"].get("neurotransmitter") == "glutamate":
            pop_id = node["data"]["id"]
            pop_pos = node["position"]
            is_affected = pop_id in affected_populations
            strength = 2 if is_affected else 1  # Higher strength for affected neurons
            for glu_node in simulation["elements"]["nodes"]:
                if glu_node["data"]["node_type"] == "ligand":
                    glu_pos = glu_node["position"]
                    if distance(pop_pos, glu_pos) < release_distance:
                        edge = {
                            "data": {
                                "id": f"release_{pop_id}_to_{glu_node['data']['id']}",
                                "source": pop_id,
                                "target": glu_node["data"]["id"],
                                "label": "Releases",
                                "edge_type": "releases",
                                "strength": strength
                            }
                        }
                        simulation["elements"]["edges"].append(edge)

    # Edges from glutamate nodes to neuronal populations (effects)
    effect_distance = 50
    for node in simulation["elements"]["nodes"]:
        if node["data"]["node_type"] == "neuronal_population":
            pop_id = node["data"]["id"]
            pop_pos = node["position"]
            for glu_node in simulation["elements"]["nodes"]:
                if glu_node["data"]["node_type"] == "ligand":
                    glu_pos = glu_node["position"]
                    if distance(pop_pos, glu_pos) < effect_distance:
                        edge = {
                            "data": {
                                "id": f"effect_{glu_node['data']['id']}_on_{pop_id}",
                                "source": glu_node["data"]["id"],
                                "target": pop_id,
                                "label": "Affects",
                                "edge_type": "affects",
                                "strength": 1
                            }
                        }
                        simulation["elements"]["edges"].append(edge)

    # Edges from TBI injury zone to affected neuronal populations
    for pop_id in affected_populations:
        edge = {
            "data": {
                "id": f"injury_to_{pop_id}",
                "source": "tbi_injury_zone",
                "target": pop_id,
                "label": "Damages",
                "edge_type": "damages"
            }
        }
        simulation["elements"]["edges"].append(edge)

    return simulation

if __name__ == "__main__":
    num_glutamate_nodes = 10000
    simulation_data = generate_simulated_brain(num_glutamate_nodes)
    with open("expanded_mouse_brain_simulation.json", "w") as outfile:
        json.dump(simulation_data, outfile, indent=2)
    print(f"Simulation JSON with {num_glutamate_nodes} glutamate nodes generated and saved to 'expanded_mouse_brain_simulation.json'")

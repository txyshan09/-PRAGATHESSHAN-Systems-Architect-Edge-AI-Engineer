"""
Q-Logist Optimization Engine
Applies simulated annealing optimization to solve high-density 
combinatorial supply chain asset routing and traffic matrix gridlocks.
"""

import math
import random

class QLogistOptimizer:
    def __init__(self, coordinate_nodes, initial_temperature=1000.0, cooling_rate=0.995):
        # A matrix list of [X, Y] positions representing physical deployment targets
        self.nodes = coordinate_nodes
        self.temperature = initial_temperature
        self.cooling_rate = cooling_rate

    def calculate_total_distance(self, route_permutation):
        """
        Computes the total Euclidean distance matrix across a given path permutation.
        """
        total_distance = 0.0
        num_nodes = len(route_permutation)
        
        for i in range(num_nodes):
            node_a = self.nodes[route_permutation[i]]
            node_b = self.nodes[route_permutation[(i + 1) % num_nodes]] # Completes route loop
            
            # Euclidean coordinate math
            total_distance += math.sqrt((node_a[0] - node_b[0])**2 + (node_a[1] - node_b[1])**2)
            
        return round(total_distance, 4)

    def optimize_route(self, max_iterations=2000):
        """
        Executes a thermodynamic cooling schedule optimization step.
        """
        num_nodes = len(self.nodes)
        if num_nodes < 3:
            return list(range(num_nodes)), 0.0

        # Initialize base state tracking arrays
        current_route = list(range(num_nodes))
        random.shuffle(current_route)
        current_distance = self.calculate_total_distance(current_route)
        
        best_route = list(current_route)
        best_distance = current_distance

        for _ in range(max_iterations):
            if self.temperature < 0.01:
                break

            # Step 1: Generate an adjacent route matrix by swapping two random indexes
            new_route = list(current_route)
            idx_a, idx_b = random.sample(range(num_nodes), 2)
            new_route[idx_a], new_route[idx_b] = new_route[idx_b], new_route[idx_a]
            
            new_distance = self.calculate_total_distance(new_route)
            cost_delta = new_distance - current_distance

            # Step 2: Accept better routes immediately, or accept worse routes based on probability
            if cost_delta < 0 or random.random() < math.exp(-cost_delta / self.temperature):
                current_route = new_route
                current_distance = new_distance

                if current_distance < best_distance:
                    best_route = list(current_route)
                    best_distance = current_distance

            # Step 3: Cool down temperature threshold parameters
            self.temperature *= self.cooling_rate

        return best_route, best_distance

if __name__ == "__main__":
    print("Initializing Q-Logist Combinatorial Matrix Test Optimization...")
    
    # Define 6 mock delivery distribution nodes [X, Y coordinate systems]
    mock_supply_chain_nodes = [
        [1.2, 3.4], [5.6, 7.8], [9.1, 2.3],
        [4.5, 6.1], [0.8, 9.9], [3.3, 5.5]
    ]

    optimizer = QLogistOptimizer(mock_supply_chain_nodes, initial_temperature=500.0, cooling_rate=0.99)
    optimized_path, distance_metrics = optimizer.optimize_route()

    print(f"Optimal Node Processing Sequence: {optimized_path}")
    print(f"Minimized Cost Trajectory Weight: {distance_metrics} coordinate units")

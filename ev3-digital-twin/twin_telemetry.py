"""
Digital Twin Telemetry Loop Engine
Continuously serializes and packages state variables to stream state changes
between physical hardware tracks and the virtual monitoring twin environment.
"""

import json
import time
from controllers.sensor_fusion import RobotStateEstimator

class TelemetryLoop:
    def __init__(self, sample_rate_hz=20):
        # Initialize tracking estimator variables
        self.estimator = RobotStateEstimator()
        self.interval = 1.0 / sample_rate_hz
        self.is_active = True

    def run_stream_loop(self, simulated_hardware_bus):
        """
        Executes a localized simulation tracking real motor adjustments.
        """
        print("⚡ Digital Twin Telemetry Transmission Channel Initialized.")
        
        try:
            while self.is_active:
                # Capture real-time hardware data ticks from encoders and gyros
                encoder_data = simulated_hardware_bus.read_wheel_encoders()
                gyro_data = simulated_hardware_bus.read_gyro_heading()

                # Step 1: Compute non-linear kinematic predictions
                self.estimator.predict_state(
                    delta_left_wheel=encoder_data['left_delta'],
                    delta_right_wheel=encoder_data['right_delta']
                )

                # Step 2: Inject real gyro sensor values to drop drift tolerances
                self.estimator.update_with_gyro(gyro_data['angle_rad'])

                # Step 3: Package estimated state results into clean metrics maps
                current_metrics = self.estimator.get_telemetry_state()
                current_metrics['timestamp_ms'] = int(time.time() * 1000)

                # Step 4: Serialize state variables into production-ready data lines
                telemetry_packet = json.dumps(current_metrics)
                
                # Visual anchor representing live console streaming outputs
                print(f"[TWIN STREAM] {telemetry_packet}")

                # Maintain precise timing loops
                time.sleep(self.interval)

        except KeyboardInterrupt:
            self.is_active = False
            print("\n🛑 Telemetry Stream Disconnected Safely.")

# Mock class representing incoming physical layer readings for standalone execution checks
class MockHardwareBus:
    def read_wheel_encoders(self):
        return {'left_delta': 0.02, 'right_delta': 0.021}
    def read_gyro_heading(self):
        return {'angle_rad': 0.05}

if __name__ == "__main__":
    # Self-contained testing execution initialization
    bus = MockHardwareBus()
    streamer = TelemetryLoop(sample_rate_hz=5)
    
    # Run loop through 3 simple update ticks to verify operation constraints
    print("Executing standalone validation run...")
    for _ in range(3):
        streamer.estimator.predict_state(0.01, 0.01)
        print(f"Verified Packet Output State: {streamer.estimator.get_telemetry_state()}")

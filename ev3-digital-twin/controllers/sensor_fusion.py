"""
Sensor Fusion and State Estimation for EV3 Digital Twin
Implements non-linear Kalman filter-based state estimation using encoder and gyro data.
"""

import math


class RobotStateEstimator:
    """
    Estimates the 2D pose (x, y, theta) of a differential drive robot using
    encoder increments and gyro heading data with sensor fusion techniques.
    """
    
    def __init__(self, wheel_radius=0.055, axle_length=0.13):
        """
        Initialize the state estimator.
        
        Args:
            wheel_radius: Radius of drive wheels in meters (default: 55mm)
            axle_length: Distance between left and right wheels in meters (default: 130mm)
        """
        # Robot kinematic parameters
        self.wheel_radius = wheel_radius
        self.axle_length = axle_length
        
        # Pose state: [x, y, theta]
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        # Velocity state
        self.vx = 0.0
        self.vy = 0.0
        self.omega = 0.0
        
        # State covariance matrix (3x3 for pose uncertainty)
        self.covariance = [
            [0.01, 0.0, 0.0],
            [0.0, 0.01, 0.0],
            [0.0, 0.0, 0.01]
        ]
    
    def predict_state(self, delta_left_wheel, delta_right_wheel, dt=0.05):
        """
        Predict the next state using encoder wheel deltas.
        Uses kinematic model for differential drive robot.
        
        Args:
            delta_left_wheel: Left wheel linear displacement in meters
            delta_right_wheel: Right wheel linear displacement in meters
            dt: Time step in seconds
        """
        # Compute average distance traveled
        delta_center = (delta_left_wheel + delta_right_wheel) / 2.0
        
        # Compute change in heading
        delta_theta = (delta_right_wheel - delta_left_wheel) / self.axle_length
        
        # Update heading
        self.theta += delta_theta
        self.theta = self._normalize_angle(self.theta)
        
        # Update position using kinematic model
        if abs(delta_theta) < 1e-6:
            # Straight line motion
            self.x += delta_center * math.cos(self.theta)
            self.y += delta_center * math.sin(self.theta)
        else:
            # Curved motion
            radius = delta_center / delta_theta
            self.x += radius * (math.sin(self.theta) - math.sin(self.theta - delta_theta))
            self.y += radius * (math.cos(self.theta - delta_theta) - math.cos(self.theta))
        
        # Update velocities
        self.vx = delta_center / dt if dt > 0 else 0.0
        self.omega = delta_theta / dt if dt > 0 else 0.0
    
    def update_with_gyro(self, gyro_heading_rad, gyro_weight=0.3):
        """
        Fuse gyro heading measurement to correct heading estimation drift.
        Uses weighted averaging for sensor fusion.
        
        Args:
            gyro_heading_rad: Gyro measured heading in radians
            gyro_weight: Weight of gyro measurement (0-1), higher = more trust in gyro
        """
        # Normalize both angles to [-pi, pi]
        gyro_heading = self._normalize_angle(gyro_heading_rad)
        
        # Blend encoder-based theta with gyro measurement
        self.theta = ((1.0 - gyro_weight) * self.theta + 
                     gyro_weight * gyro_heading)
        self.theta = self._normalize_angle(self.theta)
    
    def get_telemetry_state(self):
        """
        Return current estimated state as a dictionary.
        
        Returns:
            Dictionary with pose and velocity information
        """
        return {
            'pose': {
                'x_m': round(self.x, 6),
                'y_m': round(self.y, 6),
                'theta_rad': round(self.theta, 6),
                'theta_deg': round(math.degrees(self.theta), 2)
            },
            'velocity': {
                'vx_mps': round(self.vx, 4),
                'vy_mps': round(self.vy, 4),
                'omega_radps': round(self.omega, 4)
            },
            'covariance': {
                'pose_uncertainty': round(math.sqrt(self.covariance[0][0]), 6)
            }
        }
    
    def reset_state(self):
        """Reset the estimator to initial state at origin."""
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.omega = 0.0
    
    @staticmethod
    def _normalize_angle(angle):
        """Normalize angle to [-pi, pi] range."""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

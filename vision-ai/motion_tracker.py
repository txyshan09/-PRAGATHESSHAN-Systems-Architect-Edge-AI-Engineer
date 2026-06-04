"""
Silambam Kinematics Tracking Engine
Processes 3D skeletal tracking coordinates to analyze weapon velocity, 
joint rotation angles, and biomechanical alignment deviations in real time.
"""

import math

class SilambamMotionTracker:
    def __init__(self):
        # Dictionary to store previous position vectors to calculate speed changes
        self.previous_joints = {}

    def calculate_joint_angle(self, point_a, point_b, point_c):
        """
        Calculates the 2D geometric angle formed by three coordinates.
        Example: Pass Shoulder (A), Elbow (B), and Wrist (C) to find elbow extension.
        """
        try:
            # Vector 1 (B -> A) and Vector 2 (B -> C)
            ba = [point_a[0] - point_b[0], point_a[1] - point_b[1]]
            bc = [point_c[0] - point_b[0], point_c[1] - point_b[1]]

            # Dot product and vector magnitudes
            dot_product = ba[0]*bc[0] + ba[1]*bc[1]
            magnitude_ba = math.sqrt(ba[0]**2 + ba[1]**2)
            magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)

            if magnitude_ba == 0 or magnitude_bc == 0:
                return 0.0

            # Cosine rule calculation
            cosine_angle = dot_product / (magnitude_ba * magnitude_bc)
            # Clip value to avoid mathematical boundary exceptions
            cosine_angle = max(-1.0, min(1.0, cosine_angle))
            
            angle_rad = math.acos(cosine_angle)
            return round(math.degrees(angle_rad), 2)
            
        except Exception:
            return 0.0

    def estimate_velocity(self, joint_id, current_coords, time_delta):
        """
        Computes the frame-to-frame displacement speed of a target joint tracking dot.
        """
        if time_delta <= 0 or joint_id not in self.previous_joints:
            self.previous_joints[joint_id] = current_coords
            return 0.0

        prev_coords = self.previous_joints[joint_id]
        
        # Euclidean distance formula between coordinates
        distance = math.sqrt((current_coords[0] - prev_coords[0])**2 + 
                             (current_coords[1] - prev_coords[1])**2)
        
        velocity = distance / time_delta
        
        # Save current position for next frame update calculation
        self.previous_joints[joint_id] = current_coords
        return round(velocity, 2)

    def assess_form_alignment(self, left_shoulder, right_shoulder, spine_base):
        """
        Validates postural stability. Checks if the upper body center line 
        tilts off-balance during explosive weapon maneuvers.
        """
        # Calculate coordinate center point of shoulders
        shoulder_center_x = (left_shoulder[0] + right_shoulder[0]) / 2.0
        
        # Calculate horizontal deviation from base anchor
        drift_delta = abs(shoulder_center_x - spine_base[0])
        
        if drift_delta > 0.15:
            return "⚠️ ALERT: Spine posture off-balance. Correction needed."
        return "✅ Posture stable. Optimal rotation axis maintained."

if __name__ == "__main__":
    print("Initializing Silambam Kinematics Engine Unit Validation...")
    tracker = SilambamMotionTracker()

    # Simulated joint data positions [X coordinate, Y coordinate]
    mock_shoulder = [0.5, 0.3]
    mock_elbow = [0.5, 0.5]
    mock_wrist_frame_1 = [0.7, 0.5]
    mock_wrist_frame_2 = [0.8, 0.6]

    # 1. Verify angle derivation math engine
    joint_angle = tracker.calculate_joint_angle(mock_shoulder, mock_elbow, mock_wrist_frame_1)
    print(f"Angle Calculation Test: {joint_angle} Degrees (Expected 90.0)")

    # 2. Verify tracking acceleration computation speed
    tracker.estimate_velocity("right_wrist", mock_wrist_frame_1, 0.033)
    calculated_speed = tracker.estimate_velocity("right_wrist", mock_wrist_frame_2, 0.033)
    print(f"Velocity Vector Tracking Speed: {calculated_speed} coordinate units/sec")

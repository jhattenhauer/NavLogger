import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import State
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class logger(Node):
    def __init__(self):
        super().__init__('logger')

        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.subscription = self.create_subscription(
            State,
            '/mavros/state',
            self.listener_callback,
            qos_profile
        )

        self.subscription = self.create_subscription(
            NavSatFix,
            '/mavros/global_position/global',
            self.listener_callback,
            qos_profile  # Apply the QoS setting here
        )

    def listener_callback(self, global_msg, state_msg):
        if str(state_msg.mode) == "GUIDED":   
            message = f"Received GPS Data: {global_msg.latitude}, {global_msg.longitude}, {global_msg.altitude}\n"
            with open("/home/james/ros2_ws/src/NavLogger/logged.txt", 'a') as file:
                file.write(message)

def main(args=None):
    rclpy.init(args=args)
    node = logger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#chatgpt code for distance>5m
#get roberts function

#import math
#
#def haversine(lat1, lon1, lat2, lon2):
#    R = 6371000  # Radius of Earth in meters
#    phi1 = math.radians(lat1)
#    phi2 = math.radians(lat2)
#    delta_phi = math.radians(lat2 - lat1)
#    delta_lambda = math.radians(lon2 - lon1)
#
#    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
#    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#
#    distance = R * c  # Distance in meters
#    return distance
#
## Example usage
#lat1, lon1 = 37.7749, -122.4194  # First coordinate
#lat2, lon2 = 37.77495, -122.41945  # Second coordinate
#
#distance = haversine(lat1, lon1, lat2, lon2)
#print(f"Distance: {distance:.2f} meters")
#
#if distance <= 5:
#    print("The points are within 5 meters.")
#else:
#    print("The points are more than 5 meters apart.")


#mavros/gllobal_position/global message example:
#header:
#  stamp:
#    sec: 1769
#    nanosec: 837820546
#  frame_id: base_link
#status:
#  status: 0
#  service: 1
#latitude: 47.5714716
#longitude: -52.8287142
#altitude: 167.90131338980666
#position_covariance:
#- 0.2304
#- 0.0
#- 0.0
#- 0.0
#- 0.2304
#- 0.0
#- 0.0
#- 0.0
#- 0.697225
#position_covariance_type: 2

#state message example:
#header:
#  stamp:
#    sec: 1769
#    nanosec: 837820546
#  frame_id: ''
#connected: true
#armed: false
#guided: true
#manual_input: false
#mode: "GUIDED"
#system_status: 4

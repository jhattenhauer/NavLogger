import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import State
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
import os
import time

file_path = '/home/james/Documents/dev/NavLogger/test.waypoints'
file = open(file_path, 'a')

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
            time.sleep(10) 
            try:        
                node_number = str(file.readlines()[-1])[0]
                message = f"{node_number+1}\t0\t3\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t{global_msg.latitude}\t{global_msg.longitude}\t{global_msg.altitude}\t100.000000"            
                file.write(message)
            except:
                print("An Error Occured")

def main(args=None):
    if os.stat(file_path).st_size == 0: #checks and writes if header line in file
        file.write('QGC WPL 110\n0\t1\t0\t0\t0\t0\t0\t0\t0\t0\t0\t1')
    rclpy.init(args=args)
    node = logger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#Example coordinate
#6	0	3	16	0.00000000	0.00000000	0.00000000	0.00000000	47.57154050	-52.82818790	100.000000	1

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

import rclpy
from rclpy.node import Node
import time

class HelloWorldNode(Node):
    def __init__(self, name):
        super().__init__(name)
        while rclpy.ok():
            self.get_logger().info("Hello World")# Output ROS2 logs
            time.sleep(0.5)# Sleep control loop time

def main(args=None):
    # Main entry point for the ROS2 node
    rclpy.init(args=args)
    # Initialize the ROS2 Python interface
    node = HelloWorldNode("helloworld")
    # Create and initialize the ROS2 node object
    rclpy.spin(node)
    # Loop and wait for ROS2 to exit.
    node.destroy_node()
    rclpy.shutdown()
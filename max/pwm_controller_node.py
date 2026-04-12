from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node

class PWMControllerNode(Node):
    def __init__(self):
        super().__init__('pwm_controller_node')

        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_callback, 10
        )

        self.get_logger().info('pwm controller node started')

    def cmd_callback(self, msg):
        lin = msg.linear.x
        ang = msg.angular.z
        self.get_logger().info(f'pwm received: {lin} -- {ang}')

def main(args=None):
    rclpy.init(args=args)
    node = PWMControllerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

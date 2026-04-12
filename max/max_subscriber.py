import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class MaxController(Node):
    def __init__(self):
        super().__init__('mecanum_controller')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Robot geometry
        self.wheel_radius = 0.05   # meters
        self.lx = 0.15             # half length
        self.ly = 0.12             # half width

        self.get_logger().info('Mecanum controller started')

    def cmd_vel_callback(self, msg: Twist):
        vx = msg.linear.x     # forward/backward
        vy = msg.linear.y     # strafe left/right
        wz = msg.angular.z    # rotation

        # Mecanum inverse kinematics
        k = self.lx + self.ly
        r = self.wheel_radius

        front_left  = (1.0 / r) * (vx - vy - k * wz)
        front_right = (1.0 / r) * (vx + vy + k * wz)
        rear_left   = (1.0 / r) * (vx + vy - k * wz)
        rear_right  = (1.0 / r) * (vx - vy + k * wz)

        self.get_logger().info(
            f"FL={front_left:.2f}, FR={front_right:.2f}, "
            f"RL={rear_left:.2f}, RR={rear_right:.2f}"
        )

        self.send_to_motors(front_left, front_right, rear_left, rear_right)

    def send_to_motors(self, fl, fr, rl, rr):
        # Replace this with your real hardware code
        # Example:
        # self.set_motor(front_left_motor, fl)
        # self.set_motor(front_right_motor, fr)
        # self.set_motor(rear_left_motor, rl)
        # self.set_motor(rear_right_motor, rr)
        pass


def main(args=None):
    rclpy.init(args=args)
    node = MaxController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

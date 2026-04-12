from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node

class MoveNode(Node):
    index=0
    def __init__(self):
        super().__init__('move_node')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.timer = self.create_timer(2.0, self.move)
        self.get_logger().info('move_node init')

    def forward(self):
        msg = Twist()
        msg.linear.x = 0.2
        self.pub.publish(msg)
        self.get_logger().info('forward')

    def backward(self):
        msg = Twist()
        msg.linear.x = -0.2
        self.pub.publish(msg)
        self.get_logger().info('backward')

    def stop(self):
        msg = Twist()
        msg.linear.x = 0.0
        self.pub.publish(msg)
        self.get_logger().info('stop')

    def move(self):
        MoveNode.index += 1
        if MoveNode.index == 1:
            self.forward()
        elif MoveNode.index == 2:
            self.stop()
        elif MoveNode.index == 3:
            self.backward()
        elif MoveNode.index == 4:
            self.stop()
        elif MoveNode.index > 4:
            MoveNode.index = 0

def main(args=None):
    rclpy.init(args=args)
    node = MoveNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

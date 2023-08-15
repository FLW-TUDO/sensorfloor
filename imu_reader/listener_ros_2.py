#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
import json
from time import time

topic = '/aerobie/vicon/pose'

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(TransformStamped, topic, self.callback, 10)

    def callback(self, data):
        global topic
        j_msg = {
            'object': topic,
            'translation': [data.transform.translation.x, data.transform.translation.y, data.transform.translation.z],
            'rotation': [data.transform.rotation.x, data.transform.rotation.y, data.transform.rotation.z],
            'time': time()
        }
        with open("vicon_data.txt", "a+") as test_data:
            test_data.write(json.dumps(j_msg) + '\n')
        test_data.close()


def listener():
    rclpy.init()

    minimal_publisher = MinimalSubscriber()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    listener()

#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt

HOST = 'raspberrypi.local'
PORT = 1883

class SnipsClient():

    # Initialization happens when the object is created:
    def __init__(self):

        # Set up a publisher called "publish", for an int
        self.pub = rospy.Publisher(
                "snips/output",
                String,
                queue_size=1)

        # Set up a subscriber called "subscribe" as a String
        self.sub = rospy.Subscriber(
                "snips/input",
                String,
                self.callback)

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(HOST, PORT, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to {0} with result code {1}".format(HOST, rc))

        self.client.subscribe("hermes/hotword/default/detected")
        self.client.subscribe("hermes/asr/textCaptured")
        self.client.subscribe('hermes/intent/#')

    def on_message(self, client, userdata, msg):
        print("Message received on topic {0}: {1}"\
            .format(msg.topic, msg.payload))

        val = str(msg.topic) + str(msg.payload)
        self.pub.publish(val)

    def loop_forever(self):


        self.client.loop_forever()

        # rate = rospy.Rate(1) # update rate of 1hz
        # while not rospy.is_shutdown():
        #     rate.sleep()

    def callback(self, data):

        # Print the string stored in the ROS String msg:
        rospy.loginfo("I heard: " + data.data)


if __name__ == '__main__':
    # initialization of the ros node
    rospy.init_node("snipsclient", anonymous=True)

    sc = SnipsClient()
    sc.loop_forever()

    rospy.spin()

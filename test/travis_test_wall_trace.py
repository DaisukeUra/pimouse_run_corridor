#!/usr/bin/env python
import unittest
import rostest
import rosnode
import rospy
import time


class WallTraceTest(unittest.TestCase):

    def set_and_get(self, lf, ls, rs, rf):
        with open("/dev/rtlightsensor0", "w"):
            with open("/dev/rtlightsensor0", "w") as f:
                f.write("%d %d %d %d\n" % (rf, rs, ls, lf))

            time.sleep(0.3)

        with open("/dev/rtmotor_raw_l0", "r") as lf, open("/dev/rtmotor_raw_r0", "r") as rf:
            left = int(lf.readline().rstrip())
            right = int(rf.readline().rstrip())

        return left, right

    def test_io(self):
        left, right = self.set_and_get(400, 100, 100, 0)
        self.assertTrue(left == right == 0, "cant stop")

        left, right = self.set_and_get(0, 5, 1000, 0)
        self.assertTrue(left == right != 0, "stop wrongly by side sensors")

        left, right = self.set_and_get(0, 10, 0, 0)
        self.assertTrue(left < right, "dont curve to left")

        left, right = self.set_and_get(0, 200, 0, 0)
        self.assertTrue(left > right, "dont curve to right")

        left, right = self.set_and_get(0, 5, 0, 0)
        self.assertTrue(0 < left == right, "curve wrongly")


if __name__ == "__main__":
    time.sleep(3)
    rospy.init_node("travis_test_wall_trace")
    rostest.rosrun('pymouse_run_corridor', 'travis_test_wall_trace', WallTraceTest)
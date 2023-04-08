import os
from unittest import TestCase

from simulator.parking_simulator import ActivityConfig, Action


class TestActivityConfig(TestCase):
    TESTDIR = "tests/data"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_activity1(self):
        activity_configfile = os.path.join(self.TESTDIR, "activity1.json")
        try:
            act_cfg = ActivityConfig(activity_configfile)
            activity = act_cfg.get_activity()
            self.assertEqual(activity[0].action, Action.PARK.value)
            self.assertEqual(activity[3].action, Action.UNPARK.value)
        except Exception as e:
            self.assertFalse(True)

    def test_illegal_action(self):
        activity_configfile = os.path.join(self.TESTDIR, self._testMethodName + ".json")
        self.assertRaisesRegexp(Exception, ".*Illegal action value: block must be one of 'park','unpark'", ActivityConfig, activity_configfile)

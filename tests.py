from __future__ import division
import sys
import unittest

import numpy as np
import numpy.testing

import npinterval


class TestInterval(unittest.TestCase):
    def test_single(self):
        """Test the interval warns if only 1 sample is included"""
        # Don't know how to test warnings below python 3.2
        if sys.version_info[0] + 0.1*sys.version_info[1] < 3.2:
            return
        x = np.array([-5, -3, -2, -2, 100])
        with self.assertWarns(RuntimeWarning):
            npinterval.interval(x, 1/5)

    def test_intervals(self):
        """Test the interval function correctly computes valid intervals"""
        x = np.array([-5, -3, -2, -2, 100])
        self.assertEqual(
            npinterval.interval(x, 2/5),
            (-2, -2, 2, 4))
        self.assertEqual(
            npinterval.interval(x, 3/5),
            (-3, -2, 1, 4))
        self.assertEqual(
            npinterval.interval(x, 4/5),
            (-5, -2, 0, 4))

    def test_full(self):
        """Test the interval function correctly finds the full interval"""
        x = np.array([-5, -3, -2, -2, 100])
        self.assertEqual(
            npinterval.interval(x, 1),
            (-5, 100, 0, 5))

    def test_invalid(self):
        """Test the interval function catches invalid intervals"""
        x = np.array([-5, -3, -2, -2, 100])
        with self.assertRaises(ValueError):
            npinterval.interval(x, 1.01)
        with self.assertRaises(ValueError):
            npinterval.interval(x, 0)


class TestHalfSampleMode(unittest.TestCase):
    def test_left(self):
        """Test edge case where mode is left-most values"""
        x = np.array([-1.1, -1, 0, 1, 2, 100])
        self.assertEqual(npinterval.half_sample_mode(x), -1.05)

    def test_right(self):
        """Test edge case where mode is right-most values"""
        x = np.array([-100, -2, -1, 0, 1, 1.1])
        self.assertEqual(npinterval.half_sample_mode(x), +1.05)

    def test_central(self):
        """Test edge case where mode is near middle"""
        x = np.array([-100, -2, 0, 0, 1, 1.1])
        self.assertEqual(npinterval.half_sample_mode(x), 0)

    def test_edges(self):
        """Test edge cases"""
        x = np.array([0, 1])
        self.assertEqual(npinterval.half_sample_mode(x), 0.5)
        x = np.array([0, 1, 1])
        self.assertEqual(npinterval.half_sample_mode(x), 1)


if __name__ == '__main__':
    unittest.main()

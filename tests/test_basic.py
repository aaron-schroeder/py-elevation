# -*- coding: utf-8 -*-

import unittest

import elevation

import pandas as pd


class TestAlgorithms(unittest.TestCase):

  def test_time_smooth(self):
    """Just see if the thing works.

    (indirectly) demonstrate usage of the elevation smoothing method,
    which is finicky about the interactions of parameters and array
    lengths.
    """
    elevation_series = pd.Series([1.0 * i for i in range(60)])

    self.assertIsInstance(
      elevation.time_smooth(elevation_series),  # window_len=3),
      pd.Series)

  def test_distance_smooth(self):
    """Just see if the thing works.
    
    Demonstrate usage of the elevation smoothing method, which
    is finicky about the interactions of parameters and array
    lengths.
    """
    distance_series = pd.Series([3.0 * i for i in range(1000)])
    elevation_series = pd.Series([1.0 * i for i in range(1000)])

    self.assertIsInstance(
      elevation.distance_smooth(distance_series, elevation_series),
      pd.Series)


if __name__ == '__main__':
  unittest.main()
import math
import warnings

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter


def threshold_filter(elevation_series):
  """Filter elevation series by breaking it into 5m vert increments."""
  ref_elev = elevation_series.iloc[0]
  elev_array = []
  for i, elev in elevation_series.iteritems():
    if abs(elev - ref_elev) > 5:
      ref_elev = elev
    elev_array.append(ref_elev) 

  elevation_series.iloc[:] = elev_array

  return elevation_series


def flatten_series(elevation_series):
  """Return a pd.Series with no change in elevation."""
  elevation_series.iloc[:] = elevation_series.mean()

  return elevation_series


def time_smooth(elevation_series, sample_len=1, window_len=21, polyorder=2):
  """Smooths noisy elevation time series.

  Because of GPS and DEM inaccuracy, elevation data is not smooth.
  Calculations involving terrain slope (the derivative of elevation
  with respect to distance, d_y/d_x) will not yield reasonable
  values unless the data is smoothed.

  This method's approach follows the overview outlined in the 
  NREL paper found in the Resources section and cited in README.
  However, unlike the algorithm in the paper, which samples regularly
  over distance, this algorithm samples regularly over time (well, it 
  presumes the elevation values are sampled at even 1-second intervals.
  The body only cares about energy use over time, not over distance.
  The noisy elevation data is downsampled and passed through a 
  Savitzky-Golay (SG) filter. Parameters for the filters were not 
  described in the paper, so they must be tuned to yield intended
  results when applied to a particular type of data. Because the
  assumptions about user behavior depend on the activiy being performed,
  the parameters will likely differ for a road run, a trail run, or a
  trail hike.

  Args:
    elevations (pandas.Series): elevations above sea level corresponding
      to the time of each sample (assumed 1-second interval).
    sample_len (int): time (in seconds) between between desired 
      resampled data. Default is 1.
    window_len (int): length of the window used in the SG filter.
      Must be positive odd integer.
    polyorder (int): order of the polynomial used in the SG filter. 
      Must be less than `window_len`.

  Returns:
    pandas.Series: elevation series that results from this smoothing 
      algorithm.

  TODO: 
    * Check if something about this method (interp?) is making grade
      really wacky when I am about to stop moving.
    * (Maybe)Combine a binomial filter with existing SG filter and 
      test effects on algorithm performance.

  """
  elevs_smooth = elevation_series.copy()
    
  try:
    with warnings.catch_warnings():
      warnings.simplefilter(action='ignore', category=FutureWarning)
      warnings.simplefilter(action='ignore', category=RuntimeWarning)
      
      elevs_smooth.iloc[:] = savgol_filter(elevation_series, window_len, polyorder)
  
  except ValueError as e:
    raise Exception('Elevation series too short to smooth') from e

  return elevs_smooth


def distance_smooth(distance_series, elevation_series, sample_len=5.0,
                     window_len=21, polyorder=2):
  """Like to `time_smooth`, but sampled over distance instead of time.

  See documentation for `time_smooth` for more info.

  WIP!!!

  Args:
    distances (pandas.Series): cumulative distances along a path.
    elevations (pandas.Series): elevations above sea level corresponding
      to the same path.
    sample_len (float): distance between between desired resampled data.
    window_len (int): length of the window used in the SG filter.
      Must be positive odd integer.
    polyorder (int): order of the polynomial used in the SG filter. 
      Must be less than `window_len`.

  Returns:
    pandas.Series: elevation series that results from this smoothing 
      algorithm.
  """

  # Subsample elevation data in evenly-spaced intervals, with each
  # point representing elevation value at the interval midpoint.
  n_sample = math.ceil(
    (distance_series.iloc[-1] - distance_series.iloc[0]) / sample_len
  )
  distance_ds = np.linspace(
    distance_series.iloc[0],
    distance_series.iloc[-1], 
    n_sample + 1
  )
  interp_fn = interp1d(distance_series, elevation_series, kind='linear')
  elevation_ds = interp_fn(distance_ds)

  # Pass downsampled data through a Savitzky-Golay filter (attenuating
  # high-frequency noise). Calculate elevations at the original distance
  # values via interpolation.
  # TODO (aschroeder): Add a second, binomial filter?
  # TODO (aschroeder): Fix the scipy/signal/arraytools warning!
  with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning)

    elevation_sg = savgol_filter(elevation_ds, window_len, polyorder)

  # (At this point, the NREL algorithm would throw out raw elevation
  # values that drastically differed from the filtered values, then
  # interpolate elevation values at those points, then re-run the
  # S-G filter...but I don't think there are elevation values that
  # should be thrown out, so I don't do that. Need to benchmark this
  # algorithm on a variety of time seriesto make sure this is the 
  # right call.)

  # Backfill the elevation values at the original distance coordinates
  # by interpolation between the downsampled, smoothed points.
  interp_function = interp1d(
    distance_ds,
    elevation_sg, 
    #fill_value='extrapolate', kind='linear',
    fill_value='extrapolate', kind='quadratic',
  )
  elevation_smooth = pd.Series(interp_function(distance_series))

  return elevation_smooth


def gain_naive(elevation_series):
  """Calculate elevation gain (scalar) from a series.

  TODO: Make sure mtd registration can handle funcs w scalar output
  """
  #print(elevation)
  diffs = elevation_series.diff(1)
  diffs[diffs < 0] = 0.0

  return diffs.sum()


def loss_naive(elevation_series):
  """Calculate elevation loss (scalar) from a pd.Series.

  TODO: Not DRY. Repurpose the gain function.
  """
  diffs = elevation_series.diff(1)
  diffs[diffs > 0] = 0.0

  return -diffs.sum()
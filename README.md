# py-elevation

> Python library for working with elevation and grade time series.

<!--[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)-->
[![License](http://img.shields.io/:license-mit-blue.svg)](http://badges.mit-license.org)

---

## Table of Contents                                                                    
- [Table of Contents](#table-of-contents)
- [Background](#background)
- [Introduction](#introduction)
- [The Elevation Smoothing Algorithm](#the-elevation-smoothing-algorithm)
- [Dependencies and Installation](#dependencies-and-installation)
- [Example](#example)
- [Project Status](#project-status)
- [Contact](#contact)
- [License](#license)

---

## Background

This project originated as the part of my 
[spatialfriend package](https://github.com/aaron-schroeder/spatialfriend) that
handled elevation smoothing and statistics like gain and loss. Lately, I've 
been interested in keeping my work in more self-contained modules with lighter
dependencies, so I split it out.

---

## Introduction

Determining one's elevation on Earth's surface has become a lot easier thanks
to high-accuracy consumer GPS products and digital elevation models (DEMs) of
Earth's topography. Still, there are errors in GPS location and in every Earth
surface model. When working with elevation and position time series, for example
calculating instantaneous slopes during a trail running workout, stricter 
requirements are placed on the data. Even with a perfectly accurate DEM,
inaccurate GPS data can yield totally unreasonable elevation profiles and path
slopes, documenting work or elevation gain that the runner did not actually do.
The same can be said for a perfectly accurate GPS trace on an inaccurate DEM.

<!--The goal of this project is to take GPS data of all resolutions, and return
geospatial data and calculations that actually match the athlete's experience.-->
The goal of this project is to wrangle messy or unreasonable elevation data, and
return stats and time series that actually match the athlete's experience.
No more unreasonably steep slopes or noisy data in your elevation profile 
making running power calculations meaningless (if you are into that kind of 
thing). No more wondering if those elevation measurements you read on GPS device
or barometric altimeter are accurate. No more apples to oranges data comparisons
because of differences between devices or datasets.

<!-- This applies to py-distance, not this one: -->
<!-- No more adding to your workout's distance because your GPS was drifting around while you were 
waiting at a stoplight. -->

<!-- This package is all about being able to hit record on that device, head
out for your run/hike/bike ride, and forget about it. Bring that messy
activity file and we will process the data once it is all done. -->

---

## The Elevation Smoothing Algorithm

The algorithm I apply to filter elevation time series is based on a paper produced by
the National Renewable Energy Laboratory. Their algorithm is meant to smooth the elevation
time series of a moving vehicle for more reasonable estimates of road grades for energy consumption
models. This actually isn't that different from my end goal of smoothing elevation series for
more reasonable estimates of elevation gain and energy consumption by ambulating humans!
The paper is included in the [`resources` folder]()

---

## Dependencies and Installation

<!-- This applies to py-distance: 
[GeoPy](https://github.com/geopy/geopy), -->

[Pandas](http://pandas.pydata.org/) and [SciPy](https://www.scipy.org/) are required.

To install (since I am not on pypi yet), first clone this repo.
```
git clone https://github.com/aaron-schroeder/py-elevation.git
```
Now you have a local version of this package that you can install with `pip`
(the `setup.py` file is configured to make this work).

Activate whatever virtual environment where you wish to install `elevation`,
and then:
```
pip install ${local_path_to_py-elevation_dir}
```

---

## Example

`py-elevation` provides the `elevation` package.

ADAPT THIS
```python
import numpy as np
import pandas as pd

import elevation

# Generate some distance coordinates.
num_samples = 600
distance_series = pd.Series([3.0 * i for i in range(num_samples)]) 

# Generate some noisy elevation coordinates
noise_mean = 0.0
std = 0.5
noise = np.random.normal(noise_mean, std, size=num_samples)
signal = pd.Series([1600.0 + 100.0 * math.sin(0.01 * i) for i in range(num_samples)])

elevation_series = signal + noise

# Compare the elevation gain using the different elevation sources.
print(sf.elevation_gain(google_elevs))
print(sf.elevation_gain(img_elevs))

# Use the algorithm to smooth the elevation profiles, and calculate
# reasonable grades between points.
grade_google = sf.grade_smooth(distances, google_elevs)
grade_img = sf.grade_smooth(distances, img_elevs)
```

---

## Project Status

### Complete

- Implement an algorithm to smooth noisy elevation time series.

### Current Activities

- Implement a smoothing algorithm for elevation series as a function of
  distance (similar to how the completed time-smoother works.)
- Make the elevation gain algorithm smarter, or create an alternate
  algorithm to emulate algorithms employed by Strava/TrainingPeaks/Garmin.
- Describe the algorithms in more detail. Maybe in a wiki?
- Provide references to papers and other resources where I got inspiration
  for each algorithm.

### Future Work

- Benchmark algorithm performance (speed, accuracy, and consistency):
   - Generate dummy time series of (distance, elevation) data to check
     smoothing algorithm.
   - Generate series of GPS points to obtain elevation coordinates from
     various DEMs (using upcoming `elevation-query` package) to compare elevation
     datasets with and without smoothing.

---

## Contact

You can get in touch with me at the following places:

<!-- - Website: <a href="https://trailzealot.com" target="_blank">trailzealot.com</a>-->
- GitHub: <a href="https://github.com/aaron-schroeder" target="_blank">github.com/aaron-schroeder</a>
- LinkedIn: <a href="https://www.linkedin.com/in/aarondschroeder/" target="_blank">linkedin.com/in/aarondschroeder</a>
- Twitter: <a href="https://twitter.com/trailzealot" target="_blank">@trailzealot</a>
- Instagram: <a href="https://instagram.com/trailzealot" target="_blank">@trailzealot</a>

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg)](http://badges.mit-license.org)

This project is licensed under the MIT License. See
[LICENSE](https://github.com/aaron-schroeder/py-activityreaders/blob/master/LICENSE)
file for details.

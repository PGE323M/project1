#!/usr/bin/env python

# Copyright 2018-2020 John T. Foster
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
import nbconvert
import numpy as np

with open("project1.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("project1.py", "w") as f:
    f.write(python_file)

from project1 import *


class TestSolution(unittest.TestCase):

    def test_extrapolate_depth(self):

        depth = extrapolate_depth('Nechelik_Data.csv', 54, 22)

        ans = np.array([[  2.70173155,  14.61847619,  24.75209183,  34.67826221,
         45.44437714,  57.59245966,  68.78224487,  80.74127656,
         93.33218919, 104.92247446],
       [ 65.56019807,  82.074415  ,  91.4114576 , 101.08788026,
        112.58602273, 124.47371216, 133.36619646, 140.26372697,
        144.79608252, 144.38027237],
       [130.12883762, 142.95904286, 152.57926161, 155.04714833,
        154.48411818, 152.21118072, 150.96466227, 148.46526713,
        145.4597082 , 139.93757709],
       [155.24926496, 155.37301106, 154.11428633, 149.92800778,
        146.03594214, 142.35462312, 140.11571568, 135.07962928,
        128.332499  , 122.3394009 ],
       [151.15995179, 148.28292214, 143.97502747, 139.15637031,
        135.05617018, 130.7246469 , 126.57847504, 122.21429303,
        118.62278665, 115.57720736],
       [143.73023011, 140.65271043, 136.55451279, 133.21773345,
        128.99558116, 125.16930013, 121.93717074, 118.81040867,
        115.54214496, 112.75619709],
       [137.47723739, 134.19496031, 131.3469027 , 127.93072662,
        124.63255187, 122.15669922, 120.11714503, 118.291131  ,
        115.54858713, 113.84711935],
       [132.06298958, 129.22726407, 126.36815605, 123.6668177 ,
        121.3084949 , 119.12047552, 117.95847689, 115.73521596,
        114.05345113, 112.13128615],
       [125.62886418, 123.10016293, 121.16497259, 119.45967825,
        117.40247364, 115.58775299, 113.97347575, 111.66651658,
        110.59510072, 110.09450219],
       [119.23080888, 117.58698671, 115.68735178, 113.77367335,
        112.5836805 , 111.55229405, 110.34970856, 108.52301829,
        106.98599511, 105.21573825]])

        np.testing.assert_allclose(depth[10:20,10:20], ans, atol=10)


    def test_nans(self):

        depth = extrapolate_depth('Nechelik_Data.csv', 54, 22)

        ans = np.array([[ np.nan,  np.nan],
                        [ np.nan,  np.nan],
                        [ np.nan,  np.nan] ])

        np.testing.assert_allclose(depth[:3,:2], ans)

if __name__ == '__main__':
        unittest.main()

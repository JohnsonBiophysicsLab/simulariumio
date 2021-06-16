#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pytest

from simulariumio.readdy import ReaddyConverter, ReaddyData
from simulariumio import UnitData, MetaData


@pytest.mark.parametrize(
    "trajectory, expected_data",
    [
        # 4 particles 3 frames
        (
            ReaddyData(
                meta_data=MetaData(
                    box_size=np.array([20.0, 20.0, 20.0]),
                ),
                timestep=0.1,
                path_to_readdy_h5="simulariumio/tests/data/readdy/test.h5",
                radii={"C": 3.0, "A": 2.0, "B": 2.0},
                ignore_types=["E"],
                type_grouping={"C": ["A", "D"]},
                time_units=UnitData("ms", 1e-6),
                spatial_units=UnitData("nm"),
            ),
            {
                "trajectoryInfo": {
                    "version": 2,
                    "timeUnits": {
                        "magnitude": 1.0,
                        "name": "ns",
                    },
                    "timeStepSize": 0.1,
                    "totalSteps": 3,
                    "spatialUnits": {
                        "magnitude": 1.0,
                        "name": "nm",
                    },
                    "size": {"x": 20.0, "y": 20.0, "z": 20.0},
                    "cameraDefault": {
                        "position": {"x": 0, "y": 0, "z": 120},
                        "lookAtPosition": {"x": 0, "y": 0, "z": 0},
                        "upVector": {"x": 0, "y": 1, "z": 0},
                        "fovDegrees": 75.0,
                    },
                    "typeMapping": {"2": {"name": "C"}, "1": {"name": "B"}},
                },
                "spatialData": {
                    "version": 1,
                    "msgType": 1,
                    "bundleStart": 0,
                    "bundleSize": 3,
                    "bundleData": [
                        {
                            "frameNumber": 0,
                            "time": 0.0,
                            "data": [
                                1000.0,
                                0.0,
                                2.0,
                                -4.076107488021348,
                                3.9849372168961708,
                                7.892235671222785,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                1.0,
                                1.0,
                                -2.780407911074236,
                                4.762366216929244,
                                9.202490133610398,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                2.0,
                                2.0,
                                8.19869797660185,
                                1.4425866729829266,
                                6.215047907498356,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                3.0,
                                1.0,
                                8.66544980756901,
                                1.97558947182814,
                                8.08535556794141,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                            ],
                        },
                        {
                            "frameNumber": 1,
                            "time": 0.1,
                            "data": [
                                1000.0,
                                0.0,
                                2.0,
                                -3.600301271046627,
                                4.360124409946104,
                                6.956371030429721,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                1.0,
                                1.0,
                                -2.761977374836856,
                                4.835017769931593,
                                9.136878226258032,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                2.0,
                                2.0,
                                7.755862317430045,
                                1.3102736549734222,
                                6.862906605118455,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                3.0,
                                1.0,
                                8.704102749692902,
                                1.8166930930965905,
                                7.8727242890809475,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                            ],
                        },
                        {
                            "frameNumber": 2,
                            "time": 0.2,
                            "data": [
                                1000.0,
                                0.0,
                                2.0,
                                -2.5613935239104135,
                                5.2768511678362575,
                                -9.666619435197141,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                1.0,
                                1.0,
                                -4.252869632733068,
                                4.420710058343225,
                                6.427577234992345,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                2.0,
                                2.0,
                                4.230292288749659,
                                0.2170518151763472,
                                3.88903614029613,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                3.0,
                                1.0,
                                -8.417490965010238,
                                4.002378907710486,
                                -9.198614964227042,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                            ],
                        },
                    ],
                },
                "plotData": {"version": 1, "data": []},
            },
        )
    ],
)
def test_readdy_converter(trajectory, expected_data):
    converter = ReaddyConverter(trajectory)
    buffer_data = converter._read_trajectory_data(converter._data)
    assert expected_data == buffer_data
    assert converter._check_agent_ids_are_unique_per_frame(buffer_data)

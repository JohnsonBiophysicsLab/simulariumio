#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from simulariumio.mcell import McellConverter, McellData


@pytest.mark.parametrize(
    "trajectory, expected_data",
    [
        # truncated data from organelle model example
        (
            McellData(
                path_to_data_model_json="simulariumio/tests/data/mcell/"
                "organelle_model_viz_output/Scene.data_model.00.json",
                path_to_binary_files="simulariumio/tests/data/mcell/"
                "organelle_model_viz_output",
                surface_mol_rotation_angle=0.0,
            ),
            {
                "trajectoryInfo": {
                    "version": 2,
                    "timeUnits": {
                        "magnitude": 1.0,
                        "name": "s",
                    },
                    "timeStepSize": 1e-6,
                    "totalSteps": 3,
                    "spatialUnits": {
                        "magnitude": 1.0,
                        "name": "µm",
                    },
                    "size": {"x": 1.28, "y": 1.28, "z": 1.28},
                    "cameraDefault": {
                        "position": {"x": 0, "y": 0, "z": 120},
                        "lookAtPosition": {"x": 0, "y": 0, "z": 0},
                        "upVector": {"x": 0, "y": 1, "z": 0},
                        "fovDegrees": 50.0,
                    },
                    "typeMapping": {
                        "0": {"name": "b"},
                        "1": {"name": "t2"},
                        "2": {"name": "a"},
                    },
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
                                0.0,
                                0.12416012585163116,
                                -0.1974048614501953,
                                -0.10042950510978699,
                                0.0,
                                0.0,
                                0.0,
                                0.005,
                                0.0,
                                1000.0,
                                1.0,
                                1.0,
                                -0.027653440833091736,
                                0.1265464723110199,
                                -0.07352104783058167,
                                -0.15157891809940338,
                                -0.9325763583183289,
                                -0.3276052474975586,
                                0.005,
                                0.0,
                                1000.0,
                                2.0,
                                2.0,
                                0.3647538423538208,
                                0.1595117300748825,
                                0.3979622721672058,
                                0.0,
                                0.0,
                                0.0,
                                0.015,
                                0.0,
                            ],
                        },
                        {
                            "frameNumber": 1,
                            "time": 1e-6,
                            "data": [
                                1000.0,
                                0.0,
                                0.0,
                                0.10336990654468536,
                                -0.20304752886295319,
                                -0.08513453602790833,
                                0.0,
                                0.0,
                                0.0,
                                0.005,
                                0.0,
                                1000.0,
                                1.0,
                                1.0,
                                -0.0269027017056942,
                                0.12665313482284546,
                                -0.07417202740907669,
                                -0.15157891809940338,
                                -0.9325763583183289,
                                -0.3276052474975586,
                                0.005,
                                0.0,
                                1000.0,
                                2.0,
                                2.0,
                                0.38411179184913635,
                                0.17711672186851501,
                                0.4012693464756012,
                                0.0,
                                0.0,
                                0.0,
                                0.015,
                                0.0,
                            ],
                        },
                        {
                            "frameNumber": 2,
                            "time": 2e-6,
                            "data": [
                                1000.0,
                                0.0,
                                0.0,
                                0.11451153457164764,
                                -0.1880205273628235,
                                -0.08175600320100784,
                                0.0,
                                0.0,
                                0.0,
                                0.005,
                                0.0,
                                1000.0,
                                1.0,
                                1.0,
                                -0.024035021662712097,
                                0.12565766274929047,
                                -0.07266511768102646,
                                -0.15157891809940338,
                                -0.9325763583183289,
                                -0.3276052474975586,
                                0.005,
                                0.0,
                                1000.0,
                                2.0,
                                2.0,
                                0.39510709047317505,
                                0.17876243591308594,
                                0.3935079276561737,
                                0.0,
                                0.0,
                                0.0,
                                0.015,
                                0.0,
                            ],
                        },
                    ],
                },
                "plotData": {"version": 1, "data": []},
            },
        ),
    ],
)
def test_mcell_converter(trajectory, expected_data):
    converter = McellConverter(trajectory)
    buffer_data = converter._read_trajectory_data(converter._data)
    raise Exception(buffer_data["spatialData"]["bundleData"][0]["data"])
    assert expected_data == buffer_data
    assert converter._check_agent_ids_are_unique_per_frame(buffer_data)

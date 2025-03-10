#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
import numpy as np

from simulariumio.mcell import McellConverter, McellData
from simulariumio import DisplayData, MetaData, JsonWriter
from simulariumio.constants import (
    DEFAULT_CAMERA_SETTINGS,
    DISPLAY_TYPE,
    VIEWER_DIMENSION_RANGE,
    VIZ_TYPE,
)
from simulariumio.exceptions import InputDataError

data = McellData(
    path_to_data_model_json="simulariumio/tests/data/mcell/"
    "organelle_model_viz_output/Scene.data_model.00.json",
    path_to_binary_files="simulariumio/tests/data/mcell/" "organelle_model_viz_output",
)
converter = McellConverter(data)
results = JsonWriter.format_trajectory_data(converter._data)

# value of automatically generated scale factor, so that position
# data fits within VIEWER_DIMENSION_RANGE
range = 0.5016988515853882 - -0.02
default_scale_factor = VIEWER_DIMENSION_RANGE.MIN / range


@pytest.mark.parametrize(
    "typeMapping, expected_typeMapping",
    [
        (
            results["trajectoryInfo"]["typeMapping"],
            {
                "0": {
                    "name": "b",
                    "geometry": {
                        "displayType": "SPHERE",
                    },
                },
                "1": {
                    "name": "t2",
                    "geometry": {
                        "displayType": "SPHERE",
                    },
                },
                "2": {
                    "name": "a",
                    "geometry": {
                        "displayType": "SPHERE",
                    },
                },
            },
        )
    ],
)
def test_typeMapping_default(typeMapping, expected_typeMapping):
    assert expected_typeMapping == typeMapping


@pytest.mark.parametrize(
    "camera_settings, expected_camera_settings",
    [
        (
            results["trajectoryInfo"]["cameraDefault"],
            {
                "position": {
                    "x": DEFAULT_CAMERA_SETTINGS.CAMERA_POSITION[0],
                    "y": DEFAULT_CAMERA_SETTINGS.CAMERA_POSITION[1],
                    "z": DEFAULT_CAMERA_SETTINGS.CAMERA_POSITION[2],
                },
                "lookAtPosition": {
                    "x": DEFAULT_CAMERA_SETTINGS.LOOK_AT_POSITION[0],
                    "y": DEFAULT_CAMERA_SETTINGS.LOOK_AT_POSITION[1],
                    "z": DEFAULT_CAMERA_SETTINGS.LOOK_AT_POSITION[2],
                },
                "upVector": {
                    "x": DEFAULT_CAMERA_SETTINGS.UP_VECTOR[0],
                    "y": DEFAULT_CAMERA_SETTINGS.UP_VECTOR[1],
                    "z": DEFAULT_CAMERA_SETTINGS.UP_VECTOR[2],
                },
                "fovDegrees": DEFAULT_CAMERA_SETTINGS.FOV_DEGREES,
            },
        )
    ],
)
def test_camera_setting_default(camera_settings, expected_camera_settings):
    assert camera_settings == expected_camera_settings


@pytest.mark.parametrize(
    "box_size, expected_box_size",
    [
        (
            results["trajectoryInfo"]["size"],
            {
                "x": 1.28 * default_scale_factor,
                "y": 1.28 * default_scale_factor,
                "z": 1.28 * default_scale_factor,
            },
        )
    ],
)
def test_box_size_default(box_size, expected_box_size):
    assert box_size == expected_box_size


box_size = 50.0
scale_factor = 10
data_with_meta_data = McellData(
    path_to_data_model_json="simulariumio/tests/data/mcell/"
    "organelle_model_viz_output/Scene.data_model.00.json",
    path_to_binary_files="simulariumio/tests/data/mcell/" "organelle_model_viz_output",
    meta_data=MetaData(
        box_size=np.array([box_size, box_size, box_size]),
        scale_factor=scale_factor,
    ),
)
converter_meta_data = McellConverter(data_with_meta_data)
results_meta_data = JsonWriter.format_trajectory_data(converter_meta_data._data)


# test box data provided, scale_factor provided
@pytest.mark.parametrize(
    "box_size, expected_box_size",
    [
        (
            results_meta_data["trajectoryInfo"]["size"],
            {
                "x": box_size * scale_factor,
                "y": box_size * scale_factor,
                "z": box_size * scale_factor,
            },
        )
    ],
)
def test_box_size_scale_factor_provided(box_size, expected_box_size):
    assert box_size == expected_box_size


a_name = "Kinesin"
a_radius = 0.03
a_url = "https://files.rcsb.org/download/3KIN.pdb"
a_color = "#0080ff"
t2_name = "Transporter"
t2_color = "#ff1493"
data_with_display_data = McellData(
    path_to_data_model_json="simulariumio/tests/data/mcell/"
    "organelle_model_viz_output/Scene.data_model.00.json",
    path_to_binary_files="simulariumio/tests/data/mcell/" "organelle_model_viz_output",
    meta_data=MetaData(box_size=np.array([box_size, box_size, box_size])),
    display_data={
        "a": DisplayData(
            name=a_name,
            radius=a_radius,
            display_type=DISPLAY_TYPE.PDB,
            url=a_url,
            color=a_color,
        ),
        "t2": DisplayData(
            name=t2_name,
            display_type=DISPLAY_TYPE.SPHERE,
            color=t2_color,
        ),
    },
    surface_mol_rotation_angle=0.0,
)

converter_display_data = McellConverter(data_with_display_data)
results_display_data = JsonWriter.format_trajectory_data(converter_display_data._data)
range = 0.5016988515853882 + 0.005 + 0.00015
auto_scale_factor = VIEWER_DIMENSION_RANGE.MIN / range


@pytest.mark.parametrize(
    "typeMapping, expected_typeMapping",
    [
        (
            results_display_data["trajectoryInfo"]["typeMapping"],
            {
                "0": {
                    "name": "b",
                    "geometry": {
                        "displayType": "SPHERE",
                    },
                },
                "1": {
                    "name": t2_name,
                    "geometry": {
                        "displayType": "SPHERE",
                        "color": t2_color,
                    },
                },
                "2": {
                    "name": a_name,
                    "geometry": {
                        "displayType": "PDB",
                        "url": a_url,
                        "color": a_color,
                    },
                },
            },
        )
    ],
)
def test_typeMapping(typeMapping, expected_typeMapping):
    assert expected_typeMapping == typeMapping


@pytest.mark.parametrize(
    "box_size, expected_box_size",
    [
        (
            results_display_data["trajectoryInfo"]["size"],
            {
                "x": box_size * auto_scale_factor,
                "y": box_size * auto_scale_factor,
                "z": box_size * auto_scale_factor,
            },
        )
    ],
)
def test_box_size_provided(box_size, expected_box_size):
    # if a box size is provided, we should use it
    assert box_size == expected_box_size


@pytest.mark.parametrize(
    "bundleData, expected_bundleData",
    [
        (
            # just testing the first frame
            results_display_data["spatialData"]["bundleData"][0],
            [
                VIZ_TYPE.DEFAULT,  # first agent
                0.0,  # id
                0.0,  # type
                0.12416012585163116 * auto_scale_factor,  # x
                -0.1974048614501953 * auto_scale_factor,  # y
                -0.10042950510978699 * auto_scale_factor,  # z
                0.0,  # x rotation
                0.0,  # y rotation
                0.0,  # z rotation
                0.005 * auto_scale_factor,  # radius
                0.0,  # number of subpoints
                VIZ_TYPE.DEFAULT,  # second agent
                1.0,
                1.0,
                -0.027653440833091736 * auto_scale_factor,
                0.1265464723110199 * auto_scale_factor,
                -0.07352104783058167 * auto_scale_factor,
                -160.8765121025542,
                0.0,
                -9.231996800714258,
                0.005 * auto_scale_factor,
                0.0,
                VIZ_TYPE.DEFAULT,  # third agent
                2.0,
                2.0,
                0.3647538423538208 * auto_scale_factor,
                0.1595117300748825 * auto_scale_factor,
                0.3979622721672058 * auto_scale_factor,
                0.0,
                0.0,
                0.0,
                0.00015 * auto_scale_factor,
                0.0,
            ],
        )
    ],
)
def test_bundleData(bundleData, expected_bundleData):
    assert np.isclose(expected_bundleData, bundleData["data"]).all()


def test_agent_ids():
    assert JsonWriter._check_agent_ids_are_unique_per_frame(results_display_data)


@pytest.mark.parametrize(
    "v, expected_perpendicular",
    [
        (
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        )
    ],
)
def test_perp_vector(v, expected_perpendicular):
    mcell_perpendicular = McellConverter._get_perpendicular_vector(v, 0.0)
    assert (expected_perpendicular == mcell_perpendicular).all()


@pytest.mark.parametrize(
    "v1, v2, expected_result",
    [
        (
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [
                [0.0, 0.0, 1.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
            ],
        )
    ],
)
def test_rotation_matrix(v1, v2, expected_result):
    rotation_matrix = McellConverter._get_rotation_matrix(v1, v2)
    assert (rotation_matrix == expected_result).all()


@pytest.mark.parametrize(
    "v1, expected_result",
    [
        (
            [0.0, 0.0, 1.0],
            [90.0, 0.0, 90.0],
        )
    ],
)
def test_get_euler_angles(v1, expected_result):
    euler_angles = McellConverter._get_euler_angles(v1, 45)
    assert (euler_angles == expected_result).all()


def test_input_file_error():
    invalid_json = McellData(
        path_to_data_model_json="simulariumio/tests/data/md/example.xyz",
        path_to_binary_files="simulariumio/tests/data/mcell/organelle_model_viz_output",
    )
    with pytest.raises(InputDataError):
        McellConverter(invalid_json)

    wrong_bin = McellData(
        path_to_data_model_json="simulariumio/tests/data/mcell/"
        "organelle_model_viz_output/Scene.data_model.00.json",
        path_to_binary_files="simulariumio/tests/data/mcell/"
        "organelle_model_example_files/mcell/output_data/react_data/seed_00001",
    )
    with pytest.raises(InputDataError):
        McellConverter(wrong_bin)


def test_callback_fn():
    callback_fn_0 = Mock()
    call_interval = 0.000000001
    McellConverter(data, callback_fn_0, call_interval)
    assert callback_fn_0.call_count > 1

    # calls to the callback function should be strictly increasing
    # and the value should never exceed 1.0 (100%)
    call_list = callback_fn_0.call_args_list
    last_call_val = 0.0
    for call in call_list:
        call_value = call.args[0]
        assert call_value >= last_call_val
        assert call_value <= 1.0
        last_call_val = call_value

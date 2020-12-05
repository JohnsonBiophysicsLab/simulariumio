#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from typing import Any, Dict, List

import numpy as np

from ..constants import SPATIAL_UNIT_OPTIONS
from ..exceptions import DataError

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


class ReaddyData:
    spatial_units: str
    box_size: np.ndarray
    timestep: float
    path_to_readdy_h5: str
    radii: Dict[str, float]
    ignore_types: List[str]
    type_grouping: Dict[str, List[str]]
    scale_factor: float
    plots: List[Dict[str, Any]]

    def __init__(
        self,
        spatial_units: str,
        box_size: np.ndarray,
        timestep: float,
        path_to_readdy_h5: str,
        radii: Dict[str, float] = None,
        ignore_types: List[str] = None,
        type_grouping: Dict[str, List[str]] = None,
        scale_factor: float = 1.0,
        plots: List[Dict[str, Any]] = [],
    ):
        """
        This object holds simulation trajectory outputs
        from ReaDDy (https://readdy.github.io/)
        and plot data

        Parameters
        ----------
        spatial_units : str
            A string specifying the units for spatial data,
            which includes positions, box size, radii. 
            Options:
                Ym = yottameters
                Zm = zettameters
                Em = exameters
                Pm = petameters
                Tm = terameters
                Gm = gigameters
                Mm = megameters
                km = kilometers
                hm = hectometers
                dam = decameters
                m = meters
                dm = decimeters
                cm = centimeters
                mm = millimeters
                um or μm = micrometers (microns)
                nm = nanometers
                A = angstroms
                pm = picometers
                fm = femptometers
                am = attometers
                zm = zeptometers
                ym = yoctometers
        box_size : np.ndarray (shape = [3])
            A numpy ndarray containing the XYZ dimensions
            of the simulation bounding volume
        timestep : float
            A float amount of time in seconds that passes each step
            Default: 0.0
        path_to_readdy_h5 : str
            A string path to the ReaDDy trajectory file (.h5)
        radii : Dict[str, float] (optional)
            A mapping of ReaDDy particle type to radius
            of each visualized sphere for that type
            Default: 1.0 (for each particle)
        ignore_types : List[str] (optional)
            A list of string ReaDDy particle types to ignore
        type_grouping : Dict[str, List[str]] (optional)
            A mapping of a new group type name to a list of
            ReaDDy particle types to include in that group
            e.g. {"moleculeA":["A1","A2","A3"]}
        scale_factor : float (optional)
            A multiplier for the ReaDDy scene, use if
            visualization is too large or small
            Default: 1.0
        plots : List[Dict[str, Any]] (optional)
            An object containing plot data already
            in Simularium format
        """
        if spatial_units not in SPATIAL_UNIT_OPTIONS:
            raise DataError(f"Unrecognized spatial unit: {spatial_units}")
        self.spatial_units = spatial_units
        self.box_size = box_size
        self.timestep = timestep
        self.path_to_readdy_h5 = path_to_readdy_h5
        self.radii = radii
        self.ignore_types = ignore_types
        self.type_grouping = type_grouping
        self.scale_factor = scale_factor
        self.plots = plots

from MDAnalysis import Universe
from typing import Dict, List, Tuple
import os

from ..trajectory_converter import TrajectoryConverter
from ..data_objects import AgentData, TrajectoryData, DimensionData, UnitData
from ..constants import VIZ_TYPE, VALUES_PER_3D_POINT
from .nerdss_data import NerdssData


class NerdssConverter(TrajectoryConverter):
    def __init__(
        self,
        input_data: NerdssData,
    ):
        """
        Parameters
        ----------
        input_data : NerdssData
            An object containing info for reading
            NERDSS simulation trajectory outputs and plot data
        """
        self._data = self._read(input_data)

    def _is_intra_molecular_bond_site(self, input_data: NerdssData, name: str) -> bool:
        for bond in input_data.intra_molecular_bonds:
            if bond.agent_name_a == name or bond.agent_name_b == name:
                return True
        return False

    def _is_inter_molecular_bond_site(self, input_data: NerdssData, name: str) -> bool:
        for bond in input_data.inter_molecular_bonds:
            if bond.agent_name_a == name or bond.agent_name_b == name:
                return True
        return False

    def _read_pdb_files(self, input_data: NerdssData) -> AgentData:
        file_list = os.listdir(input_data.path_to_pdb_files)
        file_list.sort()
        n_timesteps = len(file_list)
        dimensions = DimensionData(
            total_steps=n_timesteps, max_agents=0, max_subpoints=VALUES_PER_3D_POINT * 2
        )
        time_steps = []
        for file in file_list:
            u = Universe(os.path.join(input_data.path_to_pdb_files, file))
            n_agents = len(u.atoms.positions)
            if n_agents*2 > dimensions.max_agents:
                dimensions.max_agents = n_agents*2
            time_steps.append(os.path.splitext(file)[0])
        time_steps.sort(key=int)
        agent_data = AgentData.from_dimensions(dimensions)
        agent_data.n_timesteps = n_timesteps

        # keep track of fiber positions for bonds as we go
        # as this is populated, it will be a List[List[float]]
        # with shape [timesteps, agents, 6], as every bond will
        # be represented as a fiber with 6 positional data points,
        # the XYZ coords of one bond site + the XYZ coords of the other bond site
        fiber_positions = [[] for i in range(n_timesteps)]

        for time_index in range(n_timesteps):
            # we are assuming the time is the file name
            universe = Universe(
                os.path.join(
                    input_data.path_to_pdb_files, time_steps[time_index] + ".pdb"
                )
            )
            atoms = universe.atoms
            temp_n_agents = len(atoms)
            agent_data.positions[time_index][0:temp_n_agents] = universe.atoms.positions

            # TODO: shift times so the trajectory will start at time=0
            agent_data.times[time_index] = (
                float(time_steps[time_index]) * input_data.time_units.magnitude
            )


            agent_data.n_agents[time_index] = len(atoms)


            # dict of potential inter bond sites, represented as a dict where the key
            # is the name and the value is a list of XYZ position coordinates of
            # agents of this type
            #inter_bond_sites = Dict[str, List]

            # Loop through the atoms, set each as a new agent and set their position
            # determine type based on resname and name. Create fiber agents to represent
            # bonds, when appropriate
            for residue in universe.residues:
                com_true = 0
                resname = residue.resname
                # list of potential intra bond sites, represented as a dict where the
                # key is the name and the value is a list of XYZ position coordinates of
                # agents of this type
                #intra_bond_sites = Dict[str, List]
                for atom in residue.atoms:
                    name = atom.name
                    atom_index = atom.index
                    # Currently representing agent names as residue_name#atom_name,
                    # which are directly extracted from the pdb files. If there is a
                    # better naming scheme, feel free to change. In this current code,
                    # the input agent names in BondData would also need to match this
                    full_name = resname + "#" + name
                    position = atom.position
                    if name != "ref":
                    	if name == "COM":
                    		com_coord = position
                    		com_true = 1
                    	elif com_true==1:
                    		bond_site_coord = position
                    		bond_coords = list(com_coord) + list(bond_site_coord)
                    		fiber_positions[time_index].append(bond_coords)

                    agent_data.types[time_index].append(
                        TrajectoryConverter._get_display_type_name_from_raw(
                            full_name, input_data.display_data
                        )
                    )
                    agent_data.unique_ids[time_index][atom_index] = atom.id

                    # Get the user provided display data for this raw_type_name
                    input_display_data = (
                        TrajectoryConverter._get_display_data_for_agent(
                            full_name, input_data.display_data
                        )
                    )

                    agent_data.radii[time_index][atom_index] = (
                        input_display_data.radius
                        if input_display_data and input_display_data.radius is not None
                        else 1.0
                    )

                # TODO: loop through the list of potential bond sites, intra_bond_sites,
                # for this residue, checking if any pair of the atoms should have a bond
                # based on the thresholds specified in input_data.inter_molecular_bonds
                #
                # BondData.is_valid_bond(...) can be used to determine if a bond should
                # be drawn
                #
                # Append a list of 6 position points (XYZ coordinates for each of the
                # two bond site) to fiber_positions[time_index]

            # TODO: loop through the list of potential bond sites, inter_bond_sites, for
            # this timestep, checking if any pair of atoms should have a bond based on
            # the thresholds specified in input_data.intra_molecular_bonds
            #
            # BondData.is_valid_bond(...) can be used to determine if a bond should be
            # drawn
            #
            # Append a list of 6 position points (XYZ coordinates for each of the two
            # bond site) to fiber_positions[time_index]

        # build AgentData object for fiber data

        last_uid = agent_data.unique_ids.max()
        for timestep in range(n_timesteps):
            # fiber_positions[timestep] = [[x,y,z,x,y,z], [x,y,z,x,y,z], ....]
            # where [x,y,z,x,y,z] represents a single fiber agent
            n_fibers = len(fiber_positions[timestep])
            n_atoms = int(agent_data.n_agents[timestep])
            agent_data.n_agents[timestep] = n_fibers + n_atoms
            for agent_index in range(n_fibers):
                #print(f'n_atoms:{n_atoms}')
                agent_data.subpoints[timestep][agent_index+n_atoms] = fiber_positions[timestep][
                    agent_index
                ]
                agent_data.n_subpoints[timestep][agent_index+n_atoms] = VALUES_PER_3D_POINT * 2
                agent_data.viz_types[timestep][agent_index+n_atoms] = VIZ_TYPE.FIBER
                agent_data.radii[timestep][agent_index+n_atoms] = .3
                agent_data.types[timestep].append("bonds")
                last_uid += 1
                agent_data.unique_ids[timestep][agent_index+n_atoms] = last_uid
        agent_data.types[timestep][agent_index+n_atoms] = TrajectoryConverter._get_display_type_name_from_raw("bonds", input_data.display_data)

        return agent_data

    def _read(self, input_data: NerdssData) -> TrajectoryData:
        """
        Return a TrajectoryData object containing the NERDSS data
        """
        print("Reading PDB Data -------------")
        agent_data = self._read_pdb_files(input_data)
        result = TrajectoryData(
            meta_data=input_data.meta_data,
            agent_data=agent_data,
            time_units=UnitData(name=input_data.time_units.name),
            spatial_units=input_data.spatial_units,
            plots=input_data.plots,
        )
        # add the fiber agents, representing bonds, into the trajectory
        return result

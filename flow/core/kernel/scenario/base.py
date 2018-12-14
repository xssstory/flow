"""Script containing the base scenario kernel class."""

# length of vehicles in the network, in meters
VEHICLE_LENGTH = 5


class KernelScenario(object):
    """Base scenario kernel.

    This kernel subclass is responsible for generating any simulation-specific
    components needed to simulate a traffic network. This may include network
    creating configuration files that support the generating of certain traffic
    networks in a simulator (e.g. sumo), or may be as simple as passing network
    features from the scenario class (see flow/scenarios/base_scenario.py) and
    transferring them to the simulator kernel later on.

    In addition to generating files for network initialization, the scenario
    kernel performs two auxiliary tasks:

    * State acquisition: The scenario kernel contains several methods that can
      be used to acquire state information on the properties of the network
      that is being simulated, e.g. the number of lanes on an edge, the length
      of an edge, the available routes from a starting position, etc... If, for
      example, you would like to determine the maximum speed a vehicle can
      travel within the network, this can be done by calling the following
      command:

        >>> from flow.envs.base_env import Env
        >>> env = Env(...)
        >>> max_speed = env.k.scenario.max_speed()

      All relevant methods may be found within the Flow documentation.

    * Methods for generating initial vehicle positions: Initial vehicle
      positions are generated by the abstract scenario kernel, and may be
      overridden by the network generated from a flow.scenarios.Scenario object
      if the spacing in ``initial_config`` is set to random. Default initial
      positions include uniform starting positions (where all vehicles are
      equally spacing) or random starting positions (limited by some min_gap).
      For more details on how to augment the starting position of vehicles,
      see:  # TODO: create tutorial
    """

    def __init__(self, master_kernel):
        """Instantiate the base scenario kernel.

        Parameters
        ----------
        master_kernel : flow.core.kernel.Kernel
            the higher level kernel (used to call methods from other
            sub-kernels)
        """
        self.master_kernel = master_kernel
        self.kernel_api = None

    def generate_network(self, network):
        """Generate the necessary prerequisites for the simulating a network.

        Parameters
        ----------
        network : flow.scenarios.Scenario
            an object containing relevant network-specific features such as the
            locations and properties of nodes and edges in the network
        """
        raise NotImplementedError

    def pass_api(self, kernel_api):
        """Acquire the kernel api that was generated by the simulation kernel.

        Parameters
        ----------
        kernel_api : any
            an API that may be used to interact with the simulator
        """
        self.kernel_api = kernel_api

    def update(self, reset):
        """Update the scenario with current state information.

        Since scenarios are generally static, this will most likely not include
        any actions being performed. This is primarily here for consistency
        with other sub-kernels.

        Parameters
        ----------
        reset : bool
            specifies whether the simulator was reset in the last simulation
            step
        """
        raise NotImplementedError

    def close(self):
        """Close the scenario."""
        raise NotImplementedError

    ###########################################################################
    #                        State acquisition methods                        #
    ###########################################################################

    def edge_length(self, edge_id):
        """Return the length of a given edge/junction.

        Return -1001 if edge not found.
        """
        raise NotImplementedError

    def length(self):
        """Return the total length of all junctions and edges."""
        raise NotImplementedError

    def speed_limit(self, edge_id):
        """Return the speed limit of a given edge/junction.

        Return -1001 if edge not found.
        """
        raise NotImplementedError

    def max_speed(self):
        """Return the maximum achievable speed on any edge in the network."""
        raise NotImplementedError

    def num_lanes(self, edge_id):
        """Return the number of lanes of a given edge/junction.

        Return -1001 if edge not found.
        """
        raise NotImplementedError

    def get_edge_list(self):
        """Return the names of all edges in the network."""
        raise NotImplementedError

    def get_junction_list(self):
        """Return the names of all junctions in the network."""
        raise NotImplementedError

    def get_edge(self, x):  # TODO: maybe remove
        """Compute an edge and relative position from an absolute position.

        Parameters
        ----------
        x : float
            absolute position in network

        Returns
        -------
        edge position : tup
            1st element: edge name (such as bottom, right, etc.)
            2nd element: relative position on edge
        """
        raise NotImplementedError

    def get_x(self, edge, position):  # TODO: maybe remove
        """Return the absolute position on the track.

        Parameters
        ----------
        edge : str
            name of the edge
        position : float
            relative position on the edge

        Returns
        -------
        absolute_position : float
            position with respect to some global reference
        """
        raise NotImplementedError

    def next_edge(self, edge, lane):
        """Return the next edge/lane pair from the given edge/lane.

        These edges may also be internal links (junctions). Returns an empty
        list if there are no edge/lane pairs in front.
        """
        raise NotImplementedError

    def prev_edge(self, edge, lane):
        """Return the edge/lane pair right before this edge/lane.

        These edges may also be internal links (junctions). Returns an empty
        list if there are no edge/lane pairs behind.
        """
        raise NotImplementedError

    ###########################################################################
    #            Methods for generating initial vehicle positions.            #
    ###########################################################################

    def generate_starting_positions(self,
                                    initial_config,
                                    num_vehicles=None,
                                    **kwargs):
        """Generate starting positions for vehicles in the network.

        Calls all other starting position generating classes.

        Parameters
        ----------
        initial_config : flow.core.params.InitialConfig
            see flow/core/params.py
        num_vehicles : int, optional
            number of vehicles to be placed on the network. If no value is
            specified, the value is collected from the vehicles class
        kwargs : dict
            additional arguments that may be updated beyond initial
            configurations, such as modifying the starting position

        Returns
        -------
        startpositions : list of tuple (float, float)
            list of start positions [(edge0, pos0), (edge1, pos1), ...]
        startlanes : list of int
            list of start lanes
        startvel : list of float
            list of start speeds
        """
        raise NotImplementedError

    def gen_even_start_pos(self, initial_config, num_vehicles, **kwargs):
        """Generate uniformly spaced starting positions.

        If the perturbation term in initial_config is set to some positive
        value, then the start positions are perturbed from a uniformly spaced
        distribution by a gaussian whose std is equal to this perturbation
        term.

        Parameters
        ----------
        initial_config : InitialConfig type
            see flow/core/params.py
        num_vehicles : int
            number of vehicles to be placed on the network
        kwargs : dict
            extra components, usually defined during reset to overwrite initial
            config parameters

        Returns
        -------
        startpositions : list of tuple (float, float)
            list of start positions [(edge0, pos0), (edge1, pos1), ...]
        startlanes : list of int
            list of start lanes
        startvel : list of float
            list of start speeds
        """
        raise NotImplementedError

    def gen_random_start_pos(self, initial_config, num_vehicles, **kwargs):
        """Generate random starting positions.

        Parameters
        ----------
        initial_config : InitialConfig type
            see flow/core/params.py
        num_vehicles : int
            number of vehicles to be placed on the network
        kwargs : dict
            extra components, usually defined during reset to overwrite initial
            config parameters

        Returns
        -------
        startpositions : list of tuple (float, float)
            list of start positions [(edge0, pos0), (edge1, pos1), ...]
        startlanes : list of int
            list of start lanes
        startvel : list of float
            list of start speeds
        """
        raise NotImplementedError

    def gen_custom_start_pos(self, initial_config, num_vehicles, **kwargs):
        """Generate a user defined set of starting positions.

        Parameters
        ----------
        initial_config : InitialConfig type
            see flow/core/params.py
        num_vehicles : int
            number of vehicles to be placed on the network
        kwargs : dict
            extra components, usually defined during reset to overwrite initial
            config parameters

        Returns
        -------
        startpositions : list of tuple (float, float)
            list of start positions [(edge0, pos0), (edge1, pos1), ...]
        startlanes : list of int
            list of start lanes
        startvel : list of float
            list of start speeds
        """
        raise NotImplementedError

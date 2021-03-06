"""Grid example."""
from flow.controllers import GridRouter, IDMController, RLController
from flow.controllers.routing_controllers import MinicityRouter, InflowRouter
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams
from flow.core.params import VehicleParams, PersonParams
from flow.core.params import TrafficLightParams
from flow.core.params import SumoCarFollowingParams, SumoLaneChangeParams
from flow.core.params import InFlows
# from flow.envs.ring.accel import AccelEnv, ADDITIONAL_ENV_PARAMS
from flow.envs.dispatch_and_reposition import DispatchAndRepositionEnv, ADDITIONAL_ENV_PARAMS
from flow.networks import GridnxmNetwork
from flow.utils.trafficlights import get_uniform_random_phase

v_enter = 10
inner_length = 50
n_rows = 4
n_columns = 4
horizon = 500

grid_array = {
    "inner_length": inner_length,
    "row_num": n_rows,
    "col_num": n_columns,
    "sub_edge_num": 1
}

def get_non_flow_params(enter_speed, add_net_params, inflows=None):
    """Define the network and initial params in the absence of inflows.

    Note that when a vehicle leaves a network in this case, it is immediately
    returns to the start of the row/column it was traversing, and in the same
    direction as it was before.

    Parameters
    ----------
    enter_speed : float
        initial speed of vehicles as they enter the network.
    add_net_params: dict
        additional network-specific parameters (unique to the grid)

    Returns
    -------
    flow.core.params.InitialConfig
        parameters specifying the initial configuration of vehicles in the
        network
    flow.core.params.NetParams
        network-specific parameters used to generate the network
    """
    additional_init_params = {'enter_speed': enter_speed}
    initial = InitialConfig(
        x0=2.5, spacing='uniform', min_gap=10, additional_params=additional_init_params) # gap needs to be large enough
    net = NetParams(inflows=inflows, additional_params=add_net_params)

    return initial, net

persons = PersonParams()
vehicles = VehicleParams()

vehicles.add(
    veh_id="inflow",
    acceleration_controller=(IDMController, {}),
    routing_controller=(InflowRouter, {'inflow': 'top_left'}),
    car_following_params=SumoCarFollowingParams(
        speed_mode='all_checks',
        min_gap=5,
        decel=10.0,  # avoid collisions at emergency stops
        max_speed=10,
    ),
    lane_change_params=SumoLaneChangeParams(
        lane_change_mode="no_lc_safe",
    ),
    initial_speed=0,
    num_vehicles=0)
vehicles.add(
    veh_id="taxi",
    initial_speed=0,
    acceleration_controller=(RLController, {}),
    # routing_controller=(MinicityRouter, {}),
    car_following_params=SumoCarFollowingParams(
        speed_mode='all_checks',
        min_gap=5,
        decel=10.0,  # avoid collisions at emergency stops
        max_speed=10,
    ),
    lane_change_params=SumoLaneChangeParams(
        lane_change_mode="sumo_default",
    ),
    num_vehicles=20,
    is_taxi=False)

tl_logic = TrafficLightParams(baseline=False)
phases = get_uniform_random_phase('center', means=[10.0, 1.0, 10.0, 1.0], noises=[0.5], T=horizon)
tl_logic.add("center9", programID=10, phases=phases)
tl_logic.add("center10", programID=10, phases=phases)
tl_logic.add("center5", programID=10, phases=phases)
tl_logic.add("center6", programID=10, phases=phases)

additional_net_params = {
    "grid_array": grid_array,
    "speed_limit": 35,
    "horizontal_lanes": 1,
    "vertical_lanes": 1,
    "print_warnings": False, # warnings in building net
    # "inflow": ['top_left', 'midbot_left', 'top_midright']
}

# inflows = InFlows()
# inflows.add('inflow_top_left', 'inflow', probability=0.2, depart_speed='random', \
#     name='inflow_top_left')
# # inflows.add('inflow_midtop_left', 'inflow', probability=0.2, depart_speed='random', \
# #     name='inflow_midtop_left')
# inflows.add('inflow_midbot_left', 'inflow', probability=0.2, depart_speed='random', \
#     name='inflow_midbot_left')
# # inflows.add('inflow_top_midleft', 'inflow', probability=0.2, depart_speed='random', \
# #     name='inflow_top_midleft')
# inflows.add('inflow_top_midright', 'inflow', probability=0.2, depart_speed='random', \
#     name='inflow_top_midright')

initial_config, net_params = get_non_flow_params(
    enter_speed=v_enter,
    # inflows=inflows,
    add_net_params=additional_net_params)

additional_params = ADDITIONAL_ENV_PARAMS.copy()
additional_params["time_price"] = 0.02
additional_params["distance_price"] = 0.005
additional_params["pickup_price"] = 1
additional_params["wait_penalty"] = 0.000
additional_params["tle_penalty"] = 0.02
additional_params["person_prob"] = 0.06
additional_params["max_waiting_time"] = 20
additional_params["free_pickup_time"] = 0.0
additional_params["distribution"] = 'mode-13'
additional_params["n_mid_edge"] = 1
additional_params["use_tl"] = True
flow_params = dict(
    # name of the experiment
    exp_tag='grid-intersection',

    # name of the flow environment the experiment is running on
    env_name=DispatchAndRepositionEnv,

    # name of the network class the experiment is running on
    network=GridnxmNetwork,

    # simulator that is used by the experiment
    simulator='traci',

    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=SumoParams(
        sim_step=1,
        render=False,
        print_warnings=False,
        restart_instance=True
        # taxi_dispatch_alg="greedy"
    ),

    # environment related parameters (see flow.core.params.EnvParams)

    env=EnvParams(
        horizon=horizon,
        additional_params=additional_params,
    ),

    # network-related parameters (see flow.core.params.NetParams and the
    # network's documentation or ADDITIONAL_NET_PARAMS component)
    net=net_params,

    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.params.VehicleParams)
    veh=vehicles,
    per=persons,

    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=initial_config,

    # traffic lights to be introduced to specific nodes (see
    # flow.core.params.TrafficLightParams)
    tls=tl_logic,
)

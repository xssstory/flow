
from flow.core.params import AimsunParams, NetParams, VehicleParams, EnvParams, InitialConfig
from flow.core.experiment import Experiment
# from flow.networks import Network
# from flow.envs import TestEnv
from coordinated_lights import CoordinatedNetwork, CoordinatedEnv, ADDITIONAL_ENV_PARAMS
import os

sim_step = 0.8  # seconds
detector_step = 300  # seconds
env_params = EnvParams(horizon=3600//sim_step,
                       sims_per_step=int(detector_step/sim_step),
                       additional_params=ADDITIONAL_ENV_PARAMS)
initial_config = InitialConfig()
vehicles = VehicleParams()

net_params = NetParams(
    template=os.path.expanduser("no_api_scenario.ang")
)

sim_params = AimsunParams(
    sim_step=sim_step,
    render=False,
    emission_path='data',
    replication_name="Replication (one hour)",
    centroid_config_name="Centroid Configuration 8040652"
)

network = CoordinatedNetwork(
    name="template",
    net_params=net_params,
    initial_config=initial_config,
    vehicles=vehicles
)

env = CoordinatedEnv(
    env_params,
    sim_params,
    network,
    simulator="aimsun"
)

exp = Experiment(env)
exp.run(1, int(3900/detector_step))

import copy
import glob
import os
import sys
import time
from collections import deque

import gym
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from .a2c_ppo_acktr import algo, utils
from .a2c_ppo_acktr.algo import gail
from .a2c_ppo_acktr.arguments import get_args
from .a2c_ppo_acktr.envs import make_vec_envs
from .a2c_ppo_acktr.model import Policy
from .a2c_ppo_acktr.storage import RolloutStorage
from .evaluation import evaluate

def eval_ppo(flow_params=None):
    args = get_args(sys.argv[2:])

    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)

    if args.cuda and torch.cuda.is_available() and args.cuda_deterministic:
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True

    log_dir = os.path.expanduser(args.log_dir)
    eval_log_dir = log_dir + "_eval"
    utils.cleanup_log_dir(log_dir)
    utils.cleanup_log_dir(eval_log_dir)

    torch.set_num_threads(1)
    device = torch.device("cuda:0" if args.cuda else "cpu")

    save_path = os.path.join(os.path.join(args.save_dir, args.algo), args.experiment_name)
    pt =  os.path.join(save_path, str(args.eval_ckpt) + ".pt")
    actor_critic, ob_rms = torch.load(pt, map_location='cpu')
    actor_critic.to(device)

    screenshot_path = os.path.join(save_path, "images") if args.save_screenshot else None

    flow_params['sim'].render = not args.disable_render_during_eval
    flow_params['sim'].save_render = screenshot_path
    eval_envs = make_vec_envs(args.env_name, args.seed, args.num_processes, \
        None, save_path, True, device=device, flow_params=flow_params, verbose=True)
    evaluate(actor_critic, eval_envs, ob_rms, args.num_processes, device, save_path=save_path, \
        do_plot_congestion=args.plot_congestion, ckpt=args.eval_ckpt, verbose=True)
    eval_envs.close()
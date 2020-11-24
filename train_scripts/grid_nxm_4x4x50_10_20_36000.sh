python train/train.py \
    grid_nxm_4x4x50_10_20_36000 \
    --experiment-name=grid_nxm_4x4x50_10_20_36000 \
    --num-env-steps=10000000 \
    --algo=ppo \
    --use-gae \
    --lr=2.5e-4 \
    --clip-param=0.1 \
    --value-loss-coef=0.5 \
    --num-processes=1 \
    --num-steps=128 \
    --num-mini-batch=4 \
    --log-interval=1 \
    --use-linear-lr-decay \
    --entropy-coef=0.01 

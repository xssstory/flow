python train/train.py \
    test \
    --experiment-name=test \
    --num-env-steps=200000000 \
    --algo=ppo \
    --use-gae \
    --lr=2.5e-4 \
    --clip-param=0.2 \
    --value-loss-coef=0.5 \
    --num-envs=1 \
    --num-actors=1 \
    --num-splits=1 \
    --eval-num-processes=1 \
    --num-steps=500 \
    --num-mini-batch=4 \
    --log-interval=1 \
    --save-interval=32 \
    --eval-interval=32 \
    --use-linear-lr-decay \
    --popart-reward \
    --entropy-coef=0.01 \
    --gamma=0.999 \
    --queue-size=5 \
    --reuse=1

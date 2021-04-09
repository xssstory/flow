python train/train.py \
    test-stl-nw-profit-X1-1-large \
    --experiment-name=test-stl-nw-profit-X1-1-large_test2_2 \
    --num-env-steps=400000000 \
    --algo=ppo \
    --use-gae \
    --lr=2.5e-4 \
    --clip-param=0.2 \
    --value-loss-coef=0.5 \
    --num-envs=200 \
    --num-actors=2 \
    --num-splits=2 \
    --eval-num-processes=50 \
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

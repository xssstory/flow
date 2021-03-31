python train/train.py \
    test-stl-nw-profit-X2-large \
    --experiment-name=test-stl-nw-profit-X2-large_test \
    --num-env-steps=300000000 \
    --algo=ppo \
    --use-gae \
    --lr=2.5e-4 \
    --clip-param=0.1 \
    --value-loss-coef=0.5 \
    --num-envs=100 \
    --num-actors=1 \
    --num-splits=1 \
    --eval-num-processes=50 \
    --num-steps=500 \
    --num-mini-batch=4 \
    --log-interval=1 \
    --save-interval=20 \
    --eval-interval=20 \
    --use-linear-lr-decay \
    --popart-reward \
    --entropy-coef=0.01 \
    --gamma=0.999 \
    --queue-size=5 \
    --reuse=1

python train/train.py \
    test-uniform-negative-nomiss \
    --experiment-name=test-uniform-negative-nomiss \
    --num-env-steps=500000000 \
    --algo=ppo \
    --use-gae \
    --lr=2.5e-4 \
    --clip-param=0.1 \
    --value-loss-coef=0.5 \
    --num-processes=150 \
    --num-steps=500 \
    --num-mini-batch=4 \
    --log-interval=1 \
    --save-interval=10 \
    --eval-interval=20 \
    --use-linear-lr-decay \
    --popart-reward \
    --entropy-coef=0.01 \
    --gamma=0.999

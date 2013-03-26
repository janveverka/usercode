## Source me to make data/MC comparison plots
rootplot vg_data_test.root vg_zg_test.root \
    --legend-entries=Data,MC \
    --data=1 \
    --normalize=1 \
    --draw='hist' \
    --stack \
    --fill \
    --grid \
    --ratio-split=1 \
    --output=test.plots \

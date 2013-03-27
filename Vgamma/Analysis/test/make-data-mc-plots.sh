## Source me to make data/MC comparison plots
rootplot data.root zz.root wz.root zjets.root zmmg.root \
    --legend-entries=Data,zz,wz,Zjets,Zgamma \
    --data=1 \
    --normalize=1 \
    --draw='hist' \
    --stack \
    --fill \
    --grid \
    --ratio-split=1 \
    --output=test.plots \
    --logy

# USAGE: . make-plots.sh

rootplotmpl vecbos_official.root Pileup2D \
    --ymin=0.0 --output=official --draw2D=colz --legend-entries=Official

rootplotmpl vecbos_private_v3.root Pileup2D \
    --ymin=0.0 --output=private_v3  --draw2D=colz --legend-entries='Private v3'

# rootplotmpl rootplot_config.py \
#     --normalize=2 --ymin=0.0 --output=liny --grid \
#     --legend-entries=Official,Private --data=2 --ratio-split=1

# rootplot rootplot_config.py \
#     --normalize=2 --ymin=0.0 --output=logy --grid --logy --hist \
#     --legend-entries=Official,Private --data=2 --ratio-split=1

rootplotmpl rootplot_config.py --output=liny 

rootplotmpl rootplot_config.py --output=logy --logy --hist

# rootplotmpl vecbos_official.root vecbos_private.root \
#     --ymin=0.0 --output=ratio \
#     --legend-entries=Official,Private --ratio=1

DIR=public_html/plots/$(date +%Y)/$(date +%y-%m-%d)

ssh positron01.hep.caltech.edu \
    "echo \"if [[ ! -d $DIR ]]; then mkdir -p $DIR; fi\" | bash"

tar czf plots.tgz liny/ logy/ official/ private_v3/ && \
    scp plots.tgz positron01.hep.caltech.edu:$DIR && \
    ssh positron01.hep.caltech.edu "cd $DIR && tar xzf plots.tgz"

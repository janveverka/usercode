# USAGE: . make-plots.sh
PRIVATE_VERSION=${1:-1}
rootplotmpl vecbos_official.root Pileup2D \
    --ymin=0.0 --output=official --draw2D=colz --legend-entries=Official

rootplotmpl vecbos_private_v${PRIVATE_VERSION}.root Pileup2D \
    --ymin=0.0 --output=private_v${PRIVATE_VERSION}  --draw2D=colz \
    --legend-entries="Private v${PRIVATE_VERSION}"

# rootplotmpl rootplot_config.py \
#     --normalize=2 --ymin=0.0 --output=liny --grid \
#     --legend-entries=Official,Private --data=2 --ratio-split=1

# rootplot rootplot_config.py \
#     --normalize=2 --ymin=0.0 --output=logy --grid --logy --hist \
#     --legend-entries=Official,Private --data=2 --ratio-split=1

rootplotmpl rootplot_config_v${PRIVATE_VERSION}.py \
    --output=liny_v${PRIVATE_VERSION} 

rootplotmpl rootplot_config_v${PRIVATE_VERSION}.py \
    --output=logy_v${PRIVATE_VERSION} --logy --hist

# rootplotmpl vecbos_official.root vecbos_private.root \
#     --ymin=0.0 --output=ratio \
#     --legend-entries=Official,Private --ratio=1

DIR=public_html/plots/$(date +%Y)/$(date +%y-%m-%d)

ssh positron01.hep.caltech.edu \
    "echo \"if [[ ! -d $DIR ]]; then mkdir -p $DIR; fi\" | bash"

tar czf plots.tgz liny_v${PRIVATE_VERSION}/ logy_v${PRIVATE_VERSION}/ \
        official/ private_v${PRIVATE_VERSION}/ && \
    scp plots.tgz positron01.hep.caltech.edu:$DIR && \
    ssh positron01.hep.caltech.edu "cd $DIR && tar xzf plots.tgz"


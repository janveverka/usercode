# USAGE: . make-plots.sh

rootplotmpl vecbos_official.root \
    --ymin=0.0 --output=official --draw2D=colz --legend-entries=Official

rootplotmpl vecbos_private.root \
    --ymin=0.0 --output=private  --draw2D=colz --legend-entries=Private

rootplotmpl vecbos_official.root vecbos_private.root \
    --normalize=2 --ymin=0.0 --output=liny \
    --legend-entries=Official,Private --data=2 --processors=1

rootplotmpl vecbos_official.root vecbos_private.root \
    --normalize=2 --ymin=0.0 --output=logy --logy --hist \
    --legend-entries=Official,Private --data=2 --processors=1

# rootplotmpl vecbos_official.root vecbos_private.root \
#     --ymin=0.0 --output=ratio \
#     --legend-entries=Official,Private --ratio=1

DIR=public_html/plots/$(date +%Y)/$(date +%y-%m-%d)

ssh positron01.hep.caltech.edu \
    "echo \"if [[ ! -d $DIR ]]; then mkdir -p $DIR; fi\" | bash"

tar czf plots.tgz liny/ logy/ official/ private/ && \
    scp plots.tgz positron01.hep.caltech.edu:$DIR && \
    ssh positron01.hep.caltech.edu "cd $DIR && tar xzf plots.tgz"
# USAGE: . make-plots.sh

rootplotmpl vecbos_official.root \
    --ymin=0.0 --output=official --legend-entries=Official

rootplot vecbos_private.root \
    --ymin=0.0 --output=private --legend-entries=Private

rootplot vecbos_official.root vecbos_private.root \
    --normalize=2 --ymin=0.0 --output=liny \
    --legend-entries=Official,Private --draw2D=colz

rootplot vecbos_official.root vecbos_private.root \
    --normalize=2 --ymin=0.0 --output=logy --logy \
    --legend-entries=Official,Private --draw2D=colz

DIR=public_html/plots/$(date +%Y)/$(date +%y-%m-%d)

ssh positron01.hep.caltech.edu \
    "echo \"if [[ ! -d $DIR ]]; then mkdir -p $DIR; fi\" | bash"

tar czf plots.tgz liny/ logy/ official/ private/ && \
    scp plots.tgz positron01.hep.caltech.edu:$DIR && \
    ssh positron01.hep.caltech.edu "cd $DIR && tar xzf plots.tgz"
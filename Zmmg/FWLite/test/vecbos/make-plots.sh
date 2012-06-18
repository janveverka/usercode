# USAGE: . make-plots.sh

rootplot vecbos_official.root vecbos_private.root rootplot_config.py \
    --normalize=2 --ymin=0.0 --output=liny

rootplot vecbos_official.root vecbos_private.root rootplot_config.py \
    --normalize=2 --ymin=0.0 --output=logy --logy

DIR=public_html/plots/$(date +%Y)/$(date +%y-%m-%d)

ssh positron01.hep.caltech.edu \
    "echo \"if [[ ! -d $DIR ]]; then mkdir -p $DIR; fi\" | bash"

tar czf plots.tgz liny/ logy/ && \
    scp plots.tgz positron01.hep.caltech.edu:$DIR && \
    ssh positron01.hep.caltech.edu "cd $DIR && tar xzf plots.tgz"
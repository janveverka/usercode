rootplotmpl vecbos_test.root \
    --ymin=0.0 --legend-entries=Test --ymin=0.0 --draw2D=colz --output=test

DIR=public_html/plots/$(date +%Y)/$(date +%y-%m-%d)

ssh positron01.hep.caltech.edu \
    "echo \"if [[ ! -d $DIR ]]; then mkdir -p $DIR; fi\" | bash"

tar czf test.tgz test/ && \
    scp test.tgz positron01.hep.caltech.edu:$DIR && \
    ssh positron01.hep.caltech.edu "cd $DIR && tar xzf test.tgz"

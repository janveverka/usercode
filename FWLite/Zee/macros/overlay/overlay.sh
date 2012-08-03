## Usage: source run.sh
echo "Making the overlay plot of two Z fits..." && \
    root -l -b -q fitZraw.C < tight.in 2>&1 | tee tight.out && \
    root -l -b -q fitZraw.C < mva.in 2>&1 | tee mva.out && \
    root -l overlay.C

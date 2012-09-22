#!/bin/bash
CONFIG=${1:-$CMSSW_BASE/src/Vgamma/Analysis/test/vg_test_cfg.py}
vg-analyze $CONFIG
ROOTFILE=$(ls -rt *.root | tail -1)
rootplot $ROOTFILE --output=${ROOTFILE%*.root}.plots

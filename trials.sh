#! /bin/bash

declare -a pkgs=("pandas" "dplython" "dfply" "siuba" "siuba-fast" "datar")

for x in ${pkgs[@]}; do
    echo "--- $x --- "
    ipython trials.py $x
done
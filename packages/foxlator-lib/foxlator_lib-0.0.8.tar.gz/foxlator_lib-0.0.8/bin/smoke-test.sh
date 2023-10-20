#!/bin/bash
# --- Script used to perform a smoke test on a newly built package
python3.10 -m pip install ./dist/foxlator_lib*.whl --force-reinstall
version=$(python3.10 -c 'import foxlator_lib as fll; print(fll.utils.get_version())' 2>&1)

if [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
    echo "$ - Smoke test passed!"
else
    echo "$ - ERROR! smoke test failed:" $version
    exit -1
fi

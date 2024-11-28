

#!/bin/sh
#kill all python processes
pkill -9 Python
pkill -9 Python3
pkill -9 Python3.9
pkill -9 Python3.8
pkill -9 Python3.7

#get system information
chip=$(arch)
os_ver=$(sw_vers -productVersion)

python_ver="3.9"
if [ $chip = 'i386' ]; then
    if echo -e "$os_ver \n10.15.0" | sort -V | tail -n1 | grep -Fq "10.15.0"; then
        python_ver="3.7"
        printf "Correct python ver: 3.7"
    elif echo -e "$os_ver \n12.0.0" | sort -V | tail -n1 | grep -Fq "12.0.0"; then
        python_ver="3.8"
        printf "Correct python ver: 3.8"
    fi
fi

cd "$(dirname "$0")"
if [ -d bin ]; then
   source ./bin/activate
   printf "activating virtual environment"
fi
cd src
python3.7 fisch.py
python3.8 fisch.py
python3.9 fisch.py

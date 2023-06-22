#!/bin/bash
cd SATA_bin
# start SATA tool
python3 SATA_execute_tool.py
# first plot
python3 SATA_coord_zoom.py
python3 SATA_coord_sections.py
python3 SATA_last_ten_eqs.py
./combined_plots.sh
# start the banner in background
python3 SATA_close_banner.py &
# refresh earthquake list and notify every 5 minutes
sleep 300 # wait 5 minutes
while test -f temp/running; do
python3 SATA_refresh.py # check for a refresh of earthquake list
fuser -k -TERM combined_plots.pdf # close open pdf
python3 SATA_coord_zoom.py
python3 SATA_coord_sections.py
python3 SATA_last_ten_eqs.py
./combined_plots.sh # plot new list
# send notification
now=$(date)
notify-send "SATA" "Last update: $now"
sleep 300 # wait 5 minutes
done
rm -r temp combined_plots.pdf

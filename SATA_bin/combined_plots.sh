#!/bin/bash

string1="temp/path"
string2=$(cat "$string1")
string1="Plots/Eqs_gmt.txt"

terremoti=$string2$string1
cpt_file="cpt_file"

tail -n 1 "${terremoti}" > last_earthquake
head -n -1 "${terremoti}" > old_earthquakes

cut -f7 -d$'\t' last_earthquake > lat_last_earthquake
cut -f8 -d$'\t' last_earthquake > lon_last_earthquake

cut -f3 -d$'\t' last_earthquake > year_month_day
cut -f2 -d$'\t' last_earthquake >> year_month_day
cut -f1 -d$'\t' last_earthquake >> year_month_day
sed -i ':a;N;$!ba;s/\n/-/g' year_month_day

cut -f4 -d$'\t' last_earthquake > hour_minut_sec
cut -f5 -d$'\t' last_earthquake >> hour_minut_sec
cut -f6 -d$'\t' last_earthquake >> hour_minut_sec
sed -i ':a;N;$!ba;s/\n/:/g' hour_minut_sec

cut -f7 -d$'\t' last_earthquake > coord_string
echo " " >> coord_string
cut -f8 -d$'\t' last_earthquake >> coord_string
sed -i ':a;N;$!ba;s/\n//g' coord_string

cut -f9 -d$'\t' last_earthquake > depth
echo " km" >> depth
sed -i ':a;N;$!ba;s/\n//g' depth

cut -f10 -d$'\t' last_earthquake >> magnitude
echo " Mw" >> magnitude
sed -i ':a;N;$!ba;s/\n//g' magnitude

echo "Last eqs: " > all_data
cat year_month_day >> all_data
echo " " >> all_data
cat hour_minut_sec >> all_data  
echo " - " >> all_data
cat coord_string >> all_data
echo " - " >> all_data
cat depth >> all_data
echo " - " >> all_data
cat magnitude >> all_data
sed -i ':a;N;$!ba;s/\n//g' all_data

rm hour_minut_sec depth coord_string magnitude year_month_day 

python3 SATA_coord_zoom.py
coord_gmt=$(cat ./temp/coord_gmt)
all_data=$(cat all_data)
gmt makecpt -Crainbow -T0/100/2 -Z > $cpt_file
gmt begin combined_plots
    # Primo subplot: mappa_sismicita_scaled_mg_depth_full_italy
    gmt subplot begin 1x2 -Fs14c/8c -M1.2c 
        gmt subplot set 0,0
        gmt coast -R6/19/36/48 -JM6i -B -Glightgray -Na0.5 -B+glightblue -W0.3p,black
        gmt psxy DISS_gmt/CSSTOP321.gmt -R6/19/36/48 -JM6i -W0.5,red -t70
        gmt psxy DISS_gmt/CSSPLN321.gmt -R6/19/36/48 -JM6i -W0.1 -G"#FF0000AA" -t85
        gmt plot old_earthquakes -Wfaint -R6/19/36/48 -JM6i -i7,6,8,9+s0.05 -Scc -C$cpt_file
        gmt plot last_earthquake -Wfaint -R6/19/36/48 -JM6i -i7,6,8,9 -Sa0.28 -Gyellow
    # Secondo subplot: mappa_sism_zoom
        gmt subplot set 0,1 
        gmt coast -R$coord_gmt -JM6i -B -Glightgray -Na0.5 -W0.5,black -B+glightblue
        gmt psxy DISS_gmt/CSSTOP321.gmt -R$coord_gmt -JM6i -W0.5,red -t70
        gmt psxy DISS_gmt/CSSPLN321.gmt -R$coord_gmt -JM6i -W0.1 -G"#FF0000AA" -t85
        gmt plot old_earthquakes -Wfaint -R$coord_gmt -JM6i -i7,6,8,9+s0.20 -Scc -C$cpt_file
        gmt plot last_earthquake -Wfaint -R$coord_gmt -JM6i -i7,6,8,9 -Sa0.80 -Gyellow
    	gmt subplot end
   gmt colorbar -C$cpt_file -DjCB+w3i/0.1i+o0.5i/0i+h -Bxa20f5 -By+l"Eq. Depth" -X7.5 -Y18
   echo -e "$(cat all_data)" | gmt text -R9/10/1/11 -JM6i -Bn -F+cTL+f13p -X+10.3 -Y-153 -N
gmt end show

rm old_earthquakes lat_last_earthquake lon_last_earthquake cpt_file last_earthquake all_data #coord_gmt

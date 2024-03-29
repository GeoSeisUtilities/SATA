#!/bin/bash

string1="temp/path"
string2=$(cat "$string1")
string1="Plots/Eqs_gmt.txt"

terremoti=$string2$string1
cpt_file="cpt_file"

tail -n 1 "${terremoti}" > last_earthquake
head -n -1 "${terremoti}" > old_earthquakes
#tolgo l'header per la parte di GMT per le sezioni
tail -n +2 old_earthquakes > old_earthquake_nohead

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

echo "Last eq: " > all_data
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

length_sect=$(awk -F'\t' '{print $1}' ./temp/sez_gmt)
depth=$(awk -F'\t' '{print $2}' ./temp/sez_gmt)
start_lat=$(awk -F'\t' '{print $3}' ./temp/sez_gmt)
start_lon=$(awk -F'\t' '{print $4}' ./temp/sez_gmt)
end_lat=$(awk -F'\t' '{print $5}' ./temp/sez_gmt)
end_lon=$(awk -F'\t' '{print $6}' ./temp/sez_gmt)

echo "${start_lon}" "${start_lat}" > temp/coord_section_map_view
echo "${end_lon}" "${end_lat}" >> temp/coord_section_map_view

coord_gmt=$(cat ./temp/coord_gmt)
all_data=$(cat all_data)


gmt makecpt -Crainbow -T0/100/2 -Z > $cpt_file
gmt begin combined_plots
    gmt subplot begin 2x2 -Fs14c/8c -M1.2c 
        # Primo subplot: mappa_sismicita_scaled_mg_depth_full_italy
        gmt subplot set 0,0
        gmt coast -R6/19/36/48 -JM6i -B -Glightgray -Na0.5 -B+glightblue -W0.3p,black
        gmt grdimage @earth_gebco_02m -R6/19/36/48 -JM6i -t80
        gmt psxy DISS_gmt/CSSTOP321.gmt -R6/19/36/48 -JM6i -W0.5,red -t60
        gmt psxy DISS_gmt/CSSPLN321.gmt -R6/19/36/48 -JM6i -W0.1 -G"#FF0000AA" -t75
        gmt plot DISS_gmt/Cities.txt -R6/19/36/48 -JM6i -SS0.1c -Wblack -Gwhite
        gmt text DISS_gmt/Cities.txt -R6/19/36/48 -JM6i -F+f5p,black -D0.15/0.15
        gmt plot old_earthquakes -Wfaint -R6/19/36/48 -JM6i -i7,6,8,9+s0.05 -Sc -C$cpt_file #-Scc
        gmt plot temp/coord_section_map_view -R6/19/36/48 -JM6i -Wblack
        gmt plot temp/coord_section_map_view -R6/19/36/48 -JM6i -Sc0.1c -Wblack
        gmt plot last_earthquake -Wfaint -R6/19/36/48 -JM6i -i7,6,8,9 -Sa0.28 -Gyellow
        # Secondo subplot: mappa_sism_zoom
        gmt subplot set 0,1 
        gmt coast -R$coord_gmt -JM6i -B -Glightgray -Na0.5 -W0.5,black -B+glightblue
        gmt grdimage @earth_gebco_03s -R$coord_gmt -JM6i -t80
        #gmt grdimage @earth_relief_03s -R$coord_gmt -JM6i -Cgray -t20
        gmt psxy DISS_gmt/CSSTOP321.gmt -R$coord_gmt -JM6i -W2,red -t60
        gmt psxy DISS_gmt/CSSPLN321.gmt -R$coord_gmt -JM6i -W0.1 -G"#FF0000AA" -t85
        gmt text DISS_gmt/Fault_names.txt -R$coord_gmt -JM6i -F+f12p,Helvetica,red
        gmt plot DISS_gmt/Cities.txt -R$coord_gmt -JM6i -SS0.3c -Wblack -Gwhite
        gmt text DISS_gmt/Cities.txt -R$coord_gmt -JM6i -F+f11p,black -D0.4/0.4
        gmt plot old_earthquakes -Wfaint -R$coord_gmt -JM6i -i7,6,8,9+s0.20 -Scc -C$cpt_file
        gmt plot temp/coord_section_map_view -R$coord_gmt -JM6i -Wblack
        gmt plot temp/coord_section_map_view -R$coord_gmt -JM6i -Sc0.2c -Wblack
        gmt plot temp/coord_section_start -JM6i -Sl0.5c+tA -D-0.3/-0.3 -Wblack -Gblack
        gmt plot temp/coord_section_end -JM6i -Sl0.5c+tB -D0.3/0.3 -Wblack -Gblack
        gmt plot last_earthquake -Wfaint -R$coord_gmt -JM6i -i7,6,8,9 -Sa0.80 -Gyellow
        gmt subplot end
    # Terzo subplot (non proprio): section
    gmt psbasemap -JX23.0c/8.5c -R0/$length_sect/$depth/3 -B10g10 -Y1.5
    
    for source in $(ls DISS_gmt/vertex_sources/);
    do   
    	gmt project DISS_gmt/vertex_sources/${source} -C$start_lon/$start_lat -E$end_lon/$end_lat -Q -W-0.5/0.5 > temp/projected_DISS
    	sort -k2 -r temp/projected_DISS > temp/projected_DISS_
    	mv temp/projected_DISS_ temp/projected_DISS
    	gmt psxy temp/projected_DISS -JX23.0c/8.5c -R0/$length_sect/$depth/3 -i3,2 -W3,red #-Ss0.1
    done
    echo 0	$depth > temp/label
    gmt plot temp/label -JX23.0c/8.5c -Sl1c+tA -D0.5/0.5 -Wblack -Gblack
    echo $length_sect	$depth > temp/label
    gmt plot temp/label -JX23.0c/8.5c -Sl1c+tB -D-0.5/0.5 -Wblack -Gblack
    # parte del terzo plot per avere la topografia sulla sezione
    gmt grdtrack -G@earth_relief_01m -E$start_lon/$start_lat/$end_lon/$end_lat -N > ciao
    while read -r line; do
	colonna=$(echo "$line" | awk '{printf "%.3f", $3/1000}')
	echo "$colonna" >> output
    done < ciao
    tr ',' '.' < output > output2
    paste -d '\t' ciao output2 > output3
    rm output output2 ciao
    gmt project output3 -C$start_lon/$start_lat -E$end_lon/$end_lat -Q -W-30/30 -i0,1,3 > proiezione_output
    gmt plot proiezione_output -JX23.0c/8.5c -R0/$length_sect/$depth/3 -W2p,blue -i3,2
    # fine del plot con i terremoti, sia l'ultimo che gli altri in sezione  
    gmt project last_earthquake -C$start_lon/$start_lat -E$end_lon/$end_lat -Q -W-10/10 -i7,6,10 > temp/proiezione_sez_SATA_last
    gmt project old_earthquake_nohead -C$start_lon/$start_lat -E$end_lon/$end_lat -Q -W-10/10 -i7,6,10 > temp/proiezione_sez_SATA_old
    gmt psxy temp/proiezione_sez_SATA_old -JX23c/8.5c -R0/$length_sect/$depth/3 -i3,2 -Sc0.2 -Gpurple -W0.05,black
    gmt psxy temp/proiezione_sez_SATA_last -JX23c/8.5c -R0/$length_sect/$depth/3 -i3,2 -Sa0.5 -Gyellow -W0.05,black
    # Quarto subplot (non proprio): elenco ultimi 10 terremoti
    gmt pstext temp/table_ten_eqs -R-15/18/0.5/11.5 -JX8.5 -B0 -F+f10p,Helvetica -X23.8
    gmt colorbar -C$cpt_file -DjCB+w3i/0.1i+o0.5i/0i+h -Bxa20f5 -By+l"Eq. Depth" -X-22 -Y29
    echo -e "$(cat all_data)" | gmt text -R0/1/0/1 -JM6i -Bn -F+cTL+f13p -Y-13.7 -X-1 -N
    gmt text DISS_gmt/info -R-3/3/0/3 -JX30c/1 -Bn -F+f11p,Helvetica -Y-17
gmt end show


rm old_earthquakes old_earthquake_nohead lat_last_earthquake lon_last_earthquake cpt_file last_earthquake temp/proiezione_sez_SATA_last all_data output3 proiezione_output #coord_gmt temp/proiezione_sez_SATA_old


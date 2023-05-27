# SATA - Seismicity Automatic Tool Analysis

SATA is a Python and GMT tool designed to automatically retrieve data from the INGV (http://terremoti.ingv.it/) online earthquakes database. It captures earthquake information and generates real-time plots. This *readme.md* file provides a comprehensive overview of the tool in its current release. Furthermore, quick commands and relevant information are also available within each window of the SATA GUI (Graphical User Interface).

## *Hardware and software specification*

SATA works on Linux (tested on Manjaro 22.1.2 and Ubuntu 22.04.02 LTS). However, it should work also on Windows machines by using a WSL system (Windows Subsystem Linux) that is available on the official Microsoft Store (many OS are available but we suggest using Ubuntu). 

SATA does not consume many resources: its reactivity depends on hardware specifications but, especially, depends on the internet connection and the velocity of download.

The tool requires:

- Python (version >= 3) and the modules above (to be manually installed)
  
  - tkinter module
  
  - bs4 module
  
  - plyer module

- GMT (version > 6)

## *How it works*

SATA tool is composed of a 'main' script (the one you have to run in a terminal) called  *SATA_tool.sh*. It is a bash script which simply runs a sequence of scripts as described inside it. These Python and bash scripts are stored in the *SATA_bin* folder and they are (in order of execution):

- SATA_execute_tool.py - it launches the starting GUI of SATA. Here you can choose the store folder and the frequency for splitting the earthquake list (for more information see ***Usage: input - output*** chapter). When the tool starts, it downloads the last week's seismic events from the INGV online database; these require some minutes depending on the number of earthquakes and the internet velocity. A notification will advise the user about the start of the first download phase. This script also creates the storage folder *SATA_tool_files* in the directory set by the user and a *temp* folder inside *SATA_bin*. 

- SATA_coord_zoom.py - it reads the coordinates of the last earthquake to calculate the boundary of the second plot (see after).

- combined_plots.sh - this bash script runs GMT to create and show a plot of downloaded earthquakes; each plot contains the main seismogenic faults as reported by the DISS database ([DISS - Mapper](https://diss.ingv.it/diss330/dissmap.html)). The plot is composed of two panels: 
  
  - On the left is an 'Italy plot' representing the last 300 earthquakes of the INGV database. Different points dimensions are related to different magnitudes. The last seismic event is plotted as a star.
  
  - On the right a 'Detailed plot' which is a zoom of 1°x1° on the last available earthquake. On the top, there is the colour bar used to classify events by depth, and a summary of the last earthquake. This is a really interesting plot in the case of a seismic sequence because it allows having an automatic zoom on the sequence in real-time. Depth and magnitude follow the same scales as the other plot.

- SATA_close_banner.py - the python script create a banner to advise the user that SATA is running. The banner has two buttons for controlling the SATA actions:
  
  - *Save plot* button: it saves the plot you are shown on screen in pdf format. The plot is stored together with the input GMT files in a folder (under the *'SATA_tool_files/Plots/'* path) named by the date and time of the button pushing.
  
  - *Stop tool* button: SATA checks the existence of a file called *running* stored in the *temp* folder. This button deletes the *running* file to stop the tool at the next check. As a consequence, the GUI window will disappear but SATA will be completely stopped at the next refresh. The refresh time is set at 5 minutes (300 seconds) but it can easily be changed by modifying the main script *SATA_tool.sh* at line 18 (*sleep 300*)

- SATA_refresh.py - it reads the first page of the INGV database (last 30 events) and checks if there are new events to be stored locally and to be plotted. The comparison is made using the events ID. The main bash script runs it each 5 minutes and a notification will be shown on the screen reporting the time of the last refresh. This script also split the earthquake list following the preferences set by the user in the first window of the GUI (see next chapter).

## *Usage: input - output*

SATA requires only the storage path and the preference of storage for the earthquakes list. The directory can be indicated by pasting the complete path in the available space, or by clicking on the *browse* button and navigating in the preferred folder. Once started the tool will create a *SATA_tool_files* folder containing two subdirectories:

- Earthquakes - contain the list of seismic events appended in the last week, the actual list to be refreshed every 5 minutes and all the lists split by the time selected (see below).

- Plots - contains the files of coordinates to plot earthquakes with GMT and a folder for each saved plot: by pushing the *Save plot* button a folder named with the actual time is created; it contains the plot and the input GMT files.

SATA storage in the *Earthquakes* folder lists of seismic events for a precise period of time as reported by the list name. In the first window of the tool the user can decide the length of earthquake lists in terms of consecutive days:

- Daily: it creates a separate list of events for each day.

- Weekly: it creates a separate list of events for each week. SATA considers a week as composed of 7 consecutive days starting from the day it begins the download.

- Monthly: it creates a separate list of events for each week. SATA considers a week as composed of 30 consecutive days starting from the day it begin the download.

## *Usage: tool*

For using SATA, clone the repository or download it as a zip. The files can be stored everywhere on the local PC but you must maintain the relative position of files (do not move *SATA_tool*.sh without moving *SATA_bin* and do not put it inside the latter folder).

To run SATA you should need two steps:

1) Make bash scripts executable
   
   ```bash
   cd /your-download-directory/
   chmod +x SATA_tool.sh
   cd SATA_bin
   chmod +x combined_plot.sh
   ```
2. Simply run it
   
   ```bash
   ./SATA_tool.sh
   ```

The dimension of storage will variate depending on how long you will use the tool (each earthquake is stored in a text file so the dimension should not be so big). The only space allocated is the one in the folder set by the user: the dimension of the folder containing SATA scripts will not change more than some KiloBytes (the dimension of the *temp* folder)

## *Bugs and upgrades*

One known bug is about the transparency of seismogenic structures on the GMT plots. The command of transparency works properly only on some PC but it should be a problem with the version of Ghostscript (package for managing ps files) or GMT. It works with version 9 of GS.

A future upgrade will include another plot showing earthquakes represented in the 'zoomed' area through a cross vertical section.

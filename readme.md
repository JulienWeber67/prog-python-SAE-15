# Data sets location
This directory contains three another ones related to the data sets and called **raw**, **processed**, **cleaned**. A description of each one is given below. 

## Raw directory
This directory contains original and immutable data sets. Do not edit raw data, especially with Excel, open files only in read only mode. Each data file is related to an energy consumption profile of the Fipy Pycomm device with a different coding rate and a couple of spreading factors either seven or twelve. All data files have the following structure :

- Timestamp (in second),
- File Main Current (in A),
- File Main Voltage (in V),
- File Main Energy (in J),
- File UART (TXT).

The TimeStamp field indicates when the observations have been made. The current, voltage fields contains information on the current and voltage needed by the device. The energy field indicate the total energy consumed by the device. The last field contains received or sent text through the UART link, it was always used as debug information. Le nommage de chaque fichier respecte le formalisme suivant : *energy-bande passante-facteur d'étalement-taux de bits redondants.csv*.  

## Processed directory
This directory contains intermediate transformed data sets. This working directory could contain multiple data sets.

## Cleaned directory
This directory contains canonical data sets could be used for publication. These data sets would be used for the analysis.

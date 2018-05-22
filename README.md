# GenerateSPLConquerorExperiments
#### Contains all the code needed to create and generate SPLConqueror Experiments with Thor

The idea is that with a simple script the experiments are created (see create_experiments.py) and as a json string stored in a .txt file.

This experiment file is used as input for generate_all.py. This script with the help of the scripts calc_configuration.py and create_a_scripts.py uses Thor to generate the performance influence model (Stored in the files featSolution.txt and interactionSolution.txt that are output from Thor) then calculates a measurements.xml data that SPLConqueror can use as input. Finally for all experiments the corresponding .a scripts are created. With those scripts the experiments can be finaly conducted.

This is done to allow the main generation of the data to be done on the cluster and just uploading a experiments.txt.

The arguments for generate_all.py are:
1. path where the generated experiments will be stored
2. path to the experiments.txt
3. path to the feature model
4. path to the a file that contains all configurations
5. bool if the experiments have interactions (ThorCOM can not generate data with no interactions)
6. int number of repetitions (each experiment will repeated multiple times to account for varying generated data)

An example folder is included in the repo with a test feature model and configuration.
Additionally in the ExampleArgs.txt file example arguments for the generate_all.py script are given. 
Please replace the '.' and give the explicit path to each file.

## calc_pemoco Info

PeMoCo requires two SPLConqueror .log files so it can compare the two performance-influence models.
This script uses an existing SPLConqueror .log file and the feat and interaction solution of Thor to generate a new reference .log file.

These two files with the measurements.csv and the feature model are all needed as input for PeMoCo.
Additionally as the measurements file were orignally .xml files, there is a method included that rewrites the measuremnts file to a .csv file

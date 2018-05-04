# GenerateSPLConquerorExperiments
#### Contains all the code needed to create and generate SPLConqueror Experiments with Thor

The idea is that with a simple script the experiments are created (see create_experiments.py) and as a json string stored in a .txt file.
This experiment file is used as input for generate_all.py. This script with the help of the scripts calc_configuration.py and create_a_scripts.py uses Thor to generate the performance influence model (Stored in the files featSolution.txt and interactionSolution.txt that are output from Thor) then calculates a measurements.xml data that SPLConqueror can use as input. Finally for all experiments the corresponding .a scripts are created. With those scripts the experiments can be finaly conducted.

This is done to allow the main generation of the data to be done on the cluster and just uploading a experiments.txt.

The arguments for generate_all.py are:
1. path where the generated experiments will be stored
2. path to the experiments.txt
3. path to the a file that contains all configurations
4. bool if the experiments have interactions (ThorCOM can not generate data with no interactions)
5. int number of repetitions (each experiment will repeated multiple times to account for varying generated data)

An example will be provided later on.

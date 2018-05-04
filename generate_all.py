import os
import time
import sys
import json
import calc_configuration
import create_a_scripts

thor_dist_path = "C:\\Users\\Jakob\\Documents\\BachelorThesisOtherRepos\\thor-avm\\corpusData\\DistributionProfiles\\"
thor_exe = "C:\\Users\\Jakob\\Documents\\BachelorThesisOtherRepos\\ThorFork\\thor-avm\\Thor\\ThorCOM\\bin\\Debug\\ThorCOM.exe"
progress_file_path = "C:\\Users\\Jakob\\Documents\\progress.txt"
#thor_dist_path = "/scratch/hoffmanj/Thor/DistributionProfiles/"
#thor_exe = "/scratch/hoffmanj/Thor/ThorCOM/bin/Debug/ThorCOM.exe"
#progress_file_path = "/scratch/hoffmanj/progress.txt"


def generate_experiments(experiments, base_path, repetitions):
    progress_file = open(progress_file_path, 'a+')
    progress_file.write("Thor Progress:\n")
    progress_file.close()
    experiment_nr = 1
    total_nr = len(experiments)
    for experiment in experiments:
        experiment_path = base_path + os.sep + experiment[0]
        start_time = time.time()
        generate_scripts(experiment_path, experiment, repetitions)
        elapsed_time = int(time.time() - start_time) / 60
        progress_file = open(progress_file_path, 'a+')
        progress_file.write(
            str(experiment_nr) + "/" + str(total_nr) + "ElapsedTime = " + str(elapsed_time) + "minutes\n")
        progress_file.close()
        experiment_nr = experiment_nr + 1


def generate_scripts(experiment_path, experiment, repetitions):
    for i in range(repetitions):
        path = experiment_path + os.sep + str(i) + os.sep
        generate_script(path, experiment, seed=i+1)
        execute_thor(path + "script.txt", i)
        clean_up_after_thor(path)
        add_root_offset(path + "featSolution.txt", experiment[9])


# experiment = ("id_string", "fm path", "f dist path/string", "i dist path/string", "variant dist path", "i count", "i order", "f scale", "i scale", "root offset")
def generate_script(path, experiment, seed):
    print(experiment)
    os.makedirs(path)
    script = open(path + "script.txt", "w")
    script.write("set output " + path + "\n")
    script.write("set log_folder " + path + "\n")
    script.write("set logging true\n")
    script.write("load model " + experiment[1] + "\n")
    script.write("load feature_distribution " + experiment[2] + "\n")
    script.write("load interaction_distribution " + experiment[3] + "\n")
    script.write("load variant_distribution " + experiment[4] + "\n")
    script.write("set interaction_count " + experiment[5] + "\n")
    script.write("set interaction_degrees " + experiment[6] + "\n")
    script.write("set seed " + str(seed) + "\n")
    if experiment[7][0]:
        script.write("set feature_scale_min " + str(experiment[7][1]) + "\n")
        script.write("set feature_scale_max " + str(experiment[7][2]) + "\n")
        script.write("set feature_scale_early\n")
    if experiment[8][0]:
        script.write("set interaction_scale_min " + str(experiment[8][1]) + "\n")
        script.write("set interaction_scale_max " + str(experiment[8][2]) + "\n")
        script.write("set interaction_scale_early\n")
    script.writelines([
        "set feature_fitness true\n",
        "set interaction_fitness true\n",
        "set variant_fitness false\n",
        "set variant false\n",
        "set euclidean_distance true\n",
        "set weight_feature 1\n",
        "set weight_interaction 1\n",
        "set weight_variant 0\n"
        "set scale_interactions true\n"])
    script.close()


def execute_thor(arg_path, counter):
    print(arg_path)
    os.system(thor_exe + " " + arg_path)
    print("Thor Startet" + str(counter))


def clean_up_after_thor(path):
    allowed_files = ["script.txt", "featSolution.txt", "interactionSolution.txt","Fitn"]
    for filename in os.listdir(path):
        if filename not in allowed_files:
            os.remove(path + filename)
    if len(os.listdir(path)) < 2:
        print("Error")


def add_root_offset(file_path, offset):
    file = open(file_path, "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        line_value = line.split(":")
        if line_value[0] == "root":
            lines.remove(line)
            lines.append("root: " + str(float(line_value[1]) + float(offset)))
            print(lines)
            file = open(file_path, "w")
            file.writelines(lines)
            file.close()
            break


def open_experiments(path):
    data = open(path).read()
    return json.loads(data)


if __name__ == '__main__':
    progress_file = open(progress_file_path, 'a+')
    progress_file.write("Script started\n")
    progress_file.close()
    base_path = sys.argv[1]
    experiments_path = sys.argv[2]
    feature_model_path = sys.argv[3]
    configuration_path = sys.argv[4]
    has_interactions = bool(sys.argv[5])
    repetitions = 10
    if len(sys.argv) > 6:
        repetitions = int(sys.argv[6])
    experiments = open_experiments(experiments_path)
    print(len(experiments))
    generate_experiments(experiments=experiments, base_path=base_path, repetitions=repetitions)
    calc_configuration.calc_all(base_path=base_path, configuration_path=configuration_path,
                                has_interactions=has_interactions)
    create_a_scripts.generate_a_scripts(base_path=base_path, out_path=base_path + os.sep + "Scripts",
                                        feature_model_path=feature_model_path, sampling="select-all-measurements true")



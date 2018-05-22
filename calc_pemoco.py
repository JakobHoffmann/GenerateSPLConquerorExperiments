import os
import xml.etree.ElementTree as ET
import csv
pemoco_path = "C:\\Users\\Jakob\\Documents\\BachelorThesisOtherRepos\\PeMoCo\\PeMoCo\\bin\\Debug\\PeMoCo.exe"


def calc_all_pemoco(experiment_path, fm_path):
    for folder in os.listdir(experiment_path):
        if folder not in ["Scripts", "ExperimentsUtil"]:
            for experiment_nr in os.listdir(experiment_path + os.sep + folder):
                start_pemoco(os.path.join(experiment_path, folder, experiment_nr), fm_path)


def start_pemoco(path, fm_path):
    prepare_reference_log(path)
    if not os.path.isfile(path + os.sep + "measurements.csv"):
        convert_measurements_to_csv(path + os.sep + "measurements.xml")
    featureModel = fm_path
    equationFile = path + os.sep + "log.log"
    logFile = path + os.sep + "log_true.log"
    csvResultFile = path + os.sep + "measurements.csv"
    outputFile = path + os.sep + "pemoco_out.txt"
    args = " --featureModel " + featureModel + " --equationFile " + equationFile + " --logFile " + logFile + " --csvResultFile "+ csvResultFile + " --outputFile " + outputFile
    os.system(pemoco_path + args)


def prepare_reference_log(path):
    if os.path.isfile(path + os.sep + "log.txt"):
        os.rename(path + os.sep + "log.txt", path + os.sep + "log.log")
    original_log = open(path + os.sep + "log.log").readlines()
    new_log = []
    model, complexity = get_model(path)
    for i, line in enumerate(original_log):
        if ";" not in line:
            new_log.append(line)
        if "1;" == line[0:2]:
            new_log.append("1;" + model + ";0;0;0;0;0" + str(complexity) + "0;0;0;0\n")
    new_log.append("command: clean-sampling")
    file = open(path + os.sep + "log_true.log", "w")
    file.writelines(new_log)
    file.close()


def get_model(path):
    feat_solution = open(path + os.sep + "featSolution.txt").readlines()
    interaction_solution = open(path + os.sep + "interactionSolution.txt").readlines()
    model = ""
    for line in feat_solution:
        line = line.split(":")
        model = model + line[1].replace(" ", "").replace("\n", "") + " * " + line[0] + " + "
    for line in interaction_solution:
        line = line.split(":")
        model = model + line[1].replace(" ", "").replace("\n", "") + " * "
        interactions = line[0].split("#")
        for feature in interactions:
            model = model + feature + " * "
        model = model[:-2] + "+ "
    model = model[:-3]
    return model, len(model.split("+"))


def convert_measurements_to_csv(xml_path):
    csv_file = open(xml_path.replace(".xml", ".csv"),'w', newline='')
    fieldnames = ["Configuration", "Performance"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
    csv_writer.writeheader()
    root = ET.parse(xml_path).getroot()
    for row in root:
        configuration = ""
        nfp = ""
        for data in row:
            if data.attrib['columname'] == "Configuration":
                configuration = data.text
            else:
                nfp = float(data.text.replace("\n",""))
        configuration = configuration.replace(",", "%_%")
        csv_dict = dict()
        csv_dict["Configuration"] = configuration
        csv_dict["Performance"] = nfp
        csv_writer.writerow(csv_dict)
    csv_file.close()


if __name__ == '__main__':
    fm_path = "C:\\Users\\Jakob\\Documents\\BachelorThesis\\Experiments\\ExperimentsUtil\\BerkeleyCFeatureModel.xml"
    calc_all_pemoco("C:\\Users\\Jakob\\Documents\\ExperimentsConducted\\BaseIncrease", fm_path)
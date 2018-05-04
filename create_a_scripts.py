import os


def generate_a_scripts(base_path, out_path, feature_model_path, sampling):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for folder in os.listdir(base_path):
        if folder not in ['Scripts', 'ExperimentsUtil']:
            for sub_folder in os.listdir(base_path + os.sep + folder):
                relative_path = "../" + folder + "/" + sub_folder
                script_name = folder + "_" + sub_folder + ".a"
                write_a_file(relative_path, out_path, feature_model_path, script_name, sampling)


def write_a_file(relativePath, out_path, feature_model_path, script_name, sampling):
    lines = ["log " + relativePath + "/log.txt\n",
             "vm" + feature_model_path + "\n",
             "all " + relativePath + "/measurements.xml\n",
             "mlsettings learn_logFunction:true stopOnLongRound:false\n",
             "nfp Performance\n",
             sampling + "\n",
             "learn-splconqueror\n",
             "analyze-learning\n"
             "predict-configs-splconqueror\n",
             "measurementstocsv " + relativePath + "/SPLConquerorMeasurements.csv\n"]
    open(out_path + os.sep + script_name, "w").writelines(lines)

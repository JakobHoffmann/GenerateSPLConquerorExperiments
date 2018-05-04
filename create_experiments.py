import os
import json
thor_dist_path = "C:\\Users\\Jakob\\Documents\\BachelorThesisOtherRepos\\ThorFork\\thor-avm\\corpusData\\DistributionProfiles"
local_thor_dist_path = "C:\\Users\\Jakob\\Documents\\BachelorThesisOtherRepos\\ThorFork\\thor-avm\\corpusData\\DistributionProfiles"


# experiment = ("id_string", "fm path", "fv dist path/string", "iv dist path/string", "variant dist path", "i count", "i order", "f scale", "i scale")
def create_fv_scale_experiments(base_path, fv_distribution_list, scale_list):
    experiments = []
    for distribution in fv_distribution_list:
        for scale in scale_list:
            id = distribution[1] + "_" +distribution[0] + "_min" + str(scale[1]) + "max" + str(scale[2])
            fm_path = base_path + os.sep + "ExperimentsUtil" + os.sep + "BerkeleyCFeatureModel.xml"
            fv_dist = thor_dist_path + os.sep +"FeatureValues" + os.sep + distribution[0] + os.sep + distribution[1]
            iv_dist = thor_dist_path + os.sep +"InteractionValues" + os.sep + "BinarySize" + os.sep +"BDB_iv.txt"
            variant_dist = thor_dist_path + os.sep +"VariantValues" + os.sep + "Performance" + os.sep + "Email_allMeasurements.xml_variants.txt"
            i_count = "2"
            i_order = "1"
            f_scale = scale
            i_scale = [False]
            experiments.append((id, fm_path, fv_dist, iv_dist, variant_dist, i_count, i_order, f_scale, i_scale))
    return experiments


# experiment = ("id_string", "fm path", "fv dist path/string", "iv dist path/string", "variant dist path", "i count", "i order", "f scale", "i scale", "root offset")
def create_iv_scale_experiments(base_path, iv_distribution_list, scale_list):
    experiments = []
    for distribution in iv_distribution_list:
        for scale in scale_list:
            id = str(distribution[1]) + "_" + distribution[0] + "_min" + str(scale[1]) + "max" + str(scale[2])
            fm_path = base_path + os.sep + "ExperimentsUtil" + os.sep + "BerkeleyCFeatureModel.xml"
            fv_dist = "normal_distribution 25 10"
            iv_dist = thor_dist_path + os.sep +"InteractionValues" + os.sep + distribution[0] + os.sep + distribution[1]
            variant_dist = thor_dist_path + os.sep +"VariantValues" + os.sep + "Performance" + os.sep + "Email_allMeasurements.xml_variants.txt"
            i_count = "8"
            i_order = "1"
            f_scale = [False]
            i_scale = scale
            root_offset = scale[2]
            experiments.append((id, fm_path, fv_dist, iv_dist, variant_dist, i_count, i_order, f_scale, i_scale, root_offset))
    return experiments


def get_dist_list(type):
    path = local_thor_dist_path + "\\" + type
    dist_list = []
    for folder in os.listdir(path):
        for dist in os.listdir(path + "\\" + folder):
            if check_dist(path + "\\" + folder + "\\" + dist):
                dist_list.append((folder, dist))
    return dist_list


def check_dist(path):
    dist = open(path).read()
    dist = dist.replace("[", "").replace("]", "").split(",")
    if len(dist) > 9:
        return True
    else:
        print(path)
        return False


if __name__ == '__main__':
    base_path = "C:\\Users\\Jakob\\Documents\\Experiments\\FeatureScale"
    dist_list = get_dist_list("InteractionValues")
    scales = [(True, 0, 10), (True, 0, 50), (True, 0, 100), (True, 0, 500), (True, 0, 1000), (True, 0, 5000),
              (True, 0, 10000)]
    experiments = create_iv_scale_experiments(base_path,dist_list,scales)
    print(experiments[0])
    print(len(experiments))
    out_file = open("C:\\Users\\Jakob\\Documents\\InteractionScaleExperiments.txt", 'w')
    json.dump(experiments, out_file)
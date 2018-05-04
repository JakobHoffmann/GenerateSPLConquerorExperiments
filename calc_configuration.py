import os
import xml.etree.ElementTree as ET


def calc_all(base_path, configuration_path, has_interactions):
    for experiment_dir in os.listdir(base_path):
        if experiment_dir not in ['Scripts','ExperimentsUtil']:
            for experiment_nr in os.listdir(base_path + os.sep + experiment_dir):
                path = base_path + os.sep + experiment_dir + os.sep + experiment_nr + os.sep
                calc_all_nfp(path + "featSolution.txt", path + "interactionSolution.txt", configuration_path,
                             path + "measurements.xml", has_interactions)


def calc_all_nfp(feature_solution_path, interaction_solution_path, configuration_path, out_file, has_interactions):
    feature_map = get_feature_map(feature_solution_path)
    interaction_map = []
    if has_interactions:
        interaction_map = get_interaction_map(interaction_solution_path)
    configuration_file = open(configuration_path)
    tree = ET.ElementTree()
    root = ET.Element('results')
    tree._setroot(root)
    for configuration in configuration_file.readlines():
        nfp = calc_nfp(configuration, feature_map, interaction_map, has_interactions)
        configuration_text = configuration.replace('\n', '').replace(':', '')
        element = ET.Element('row')
        data_config = ET.Element('data',{'columname':'Configuration'})
        data_config.text = configuration_text
        data_nfp = ET.Element('data',{'columname':'Performance'})
        data_nfp.text = str(nfp)
        element.append(data_config)
        element.append(data_nfp)
        root.append(element)
    tree.write(out_file)


def calc_nfp(configuration, feature_map, interaction_map, has_interactions):
    features = configuration.replace(',:\n', '').split(',')
    nfp = 0
    for feature in features:
        nfp = nfp + feature_map[feature]
    if has_interactions:
        nfp = nfp + find_interactions(features, interaction_map)
    return nfp


# Calculates and returns the nfp value of all the interactions the given list of features fulfills.
def find_interactions(features, interaction_map):
    all_interaction_values = 0
    for feature in sorted(features):
        if feature in interaction_map:
            for interaction in interaction_map[feature]:
                interaction_fitting = True
                for participant in interaction[0]:
                    interaction_fitting = interaction_fitting and (participant in features)
                if interaction_fitting:
                    all_interaction_values = all_interaction_values + interaction[1]
    return all_interaction_values


def get_feature_map(feature_solution_path):
    feat_solution = open(feature_solution_path).readlines()
    feature_map = dict()
    for line in feat_solution:
        values = line.split(':')
        feature_map[values[0]] = float(values[1])
    return feature_map


# Stores the interactions in a data structure.
# All the features are sorted alphabetically.
# The first feature in the Alphabet is the Key for a List of all Interactions where that feature participates.
# For example:
# key = feature1
# value = [[['feature1', 'feature2'], 6.66], [['feature1', 'feature3', 'feature5'], 42.0]]
def get_interaction_map(interaction_solution_path):
    if interaction_solution_path is "":
        return ""
    interactions_solution = open(interaction_solution_path).readlines()
    interaction_map = dict()
    for line in interactions_solution:
        values = line.split(':')
        interaction_features = sorted(values[0].split('#'))
        values[0] = interaction_features
        values[1] = float(values[1])
        if interaction_features[0] in interaction_map:
            print("")
            interaction_map[interaction_features[0]].append(values)
        else:
            interaction_map[interaction_features[0]] = [values]
    return interaction_map


def write_xml(configurations, out_file):
    tree = ET.ElementTree()
    root = ET.Element('results')
    tree._setroot(root)
    for config in configurations:
        values = config.split(':')
        element = ET.Element('row')
        data_config = ET.Element('data',{'columname':'Configuration'})
        data_config.text = values[0]
        data_nfp = ET.Element('data',{'columname':'Performance'})
        data_nfp.text = values[1]
        element.append(data_config)
        element.append(data_nfp)
        root.append(element)
    tree.write(out_file)

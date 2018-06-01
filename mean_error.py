import csv


def analyze_error_result(result_path):
    nr_lines = len(open(result_path, 'r').readlines()) - 1
    csv_reader = csv.reader(open(result_path, 'r'), delimiter=';')
    next(csv_reader)
    mean_error = 0.0
    for row in csv_reader:
        # SPLConqueror appends to the result file.
        if row[1] == 'MeasuredValue':
            mean_error = 0.0
        else:
            exact_result = float(row[1])
            predicted_result = float(row[2])
            percent_error = abs(abs(exact_result - predicted_result) / exact_result)
            mean_error = mean_error + percent_error
    mean_error = mean_error / nr_lines
    return mean_error
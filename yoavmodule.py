import pandas as pd
import numpy as np

inp = ['data/train_data.csv', 'data/val_data.csv', 'data/test_data.csv']


def check_intercepted_data(list_of_files):
    """Checks if the training, validating and testing data files overlap each other.

        inp = list containing the names of the data files."""

    interception_results = 'Interception results:'
    num_of_overlaps = 0

    # for each file, reads the 'loc string' column values and inserts them into a numpy Array
    train_array = pd.read_csv(list_of_files[0])['loc_string'].to_numpy()
    val_array = pd.read_csv(list_of_files[1])['loc_string'].to_numpy()
    test_array = pd.read_csv(list_of_files[2])['loc_string'].to_numpy()

    # check if the arrays overlap each other
    if np.intersect1d(train_array, val_array).size > 0:
        interception_results += '\n train overlaps with val'
        num_of_overlaps += 1
    if np.intersect1d(train_array, test_array).size > 0:
        interception_results += '\n train overlaps with test'
        num_of_overlaps += 1
    if np.intersect1d(test_array, val_array).size > 0:
        interception_results += '\n test overlaps with val'
        num_of_overlaps += 1
    if num_of_overlaps == 0:
        interception_results += '\n There are no overlaps'

    print(interception_results)


def is_variation_length_ok(list_of_files):
    """Checks if all the genetic variation lengths of each data file equals 1

    inp = list containing the names of the data files."""

    # Read train, valid and test data
    train_data = pd.read_csv(list_of_files[0])
    val_data = pd.read_csv(list_of_files[1])
    test_data = pd.read_csv(list_of_files[2])

    # Concat all data files into a dataframe 'all_data'
    all_data = pd.concat([train_data, val_data, test_data])

    # Create an array out of 'start' and 'end' columns of 'all data' dataframe
    start_arr = all_data['start'].to_numpy()
    end_arr = all_data['end'].to_numpy()

    # Create an array of length of each genetic variation
    length_arr = end_arr-start_arr

    # Return True if all lengths are 1, Return False if one of the lengths is different from 1
    for len in length_arr:
        if len != 1:
            return False
    return True
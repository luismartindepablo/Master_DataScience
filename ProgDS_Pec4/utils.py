import re
import os
import pandas as pd


# Create folders
def create_folder(folder_name):
    """Creates a folder if it does not exists"""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


# Ejercicio 1
def count_patterns(pattern, file):
    """
    Given a file returns the number of lines where
    a certain pattern appears.

    :param pattern: pattern to search in regex
    :param file: file to read
    """
    count = 0
    with open(file, 'r') as f:
        for line in f:
            if re.search(pattern, line):
                count += 1
    print("The pattern '{}' appears {} times.".format(pattern, count))


# Ejercicio 2
def clean_dataset(dataset, pollsters, output_name):
    """
    Function to clean the datasets following
    the given instructions

    :param dataset: dataset to clean
    :param pollsters: xlsx file with pollsters inf
    :param output_name: name of the clean dataset

    :return: clean dataset
    """
    # No banned pollsters
    no_banned = pollsters[pollsters['Banned by 538'] == 'no'].Pollster
    # Interviews with no banned pollster
    dataset = dataset[dataset.pollster.isin(no_banned)]
    # Non tracked interviews
    dataset = dataset[dataset.tracking == False]
    # Reset index
    dataset = dataset.reset_index(drop=True)
    # Save clean data
    dataset.to_csv("./data/" + output_name, index=False)
    # Return clean data
    return dataset


# Ejercicio 3
def pattern_search(pattern, dataset, column):
    """
    Given a dataset with a string column ,
    filter rows containing a certain pattern.

    :param pattern: string to search
    :param dataset: dataset with a column to search
    :param column: column to search from

    :return: filtered dataset with matched rows
    """
    # Filter
    dataset = dataset[dataset[column].str.contains(pattern, regex=True)]
    # Reset index
    dataset = dataset.reset_index(drop=True)
    # Return
    return dataset

# Ejercicio 4
def grade_cleaning(dataset, pollsters):
    """
    Given a dataset with pollsters column and the pollsters grade in traditional
    format, it merges the columns and floors the grade.

    :param dataset: left side of the merge
    :param pollster: right side of the merge. Must have a column with the
                     pollsters and another with the grades.

    :return: merge dataset
    """
    # Merge grades
    dataset_grades = pd.merge(dataset, pollsters[["Pollster", "538 Grade", "Predictive    Plus-Minus"]],
                                    how='inner', left_on='pollster', right_on='Pollster')
    dataset_grades = dataset_grades.drop(['Pollster'], axis=1)
    # Transform grades
    dataset_grades["538 Grade"] = dataset_grades["538 Grade"].apply(lambda x: sorted(x)[-1])
    # Save dataset
    dataset_grades.to_csv("./data/concern_polls_grades.csv", index=False)
    # Return
    return dataset_grades

# Ejercicio 5
def grades_to_number(grade):
    """
    Given a grade in traditional format returns its numerical value.

    :param grade: grade in traditional format

    :return: grade in numerical format
    """
    # Conditions
    if grade == "A":
        return 1
    elif grade == "B":
        return 0.5
    elif grade == "C":
        return 0
    elif grade == "D":
        return -0.5
    else:
        return -1
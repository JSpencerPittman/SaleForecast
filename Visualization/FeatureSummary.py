EXPLANATION_FILE = "Visualization/Explanation.txt"

import pandas as pd

def explain_data(dataset):
    clear_explanation_file()
    with open(EXPLANATION_FILE, "a") as outputFile:
        # Size
        print("No. of Training Examples: ", dataset.shape[0], file=outputFile)
        print("No. of Features : ", dataset.shape[1], file=outputFile)
        # Features and corresponding types
        for feat, dtype in zip(dataset.columns, dataset.dtypes):
            print("Feature: ", feat, "\nType: ", dtype, file=outputFile)
            if pd.api.types.is_numeric_dtype(dtype) and dtype != bool:
                print("\tMean: ", dataset[feat].mean(), file=outputFile)
                print("\tStd: ", dataset[feat].std(), file=outputFile)
                print("\tMax: ", dataset[feat].max(), file=outputFile)
                print("\tMin: ", dataset[feat].min(), file=outputFile)
                print("\tMedian: ", dataset[feat].median(), file=outputFile)
                print("\t10%: ", dataset[feat].quantile(0.1), file=outputFile)
                print("\t25%: ", dataset[feat].quantile(0.25), file=outputFile)
                print("\t75%: ", dataset[feat].quantile(0.75), file=outputFile)
                print("\t90%: ", dataset[feat].quantile(0.9), file=outputFile)
        print('\n\n', file=outputFile)
        
def clear_explanation_file():
    with open(EXPLANATION_FILE, "w") as outputFile:
        print('', file=outputFile)
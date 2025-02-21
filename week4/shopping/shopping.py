import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    int_value = ["Administrative", "Informational", "ProductRelated", "OperatingSystems", "Browser", "Region", "TrafficType"]
    float_value = ["Administrative_Duration", "Informational_Duration", "ProductRelated_Duration", "BounceRates", "ExitRates", "PageValues", "SpecialDay"]
    evidence, labels = [], []
    
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tmp = {i:0 for i in row}
            for i in int_value:
                tmp[i] = int(row[i])
            for i in float_value:
                tmp[i] = float(row[i])
            tmp["Month"] = get_month_index(row["Month"])
            tmp["VisitorType"] = 1 if row["VisitorType"] == "Returning_Visitor" else 0
            tmp["Weekend"] = 1 if row["Weekend"] == "TRUE" else 0
            tmp["Revenue"] = 1 if row["Revenue"] == "TRUE" else 0
            
            tmp = list(tmp.values())
            labels.append(tmp[-1])
            evidence.append(tmp[:-1])
    return evidence, labels

def get_month_index(month_name: str) -> int:
    """
    Given a month name, return the corresponding index from 0 (January) to 11 (December).
    """
    try:
        return datetime.strptime(month_name, "%b").month - 1
    except ValueError:
        return datetime.strptime(month_name, "%B").month - 1


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neighbour = KNeighborsClassifier(n_neighbors=1)
    return neighbour.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = [0, 0]
    specificity = [0, 0]
    for actual, predict in zip(labels, predictions):
        if actual == 1:
            sensitivity[1] += 1
            if actual == predict:
                sensitivity[0] += 1
        else:
            specificity[1] += 1
            if actual == predict:
                specificity[0] += 1
    return [sensitivity[0]/sensitivity[1], specificity[0]/specificity[1]]


if __name__ == "__main__":
    main()

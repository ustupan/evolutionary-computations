import random
from sklearn import metrics

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler

def DecisionTreeParametersFeatures(numberFeatures, icls):
    genome = list()

    criterion = ["gini", "entropy"]
    genome.append(criterion[random.randint(0, 1)])

    splitter = ["best", "random"]
    genome.append(splitter[random.randint(0, 1)])

    max_depth = random.randint(1, 50)
    genome.append(max_depth)

    for i in range(0, numberFeatures):
        genome.append(random.randint(0, 1))
    return icls(genome)


def DecisionTreeClassifierFitness(y, df, numberOfAtributtes, individual):
    split = 5
    cv = StratifiedKFold(n_splits=split)

    listColumnsToDrop = []  # lista cech do usuniecia
    for i in range(numberOfAtributtes, len(individual)):
        if individual[i] == 0:  # gdy atrybut ma zero to usuwamy cechę
            listColumnsToDrop.append(i - numberOfAtributtes)
    dfSelectedFeatures = df.drop(df.columns[listColumnsToDrop], axis=1, inplace=False)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(dfSelectedFeatures)
    estimator = DecisionTreeClassifier(criterion=individual[0], splitter=individual[1], max_depth=individual[2])
    resultSum = 0
    for train, test in cv.split(df_norm, y):
        estimator.fit(df_norm[train], y[train])
        predicted = estimator.predict(df_norm[test])
        expected = y[test]
        tn, fp, fn, tp = metrics.confusion_matrix(expected, predicted).ravel()
        result = (tp + tn) / (tp + fp + tn + fn)
        resultSum = resultSum + result  # zbieramy wyniki z poszczególnych etapów walidacji krzyżowej
    return resultSum / split,


def mutationDecisionTree(individual):
    numberParamer = random.randint(0, len(individual) - 1)
    if numberParamer == 0:
        criterion = ["gini", "entropy"]
        individual[0] = criterion[random.randint(0, 1)]

    elif numberParamer == 1:
        splitter = ["best", "random"]
        individual[1] = splitter[random.randint(0, 1)]

    elif numberParamer == 2:
        max_depth = random.randint(1, 50)
        individual[2] = max_depth

    else:  # genetyczna selekcja cech
        if individual[numberParamer] == 0:
            individual[numberParamer] = 1
        else:
            individual[numberParamer] = 0

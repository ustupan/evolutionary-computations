import random

from sklearn import metrics

from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler

from sklearn.ensemble import RandomForestClassifier


def RandomForestParametersFeatures(numberFeatures, icls):
    genome = list()

    n_estimators = random.randint(5, 200)
    genome.append(n_estimators)

    criterion = ["gini", "entropy"]
    genome.append(criterion[random.randint(0, 1)])

    max_depth = random.randint(1, 32)
    genome.append(max_depth)

    min_samples_split = random.uniform(0.1, 1)
    genome.append(min_samples_split)

    min_samples_leaf = random.uniform(0, 0.5)
    genome.append(min_samples_leaf)

    for i in range(0, numberFeatures):
        genome.append(random.randint(0, 1))
    return icls(genome)


def RandomForestParametersFeatureFitness(y, df, numberOfAtributtes, individual):
    split = 5
    cv = StratifiedKFold(n_splits=split)

    listColumnsToDrop = []  # lista cech do usuniecia
    for i in range(numberOfAtributtes, len(individual)):
        if individual[i] == 0:  # gdy atrybut ma zero to usuwamy cechę
            listColumnsToDrop.append(i - numberOfAtributtes)
    dfSelectedFeatures = df.drop(df.columns[listColumnsToDrop], axis=1, inplace=False)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(dfSelectedFeatures)
    estimator = RandomForestClassifier(n_estimators=individual[0], criterion=individual[1], max_depth=individual[2],
                                       min_samples_split=individual[3], min_samples_leaf=individual[4])
    resultSum = 0
    for train, test in cv.split(df_norm, y):
        estimator.fit(df_norm[train], y[train])
        predicted = estimator.predict(df_norm[test])
        expected = y[test]
        tn, fp, fn, tp = metrics.confusion_matrix(expected, predicted).ravel()
        result = (tp + tn) / (tp + fp + tn + fn)
        resultSum = resultSum + result  # zbieramy wyniki z poszczególnych etapów walidacji krzyżowej
    return resultSum / split,


def mutationRandomForest(individual):
    numberParamer = random.randint(0, len(individual) - 1)

    if numberParamer == 0:
        n_estimators = random.randint(5, 200)
        individual[0] = n_estimators

    elif numberParamer == 1:
        criterion = ["gini", "entropy"]
        individual[1] = criterion[random.randint(0, 1)]

    elif numberParamer == 2:
        max_depth = random.randint(1, 32)
        individual[2] = max_depth

    elif numberParamer == 3:
        min_samples_split = random.uniform(0.1, 1)
        individual[3] = min_samples_split

    elif numberParamer == 4:
        min_samples_leaf = random.uniform(0, 0.5)
        individual[4] = min_samples_leaf

    else:  # genetyczna selekcja cech
        if individual[numberParamer] == 0:
            individual[numberParamer] = 1
        else:
            individual[numberParamer] = 0

import random
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.dummy import DummyClassifier


def DummyParametersFeatures(numberFeatures, icls):
    genome = list()

    strategy = ["stratified", "most_frequent", "prior", "uniform", "constant"]
    genome.append(strategy[random.randint(0, 4)])

    random_state = random.randint(0, 10)
    genome.append(random_state)

    constant = random.random()
    genome.append(constant)

    for i in range(0, numberFeatures):
        genome.append(random.randint(0, 1))
    return icls(genome)


def DummyClassifierFitness(y, df, numberOfAtributtes, individual):
    split = 5
    cv = StratifiedKFold(n_splits=split)

    listColumnsToDrop = []  # lista cech do usuniecia
    for i in range(numberOfAtributtes, len(individual)):
        if individual[i] == 0:  # gdy atrybut ma zero to usuwamy cechę
            listColumnsToDrop.append(i - numberOfAtributtes)
    dfSelectedFeatures = df.drop(df.columns[listColumnsToDrop], axis=1, inplace=False)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(dfSelectedFeatures)
    estimator = DummyClassifier(strategy=individual[0], random_state=individual[1], constant=individual[2])
    resultSum = 0
    for train, test in cv.split(df_norm, y):
        estimator.fit(df_norm[train], y[train])
        predicted = estimator.predict(df_norm[test])
        expected = y[test]
        tn, fp, fn, tp = metrics.confusion_matrix(expected, predicted).ravel()
        result = (tp + tn) / (tp + fp + tn + fn)
        resultSum = resultSum + result  # zbieramy wyniki z poszczególnych etapów walidacji krzyżowej
    return resultSum / split


def mutationDummy(individual):
    numberParamer = random.randint(0, len(individual) - 1)
    if numberParamer == 0:
        strategy = ["stratified", "most_frequent", "prior", "uniform", "constant"]
        individual[0] = strategy[random.randint(0, 4)]

    elif numberParamer == 1:
        random_state = random.randint(0, 10)
        individual[1] = random_state

    elif numberParamer == 2:
        constant = random.random()
        individual[2] = constant

    else:  # genetyczna selekcja cech
        if individual[numberParamer] == 0:
            individual[numberParamer] = 1
        else:
            individual[numberParamer] = 0

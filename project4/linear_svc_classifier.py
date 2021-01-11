import random
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import LinearSVC
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold


def LinearSVCParametersFeatures(numberFeatures, icls):
    genome = list()

    listLoss = ['hinge', 'squared_hinge']
    loss = listLoss[random.randint(0, 1)]
    genome.append(loss)

    for i in range(0, numberFeatures):
        genome.append(random.randint(0, 1))

    return icls(genome)


def LinearSVCParametersFeatureFitness(y, df, numberOfAtributtes, individual):
    split = 5
    cv = StratifiedKFold(n_splits=split)

    listColumnsToDrop = []  # lista cech do usuniecia
    for i in range(numberOfAtributtes, len(individual)):
        if individual[i] == 0:  # gdy atrybut ma zero to usuwamy cechę
            listColumnsToDrop.append(i - numberOfAtributtes)

    dfSelectedFeatures = df.drop(df.columns[listColumnsToDrop], axis=1, inplace=False)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(dfSelectedFeatures)
    estimator = LinearSVC(loss=individual[0], max_iter=6000, random_state=101)
    resultSum = 0
    for train, test in cv.split(df_norm, y):
        estimator.fit(df_norm[train], y[train])
        predicted = estimator.predict(df_norm[test])
        expected = y[test]
        tn, fp, fn, tp = metrics.confusion_matrix(expected, predicted).ravel()
        result = (tp + tn) / (tp + fp + tn + fn)
        resultSum = resultSum + result

    return resultSum / split,


def mutationLinearSVC(individual):
    numberParamer = random.randint(0, len(individual) - 1)
    if numberParamer == 0:
        # loss
        listLoss = ['hinge', 'squared_hinge']
        individual[0] = listLoss[random.randint(0, 1)]
    elif numberParamer == 1:
        if individual[numberParamer] == 0:
            individual[numberParamer] = 1
        else:
            individual[numberParamer] = 0

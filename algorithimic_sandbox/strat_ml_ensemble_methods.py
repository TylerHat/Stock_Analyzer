import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow

# import historical data

def ml_ensamble(data):
    train_data = data[:int(len(data)*0.8)]
    test_data = data[int(len(data)*0.8):]

    # create the features and labels for the training set
    features = train_data[["Open", "High", "Low", "Close"]]
    labels = train_data["Close"].shift(1)

    # create the deature and labels for the test set
    test_features = test_data[["Open", "High", "Low", "Close"]]
    test_labels = test_data["Close"].shift(1)

    # define the ensemble trading strat 
    class EnembleTradingStrat:

        def __init__(self, models):
            self.models= models
        
        def predict(self, features):
            predictions = []
            for model in self.models:
                prediction = model.predict(features)

                predictions.append(prediction)

            return np.mean(predictions, axis=0)
        
        def evaluate(self, predictions, labels):
            accuracy = np.mean(predictions == labels)

            return accuracy
        
        # create the models
    model1 = tensorflow.keras.models.load_model("model1.h5")

    model2 = tensorflow.keras.models.load_model("model2.h5")

    model3 = tensorflow.keras.models.load_model("model3.h5")

    # create the ensemble strat
    strategy = EnembleTradingStrat([model1, model2, model3])

    # evaluate the strat
    predictions =strategy.predict(test_features)
    accuracy = strategy.evaluate(predictions, test_labels)

    # plot the prediction and the actual
    plt.plot(labels, label = "Actual")
    plt.plot(predictions, label="Prediction")
    plt.legend()
    plt.show()
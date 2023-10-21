
from joblib import load
import numpy as np
from tensorflow import keras
import pkg_resources

class EnduranceModel():
    def __init__(self):
        scaler_path = pkg_resources.resource_filename('perf_end_Julespyvar', 'endurance/scaler_endurance.joblib')
        imputer_path = pkg_resources.resource_filename('perf_end_Julespyvar', 'endurance/imputer_endurance.joblib')
        weights_path = pkg_resources.resource_filename('perf_end_Julespyvar', 'endurance/model_weights_endurance.ckpt')
        
        scaler_endurance = load(scaler_path)
        imputer_endurance = load(imputer_path)

        
        model_endurance = keras.Sequential()
        inp = keras.layers.Input(shape=(11)) 
        model_endurance.add(inp)
        layer1 = keras.layers.Dense(26, activation='tanh')
        model_endurance.add(layer1)
        out = keras.layers.Dense(1)
        model_endurance.add(out)
        model_endurance.compile(loss=keras.losses.Huber, optimizer='adam')
        model_endurance.compile()
        model_endurance.load_weights(weights_path)
        
        self.scaler = scaler_endurance
        self.imputer = imputer_endurance
        self.prediction_model = model_endurance

        pass

    def predict(
        self,
        input_variables = np.array([  ### This should be an array with float values, order matters and missing values are accepted
            23.5, #Age (years)
            13.1, #Training years
            16.7, #Training hours/week
            np.nan, #Height (cm)
            74.6, #Weight (kg)
            66.8, #HR rest
            195.2, #peak HR
            25.4, #HR recovery (bpm)
            121.5, #HR reserve (bpm)
            np.nan, #SMM (kg)
            14.3 #PBF (%)
        ])
        ):
        input = np.array([input_variables])
        imputed_input = self.imputer.transform(input)
        scaled_inputs = self.scaler.transform(imputed_input)
        prediction = self.prediction_model.predict(scaled_inputs)
        return round(prediction[0][0], 1)

class PerformanceModel():
    def __init__(self):
        scaler_path = pkg_resources.resource_filename('perf_end_Julespyvar', 'performance/scaler_performance.joblib')
        imputer_path = pkg_resources.resource_filename('perf_end_Julespyvar', 'performance/imputer_performance.joblib')
        weights_path = pkg_resources.resource_filename('perf_end_Julespyvar', 'performance/model_weights_performance.ckpt')
        
        scaler_performance = load(scaler_path)
        imputer_performance = load(imputer_path)
        self.scaler = scaler_performance
        self.imputer = imputer_performance
        
        model_performance = keras.Sequential()
        inp = keras.layers.Input(shape=(11))
        model_performance.add(inp)
        layer1 = keras.layers.Dense(27, activation='tanh')
        model_performance.add(layer1)
        layer2 = keras.layers.Dense(23, activation='tanh')
        model_performance.add(layer2)
        out = keras.layers.Dense(1)
        model_performance.add(out)
        model_performance.compile(loss=keras.losses.Huber, optimizer='SGD')
        model_performance.compile()
        model_performance.load_weights(weights_path)
        self.prediction_model = model_performance

        pass
        
        
    def predict(
        self,
        input_variables = np.array([  ### This should be an array with float values, order matters and missing values are accepted
            23.5, #Age (years)
            13.1, #Training years
            16.7, #Training hours/week
            np.nan, #Height (cm)
            74.6, #Weight (kg)
            66.8, #HR rest
            195.2, #peak HR
            25.4, #HR recovery (bpm)
            121.5, #HR reserve (bpm)
            np.nan, #SMM (kg)
            14.3 #PBF (%)
        ])
        ):
        
        input = np.array([input_variables])
        imputed_input = self.imputer.transform(input)
        scaled_inputs = self.scaler.transform(imputed_input)
        prediction = self.prediction_model.predict(scaled_inputs)
        return round(prediction[0][0], 1)
        
        
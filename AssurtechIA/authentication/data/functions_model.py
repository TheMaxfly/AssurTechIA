import pandas as pd

class InsurancePredictor:
    def __init__(self, model):
        self.model = model

    def transform_bmi(self, X):
        bins = [0, 29.999, 100]
        labels = ['Normal weight', 'Obesity']
        X = X.copy()
        X["bmi_category"] = pd.cut(X['bmi'], bins=bins, labels=labels, right=False)
        return X

    def predict(self, data):
        # S'assurer que les colonnes sont dans le bon ordre
        required_columns = ['age', 'size', 'weight', 'number_children', 'is_smoker', 'region', 'genre', 'bmi']
        data = data[required_columns]
        
        
        data_transformed = self.transform_bmi(data)
        
        
        return self.model.predict(data_transformed)

    def bmi_calculation(weight, size):
        size_m = size / 100
        return round((weight / (size_m**2)), 2)

    def convert_to_english(genre, region, is_smoker):
    
        genre_mapping = {
        'homme': 'male',
        'femme': 'female'
        }
    
    
        region_mapping = {
        'sud-ouest': 'southwest',
        'nord-ouest': 'northwest',
        'sud-est': 'southeast',
        'nord-est': 'northeast'
        }
    
    
        smoker_mapping = {
        'oui': 'yes',
        'non': 'no'
        }
    
        return (
        genre_mapping.get(genre, genre),
        region_mapping.get(region, region),
        smoker_mapping.get(is_smoker, is_smoker)
        )
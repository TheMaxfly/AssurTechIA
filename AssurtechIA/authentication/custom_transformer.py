class DropFeatureSelector:
    def __init__(self, features_to_drop):
        self.features_to_drop = features_to_drop

    def transform(self, X):
        return X.drop(columns=self.features_to_drop)

    def fit(self, X, y=None):
        return self

import numpy as np
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score
import joblib

class AudioClassifier:
    def __init__(self, model_type='random_forest', scaler_type='standard'):
        """
        Initialize the audio classifier.

        Args:
            model_type: 'random_forest' or 'svm'
        """

        self.label_encoder = LabelEncoder()

        self.scaler_type = scaler_type
        if scaler_type == 'standard':
            self.scaler = StandardScaler()
        elif scaler_type == 'minmax':
            self.scaler = MinMaxScaler()
        elif scaler_type == 'robust':
            self.scaler = RobustScaler()
        else:
            raise ValueError("scaler must be 'standard', 'minmax', or 'robust'")

        self.model_type = model_type
        if model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'svm':
            self.model = SVC(kernel='rbf', random_state=42)
        else:
            raise ValueError("model_type must be 'random_forest' or 'svm'")

    def train(self, X, y, test_size=0.2):
        """
        Train the classifier.

        Args:
            X: Feature matrix
            y: Labels
            test_size: Proportion of data for testing

        Returns:
            Dictionary with training results
        """
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)

        # Split data
        X_train, _, y_train, _ = train_test_split(
            X, y_encoded, test_size=test_size, random_state=42, stratify=y_encoded
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)

        # Train model
        print(f"\nTraining {self.model_type} classifier with {self.scaler_type} scaler...")
        self.model.fit(X_train_scaled, y_train)

    def predict(self, features):
        """
        Predict category for a single audio file.

        Args:
            audio_path: Path to audio file

        Returns:
            Predicted category and probability
        """
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        prediction = self.model.predict(features_scaled)
        category = self.label_encoder.inverse_transform(prediction)[0]

        # Get probability if available
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(features_scaled)[0]
            confidence = np.max(proba)
        else:
            confidence = None

        return category, confidence

    def cross_validate_analysis(self, X, y, n_folds=10):
        """
        Perform 10-fold cross-validation and analyze performance.

        Args:
            X: Feature matrix
            y: Labels
            n_folds: Number of folds for cross-validation

        Returns:
            Dictionary with cross-validation results
        """
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)

        # Scale features first (we'll use pipeline-like approach in CV)
        X_scaled = self.scaler.fit_transform(X)

        cv = KFold(n_splits=n_folds, random_state=42, shuffle=True)

        metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
        scoring = {metric: metric for metric in metrics}
        cv_results = cross_validate(
            self.model,
            X_scaled,
            y_encoded,
            scoring = scoring,
            cv=cv,
            return_train_score=True)

        results = {}
        for metric in metrics:
            test_scores = cv_results[f'test_{metric}']
            train_scores = cv_results[f'train_{metric}']
            results[metric] = {
                'test_mean': np.mean(test_scores),
                'test_std': np.std(test_scores),
                'test_min': np.min(test_scores),
                'test_max': np.max(test_scores),
                'train_mean': np.mean(train_scores),
                'train_std': np.std(train_scores),
            }

            print(f"\n\n --- {metric.capitalize()} --- \n\n"
                  f"Test Mean: {results[metric]['test_mean']:.4f}    "
                  f"Test Std: {results[metric]['test_std']:.4f}    "
                  f"Test Min: {results[metric]['test_min']:.4f}    "
                  f"Test Max: {results[metric]['test_max']:.4f}")

        # Other reports
        y_pred = self.model.predict(X_scaled)

        accuracy = accuracy_score(y_encoded, y_pred)
        print(f"\n\n --- Accuracy score --- \n\n Accuracy: {accuracy:.4f}")
        print("\n\n --- Classification Report --- \n\n")
        print(classification_report(y_encoded, y_pred, target_names=self.label_encoder.classes_))

        print("\n\n --- Confusion Matrix --- \n\n")
        print(confusion_matrix(y_encoded, y_pred))

    def get_accuracy_score(self, X, y):
        """Calculate accuracy score."""
        X_scaled = self.scaler.fit_transform(X)
        y_encoded = self.label_encoder.fit_transform(y)
        y_pred = self.model.predict(X_scaled)
        return accuracy_score(y_encoded, y_pred)

    def save_model(self, filepath='audio_classifier.pkl'):
        """Save the trained model."""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'model_type': self.model_type
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath='audio_classifier.pkl'):
        """Load a trained model."""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoder = model_data['label_encoder']
        self.model_type = model_data['model_type']
        print(f"Model loaded from {filepath}")


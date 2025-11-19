import numpy as np
import matplotlib.pyplot as plt
from classifier import AudioClassifier
from data_loader import DataLoader
from dotenv import load_dotenv
import os

class Sample():

    def get_env_flag(self, var_name):
        return os.getenv(var_name, 'False') == 'True'

    def ablation_study(self):
        print("\n========= Ablation Study: Different Feature Sets =========")
        feature_sets = [
            {'model_type': 'random_forest', 'scaler_type': 'standard', 'mfcc_mean': True, 'mfcc_std': False, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'random_forest', 'scaler_type': 'standard', 'mfcc_mean': False, 'mfcc_std': True, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'random_forest', 'scaler_type': 'standard', 'mfcc_mean': False, 'mfcc_std': False, 'mel_mean': True, 'mel_std': False},
            {'model_type': 'random_forest', 'scaler_type': 'standard', 'mfcc_mean': False, 'mfcc_std': False, 'mel_mean': False, 'mel_std': True},
            {'model_type': 'random_forest', 'scaler_type': 'standard', 'mfcc_mean': True, 'mfcc_std': True, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'random_forest', 'scaler_type': 'standard', 'mfcc_mean': False, 'mfcc_std': True, 'mel_mean': False, 'mel_std': True},
            {'model_type': 'random_forest', 'scaler_type': 'standard', 'mfcc_mean': True, 'mfcc_std': True, 'mel_mean': False, 'mel_std': True},

            {'model_type': 'svm', 'scaler_type': 'standard', 'mfcc_mean': True, 'mfcc_std': False, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'svm', 'scaler_type': 'standard', 'mfcc_mean': False, 'mfcc_std': True, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'svm', 'scaler_type': 'standard', 'mfcc_mean': False, 'mfcc_std': False, 'mel_mean': True, 'mel_std': False},
            {'model_type': 'svm', 'scaler_type': 'standard', 'mfcc_mean': False, 'mfcc_std': False, 'mel_mean': False, 'mel_std': True},
            {'model_type': 'svm', 'scaler_type': 'standard', 'mfcc_mean': True, 'mfcc_std': True, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'svm', 'scaler_type': 'standard', 'mfcc_mean': False, 'mfcc_std': True, 'mel_mean': False, 'mel_std': True},
            {'model_type': 'svm', 'scaler_type': 'standard', 'mfcc_mean': True, 'mfcc_std': True, 'mel_mean': False, 'mel_std': True},

            {'model_type': 'random_forest', 'scaler_type': 'robust', 'mfcc_mean': True, 'mfcc_std': False, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'random_forest', 'scaler_type': 'robust', 'mfcc_mean': False, 'mfcc_std': True, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'random_forest', 'scaler_type': 'robust', 'mfcc_mean': False, 'mfcc_std': False, 'mel_mean': True, 'mel_std': False},
            {'model_type': 'random_forest', 'scaler_type': 'robust', 'mfcc_mean': False, 'mfcc_std': False, 'mel_mean': False, 'mel_std': True},
            {'model_type': 'random_forest', 'scaler_type': 'robust', 'mfcc_mean': True, 'mfcc_std': True, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'random_forest', 'scaler_type': 'robust', 'mfcc_mean': False, 'mfcc_std': True, 'mel_mean': False, 'mel_std': True},
            {'model_type': 'random_forest', 'scaler_type': 'robust', 'mfcc_mean': True, 'mfcc_std': True, 'mel_mean': False, 'mel_std': True},

            {'model_type': 'svm', 'scaler_type': 'robust', 'mfcc_mean': True, 'mfcc_std': False, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'svm', 'scaler_type': 'robust', 'mfcc_mean': False, 'mfcc_std': True, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'svm', 'scaler_type': 'robust', 'mfcc_mean': False, 'mfcc_std': False, 'mel_mean': True, 'mel_std': False},
            {'model_type': 'svm', 'scaler_type': 'robust', 'mfcc_mean': False, 'mfcc_std': False, 'mel_mean': False, 'mel_std': True},
            {'model_type': 'svm', 'scaler_type': 'robust', 'mfcc_mean': True, 'mfcc_std': True, 'mel_mean': False, 'mel_std': False},
            {'model_type': 'svm', 'scaler_type': 'robust', 'mfcc_mean': False, 'mfcc_std': True, 'mel_mean': False, 'mel_std': True},
            {'model_type': 'svm', 'scaler_type': 'robust', 'mfcc_mean': True, 'mfcc_std': True, 'mel_mean': False, 'mel_std': True},
        ]

        data = data_loader.load_wavs("data", classes, n_files=14)  # Load once to avoid repeated I/O
        for i, fs in enumerate(feature_sets):
            X, y = data_loader.extract_features_from_data(
                data,
                mfcc_mean=fs['mfcc_mean'],
                mfcc_std=fs['mfcc_std'],
                mel_mean=fs['mel_mean'],
                mel_std=fs['mel_std']
            )

            classifier = AudioClassifier(model_type=fs['model_type'], scaler_type=fs['scaler_type'])
            classifier.train(X, y, test_size=0.2)
            feature_sets[i]['accuracy'] = classifier.get_accuracy_score(X, y)

        print("\n\nAblation Study Results:")
        print("Feature Set\t\t\tAccuracy")

        categories = []
        accuracies = []
        for i, fs in enumerate(feature_sets):
            print(f"Set {i+1}: Model type={fs['model_type']},  MFCC Mean={fs['mfcc_mean']}, MFCC Std={fs['mfcc_std']}, Mel Mean={fs['mel_mean']}, Mel Std={fs['mel_std']}, Accuracy={fs['accuracy']:.4f}")
            category = f"{fs['model_type']}_{fs['scaler_type']}"
            if fs['mfcc_mean']:
                category += "_mfccMean"
            if fs['mfcc_std']:
                category += "_mfccStd"
            if fs['mel_mean']:
                category += "_melMean"
            if fs['mel_std']:
                category += "_melStd"

            categories.append(category)
            accuracies.append(fs['accuracy'])

        # Bar plot
        sorted_data = sorted(zip(accuracies, categories), reverse=True)
        sorted_values = [item[0] for item in sorted_data]
        sorted_categories = [item[1] for item in sorted_data]
        plt.figure(figsize=(12, 6))
        plt.barh(sorted_categories, sorted_values, color='skyblue')
        plt.xlabel('Accuracy')
        plt.title('Ablation Study: Impact of Different Feature Sets on Accuracy')
        plt.xlim(0, 1)
        plt.tight_layout()
        plt.show()

    def predict_on_test_files(self, data_loader, classifier):
        print("\n========= Evaluation on new audio files =========")
        test_audios = [
            "data/microwave/micro-long2.wav",
            "data/clothes/clothes-long.wav",
            "data/microwave/microwave-long.wav",
            "data/blender/wavs/blender20.wav",
            "data/dish-washer/wavs/washmac16.wav",
            "data/music/music-long2-sp010.wav"
        ]

        for test_audio in test_audios:
            y, sr = data_loader.load_wav_file(test_audio)
            features = data_loader.extract_features(y, sr)
            category, confidence = classifier.predict(features)
            print(f"\nPredicted: {category} for file {test_audio} (confidence: {confidence:.4f})")

if __name__ == "__main__":

    load_dotenv()
    sample = Sample()

    # Load data
    directory_path = "data/blender/wavs"
    data_loader = DataLoader()
    classes = ["blender", "clothes", "dish-washer", "microwave", "music"]

    print("Loading dataset...")
    X, y = data_loader.prepare_data("data", classes, 20) # Limit to 14 files per class because we only have 14 microwave samples

    print(f"\nDataset: {len(X)} samples, {X.shape[1]} features")
    print(f"Classes: {np.unique(y)}")

    # Initialize classifier
    classifier = AudioClassifier(model_type='random_forest', scaler_type='robust')

    # Train
    classifier.train(X, y, test_size=0.2)

    # Cross-validation analysis
    perform_cross_validation_analysis = sample.get_env_flag("perform_cross_validation_analysis")
    if perform_cross_validation_analysis:
        print("\n========= Cross-validation analysis =========")
        classifier.cross_validate_analysis(X, y, n_folds=10)

    # Save model
    save_model = sample.get_env_flag("save_model")
    if save_model:
        classifier.save_model('audio_classifier.pkl')

    # Evaluate on files not on training set
    preform_predict_on_test_files = sample.get_env_flag("perform_predict_on_test_files")
    if preform_predict_on_test_files:
        sample.predict_on_test_files(data_loader, classifier)

    # Ablation study: impact of different feature sets

    perform_ablation_study = sample.get_env_flag("perform_ablation_study")
    if perform_ablation_study:
        sample.ablation_study()

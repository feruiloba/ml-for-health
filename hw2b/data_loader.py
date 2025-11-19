import os
from pathlib import Path
import librosa
import librosa.feature
import numpy as np

class DataLoader:


    def extract_features_from_data(self, data, mfcc_mean=True, mfcc_std=True, mel_mean=True, mel_std=True):
        """
        Extract features and labels from loaded data.

        Args:
            data: List of tuples (y, sr, label)
            mfcc_mean: Whether to include MFCC mean features
            mfcc_std: Whether to include MFCC std features
            mel_mean: Whether to include Mel spectrogram mean features
            mel_std: Whether to include Mel spectrogram std features
        Returns:
            X: List of feature vectors
            y: List of labels
        """
        X = []
        y = []
        for _, (x, sr, category) in enumerate(data):
            features = self.extract_features(
                y=x,
                sr=sr,
                use_mfcc_mean=mfcc_mean,
                use_mfcc_std=mfcc_std,
                use_mel_mean=mel_mean,
                use_mel_std=mel_std)

            if features is not None:
                X.append(features)
                y.append(category)

        return X, y

    """
    Transform the raw audio waveform into features that are more informative for machine learning models.
    Features include:
    - Mel-Frequency Cepstral Coefficients (MFCCs): Represent the spectral envelope of the sound.
    - Mel Spectrograms: Visualize the frequency content over time, scaled to the Mel scale.
    """
    def extract_features(self, y, sr, n_mfcc=128, n_mels=128, use_mfcc_mean=True, use_mfcc_std=True, use_mel_mean=True, use_mel_std=True):
        """
        Extract MFCC and Mel spectrogram features from audio file.

        Args:
            y: Audio time series
            sr: Sampling rate of y
            n_mfcc: Number of MFCC coefficients
            n_mels: Number of Mel bands

        Returns:
            Feature vector
        """
        # Extract MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        mfccs_mean = np.mean(mfccs, axis=1)
        mfccs_std = np.std(mfccs, axis=1)

        # Extract Mel spectrogram
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        mel_mean = np.mean(mel_spec_db, axis=1)
        mel_std = np.std(mel_spec_db, axis=1)

        # Combine features
        features = []
        if use_mfcc_mean:
            features.append(mfccs_mean)
        if use_mfcc_std:
            features.append(mfccs_std)
        if use_mel_mean:
            features.append(mel_mean)
        if use_mel_std:
            features.append(mel_std)

        features = np.concatenate(features)

        return features

    def prepare_data(self, data_dir, categories, n_files=20, mfcc_mean=True, mfcc_std=True, mel_mean=True, mel_std=True):
        """
        Prepare training data from directory structure.

        Args:
            data_dir: Root directory containing category folders
            categories: List of category names (folder names)

        Returns:
            X (features), y (labels)
        """

        data = self.load_wavs(data_dir, categories, n_files=n_files)
        X, y = self.extract_features_from_data(data, mfcc_mean, mfcc_std, mel_mean, mel_std)

        return np.array(X), np.array(y)

    def load_wavs(self, data_dir, categories, n_files=20):
        """
        Get list of WAV file paths and their corresponding labels.

        Expected structure:
        data/
            category1/
                wavs/
                    audio1.wav
                    audio2.wav
            category2/
                wavs/
                    audio3.wav
                    audio4.wav

        Args:
            data_dir: Root directory containing category folders
            categories: List of category names (folder names)
            n_files: Number of files to load per category
        """

        data = []

        for category in categories:
            wavs_path = Path(data_dir) / category / "wavs"

            if not wavs_path.exists():
                print(f"Warning: {wavs_path} does not exist")
                continue

            audio_paths = os.listdir(wavs_path)
            print(f"Loading {n_files} files from {category}")


            for file_path in audio_paths[:n_files]:
                audio_path = wavs_path / file_path
                x, sr = self.load_wav_file(audio_path)
                data.append((x, sr, category))

        return data

    """
    Load and preprocess audio files for machine learning tasks.
    This includes loading WAV files, resampling to a consistent sample rate,
    normalizing amplitude, and trimming silence.
    """
    def load_wav_file(self, path):
        y, sr = librosa.load(path, sr=44100, duration=30)
        if sr != 16000:
            y = librosa.resample(y=y, orig_sr=sr, target_sr=16000)
            sr = 16000

        # Scale the audio amplitude to a consistent range (e.g., -1 to 1) to prevent bias towards louder signals.
        y = librosa.util.normalize(y)

        # Trim silence from the beginning and end of audio clips
        librosa.effects.trim(y, top_db=20)

        return y, sr
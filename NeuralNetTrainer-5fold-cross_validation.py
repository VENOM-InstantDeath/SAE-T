import soundfile # to read audio file
import numpy as np
import librosa # to extract speech features
import glob
import os
import pickle # to save model after training
from sklearn.model_selection import train_test_split # for splitting training and testing
from sklearn.model_selection import KFold  # for cross validation
from sklearn.neural_network import MLPClassifier # multi-layer perceptron model
from sklearn.metrics import accuracy_score, confusion_matrix # to measure how good we are

def extract_feature(file_name, **kwargs):
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            result = np.hstack((result, mel))
        if contrast:
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, contrast))
        if tonnetz:
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
            result = np.hstack((result, tonnetz))
    return result

# we allow only these emotions ( feel free to tune this on your need )
Emociones = [
    "Anger",
    "Sadness",
    "Disgust",
    "Fear",
    "Neutral",
    "Happiness"
]

def load_data():
    X, y = [], []
    print(len(glob.glob('data/*.wav')))
    #n = 0
    for file in glob.glob("data/*.wav"):
        #if n==200: break
        #n+=1
        # get the base name of the audio file
        basename = os.path.basename(file)
        # get the emotion label
        emotion = basename.split("_")[0]
        # we allow only AVAILABLE_EMOTIONS we set ==> We accept every emotion.
        #if emotion not in AVAILABLE_EMOTIONS:
        #    continue
        # extract speech features
        features = extract_feature(file, mfcc=True, chroma=True, mel=True)
        # add to data
        X.append(features)
        y.append(emotion)
    # split the data to training and testing and return it
    return np.array(X), np.array(y)

X, y = load_data()

print("[+] Number of training samples:", X.shape[0])
#print("[+] Number of testing samples:", X_test.shape[0])
print("[+] Number of features:", X.shape[1])

# best model, determined by a grid search
model_params = {
    'alpha': 0.01,
    'batch_size': 256,
    'epsilon': 1e-08, 
    'hidden_layer_sizes': (300,), 
    'learning_rate': 'adaptive', 
    'max_iter': 500, 
}
# initialize Multi Layer Perceptron classifier
# with best parameters
model = MLPClassifier(**model_params)
kf = KFold(n_splits=5, random_state=0, shuffle=True)
scores = []
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    print("[*] Training the model...")
    model.fit(X_train, y_train)
    
    # predict 25% of data to measure how good we are
    y_pred = model.predict(X_test)
    
    # calculate the accuracy
    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    
    print("Accuracy: {:.2f}%".format(accuracy*100))
    print(y_test)
    print(confusion_matrix(y_test,y_pred, labels=Emociones))
    scores.append(accuracy*100)

print(f"Overall Accuracy: {np.mean(scores):.2f}")
# now we save the model
# make result directory if doesn't exist yet
if not os.path.isdir("result"):
    os.mkdir("result")

pickle.dump(model, open("result/mlp_classifier.model", "wb"))

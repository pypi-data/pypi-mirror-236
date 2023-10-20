import pandas as pd
import numpy as np
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
df = pd.read_csv("/Users/wongdowling/Documents/Github/DQ_Dowling/new_ID/w_Ep/csv_data/electron1_data.csv")

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Plot a confusion matrix.
# cm is the confusion matrix, names are the names of the classes.
def plot_confusion_matrix(cm, names, title='Confusion matrix', 
                            cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(names))
    plt.xticks(tick_marks, names, rotation=45)
    plt.yticks(tick_marks, names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    

# Plot an ROC. pred - the predictions, y - the expected output.
def plot_roc(pred,y):
    fpr, tpr, _ = roc_curve(y, pred)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.6f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.show()

def train_model(x, y):
    x_train, x_test, y_train, y_test = train_test_split(    
    x, y, test_size=0.25, random_state=42)

    model = Sequential()
    model.add(Dense(100, input_dim=x.shape[1], activation='relu',
                    kernel_initializer='random_normal'))
    model.add(Dense(50,activation='relu',kernel_initializer='random_normal'))
    model.add(Dense(25,activation='relu',kernel_initializer='random_normal'))
    model.add(Dense(1,activation='sigmoid',kernel_initializer='random_normal'))
    model.compile(loss='binary_crossentropy', 
                optimizer=tensorflow.keras.optimizers.Adam(),
                metrics =['accuracy'])
    monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, 
        patience=60, verbose=1, mode='auto', restore_best_weights=True)

    model.fit(x_train,y_train,validation_data=(x_test,y_test),
            callbacks=[monitor],verbose=2,epochs=1000)
    return model

def save_model(model, fname):
    model.save(fname)

def load_model(mname):
    loaded_model = load_model(mname)
    return loaded_model


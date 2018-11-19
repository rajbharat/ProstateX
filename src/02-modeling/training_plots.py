"""
Author: F. Chollet
Created: 2018-11-19
Description: Simple plotting script adapted from Deep Learning with Python Book 
"""
import matplotlib.pyplot as plt

def plot_metrics(history, sequence_type):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(acc)+1)

    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title(sequence_type + ' training and validation accuracy')
    plt.xlabel('Epoch')
    plt.legend()

    plt.figure()

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title(sequence_type + ' training and validation loss')
    plt.xlabel('Epoch')
    plt.legend()

    plt.show()
    return
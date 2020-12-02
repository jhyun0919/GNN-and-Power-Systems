import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def data_scaler(data):
    scaler = MinMaxScaler()
    if data.ndim == 3:
        data = data.squeeze()
    scaler.fit(data)
    data = scaler.transform(data)

    return data, scaler


def split_dataset(dataset, train_ratio, test_ratio, shuffle=True):
    # set index
    train_len = int(len(dataset) * train_ratio)
    test_len = int(len(dataset) * test_ratio)

    # split dataset
    train_dataset = dataset[:train_len]
    val_dataset = dataset[train_len + 1 : -test_len]
    test_dataset = dataset[-test_len:]

    return train_dataset, val_dataset, test_dataset


def neighboring_func(u, o, Os):
    if u.ndim == 2:
        u = u.squeeze()
    if o.ndim == 2:
        o = o.squeeze()
    if Os.ndim == 3:
        Os = Os.squeeze()

    N = abs(np.corrcoef(u, Os)[0])
    m = abs(np.corrcoef(u, o)[0][1])

    counter = 0
    for n in N[1:]:
        if m <= n:
            counter += 1
    return counter


def N_o(x):
    return x


class FCN1(tf.keras.Model):
    def __init__(self, d_node_num):
        super(FCN1, self).__init__()
        self.N_o = N_o()
        self.neighbor = neighboring_func()
        self.flatten = tf.keras.layers.Flatten()
        self.dense = tf.keras.layers.Dense(d_node_num, activation="relu")

    def call(self, x):
        x = self.N_o(x)
        x = self.dense(x)

        x = self.dense(x)
        x = self.dense(x)

        return x


class FCN2(tf.keras.Model):
    def __init__(self, d_node_num):
        super(FCN2, self).__init__()
        self.N_o = N_o()
        self.neighbor = neighboring_func()
        self.flatten = tf.keras.layers.Flatten()
        self.dense = tf.keras.layers.Dense(d_node_num, activation="relu")

    def call(self, x):
        x = self.N_o(x)
        x = self.dense(x)

        x = self.dense(x)

        return x


class GCN1(tf.keras.Model):
    def __init__(self, ratio, d_node_num):
        super(GCN1, self).__init__()
        self.N_o = N_o()
        self.neighbor = neighboring_func()
        self.flatten = tf.keras.layers.Flatten()
        self.dense = tf.keras.layers.Dense(d_node_num, activation="relu")
        self.conv1 = tf.keras.layers.Conv1D(30, activation="relu")
        self.conv2 = tf.keras.layers.Conv1D(20, activation="relu")

    def call(self, x):
        x = self.N_o(x)
        x = self.self.dense(x)

        x = self.conv1(x)
        x = self.conv1(x)
        x = self.conv1(x)
        x = self.conv2(x)

        return x


class GCN2(tf.keras.Model):
    def __init__(self, ratio, d_node_num):
        super(GCN2, self).__init__()
        self.N_o = N_o()
        self.neighbor = neighboring_func()
        self.flatten = tf.keras.layers.Flatten()
        self.dense = tf.keras.layers.Dense(d_node_num, activation="relu")
        self.conv = tf.keras.layers.Conv1D(20, activation="relu")

    def call(self, x):
        x = self.N_o(x)
        x = self.self.dense(x)

        x = self.conv(x)
        x = self.conv(x)

        return x

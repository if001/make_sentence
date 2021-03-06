from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.optimizers import RMSprop
from keras import optimizers
from keras.models import Model
from keras import backend as K

from itertools import chain
import numpy as np
import random
import sys
import matplotlib.pyplot as plt


from lib.Const import Const
from lib.DataShaping import DataShaping
from lib.StringOperation import StringOperation
from nn.HRED import HRED


def make_sentens_vec(decoder_model, states_h, states_c, start_token, end_token):
    sentens_vec = []
    word_vec = start_token

    stop_condition = False
    while not stop_condition:
        word_vec = decoder_model.predict([word_vec, states_h, states_c])
        sentens_vec.append(word_vec.reshape(len(start_token[0][0])))
        if (np.allclose(word_vec, end_token) or len(sentens_vec) == 15):
            stop_condition = True
    return sentens_vec


def get_word_lists(file_path):
    print("make wordlists")
    lines = open(file_path).read().split("\n")
    wordlists = []
    for line in lines:
        wordlists.append(line.split(" "))
    print("wordlist num:", len(wordlists))
    return wordlists[:-1]


def save_model_fig(model, fname):
    import pydot
    from keras.utils import plot_model
    plot_model(model, to_file=fname)


def training():
    ds = DataShaping()
    hred = HRED()

    word_lists = get_word_lists(Const.seq2seq_train_file)

    if '--resume' in sys.argv:
        encoder_model = hred.load_models('param_seq2seq_encoder.hdf5')
        decoder_model = hred.load_models('param_seq2seq_decoder.hdf5')
        context_h = hred.load_models('param_seq2seq_h.hdf5')
        context_c = hred.load_models('param_seq2seq_c.hdf5')
    else:
        encoder_model = hred.build_encoder()
        decoder_model = hred.build_decoder()
        context_h = hred.build_context_model()
        context_c = hred.build_context_model()

        encoder_model = hred.model_compile(encoder_model)
        decoder_model = hred.model_compile(decoder_model)
        context_h = hred.model_compile(context_h)
        context_c = hred.model_compile(context_c)

    autoencoder = hred.build_autoencoder(
        encoder_model, decoder_model, context_h, context_c)
    autoencoder = hred.model_compile(autoencoder)

    meta_hh = np.array([[(random.randint(0, 10) / 10)
                         for i in range(hred.latent_dim)]])
    meta_hc = np.array([[(random.randint(0, 10) / 10)
                         for i in range(hred.latent_dim)]])
    meta_ch = np.array([[(random.randint(0, 10) / 10)
                         for i in range(hred.latent_dim)]])
    meta_cc = np.array([[(random.randint(0, 10) / 10)
                         for i in range(hred.latent_dim)]])

    for i in range(100000):
        train_data, teach_data, teach_target_data = ds.make_data_seq(
            word_lists, Const.batch_size, i)
        print("shape::", meta_cc.shape)
        hist = hred.train_autoencoder(
            autoencoder, train_data, teach_data, teach_target_data, meta_hh, meta_hc, meta_ch, meta_cc)

        state_h, state_c = encoder_model.predict(train_data)
        state_h = state_h.reshape(hred.batch_size, 1, hred.latent_dim)
        state_c = state_c.reshape(hred.batch_size, 1, hred.latent_dim)
        _, meta_hh, meta_hc = context_h.predict([state_h, meta_hh, meta_hc])
        _, meta_ch, meta_cc = context_c.predict([state_c, meta_ch, meta_cc])

        if i % 100 == 0:
            hred.save_models('param_seq2seq_encoder.hdf5', encoder_model)
            hred.save_models('param_seq2seq_decoder.hdf5', decoder_model)
            hred.save_models('param_seq2seq_h.hdf5', context_h)
            hred.save_models('param_seq2seq_c.hdf5', context_c)


def make_sentens():
    word_lists = get_word_lists(Const.seq2seq_train_file)

    ds = DataShaping()
    so = StringOperation()

    # load
    hred = HRED()
    encoder_model = hred.load_models('param_seq2seq_encoder.hdf5')
    decoder_model = hred.load_models('param_seq2seq_decoder.hdf5')
    context_h = hred.load_models('param_seq2seq_h.hdf5')
    context_c = hred.load_models('param_seq2seq_c.hdf5')

    autoencoder = hred.build_autoencoder(
        encoder_model, decoder_model, context_h, context_c)
    autoencoder = hred.model_compile(autoencoder)

    sentens1, sentens2 = ds.select_random_sentens(word_lists)

    sentens_vec_batch1 = []
    sentens_vec_batch1 = ds.train_data_shaping(sentens_vec_batch1, sentens1)
    sentens_vec_batch1 = np.array(sentens_vec_batch1)
    sentens_vec_batch2 = []
    sentens_vec_batch2 = ds.train_data_shaping(sentens_vec_batch2, sentens2)
    sentens_vec_batch2 = np.array(sentens_vec_batch2)

    # make meta state value
    meta_hh = np.array([[(random.randint(0, 10) / 10)
                         for i in range(hred.latent_dim)]])
    meta_hc = np.array([[(random.randint(0, 10) / 10)
                         for i in range(hred.latent_dim)]])
    meta_ch = np.array([[(random.randint(0, 10) / 10)
                         for i in range(hred.latent_dim)]])
    meta_cc = np.array([[(random.randint(0, 10) / 10)
                         for i in range(hred.latent_dim)]])

    state_h, state_c = encoder_model.predict(sentens_vec_batch1)
    state_h = state_h.reshape(hred.batch_size, 1, hred.latent_dim)
    state_c = state_c.reshape(hred.batch_size, 1, hred.latent_dim)

    # make state value
    _, meta_hh, meta_hc = context_h.predict([state_h, meta_hh, meta_hc])
    _, meta_ch, meta_cc = context_c.predict([state_c, meta_ch, meta_cc])
    print(sentens_vec_batch2.shape)
    state_h, state_c = encoder_model.predict(sentens_vec_batch2)

    state_h = state_h.reshape(hred.batch_size, 1, hred.latent_dim)
    state_h, _, _ = context_h.predict([state_h, meta_hh, meta_hc])
    state_h = np.array(state_h)

    state_c = state_c.reshape(hred.batch_size, 1, hred.latent_dim)
    state_c, _, _ = context_c.predict([state_c, meta_ch, meta_cc])
    state_c = np.array(state_c)

    # predict
    for _ in range(10):
        start_token = so.sentens_array_to_vec(["BOS"])
        start_token = np.array([start_token])
        end_token = so.sentens_array_to_vec(["。"])
        end_token = np.array([end_token])
        decode_sentens_vec = make_sentens_vec(
            decoder_model, state_h, state_c, start_token, end_token)
        decode_sentens_arr = so.sentens_vec_to_sentens_arr_prob(
            decode_sentens_vec)
        sentens = so.sentens_array_to_str(decode_sentens_arr)
        print(sentens)
        print("--")

        # cal state value
        decode_sentens_vec = np.array([decode_sentens_vec[::-1]])
        state_h, state_c = encoder_model.predict(decode_sentens_vec)
        state_h = np.array(state_h)
        state_c = np.array(state_c)


def main():
    if '--training' in sys.argv:
        training()
    elif '--predict' in sys.argv:
        make_sentens()
    else:
        print("invalid arg!!")


if __name__ == "__main__":
    main()

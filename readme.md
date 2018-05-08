## run
training

```
python3 make_sentens.py -train
```


resume training

```
python3 make_sentens.py --train --resume
```


## architecher

### encoder

```
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
input_1 (InputLayer)         (None, None, 128)         0
_________________________________________________________________
dense_1 (Dense)              (None, None, 128)         16512
_________________________________________________________________
bidirectional_1 (Bidirection (None, None, 512)         788480
_________________________________________________________________
lstm_2 (LSTM)                [(None, 256), (None, 256) 787456
=================================================================
Total params: 1,592,448
Trainable params: 1,592,448
Non-trainable params: 0
_________________________________________________________________
```


### decoder

```
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to
==================================================================================================
input_4 (InputLayer)            (None, None, 128)    0
__________________________________________________________________________________________________
dense_2 (Dense)                 (None, None, 128)    16512       input_4[0][0]
__________________________________________________________________________________________________
bidirectional_2 (Bidirectional) (None, None, 512)    788480      dense_2[0][0]
__________________________________________________________________________________________________
input_2 (InputLayer)            (None, 256)          0
__________________________________________________________________________________________________
input_3 (InputLayer)            (None, 256)          0
__________________________________________________________________________________________________
lstm_4 (LSTM)                   [(None, None, 256),  787456      bidirectional_2[0][0]
                                                                 input_2[0][0]
                                                                 input_3[0][0]
__________________________________________________________________________________________________
dense_3 (Dense)                 (None, None, 128)    32896       lstm_4[0][0]
__________________________________________________________________________________________________
dropout_1 (Dropout)             (None, None, 128)    0           dense_3[0][0]
__________________________________________________________________________________________________
dense_4 (Dense)                 (None, None, 128)    16512       dropout_1[0][0]
==================================================================================================
Total params: 1,641,856
Trainable params: 1,641,856
Non-trainable params: 0
__________________________________________________________________________________________________
```

### context model  (hidden state h in LSTM)

```
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to
==================================================================================================
input_5 (InputLayer)            (None, None, 256)    0
__________________________________________________________________________________________________
input_6 (InputLayer)            (None, 256)          0
__________________________________________________________________________________________________
input_7 (InputLayer)            (None, 256)          0
__________________________________________________________________________________________________
lstm_5 (LSTM)                   [(None, 256), (None, 525312      input_5[0][0]
                                                                 input_6[0][0]
                                                                 input_7[0][0]
==================================================================================================
Total params: 525,312
Trainable params: 525,312
Non-trainable params: 0
__________________________________________________________________________________________________
```

### context model (hidden state c in LSTM)

```
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to
==================================================================================================
input_8 (InputLayer)            (None, None, 256)    0
__________________________________________________________________________________________________
input_9 (InputLayer)            (None, 256)          0
__________________________________________________________________________________________________
input_10 (InputLayer)           (None, 256)          0
__________________________________________________________________________________________________
lstm_6 (LSTM)                   [(None, 256), (None, 525312      input_8[0][0]
                                                                 input_9[0][0]
                                                                 input_10[0][0]
==================================================================================================
Total params: 525,312
Trainable params: 525,312
Non-trainable params: 0
__________________________________________________________________________________________________
```


### autoencoder

```
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to
==================================================================================================
input_11 (InputLayer)           (None, None, 128)    0
__________________________________________________________________________________________________
dense_1 (Dense)                 (None, None, 128)    16512       input_11[0][0]
__________________________________________________________________________________________________
bidirectional_1 (Bidirectional) (None, None, 512)    788480      dense_1[1][0]
__________________________________________________________________________________________________
input_16 (InputLayer)           (None, None, 128)    0
__________________________________________________________________________________________________
lstm_2 (LSTM)                   [(None, 256), (None, 787456      bidirectional_1[1][0]
__________________________________________________________________________________________________
dense_2 (Dense)                 (None, None, 128)    16512       input_16[0][0]
__________________________________________________________________________________________________
reshape_1 (Reshape)             (None, 1, 256)       0           lstm_2[1][1]
__________________________________________________________________________________________________
input_12 (InputLayer)           (None, 256)          0
__________________________________________________________________________________________________
input_13 (InputLayer)           (None, 256)          0
__________________________________________________________________________________________________
reshape_2 (Reshape)             (None, 1, 256)       0           lstm_2[1][2]
__________________________________________________________________________________________________
input_14 (InputLayer)           (None, 256)          0
__________________________________________________________________________________________________
input_15 (InputLayer)           (None, 256)          0
__________________________________________________________________________________________________
bidirectional_2 (Bidirectional) (None, None, 512)    788480      dense_2[1][0]
__________________________________________________________________________________________________
lstm_5 (LSTM)                   [(None, 256), (None, 525312      reshape_1[0][0]
                                                                 input_12[0][0]
                                                                 input_13[0][0]
__________________________________________________________________________________________________
lstm_6 (LSTM)                   [(None, 256), (None, 525312      reshape_2[0][0]
                                                                 input_14[0][0]
                                                                 input_15[0][0]
__________________________________________________________________________________________________
lstm_4 (LSTM)                   [(None, None, 256),  787456      bidirectional_2[1][0]
                                                                 lstm_5[1][0]
                                                                 lstm_6[1][0]
__________________________________________________________________________________________________
dense_3 (Dense)                 (None, None, 128)    32896       lstm_4[1][0]
__________________________________________________________________________________________________
dropout_1 (Dropout)             (None, None, 128)    0           dense_3[1][0]
__________________________________________________________________________________________________
dense_4 (Dense)                 (None, None, 128)    16512       dropout_1[1][0]
==================================================================================================
Total params: 4,284,928
Trainable params: 4,284,928
Non-trainable params: 0
__________________________________________________________________________________________________
```



## error
Bug of Keras(2.1.1)??
Layer lstm_4 was passed non-serializable keyword arguments: {'initial_state': [<tf.Tensor 'input_2:0' shape=(?, 256) dtype=float32>, <tf.Tensor 'input_3:0' shape=(?, 256) dtype=float32>]}. They will not be included in the serialized model (and thus will be missing at deserialization time).

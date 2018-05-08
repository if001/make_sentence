
from lib.WordVec import MyWord2Vec
from lib.Const import Const

fname = Const.word2vec_train_file

#w2v = MyWord2Vec.train(fname, "save")
model = MyWord2Vec.load_model()

print("corpus: ", model.corpus_count)
voc = model.wv.vocab.keys()
print("vocab: ", len(voc))
print(voc)

# vec = MyWord2Vec.str_to_vector(model, "引か")
# print(vec)
# import pylab as plt
# plt.plot(vec)
# plt.show()

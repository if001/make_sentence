"""
定数用
"""

#import pylab as plt
# import lib
from . import SetProject


class Const():
    """ valiable setting"""
    word_feat_len = 128
    batch_size = 1

    """ directory setting"""
    project_dir = SetProject.get_path()

    """ word2vec """
    word2vec_train_file = project_dir + "/aozora_text/files/files_all_rnp.txt"
    word2vec_wait = project_dir + '/lib/model/text8.model'

    """ seq2seq """
    seq2seq_wait_save_dir = project_dir + '/nn/weight/'
    seq2seq_train_file = project_dir + "/aozora_text/files/files_all_rnp.txt"
    # seq2seq_train_file = project_dir+"/aozora_text/files/tmp.txt"

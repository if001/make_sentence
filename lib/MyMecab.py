# -*- coding: utf-8 -*-

import sys
import MeCab
import re

#文字列を受け取って、単語ごとに切ったリストを返す
def get_words(wordline):
   m = MeCab.Tagger("-Owakati")
   m.parse('')
   words = m.parse(wordline)
   words_list = []

   tmp=""
   for value in words:
      tmp += value
      if value == " ":
         words_list.append(tmp[:-1])
         tmp = ""

   return words_list

if __name__ == '__main__':
   text = u's今日は良い天気ですね。e'
   # get_words(text)
   print(get_words(text))

   word_list = get_words_to_katakana(text)
   print(word_list)
   hira_word_list = kata_to_hira(word_list)
   print(hira_word_list)

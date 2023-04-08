import csv
import os

current_path = os.getcwd()

stop_words_file = open(current_path + "/data" + "/stop-words.txt", "r")
stop_words = stop_words_file.readlines()

for i in range(len(stop_words) - 1):
  stop_words[i] = stop_words[i].strip()


def tokenize(one_line: str, word_and_freq: list, word_list: list):
  special_chars = " !#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

  # replace all special characters with '*'
  for sc in special_chars:
    one_line = one_line.replace(sc, '*')

  # Separate words by '*'
  for word in one_line.split('*'):
    trimed_word = word.replace('\n', '').replace('\"', '')

    if trimed_word not in stop_words and trimed_word in word_list:
      for waf in word_and_freq:
        if waf[0] == trimed_word:
          waf[1] += 1

    elif trimed_word not in stop_words and trimed_word not in word_list:
      word_list.append(trimed_word)
      word_and_freq.append([trimed_word, 1])


f = open(current_path + "/data" + "/train.csv", "r", encoding="utf-8")
rdr = csv.reader(f)

lines = []
for r in rdr:
  lines.append(r[1].lower())

word_and_freq = []
word_list = []

for l in lines:
  tokenize(l, word_and_freq, word_list)

word_and_freq.sort(key=lambda x: x[1], reverse=True)

print("These are the 50 words that appeared the most in sentences")
print("The content in parentheses is the number of times the word appeared")
for i in range(1, 51):
  print(str(i) + ". " + word_and_freq[i][0] +
        " (" + str(word_and_freq[i][1]) + ")")
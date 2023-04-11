import csv
import os

current_path = os.getcwd()

stop_words_file = open(current_path + "/data" + "/stop-words.txt", "r")
stop_words = stop_words_file.readlines()

for i in range(len(stop_words) - 1):
  stop_words[i] = stop_words[i].strip()


def tokenize(one_line: str, word_and_freq: dict, word_list: list):
  """
  function that splits sentences into words and updates the number of appearances of each word
  """
  special_chars = " !#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

  # make all characters to lowercase
  one_line = one_line.lower()

  # replace all special characters with '*'
  for sc in special_chars:
    one_line = one_line.replace(sc, '*')

  # Separate words by '*'
  tokend_line = one_line.split('*')
  for word in tokend_line:
    trimed_word = word.replace('\n', '').replace('\"', '')

    # Adjusts the number of appearances of words
    # if a word is in stop words, ignore it
    if trimed_word not in stop_words and trimed_word in word_list:
      for waf in word_and_freq:
        if waf[0] == trimed_word:
          waf[1] += 1
    elif trimed_word not in stop_words and trimed_word not in word_list:
      word_list.append(trimed_word)
      word_and_freq.append([trimed_word, 1])

  return tokend_line


def tokenize_line(one_line):
  special_chars = " !#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

  # make all characters to lowercase
  one_line = one_line.lower()

  # replace all special characters with '*'
  for sc in special_chars:
    one_line = one_line.replace(sc, '*')

  # Separate words by '*'
  return one_line.split('*')


def get_five_star_rate(reader):
  """
  function to get the rate of five star reviews - value of P(5-star review)
  """
  five_star = 0
  total_review_count = 0

  for r in reader:
    if r[0] == '5':
      five_star += 1
    total_review_count += 1

  return five_star / total_review_count


def get_list_of_five_star_rate_each_word(final_features: list, processed_reviews: list, total_five_star_rate: float):
  '''
  make list of [word, P(word | 5-star review)]
  P(word | 5-star review) = P(word, 5-star review) / P(5-star review)
  P(word, 5-star review) = num of 5 star review that contains "word" / total review
  '''
  rate_list = []  # list of [word, P(word | 5-star review)]
  whole_review_size = len(processed_reviews)

  five_word_count = 0  # number of 5-star reviews that a particular word appears
  for word in final_features:
    for review in processed_reviews:
      # 5-star review and contains the word
      if review[0] == '5' and word in review[1]:
        five_word_count += 1

    # P(word, 5-star review)
    word_and_five_star_rate = five_word_count / whole_review_size

    # laplace smoothing
    if word_and_five_star_rate == 0:
      word_and_five_star_rate = (five_word_count + 1) / \
          (whole_review_size + 1000)

    rate_list.append([word, word_and_five_star_rate / total_five_star_rate])
    five_word_count = 0  # reset word count

  return rate_list


def predict(review, final_features, rate_list):
  '''
  predict if the review is positive review or negative review
  '''
  review_body = review[1]

  predicted_five_star_rate = 1

  for word in review_body:
    if word in final_features:
      for rl in rate_list:
        if rl[0] == word:
          predicted_five_star_rate *= rl[1]

  if predicted_five_star_rate >= 0.5:
    return True
  else:
    return False


# get csv files
train_file = open(current_path + "/data" + "/train.csv", "r", encoding="utf-8")
test_file = open(current_path + "/data" + "/test.csv", "r", encoding="utf-8")

# list to calculate freq of words
word_and_freq_train = []
word_list_train = []

# get csv file to obj
train_reader = csv.reader(train_file)
test_reader = csv.reader(test_file)

# get only review from csv
lines_train = []
for tr in train_reader:
  lines_train.append([tr[0], tr[1].lower()])

# extract feature
for i in range(0, len(lines_train) - 1):
  lines_train[i][1] = tokenize(
      lines_train[i][1], word_and_freq_train, word_list_train)

# get top 1000 words
word_and_freq_train.sort(key=lambda x: x[1], reverse=True)
final_features = word_and_freq_train[1:1001]

print("Model training complete.")

# rate of five star reviews
five_star_rate = get_five_star_rate(lines_train)

# list of [word, P(word | 5-star_review)]
# P(word | 5-star_review) = P(word, 5-star_review) / P(5-star_review)
good_review_rate_each_word = get_list_of_five_star_rate_each_word(
    final_features, lines_train, five_star_rate)

test_reviews = []
for tr in test_reader:
  test_reviews.append([tr[0], tr[1].lower()])

for i in range(len(test_reviews) - 1):
  test_reviews[i][1] = tokenize_line(test_reviews[i][1])

# predict review of test.csv and evaluate
answer = []

for review in test_reviews:
  predicted = predict(review, final_features, good_review_rate_each_word)

  if predicted is True:
    if review[0] == '5':
      answer.append(True)
    else:
      answer.append(False)
  elif predicted is False:
    if review[0] == '5':
      answer.append(False)
    else:
      answer.append(True)

# calculate accuracy
accurated_count = 0
for a in answer:
  if a == True:
    accurated_count += 1

accuracy = accurated_count / len(answer)

# print accuracy
print("Accuracy: " + str(accuracy * 100) + "%")

# close files
train_file.close()
test_file.close()
stop_words_file.close()

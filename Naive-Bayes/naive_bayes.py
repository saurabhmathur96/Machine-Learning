#!/usr/bin/env python

'''
P(class_j|a_1, a_2, .. , a_n) = P(a_1, a_2, .. , a_n|class_j) * P(class_j) / ( P(a_1, a_2, .. , a_n) )

    assumption -> all prob. of each word is independant wrt class_j
    p(a_1, a_2, .. , a_n | class_j) = product( P(a_i|class_j) )

=> P(class_j)* product( P(a_i | v_j) )

'''
INPUT_FILE = 'SMSSpamCollection'
import re
from collections import Counter
import csv
import sys
import math

def get_words(text):
  '''
  returns a list of words (case-insensitive) in given string
  '''
  return re.compile('\w+').findall(text)
  
def product(ls):
  '''
  return the product of a list
  '''
  return reduce(lambda x,y: x*y, ls)


def train(data):
   spam_count = Counter(data['spam'])
   ham_count = Counter(data['ham'])
   spam_len = len(data['spam'])
   ham_len = len(data['ham'])
   p_spam = float(spam_len)/(spam_len + ham_len)
   p_ham = 1-p_spam
   
   spam_probs = {word: float(spam_count[word])/sum(spam_count.values()) for word in data['spam']}
   ham_probs = {word: float(ham_count[word])/sum(ham_count.values()) for word in data['ham']}
   
   model = {'spam_probs': spam_probs, 'ham_probs': ham_probs, 'spam_count': spam_count, 'ham_count':ham_count, 'p_spam':p_spam, 'p_ham': p_ham}
   
   return model




def predict(line, model):
    words = get_words(line)
    
    
    score = {'spam': 0, 'ham':0}
    
    for word in words:
       p_word_spam = model['spam_probs'].get(word, 1e-5)
       p_word_ham = model['ham_probs'].get(word, 1e-5)
       score['spam'] += math.log(model['p_spam']) + math.log(p_word_spam)
       score['ham'] += math.log(model['p_ham']) + math.log(p_word_ham)
       
       
    if (score['spam'] > score['ham'] ):
       return 'spam'
    else:
       return 'ham'
       

def load_dataset(file_name):
    words = {'spam': [], 'ham': []}
    #load data
    with open(file_name) as f:
       reader = csv.reader(f, delimiter='\t')
       
       for line in reader:
          if line[0] == 'spam':
             words['spam'] += get_words(line[1].lower())
          elif line[0] == 'ham':
             words['ham'] += get_words(line[1].lower())
          else:
             print 'error parsing line : ' + line
    length = min(len(words['spam']), len(words['ham']))
    #print length
    #print len(words['ham'])
    words['ham'] = words['ham'][:length]
    words['spam'] = words['spam'][:length]
    return words

def main():
   dataset = load_dataset(INPUT_FILE)
   model = train(dataset)
   line = raw_input()
   print predict(line, model)
      
if __name__ == '__main__':
   main()

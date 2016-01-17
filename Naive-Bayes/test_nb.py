#!/usr/bin/env python
INPUT_FILE = 'SMSSpamCollection'
TEST_FILE = 'TestCollection'
import csv
import naive_bayes

dataset = naive_bayes.load_dataset(INPUT_FILE)
model = naive_bayes.train(dataset)
total = {'spam': 0, 'ham': 0}
correct = {'spam': 0, 'ham': 0}
with open(TEST_FILE) as f:
   reader = csv.reader(f, delimiter='\t')
   for line in reader:
      result = line[0]
      #print result,
      #print ': '
      prediction = naive_bayes.predict(line[1], model)
      if(result == 'ham'):
         if prediction == result :
            correct['ham'] += 1
         total['ham'] += 1
      else:
         if prediction == result :
            correct['spam'] += 1
         
         total['spam'] += 1
      

print 'ham accuracy: {}%'.format( float(correct['ham'])*100/total['ham'] )
print 'spam accuracy: {}%'.format(float(correct['spam'])*100/total['spam'] )

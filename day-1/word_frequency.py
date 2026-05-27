# This file contains code to count the frequency of each word in a given sentence and print the results in a sorted manner.
# The word_frequency function takes a sentence as input, converts it to lowercase, splits it into words, and counts the frequency of each word while removing punctuation.
# The results are printed in descending order of frequency. 
# Additionally, the word_frequency_counter function uses the Counter class from the collections module to achieve the same result more efficiently.

sentence = "Python is a great programming language. I love learning Python because it's so versatile and powerful. Python's simplicity and readability make it a joy to work with." 

def word_frequency(sentence):
    words = sentence.lower().split()
    frequency = {}
    for word in words:
        word = word.strip(".,!?;:")  # Remove punctuation
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

freq = word_frequency(sentence)
for word, count in sorted(freq.items(), key=lambda item: item[1], reverse=True):
    print(f"'{word}': {count}")

from collections import Counter
def word_frequency_counter(sentence):
    words = sentence.lower().split()
    words = [word.strip(".,!?;:") for word in words]  # Remove punctuation
    return Counter(words)

freq_counter = word_frequency_counter(sentence)
for word, count in freq_counter.most_common():
    print(f"'{word}': {count}")
# Simple hangman solver, guesses letters in order of frequency
import re
import sys
import logging
print('noora')

MAX_MISSES = 8


words = []

word = input().strip()
while word:
    #word = word.encode('latin-1').decode('utf-8')
    words.append(word)
    word = input().strip()

original_words = words

try:
    status = input()
    #status = status.encode('latin-1').decode('utf-8')
    while status:
        index = 0
        words = original_words
        guesses_left = MAX_MISSES

        # filter words with correct lenght
        words = [word for word in words if len(word) == len(status)]
        guessed_letters = []
        letters = {letter for word in words for letter in word}
        frequencies = [(letter, sum(word.count(letter) for word in words),  len([word for word in words if letter in word])) for letter in letters]
        guess_order = sorted(frequencies, key=lambda a: (a[1], -a[1]), reverse=True)
        #frequencies = [(letter, len([word for word in words if letter in word])) for letter in letters]
        guess_order = sorted(frequencies, key=lambda a: a[1], reverse=True)
        while True:
            word_count = len(words)

            # if three or less words left, guess that
            if len(words) <= 3 and len(words) <= guesses_left:
                print(words[0])
            # else guess next letter
            else:
                letter = guess_order[index][0]
                index += 1
                print(letter)
                guessed_letters.append(letter)

            result = input()
            #result = result.encode('latin-1').decode('utf-8')
            status = input()
            #status = status.encode('latin-1').decode('utf-8')

            # when winning or losing and starting a new game prints three lines
            if status.startswith('WIN') or status.startswith('LOSE') or not status:
                status = input()
                #status = status.encode('latin-1').decode('utf-8')
                break

            # if hit, filter words with correct regex
            if result.startswith('HIT'):
                remaining_letters = '[' + ''.join(list(filter(lambda l: l != letter, letters))) + ']'
                regex = remaining_letters + '{'
                n = 0
                for c in status:
                    if c == '.':
                        n+=1
                    else:
                        regex += (str(n) + '}' + c + remaining_letters + '{')
                        n = 0
                if regex.endswith('{'):
                    regex += '0}'
                r = re.compile(regex)

                # filter words and count new frequencies
                words = list(filter(r.match, words))

            # if missed, filter words with incorrect letters
            if result.startswith('MISS'):
                if len(words) <= 3 and len(words) <= guesses_left:
                    del words[0]
                else:
                    guesses_left -= 1
                    words = list(filter(lambda w: letter not in w, words))

            # ignore letters that have already been guessed
            letters = {letter for word in words for letter in word if letter not in guessed_letters}
            # count new frequencies if the number of words has changed
            if len(words) < word_count:
                frequencies = [(letter, sum(word.count(letter) for word in words),  len([word for word in words if letter in word])) for letter in letters]
                guess_order = sorted(frequencies, key=lambda a: (a[1], -a[1]), reverse=True)
                # start from the beginning of the new guess_order
                index = 0

except EOFError:
    pass

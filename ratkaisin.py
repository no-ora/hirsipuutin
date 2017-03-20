# Simple hangman solver, guesses letters in order of frequency
import re
import sys
print('noora')

words = []

word = input().strip()
while word:
    word = word.encode('latin-1').decode('utf-8')
    words.append(word)
    word = input().strip()

original_words = words

try:
    status = input()
    status = status.encode('latin-1').decode('utf-8')
    while status:
        index = 0
        words = original_words

        # filter words with correct lenght
        words = [word for word in words if len(word) == len(status)]
        guessed_letters = []
        letters = {letter for word in words for letter in word}
        frequencies = [(letter, sum(word.count(letter) for word in words)) for letter in letters]
        guess_order = sorted(frequencies, key=lambda a: a[1], reverse=True)
        while True:
            # if only one word left, guess that
            if len(words) == 1:
                sys.stdout.buffer.write((words[0] + '\n').encode('utf-8'))
            
            # else guess next letter
            else:
                letter = guess_order[index][0]
                index += 1
                sys.stdout.buffer.write((letter + '\n').encode('utf-8'))
                guessed_letters.append(letter)
            
            result = input()
            result = result.encode('latin-1').decode('utf-8')
            status = input()
            status = status.encode('latin-1').decode('utf-8')

            # when winning or losing and starting a new game prints three lines
            if status.startswith('WIN') or status.startswith('LOSE') or not status:
                status = input()
                status = status.encode('latin-1').decode('utf-8')
                break

            # if hit, filter words with correct regex
            if result.startswith('HIT'):
                regex = '.{'
                n = 0
                for c in status:
                    if c == '.':
                        n+=1
                    else:
                        regex += (str(n) + '}' + c + '.{')
                        n = 0
                if regex.endswith('{'):
                    regex += '0}'
                r = re.compile(regex)

                # filter words and count new frequencies
                words = list(filter(r.match, words))

            # if missed, filter words with incorrect letters
            if result.startswith('MISS'):
                words = list(filter(lambda w: letter not in w, words))

            # ignore letters that have already been guessed
            letters = {letter for word in words for letter in word if letter not in guessed_letters}
            frequencies = [(letter, sum(word.count(letter) for word in words)) for letter in letters]
            guess_order = sorted(frequencies, key=lambda a: a[1], reverse=True)

            # start from the beginning of the new guess_order
            index = 0

except EOFError:
    pass

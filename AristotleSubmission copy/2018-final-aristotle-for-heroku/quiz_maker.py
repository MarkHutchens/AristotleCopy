__author__ = 'mark'

# Arbitrary change for git
# These functions return plausible quiz question prompts
from collections import defaultdict


import random
class Quizzer():
    def __init__(self):
        self.last = defaultdict(int)

    def pair(self,min=4, max=1000):
        num = random.randint(min,max)
        decimal = '{0:d}'.format(num)
        binary = '{0:b}'.format(num)
        return(decimal, binary)


    def describe_script_dec(self):
        number = self.pair()
        to_return = [] #List of sentences to print, possibly with delay in between
        to_add = [] #List of decimal ints we're keeping track of
        length = len(number[1])
        if len(number[1]) == 0:
            return to_return
        def subsentence(number, length, place):
            # 'place' kinda unintuitively goes backwards
            to_return = " has a "
            if place == length - 1:
                to_return = number[1] + to_return
            elif place == 0:
                to_return = "And it" + to_return
            else:
                to_return = "It" + to_return
            to_return += number[1][length-place - 1] + " in the " + str(2**place) + " place."
            return to_return

        to_return.append("Let's try the number " + number[1] + ".")
        for place in range(length)[::-1]:
            to_return.append(subsentence(number, length, place))
            to_add.append(str((2**(place)) * (int(number[1][length-place - 1]))))

        to_return.append(" + ".join(to_add) + " is " + number[0] + ".")
        return to_return

    def equal_quiz(self):
        decimal, binary = self.pair(min=6,max=63)
        self.last['decimal'] = int(decimal)

        return("What is %s in binary?" %decimal)

    def equal_quiz_grade(self, answer):
        correct = '{0:b}'.format(self.last['decimal'])
        if str(answer) == correct:
            return("Correct! \nHere's another question: %s" %self.equal_quiz())
        else:
            return("Sorry, that's incorrect. You said %s when the answer is %s. \nHere's another question: %s" %(answer, correct, self.equal_quiz()))

if __name__ == "__main__":
    q = Quizzer()
    #print(q.pair())
    print(q.equal_quiz())
    print(q.equal_quiz_grade("1101"))
    #for line in script:
    #    print(line)
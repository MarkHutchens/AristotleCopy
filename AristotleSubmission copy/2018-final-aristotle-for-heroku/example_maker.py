__author__ = 'mark'
import random
from collections import defaultdict

class Example_Maker():
    """
    This bad boy has lots of examples of binary/decimal for us to play with
    """

    def __init__(self):
        self.counter = defaultdict(int)
        self.debug = False
        pass

    def pair(self,min=4, max=1000, preset=None):
        # Literally the same code again, maybe should make a superclass
        if preset:
            num = int(preset)
        else:
            num = random.randint(min,max)
        decimal = '{0:d}'.format(num)
        binary = '{0:b}'.format(num)
        return(decimal, binary)



    def rephrase_binary_counting(self, first=None, second=None,):
        self.counter['count_count'] += 1
        # if randint == 1:
        #     to_return = \
        #         """Alright then. Let's start small
        #             Zero and one are represented as 0 and 1, just like you're familiar with.
        #             But binary doesn't have the 2 symbol to say 'two'.
        #             So our only option is to carry the 1. So two is represented as '10'
        #             That's 'One two, and zero ones'
        #             Then three would be 11. What would four be?""".split("\n")
        #     # This should probably just be in DialogFlow, it's too deterministic.
        if first != None and second != None:
            decimal, binary = self.pair(preset=first)
            to_return = ["Sure."]
        elif self.counter['count_count'] == 1:
            decimal, binary =  self.pair(min=5, max=15)
            while self.palindrome(binary): # Pedagogically want to avoid palindromes here.
                decimal, binary =  self.pair(min=5, max=15)
            to_return = ["Let's try a smaller number then."]
        else:
            to_return = ["We can do another counting example, sure!"]
            decimal, binary =  self.pair(min=5, max=127) # Don't want to be too restricted with extended requests
            while self.palindrome(binary):
                decimal, binary =  self.pair(min=5, max=127)

        decimal2 = decimal

        to_return.append("%s in decimal will be represented as %s in binary." %(decimal, binary))
        to_return.append("We'll go right to left as we make our binary number.")
        to_return.append("")
        for binary_digit in binary[::-1]:
            next = str(int(int(decimal2) / 2))
            to_return.append("%s divided by two (%s) has a remainder of %s." %(decimal2, next, binary_digit))
            decimal2 = next
        to_return.append("So our binary number, reading from bottom to top, is %s." %binary)
        to_return.append("If you want another example, just ask for 'another counting', alright? Otherwise we can move on.")
        if self.debug: to_return.append("DEBUG NOTE: count is %d" %(self.counter['count']))


        return to_return

    def rephrase_decimal_counting(self):
        # Taken from the quiz_maker class that will have a different purpose going forward.
        number =  self.pair(min=100, max=10000) # Don't want to be too restricted with extended requests

        to_return = [] #List of sentences to print, possibly with delay in between
        to_add = [] #List of decimal ints we're keeping track of
        length = len(number[0])
        if len(number[0]) == 0:
            return to_return
        def subsentence(number, length, place):
            # 'place' kinda unintuitively goes backwards
            to_return = " has a "
            if place == length - 1:
                to_return = number[0] + to_return
            elif place == 0:
                to_return = "And it" + to_return
            else:
                to_return = "It" + to_return
            to_return += number[0][length-place - 1] + " in the " + str(10**place) + " place."
            return to_return

        to_return.append("Let's try the number " + number[0] + ".")
        for place in range(length)[::-1]:
            to_return.append(subsentence(number, length, place))
            to_add.append(str((10**(place)) * (int(number[0][length-place - 1]))))

        to_return.append(" + ".join(to_add) + " is " + number[0] + ".")
        to_return.append("Do you understand? Should we move on?")
        return to_return

    def addition_example(self, first=None, second=None, third=None):
        self.counter['addition'] += 1
        to_return = []
        #if self.counter['addition'] == 1:
        def subloop(up,dwn,car):
            to_return = []
            to_return.append("Our two digits are %s and %s." %(up,dwn))
            if car == '1': #Don't need text if it's 0.
                to_return.append("And you have another 1 from the carry.")
            result = int(up) + int(dwn) + int(car)
            if result == 0:
                to_return.append("So we have 0 here, simple enough.")
            elif result == 1:
                to_return.append("That means we put a 1 in this digit.")
            elif result == 2:
                to_return.append("Two 1s means we get a 0 and a carry.")
            elif result == 3:
                to_return.append("That means we get a 1 AND a carry.")
            return to_return, str(int(result >= 2))

        decimal1, binary1 = self.pair(min=3,max=15,preset=first)
        decimal2, binary2 = self.pair(min=int(decimal1), max=31, preset=second) #Guarantee this one's at least as big
        decimal3 = str(int(decimal2) + int(decimal1))
        binary3 = '{0:b}'.format(int(decimal3))
        to_return.append("%s + %s = %s in decimal, right?" %(decimal2,decimal1, decimal3))
        to_return.append("That's like writing %s + %s = %s in binary." %(binary2, binary1, binary3))
        to_return.append("Again, we'll work from the right to the left.")

        # Make these numbers all the same length.
        binary1, binary3 = self.padding(binary1, binary3)
        binary2, binary3 = self.padding(binary2, binary3)
        carry = '0'
        for digit in range(len(binary3))[::-1]:
            to_add, carry = subloop(binary1[digit], binary2[digit], carry)
            to_return.extend(to_add)
            if digit != 0:
                to_return.append("Our current result is %s" %binary3[digit:])
            else:
                to_return.append("And our final result is %s or %s." %(binary3,decimal3))
        if third != None:
            if decimal3 == str(third):
                to_return.append("Which is the same, so you are right!")
            else:
                to_return.append("Which is different from %d, sorry." %third)
        return to_return

    def decimal_addition_example(self, first=None, second=None, third=None):
        # Ew, copy/pasted code.
        self.counter['addition'] += 1
        to_return = []
        #if self.counter['addition'] == 1:
        def subloop(up,dwn,car):
            to_return = []
            to_return.append("Our two digits are %s and %s." %(up,dwn))
            if car == '1': #Don't need text if it's 0.
                to_return.append("And you have another 1 from the carry.")
            result = int(up) + int(dwn) + int(car)
            if result <= 9:
                to_return.append("So we get a %d in this place." %result)
            else:
                to_return.append("We get %d, which is too big, so we carry the 1" %result)
            return to_return, str(int(result >= 10))

        decimal1, binary1 = self.pair(min=120,max=999,preset=first)
        decimal2, binary2 = self.pair(min=int(decimal1), max=1000, preset=second) #Guarantee this one's at least as big
        decimal3 = str(int(decimal2) + int(decimal1))
        binary3 = '{0:b}'.format(int(decimal3))
        to_return.append("Let's add %s and %s" %(decimal2,decimal1))
        to_return.append("We'll work small to large, right to left.")

        # Make these numbers all the same length.
        decimal1, decimal3 = self.padding(decimal1, decimal3)
        decimal2, decimal3 = self.padding(decimal2, decimal3)
        carry = '0'
        for digit in range(1,len(decimal3) + 1):
            if self.debug: print(decimal1, decimal2, decimal3, digit)
            if digit != len(decimal3):
                to_add, carry = subloop(decimal1[-digit], decimal2[-digit], carry)
                to_return.extend(to_add)
                to_return.append("Our current result is %s" %decimal3[-digit:])
            else:
                # Final digit. More interesting than binary case.
                if digit > len(decimal2):
                    to_return.append("That last 1 goes in front.")
                else:
                    to_add, carry = subloop(decimal1[-digit], decimal2[-digit], carry)
                    to_return.extend(to_add)
                to_return.append("And our final result is %s." %(decimal3))
        if third != None:
            if decimal3 == str(third):
                to_return.append("Which is the same, so you are right!")
            else:
                to_return.append("Which is different from %d, sorry." %third)
        return to_return


    def conversion_check(self, binary='0', decimal='0'):
        if str(binary) == '{0:b}'.format(int(decimal)):
            return(["Yes they are the same."])
        else:
            to_return = ["No they are not equal"]
            to_return.append("%s is %s in binary. And %s is %s in decimal." \
                             %(str(decimal), '{0:b}'.format(int(decimal)), str(binary), int(str(binary),2)))
            return to_return


    def fraction_examples(self, req, params):

        num = str(params.get('number'))[:-2]
        result = None
        for digit in num:
            if digit in '23456789':
                result = self.fraction_decimal2binary(num)
            else:
                result = self.fraction_binary2decimal(num)
        return result

    def fraction_binary2decimal(self, num):
        t = num.split('.')
        result = str(int(t[0], 2) + int(t[1], 2) / 2.**len(t[1]))
        to_return = []
        to_return.append("%s in binary is %s in decimal" %(num,result))
        to_return.append("Let's step through it.")
        to_return.append("First, we count the places to move the decimal, which is %s. This will go in the denominator." %len(t[1]))
        numerator = (str(int(t[0], 2) + int(t[1], 2)))
        to_return.append("That gives us %s, or %s in decimal, as the numerator." %("{0:b}".format(int(numerator)), numerator))
        denominator = 2**len(t[1])
        to_return.append("Two raised to the power of %s (%s) is the denominator." %(len(t[1]), denominator))
        to_return.append("%s/%s is %s." %(numerator, denominator, result))
        return to_return

    def fraction_decimal2binary(self, num):
        to_return = ["Our strategy is to repeatedly multiply times two, and see if we're over one."]
        int_part = int(float(num))
        fract_part = float(num) - int_part
        binary = ''
        int_part = bin(int_part)[2:]
        k = 8
        while k > 0:
            to_return.append("%.4f times two is %.4f,"%(fract_part, fract_part * 2))
            fract_part = fract_part*2
            new_int = int(fract_part)
            if new_int == 1:
                fract_part -= 1
                binary = binary+'1'
                to_return.append("which is over 1.")
            else:
                binary = binary + '0'
                to_return.append("which is under 1.")
            if fract_part == 0: # Truncate after we're done
                to_return.append("And that's all that's left.")
                break
            to_return.append("So far we have %s" %(str(int_part)+'.'+binary))
            k -= 1
        if k == 0:
            to_return.append("And we'll cut it off there, or we'll be here all day.")
        to_return.append("%s is our final result."%(str(int_part)+'.'+binary))
        return to_return

    def subtraction_decimal(self, num1=None,num2=None,guessing=None):
        to_return = []
        #make sure the first num is greater than the second one. If not, exchange them
        if int(num1) < int(num2):
            tmp = num2
            num2 = num1
            num1 = tmp
        to_return.append('I am putting the larger number on the left, so %s - %s.' %(num1, num2))
        #padding numbers
        if len(num1) != len(num2):
            num1, num2 = self.padding(num1, num2)
            to_return.append('It will make our life easier if the two numbers are in the same length. If they were not, I would suggest to pad zeros before the shorter one. So we got %s and %s .' %(num1, num2))
        k = len(num1)-1
        num3=[0]*(1+k)
        num1 = list(num1)
        num2 = list(num2)
        to_return.append("Let's start subtraction now. We will work right to left.")
        while k >= 0:
            if int(num1[k])>int(num2[k]):
                num3[k] = int(num1[k])-int(num2[k])
            elif int(num1[k]) == int(num2[k]):
                num3[k] = int(num1[k])-int(num2[k])
            else:
                num1_rest = num1[:k]
                num2_rest = num2[:k]
                num3[k] = int(num1[k])+10-int(num2[k])
                i = len(num1_rest)
                to_return.append("Since %s is smaller than %s, we need to borrow one from the left digit. If the left digit is 0, we keep going left until we can get 1 to borrow."%(num1[k], num2[k]))
                while i > 0:
                    if int(num1_rest[i-1]) > 0:
                        borrowing_idx = i-1
                        num1[borrowing_idx] = str(int(num1[borrowing_idx])-1)
                        for j in range(i,k):
                            num1[j] = 9
                        break
                    i -= 1
            k -= 1
        str_ans = ''.join([str(i) for i in num3])
        to_return.append("So we got %s." %(str_ans))
        if guessing != None:
            guessing, num3 = self.padding(guessing, str_ans)
            if guessing == num3:
                to_return.append("You are right!")
            else:
                to_return.append("Your answer is different to mine.")
        return to_return

    def subtraction_binary(self, num1=None,num2=None,guessing=None):
        to_return = []

        if int(num1,2) < int(num2,2):
            tmp = num2
            num2 = num1
            num1 = tmp
        to_return.append('I am putting the larger number on the left, so %s - %s.' %(num1, num2))
        if len(num1) != len(num2):
            num1, num2 = self.padding(num1, num2)
        k = len(num1)-1
        num3=[0]*(1+k)
        num1 = list(num1)
        num2 = list(num2)
        to_return.append("Let's start subtraction now. We will work right to left.")
        while k >= 0:
            if int(num1[k])>int(num2[k]):
                num3[k] = int(num1[k],2)-int(num2[k],2)
            elif int(num1[k]) == int(num2[k]):
                num3[k] = int(num1[k])-int(num2[k])
            else:
                num1_rest = num1[:k]
                num2_rest = num2[:k]
                num3[k] = int(num1[k],2)+2-int(num2[k],2)
                i = len(num1_rest)
                to_return.append("Since %s is smaller than %s, we need to borrow one from the left digit. If the left digit is 0, we keep going left until we can get 1 to borrow."%(num1[k], num2[k]))
                while i > 0:
                    if int(num1_rest[i-1]) > 0:
                        borrowing_idx = i-1
                        num1[borrowing_idx] = str(int(num1[borrowing_idx])-1)
                        for j in range(i,k):
                            num1[j] = 1
                        break
                    i -= 1
            k -= 1
        str_ans = ''.join([str(i) for i in num3])
        to_return.append("So we got %s." %(str_ans))
        if guessing != None:
            guessing, num3 = self.padding(guessing, str_ans)
            if guessing == num3:
                to_return.append("You are right!")
            else:
                to_return.append("Your answer is different to mine.")
        return to_return


    def padding(self, num1, num2):
        # Make num1 as long as num2 with leading zeroes
        a = len(num1)-len(num2)
        if a > 0:
            num2 = '0'*abs(a)+num2
        elif a < 0:
            num1 = '0'*abs(a)+num1
        return num1,num2


    def palindrome(self, string):
        return(string == string[::-1])

if __name__ == "__main__":
    num1 = "101"
    num2 = "7"
    em = Example_Maker()
    phrase = em.subtraction_decimal('1001', '111','10')
    for line in phrase:
        print(line)
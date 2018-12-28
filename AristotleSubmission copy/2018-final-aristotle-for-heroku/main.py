#! /usr/bin/env python3 

from flask import Flask, request, make_response, jsonify
import json
import quiz_maker
import example_maker
import os
app = Flask(__name__)

em = example_maker.Example_Maker()
qm = quiz_maker.Quizzer()
debug = False


@app.route("/webhook", methods=["POST", "GET"])

def webhook():
    # These action names are so long :(
    global em
    global qm
    if request.method == 'POST':
        req = request.get_json(silent=True, force=True)
        action = req.get('queryResult').get('action')
        params = None
        try:
            params = req.get('queryResult').get('parameters')
        except:
            pass

        if action == 'Countingintro.Countingintro-yes.Doknowdecimalmoveontobinary-no'\
                or action == 'Countingintro.Countingintro-no.Countingintro-no-yes.Understanddecimalmoveontobinary-no'\
                or action == 'Anothercounting':
            res = counting_binary_examples(req)

        elif action == 'Convertbinarydecimal':
            pass
        elif action == 'Convertdecimalbinary':
            pass
        elif action == 'Countingintro.Countingintro-no.Countingintro-no-no':
            res = counting_decimal_examples(req)
        elif action == 'Additionintro.Additionintro-custom.dontknowcarry-custom'\
                or action == "Additionintro.Additionintro-custom.dontknowcarry-custom.dontunderstandcarryneedexamples-custom":
            res = addition_carry_examples(req, params)
        elif action == 'Additionintro.Additionintro-custom.dontknowcarry-custom.understandcarrymovetoaddition-custom'\
                or action == 'Additionintro.Additionintro-custom.knowcarry-no'\
                or action == 'Additionintro.Additionintro-custom.knowcarry-custom'\
                or action == 'Additionintro.Additionintro-custom.knowcarry-no.dontunderstandadditionneedexamples-custom'\
                or action == 'Additionagain':
            res = addition_examples(req, params)
        elif action == "Countingintro.Countingintro-yes.Doknowdecimalmoveontobinary-no.Doesntunderstandbinary-needsexamples-custom":
            params = req.get('queryResult').get('parameters')
            res = conversion_example(params)

        elif action == "Countingquiz":
            res = qm.equal_quiz()
        elif action == "Countingquiz.answer":
            params = req.get('queryResult').get('parameters')
            res = qm.equal_quiz_grade(str(params.get('number'))[:-2])


        elif action == "Subtractionintro.Subtractionintro-yes.knowaddition-no.Doesntunderstandsubtractionneedsexamples-custom":
            # Numbers one and two are both in here.
            number0, number1 = str(params.get('number')), str(params.get('number1'))
            try:
                number2 = str(params.get('number2'))[:-2]
            except:
                number2 = None
            chars = set('23456789')
            if not any((c in chars) for c in number0) and not any((c in chars) for c in number1):
                res="\n".join(em.subtraction_binary(str(number0)[:-2], str(number1)[:-2], number2))
            else:
                res="\n".join(em.subtraction_decimal(str(number0)[:-2], str(number1)[:-2], number2))

        elif action == "Fractionsintro.Fractionsintro-yes.Wantstocontinuetalkfractions-no.Doesntunderstandfractionsneedsexamples-custom":
            number = str(params.get('number'))
            chars = set('23456789')
            if not any((c in chars) for c in number):
                res="\n".join(em.fraction_binary2decimal(number))
            else:
                res="\n".join(em.fraction_decimal2binary(number))

        else:
            res = "It's nice to talk to you! But I did not understand."
            if debug: res = res + "DEBUG: %s" %action
        return make_response(jsonify({'fulfillmentText': res}))

def counting_binary_examples(req):
    return('\n'.join(em.rephrase_binary_counting()))
    
def counting_decimal_examples(req):
    # I am not prioritizing this one. Decimal calculations are less likely to matter. ~Mark
    # Okay, time to go for it.
    return ('\n'.join(em.rephrase_decimal_counting()))

def addition_carry_examples(req, params=None):
    # Also not a piority. ATM just gonna do the same as the counting example
    number0, number1, number2 = None, None, None
    if params != None:
        if debug: print(params)
        try:
            number0 = str(params.get('number'))[:-2]
            number1 = str(params.get('number1'))[:-2]
            number0 = int(number0)
            number1 = int(number1)
            try:
                if params.get('number2') != "":
                    number2 = str(params.get('number2'))[:-2]
                    number2 = int(number2)
            except: pass
            if debug: print("got to assigning:", number0, number1, number2)
            to_return = '\n'.join(em.decimal_addition_example(first=number0, second=number1, third=number2))
            return(to_return)
        except:
            if debug: print("Got an error in assigning numbers")
            pass
    return('\n'.join(em.decimal_addition_example()))
    pass

def addition_examples(req, params):
    if params != None:
        number0, number1, number2 = None, None, None
        if debug: print(params)
        try:
            number0 = str(params.get('number'))[:-2]
            number1 = str(params.get('number1'))[:-2]
            number0 = int(number0,2)
            number1 = int(number1,2)
            try:
                if params.get('number2') != "":
                    number2 = str(params.get('number2'))[:-2]
                    number2 = int(number2,2)
            except: pass
            if debug: print("got to assigning:", number0, number1, number2)
            to_return = '\n'.join(em.addition_example(first=number0, second=number1, third=number2))
            return(to_return)
        except:
            if debug: print("Got an error in assigning numbers")
            pass
    return('\n'.join(em.addition_example()))


def conversion_example(params):
    number0 = str(params.get('number'))[:-2]
    number1 = str(params.get('number1'))[:-2]
    print(number0, number1)
    chars = set('23456789')
    if not any((c in chars) for c in number0):
        binary = number0
        decimal = number1
    elif not any((c in chars) for c in number1):
        binary = number1
        decimal = number0
    else:
        return("There doesn't seem to be a binary number here. Could you try again?")

    return('\n'.join(em.conversion_check(binary=binary, decimal=decimal)))

        
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
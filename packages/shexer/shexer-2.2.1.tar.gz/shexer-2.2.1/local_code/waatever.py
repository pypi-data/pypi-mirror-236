# SECRET_NUMBER = 7
# user_answer = int(input("Guess a number a number between 1 and 100: "))
# prev_answer = user_answer
# attempts = 1
# while user_answer != SECRET_NUMBER:
#     if user_answer < 1 or user_answer > 100:
#         print("FOCUS! I said between 1 and 100")
#     else:
#         if user_answer < SECRET_NUMBER:
#             if user_answer < prev_answer and prev_answer < SECRET_NUMBER:
#                 print("I told you greater than", prev_answer, "! So greater!")
#             else:
#                 print("Wrong, it's greater. Try again: ")
#         else:   # user_answer > SECRET_NUMBER
#             if user_answer > prev_answer and prev_answer > SECRET_NUMBER:
#                 print("I told you lower than ", prev_answer, "! So lower!")
#             else:
#                 print("Wrong, it's lower. Try again: ")
#     attempts = attempts + 1
#     prev_answer = user_answer
#     user_answer = int(input())
# print("You guessed it! It took you", attempts, "tries")

print("1 - Add 3 numbers")
print("2 - Divide two numbers")
print("3 - Count from one to a number")
print("0 - Finish program")
option = input("Introduce an option: ")
while option != "0":
    if option == "1":
        number1 = int(input("Introduce the first number: "))
        number2 = int(input("Introduce the second number: "))
        number3 = int(input("Introduce the third number: "))
        print("The result is", number1 + number2 + number3)
    elif option == "2":
        number1 = float(input("Introduce the first number: "))
        number2 = float(input("Introduce the second number: "))
        print("The result is", number1 / number2)
    elif option == "3":
        target = int(input("Introduce a number: "))
        current = 1
        while current < target:
            print(current)
            current += 1
    print("1 - Add 3 numbers")
    print("2 - Divide two numbers")
    print("3 - Count from one to a number")
    print("0 - Finish program")
    option = input("Introduce another option: ")
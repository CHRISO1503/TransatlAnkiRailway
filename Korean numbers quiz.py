from random import random
from unicodedata import digit

# mode 0 = sino-korean, mode 1 = pure korean
mode = 1
sinoUnits = ['일', '이', '삼', '사', '오', '욕', '칠', '팔', '구']
sinoOrders = ['만', '천', '백', '십']
pureUnits = ['', '하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉']
pureTens = ['', '열', '스물', '서른', '마흔', '쉰']
pureCounterExceptions = [1, 2, 3, 4, '한', '두', '세', '네']


def translateNumber(x, _mode):
    koreanString = ''
    digitList = [int(y) for y in str(x)]

    if _mode == 0:
        # Force digit list to be 5 digits long by adding 0's to front
        if (len(digitList) < 5):
            for i in range(5 - len(digitList)):
                digitList.insert(0, 0)

        # j is the index for sinoOrders
        j = 0
        zero = False
        for i in range(len(digitList)*2):
            # For even indeces, add a sinoUnit at the beginning of koreanString
            if (i % 2 == 0):
                unitIndex = digitList[len(digitList)-i//2-1]

                if (unitIndex < 0):
                    zero = True
                    continue

                koreanString = sinoUnits[unitIndex-1] + koreanString

            # For odd indeces, put a sinoOrder at the beginning of koreanString
            else:
                if (j > len(digitList)/2+0.6 or sinoUnits[unitIndex-2] == 0):
                    zero = False
                    continue
                koreanString = sinoOrders[len(sinoOrders)-j-1] + koreanString
                j += 1

        # Remove unnecessary 1's and 0's
        onesCount = 0
        for i in range(len(digitList)):
            if (digitList[i] == 0):
                if (i == len(digitList)-1):
                    # Remove final 0 which has no sinoOrder
                    koreanString = koreanString[:-1]
                else:
                    # Remove 0's which have sinoOrder attached
                    koreanString = koreanString.replace('구'+sinoOrders[i], '')

            elif (digitList[i] == 1 and i < len(digitList)-1):
                # Count number of 1's for deletion (does not include final digit)
                onesCount += 1
        # Remove ones
        koreanString = koreanString.replace('일', '', onesCount)

    elif _mode == 1:
        if (len(digitList) == 1):
            koreanString = pureUnits[digitList[0]]
        elif(len(digitList) == 2):
            koreanString = pureTens[digitList[0]] + pureUnits[digitList[1]]
        else:
            print("Number of digits is invalid for pure korean counting.")

    else:
        print("Invalid _mode.")

    return(koreanString)


def randomNumberGenerator():
    if (mode == 0):
        magnitude = round(random()*5)
        x = round(random()*10**magnitude-0.5)
    elif (mode == 1):
        x = round(random()*50-0.5)
    if x == 0:
        x = 1
    return x


def chooseMode():
    validMode = False
    while (validMode == False):
        mode = input(
            'Type 0 for Sino-Korean questions, 1 for Pure-Korean questions, or 2 for a mixture of questions. ')
        mode = int(mode)
        global randomMode
        if mode == 0 or mode == 1:
            validMode = True
            randomMode = False
            return mode
        elif mode == 2:
            validMode = True
            randomMode = True
        else:
            print('Invalid mode.')


playing = True
modeStrings = ['Sino-Korean', 'Pure Korean']
randomMode = False
mode = chooseMode()

while (playing):

    # Setup numbers for question
    if randomMode == True:
        mode = round(random()*2-0.5)
    number = randomNumberGenerator()
    translatedNumber = translateNumber(number, mode)
    numberWithCounter = translatedNumber

    # Ask question
    print('Write ' + str(number) + ' using ' + modeStrings[mode] + ':')
    guess = input()

    # Respond based on answer to question
    if (guess == translatedNumber):
        print('Correct')
    else:
        print('Incorrect')
    print(str(number) + ' in ' +
          modeStrings[mode] + ' is ' + translatedNumber + '.')

    # Show the number in front of a counter if it is different
    if (mode == 1):
        if (number % 10 in pureCounterExceptions):
            numberWithCounter = translatedNumber.rsplit(pureUnits[number % 10])
            numberWithCounter = pureCounterExceptions[number % 10 + len(
                pureCounterExceptions)//2 - 1].join(numberWithCounter)
        elif (number == 20):
            numberWithCounter = '스무'

        if translatedNumber != numberWithCounter:
            print('In front of a counter it is written ' +
                  numberWithCounter + '.')

    # Let the user decide what to do next
    play = input(
        'Type \'exit\' or \'출구\' to stop, type \'m\' to change modes, or press enter to continue.')
    if (play == 'exit' or play == '출구'):
        playing = False
    elif(play == 'm'):
        mode = chooseMode()

# Could add a mode where the user writes the digits given a korean number

from random import random
from unicodedata import digit

# mode 0 = sino-korean, mode 1 = pure korean
mode = 0
sinoUnits = ['일', '이', '삼', '사', '오', '욕', '칠', '팔', '구']
sinoOrders = ['십', '백', '천', '만']


def translateNumber(x):
    if mode == 0:
        koreanString = ''
        digitList = [int(y) for y in str(x)]

        # Force digit list to be 5 digits long by adding 0's to front
        if (len(digitList) < 5):
            for i in range(5 - len(digitList)):
                digitList.insert(0, 0)
        print(digitList)

        j = 0
        zero = False
        for i in range(len(digitList)*2):
            if (i % 2 == 0):
                unitIndex = digitList[len(digitList)-i//2-1]

                if (unitIndex < 0):
                    zero = True
                    continue

                koreanString = sinoUnits[unitIndex-1] + koreanString
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

    else:
        print('mode 2')

    return(koreanString)

def randomNumberGenerator(maxMagnitude):
    magnitude = round(random()*maxMagnitude)
    return round(random()*10**magnitude-0.5)


playing = True

while (playing):
    number = randomNumberGenerator(5)
    translatedNumber = translateNumber(number)
    print('Write ' + str(number) + ' using Sino-Korean:')
    guess = input()
    if (guess == translatedNumber):
        print('Correct')
    else:
        print('Incorrect')
    print(str(number) + ' in korean is ' + translatedNumber)

    play = input(
        'Type \'exit\' or \'출구\' to stop, or press enter to continue.')
    if (play == 'exit' or play == '출구'):
        playing = False

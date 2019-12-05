# Luhn algorithm 
def luhn_function(card_number):
    card_list = list(card_number)
    reversed_card_list = card_list[::-1]
    card_sum = 0

    for index in range(0, len(reversed_card_list)):

        if index % 2:
            temp_number = int(reversed_card_list[index])
            double_temp_number = temp_number * 2
            if double_temp_number > 9:
                subtracted_temp_number = double_temp_number - 9
                card_sum += subtracted_temp_number
            else:
                card_sum += double_temp_number

        else:
            temp_number = int(reversed_card_list[index])
            card_sum += temp_number

    return card_sum % 10 == 0

#Find the censored number by brute forcing 0-9.
def find_censored(nbr):
  x = 0
  for y in range(10):
    number = list(nbr)
    number[number.index("X")] = x
    finalnbr = "".join(map(str,number))
    x += 1
    if(luhn_function(finalnbr)):
      return x -1
#Print a concatenated string of all censored numbers 
def printCensored():
    y = ''
    with open('HA1B/1/testin.txt', 'r') as func:
        for line in func: 
            line = line.strip('\n')
            y = y + str(find_censored(line))
        print(y)    


printCensored() 
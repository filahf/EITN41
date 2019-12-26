from hashlib import sha1

#SHA1 hash the data
def compute_hash(data):
    return sha1(bytearray.fromhex(data)).hexdigest()

def print_liten():
    #Open the file and add each row to String_list[]
    with open('HA1B/3/merkle_test1.txt', 'r', encoding='utf-8') as func:
        string_list = []
        for line in func:
            line = line.strip('\n')
            string_list.append(line)
        #Save data in this string
        main_string = ""

        for index in range(0, len(string_list)-1):
            if index == 0:
                main_string = string_list.pop(index)
                
            if string_list[index].startswith("L"):
                new_string = string_list[index]
                left_string = new_string[1:]
                main_string = left_string + main_string
                main_string = compute_hash(main_string)

            else:
                new_string = string_list[index]
                right_string = new_string[1:]
                main_string = main_string + right_string
                main_string = compute_hash(main_string)
            
        print(main_string)

print_liten()
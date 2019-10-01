name = input("What's your name? ")
age = int(input("How old are you? "))

print(name)
print(age)


def str_lin():
    print(name+" "+str(age))


str_lin()


def all_str_lin():
    data1 = input("data 1: ")
    data2 = input("data 2: ")
    print(str(data1)+' '+str(data2))


all_str_lin()


def dec_machine():
    decades = int(age)//10
    return decades


nr_decades = dec_machine()
print(nr_decades)

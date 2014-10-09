from random import randint, random

def new_rand():

    my_rand = 0
    while my_rand == 0: # Make sure we never return 0 so do_work doesn't divide 0
        my_rand = randint(int(random()), int((random()+1)*1000))

    return my_rand

def do_work():

    x = ((new_rand() + new_rand()) * new_rand()) % new_rand()
    return x

def main():
    out = ""
    for y in range(5):
        out += str(do_work()) + "\n"
    return out
def do_work():
    def new_rand():
        from random import randint, random
        my_rand = 0
        while my_rand == 0: # Make sure we never return 0 so do_work doesn't divide 0
            my_rand = randint(int(random()), int((random()+1)*1000))

        return my_rand
    x = ((new_rand() + new_rand()) * new_rand()) % new_rand()
    print(x)


for y in range(5):
    do_work()
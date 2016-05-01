import goaway

l = goaway.Lock("l")
s = goaway.Strict("s")

def increment_and_copy():
    l.acquire()
    s.num += 1
    s.num2 = s.num
    l.release()

if __name__ == "__main__":

    s.num = 0

    for i in range(10):
        goaway.goaway(increment_and_copy)

    while s.num < 10:
        pass #wait

    print s.num
    print s.num2

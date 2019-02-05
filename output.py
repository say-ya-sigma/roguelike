def stage(x, y):
    print("#"*(x+2))
    for i in range(y):
        print("#" + " "*x + "#")
    print("#"*(x+2))

stage(20, 10)

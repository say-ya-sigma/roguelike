def gen_stage(x, y):
    Stage = []
    Stage.append(['#']*(x+2))
    for i in range(y):
        Stage.append(['#'] + [' ']*x + ['#'])
    Stage.append(['#']*(x+2))
    return Stage

def output_stage(Stage):
    for i in range(len(Stage)):
        print(''.join(Stage[i]))

output_stage(gen_stage(20, 10))

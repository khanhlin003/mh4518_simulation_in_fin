import random

def payoff_func(
        path_rog, 
        path_cfr, 
        path_zurn,
        denomination=1000,
        coupon=0.0875, 
        price_rog=257.65, 
        price_cfr=125.60, 
        price_zurn=412.30
        ):
    print('Hello')
    # print(f'Path ROG: {path_rog}')
    # print(f'Path CFR: {path_cfr}')
    # print(f'Path ZURN: {path_zurn}')

    coupon_payoff = denomination * coupon

    barrier_rog = price_rog * 0.6
    barrier_cfr = price_cfr * 0.6
    barrier_zurn = price_zurn * 0.6

    performance_rog = path_rog[-1] / price_rog
    performance_cfr = path_cfr[-1] / price_cfr
    performance_zurn = path_zurn[-1] / price_zurn
    worst_performance = min(performance_rog, performance_cfr, performance_zurn)
    print(f'Worst performance: {worst_performance}')

    barrier = False

    for element in path_rog:
        if element <= barrier_rog:
            barrier = True
            break

    for element in path_cfr:
        if element <= barrier_cfr:
            barrier = True
            break

    for element in path_zurn:
        if element <= barrier_zurn:
            barrier = True
            break
    print(f'Barrier event reached: {barrier}')
    
    above_initial = int((path_rog[-1] >= price_rog)) + \
                    int((path_cfr[-1] >= price_cfr)) + \
                    int((path_zurn[-1] >= price_zurn))
    print(f'Close above initial: {above_initial}')

    if (barrier==False) or (barrier==True and above_initial==3):
        denomination_payoff = denomination
    elif (barrier==True and above_initial<3):
        denomination_payoff = denomination * worst_performance
    elif path_rog[-1]==0 or path_cfr[-1]==0 or path_zurn[-1]==0:
        denomination_payoff = 0

    total_payoff = coupon_payoff + denomination_payoff
    return total_payoff

path_rog = [random.randint(100, 400) for _ in range(10)]
path_cfr = [random.randint(50, 200) for _ in range(10)]
path_zurn = [random.randint(320, 450) for _ in range(10)]

print(f'Final payoff: {payoff_func(path_rog, path_cfr, path_zurn)}')
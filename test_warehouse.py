import environment as we
from environment import Warehouse
from environment import SimulationTimeClock
from environment import Dock
from environment import Pos
from environment import Forklift
from environment import Aisle
from environment import Order

from policy import BasicPolicy
from policy import RandomPolicy
from policy import GreedyPolicy
from policy import MCTSPolicy
import time

########################################################################################################################
''' 테스트용 코드, 엑셀로 계산한 기대값과 동일한지 확인
'''
def make_test_warehouse_env_01():
    time_clock = SimulationTimeClock() # 해당 창고내에서는 공유해야할 Time
    size = (10,10) #창고 사이즈 (Grid 구조가정)
    docks = [Dock(0, Pos(0,0,0)),
             Dock(1,Pos(9,0,0))  ]
    aisles = [Aisle(0, time_clock, Pos(0,4,0), 5),
              Aisle(1, time_clock, Pos(5,4,0), 5),
              Aisle(2, time_clock, Pos(9,4,0), 5)
              ]

    forklifts = [Forklift(0,time_clock, Pos(9,0,0)),
                 Forklift(1, time_clock, Pos(9,0,0)) ]

    orders = []
    order_no = 0

    #order 생성
    for i in range(len(aisles)):# i = aisle 번호
        for j in range(2):
            #no, pos, aisle_no, truck_no
            pos = Pos(aisles[i].pos.x, aisles[i].pos.y + 1 + j, 1) # x, y, z
            aisle_no = i # np.random.randint(0,len(aisles))
            order = Order(order_no, pos, aisles[aisle_no], 1) #i번 aisle에 truck_no 기준 order
            order_no += 1
            orders.append(order)
            print('> Order create:', order)

    #time_clock, size, docks,  aisles, forklifts
    env = Warehouse(time_clock, size, docks, aisles, forklifts)
    env.set_orders(orders)

    return env




''' 테스트용 코드, 엑셀로 계산한 기대값과 동일한지 확인
'''

def make_test_warehouse_env(order_count):

    time_clock = SimulationTimeClock() # 해당 창고내에서는 공유해야할 Time
    size = (10,10) #창고 사이즈 (Grid 구조가정)
    docks = [Dock(0, Pos(0,0,0)),
             Dock(1,Pos(9,0,0))  ]
    aisles = [Aisle(0, time_clock, Pos(0,4,0), 5),
              Aisle(1, time_clock, Pos(5,4,0), 5),
              Aisle(2, time_clock, Pos(9,4,0), 5)
              ]

    forklifts = [Forklift(0,time_clock, Pos(0,0,0)),
                 Forklift(1, time_clock, Pos(0,0,0)),
                 Forklift(2, time_clock, Pos(9, 0, 0)),
                 Forklift(3, time_clock, Pos(9, 0, 0))
                ]

    orders = []
    order_no = 0

    #order 생성
    for i in range(order_count):# i = aisle 번호
        add_y = i % 5
        aisle_no = i % len(aisles)
        pos = Pos(aisles[aisle_no].pos.x, aisles[aisle_no].pos.y + 1 + add_y, 1) # x, y, z
        order = Order(order_no, pos, aisles[aisle_no], 1) #i번 aisle에 truck_no 기준 order
        order_no += 1
        orders.append(order)
        #print('> Order create:', order)

    #time_clock, size, docks,  aisles, forklifts
    env = Warehouse(time_clock, size, docks, aisles, forklifts)
    env.set_orders(orders)

    return env



def test_warehouse_01():
    env = make_test_warehouse_env_01()
    expected_value = 84
    policy = BasicPolicy()
    we.execute(env, policy)
    print('**' * 30)

    print('[Result]')
    print('Finish time clock value=', env.finish_time_clock,':uncompleted orders=',len(env.available_orders))


def test_warehouse_02():
    env = make_test_warehouse_env_01()
    expected_value = None
    policy = RandomPolicy()
    we.execute(env, policy)
    print('**' * 30)

    print('[Result]')
    print('Finish time clock value=', env.finish_time_clock,':uncompleted orders=',len(env.available_orders))


def test_warehouse_03():
    env = make_test_warehouse_env_01()
    expected_value = None
    policy = GreedyPolicy()
    we.execute(env, policy)
    print('**' * 30)

    print('[Result]')
    print('Finish time clock value=', env.finish_time_clock,':uncompleted orders=',len(env.available_orders))


def test_warehouse_04():
    env = make_test_warehouse_env_01()
    expected_value = None
    policy = MCTSPolicy()
    we.execute(env, policy)
    print('**' * 30)

    print('[Result]')
    print('Finish time clock value=', env.finish_time_clock,':uncompleted orders=',len(env.available_orders))


def test_warehouse_mcts(order_count, max_iteration=200, exploration_constant=1.41):
    start = time.time()

    env = make_test_warehouse_env(order_count) #order 60개기준
    expected_value = None
    policy = MCTSPolicy(max_iteration=200, exploration_constant=1.41)
    we.execute(env, policy)
    print('**' * 30)

    print('[Result] MCTS')
    print('Finish time clock value=', env.finish_time_clock,':uncompleted orders=',len(env.available_orders))
    print('Order=', policy.result_order)
    print('Folklift=', policy.result_folklift)
    end = time.time()
    print('time', (end - start))


def test_warehouse_random(order_count, max_iteration):
    start = time.time()

    #반복수행
    best = 99999999999
    for i in range(max_iteration):
        env = make_test_warehouse_env(order_count) #order 60개기준
        policy = RandomPolicy()
        we.execute(env, policy)
        if best > env.finish_time_clock:
            best = env.finish_time_clock
        #print('Finish time clock value=', env.finish_time_clock,':uncompleted orders=',len(env.available_orders))

    print('[Result] RandomPolicy')
    print("Random Best=", best)
    end = time.time()
    print('time', (end - start))

def test_warehouse_greedy(order_count):
    start = time.time()
    env = make_test_warehouse_env(order_count) #order 60개기준
    expected_value = None
    policy = GreedyPolicy()
    we.execute(env, policy)
    print('**' * 30)
    print('[Result]GreedyPolicy')
    print('Finish time clock value=', env.finish_time_clock,':uncompleted orders=',len(env.available_orders))
    end = time.time()
    print('time', (end - start))


########################################################################################################################


if __name__ == '__main__':
    #test_warehouse_01()
    #test_warehouse_02()
    #test_warehouse_03()
    #test_warehouse_04()

    #test_warehouse_mcts(60, max_iteration=200, exploration_constant=10)
    #test_warehouse_random(60, 10000)
    #test_warehouse_60_greedy(60)

    # test_warehouse_mcts(20, max_iteration=200, exploration_constant=1.41)
    # test_warehouse_mcts(20, max_iteration=200, exploration_constant=10)
    # test_warehouse_random(20, 10000)
    # test_warehouse_greedy(20)

    # test_warehouse_mcts(40, max_iteration=200, exploration_constant=1.41)
    # test_warehouse_mcts(40, max_iteration=200, exploration_constant=10)
    # test_warehouse_random(40, 10000)
    # test_warehouse_greedy(40)

    test_warehouse_mcts(80, max_iteration=200, exploration_constant=1.41)
    test_warehouse_mcts(80, max_iteration=200, exploration_constant=10)
    test_warehouse_random(80, 10000)
    test_warehouse_greedy(80)


    test_warehouse_mcts(100, max_iteration=200, exploration_constant=1.41)
    test_warehouse_mcts(100, max_iteration=200, exploration_constant=10)
    test_warehouse_random(100, 10000)
    test_warehouse_greedy(100)



#warehouse_test.py

import warehouse as we
import policy as p



''' 테스트용 코드, 엑셀로 계산한 기대값과 동일한지 확인
'''
def make_test_warehouse_env_01():
    time_clock = we.SimulationTimeClock() # 해당 창고내에서는 공유해야할 Time
    size = (10,10) #창고 사이즈 (Grid 구조가정)
    docks = [we.Dock(0, we.Pos(0,0,0)),
             we.Dock(1,we.Pos(9,0,0))  ]
    aisles = [we.Aisle(0, time_clock, we.Pos(0,4,0), 5),
              we.Aisle(1, time_clock, we.Pos(5,4,0), 5),
              we.Aisle(2, time_clock, we.Pos(9,4,0), 5)
              ]

    forklifts = [we.Forklift(0,time_clock, we.Pos(9,0,0)),
                 we.Forklift(1, time_clock, we.Pos(9,0,0)) ]

    orders = []
    order_no = 0

    #order 생성
    for i in range(len(aisles)):# i = aisle 번호
        for j in range(2):
            #no, pos, aisle_no, truck_no
            pos = we.Pos(aisles[i].pos.x, aisles[i].pos.y + 1 + j, 1) # x, y, z
            aisle_no = i # np.random.randint(0,len(aisles))
            order = we.Order(order_no, pos, aisles[aisle_no], 1) #i번 aisle에 truck_no 기준 order
            order_no += 1
            orders.append(order)
            #print('> Order create:', order)

    #time_clock, size, docks,  aisles, forklifts
    env = we.Warehouse(time_clock, size, docks, aisles, forklifts)
    env.set_orders(orders)

    return env


''' 테스트용 코드, 엑셀로 계산한 기대값과 동일한지 확인
'''
def make_test_env_o60_f2():
    time_clock = we.SimulationTimeClock() # 해당 창고내에서는 공유해야할 Time
    size = (10,10) #창고 사이즈 (Grid 구조가정)
    docks = [we.Dock(0, we.Pos(0,0,0)),
             we.Dock(1, we.Pos(9,0,0))  ]
    aisles = [we.Aisle(0, time_clock, we.Pos(0,4,0), 5),
              we.Aisle(1, time_clock, we.Pos(5,4,0), 5),
              we.Aisle(2, time_clock, we.Pos(9,4,0), 5)
              ]

    forklifts = [we.Forklift(0,time_clock, we.Pos(9,0,0)),
                 we.Forklift(1, time_clock, we.Pos(9,0,0))
                ]

    orders = []
    order_no = 0

    #order 생성
    for i in range(len(aisles)):# i = aisle 번호
        for j in range(20):
            #no, pos, aisle_no, truck_no

            add_y = j % 5
            pos = we.Pos(aisles[i].pos.x, aisles[i].pos.y + 1 + add_y, 1) # x, y, z
            aisle_no = i # np.random.randint(0,len(aisles))
            order = we.Order(order_no, pos, aisles[aisle_no], 1) #i번 aisle에 truck_no 기준 order
            order_no += 1
            orders.append(order)
            #print('> Order create:', order)

    #time_clock, size, docks,  aisles, forklifts
    env = we.Warehouse(time_clock, size, docks, aisles, forklifts)
    env.set_orders(orders)

    return env

def make_test_env_o60_f3():
    time_clock = we.SimulationTimeClock() # 해당 창고내에서는 공유해야할 Time
    size = (10,10) #창고 사이즈 (Grid 구조가정)
    docks = [we.Dock(0, we.Pos(0,0,0)),
             we.Dock(1, we.Pos(9,0,0))  ]
    aisles = [we.Aisle(0, time_clock, we.Pos(0,4,0), 5),
              we.Aisle(1, time_clock, we.Pos(5,4,0), 5),
              we.Aisle(2, time_clock, we.Pos(9,4,0), 5)
              ]

    forklifts = [we.Forklift(0,time_clock, we.Pos(0,0,0)),
                 we.Forklift(1, time_clock, we.Pos(5,0,0)),
                 we.Forklift(2, time_clock, we.Pos(9, 0, 0)),
                 ]

    orders = []
    order_no = 0

    #order 생성
    for i in range(len(aisles)):# i = aisle 번호
        for j in range(20):
            #no, pos, aisle_no, truck_no

            add_y = j % 5
            pos = we.Pos(aisles[i].pos.x, aisles[i].pos.y + 1 + add_y, 1) # x, y, z
            aisle_no = i # np.random.randint(0,len(aisles))
            order = we.Order(order_no, pos, aisles[aisle_no], j % 2 ) #i번 aisle에 truck_no 기준 order
            order_no += 1
            orders.append(order)
            #print('> Order create:', order)

    #time_clock, size, docks,  aisles, forklifts
    env = we.Warehouse(time_clock, size, docks, aisles, forklifts)
    env.set_orders(orders)

    return env


def make_test_env_o12_f3():
    time_clock = we.SimulationTimeClock() # 해당 창고내에서는 공유해야할 Time
    size = (10,10) #창고 사이즈 (Grid 구조가정)
    docks = [we.Dock(0, we.Pos(0,0,0)),
             we.Dock(1, we.Pos(9,0,0))  ]
    aisles = [we.Aisle(0, time_clock, we.Pos(0,4,0), 5),
              we.Aisle(1, time_clock, we.Pos(5,4,0), 5),
              we.Aisle(2, time_clock, we.Pos(9,4,0), 5)
              ]

    forklifts = [we.Forklift(0,time_clock, we.Pos(0,0,0)),
                 we.Forklift(1, time_clock, we.Pos(5,0,0)),
                 we.Forklift(2, time_clock, we.Pos(9, 0, 0)),
                 ]

    orders = []
    order_no = 0

    #order 생성
    for i in range(len(aisles)):# i = aisle 번호
        for j in range(4):
            #no, pos, aisle_no, truck_no

            add_y = j % 5
            pos = we.Pos(aisles[i].pos.x, aisles[i].pos.y + 1 + add_y, 1) # x, y, z
            aisle_no = i # np.random.randint(0,len(aisles))
            order = we.Order(order_no, pos, aisles[aisle_no], j % 2 ) #i번 aisle에 truck_no 기준 order
            order_no += 1
            orders.append(order)
            #print('> Order create:', order)

    #time_clock, size, docks,  aisles, forklifts
    env = we.Warehouse(time_clock, size, docks, aisles, forklifts)
    env.set_orders(orders)

    return env


def test_warehouse_01_basic():
    env = make_test_warehouse_env_01()
    expected_value = 84
    policy = p.BasicPolicy()
    we.execute(env, policy)
    print_result(env, policy)


def test_warehouse_01_random():
    env = make_test_warehouse_env_01()
    expected_value = None
    policy = p.RandomPolicy()
    we.execute(env, policy)
    print_result(env, policy)


def test_warehouse_01_greedy():
    env = make_test_warehouse_env_01()
    expected_value = None
    policy = p.GreedyPolicy()
    we.execute(env, policy)
    print_result(env, policy)


def test_warehouse_01_mcts():
    env = make_test_warehouse_env_01()
    expected_value = None
    policy = p.MCTSPolicy()
    we.execute(env, policy)
    print_result(env, policy)


def test_warehouse_60_mcts():
    env = make_test_env_o60_f2() #order 60개기준
    expected_value = None
    policy = p.MCTSPolicy()
    we.execute(env, policy)
    print('Expected value=', 835)
    print_result(env, policy)


def test_warehouse_60_random():
    env = make_test_env_o60_f2() #order 60개기준
    expected_value = None
    policy = p.RandomPolicy()
    we.execute(env, policy)
    print_result(env, policy)

def test_warehouse_60_greedy():
    env = make_test_env_o60_f2() #order 60개기준
    expected_value = None
    policy = p.GreedyPolicy()
    we.execute(env, policy)
    print_result(env, policy)


def test_warehouse_60_greedy_f3():
    env = make_test_env_o60_f3() #order 60개기준
    expected_value = None
    policy = p.GreedyPolicy()
    we.execute(env, policy)
    print_result(env, policy)


def test_warehouse_60_random_f3():
    env = make_test_env_o60_f3() #order 60개기준
    expected_value = None
    policy = p.RandomPolicy()
    we.execute(env, policy)
    print_result(env, policy)


def test_warehouse_60_mcts_f3():
    env = make_test_env_o60_f3() #order 60개기준
    policy = p.MCTSPolicy()
    #policy.max_iteration = 200
    we.execute(env, policy)
    print_result(env, policy)

def test_warehouse_60_mcts_f3_m200():
    env = make_test_env_o60_f3() #order 60개기준
    policy = p.MCTSPolicy()
    policy.max_iteration = 200
    we.execute(env, policy)
    print_result(env, policy)


def test_warehouse_12_random_f3():
    env = make_test_env_o12_f3()
    policy = p.RandomPolicy()
    we.execute(env, policy)
    print_result(env, policy)


def test_warehouse_12_mcts_f3():
    env = make_test_env_o12_f3()
    policy = p.MCTSPolicy()
    policy.print_node_flag = True
    we.execute(env, policy)
    print_result(env, policy)


def print_result(env, policy):

    print('**' * 30)
    print('[Result]',policy)
    print('Finish time clock value=', env.finish_time_clock,':uncompleted orders=', len(env.available_orders))
    total_waiting = 0
    for f in env.forklifts:
        print('F', f.no, ' waiting time=', f.waiting_time)
        total_waiting += f.waiting_time
    print('Total waiting time=', total_waiting)




if __name__ == '__main__':
    #test_warehouse_01()
    #test_warehouse_02()
    #test_warehouse_03()
    #test_warehouse_04()
    #test_warehouse_60_mcts()
    #test_warehouse_60_random()
    #test_warehouse_60_greedy()
    test_warehouse_60_mcts_f3()  #576
    test_warehouse_60_mcts_f3_m200() #568
    #test_warehouse_60_greedy_f3()
    #test_warehouse_60_random_f3()
    #test_warehouse_12_random_f3()
    #test_warehouse_12_mcts_f3()




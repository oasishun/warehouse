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


def test_warehouse_01():
    env = make_test_warehouse_env_01()
    expected_value = 84
    policy = BasicPolicy()
    we.execute(env, policy, expected_value)
    print('**' * 30)


def test_warehouse_02():
    env = make_test_warehouse_env_01()
    expected_value = None
    policy = RandomPolicy()
    we.execute(env, policy, expected_value)
    print('**' * 30)

def test_warehouse_03():
    env = make_test_warehouse_env_01()
    expected_value = None
    policy = GreedyPolicy()
    we.execute(env, policy, expected_value)
    print('**' * 30)


########################################################################################################################


if __name__ == '__main__':
    #test_warehouse_01()
    #test_warehouse_02()
    test_warehouse_03()



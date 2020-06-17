import warehouse as we
import policy as p
import test_warehouse as t
import sys
import time

def permutation(arr):
    if len(arr) == 1:
        return [arr]

    perm_list = []  # resulting list
    for order in arr:
        remaining_elements = [x for x in arr if x != order]
        z = permutation(remaining_elements)  # permutations of sublist

        for t in z:
            # clone을 생성하여 붙여넣는다.
            perm_list.append([order] + t)

    return perm_list


def getInitialSeq(size):
    seq_arr = []
    for i in range(0, size):
        seq_arr.append(i)
    return seq_arr


def test_warehouse_full_search():


    #6개 order
    #env = t.make_test_warehouse_env_01()

    #12개 order
    env = t.make_test_env_o9_f3() # 9! =     362,880  <-- 354초 소요됨
    #env = t.make_test_env_o12_f3  #12! = 479,001,600  <--
    #env = t.make_test_env_o10_f3()  #10! =   3,628,800  <--3540초 (약1시간)

    # 초기 order seq 생성
    initial_seq = getInitialSeq(len(env.orders))
    print('initial seq=', initial_seq)

    # 순열 생성
    order_seq_permutation = permutation(initial_seq)
    #print('order_seq_permutation=', order_seq_permutation)

    # 실행 후 결과값 정의
    max_order_seq = []
    max_reward = sys.maxsize * -1
    uncompleted_orders = []

    # 생성된 순열에 대해 모두 실행

    size = len(order_seq_permutation)

    for i in range(size):

        # env, orders copy
        clone_env = env.copy()
        clone_orders = clone_env.orders.copy()

        curr_order_seq = order_seq_permutation.pop(0)

        if i > 0 and i % 100 == 0:
            print(i, ':curr_order_seq=', curr_order_seq)

        curr_orders = []
        for seq in curr_order_seq:
            curr_orders.append(clone_orders[seq])

        sequentail_policy = p.SequentialPolicy(curr_orders)
        we.execute(clone_env, sequentail_policy)
        reward = 0 - clone_env.finish_time_clock

        if max_reward < reward:
            max_reward = reward
            max_order_seq = curr_order_seq
            uncompleted_orders = clone_env.available_orders

    print('[Result]')
    print('Order Sequnce=', max_order_seq)
    print('Finish time clock value=', max_reward * -1, ':uncompleted orders=', len(uncompleted_orders))


if __name__ == '__main__':
    start_time = time.time() #시간측정용

    test_warehouse_full_search()

    end_time = time.time()  # 시간측정용
    print('[Engine Running time] =', (end_time - start_time), ' second')


import numpy as np
import environment as we

########################################################################################################

MAX_DISTANCE = 10**40

class BasicPolicy:

    def __repr__(self):
        return 'BasicPolicy'

    def get_action(self, env, state):
        orders = env.available_orders

        forklift = None
        order = None

        if len(orders) > 0:
            for f in env.forklifts:
                if f.order == None:  # 가용한 지게차가 있는 경우
                    forklift = f
                    # 순서대로 선택하는 방식
                    order = orders[0]
                    break

        return we.Action(forklift, order)

########################################################################################################

class RandomPolicy:

    def __repr__(self):
        return 'RandomPolicy'

    def get_action(self, env, state):
        orders = env.available_orders

        forklift = None
        order = None

        if len(orders) > 0:
            for f in env.forklifts:
                if f.order == None:  # 가용한 지게차가 있는 경우
                    forklift = f
                    #Random 하게 선택하는 방식
                    order = np.random.choice(orders)
                    break

        return we.Action(forklift, order)


########################################################################################################

class GreedyPolicy:
    def __repr__(self):
        return 'GreedyPolicy'

    def get_action(self, env, state):
        orders = env.available_orders
        forklift = None
        order = None

        if len(orders) > 0:
            min_distance = MAX_DISTANCE

            for f in env.forklifts:
                if f.order == None:  # 가용한 지게차가 있는 경우
                    #지게차와 가장 가까운 곳의 선반쪽 선택
                    temp_order, temp_distance = self.get_nearest_order(f.pos, orders)

                    if temp_distance < min_distance:
                        forklift = f
                        order = temp_order

        return we.Action(forklift, order)


    def get_nearest_order(self, from_pos, available_orders):

        nearest_order = None
        min_distance = MAX_DISTANCE

        for order in available_orders:
            dist = we.distance(from_pos, order.pos)

            if dist < min_distance:
                min_distance = dist
                nearest_order = order

        return (nearest_order, min_distance)


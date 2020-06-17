#policy.py

import warehouse as we
import numpy as np
import math



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

class FullSearchPolicy:

    def __repr__(self):
        return 'FullSearchPolicy'

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

class SequentialPolicy:
    def __init__(self, order_sequence):
        self.order_sequence = order_sequence


    def get_action(self, env, state):

        #순차적으로 order를 배분함
        forklift = None
        order = None

        if len(self.order_sequence) > 0:
            for f in env.forklifts:
                if f.order == None:  # 가용한 지게차가 있는 경우
                    forklift = f
                    #Random 하게 선택하는 방식
                    order = self.order_sequence[0]
                    self.order_sequence.remove(order)
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

#######################################################################################################################
class Node:
    def __init__(self, root, parent, orders, order_no, forklift):

        if root == None:
            self.root = self
            self.depth = 0
            self.order_no = -1
            self.order_no_sequence = []
        else:
            self.root = root
            self.depth = parent.depth + 1
            self.order_no = order_no
            self.order_no_sequence = parent.order_no_sequence + [order_no]

        self.parent = parent
        self.children = []
        self.orders = orders.copy()
        self.forklift = forklift
        self.visits = 0
        self.total_reward = 0
        self.avg_reward = 0
        self.ucb = 0

    def __repr__(self):
        return 'depth=' + str(self.depth) + ',order_no=' + str(self.order_no)

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def remove_order_no(self, order_no):
        for order in self.orders:
            if order.no == order_no:
                self.orders.remove(order)
                break


    def get_avg_reward(self):

        if self.visits == 0:
            return 0

        self.avg_reward = (self.total_reward / self.visits)

        return self.avg_reward


    def select_node(self, forklift):
        if len(self.children) == 0: #미방문 노드
            # self.expand_node(forklift)
            # selected_node = np.random.choice(self.children)
            # print('leaf found:', self.order)
            return self
        else:
            #child  node들 점수 비교
            #print('compare UCB')
            children_sorted = sorted(self.children, key=lambda x: x.ucb)
            selected_node = children_sorted[-1]

            return selected_node.select_node(forklift)

    def expand_node(self, forklift):
        for order in self.orders:
            child_order_list = self.orders.copy()
            child_order_list.remove(order)

            ################available 은 모두 할수 있는 상태이고... child 만드는 것은 제한이 필요함

            child = Node(self.root, self, child_order_list, order.no, forklift)
            self.add_child(child)

        if len(self.children) > 0:
            expanded_node = np.random.choice(self.children)
        else:
            expanded_node = self

        return expanded_node


    def back_propagate(self, reward):
        #print('back_propagate:')
        self.visits += 1
        self.total_reward += reward

        if self.parent != None:
            self.recalcuate_upper_confidence_bound()
            self.parent.back_propagate(reward)

    def recalcuate_upper_confidence_bound(self):
        exploration_constant = 2 #적절한 수준의 값으로 조정 필요함: 2, 20
        avg = (self.total_reward / self.visits)
        deviation = math.sqrt(math.log(self.parent.visits + 1) / self.visits )

        self.ucb = avg  + (exploration_constant * deviation)

        return self.ucb

    def print_node(self):
        print(self.order_no_sequence,':v=', self.visits, ',total_reward=', self.total_reward,',avg_reward=',
              self.get_avg_reward(),',UCB=', self.ucb)

        for child in self.children:
            child.print_node()

    def get_max_reward_child(self):

        max_value = self.children[0].get_avg_reward()
        max_child = self.children[0]

        for child in self.children:
            if child.get_avg_reward() > max_value:
                max_child = child
                max_value = child.get_avg_reward()
            elif child.get_avg_reward() == max_value:
                if child.visits > max_child.visits:
                    max_child = child
                    max_value = child.get_avg_reward()

        return max_child


class MCTSPolicy:
    def __init__(self):
        self.max_iteration = 100
        self.initial_env = None
        self.print_node_flag = False
        self.root = None

    def __repr__(self):
        return 'MCTSPolicy'

    def exeucte_mcts(self, env, state, forklift):
        self.root = Node(None, None, env.available_orders, None, None)

        if state != None:
            for order in state.order_history:
                self.root.order_no_sequence.append(order.no)
                self.root.remove_order_no(order.no)

        count = 0
        while count < self.max_iteration :#(1 + 10 * (len(env.available_orders) - 1)) :
            count += 1

            # 1. selection & expansion
            selected_node = self.root.select_node(forklift)

            # 2. expansion
            expanded_node = selected_node.expand_node(forklift)

            # 3. rollout
            reward = self.rollout(env, expanded_node)

            # 4. backpropagation
            expanded_node.back_propagate(reward)

        # root node 하위 중에 reward가 최대인 것
        max_child = self.root.get_max_reward_child()
        mcts_order = env.get_order_by_no(max_child.order_no)

        print('>>>>>>>>>> ORDER=', max_child.order_no, ',forklift=', forklift.no)

        if self.print_node_flag:
            self.root.print_node()

        return mcts_order


    def get_action(self, env, state):
        if self.initial_env is None:
            self.initial_env = env.copy()

        forklift = None
        mcts_order = None
        copied_order = None

        if len(env.available_orders) > 0:
            for f in env.forklifts:
                if f.order is None:  # 가용한 지게차가 있는 경우
                    forklift = f
                    copied_order = self.exeucte_mcts(self.initial_env, state, forklift)
                    mcts_order = env.get_order_by_no(copied_order.no)
                    break

        return we.Action(forklift, mcts_order)

    def rollout(self, env, node):
        clone_env = env.copy() #초기 상태를 복사해서 실행
        #Order의 순서는 현재 상태까지 상태 사용, 나머지는 random 정렬 (fast roll out)
        pre_order_sequence = []
        random_order_sequence = clone_env.orders.copy()

        for order_no in node.order_no_sequence:
            order = clone_env.get_order_by_no(order_no)
            random_order_sequence.remove(order)
            pre_order_sequence.append(order)

        np.random.shuffle(random_order_sequence)
        order_sequence = pre_order_sequence + random_order_sequence

        sequentail_policy = SequentialPolicy(order_sequence)

        we.execute(clone_env, sequentail_policy)
        reward = 0 - clone_env.finish_time_clock

        return reward

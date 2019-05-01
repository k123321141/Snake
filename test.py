import time
import sys
import random
from threading import Thread, Lock
from utils import getch
from collections import deque

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter([self.x, self.y])

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    def __hash__(self):
        return 10723 * self.x.__hash__() + self.y.__hash__()

    def __str__(self):
        return str([self.x, self.y])

class UI:
    def __init__(self, width, height):
        # width, height : int
        self.width = width
        self.height = height
        self.table = [[' ']*width for y in range(height)]
        self.wall_token = '1'
        self.body_token = 'o'
        self.head_token = 'O'
        self.dot_token = 'x'

    def draw_snake(self, body):
        for i, (x, y) in enumerate(body):
            if i == 0:
                self.table[y][x] = 'O'
            else:
                self.table[y][x] = 'o'

    def draw_dots(self, dots):
        for i, (x, y) in enumerate(dots):
            self.table[y][x] = self.dot_token

    def refresh(self):
        for y in range(self.height):
            for x in range(self.width):
                self.table[y][x] = ' '
        #         4 wall
        for y in range(self.height):
            self.table[y][0] = self.wall_token
            self.table[y][-1] = self.wall_token
        for x in range(self.width):
            self.table[0][x] = self.wall_token
            self.table[-1][x] = self.wall_token

    def draw_ui(self, snake, dots, length):
        ret = ''
        self.refresh()
        self.draw_snake(snake)
        self.draw_dots(dots)

        for h in range(self.height):
            ret += (''.join([x for x in self.table[h]])) + '\r\n'
        # game info
        ret += 'current length : %3d\r\n' % length
        print(ret)


class Key_input:
    def __init__(self, direction):
        self.key = direction 


class Game:
    def __init__(self, width, height):
        self.key_input = Key_input('left')
        self.lock = Lock()
        self.period = 0.1
        self.listen_period = 0.0001
        self.width = width
        self.height = height
        self.threshold = 5 
        # body position
        self.body = deque()
        # init body
        self.len = 10
        for i in range(self.len):
            point = Point(width//2 + i, height//2)
            self.body.append(point)
    
        self.dots = set([Point(width // 2, width // 2+1)])

        self.direction = self.key_input.key
        self.pre_direction = 'None'
        self.ui = UI(width, height)

    def start_listen(self):
        def _listen(period, lock, var):
            arrow_input = {
                            'w': 'up',
                            's': 'down',
                            'a': 'left',
                            'd': 'right',
                            'q': 'quit',
                          }
            try:
                while True:
                    time.sleep(period)
                    char = getch()
                    if char in arrow_input:
                        lock.acquire()
                        var.key = arrow_input[char]
                        lock.release()
            except Exception:
                print('exit listen thread.')
                # shut down cleanly

        Thread(target=_listen, args=(self.listen_period, self.lock, self.key_input)).start()

    def generate_dot(self):
        while (self.width-1) * (self.height-1) - self.len > 0:
            random_x = random.randint(1+self.threshold, self.width-2-self.threshold)
            random_y = random.randint(1+self.threshold, self.height-2-self.threshold)
            dot = Point(random_x, random_y)
            if dot in self.dots:
                continue
            else:
                self.dots.add(dot)
                break

    def eating_dot(self, head, tail):
        if head in self.dots:
            self.dots.remove(head)
            self.body.append(tail)
            self.len += 1
            self.generate_dot()
            self.period = max(0.2 - (0.01*self.len), 0.02)

    def check_dead(self):
        # hit the walls
        x, y = self.body[0]
        if x == 0 or x == self.width-1:
            return True
        elif y == 0 or y == self.height-1:
            return True
        # hit the body
        for i, (x_, y_) in enumerate(self.body):
            if x == x_ and y == y_ and i > 0:
                return True
        return False

    def game_start(self):
        self.start_listen()
        while True:
            time.sleep(self.period)
            # check head direction
            self.lock.acquire()
            self.direction = self.key_input.key
            self.lock.release()
#             quit the game
            if self.direction == 'quit':
                print('Quit the Game.')
                sys.stdin.close()
                break
            # check direction is valid
            if self.direction == 'left' and self.pre_direction == 'right' or \
                    self.direction == 'right' and self.pre_direction == 'left' or \
                    self.direction == 'up' and self.pre_direction == 'down' or \
                    self.direction == 'down' and self.pre_direction == 'up':
                self.direction = self.pre_direction
            else:
                self.pre_direction = self.direction
    #         move head
            x, y = head = self.body[0]
            tail = self.body.pop()
            if self.direction == 'left':
                new_head = Point(x-1, y)
            elif self.direction == 'right':
                new_head = Point(x+1, y)
            elif self.direction == 'up':
                new_head = Point(x, y-1)
            elif self.direction == 'down':
                new_head = Point(x, y+1)
            self.body.appendleft(new_head)
            # eat dot
            self.eating_dot(new_head, tail)
            self.ui.draw_ui(self.body, self.dots, self.len)
            if self.check_dead():
                print('GAME OVER')
                sys.stdin.close()
                break


if __name__ == '__main__':
    try:
        g = Game(30, 30)
        g.game_start()
    except Exception as e:
        sys.stdin.close()
        raise e

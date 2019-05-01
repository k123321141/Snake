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

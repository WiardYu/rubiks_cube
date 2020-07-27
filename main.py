import console, os

color = {
    1: '\033[1;34;40m■\033[0m',
    2: '\033[1;32;40m■\033[0m',
    3: '\033[1;35;40m■\033[0m',
    4: '\033[1;31;40m■\033[0m',
    5: '\033[1;33;40m■\033[0m',
    6: '\033[1;37;40m■\033[0m'}

# 初始化魔方，cube=[前,后,左,右,上,下]
cube = [
    [1,1,1,1,1,1,1,1,1], # 前蓝
    [2,2,2,2,2,2,2,2,2], # 后绿
    [3,3,3,3,3,3,3,3,3], # 左橙
    [4,4,4,4,4,4,4,4,4], # 右红
    [5,5,5,5,5,5,5,5,5], # 上黄
    [6,6,6,6,6,6,6,6,6]] # 下白


def show_cube(cube):
    '''显示魔方“上下左右前”五个面'''
    print('依次为 前 后 左 右 上 下:')
    for c in cube:
        for i, j in enumerate(c):
            if (i+1)%3 == 0:
                print(color[j])
            else:
                print(color[j], end='')
        print('')


def surface_rotate(l, times=1, direction=1):
    '''旋转表面的九个颜色，
    times控制次数，默认等于1旋转90度，2旋转180度，
    direction控制方向，默认等于1为顺时针，0为逆时针。'''

    one_time = [(0, 2), (0, -1), (0, -3), (1, 3), (3, -2), (-2, -4)]
    two_times = [(0, -1), (1, -2), (2, -3), (3, -4)]

    if times == 1:
        index = one_time
    else:
        index = two_times

    if not direction:
        index.reverse()
    for i, j in index:
        l[i], l[j] = l[j], l[i]


def whole_rotate(cube, cmd):
    '''旋转魔方整体，
    cmd=['x', 在右方看向魔方并顺时针转动整个魔方
         'x!', 逆时针的x
         'y', 在上方看向魔方并顺时针转动整个魔方
         'y!', 逆时针的y
         'z', 在前方看向魔方并顺时针转动整个魔方
         'z!', 逆时针的z
         'o'] 使魔方背面朝前（两个y）
    '''

    # 背面朝前
    if cmd == 'o':
        # 左右侧交换
        cube[2], cube[3] = cube[3], cube[2]
        # 前后交换
        cube[0], cube[1] = cube[1], cube[0]
        # 上下面旋转180度
        surface_rotate(cube[4], 2)
        surface_rotate(cube[5], 2)

    # 左面朝前
    elif cmd == 'y!':
        index = [(0, 3), (0, 1), (0, 2)]
        for i, j in index:
            cube[i], cube[j] = cube[j], cube[i]
        # 逆时针旋转顶面
        surface_rotate(cube[4], 1, 0)
        # 顺时针旋转底面
        surface_rotate(cube[5], 1, 1)

    # 右面朝前
    elif cmd == 'y':
        index = [(0, 2), (0, 1), (0, 3)]
        for i, j in index:
            cube[i], cube[j] = cube[j], cube[i]
        # 顺时针旋转顶面
        surface_rotate(cube[4], 1, 1)
        # 逆时针旋转底面
        surface_rotate(cube[5], 1, 0)

    # 上面朝前
    elif cmd == 'x!':
        index = [(0, 5), (0, 1), (0, 4)]
        for i, j in index:
            cube[i], cube[j] = cube[j], cube[i]
        surface_rotate(cube[1], 2)
        surface_rotate(cube[4], 2)
        # 顺时针旋转左面
        surface_rotate(cube[2], 1, 1)
        # 逆时针旋转右面
        surface_rotate(cube[3], 1, 0)

    # 下面朝前
    elif cmd == 'x':
        index = [(0, 4), (0, 1), (0, 5)]
        for i, j in index:
            cube[i], cube[j] = cube[j], cube[i]
        surface_rotate(cube[1], 2)
        surface_rotate(cube[5], 2)
        # 逆时针旋转左面
        surface_rotate(cube[2], 1, 0)
        # 顺时针旋转右面
        surface_rotate(cube[3], 1, 1)


def rotate_front_layer(cube, direction=1):
    '''转动前面第一层，
    direction控制方向，默认等于1为顺时针，0为逆时针。'''
    face_index = [
        [(2, 4), [(2, 8), (5, 7), (8, 6)]],
        [(2, 3), [(2, 6), (5, 3), (8, 0)]],
        [(2, 5), [(2, 0), (5, 1), (8, 2)]]
        ]
    if not direction:
        face_index.reverse()
    # 旋转表面
    surface_rotate(cube[0], 1, direction)
    # 旋转周围块
    for idx in face_index:
        f_1, f_2 = idx[0]
        for clr_1, clr_2 in idx[1]:
            cube[f_1][clr_1], cube[f_2][clr_2] = cube[f_2][clr_2], cube[f_1][clr_1]


def rules(cube, cmd):
    '''使魔方可以使用常规规则操作
    cmd=['L', 'L!', 
         'R', 'R!', 
         'U', 'U!', 
         'D', 'D!', 
         'F', 'F!', 
         'B', 'B!']'''

    cmd_dict = {
        'L': ['y!', 1, 'y'],
        'L!': ['y!', 0, 'y'],
        'R': ['y', 1, 'y!'],
        'R!': ['y', 0, 'y!'],
        'U': ['x!', 1, 'x'],
        'U!': ['x!', 0, 'x'],
        'D': ['x', 1, 'x!'],
        'D!': ['x', 0, 'x!'],
        'F': ['', 1, ''],
        'F!': ['', 0, ''],
        'B': ['o', 1, 'o'],
        'B!': ['o', 0, 'o']
    }
    func_list = [whole_rotate, rotate_front_layer, whole_rotate]
    cmd_list = cmd_dict[cmd]
    for i in range(3):
        func_list[i](cube, cmd_list[i])


# main
formula = 'B! U L! U! B! R! F! D! L F L F U U L U U L! B B U L L U L! B! D! B L L F F L L'
f_list = formula.split(' ')
os.system('cls')
#show_cube(cube)
for f in f_list:
    rules(cube, f)

show_cube(cube)

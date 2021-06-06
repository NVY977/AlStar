import pygame as pg
from heapq import *


# Функция для формирования окружностей
def get_circle(x, y):
    return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 4


# Функция для определения соседних клеток
def get_neighbours(x, y):
    # Не вылезали за границы экрана, а также не должно быть препятствий
    check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1] , [-1, -1], [1, -1], [1, 1], [-1, 1]
    # Возвращаем справа,слева,вверху и внизу
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]


# Функция определяющая клик нашей мышки
def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.circle(sc, pg.Color('magenta'), *get_circle(grid_x, grid_y))  # Изображаем круг, которым водим
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


# В качестве эвристики выбираем манхетонское расстояние
# Суть: Расстояние городских кварталов  d_{1} между двумя векторами {a} ,{b}  в n-мерном вещественном
# векторном пространстве с заданной системой координат — сумма длин проекций отрезка между точками на оси координат.
def heuristic(a, b):
    # Движемся в 4 направления
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def dijkstra(start, goal, graph):
    queue = []  # Общая очередь
    # Кучи реализуют приоритетную очередь
    heappush(queue, (0, start))  # Добавляем в кучу heap
    cost_visited = {start: 0}  # Задаем словарь, чтобы следить за общей стоимостью из начальной вершины
    visited = {start: None}
    while queue:
        cur_cost, cur_node = heappop(queue)  # Вынимаем вершину и стоимость из кучи с минимальной ценной
        if cur_node == goal:
            break
        neighbours = graph[cur_node]
        # Для всех новых вершин
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            # Новая цена
            new_cost = cost_visited[cur_node] + neigh_cost
            # Если в словаре нет пути до нее или новая цена меньше, чем предыдущая
            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                #  Формируем приоритет для вершины добавляя к цене пути значение эвристики
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))  # Заносим вершину в очередь со значением приоритета
                cost_visited[neigh_node] = new_cost  # Обновили цену
                visited[neigh_node] = cur_node  # Пишем что пришли к этой вершине из текущей
    return visited


cols, rows = 23, 13
TILE = 70
# Создадим сетку
pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
# set grid
grid = ['22222222222222222222212',
        '22222292222911112244412',
        '22444422211112911444412',
        '24444444212777771444912',
        '24444444219777771244112',
        '92444444212777791192144',
        '22229444212777779111144',
        '11111112212777772771122',
        '27722211112777772771244',
        '27722777712222772221244',
        '22292777711144429221244',
        '22922777222144422211944',
        '22222777229111111119222']
grid = [[int(char) for char in string] for string in grid]  # Преобразовали в инт
# Сформируем наш граф согласно сетки
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        # Проходимся по массиву клеток и для каждой определяем соседей
        graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y)

# Начальные позици и создали очередь, которую засунули в кучу
start = (0, 7)
goal = start
queue = []
heappush(queue, (0, start))
visited = {start: None}
# Бэкграунд
bg = pg.image.load('../img/2.png').convert()
bg = pg.transform.scale(bg, (cols * TILE, rows * TILE))  # Установили под наше разрешение
while True:
    sc.blit(bg, (0, 0))  # Сделали фоном
    # Считали клик закинули в дейкстру
    mouse_pos = get_click_mouse_pos()
    if mouse_pos:
        visited = dijkstra(start, mouse_pos, graph)
        goal = mouse_pos

    # Рисуем путь от начала до нашей цели
    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        pg.draw.circle(sc, pg.Color('white'), *get_circle(*path_segment))
        path_segment = visited[path_segment]
    pg.draw.circle(sc, pg.Color('red'), *get_circle(*start))
    pg.draw.circle(sc, pg.Color('red'), *get_circle(*path_head))

    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(30)

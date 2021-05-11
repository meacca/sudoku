from itertools import product as prod
def solve(grid):
    # Количество строчек в одном квадрате
    S_N = int(len(grid)**0.5)
    # Количество строчек в таблице
    N = int(len(grid))

    # Соответствие между заполнением ячейки цифрой и ограничениями, которые в
    # результате выполняются
    available_actions = {}
    for r, c, n in prod(range(N), range(N), range(1, N + 1)):
        available_actions[(r, c, n)] = [
            # Заполнение ячейки таблицы
            ("cell", (r, c)),
            # Цифра в соответствующей строке
            ("row", (r, n)),
            # Цифра в соответствующей колонке
            ("column", (c, n)),
            # Цифра в соответствующем квадрате
            ("square", ((r // S_N) * S_N + (c // S_N), n))]

    # Требования которые должны выполняться для конечного решения задачи
    # Заполнение всех ячеек таблицы
    restrictions = {i: set() for i in [("cell", cell) for cell in prod(range(N), range(N))] +
         # В каждой строке должны присутствовать все цифры
         [("row", row) for row in prod(range(N), range(1, N + 1))] +
         # В каждой колонке должны присутствовать все цифры
         [("column", column) for column in prod(range(N), range(1, N + 1))] +
         # В каждом квадрате должны присутсвовать все цифры
         [("square", square) for square in prod(range(N), range(1, N + 1))]}

    # Соответствие между ограничениями на конечное решение и действиями,
    # приводящими к их удволетворению
    for act in available_actions:
        for restriction in available_actions[act]:
            restrictions[restriction].add(act)

    # Учет выполнения ряда ограничений в соответствии с частичной заполненностью таблицы
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != 0:
                set_value(restrictions, available_actions, (i, j, grid[i][j]))

    # Получение итератора со всеми возможными решениями
    for solution in get_recursive_solution(restrictions, available_actions, list()):
        for row, column, value in solution:
            grid[row][column] = value
        yield grid

# restrictions - cоответствие между ограничениями на конечное решение и действиями,
# приводящими к их удволетворению
# available_actions - cоответствие между действиями и ограничениями, которые в
# результате выполняются
# solution - список действий приводящих к решению
def get_recursive_solution(restrictions, available_actions, solution):
    if len(restrictions) > 0:
        # Получения ограничения с минимальным количеством действий для его удволетворения
        min_len = -1;
        for key, value in restrictions.items():
            if(len(restrictions[key]) < min_len or min_len == -1):
                min_len = len(restrictions[key])
                c = key
        # Перебор все возможных действий для удволетворения выбранного ограничения
        for r in restrictions[c].copy():
            acts = set_value(restrictions, available_actions, r)
            solution.append(r)
            for s in get_recursive_solution(restrictions, available_actions, solution):
                yield s
            solution.pop()
            unset_value(restrictions, available_actions, r, acts)
    # Все необходимые ограничения выполнены
    else:
        yield solution.copy()

# Выолнения действия по заполнению ячейки таблицы цифрой
def set_value(restrictions, available_actions, act):
    acts = []
    # Итерирование по выполняющимся ограничениям
    for j in available_actions[act]:
        # Итерирование по другим действиям, которые могли удовлетворить то же
        # ограничение, но теперь не возможны из-за правил судоку
        for i in restrictions[j]:
            # Удаление действий взимоисключающих с выбранным из возможных способов
            # удовлетворения оставшихся ограничений
            for k in available_actions[i]:
                if k != j:
                    restrictions[k].remove(i)
        # Удаление ограничения из словаря и сохранение списка действий, способных его выполнить
        acts.append(restrictions.pop(j))
    return acts

# Выполнения действия по очищению ячейки таблицы
def unset_value(restrictions, available_actions, act, acts):
    # Итерирование по ограничениям, которые удовлетворяло отмененное действие
    for j in available_actions[act][::-1]:
        # Возвращение ограничения и списка действий способных его выполнить
        restrictions[j] = acts.pop()
        # Добавление действий взимоисключающих с отмененным
        for i in restrictions[j]:
            for k in available_actions[i]:
                if k != j:
                    restrictions[k].add(i)

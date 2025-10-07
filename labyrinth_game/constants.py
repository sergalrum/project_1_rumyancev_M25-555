# labyrinth_game/constants.py

# Базовые параметры игры
ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта. Стены покрыты мхом. На полу лежит старый факел.',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None,
        'hidden_items': []
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.',
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': (
            'На пьедестале надпись: "Назовите число, которое идет после девяти". Введите ответ цифрой или словом.',
            '10'
        ),
        'hint': 'Подумайте о следующем числе после 9'
    },
    'trap_room': {
        'description': 'Комната с хитрой плиточной поломкой. На стене видна надпись: "Осторожно — ловушка".',
        'exits': {'west': 'entrance'},
        'items': ['rusty_key'],
        'puzzle': (
            'Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд (введите "шаг шаг шаг")',
            'шаг шаг шаг'
        ),
        'is_trapped': True
    },
    'library': {
        'description': 'Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ от сокровищницы.',
        'exits': {'east': 'hall', 'north': 'armory', 'west': 'chapel'},
        'items': ['ancient_book'],
        'puzzle': (
            'В одном свитке загадка: "Что растет, когда его съедают?" (ответ одно слово)',
            'резонанс'
        )
    },
    'armory': {
        'description': 'Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая шкатулка.',
        'exits': {'south': 'library'},
        'items': ['sword', 'bronze_box'],
        'puzzle': None
    },
    'treasure_room': {
        'description': 'Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.',
        'exits': {'south': 'hall'},
        'items': ['treasure_chest'],
        'puzzle': (
            'Дверь защищена кодом. Введите код (подсказка: это число пятикратного шага, 2*5= ? )',
            '10'
        ),
        'locked': True
    },
    'chapel': {
        'description': 'Древняя часовня. В центре — алтарь с горящими свечами. В воздухе витает запах ладана.',
        'exits': {'south': 'crypt', 'east': 'library'},
        'items': [],
        'puzzle': None
    },
    'crypt': {
        'description': 'Темный склеп с каменными саркофагами. Слышится капание воды.',
        'exits': {'north': 'chapel'},
        'items': [],
        'puzzle': None
    }
}

# Команды игры
COMMANDS = {
    'go <direction>': 'перейти в указанном направлении',
    'north': 'движение на север',
    'south': 'движение на юг',
    'east': 'движение на восток',
    'west': 'движение на запад',
    'look': 'осмотреть комнату',
    'take <item>': 'поднять предмет',
    'use <item>': 'использовать предмет',
    'use <item> on <target>': 'использовать предмет на объекте',
    'inventory': 'показать инвентарь',
    'hint': 'получить подсказку к загадке',
    'map': 'показать карту',
    'status': 'показать статус',
    'save': 'сохранить игру',
    'load': 'загрузить сохранение',
    'drop <item>': 'выбросить предмет',
    'examine <item>': 'осмотреть предмет',
    'combine <item1> <item2>': 'объединить предметы',
    'quit': 'выйти из игры',
    'help': 'показать список команд'
}

# Игровые параметры
GAME_SETTINGS = {
    'max_health': 100,
    'time_limit': 100,  # максимальное количество шагов
    'health_drain': 1,  # потеря здоровья за ход
    'trap_threshold': 3,  # максимальное количество ловушек
    'win_condition': ['treasure_chest', 'sword', 'rusty_key'],  # предметы для победы
    'starting_health': 100,
    'starting_energy': 100,
    'max_inventory_size': 10,
    'puzzle_attempts': 3,
    'save_limit': 3
}

# Секретные значения и коды
SECRETS = {
    'treasure_code': '1234',
    'hidden_passage': 'east wall',
    'master_key': 'golden_key',
    'emergency_exit': 'north_wall'
}

# Начальное состояние игры
INITIAL_STATE = {
    'current_room': 'entrance',
    'player_inventory': [],
    'steps_taken': 0,
    'health': GAME_SETTINGS['max_health'],
    'energy': GAME_SETTINGS['starting_energy'],
    'game_over': False,
    'traps_counter': 0,
    'hint_requested': False,  # флаг для подсказки
    'save_slots': {'slot1': None, 'slot2': None, 'slot3': None},
    'last_save': None,
    'puzzles_solved': 0,
    'items_collected': 0
}

# Сообщения об ошибках
ERROR_MESSAGES = {
    'no_item': 'Такого предмета нет в комнате',
    'no_room': 'Такой комнаты не существует',
    'no_command': 'Неизвестная команда',
    'locked': 'Дверь заперта',
    'empty_inventory': 'Ваш инвентарь пуст',
    'full_inventory': 'Инвентарь переполнен',
    'wrong_answer': 'Неверный ответ',
    'no_save_slot': 'Нет свободного слота для сохранения',
    'invalid_input': 'Неверный формат ввода'
}

# Успешные сообщения
SUCCESS_MESSAGES = {
    'item_taken': 'Предмет успешно взят',
    'puzzle_solved': 'Загадка решена!',
    'door_opened': 'Дверь открыта',
    'item_used': 'Предмет использован',
    'hint_received': 'Вы получили подсказку',
    'save_success': 'Игра успешно сохранена',
    'load_success': 'Игра успешно загружена'
}

# Визуальные элементы
VISUALS = {
    'health_bar': '█',
    'energy_bar': '░',
    'map_symbols': {
        'wall': '#',
        'door': 'D',
        'item': 'I',
        'player': 'P'
    }
}

# Система наград
REWARDS = {
    'puzzle_solved': 10,
    'item_found': 5,
    'trap_avoided': 15,
    'boss_defeated': 50
}
# labyrinth_game/player_actions.py


from . import constants, utils

#import re
#import random
#import json


# Вспомогательные функции (для внутренней логики)

def validate_command(command):
    """Проверка корректности команды."""
    if not command:
        return False
    if command.isdigit():
        print("Команды не могут состоять только из цифр.")
        return False
    return True

def get_input(prompt="> "):
    """Получает ввод от пользователя с обработкой ошибок."""
    try:
        user_input = input(prompt).strip()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    """Показывает содержимое инвентаря."""
    if game_state['player_inventory']:
        print("\nВаш инвентарь:")
        for item in game_state['player_inventory']:
            print(f"- {item}")
    else:
        print("Ваш инвентарь пуст.")

def take_item(game_state, item_name):
    """Позволяет игроку взять предмет."""
    current_room = constants.ROOMS[game_state['current_room']]
    
    if item_name in current_room['items']:
        game_state['player_inventory'].append(item_name)
        current_room['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """Использует предмет из инвентаря."""
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return
    
    match item_name:
        case 'torch':
            print("Факел освещает тёмные углы комнаты. Стало светлее!")
        case 'sword':
            print("Вы чувствуете себя увереннее с мечом в руках.")
        case 'bronze_box':
            if 'rusty_key' not in game_state['player_inventory']:
                print("Вы открываете бронзовую шкатулку и находите ржавый ключ!")
                game_state['player_inventory'].append('rusty_key')
            else:
                print("Шкатулка уже пуста.")
        case 'rusty_key':
            print("Ржавый ключ кажется важным, но пока некуда его применить.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")

def drop_item(game_state, item_name):
    """Позволяет игроку выбросить предмет."""
    if item_name in game_state['player_inventory']:
        game_state['player_inventory'].remove(item_name)
        current_room = constants.ROOMS[game_state['current_room']]
        current_room['items'].append(item_name)
        print(f"Вы бросили: {item_name}")
    else:
        print("У вас нет такого предмета.")

def examine_item(game_state, item_name):
    """Осматривает предмет более детально."""
    if item_name in game_state['player_inventory']:
        # Здесь можно добавить описания предметов
        match item_name:
            case 'torch':
                print("Старый факел, покрытый копотью. Кажется, ещё может гореть.")
            case 'sword':
                print("Поножи меч с выгравированными рунами на лезвии.")
            case 'bronze_box':
                print("Маленькая бронзовая шкатулка с замысловатым замком.")
            case _:
                print("Вы внимательно осматриваете предмет, \
                      но не находите ничего примечательного.")
    else:
        print("У вас нет такого предмета в инвентаре.")

def combine_items(game_state, item1, item2):
    """Комбинирует два предмета из инвентаря."""
    if item1 not in game_state['player_inventory'] \
            or item2 not in game_state['player_inventory']:
        print("У вас нет одного или обоих предметов.")
        return
    
    # Пример комбинации предметов
    if item1 == 'torch' and item2 == 'bronze_box':
        print("Вы соединяете факел с бронзовой шкатулкой, \
              создавая магический светильник!")
        game_state['player_inventory'].remove(item1)
        game_state['player_inventory'].remove(item2)
        game_state['player_inventory'].append('magic_lantern')
    else:
        print("Эти предметы нельзя комбинировать.")


# Основные действия игрока

def move_player(game_state, direction):
    """Обновленная функция перемещения игрока с проверкой ключа."""
    current_room = constants.ROOMS[game_state['current_room']]
    
    if direction in current_room['exits']:
        next_room = current_room['exits'][direction]
        
        # Проверка на комнату сокровищ
        if next_room == 'treasure_room':
            if 'rusty_key' in game_state['player_inventory']:
                print("Вы используете найденный ключ, \
                      чтобы открыть путь в комнату сокровищ.")
                game_state['current_room'] = next_room
                game_state['steps_taken'] += 1
                utils.describe_current_room(game_state)
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
        
        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1
        utils.describe_current_room(game_state)
        utils.random_event(game_state)  # Добавляем случайное событие
    else:
        print("Нельзя пойти в этом направлении.")

def solve_puzzle(game_state):
    """Улучшенная функция решения загадок с возможностью получения подсказки."""
    current_room_id = game_state.get('current_room')
    
    if not current_room_id:
        print("Ошибка: текущая комната не определена")
        return
    
    room = constants.ROOMS.get(current_room_id)
    
    if not room:
        print(f"Ошибка: комната '{current_room_id}' не найдена")
        return
    
    if not room.get('puzzle'):
        print("Загадок здесь нет.")
        return
    
    question, answer = room['puzzle']
    
    # Добавляем возможность получить подсказку
    if game_state.get('hint_requested'):
        hint = room.get('hint', "Подсказки нет для этой загадки.")
        print(f"\nПодсказка: {hint}")
        game_state['hint_requested'] = False  # сбрасываем флаг
        return
    
    print(f"\n{question}")
    user_answer = get_input("Ваш ответ: ")
    
    # Обработка альтернативных ответов
    if (user_answer.lower() == answer.lower() or 
        (answer.isdigit() and user_answer.lower() in ['один', 'два', 'три', \
                'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять', 'десять'])):
        print("Правильно! Вы решили загадку!")
        room['puzzle'] = None  # Загадка решена, удаляем её
        
        # Добавляем награду, зависящую от комнаты
        if 'reward' in room:
            for item in room['reward']:
                game_state['player_inventory'].append(item)
            print(f"Вы получили: {', '.join(room['reward'])}")
    else:
        print("Неверно. Попробуйте снова.")
    
    # Добавляем возможность запросить подсказку
    if room.get('hint'):
        ask_hint = input("Хотите получить подсказку? (да/нет): ").strip().lower()
        if ask_hint == 'да':
            game_state['hint_requested'] = True
            return
    
    # Проверка на ловушку в специальной комнате
    if game_state['current_room'] == 'trap_room':
        utils.trigger_trap(game_state)

def attempt_open_treasure(game_state):
    """Попытка открыть комнату сокровищ."""
    if game_state['current_room'] != 'treasure_room':
        print("Вы не в комнате сокровищ.")
        return
    
    if 'treasure_code' in game_state:
        user_input = input("Введите код для открытия сокровищницы: ")
        
        if user_input == game_state['treasure_code']:
            print("Сокровищница открылась!")
            # Логика получения награды
            reward = constants.ROOMS['treasure_room']['reward']
            game_state['player_inventory'].extend(reward)
            print(f"Вы нашли: {', '.join(reward)}")
        else:
            print("Неверный код! Попробуйте снова.")
    else:
        print("Кажется, здесь нужен особый код для открытия.")

def search_room(game_state):
    """Поиск предметов в комнате."""
    current_room = constants.ROOMS[game_state['current_room']]
    
    if not current_room['hidden_items']:
        print("В комнате больше нечего найти.")
        return
    
    found_items = current_room['hidden_items']
    current_room['hidden_items'] = []
    
    print(f"Вы нашли: {', '.join(found_items)}")
    game_state['player_inventory'].extend(found_items)

def listen_room(game_state):
    """Прослушивание комнаты на наличие звуков."""
    current_room = constants.ROOMS[game_state['current_room']]
    
    if 'sounds' in current_room:
        print(f"Вы слышите: {current_room['sounds']}")
    else:
        print("В комнате тихо.")

def use_item_on(game_state, item, target):
    """Использование предмета на определенном объекте."""
    if item not in game_state['player_inventory']:
        print(f"У вас нет {item} в инвентаре.")
        return
    
    current_room = constants.ROOMS[game_state['current_room']]
    
    if target not in current_room['objects']:
        print(f"В этой комнате нет {target}.")
        return
    
    # Пример логики использования предмета
    if item == 'torch' and target == 'altar':
        print("Вы зажигаете факел у алтаря. Свет озаряет комнату!")
        current_room['objects'][target] = 'lit_altar'
    
    elif item == 'rusty_key' and target == 'locked_door':
        print("Вы используете ключ, чтобы открыть дверь!")
        current_room['exits']['north'] = 'treasure_room'
        game_state['player_inventory'].remove('rusty_key')
    
    else:
        print(f"Нельзя использовать {item} на {target}.")

def use_key(game_state, key_name):
    """Использует ключ для открытия дверей или сундуков."""
    if key_name not in game_state['player_inventory']:
        print("У вас нет такого ключа.")
        return
    
    current_room = constants.ROOMS[game_state['current_room']]
    
    if key_name == 'rusty_key':
        if 'locked_door' in current_room['exits']:
            print("Вы открываете запертую дверь!")
            current_room['exits']['north'] = 'treasure_room'  # Пример разблокировки
            del current_room['exits']['locked_door']
        else:
            print("Здесь нет двери, которую можно открыть этим ключом.")
    else:
        print("Этот ключ не подходит ни к чему в этой комнате.")


# Обработка команд

def process_command(COMMANDS, game_state, command):
    """Обновленная обработка команд с расширенной логикой."""
    if not validate_command(command):
        return
    
    command_parts = command.lower().split()
    action = command_parts[0] if command_parts else ''
    args = command_parts[1:]
    
    try:
        match action:
            case 'go' | 'north' | 'south' | 'east' | 'west':
                # Обработка односложных команд движения
                direction = action if action \
                    in ['north', 'south', 'east', 'west'] else args[0]
                move_player(game_state, direction)
                
            case 'solve':
                # Специальная обработка в комнате сокровищ
                if game_state['current_room'] == 'treasure_room':
                    utils.attempt_open_treasure(game_state)
                else:
                    utils.solve_puzzle(game_state)
                    
            case 'look':
                utils.describe_current_room(game_state)
                
            case 'take':
                if len(args) != 1:
                    print("Пожалуйста, укажите предмет, который хотите взять")
                else:
                    take_item(game_state, args[0])
                    
            case 'use':
                if len(args) != 1:
                    print("Пожалуйста, укажите предмет, который хотите использовать")
                else:
                    use_item(game_state, args[0])
                    
            case 'inventory':
                show_inventory(game_state)
                
            case 'hint':
                    game_state['hint_requested'] = True
                    solve_puzzle(game_state)  # перевызов функции для показа подсказки
                
            case 'map':
                show_map(game_state)
                
            case 'status':
                check_status(game_state)
                
            case 'save':
                quick_save(game_state)
                
            case 'load':
                new_state = quick_load()
                if new_state:
                    game_state.update(new_state)
                    
            case 'drop':
                if len(args) != 1:
                    print("Пожалуйста, укажите предмет, который хотите выбросить")
                else:
                    drop_item(game_state, args[0])
                    
            case 'examine':
                if len(args) != 1:
                    print("Пожалуйста, укажите предмет для осмотра")
                else:
                    examine_item(game_state, args[0])
                    
            case 'combine':
                if len(args) != 2:
                    print("Пожалуйста, укажите два предмета для комбинирования")
                else:
                    combine_items(game_state, args[0], args[1])
                    
            case 'quit' | 'exit':
                print("До свидания! Спасибо за игру!")
                game_state['game_over'] = True
                
            case 'help':
                show_help(COMMANDS)
                
            case _:
                print("Неизвестная команда. Введите 'help' для списка команд.")
                
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

def handle_special_commands(game_state, command):
    """Обработка специальных команд."""
    if command.startswith('look at'):
        item = command.split('look at ')[1].strip()
        examine_item(game_state, item)
    
    elif command.startswith('use on'):
        parts = command.split('use ')
        if len(parts) > 1:
            item_target = parts[1].split(' on ')
            if len(item_target) > 1:
                item = item_target[0].strip()
                target = item_target[1].strip()
                use_item_on(game_state, item, target)
    
    elif command.startswith('search'):
        search_room(game_state)
    
    elif command.startswith('listen'):
        listen_room(game_state)

def show_help(COMMANDS):
    """Отображение списка доступных команд."""
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"{command:<16} - {description}")


# Управление состоянием игры

def update_game_state(game_state):
    """Обновление состояния игры после каждого хода."""
    # Обновление здоровья
    if 'health_drain' in game_state:
        game_state['health'] -= game_state['health_drain']
    
    # Увеличение счетчика шагов
    game_state['steps_taken'] += 1
    
    # Проверка условий
    check_game_conditions(game_state)
    
    # Случайные события
    utils.random_event(game_state)

def check_game_conditions(game_state):
    """Проверка условий победы/поражения."""
    if game_state.get('game_over'):
        return
    
    # Проверка на победу
    if 'win_condition' in game_state:
        required_items = game_state['win_condition']
        if all(item in game_state['player_inventory'] for item in required_items):
            print("\nПоздравляем! Вы собрали все необходимые предметы и победили!")
            game_state['game_over'] = True
            return
    
    # Проверка на поражение
    if game_state.get('health', 100) <= 0:
        print("\nВы погибли. Игра окончена.")
        game_state['game_over'] = True
        return
    
    # Дополнительные условия поражения
    if game_state.get('traps_counter', 0) >= 3:
        print("\nВы попали в слишком много ловушек. Игра окончена.")
        game_state['game_over'] = True
        return
    
    # Проверка времени
    if game_state.get('time_limit') \
        and game_state['steps_taken'] >= game_state['time_limit']:
        print("\nВремя вышло! Игра окончена.")
        game_state['game_over'] = True
        return

#def save_game(game_state, filename='savegame.json'):
#    """Сохранение состояния игры."""
#    try:
#        with open(filename, 'w') as f:
#            json.dump(game_state, f)
#        print("Игра сохранена.")
#    except Exception as e:
#        print(f"Ошибка сохранения: {str(e)}")

#def load_game(filename='savegame.json'):
#    """Загрузка сохраненной игры."""
#    try:
#        with open(filename, 'r') as f:
#            loaded_state = json.load(f)
#        print("Игра загружена.")
#        return loaded_state
#    except FileNotFoundError:
#        print("Нет сохраненной игры.")
#        return None
#    except Exception as e:
#        print(f"Ошибка загрузки: {str(e)}")
#        return None


# Вспомогательные методы

def initialize_game():
    """Инициализация нового игрового состояния."""
    return {
        'current_room': 'start_room',
        'player_inventory': [],
        'steps_taken': 0,
        'health': 100,
        'game_over': False,
        'traps_counter': 0,
        'time_limit': 100,  # Максимальное количество шагов
        'health_drain': 1   # Потеря здоровья за ход
    }

def main_game_loop(game_state):
    """Основной игровой цикл."""
    while not game_state['game_over']:
        command = input("\nВведите команду: ")
        process_command(constants.COMMANDS, game_state, command)
        update_game_state(game_state)


# Прочее (не совсем уже понимаю, могу ли удалить или боюсь сломать*)

def quick_save(game_state):
    """Быстрое сохранение игры."""
    utils.save_game(game_state)
    print("Игра сохранена.")

def quick_load():
    """Быстрая загрузка игры."""
    new_game_state = utils.load_game()
    if new_game_state:
        return new_game_state
    else:
        print("Загрузка не удалась.")
        return None

def show_map(game_state):
    """Показывает карту исследованных комнат."""
    visited_rooms = set()
    current_room = game_state['current_room']
    visited_rooms.add(current_room)
    
    def explore_room(room_name):
        room = constants.ROOMS[room_name]
        for direction, destination in room['exits'].items():
            if destination not in visited_rooms:
                visited_rooms.add(destination)
                explore_room(destination)
    
    explore_room(current_room)
    
    print("\nИсследованные комнаты:")
    for room in visited_rooms:
        print(f"- {room}")

def check_status(game_state):
    """Показывает статус игрока."""
    print("\nСтатус игрока:")
    print(f"Шаги: {game_state['steps_taken']}")
    print(f"Текущая комната: {game_state['current_room']}")
    #print(f"Инвентарь: {', '.join(game_state['player_inventory']) 
    # if game_state['player_inventory'] else 'Пусто'}")
    # если нижняя часть не работает, верхнюю надо соединить, но она длинная для ruff
    inventory_content = (
        ', '.join(game_state['player_inventory'])
        if game_state['player_inventory']
        else 'Пусто'
    )
    print(f"Инвентарь: {inventory_content}")

#def handle_special_events(game_state):
#    """Обрабатывает специальные игровые события."""
#    # Пример реализации:
#    current_room = constants.ROOMS[game_state['current_room']]
#    
#    if 'special_event' in current_room:
#        event = current_room['special_event']
#        print(f"\n{event['description']}")
#        
#        if 'effect' in event:
#            # Применяем эффект события
#            if event['effect'] == 'heal':
#                print("Вы чувствуете прилив сил!")
#                # Здесь можно добавить восстановление здоровья
#            elif event['effect'] == 'trap':
#                print("Ловушка сработала! Вы потеряли здоровье!")
#                # Здесь можно добавить урон
#    
#    # Случайное событие
#    if random.random() < 0.1:  # 10% шанс
#        utils.random_event(game_state)




# labyrinth_game/utils.py

from . import constants
from . import player_actions

#import json
# import random
import math

def describe_current_room(game_state):
    """Описывает текущую комнату игроку."""
    room = constants.ROOMS[game_state['current_room']]
    print(f"\n== {game_state['current_room'].upper()} ==")
    print(room['description'])
    
    # Выводим предметы
    if room['items']:
        print("\nЗаметные предметы:")
        for item in room['items']:
            print(f"- {item}")
    
    # Выводим доступные выходы
    print("\nВыходы:")
    for direction, destination in room['exits'].items():
        print(f"- {direction.capitalize()} → {destination}")
    
    # Проверяем наличие загадки
    if room['puzzle']:
        print("\nКажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    """Решает загадку в текущей комнате."""
    room = constants.ROOMS[game_state['current_room']]
    
    if not room['puzzle']:
        print("Загадок здесь нет.")
        return
    
    question, answer = room['puzzle']
    print(f"\n{question}")
    user_answer = player_actions.get_input("Ваш ответ: ")
    
    if user_answer.lower() == answer.lower():
        print("Правильно! Вы решили загадку!")
        room['puzzle'] = None  # Загадка решена, удаляем её
        
        # Добавляем награду (можно расширить логику наград)
        if 'reward' in room:
            for item in room['reward']:
                game_state['player_inventory'].append(item)
            print(f"Вы получили: {', '.join(room['reward'])}")
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами."""
    room = constants.ROOMS[game_state['current_room']]
    
    if game_state['current_room'] != 'treasure_room':
        return
    
    # Проверка наличия ключа
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    
    # Если ключа нет, предлагаем ввести код
    if room['puzzle']:
        print("\nСундук заперт. На нём есть панель для ввода кода.")
        choice = player_actions.get_input("Хотите попробовать ввести код? (да/нет): ")
        
        if choice.lower() == 'да':
            code = player_actions.get_input("Введите код: ")
            _, correct_code = room['puzzle']
            
            if code == correct_code:
                print("Замок щёлкает! Сундук открыт!")
                room['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код! Попробуйте ещё раз.")
        else:
            print("Вы отступаете от сундука.")

def show_help():
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")

#def save_game(game_state):
#    """Сохраняет текущее состояние игры в файл."""
#    try:
#        with open('savegame.json', 'w') as file:
#           json.dump({
#               'inventory': game_state['player_inventory'],
#                'current_room': game_state['current_room'],
#                'game_over': game_state['game_over'],
#               'steps_taken': game_state['steps_taken']
#           }, file, indent=4)
#           print("Игра успешно сохранена!")
#            
#   except IOError:
#       print("Ошибка при сохранении игры.")

#def load_game():
#    """Загружает сохранённую игру."""
#    try:
#        with open('savegame.json', 'r') as file:
#            saved_data = json.load(file)
#           
#           # Восстанавливаем состояние игры
#           game_state = {
#                'player_inventory': saved_data.get('inventory', []),
#                'current_room': saved_data.get('current_room', 'entrance'),
#                'game_over': saved_data.get('game_over', False),
#                'steps_taken': saved_data.get('steps_taken', 0)
#            }
#            
#            print("Игра успешно загружена!")
#            return game_state
#            
#    except FileNotFoundError:
#       print("Сохранённая игра не найдена.")
#        return None
#    except json.JSONDecodeError:
#        print("Ошибка при загрузке сохранения.")
#        return None

def pseudo_random(seed, modulo):
    value = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = value - math.floor(value)
    result = int(fractional_part * modulo)
    return result

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    
    if game_state['player_inventory']:
        index = pseudo_random(game_state['steps_taken'], len(game_state['player_inventory']))
        lost_item = game_state['player_inventory'].pop(index)
        print(f"Вы потеряли предмет: {lost_item}!")
    else:
        damage = pseudo_random(game_state['steps_taken'], 10)
        if damage < 3:
            print("Вы не смогли избежать урона! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам повезло, вы уцелели!")

def random_event(game_state):
    # Вероятность события 1/10
    if pseudo_random(game_state['steps_taken'], 10) == 0:
        event = pseudo_random(game_state['steps_taken'], 3)
        
        if event == 0:  # Находка
            current_room = constants.ROOMS[game_state['current_room']]
            current_room['items'].append('coin')
            print("Вы нашли монетку на полу!")
            
        elif event == 1:  # Испуг
            print("Вы слышите шорох позади...")
            if 'sword' in game_state['player_inventory']:
                print("Ваш меч отпугнул неизвестное существо!")
                
        elif event == 2:  # Ловушка
            if (game_state['current_room'] == 'trap_room' and 
                'torch' not in game_state['player_inventory']):
                print("Опасность! В комнате активировалась ловушка!")
                trigger_trap(game_state)

def check_victory_conditions(game_state):
    """Проверяет условия победы."""
    if game_state['current_room'] == 'treasure_room':
        room = constants.ROOMS[game_state['current_room']]
        
        if 'treasure_chest' not in room['items']:
            print("\nПоздравляем! Вы нашли все сокровища и победили!")
            game_state['game_over'] = True
            return True
            
    return False

def get_room_details(room_name):
    """Возвращает детали комнаты по её имени."""
    return constants.ROOMS.get(room_name, None)

def update_room_state(room_name, updates):
    """Обновляет состояние комнаты."""
    room = constants.ROOMS.get(room_name)
    if room:
        room.update(updates)
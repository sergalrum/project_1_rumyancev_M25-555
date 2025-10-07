# main.py

from . import utils
from . import player_actions
from . import constants
import sys

def main():
    # Инициализация игрового состояния
    game_state = constants.INITIAL_STATE.copy()
    
    # Приветственное сообщение
    print("Добро пожаловать в лабиринт!")
    print("Введите 'help' для списка команд.")
    
    # Описание начальной комнаты
    utils.describe_current_room(game_state)
    
    try:
        while not game_state['game_over']:
            # Получение команды от игрока
            command = input("\n> ").strip()
            
            # Обработка команды
            player_actions.process_command(
                constants.COMMANDS,
                game_state,
                command
            )
            
            # Обновление состояния игры
            player_actions.update_game_state(game_state)
            
            # Проверка условий завершения
            player_actions.check_game_conditions(game_state)
    
    except KeyboardInterrupt:
        print("\nИгра прервана. До свидания!")
        sys.exit(0)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Установка зависимостей проекта
install:
	poetry install

# Запуск проекта
project:
	poetry run project

# Сборка пакета
build:
	poetry build

# Тестовая публикация
publish:
	poetry publish --dry-run

# Установка пакета в систему
package-install:
	python3 -m pip install dist/*.whl

# Активация виртуального окружения
activate:
	poetry shell

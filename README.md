# Онлайн-платформа для обмена кулинарными рецептами

## Описание проекта

Веб-приложение, позволяющее пользователям делиться кулинарными рецептами, просматривать и оценивать рецепты других пользователей, а также оставлять отзывы.
Поддерживается разграничение прав доступа на основе ролей пользователей (пользователь/администратор).
Разработано в рамках экзаменационного задания.

---

## Возможности

- Регистрация и аутентификация пользователей
- Разграничение прав доступа (Пользователь / Администратор)
- Добавление, редактирование и удаление рецептов
- Просмотр рецептов с изображениями, списком ингредиентов, шагами приготовления
- Оценка рецептов и добавление отзывов
- Поддержка Markdown в рецептах
- Загрузка изображений к рецептам
- Удаление рецептов с каскадным удалением связанных отзывов и изображений
- Пагинация на главной странице
- Flash-сообщения и валидация данных

## Run

Для конфигурации проекта создайте .env файл:

```env
PYTHONPATH=src
CONFIG_PATH = config/config.yaml
```

Чтобы запустить проект, выполните следующую команду:

```bash
python -m src.run.flask.main
```

Чтобы запонить базу данных, выполните следующую команду:

```bash
python -m src.run.database.main
```

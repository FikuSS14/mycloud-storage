# My Cloud Storage

<div align="center">

![Django](https://img.shields.io/badge/Django-6.0-green)
![React](https://img.shields.io/badge/React-18-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-navy)
![Redux](https://img.shields.io/badge/Redux-Toolkit-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Облачное хранилище файлов - дипломный проект Fullstack-разработчика**

</div>

---

## О проекте

**My Cloud Storage** - это веб-приложение для хранения и управления файлами в облаке. Проект разработан в качестве дипломной работы по профессии **Fullstack-разработчик**.

Приложение позволяет пользователям:
- Регистрироваться и авторизовываться
- Загружать, скачивать, удалять и переименовывать файлы
- Делиться файлами по публичным ссылкам
- Администраторам - управлять пользователями и их файлами

---

## Функционал

### Пользовательская часть
- [x] Регистрация с валидацией:
  - Логин: 4-20 символов, латиница + цифры, первый символ - буква
  - Email: проверка формата через regex
  - Пароль: минимум 6 символов, заглавная буква, цифра, спецсимвол
- [x] Авторизация через сессии
- [x] Просмотр списка своих файлов
- [x] Загрузка файлов с комментарием
- [x] Скачивание файлов
- [x] Удаление файлов
- [x] Переименование файлов (дабл-клик по имени)
- [x] Редактирование комментария (дабл-клик)
- [x] Копирование публичной ссылки на файл
- [x] Просмотр файлов в браузере (изображения, PDF, текст)

### Административная часть
- [x] Просмотр списка всех пользователей
- [x] Информация о количестве и размере файлов у каждого пользователя
- [x] Назначение/снятие прав администратора
- [x] Удаление пользователей
- [x] Просмотр и управление файлами любого пользователя

### Технические особенности
- [x] Single Page Application (SPA) на React
- [x] REST API на Django Rest Framework
- [x] Сессионная аутентификация + CSRF защита
- [x] PostgreSQL в продакшене, SQLite для разработки
- [x] Обезличенные публичные ссылки (UUID)
- [x] Логирование операций с файлами (дата скачивания)

---

## Технологии

### Backend
| Технология | Версия | Назначение |
|------------|--------|------------|
| Python | 3.13 | Язык программирования |
| Django | 6.0 | Web-фреймворк |
| Django REST Framework | 3.17 | Построение API |
| PostgreSQL | 16 | База данных (продакшен) |
| psycopg2-binary | 2.9 | Драйвер PostgreSQL |
| django-cors-headers | - | Настройка CORS |

### Frontend
| Технология | Версия | Назначение |
|------------|--------|------------|
| React | 18.2 | UI библиотека |
| Redux Toolkit | - | Управление состоянием |
| React Router DOM | 6 | Маршрутизация |
| Axios | - | HTTP-запросы |

### Инструменты разработки
| Инструмент | Назначение |
|------------|------------|
| Black | Форматирование Python кода |
| isort | Сортировка импортов |
| flake8 | Проверка стиля кода |
| Git | Контроль версий |

---

## Установка и запуск

### Требования
- Python 3.10+
- Node.js 18+
- PostgreSQL 16 (для продакшена)
- Git

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/mycloud-storage.git
cd mycloud-storage
```

### 2. Настройка бэкенда (Django)

```bash
cd backend

# Создание виртуального окружения
python -m venv venv

# Активация окружения
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate

# Создание суперпользователя (админа)
python manage.py createsuperuser
# Логин: admin
# Email: admin@example.com
# Пароль: Admin123!

# Запуск сервера разработки
python manage.py runserver localhost:8000
```

### 3. Настройка фронтенда (React)

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск сервера разработки
npm start
```

### Структура проекта
```
mycloud-storage/
├── backend/                      # Бэкенд на Django
│   ├── core/                     # Основное приложение
│   │   ├── migrations/           # Миграции БД
│   │   ├── storage_files/        # Папка с загруженными файлами
│   │   ├── __init__.py
│   │   ├── admin.py              # Регистрация моделей в админке
│   │   ├── models.py             # Модели User и File
│   │   ├── serializers.py        # Сериализаторы DRF
│   │   ├── views.py              # API вьюхи
│   │   └── urls.py               # URL-маршруты приложения
│   ├── config/                   # Настройки проекта
│   │   ├── settings.py           # Основные настройки
│   │   └── urls.py               # Главные URL
│   ├── venv/                     # Виртуальное окружение
│   ├── manage.py
│   └── requirements.txt
├── frontend/                     # Фронтенд на React
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/           # React компоненты
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── FileList.js
│   │   │   ├── FileUpload.js
│   │   │   ├── AdminUsers.js
│   │   │   └── AdminFileView.js
│   │   ├── store/                # Redux store
│   │   │   ├── authSlice.js
│   │   │   ├── filesSlice.js
│   │   │   └── store.js
│   │   ├── services/
│   │   │   └── api.js            # Axios настройки
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── node_modules/
└── README.md
```

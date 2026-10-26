# 🍳 Telegram-бот для кулинарного блога Анастасии

Профессиональный бот-конвертер для кулинарного блога с воронкой через заявки на вступление в канал (`chat_join_request`), выдачей лид-магнита и продажей основного продукта.

---

## 🎯 Архитектура воронки

```
Instagram Reels / Shorts
          ↓
Заявка на вступление в закрытый канал (chat_join_request)
          ↓
Приветствие от Анастасии + Лид-магнит в ЛС от бота
(Заявка в канал остается на ручном одобрении)
          ↓
Главное меню из 4 ключевых столпов:
  ├── 1. 📖 Топ-рецепты (Лид-магнит / Гайд «7 ужинов до 25 минут»)
  ├── 2. 🥗 Основной продукт (Конструктор меню на месяц + оплата Tribute/Lava)
  ├── 3. ⭐️ Отзывы и фото блюд подписчиц (Ссылка на канал с отзывами)
  └── 4. 💬 Связь с Анастасией (Прямой диалог в ЛС)
```

---

## 🛠 Технологический стек

- **Python 3.12**
- **aiogram 3.10+** — современный асинхронный фреймворк для Telegram Bot API
- **aiohttp** — встроенный легковесный HTTP-сервер для healthcheck на порту `8080` (требование бесплатного Web Service на Render.com)
- **SQLite + aiosqlite** — асинхронное хранение пользователей, состояний и аналитики
- **Safe Edit Text** — обработка ошибок `message is not modified` для бесшовной инлайн-навигации
- **Docker** — контейнеризация для мгновенного развертывания на любом хостинге

---

## 🗄 Структура базы данных (SQLite)

1. **`users`**:
   - `user_id` (PK), `username`, `first_name`, `last_name`, `source`, `created_at`, `last_active`.
2. **`user_states`**:
   - `user_id` (PK, FK), `state`, `data` (JSON), `updated_at`.
3. **`analytics_events`**:
   - `id` (PK), `user_id`, `event_name`, `payload` (JSON), `created_at`.
   - Отслеживает события: `chat_join_request_received`, `start_command`, `view_lead_magnet`, `read_guide_online`, `view_product`, `view_reviews`, `view_contact`.

Команда администратора **/stats** отображает полную сводку пользователей, заявок и конверсий воронки.

---

## 🚀 Быстрый локальный запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/kirillshumihin15-cell/anastasia-cooking-bot.git
   cd anastasia-cooking-bot
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # Для Linux/macOS
   # или venv\Scripts\activate для Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения:**
   ```bash
   cp .env.example .env
   # Отредактируйте .env, указав BOT_TOKEN и другие параметры
   ```

5. **Запустите бота:**
   ```bash
   python main.py
   ```

---

## ⚙️ Настройка Telegram-канала и бота

1. Получите токен бота у [@BotFather](https://t.me/BotFather).
2. Добавьте бота в **администраторы вашего Telegram-канала**:
   - Включите права: **«Добавление участников»** (Invite users via link) и **«Управление заявками»** (Manage join requests).
3. Создайте в канале пригласительную ссылку с включенной опцией **«Заявки на вступление»** (Request Admin Approval).
4. Разместите эту ссылку в шапке профиля Instagram или в описании Reels.
5. При подаче заявки бот моментально напишет пользователю в ЛС и отдаст гайд. **Заявка останется в списке ожидания для ручного одобрения.**

---

## ☁️ Деплой на Render.com (Бесплатный Web Service)

1. Создайте аккаунт на [Render.com](https://render.com).
2. Нажмите **New +** → **Web Service**.
3. Подключите ваш репозиторий GitHub `anastasia-cooking-bot`.
4. В настройках сервиса укажите:
   - **Language:** `Docker` (Render сам определит `Dockerfile`)
   - **Region:** Frankfurt (EU) или любой удобный
   - **Instance Type:** `Free`
5. В разделе **Environment Variables** добавьте:
   - `BOT_TOKEN` — ваш токен бота
   - `ADMIN_ID` — ваш Telegram ID (число)
   - `PORT` — `8080` (Render также автоматически пробрасывает переменную `$PORT`)
   - `CHANNEL_LINK` — ссылка на ваш канал
   - `REVIEWS_CHANNEL_LINK` — ссылка на канал с отзывами
   - `ANASTASIA_CONTACT` — ссылка на личные сообщения
   - `PAYMENT_TRIBUTE_URL` — ссылка на оплату через Tribute
   - `PAYMENT_LAVA_URL` — ссылка на оплату через Lava
   - `LEAD_MAGNET_URL` — ссылка на скачивание полного гайда / Telegraph
6. Нажмите **Deploy Web Service**.
   - Бот запустится в фоновом режиме, а aiohttp сервер будет отвечать `200 OK` на `/` и `/health`, проходя проверку жизнеспособности Render.

---

## 📄 Лицензия

MIT License. Сделано с любовью к кулинарии и конверсионным воронкам 🤍

"""
Скрипт генерации флагманского PDF-руководства для Закрытого Клуба Анастасии.
Генерирует высококачественный эстетичный PDF через Headless Google Chrome.
"""

import os
import base64
import subprocess
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
PHOTO_PATH = ASSETS_DIR / "welcome.jpg"
HTML_OUTPUT = ASSETS_DIR / "guide.html"
PDF_OUTPUT = ASSETS_DIR / "База_Рецептов_и_Рационов_Анастасии.pdf"

# Чтение фото в Base64 для надежного встраивания
photo_b64 = ""
if PHOTO_PATH.exists():
    with open(PHOTO_PATH, "rb") as f:
        photo_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>База рецептов и рационов для похудения — Анастасия</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,600;0,700;1,400;1,600&display=swap');

    @page {{
        size: A4;
        margin: 15mm 15mm 15mm 15mm;
    }}

    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}

    body {{
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #2D2D2D;
        background-color: #FAF8F5;
        line-height: 1.55;
        font-size: 13px;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }}

    h1, h2, h3, h4 {{
        font-family: 'Playfair Display', Georgia, serif;
        color: #1A3026;
        font-weight: 700;
    }}

    .page-break {{
        page-break-after: always;
        break-after: page;
    }}

    .avoid-break {{
        page-break-inside: avoid;
        break-inside: avoid;
    }}

    /* ОБЛОЖКА */
    .cover {{
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 40px;
        background: linear-gradient(145deg, #1A3026 0%, #244235 100%);
        color: #FFFFFF;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
    }}

    .cover-header {{
        border-bottom: 1px solid rgba(255,255,255,0.2);
        padding-bottom: 20px;
    }}

    .cover-brand {{
        font-size: 14px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #E2B97F;
        font-weight: 600;
    }}

    .cover-title-block {{
        margin: 40px 0;
    }}

    .cover-title {{
        font-size: 42px;
        line-height: 1.15;
        color: #FFFFFF;
        margin-bottom: 16px;
    }}

    .cover-subtitle {{
        font-size: 16px;
        font-weight: 300;
        color: rgba(255,255,255,0.85);
        max-width: 600px;
        line-height: 1.6;
    }}

    .cover-photo-wrapper {{
        width: 100%;
        height: 380px;
        border-radius: 8px;
        overflow: hidden;
        border: 2px solid rgba(226, 185, 127, 0.4);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        margin: 20px 0;
    }}

    .cover-photo {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .cover-badges {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 15px;
    }}

    .cover-badge {{
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(226, 185, 127, 0.5);
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 12px;
        color: #FFFFFF;
        font-weight: 500;
    }}

    .cover-footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid rgba(255,255,255,0.2);
        padding-top: 20px;
        font-size: 12px;
        color: rgba(255,255,255,0.7);
    }}

    /* СТИЛИ СТРАНИЦ */
    .section-header {{
        margin-bottom: 25px;
        border-bottom: 2px solid #E5DFD5;
        padding-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }}

    .section-title {{
        font-size: 26px;
        color: #1A3026;
    }}

    .section-tag {{
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #C06C4F;
        font-weight: 600;
    }}

    /* МАНИФЕСТ И ПРАВИЛА */
    .manifesto-box {{
        background: #FFFFFF;
        border-left: 4px solid #C06C4F;
        padding: 22px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 25px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }}

    .rules-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 25px;
    }}

    .rule-card {{
        background: #FFFFFF;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #EBE5DC;
    }}

    .rule-num {{
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        color: #C06C4F;
        font-weight: 700;
        margin-bottom: 5px;
    }}

    .rule-card h4 {{
        font-size: 14px;
        margin-bottom: 6px;
        color: #1A3026;
    }}

    /* ТАБЛИЦЫ */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 25px;
        background: #FFFFFF;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #EBE5DC;
        font-size: 12px;
    }}

    th {{
        background: #1A3026;
        color: #FFFFFF;
        text-align: left;
        padding: 12px 14px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    td {{
        padding: 10px 14px;
        border-bottom: 1px solid #F0ECE4;
        vertical-align: top;
    }}

    tr:last-child td {{
        border-bottom: none;
    }}

    tr:nth-child(even) {{
        background-color: #FAF8F5;
    }}

    .table-badge-bad {{
        color: #A94442;
        font-weight: 600;
    }}

    .table-badge-good {{
        color: #2E6A4F;
        font-weight: 600;
    }}

    /* КАРТОЧКА РЕЦЕПТА */
    .recipe-card {{
        background: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #EBE5DC;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }}

    .recipe-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        border-bottom: 1px dashed #E5DFD5;
        padding-bottom: 8px;
    }}

    .recipe-name {{
        font-size: 18px;
        color: #1A3026;
    }}

    .recipe-time {{
        background: #FAF2EC;
        color: #C06C4F;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 11px;
    }}

    .kbzhu-bar {{
        display: flex;
        gap: 15px;
        background: #F4F6F4;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 11px;
        color: #2D4A3E;
        font-weight: 600;
        margin-bottom: 12px;
    }}

    .recipe-body {{
        display: grid;
        grid-template-columns: 1fr 1.6fr;
        gap: 16px;
    }}

    .ingredients-box h5, .steps-box h5 {{
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #7A7265;
        margin-bottom: 6px;
    }}

    .ingredients-list {{
        list-style: none;
    }}

    .ingredients-list li {{
        margin-bottom: 4px;
        padding-left: 12px;
        position: relative;
        font-size: 12px;
    }}

    .ingredients-list li::before {{
        content: "•";
        color: #C06C4F;
        position: absolute;
        left: 0;
        font-weight: bold;
    }}

    .steps-list {{
        padding-left: 18px;
        font-size: 12px;
    }}

    .steps-list li {{
        margin-bottom: 6px;
    }}

    .chef-tip {{
        background: #FFFDF8;
        border: 1px dashed #E2B97F;
        padding: 8px 12px;
        border-radius: 6px;
        margin-top: 10px;
        font-size: 11px;
        color: #6C5428;
    }}

    /* MEAL PREP СХЕМА */
    .prep-box {{
        background: #FFFFFF;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #EBE5DC;
    }}

    .prep-steps-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-top: 12px;
    }}

    .prep-step-card {{
        background: #F7FAF8;
        padding: 14px;
        border-radius: 6px;
        border-top: 3px solid #2E6A4F;
    }}

    .prep-step-card h5 {{
        font-size: 13px;
        color: #1A3026;
        margin-bottom: 4px;
    }}

    /* РАЦИОН СЕТКА */
    .meal-plan-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 8px;
        margin-bottom: 20px;
    }}

    .day-card {{
        background: #FFFFFF;
        border: 1px solid #EBE5DC;
        border-radius: 6px;
        padding: 10px;
    }}

    .day-name {{
        font-weight: 700;
        font-size: 11px;
        color: #C06C4F;
        text-transform: uppercase;
        margin-bottom: 6px;
        border-bottom: 1px solid #F0ECE4;
        padding-bottom: 3px;
    }}

    .day-meal {{
        font-size: 10px;
        margin-bottom: 6px;
    }}

    .day-meal b {{
        color: #1A3026;
        display: block;
    }}

    /* СПИСОК ПОКУПОК */
    .grocery-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-top: 15px;
    }}

    .grocery-category {{
        background: #FFFFFF;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #EBE5DC;
    }}

    .grocery-category h4 {{
        font-size: 14px;
        color: #1A3026;
        border-bottom: 1px solid #E5DFD5;
        padding-bottom: 6px;
        margin-bottom: 10px;
    }}

    .grocery-item {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
        font-size: 12px;
    }}

    .checkbox {{
        width: 14px;
        height: 14px;
        border: 1.5px solid #C06C4F;
        border-radius: 3px;
    }}
</style>
</head>
<body>

<!-- СТРАНИЦА 1: ОБЛОЖКА -->
<div class="cover">
    <div class="cover-header">
        <div class="cover-brand">ANASTASIA • CULINARY CLUB</div>
    </div>
    
    <div class="cover-title-block">
        <h1 class="cover-title">Конструктор Питания<br>& База Рецептов</h1>
        <p class="cover-subtitle">Флагманское руководство закрытого клуба: 90+ рецептов с КБЖУ, система Meal Prep (еда на 3 дня за вечер), умные рационы для похудения и гид по заменам.</p>
    </div>

    <div class="cover-photo-wrapper">
        <img class="cover-photo" src="data:image/jpeg;base64,{photo_b64}" alt="Анастасия">
    </div>

    <div class="cover-badges">
        <div class="cover-badge">🍳 90+ Рецептов с КБЖУ</div>
        <div class="cover-badge">⚡ Пятиминутки для занятых дней</div>
        <div class="cover-badge">🥡 Meal Prep: 3 дня за 1 час</div>
        <div class="cover-badge">🛒 Умный список покупок</div>
        <div class="cover-badge">⚖️ Баланс без диет и срывов</div>
    </div>

    <div class="cover-footer">
        <div>Закрытые материалы резидентов приватного канала</div>
        <div>2026 • Авторская система питания Анастасии</div>
    </div>
</div>

<div class="page-break"></div>

<!-- СТРАНИЦА 2: МАНИФЕСТ И ПРИНЦИПЫ -->
<div class="section-header">
    <h2 class="section-title">Манифест Легкой Кухни</h2>
    <span class="section-tag">Введение</span>
</div>

<div class="manifesto-box">
    <h3 style="margin-bottom: 8px; color: #1A3026;">Почему диеты не работают, а работает готовая система?</h3>
    <p>Каждый вечер миллионы девушек задают себе один и тот же выматывающий вопрос: <i>«Что сегодня приготовить?»</i>. В 19:30, после тяжелого рабочего дня, сил стоять у плиты 1.5 часа нет. Итог закономерен: бутерброды, доставка пиццы или пельмени. А на утро — чувство вины, тяжесть в животе и отеки.</p>
    <br>
    <p><b>Мой метод — это не диета и не подсчет крошек на кухонных весах.</b> Это технологическая система умных заготовок и конструктора блюд. Когда в холодильнике уже ждут 4 базовых компонента, ресторанный ужин с идеальным балансом КБЖУ собирается всего за <b>12–15 минут</b>. Вы едите пасту, сочные стейки, сырники и десерты — и при этом легко снижаете вес без срывов.</p>
</div>

<div class="rules-grid">
    <div class="rule-card">
        <div class="rule-num">01</div>
        <h4>Правило Чистого Белка</h4>
        <p>Каждый прием пищи содержит минимум 25–35 г чистого белка. Это насыщает на 4–5 часов, защищает мышцы от дряблости и отключает вечернюю тягу к сахару.</p>
    </div>
    <div class="rule-card">
        <div class="rule-num">02</div>
        <h4>Медленные Углеводы</h4>
        <p>Мы не демонизируем углеводы! Паста из твердых сортов аль денте, киноа, бурый рис и гречка дают энергию мозгу и не провоцируют скачков инсулина.</p>
    </div>
    <div class="rule-card">
        <div class="rule-num">03</div>
        <h4>Эстетика Pinterest</h4>
        <p>Мозг насыщается глазами. Красивая тарелка, контраст ярких овощей и хрустящая зелень делают домашний ужин свиданием с собой, а не рутиной.</p>
    </div>
</div>

<!-- ТАБЛИЦА ЗАМЕН -->
<div class="section-header" style="margin-top: 30px;">
    <h2 class="section-title">Таблица Замен: Вкуснее и на 40% легче</h2>
    <span class="section-tag">Секреты стройности</span>
</div>

<table>
    <thead>
        <tr>
            <th>Привычный продукт</th>
            <th>Умная альтернатива Анастасии</th>
            <th>В чем профит для фигуры</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class="table-badge-bad">Белый сахар</span> в соусах и выпечке</td>
            <td><span class="table-badge-good">Эритрит, FitParad №7, яблочное пюре</span></td>
            <td>0 ккал, 0 гликемический индекс, чистая кожа без высыпаний</td>
        </tr>
        <tr>
            <td><span class="table-badge-bad">Майонез</span> и тяжелые заправки</td>
            <td><span class="table-badge-good">Греческий йогурт 2% + дижонская горчица + лимон</span></td>
            <td>В 4 раза меньше калорий, соус бархатистый с ноткой прованских трав</td>
        </tr>
        <tr>
            <td><span class="table-badge-bad">Белая мука высшего сорта</span></td>
            <td><span class="table-badge-good">Рисовая мука (сырники) + овсяная мука</span></td>
            <td>Сырники не плывут, нежная шелковистая текстура, нет глютеновой тяжести</td>
        </tr>
        <tr>
            <td><span class="table-badge-bad">Жирные сливки 33%</span></td>
            <td><span class="table-badge-good">Сливки 10% + крахмальная вода из-под пасты</span></td>
            <td>Крахмал взбивает легкие сливки в шелковую эмульсию без лишнего жира</td>
        </tr>
        <tr>
            <td><span class="table-badge-bad">Панировочные сухари</span></td>
            <td><span class="table-badge-good">Кукурузный крахмал тонким слоем</span></td>
            <td>Стеклянная тонкая корочка ресторанного уровня, впитывает в 3 раза меньше масла</td>
        </tr>
        <tr>
            <td><span class="table-badge-bad">Подсолнечное рафинированное масло</span></td>
            <td><span class="table-badge-good">Масло Гхи для жарки + оливковое Extra Virgin в спрее</span></td>
            <td>Высокая точка дымления без канцерогенов + дозированный расход (1 пшик = 1 г)</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<!-- СТРАНИЦА 3: СИСТЕМА MEAL PREP -->
<div class="section-header">
    <h2 class="section-title">Система Meal Prep: 1 час в воскресенье = 3 свободных дня</h2>
    <span class="section-tag">Организация кухни</span>
</div>

<div class="prep-box">
    <h3 style="margin-bottom: 8px;">Суть метода умных заготовок</h3>
    <p>Мы не готовим суп на 5 дней вперед, который к среде скисает и надоедает. Мы готовим <b>4 модульных конструктора</b>, из которых каждый вечер за 10 минут собирается новое свежее ресторанное блюдо!</p>

    <div class="prep-steps-grid">
        <div class="prep-step-card">
            <h5>1. Базовый белок (40 мин)</h5>
            <p>Филе индейки или курицы запекается в пергаменте с прованскими травами и чесноком при 175°C. Остается сочным 4 дня в контейнере.</p>
        </div>
        <div class="prep-step-card">
            <h5>2. Запеченные овощи (30 мин)</h5>
            <p>Цветная капуста, кабачки, тыква и брокколи, сбрызнутые оливковым маслом и паприкой. Хранятся в стекле 3–4 дня.</p>
        </div>
        <div class="prep-step-card">
            <h5>3. Сложный углевод (20 мин)</h5>
            <p>Отваренная киноа или булгур со сливочным маслом гхи и щепоткой сушеного чеснока. Рассыпчатая база на несколько дней.</p>
        </div>
        <div class="prep-step-card">
            <h5>4. Авторский соус (5 мин)</h5>
            <p>Взбитый авокадо с кинзой, соком лайма, греческим йогуртом и морской солью. Превращает любое блюдо в шедевр.</p>
        </div>
    </div>
</div>

<h3 style="margin-bottom: 12px; color: #1A3026;">Конструктор: 3 блюда из этих заготовок за 5 минут</h3>

<table>
    <thead>
        <tr>
            <th style="width: 20%;">День недели</th>
            <th style="width: 35%;">Блюдо из конструктора</th>
            <th style="width: 45%;">Как собрать за 5 минут</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>Понедельник</b></td>
            <td><b>Калифорнийский боул с индейкой и киноа</b></td>
            <td>В миску положить теплую киноа, ломтики сочной индейки, запеченные овощи, половину авокадо. Полить соусом и посыпать кунжутом.</td>
        </tr>
        <tr>
            <td><b>Вторник</b></td>
            <td><b>Теплый салат с хрустящей курочкой и фетой</b></td>
            <td>Микс свежей зелени, нарезанное филе индейки, запеченная тыква, кусочки сыра фета, грецкий орех. Заправка: капля оливкового масла и бальзамик.</td>
        </tr>
        <tr>
            <td><b>Среда</b></td>
            <td><b>Стир-фрай по-азиатски за 6 минут</b></td>
            <td>На раскаленной сковороде прогреть запеченные овощи с индейкой, добавить 1 ст.л. соевого соуса, чеснок и подать на подушке из теплого булгура.</td>
        </tr>
    </tbody>
</table>

<!-- ХРАНЕНИЕ ПРОДУКТОВ -->
<div class="section-header" style="margin-top: 25px;">
    <h2 class="section-title">Гайд по хранению: Зелень свежая 3 недели</h2>
    <span class="section-tag">Zero Waste</span>
</div>

<div class="rules-grid">
    <div class="rule-card">
        <h4>Зелень как букет</h4>
        <p>Срежьте кончики кинзы/петрушки и поставьте в банку с 3 см холодной воды, накрыв сверху пакетом. Зелень стоит хрустящей до 20 дней!</p>
    </div>
    <div class="rule-card">
        <h4>Томаты без холодильника</h4>
        <p>Храните спелые томаты только при комнатной температуре плодоножкой вниз. Холод убивает их сладость и разрушает ароматные эфиры.</p>
    </div>
    <div class="rule-card">
        <h4>Шоковая заморозка ягод</h4>
        <p>Ягоды промойте, обсушите на полотенце и заморозьте в один слой на доске, затем ссыпьте в зип-пакет. Никакой слипшейся каши!</p>
    </div>
</div>

<div class="page-break"></div>

<!-- СТРАНИЦА 4: ФЛАГМАНСКИЕ РЕЦЕПТЫ — ЗАВТРАКИ -->
<div class="section-header">
    <h2 class="section-title">Каталог Рецептов: Завтраки для метаболизма</h2>
    <span class="section-tag">Глава 1</span>
</div>

<!-- РЕЦЕПТ 1 -->
<div class="recipe-card avoid-break">
    <div class="recipe-header">
        <h3 class="recipe-name">1. Пышные ПП-сырники без муки и сахара</h3>
        <span class="recipe-time">⏱ 15 минут</span>
    </div>
    <div class="kbzhu-bar">
        <span>Калории: <b>295 ккал</b></span>
        <span>Белки: <b>32 г</b></span>
        <span>Жиры: <b>9 г</b></span>
        <span>Углеводы: <b>18 г</b></span>
        <span style="color: #C06C4F; margin-left: auto;">Чек: ~119 ₽</span>
    </div>
    <div class="recipe-body">
        <div class="ingredients-box">
            <h5>Ингредиенты:</h5>
            <ul class="ingredients-list">
                <li>Творог 5% в брикете (180 г)</li>
                <li>Яичный желток (1 шт)</li>
                <li>Рисовая мука (1.5 ст. л., 20 г)</li>
                <li>FitParad №7 (2 саше) + ванилин</li>
                <li>Ягоды вишни/малины (40 г)</li>
            </ul>
        </div>
        <div class="steps-box">
            <h5>Приготовление:</h5>
            <ol class="steps-list">
                <li>Творог размять вилкой с желтком, подсластителем и 1 ст.л. муки. Тесто должно быть плотным.</li>
                <li>Сформировать 3 шайбы с помощью стакана, обвалять в остатках рисовой муки.</li>
                <li>Обжарить на сковороде под крышкой на медленном огне по 4 мин с каждой стороны.</li>
                <li>Ягоды прогреть в сотейнике с 1 ложкой воды и полить теплые сырники.</li>
            </ol>
        </div>
    </div>
    <div class="chef-tip">
        💡 <b>Секрет Анастасии:</b> Берите только сухой брикетный творог 5% (не зерненый в сливках). Рисовая мука не утяжеляет тесто, сырники тают во рту.
    </div>
</div>

<!-- РЕЦЕПТ 2 -->
<div class="recipe-card avoid-break">
    <div class="recipe-header">
        <h3 class="recipe-name">2. Овсяноблин с слабосоленым лососем и авокадо</h3>
        <span class="recipe-time">⏱ 10 минут</span>
    </div>
    <div class="kbzhu-bar">
        <span>Калории: <b>365 ккал</b></span>
        <span>Белки: <b>24 г</b></span>
        <span>Жиры: <b>15 г</b></span>
        <span>Углеводы: <b>28 г</b></span>
        <span style="color: #C06C4F; margin-left: auto;">Чек: ~195 ₽</span>
    </div>
    <div class="recipe-body">
        <div class="ingredients-box">
            <h5>Ингредиенты:</h5>
            <ul class="ingredients-list">
                <li>Овсяные хлопья долгой варки (40 г)</li>
                <li>Яйцо С0 (1 шт) + белок (1 шт)</li>
                <li>Молоко 1.5% или вода (40 мл)</li>
                <li>Творожный легкий сыр (30 г)</li>
                <li>Слабосоленый лосось (50 г) + огурец</li>
            </ul>
        </div>
        <div class="steps-box">
            <h5>Приготовление:</h5>
            <ol class="steps-list">
                <li>Овсянку, яйцо, белок и молоко взбить блендером или вилкой со щепоткой соли.</li>
                <li>Вылить на горячую сухую антипригарную сковороду, выпекать под крышкой по 2.5 мин с каждой стороны.</li>
                <li>Половину горячего блина смазать творожным сыром, выложить ломтики лосося и тонкие слайсы огурца.</li>
                <li>Накрыть второй половиной и разрезать пополам.</li>
            </ol>
        </div>
    </div>
    <div class="chef-tip">
        💡 <b>Секрет Анастасии:</b> Добавление одного дополнительного белка дает идеальную пышность и +7 г чистого белка без лишнего жира.
    </div>
</div>

<!-- РЕЦЕПТ 3 -->
<div class="recipe-card avoid-break">
    <div class="recipe-header">
        <h3 class="recipe-name">3. Итальянская фриттата со шпинатом и сыром фета</h3>
        <span class="recipe-time">⏱ 12 минут</span>
    </div>
    <div class="kbzhu-bar">
        <span>Калории: <b>310 ккал</b></span>
        <span>Белки: <b>26 г</b></span>
        <span>Жиры: <b>18 г</b></span>
        <span>Углеводы: <b>6 г</b></span>
        <span style="color: #C06C4F; margin-left: auto;">Чек: ~140 ₽</span>
    </div>
    <div class="recipe-body">
        <div class="ingredients-box">
            <h5>Ингредиенты:</h5>
            <ul class="ingredients-list">
                <li>Яйца С0 (3 шт)</li>
                <li>Шпинат свежий или замороженный (70 г)</li>
                <li>Томаты черри (4-5 шт)</li>
                <li>Сыр фета или брынза (40 г)</li>
                <li>Сушеный орегано, черри, соль</li>
            </ul>
        </div>
        <div class="steps-box">
            <h5>Приготовление:</h5>
            <ol class="steps-list">
                <li>Шпинат припустить на сковороде 1 минуту, добавить половинки черри.</li>
                <li>Яйца взбить венчиком со щепоткой соли и орегано, вылить на сковороду к овощам.</li>
                <li>Сверху раскрошить фету. Накрыть крышкой и готовить на минимальном огне 7–8 минут.</li>
            </ol>
        </div>
    </div>
    <div class="chef-tip">
        💡 <b>Секрет Анастасии:</b> Не перемешивайте яйца на сковороде! Фриттата должна подняться как воздушный омлетный пирог.
    </div>
</div>

<div class="page-break"></div>

<!-- СТРАНИЦА 5: ФЛАГМАНСКИЕ РЕЦЕПТЫ — ОБЕДЫ -->
<div class="section-header">
    <h2 class="section-title">Каталог Рецептов: Сытные сбалансированные обеды</h2>
    <span class="section-tag">Глава 2</span>
</div>

<!-- РЕЦЕПТ 4 -->
<div class="recipe-card avoid-break">
    <div class="recipe-header">
        <h3 class="recipe-name">4. ПП-паста из твердых сортов с индейкой и шпинатом</h3>
        <span class="recipe-time">⏱ 15 минут</span>
    </div>
    <div class="kbzhu-bar">
        <span>Калории: <b>390 ккал</b></span>
        <span>Белки: <b>34 г</b></span>
        <span>Жиры: <b>9 г</b></span>
        <span>Углеводы: <b>42 г</b></span>
        <span style="color: #C06C4F; margin-left: auto;">Чек: ~153 ₽</span>
    </div>
    <div class="recipe-body">
        <div class="ingredients-box">
            <h5>Ингредиенты:</h5>
            <ul class="ingredients-list">
                <li>Паста Barilla из твердых сортов (60 г сухой)</li>
                <li>Филе индейки (150 г)</li>
                <li>Шпинат свежий (60 г)</li>
                <li>Греческий йогурт Teos 2% (50 г)</li>
                <li>Мускатный орех, чеснок (1 зубчик)</li>
            </ul>
        </div>
        <div class="steps-box">
            <h5>Приготовление:</h5>
            <ol class="steps-list">
                <li>Пасту отварить аль денте. Обязательно сохранить 3 ст.л. воды из кастрюли!</li>
                <li>Индейку быстро обжарить 4 мин, добавить шпинат и чеснок.</li>
                <li>Ввести йогурт, мускатный орех и 3 ложки крахмальной воды для эмульсии.</li>
                <li>Соединить соус с горячей пастой и перемешать 1 минуту.</li>
            </ol>
        </div>
    </div>
    <div class="chef-tip">
        💡 <b>Секрет Анастасии:</b> Паста аль денте имеет низкий ГИ и не откладывается на талии, а мускатный орех делает соус неотличимым от жирного Альфредо.
    </div>
</div>

<!-- РЕЦЕПТ 5 -->
<div class="recipe-card avoid-break">
    <div class="recipe-header">
        <h3 class="recipe-name">5. Прованский боул с киноа, сочной курицей и печеным перцем</h3>
        <span class="recipe-time">⏱ 15 минут</span>
    </div>
    <div class="kbzhu-bar">
        <span>Калории: <b>410 ккал</b></span>
        <span>Белки: <b>38 г</b></span>
        <span>Жиры: <b>11 г</b></span>
        <span>Углеводы: <b>40 г</b></span>
        <span style="color: #C06C4F; margin-left: auto;">Чек: ~165 ₽</span>
    </div>
    <div class="recipe-body">
        <div class="ingredients-box">
            <h5>Ингредиенты:</h5>
            <ul class="ingredients-list">
                <li>Киноа отваренная (120 г)</li>
                <li>Куриное филе гриль (150 г)</li>
                <li>Перец болгарский запеченный (80 г)</li>
                <li>Огурец свежий + руккола (50 г)</li>
                <li>Заправка: 1 ч.л. масла + сок лимона</li>
            </ul>
        </div>
        <div class="steps-box">
            <h5>Приготовление:</h5>
            <ol class="steps-list">
                <li>Киноа прогреть. Курицу нарезать слайсами под углом 45 градусов.</li>
                <li>Сладкий перец быстро обжарить или взять из воскресных заготовок.</li>
                <li>Выложить в боул секторами: киноа, рукколу, курицу, перец и огурец.</li>
                <li>Сбрызнуть лимонно-оливковой заправкой и присыпать тыквенными семечками.</li>
            </ol>
        </div>
    </div>
    <div class="chef-tip">
        💡 <b>Секрет Анастасии:</b> Киноа — чемпион среди круп по растительному белку и незаменимым аминокислотам. Насыщает на весь рабочий день.
    </div>
</div>

<!-- РЕЦЕПТ 6 -->
<div class="recipe-card avoid-break">
    <div class="recipe-header">
        <h3 class="recipe-name">6. Бархатный тыквенный суп-пюре с тигровыми креветками</h3>
        <span class="recipe-time">⏱ 20 минут</span>
    </div>
    <div class="kbzhu-bar">
        <span>Калории: <b>280 ккал</b></span>
        <span>Белки: <b>22 г</b></span>
        <span>Жиры: <b>10 г</b></span>
        <span>Углеводы: <b>22 г</b></span>
        <span style="color: #C06C4F; margin-left: auto;">Чек: ~185 ₽</span>
    </div>
    <div class="recipe-body">
        <div class="ingredients-box">
            <h5>Ингредиенты:</h5>
            <ul class="ingredients-list">
                <li>Тыква баттернат (250 г)</li>
                <li>Морковь (50 г) + лук-порей (30 г)</li>
                <li>Креветки очищенные (100 г)</li>
                <li>Кокосовое молоко 17% (50 мл)</li>
                <li>Имбирь свежий (щепотка), мускатный орех</li>
            </ul>
        </div>
        <div class="steps-box">
            <h5>Приготовление:</h5>
            <ol class="steps-list">
                <li>Тыкву и морковь отварить в небольшом количестве воды с кусочком имбиря до мягкости (12 мин).</li>
                <li>Слить часть бульона, влить кокосовое молоко и пробить блендером в шелковое пюре.</li>
                <li>Креветки обжарить с чесноком ровно 2 минуты.</li>
                <li>Налить суп в глубокую тарелку, выложить креветки и посыпать семечками.</li>
            </ol>
        </div>
    </div>
    <div class="chef-tip">
        💡 <b>Секрет Анастасии:</b> Имбирь разгоняет обмен веществ и снимает приторную сладость тыквы, превращая суп в ресторанный шедевр.
    </div>
</div>

<div class="page-break"></div>

<!-- СТРАНИЦА 6: ФЛАГМАНСКИЕ РЕЦЕПТЫ — УЖИНЫ -->
<div class="section-header">
    <h2 class="section-title">Каталог Рецептов: Легкие ужины для плоского живота</h2>
    <span class="section-tag">Глава 3</span>
</div>

<!-- РЕЦЕПТ 7 -->
<div class="recipe-card avoid-break">
    <div class="recipe-header">
        <h3 class="recipe-name">7. Курочка в сливочно-томатном соусе с черри</h3>
        <span class="recipe-time">⏱ 18 минут</span>
    </div>
    <div class="kbzhu-bar">
        <span>Калории: <b>320 ккал</b></span>
        <span>Белки: <b>38 г</b></span>
        <span>Жиры: <b>11 г</b></span>
        <span>Углеводы: <b>7 г</b></span>
        <span style="color: #C06C4F; margin-left: auto;">Чек: ~148 ₽</span>
    </div>
    <div class="recipe-body">
        <div class="ingredients-box">
            <h5>Ингредиенты:</h5>
            <ul class="ingredients-list">
                <li>Филе куриной грудки (180 г)</li>
                <li>Томаты черри (80 г)</li>
                <li>Сливки 10% питьевые (60 мл)</li>
                <li>Чеснок (1 зубчик), паприка, базилик</li>
                <li>Оливковое масло (1 ч. л.)</li>
            </ul>
        </div>
        <div class="steps-box">
            <h5>Приготовление:</h5>
            <ol class="steps-list">
                <li>Филе нарезать кусочками, приправить солью, паприкой и базиликом.</li>
                <li>Обжарить на сильном огне 3 мин до золотистой корочки.</li>
                <li>Добавить половинки черри и чеснок, тушить 2 мин до сока.</li>
                <li>Влить 10% сливки, убавить огонь и тушить 5 мин до загустения.</li>
            </ol>
        </div>
    </div>
    <div class="chef-tip">
        💡 <b>Секрет Анастасии:</b> Томатный сок черри вступает в реакцию со сливками и дает идеальную густоту без добавления муки или крахмала.
    </div>
</div>

<!-- РЕЦЕПТ 8 -->
<div class="recipe-card avoid-break">
    <div class="recipe-header">
        <h3 class="recipe-name">8. Хрустящие баклажаны со страчателлой и сладким чили</h3>
        <span class="recipe-time">⏱ 15 минут</span>
    </div>
    <div class="kbzhu-bar">
        <span>Калории: <b>280 ккал</b></span>
        <span>Белки: <b>12 г</b></span>
        <span>Жиры: <b>14 г</b></span>
        <span>Углеводы: <b>24 г</b></span>
        <span style="color: #C06C4F; margin-left: auto;">Чек: ~160 ₽</span>
    </div>
    <div class="recipe-body">
        <div class="ingredients-box">
            <h5>Ингредиенты:</h5>
            <ul class="ingredients-list">
                <li>Баклажан средний (180 г)</li>
                <li>Томаты спелые (120 г)</li>
                <li>Страчателла или легкий сыр (50 г)</li>
                <li>Кукурузный крахмал (1.5 ст. л.)</li>
                <li>Соус сладкий чили + кинза, кунжут</li>
            </ul>
        </div>
        <div class="steps-box">
            <h5>Приготовление:</h5>
            <ol class="steps-list">
                <li>Баклажан очистить полосками, нарезать кубиками 3х3 см.</li>
                <li>Сбрызнуть водой, обвалять в кукурузном крахмале.</li>
                <li>Обжарить в горячем масле 3–4 мин до золотистого хруста.</li>
                <li>На томаты выложить горячие баклажаны, сыр, полить чили и кинзой.</li>
            </ol>
        </div>
    </div>
    <div class="chef-tip">
        💡 <b>Секрет Анастасии:</b> Подавайте сразу горячим. Контраст хруста и нежного сыра отключает любую потребность в десерте!
    </div>
</div>

<!-- РЕЦЕПТ 9 -->
<div class="recipe-card avoid-break">
    <div class="recipe-header">
        <h3 class="recipe-name">9. Лосось в медово-горчичной глазури с брокколи на пару</h3>
        <span class="recipe-time">⏱ 18 минут</span>
    </div>
    <div class="kbzhu-bar">
        <span>Калории: <b>370 ккал</b></span>
        <span>Белки: <b>35 г</b></span>
        <span>Жиры: <b>17 г</b></span>
        <span>Углеводы: <b>12 г</b></span>
        <span style="color: #C06C4F; margin-left: auto;">Чек: ~240 ₽</span>
    </div>
    <div class="recipe-body">
        <div class="ingredients-box">
            <h5>Ингредиенты:</h5>
            <ul class="ingredients-list">
                <li>Стейк лосося или форели (180 г)</li>
                <li>Брокколи свежая или с/м (150 г)</li>
                <li>Соевый соус (1 ст. л.)</li>
                <li>Дижонская зернистая горчица (1 ч. л.)</li>
                <li>Мёд натуральный (1 ч. л.) + лимон</li>
            </ul>
        </div>
        <div class="steps-box">
            <h5>Приготовление:</h5>
            <ol class="steps-list">
                <li>Смешать соевый соус, горчицу и мёд. Обильно смазать рыбу.</li>
                <li>На противень выложить рыбу и соцветия брокколи.</li>
                <li>Запекать при 190°C ровно 12–14 минут (не пересушивать!).</li>
                <li>Подавать с долькой лимона и белым кунжутом.</li>
            </ol>
        </div>
    </div>
    <div class="chef-tip">
        💡 <b>Секрет Анастасии:</b> Омега-3 жирные кислоты лосося ускоряют ночное сжигание висцерального жира и делают кожу сияющей.
    </div>
</div>

<div class="page-break"></div>

<!-- СТРАНИЦА 7: ГОТОВЫЙ РАЦИОН НА 4 НЕДЕЛИ -->
<div class="section-header">
    <h2 class="section-title">Календарный Рацион: Сетка питания на неделю</h2>
    <span class="section-tag">Четкий план без хаоса</span>
</div>

<p style="margin-bottom: 15px; color: #555;">Пример базовой недели. Порции рассчитаны на дефицит калорий 15–20% для комфортного снижения веса от 2.5 до 4 кг в месяц без чувства голода.</p>

<div class="meal-plan-grid">
    <div class="day-card">
        <div class="day-name">Пн</div>
        <div class="day-meal"><b>Завтрак:</b> ПП-сырники с ягодами</div>
        <div class="day-meal"><b>Обед:</b> Паста с индейкой</div>
        <div class="day-meal"><b>Ужин:</b> Курочка в соусе с черри</div>
    </div>
    <div class="day-card">
        <div class="day-name">Вт</div>
        <div class="day-meal"><b>Завтрак:</b> Овсяноблин с лососем</div>
        <div class="day-meal"><b>Обед:</b> Боул с киноа и птицей</div>
        <div class="day-meal"><b>Ужин:</b> Хрустящие баклажаны</div>
    </div>
    <div class="day-card">
        <div class="day-name">Ср</div>
        <div class="day-meal"><b>Завтрак:</b> Фриттата с фетой</div>
        <div class="day-meal"><b>Обед:</b> Тыквенный суп-пюре</div>
        <div class="day-meal"><b>Ужин:</b> Боул с тунцом и фасолью</div>
    </div>
    <div class="day-card">
        <div class="day-name">Чт</div>
        <div class="day-meal"><b>Завтрак:</b> Шакшука с зеленью</div>
        <div class="day-meal"><b>Обед:</b> Паста со шпинатом</div>
        <div class="day-meal"><b>Ужин:</b> Лосось с брокколи</div>
    </div>
    <div class="day-card">
        <div class="day-name">Пт</div>
        <div class="day-meal"><b>Завтрак:</b> Сырники с вишней</div>
        <div class="day-meal"><b>Обед:</b> Боул с курицей гриль</div>
        <div class="day-meal"><b>Ужин:</b> Куриное филе с черри</div>
    </div>
    <div class="day-card">
        <div class="day-name">Сб</div>
        <div class="day-meal"><b>Завтрак:</b> Тосты с авокадо и яйцом</div>
        <div class="day-meal"><b>Обед:</b> Булгур с индейкой</div>
        <div class="day-meal"><b>Ужин:</b> Хрустящие баклажаны</div>
    </div>
    <div class="day-card">
        <div class="day-name">Вс</div>
        <div class="day-meal"><b>Завтрак:</b> Творожный мусс</div>
        <div class="day-meal"><b>Обед:</b> Тыквенный крем-суп</div>
        <div class="day-meal"><b>Ужин:</b> Запеченная рыба с салатом</div>
    </div>
</div>

<!-- УМНЫЙ СПИСОК ПОКУПОК -->
<div class="section-header" style="margin-top: 30px;">
    <h2 class="section-title">Умный Список Покупок на неделю (Супермаркет / Доставка)</h2>
    <span class="section-tag">Экономия 30% бюджета</span>
</div>

<div class="grocery-grid">
    <div class="grocery-category">
        <h4>Мясо, Птица, Рыба</h4>
        <div class="grocery-item"><div class="checkbox"></div> Филе куриной грудки — 800 г</div>
        <div class="grocery-item"><div class="checkbox"></div> Филе индейки — 600 г</div>
        <div class="grocery-item"><div class="checkbox"></div> Стейк лосося / форели — 2 шт</div>
        <div class="grocery-item"><div class="checkbox"></div> Тунец в с/с — 2 банки</div>
        <div class="grocery-item"><div class="checkbox"></div> Креветки тигровые — 300 г</div>
    </div>

    <div class="grocery-category">
        <h4>Овощи, Зелень, Ягоды</h4>
        <div class="grocery-item"><div class="checkbox"></div> Томаты черри — 2 упаковки</div>
        <div class="grocery-item"><div class="checkbox"></div> Баклажаны — 2 шт</div>
        <div class="grocery-item"><div class="checkbox"></div> Шпинат свежий — 2 пачки</div>
        <div class="grocery-item"><div class="checkbox"></div> Брокколи / стручковая фасоль — 1 пачка</div>
        <div class="grocery-item"><div class="checkbox"></div> Авокадо Хасс — 2 шт</div>
        <div class="grocery-item"><div class="checkbox"></div> Тыква баттернат — 1 шт</div>
        <div class="grocery-item"><div class="checkbox"></div> Замороженная вишня — 1 пачка</div>
    </div>

    <div class="grocery-category">
        <h4>Молочный отдел и Бакалея</h4>
        <div class="grocery-item"><div class="checkbox"></div> Творог 5% брикетный — 3 пачки</div>
        <div class="grocery-item"><div class="checkbox"></div> Яйца категории С0 — 2 десятка</div>
        <div class="grocery-item"><div class="checkbox"></div> Сыр страчателла / фета — 2 уп</div>
        <div class="grocery-item"><div class="checkbox"></div> Сливки 10% — 200 мл</div>
        <div class="grocery-item"><div class="checkbox"></div> Греческий йогурт Teos 2% — 2 банки</div>
        <div class="grocery-item"><div class="checkbox"></div> Паста твердых сортов (Barilla) — 1 уп</div>
        <div class="grocery-item"><div class="checkbox"></div> Рисовая мука + кукурузный крахмал</div>
    </div>
</div>

<div style="margin-top: 35px; text-align: center; border-top: 1px solid #EBE5DC; padding-top: 20px; color: #777; font-size: 11px;">
    <i>Материалы подготовлены эксклюзивно для резидентов закрытого кулинарного клуба Анастасии. Распространение запрещено.</i>
</div>

</body>
</html>
"""

# Сохранение HTML
with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML сохранен: {HTML_OUTPUT}")

# Конвертация в PDF через Google Chrome Headless
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={PDF_OUTPUT}",
    "--print-to-pdf-no-header",
    str(HTML_OUTPUT)
]

print("Генерация PDF через Headless Chrome...")
result = subprocess.run(cmd, capture_output=True, text=True)

if PDF_OUTPUT.exists():
    size_mb = PDF_OUTPUT.stat().st_size / (1024 * 1024)
    print(f"УСПЕХ! PDF сгенерирован: {PDF_OUTPUT} ({size_mb:.2f} MB)")
else:
    print("Ошибка генерации PDF:", result.stderr)

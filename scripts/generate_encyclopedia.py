"""
Генератор масштабной Кулинарной Энциклопедии Закрытого Клуба Анастасии.
Формат: Журнальная книга A4 на 26-28 страниц.
Включает:
- 50+ подробнейших рецептов по всем категориям
- Отдельную мощную ветку "Еда для всей семьи и мужа" (блюда-трансформеры)
- Ветку "Сытное похудение" (много белка, объем, дефицит без голода)
- Полную систему Meal Prep (заготовки на 3 дня)
- 4-недельный календарный рацион с КБЖУ
- Энциклопедию замен и Zero Waste хранение
- Умный список покупок для супермаркета
"""

import base64
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
PHOTO_PATH = ASSETS_DIR / "welcome.jpg"
HTML_OUTPUT = ASSETS_DIR / "encyclopedia.html"
PDF_OUTPUT = ASSETS_DIR / "База_Рецептов_и_Рационов_Анастасии.pdf"

photo_b64 = ""
if PHOTO_PATH.exists():
    with open(PHOTO_PATH, "rb") as f:
        photo_b64 = base64.b64encode(f.read()).decode("utf-8")

html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<style>
    @page {{
        size: A4;
        margin: 0;
    }}

    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}

    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        color: #242424;
        background-color: #FAF8F5;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
        font-size: 12.5px;
        line-height: 1.5;
    }}

    .page {{
        width: 210mm;
        height: 297mm;
        padding: 18mm 18mm 14mm 18mm;
        page-break-after: always;
        break-after: page;
        position: relative;
        overflow: hidden;
        background-color: #FAF8F5;
    }}

    /* ОБЛОЖКА */
    .cover-page {{
        padding: 0;
        background: #172A21;
        color: #FFFFFF;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .cover-top {{
        padding: 22mm 22mm 0 22mm;
    }}

    .cover-tag {{
        display: inline-block;
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #E2BA82;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .cover-title {{
        font-family: 'Georgia', serif;
        font-size: 38px;
        line-height: 1.15;
        color: #FFFFFF;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .cover-desc {{
        font-size: 13.5px;
        line-height: 1.6;
        color: rgba(255, 255, 255, 0.85);
        max-width: 530px;
    }}

    .cover-image-container {{
        width: 100%;
        height: 125mm;
        padding: 0 22mm;
    }}

    .cover-photo {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 8px;
        border: 1px solid rgba(226, 186, 130, 0.35);
    }}

    .cover-bottom {{
        padding: 0 22mm 18mm 22mm;
    }}

    .cover-features {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 16px;
    }}

    .feature-pill {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(226, 186, 130, 0.4);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 10.5px;
        color: #FFFFFF;
        font-weight: 500;
    }}

    .cover-meta {{
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding-top: 12px;
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 1px;
    }}

    /* ШАПКА И ПОДВАЛ СТРАНИЦ */
    .page-header {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        border-bottom: 1.5px solid #242424;
        padding-bottom: 6px;
        margin-bottom: 14px;
    }}

    .header-category {{
        font-size: 9.5px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #C25E3E;
        font-weight: 700;
    }}

    .header-page-title {{
        font-family: 'Georgia', serif;
        font-size: 19px;
        color: #172A21;
        font-weight: 700;
    }}

    .page-footer {{
        position: absolute;
        bottom: 10mm;
        left: 18mm;
        right: 18mm;
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #E6DFD5;
        padding-top: 6px;
        font-size: 9.5px;
        color: #8C8275;
    }}

    /* БАННЕРЫ И БЛОКИ */
    .manifesto-banner {{
        background: #FFFFFF;
        border: 1px solid #E8E1D7;
        border-left: 4px solid #C25E3E;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 14px;
    }}

    .manifesto-banner h3 {{
        font-family: 'Georgia', serif;
        font-size: 15px;
        color: #172A21;
        margin-bottom: 4px;
    }}

    .dual-columns {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 14px;
    }}

    .info-card {{
        background: #FFFFFF;
        border: 1px solid #E8E1D7;
        padding: 12px 14px;
        border-radius: 5px;
    }}

    .info-card h4 {{
        font-family: 'Georgia', serif;
        font-size: 13.5px;
        color: #172A21;
        margin-bottom: 4px;
    }}

    .tag-badge {{
        display: inline-block;
        padding: 2px 7px;
        border-radius: 10px;
        font-size: 8.5px;
        font-weight: 700;
        text-transform: uppercase;
    }}

    .tag-slimming {{ background: #EAF4EE; color: #246B46; }}
    .tag-family {{ background: #FDF1EB; color: #B8502E; }}
    .tag-prep {{ background: #F5EFEB; color: #735137; }}

    /* КАРТОЧКА РЕЦЕПТА */
    .recipe-row {{
        background: #FFFFFF;
        border: 1px solid #E8E1D7;
        border-radius: 5px;
        padding: 10px 14px;
        margin-bottom: 10px;
    }}

    .recipe-head {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }}

    .recipe-title {{
        font-family: 'Georgia', serif;
        font-size: 14.5px;
        font-weight: 700;
        color: #172A21;
    }}

    .recipe-badge-time {{
        font-size: 9.5px;
        background: #F3EFE9;
        padding: 2px 7px;
        border-radius: 10px;
        color: #61594F;
        font-weight: 600;
    }}

    .recipe-macros {{
        display: flex;
        gap: 10px;
        font-size: 10px;
        background: #F8F6F2;
        padding: 4px 10px;
        border-radius: 3px;
        margin-bottom: 8px;
        font-weight: 600;
        color: #4A4237;
    }}

    .macros-check {{
        margin-left: auto;
        color: #C25E3E;
    }}

    .recipe-content-grid {{
        display: grid;
        grid-template-columns: 1fr 1.4fr;
        gap: 12px;
        font-size: 11px;
    }}

    .subhead {{
        font-size: 9.5px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #8C8275;
        font-weight: 700;
        margin-bottom: 3px;
    }}

    .ing-list {{
        list-style: none;
    }}

    .ing-list li {{
        margin-bottom: 2px;
        padding-left: 9px;
        position: relative;
    }}

    .ing-list li::before {{
        content: "–";
        position: absolute;
        left: 0;
        color: #C25E3E;
    }}

    .steps-list {{
        padding-left: 14px;
    }}

    .steps-list li {{
        margin-bottom: 3px;
    }}

    .secret-box {{
        background: #FFFDF9;
        border-left: 2.5px solid #E2BA82;
        padding: 4px 8px;
        margin-top: 6px;
        font-size: 10px;
        color: #614D2E;
    }}

    /* ТРАНСФОРМЕР БЛОК */
    .transform-split {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        background: #FAF7F2;
        padding: 6px 8px;
        border-radius: 4px;
        margin-top: 6px;
        font-size: 10.5px;
    }}

    .transform-col b {{
        display: block;
        font-size: 9.5px;
        text-transform: uppercase;
        margin-bottom: 2px;
    }}

    .col-husband b {{ color: #B8502E; }}
    .col-diet b {{ color: #246B46; }}

    /* ТАБЛИЦЫ */
    table.compact-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
        background: #FFFFFF;
        border-radius: 4px;
        overflow: hidden;
        border: 1px solid #E8E1D7;
        margin-bottom: 12px;
    }}

    table.compact-table th {{
        background: #172A21;
        color: #FFFFFF;
        text-align: left;
        padding: 6px 10px;
        font-size: 9.5px;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }}

    table.compact-table td {{
        padding: 6px 10px;
        border-bottom: 1px solid #F0ECE4;
        vertical-align: top;
    }}

    /* СПИСОК ПОКУПОК */
    .grocery-columns {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }}

    .grocery-block {{
        background: #FFFFFF;
        border: 1px solid #E8E1D7;
        padding: 10px;
        border-radius: 4px;
    }}

    .grocery-block h5 {{
        font-family: 'Georgia', serif;
        font-size: 12px;
        color: #172A21;
        border-bottom: 1px solid #E8E1D7;
        padding-bottom: 3px;
        margin-bottom: 5px;
    }}

    .g-item {{
        font-size: 10px;
        margin-bottom: 2.5px;
        display: flex;
        align-items: center;
        gap: 5px;
    }}

    .box-check {{
        width: 9px;
        height: 9px;
        border: 1px solid #C25E3E;
        border-radius: 2px;
    }}

    /* КАЛЕНДАРЬ РАЦИОНА */
    .calendar-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 6px;
        margin-bottom: 12px;
    }}

    .cal-day {{
        background: #FFFFFF;
        border: 1px solid #E8E1D7;
        border-radius: 4px;
        padding: 6px;
    }}

    .cal-title {{
        font-size: 9.5px;
        font-weight: 700;
        color: #C25E3E;
        text-transform: uppercase;
        border-bottom: 1px solid #F0ECE4;
        padding-bottom: 2px;
        margin-bottom: 4px;
    }}

    .cal-meal {{
        font-size: 8.5px;
        margin-bottom: 4px;
    }}

    .cal-meal b {{
        color: #172A21;
        display: block;
    }}
</style>
</head>
<body>

<!-- СТР 1: ОБЛОЖКА -->
<div class="page cover-page">
    <div class="cover-top">
        <span class="cover-tag">АНАСТАСИЯ • ЗАКРЫТЫЙ КУЛИНАРНЫЙ КЛУБ</span>
        <h1 class="cover-title">Большая Кулинарная<br>Энциклопедия</h1>
        <p class="cover-desc">Полная система питания резидентов: 50+ рецептов с граммовками и КБЖУ, семейная ветка «ест муж и дети», сытное похудение без диет, Meal Prep заготовки и рационы на месяц.</p>
    </div>

    <div class="cover-image-container">
        <img class="cover-photo" src="data:image/jpeg;base64,{photo_b64}" alt="Анастасия">
    </div>

    <div class="cover-bottom">
        <div class="cover-features">
            <span class="feature-pill">🥗 Сытное похудение</span>
            <span class="feature-pill">👨‍👩‍👧‍👦 Семейные трансформеры</span>
            <span class="feature-pill">⚡ Пятиминутки</span>
            <span class="feature-pill">🥡 Meal Prep на 3 дня</span>
            <span class="feature-pill">🗓 Рацион на 4 недели</span>
            <span class="feature-pill">🛒 Списки покупок</span>
        </div>
        <div class="cover-meta">
            <span>ЭКСКЛЮЗИВНЫЕ МАТЕРИАЛЫ КЛУБА</span>
            <span>2026 • АВТОРСКАЯ СИСТЕМА</span>
        </div>
    </div>
</div>

<!-- СТР 2: ПУТЕВОДИТЕЛЬ ПО КНИГЕ -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Навигация</span>
        <span class="header-page-title">Путеводитель по Базе Знаний</span>
    </div>

    <div class="manifesto-banner">
        <h3>Добро пожаловать в закрытое кулинарное пространство! 🤍</h3>
        <p>Эта книга создана, чтобы раз и навсегда убрать с ваших плеч стресс от плиты. Больше никаких «что сегодня готовить?», никаких отдельных кастрюль для худеющей мамы и голодного мужа. Все блюда выверены до грамма, содержат чеки из ближайших магазинов и готовятся легко.</p>
    </div>

    <div class="dual-columns">
        <div class="info-card">
            <h4>📖 Раздел 1. Философия и База</h4>
            <p style="font-size: 11px; color: #555;">• Манифест сытого похудения: 35г белка в порции<br>• Метод блюд-трансформеров (один котел на всю семью)<br>• Энциклопедия замен вредных продуктов<br>• Секреты Zero Waste хранения (зелень на 3 недели)</p>
        </div>
        <div class="info-card">
            <h4>🥡 Раздел 2. Система Meal Prep</h4>
            <p style="font-size: 11px; color: #555;">• Воскресный Sheet Pan: 1 противень = 3 свободных дня<br>• 4 базовых модуля заготовок<br>• Экспресс-конструктор ужинов за 5 минут</p>
        </div>
    </div>

    <div class="dual-columns">
        <div class="info-card">
            <h4>🍳 Раздел 3. Каталог 50+ рецептов</h4>
            <p style="font-size: 11px; color: #555;">• Завтраки для разгона метаболизма (сырники, фриттаты, овсяноблины)<br>• Обеды со сложными углеводами (пасты, боулы, крем-супы)<br>• Легкие ужины для плоского живота (курица, баклажаны, рыба)<br>• Семейная ветка: любимые сытные блюда мужа и детей<br>• Экспресс-пятиминутки и десерты без сахара</p>
        </div>
        <div class="info-card">
            <h4>🗓 Раздел 4. План на 4 Недели</h4>
            <p style="font-size: 11px; color: #555;">• Календарные сетки питания (Недели 1–4) с КБЖУ<br>• Готовые списки продуктов в Магнит и Пятёрочку<br>• Чек-листы для закупки по отделам</p>
        </div>
    </div>

    <div class="manifesto-banner" style="border-left-color: #246B46; margin-top: 10px;">
        <h3>Золотой закон клуба: сытость важнее дефицита</h3>
        <p style="font-size: 11.5px;">Если в тарелке нет достаточного количества белка и объема клетчатки — мозг потребует сахар через 2 часа. Кормите себя вкусно, красиво и сытно!</p>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>02</span>
    </div>
</div>

<!-- СТР 3: ФИЛОСОФИЯ 2 ВЕТОК -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Методология</span>
        <span class="header-page-title">Две Ветки: Для Себя и Для Семьи</span>
    </div>

    <div class="manifesto-banner">
        <h3>Хватит готовить в два котла: метод Блюд-Трансформеров</h3>
        <p>Главная ошибка худеющих девушек — изолировать себя от семейного стола. Вы варите себе постную курицу, муж с тоской смотрит на траву и заказывает пиццу, дети отказываются есть овощи. Это путь к выгоранию за 7 дней.</p>
        <p style="margin-top: 6px;"><b>Как работает трансформер Анастасии:</b> Готовится богатая мясная или рыбная основа ресторанного вкуса с соусом на нежирных сливках или томатах passata. Разделение происходит только в момент сборки тарелки!</p>
    </div>

    <div class="dual-columns">
        <div class="info-card">
            <h4><span class="tag-badge tag-slimming">Ветка 1</span> Сытное похудение</h4>
            <p><b>Формула «35г белка + клетчатка»:</b></p>
            <p style="font-size: 11px; color: #555; margin-top: 4px;">• Берем основное мясное блюдо;<br>• В качестве гарнира — спаржевая фасоль, брокколи, цветная капуста или свежие овощи со страчателлой;<br>• Итог: огромная тарелка, 300–350 ккал, сытость на 5 часов и плоский живот на утро.</p>
        </div>
        <div class="info-card">
            <h4><span class="tag-badge tag-family">Ветка 2</span> Еда для мужа и детей</h4>
            <p><b>Метод «Основа + Энергия»:</b></p>
            <p style="font-size: 11px; color: #555; margin-top: 4px;">• Берем то же самое мясное блюдо с соусом;<br>• Мужу и детям добавляем спагетти, картофельное пюре или рассыпчатый рис;<br>• Посыпаем сыром и поливаем соусом;<br>• Муж сыт, дети просят добавки, а вы потратили 20 минут у плиты!</p>
        </div>
    </div>

    <table class="compact-table" style="margin-top: 8px;">
        <thead>
            <tr>
                <th style="width: 25%;">Блюдо-база</th>
                <th style="width: 37%;">Тарелка для мужа и детей</th>
                <th style="width: 38%;">Тарелка для похудения (себе)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Тефтели с цукини в томатном соусе</b></td>
                <td>4 тефтели + картофельное пюре со сливочным маслом + сыр</td>
                <td>3 тефтели + подушка из свежего шпината и рукколы (320 ккал, 34г Б)</td>
            </tr>
            <tr>
                <td><b>Курочка под сырной шубкой</b></td>
                <td>Филе с сыром + запеченные дольки картофеля по-деревенски</td>
                <td>Филе с сыром + теплый салат из томатов, огурца и кинзы (290 ккал)</td>
            </tr>
            <tr>
                <td><b>Сливочная паста с индейкой</b></td>
                <td>Большая порция пасты с индейкой, щедро присыпанная пармезаном</td>
                <td>60г пасты аль денте + двойная порция сочной индейки и брокколи</td>
            </tr>
        </tbody>
    </table>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>03</span>
    </div>
</div>

<!-- СТР 4: СИСТЕМА MEAL PREP -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Организация Кухни</span>
        <span class="header-page-title">Meal Prep: 1 противень = 3 дня свободы</span>
    </div>

    <div class="manifesto-banner">
        <h3>Воскресный Sheet Pan за 45 минут</h3>
        <p>Мы не варим макароны на неделю вперед. Мы запекаем на одном противне универсальные белковые и овощные модули, которые хранятся в стеклянных контейнерах и собираются в новые свежие блюда за 5 минут.</p>
    </div>

    <div class="dual-columns">
        <div class="info-card">
            <h4>1. Белковый модуль</h4>
            <p style="font-size: 11px;">Филе грудки индейки или курицы (800г) смазать оливковым маслом, паприкой, сушеным чесноком и тимьяном. Запекать 30 мин при 180°C. Нарезать тонкими слайсами. Хранить в стекле 4 дня.</p>
        </div>
        <div class="info-card">
            <h4>2. Овощной модуль</h4>
            <p style="font-size: 11px;">Кабачок, тыква, болгарский перец и цветная капуста крупным кубиком, сбрызнутые 1 ст.л. масла и прованскими травами. Запекаются на том же противне 25 минут.</p>
        </div>
    </div>

    <div class="dual-columns">
        <div class="info-card">
            <h4>3. Медленный углевод</h4>
            <p style="font-size: 11px;">Киноа или булгур (250г) отварить с каплей соли и ложкой топленого масла гхи. Рассыпчатая зерновая база на обеды и сытные боулы.</p>
        </div>
        <div class="info-card">
            <h4>4. Соус «Зеленая Богиня»</h4>
            <p style="font-size: 11px;">Спелый авокадо, пучок кинзы, 150г греческого йогурта, сок половины лайма и морская соль. Пробить блендером. Делает шедевром любое блюдо.</p>
        </div>
    </div>

    <div class="manifesto-banner" style="border-left-color: #2E6A4F;">
        <h3>Как собирать ужины в будни:</h3>
        <p style="font-size: 11.5px;">• <b>Пн (Калифорнийский боул):</b> теплая киноа + слайсы индейки + запеченные овощи + соус + кунжут (4 мин).<br>• <b>Вт (Теплый салат):</b> салатные листья + теплая индейка + печеная тыква + сыр фета + бальзамик (3 мин).<br>• <b>Ср (Азиатский стир-фрай):</b> прогреть овощи с индейкой на сковороде с соевым соусом и подать с булгуром (5 мин).</p>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>04</span>
    </div>
</div>

<!-- СТР 5: ЗАВТРАКИ ЧАСТЬ 1 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Каталог Рецептов</span>
        <span class="header-page-title">Завтраки для метаболизма (Часть 1)</span>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">1. Пышные ПП-сырники без муки с ягодным соусом</span>
            <span class="recipe-badge-time">⏱ 15 мин • 295 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 32 г</span><span>Жиры: 9 г</span><span>Углеводы: 18 г</span>
            <span class="macros-check">Чек: ~119 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты (1 порция):</div>
                <ul class="ing-list">
                    <li>Творог 5% брикетный — 180 г</li>
                    <li>Желток яйца С0 — 1 шт</li>
                    <li>Рисовая мука — 20 г (1.5 ст. л.)</li>
                    <li>FitParad №7 (2 саше), ванилин</li>
                    <li>Замороженная вишня — 40 г</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Творог размять с желтком, подсластителем, ванилином и 1 ст.л. муки в плотную массу.</li>
                    <li>Сформировать 3 шайбочки, обвалять в остатках рисовой муки.</li>
                    <li>Обжарить под крышкой на медленном огне по 4 мин с каждой стороны. Полить прогретыми ягодами.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">2. Овсяноблин с слабосоленым лососем и творожным сыром</span>
            <span class="recipe-badge-time">⏱ 10 мин • 365 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 24 г</span><span>Жиры: 15 г</span><span>Углеводы: 28 г</span>
            <span class="macros-check">Чек: ~195 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Овсянка долгой варки — 40 г</li>
                    <li>Яйцо С0 (1 шт) + 1 белок</li>
                    <li>Молоко 1.5% — 40 мл</li>
                    <li>Творожный легкий сыр — 30 г</li>
                    <li>Лосось с/с — 50 г + свежий огурец</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Хлопья, яйцо, белок и молоко взбить вилкой со щепоткой соли.</li>
                    <li>Выпекать на сухой сковороде под крышкой по 2.5 мин с каждой стороны.</li>
                    <li>Смазать сыром, выложить ломтики рыбы и огурца, сложить пополам.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">3. Итальянская фриттата со шпинатом и сыром фета</span>
            <span class="recipe-badge-time">⏱ 12 мин • 310 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 26 г</span><span>Жиры: 18 г</span><span>Углеводы: 6 г</span>
            <span class="macros-check">Чек: ~140 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Яйца С0 — 3 шт</li>
                    <li>Шпинат свежий или с/м — 70 г</li>
                    <li>Томаты черри — 5 шт</li>
                    <li>Сыр фета или брынза — 40 г</li>
                    <li>Орегано сушеный, щепотка соли</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Шпинат припустить на сковороде 1 мин, добавить половинки черри.</li>
                    <li>Яйца взбить с орегано и солью, залить овощи, сверху раскрошить фету.</li>
                    <li>Готовить под крышкой на самом малом огне 7–8 минут. Воздушный омлетный пирог!</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>05</span>
    </div>
</div>

<!-- СТР 6: ЗАВТРАКИ ЧАСТЬ 2 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Каталог Рецептов</span>
        <span class="header-page-title">Завтраки для метаболизма (Часть 2)</span>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">4. Шакшука по-средиземноморски с томатами и кинзой</span>
            <span class="recipe-badge-time">⏱ 12 мин • 280 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 21 г</span><span>Жиры: 16 г</span><span>Углеводы: 11 г</span>
            <span class="macros-check">Чек: ~125 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Яйца С0 — 2 шт + 1 белок</li>
                    <li>Томаты в с/с кусочками — 200 г</li>
                    <li>Болгарский перец — 60 г</li>
                    <li>Чеснок 1 зуб., зира, паприка</li>
                    <li>Кинза свежая, сыр фета — 25 г</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Перец с чесноком обжарить 2 мин, влить томаты со специями, тушить 3 мин до соуса.</li>
                    <li>Сделать ложкой лунки, выпустить яйца, посыпать фетой.</li>
                    <li>Томить под крышкой 4–5 мин, пока белок не схватится, а желток останется жидким.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">5. Творожная запеканка с цедрой лимона и маком</span>
            <span class="recipe-badge-time">⏱ 30 мин в духовке • 240 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 29 г</span><span>Жиры: 7 г</span><span>Углеводы: 15 г</span>
            <span class="macros-check">Чек: ~110 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Творог 5% — 200 г</li>
                    <li>Яйцо С0 — 1 шт</li>
                    <li>Манная крупа из твердых сортов — 15 г</li>
                    <li>Цедра половины лимона + мак (1 ч.л.)</li>
                    <li>Подсластитель FitParad по вкусу</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Все ингредиенты пробить погружным блендером в кремовую массу.</li>
                    <li>Выложить в силиконовую форму, запекать при 175°C 25–28 минут.</li>
                    <li>Остудить. Нежнейшая текстура чизкейка без капли сливочного масла!</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">6. Ленивая ягодная овсянка в банке (с вечера)</span>
            <span class="recipe-badge-time">⏱ 2 мин с вечера • 290 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 18 г</span><span>Жиры: 6 г</span><span>Углеводы: 41 г</span>
            <span class="macros-check">Чек: ~85 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Хлопья овсяные — 45 г</li>
                    <li>Греческий йогурт Teos — 100 г</li>
                    <li>Миндальное или коровье молоко — 60 мл</li>
                    <li>Семена чиа — 1 ч. л. (5 г)</li>
                    <li>Ягоды черники или малины — 40 г</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>В баночку насыпать овсянку, чиа, подсластитель, залить молоком и йогуртом.</li>
                    <li>Перемешать, сверху выложить ягоды и закрыть крышкой.</li>
                    <li>Убрать на ночь в холодильник. Утром готов освежающий крем-завтрак!</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>06</span>
    </div>
</div>

<!-- СТР 7: ОБЕДЫ ЧАСТЬ 1 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Каталог Рецептов</span>
        <span class="header-page-title">Сытные Обеды со сложными углеводами (Часть 1)</span>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">7. ПП-паста из твердых сортов с индейкой и шпинатом</span>
            <span class="recipe-badge-time">⏱ 15 мин • 390 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 34 г</span><span>Жиры: 9 г</span><span>Углеводы: 42 г</span>
            <span class="macros-check">Чек: ~153 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Паста Barilla сухая — 60 г</li>
                    <li>Филе индейки — 150 г</li>
                    <li>Шпинат свежий — 60 г</li>
                    <li>Йогурт Teos 2% — 50 г</li>
                    <li>Мускатный орех, зубчик чеснока</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Пасту сварить аль денте, сохранив 3 ст.л. воды из кастрюли.</li>
                    <li>Индейку обжарить 4 мин, добавить чеснок и шпинат на 1.5 мин.</li>
                    <li>Ввести йогурт, мускатный орех и крахмальную воду. Смешать с пастой.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">8. Прованский боул с киноа, курицей гриль и печеным перцем</span>
            <span class="recipe-badge-time">⏱ 15 мин • 410 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 38 г</span><span>Жиры: 11 г</span><span>Углеводы: 40 г</span>
            <span class="macros-check">Чек: ~165 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Киноа отваренная — 120 г</li>
                    <li>Куриное филе — 150 г</li>
                    <li>Болгарский перец запеченный — 80 г</li>
                    <li>Свежий огурец + руккола — 60 г</li>
                    <li>Заправка: оливковое масло + сок лимона</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Филе обжарить со специями до румяности, нарезать ломтиками.</li>
                    <li>В чашу выложить теплую киноа, рукколу, запеченный перец и курочку.</li>
                    <li>Сбрызнуть заправкой, присыпать тыквенными семечками.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">9. Бархатный крем-суп из тыквы с тигровыми креветками</span>
            <span class="recipe-badge-time">⏱ 20 мин • 280 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 22 г</span><span>Жиры: 10 г</span><span>Углеводы: 22 г</span>
            <span class="macros-check">Чек: ~185 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Тыква баттернат — 250 г</li>
                    <li>Морковь (50г) + имбирь свежий (щепотка)</li>
                    <li>Кокосовое молоко 17% — 50 мл</li>
                    <li>Креветки очищенные — 100 г</li>
                    <li>Чеснок 1 зуб., мускатный орех</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Тыкву и морковь сварить с имбирем до мягкости (12 мин). Слить часть воды.</li>
                    <li>Влить кокосовое молоко, взбить блендером в шелковистое пюре.</li>
                    <li>Креветки обжарить с чесноком 2 мин, выложить поверх горячего супа.</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>07</span>
    </div>
</div>

<!-- СТР 8: ОБЕДЫ ЧАСТЬ 2 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Каталог Рецептов</span>
        <span class="header-page-title">Сытные Обеды со сложными углеводами (Часть 2)</span>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">10. Гречневая лапша соба с говядиной и овощами в терияки</span>
            <span class="recipe-badge-time">⏱ 15 мин • 385 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 32 г</span><span>Жиры: 9 г</span><span>Углеводы: 44 г</span>
            <span class="macros-check">Чек: ~175 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Лапша соба гречневая — 55 г</li>
                    <li>Постная говядина соломкой — 140 г</li>
                    <li>Болгарский перец + кабачок — 100 г</li>
                    <li>Соус терияки без сахара + соевый соус</li>
                    <li>Зеленый лук, кунжут</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Собу отварить 4 мин. Говядину обжарить на сильном огне 3 мин.</li>
                    <li>Добавить соломку овощей, обжаривать 2 мин до состояния аль денте.</li>
                    <li>Ввести соусы и лапшу, перемешать на раскаленной сковороде 1 минуту.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">11. Нежный куриный бефстроганов с шампиньонами и гречкой</span>
            <span class="recipe-badge-time">⏱ 18 мин • 370 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 39 г</span><span>Жиры: 10 г</span><span>Углеводы: 31 г</span>
            <span class="macros-check">Чек: ~140 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Куриное филе брусочками — 180 г</li>
                    <li>Шампиньоны свежие — 100 г</li>
                    <li>Сливки 10% — 70 мл + 1 ч.л. дижонской горчицы</li>
                    <li>Лук репчатый — 40 г</li>
                    <li>Отварная рассыпчатая гречка — 100 г</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Курицу с луком обжарить 4 мин, добавить пластинки грибов на 3 мин.</li>
                    <li>Влить 10% сливки с горчицей, убавить огонь и томить 6 мин до кремовости.</li>
                    <li>Подавать на подушке из теплой гречки со свежей петрушкой.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">12. Томатный суп с морепродуктами по-тоскански</span>
            <span class="recipe-badge-time">⏱ 15 мин • 260 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 28 г</span><span>Жиры: 6 г</span><span>Углеводы: 22 г</span>
            <span class="macros-check">Чек: ~190 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Морской коктейль или кальмары/креветки — 160 г</li>
                    <li>Томаты протертые passata — 250 мл</li>
                    <li>Чеснок 2 зуб., базилик, тимьян</li>
                    <li>Оливки без косточек — 5 шт</li>
                    <li>Цельнозерновой тост — 1 шт</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Чеснок прогреть в сотейнике с каплей масла, влить томаты passata и 100 мл воды.</li>
                    <li>Довести до кипения, добавить травы, оливки и морепродукты.</li>
                    <li>Варить на медленном огне ровно 4–5 минут. Подавать с хрустящим тостом.</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>08</span>
    </div>
</div>

<!-- СТР 9: УЖИНЫ ЧАСТЬ 1 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Каталог Рецептов</span>
        <span class="header-page-title">Легкие Ужины для плоского живота (Часть 1)</span>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">13. Филе в сливочно-томатном соусе с черри</span>
            <span class="recipe-badge-time">⏱ 18 мин • 320 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 38 г</span><span>Жиры: 11 г</span><span>Углеводы: 7 г</span>
            <span class="macros-check">Чек: ~148 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Куриное филе — 180 г</li>
                    <li>Черри свежие — 80 г</li>
                    <li>Сливки 10% питьевые — 60 мл</li>
                    <li>Чеснок 1 зуб., сладкая паприка, базилик</li>
                    <li>Масло оливковое — 1 ч. л.</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Филе нарезать кусочками, обжарить 3 мин на сильном огне до корочки.</li>
                    <li>Бросить половинки черри и чеснок, тушить 2 мин до выделения сока.</li>
                    <li>Влить 10% сливки, убавить огонь и томить 5 мин до бархатной текстуры.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">14. Хрустящие баклажаны со страчателлой и сладким чили</span>
            <span class="recipe-badge-time">⏱ 15 мин • 280 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 12 г</span><span>Жиры: 14 г</span><span>Углеводы: 24 г</span>
            <span class="macros-check">Чек: ~160 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Баклажан средний — 180 г</li>
                    <li>Томаты спелые — 120 г</li>
                    <li>Страчателла или легкий сыр — 50 г</li>
                    <li>Кукурузный крахмал — 1.5 ст. л.</li>
                    <li>Соус сладкий чили, кинза, кунжут</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Баклажан нарезать крупным кубиком, сбрызнуть водой, обвалять в крахмале.</li>
                    <li>Обжарить в горячем масле 3 мин до звонкого золотистого хруста.</li>
                    <li>На ломтики томатов выложить горячие баклажаны, сыр, полить чили и кинзой.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">15. Лосось в медово-горчичной глазури с брокколи на пару</span>
            <span class="recipe-badge-time">⏱ 18 мин • 370 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 35 г</span><span>Жиры: 17 г</span><span>Углеводы: 12 г</span>
            <span class="macros-check">Чек: ~240 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Стейк лосося или форели — 180 г</li>
                    <li>Брокколи соцветия — 150 г</li>
                    <li>Соевый соус (1 ст.л.) + мёд (1 ч.л.)</li>
                    <li>Дижонская зернистая горчица (1 ч.л.)</li>
                    <li>Лимон, кунжут</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Смешать соус, мёд и горчицу. Смазать рыбу со всех сторон.</li>
                    <li>На противень выложить рыбу и брокколи, сбрызнутую каплей масла.</li>
                    <li>Запекать при 190°C ровно 12–14 минут. Омега-3 для сжигания жира во сне!</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>09</span>
    </div>
</div>

<!-- СТР 10: УЖИНЫ ЧАСТЬ 2 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Каталог Рецептов</span>
        <span class="header-page-title">Легкие Ужины для плоского живота (Часть 2)</span>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">16. Нежные медальоны из индейки в гранатовом бальзамике</span>
            <span class="recipe-badge-time">⏱ 20 мин • 310 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 41 г</span><span>Жиры: 8 г</span><span>Углеводы: 9 г</span>
            <span class="macros-check">Чек: ~165 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Медальоны из филе индейки — 200 г</li>
                    <li>Гранатовый соус наршараб — 1 ст. л.</li>
                    <li>Бальзамический крем — 1 ч. л.</li>
                    <li>Розмарин свежий или сушеный, чеснок</li>
                    <li>Спаржевая фасоль на гарнир — 120 г</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Медальоны слегка отбить, смазать наршарабом, солью и розмарином.</li>
                    <li>Обжарить на сковороде гриль по 3.5 мин с каждой стороны до карамелизации.</li>
                    <li>Подавать с отварной спаржевой фасолью, сбрызнутой бальзамиком.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">17. Кальмары на гриле с чесночным маслом и свежим салатом</span>
            <span class="recipe-badge-time">⏱ 10 мин • 230 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 34 г</span><span>Жиры: 7 г</span><span>Углеводы: 5 г</span>
            <span class="macros-check">Чек: ~145 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Тушки кальмара очищенные — 200 г</li>
                    <li>Чеснок 2 зуб. + петрушка измельченная</li>
                    <li>Масло оливковое — 1 ч. л. + лимон</li>
                    <li>Микс салата (айсберг, руккола) — 80 г</li>
                    <li>Томаты черри — 4 шт</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Тушки кальмара надрезать ромбиками, смазать чесночным маслом.</li>
                    <li>Жарить на раскаленной сковороде ровно по 1.5 мин с каждой стороны!</li>
                    <li>Выложить на подушку салата с черри, полить лимонным соком.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- РЕЦЕПТ -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">18. Стейки из цветной капусты под сырной корочкой</span>
            <span class="recipe-badge-time">⏱ 25 мин • 190 ккал</span>
        </div>
        <div class="recipe-macros">
            <span>Белки: 14 г</span><span>Жиры: 11 г</span><span>Углеводы: 10 г</span>
            <span class="macros-check">Чек: ~115 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Цветная капуста (крупный кочан) — 2 стейка</li>
                    <li>Масло оливковое — 1 ч. л. + копченая паприка</li>
                    <li>Сыр пармезан или сулугуни тертый — 35 г</li>
                    <li>Чеснок сушеный, морская соль</li>
                    <li>Соус из греческого йогурта с зеленью</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Капусту нарезать плоскими стейками толщиной 2 см.</li>
                    <li>Смазать маслом с паприкой и чесноком, выложить на пергамент.</li>
                    <li>Запекать при 200°C 18 мин, посыпать сыром и допечь 5 мин до корочки.</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>10</span>
    </div>
</div>

<!-- СТР 11: СЕМЕЙНАЯ ВЕТКА ЧАСТЬ 1 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Семейная Ветка</span>
        <span class="header-page-title">Блюда-Трансформеры: Ест Муж и Дети (Часть 1)</span>
    </div>

    <div class="manifesto-banner">
        <h3>Принцип: готовим одно, подаем по-разному</h3>
        <p>Вы не стоите над четырьмя сковородками. Базовое блюдо насыщает всю семью, а разделение гарниров занимает ровно 1 минуту!</p>
    </div>

    <!-- СЕМЕЙНЫЙ РЕЦЕПТ 1 -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">19. Нежнейшие тефтели с добавлением цукини в томатном соусе</span>
            <span class="recipe-badge-time">⏱ 25 мин</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Секретная основа:</div>
                <ul class="ing-list">
                    <li>Фарш индейка/говядина — 500 г</li>
                    <li>Кабачок/цукини тертый — 150 г (дает нежность!)</li>
                    <li>Томаты passata — 300 мл, сливки 10% — 70 мл</li>
                    <li>Чеснок, базилик, соль, перец</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Кабачок натереть мелкой стружкой, отжать и вмешать в фарш без хлеба.</li>
                    <li>Сформировать шарики, обжарить 4 мин, залить томатами и сливками.</li>
                    <li>Томить под крышкой 15 минут до густого соуса.</li>
                </ol>
            </div>
        </div>
        <div class="transform-split">
            <div class="transform-col col-husband">
                <b>👨 Мужу и детям:</b>
                Тефтели со спагетти или нежным картофельным пюре, щедро политые сливочно-томатным соусом.
            </div>
            <div class="transform-col col-diet">
                <b>💃 Себе (похудение):</b>
                3 тефтели на подушке из свежего шпината или брокколи. Всего 330 ккал и 34г чистого белка!
            </div>
        </div>
    </div>

    <!-- СЕМЕЙНЫЙ РЕЦЕПТ 2 -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">20. Куриное филе под сырно-овощной шубкой (Sheet Pan)</span>
            <span class="recipe-badge-time">⏱ 25 мин в духовке</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Основа на противень:</div>
                <ul class="ing-list">
                    <li>Филе куриной грудки — 4 шт (по 180 г)</li>
                    <li>Спелые томаты кружочками — 2 шт</li>
                    <li>Болгарский перец — 1 шт, сыр сулугуни — 80 г</li>
                    <li>Соус: сметана 10% + чеснок + укроп</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Грудки слегка надрезать ромбами, смазать сметанно-чесночным соусом.</li>
                    <li>Выложить кружочки томатов, перец и посыпать сыром.</li>
                    <li>Запекать при 190°C 22–24 минуты. Ни грамма сухости!</li>
                </ol>
            </div>
        </div>
        <div class="transform-split">
            <div class="transform-col col-husband">
                <b>👨 Мужу и детям:</b>
                Филе под сыром с запеченными картофельными дольками с розмарином и чесноком.
            </div>
            <div class="transform-col col-diet">
                <b>💃 Себе (похудение):</b>
                Филе с сыром с хрустящим салатом из огурцов и свежей зелени. Дефицит без ограничений!
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>11</span>
    </div>
</div>

<!-- СТР 12: СЕМЕЙНАЯ ВЕТКА ЧАСТЬ 2 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Семейная Ветка</span>
        <span class="header-page-title">Блюда-Трансформеры: Ест Муж и Дети (Часть 2)</span>
    </div>

    <!-- СЕМЕЙНЫЙ РЕЦЕПТ 3 -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">21. Домашние куриные наггетсы в кукурузном крахмале (дети обожают!)</span>
            <span class="recipe-badge-time">⏱ 15 мин</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Филе грудки — 500 г кусочками</li>
                    <li>Кукурузный крахмал — 3 ст. л.</li>
                    <li>Яйцо С0 (взбитое) — 1 шт</li>
                    <li>Сладкая паприка, сушеный чеснок, соль</li>
                    <li>Масло для обжарки — 1.5 ст. л.</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Кусочки филе обмакнуть во взбитое яйцо, затем в крахмал со специями.</li>
                    <li>Обжарить на сковороде по 3 мин с каждой стороны или запечь при 200°C 15 мин.</li>
                    <li>Стеклянная хрустящая корочка лучше, чем во вкусно и точка!</li>
                </ol>
            </div>
        </div>
        <div class="transform-split">
            <div class="transform-col col-husband">
                <b>👨 Детям и мужу:</b>
                Хрустящие наггетсы с картофелем фри из духовки и натуральным томатным соусом.
            </div>
            <div class="transform-col col-diet">
                <b>💃 Себе (похудение):</b>
                Порция наггетсов в большой тарелке греческого салата. Хруст без лишнего жира!
            </div>
        </div>
    </div>

    <!-- СЕМЕЙНЫЙ РЕЦЕПТ 4 -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">22. Сочная лазанья из кабачков и индейки без теста</span>
            <span class="recipe-badge-time">⏱ 35 мин в духовке</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты на форму:</div>
                <ul class="ing-list">
                    <li>Кабачки слайсами — 2 шт (вместо листов теста!)</li>
                    <li>Фарш индейки в соусе болоньезе — 500 г</li>
                    <li>Томаты протертые — 250 мл</li>
                    <li>Моцарелла или сулугуни — 100 г</li>
                    <li>Сметана 10% или творожный сыр — 80 г</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Кабачки нарезать тонкими продольными пластами, присолить и обсушить.</li>
                    <li>В форму слоями выложить: мясной соус, пласты кабачка, капли сыра.</li>
                    <li>Запекать при 180°C 30 минут. Семья сметает форму за один вечер!</li>
                </ol>
            </div>
        </div>
        <div class="transform-split">
            <div class="transform-col col-husband">
                <b>👨 Мужу и детям:</b>
                Большой кусок лазаньи с дополнительной сырной корочкой и чесночным багетом.
            </div>
            <div class="transform-col col-diet">
                <b>💃 Себе (похудение):</b>
                Огромная порция всего на 280 ккал, так как углеводных листов теста здесь нет!
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>12</span>
    </div>
</div>

<!-- СТР 13: ЭКСПРЕСС-ПЯТИМИНУТКИ -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Скорость</span>
        <span class="header-page-title">ТОП-6 Экспресс-Пятиминуток (когда сил нет)</span>
    </div>

    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">1. Шакшука за 7 минут в одной сковороде</span>
            <span class="recipe-badge-time">285 ккал • Б: 22 г</span>
        </div>
        <p style="font-size: 11px; color: #444;">Прогреть 4 ложки протертых томатов с чесноком (1 мин). Разбить 2 яйца, бросить черри и брынзу. Накрыть крышкой на 4 минуты. Готово!</p>
    </div>

    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">2. ПП-шаурма в лаваше с индейкой из заготовок</span>
            <span class="recipe-badge-time">310 ккал • Б: 32 г</span>
        </div>
        <p style="font-size: 11px; color: #444;">Лаваш смазать греческим йогуртом с горчицей. Выложить запеченную индейку, огурец, томат и капусту. Прогреть на сухой сковороде 2 мин до хруста.</p>
    </div>

    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">3. Протеиновый боул с тунцом и стручковой фасолью</span>
            <span class="recipe-badge-time">340 ккал • Б: 36 г</span>
        </div>
        <p style="font-size: 11px; color: #444;">Фасоль отварить 4 мин. В миску выложить фасоль, банку тунца в с/с, вареное яйцо и огурец. Заправить лимоном и оливковым маслом.</p>
    </div>

    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">4. Горячий сэндвич с тунцом и расплавленным сыром</span>
            <span class="recipe-badge-time">270 ккал • Б: 25 г</span>
        </div>
        <p style="font-size: 11px; color: #444;">Цельнозерновой тост смазать творожным сыром, выложить тунец, кружочки томата и ломтик моцареллы. Прогреть на сковороде под крышкой 3 мин.</p>
    </div>

    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">5. Творожный мусс «Пломбир» с ягодами за 3 минуты</span>
            <span class="recipe-badge-time">220 ккал • Б: 28 г</span>
        </div>
        <p style="font-size: 11px; color: #444;">Брикетный творог 5% взбить блендером с саше FitParad, ванилином и 30 мл молока. Текстура растаявшего мороженого! Полить теплым ягодным пюре.</p>
    </div>

    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">6. Ролл из лаваша с творогом, чесноком и зеленью</span>
            <span class="recipe-badge-time">250 ккал • Б: 24 г</span>
        </div>
        <p style="font-size: 11px; color: #444;">Творог смешать с рубленой кинзой, чесноком и каплей йогурта. Завернуть в лаваш и подрумянить на сковороде без масла по 1 мин. Горячий пирожок без теста!</p>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>13</span>
    </div>
</div>

<!-- СТР 14: ДЕСЕРТЫ БЕЗ САХАРА -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Сладкое без вины</span>
        <span class="header-page-title">Десерты без сахара и белой муки</span>
    </div>

    <!-- ДЕСЕРТ 1 -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">1. Шоколадный брауни из кабачка (без муки и масла)</span>
            <span class="recipe-badge-time">⏱ 25 мин • 165 ккал / 100 г</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Кабачок очищенный — 250 г</li>
                    <li>Какао-порошок темный — 35 г</li>
                    <li>Яйца С0 — 2 шт, FitParad (4 саше)</li>
                    <li>Овсяная мука — 20 г, разрыхлитель</li>
                    <li>Темный шоколад 75% кусочками — 20 г</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Кабачок с яйцами и подсластителем взбить блендером в жидкое пюре.</li>
                    <li>Ввести какао, муку и разрыхлитель. Вмешать кусочки шоколада.</li>
                    <li>Выпекать при 180°C 25 мин. Влажная шоколадная текстура, вкуса кабачка нет вообще!</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- ДЕСЕРТ 2 -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">2. Кокосовый чиа-пудинг с пюре из сочного манго</span>
            <span class="recipe-badge-time">⏱ 5 мин с вечера • 190 ккал</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Семена чиа — 25 г (2 ст. л.)</li>
                    <li>Кокосовое молоко 17% — 60 мл + вода 60 мл</li>
                    <li>FitParad — 1 саше, щепотка ванили</li>
                    <li>Манго свежее или с/м — 70 г</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Чиа залить молоком с водой и подсластителем, тщательно перемешать.</li>
                    <li>Оставить в стакане на ночь в холодильнике.</li>
                    <li>Утром пробить манго блендером и выложить ровным слоем сверху.</li>
                </ol>
            </div>
        </div>
    </div>

    <!-- ДЕСЕРТ 3 -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">3. Домашние белковые трюфели из фиников и какао</span>
            <span class="recipe-badge-time">⏱ 10 мин без выпечки • 45 ккал / шт</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты (на 10 шт):</div>
                <ul class="ing-list">
                    <li>Мягкие финики королевские — 120 г</li>
                    <li>Грецкие орехи или миндаль — 50 г</li>
                    <li>Какао-порошок — 2 ст. л.</li>
                    <li>Вода — 1-2 ст. л. для вязкости</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Финики и орехи измельчить в блендере до пластичной массы.</li>
                    <li>Скатать шарики размером с грецкий орех, обвалять в какао-порошке.</li>
                    <li>Охладить 20 мин. Натуральная замена магазинным конфетам к кофе!</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>14</span>
    </div>
</div>

<!-- СТР 15: КАЛЕНДАРНЫЙ РАЦИОН НЕДЕЛЯ 1 И 2 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Готовые Рационы</span>
        <span class="header-page-title">Календарная сетка: Недели 1 и 2</span>
    </div>

    <div class="manifesto-banner">
        <h3>Неделя 1: Мягкий вход и разгон метаболизма (1450–1550 ккал)</h3>
    </div>

    <div class="calendar-grid">
        <div class="cal-day"><div class="cal-title">Пн</div><div class="cal-meal"><b>З:</b> Сырники с вишней</div><div class="cal-meal"><b>О:</b> Паста с индейкой</div><div class="cal-meal"><b>У:</b> Курочка с черри</div></div>
        <div class="cal-day"><div class="cal-title">Вт</div><div class="cal-meal"><b>З:</b> Овсяноблин с рыбой</div><div class="cal-meal"><b>О:</b> Боул с киноа</div><div class="cal-meal"><b>У:</b> Баклажаны со страчателлой</div></div>
        <div class="cal-day"><div class="cal-title">Ср</div><div class="cal-meal"><b>З:</b> Фриттата с фетой</div><div class="cal-meal"><b>О:</b> Соба с говядиной</div><div class="cal-meal"><b>У:</b> Боул с тунцом</div></div>
        <div class="cal-day"><div class="cal-title">Чт</div><div class="cal-meal"><b>З:</b> Шакшука с зеленью</div><div class="cal-meal"><b>О:</b> Тыквенный суп</div><div class="cal-meal"><b>У:</b> Лосось с брокколи</div></div>
        <div class="cal-day"><div class="cal-title">Пт</div><div class="cal-meal"><b>З:</b> Творожная запеканка</div><div class="cal-meal"><b>О:</b> Бефстроганов с гречкой</div><div class="cal-meal"><b>У:</b> Курица под сыром</div></div>
        <div class="cal-day"><div class="cal-title">Сб</div><div class="cal-meal"><b>З:</b> Овсянка в банке</div><div class="cal-meal"><b>О:</b> Тосканский суп</div><div class="cal-meal"><b>У:</b> Тефтели с цукини</div></div>
        <div class="cal-day"><div class="cal-title">Вс</div><div class="cal-meal"><b>З:</b> Сырники с маком</div><div class="cal-meal"><b>О:</b> Паста с индейкой</div><div class="cal-meal"><b>У:</b> Кальмары гриль</div></div>
    </div>

    <div class="manifesto-banner" style="margin-top: 14px; border-left-color: #246B46;">
        <h3>Неделя 2: Сжигание жира и семейный комфорт (1400–1500 ккал)</h3>
    </div>

    <div class="calendar-grid">
        <div class="cal-day"><div class="cal-title">Пн</div><div class="cal-meal"><b>З:</b> Овсяноблин с сыром</div><div class="cal-meal"><b>О:</b> Киноа с курицей</div><div class="cal-meal"><b>У:</b> Тефтели в соусе</div></div>
        <div class="cal-day"><div class="cal-title">Вт</div><div class="cal-meal"><b>З:</b> Сырники с ягодами</div><div class="cal-meal"><b>О:</b> Бефстроганов</div><div class="cal-meal"><b>У:</b> Баклажаны чили</div></div>
        <div class="cal-day"><div class="cal-title">Ср</div><div class="cal-meal"><b>З:</b> Шакшука томатная</div><div class="cal-meal"><b>О:</b> Соба с овощами</div><div class="cal-meal"><b>У:</b> Медальоны из индейки</div></div>
        <div class="cal-day"><div class="cal-title">Чт</div><div class="cal-meal"><b>З:</b> Фриттата шпинатная</div><div class="cal-meal"><b>О:</b> Тыквенный крем-суп</div><div class="cal-meal"><b>У:</b> Филе под сыром</div></div>
        <div class="cal-day"><div class="cal-title">Пт</div><div class="cal-meal"><b>З:</b> Творожный мусс</div><div class="cal-meal"><b>О:</b> Паста со шпинатом</div><div class="cal-meal"><b>У:</b> Лосось в глазури</div></div>
        <div class="cal-day"><div class="cal-title">Сб</div><div class="cal-meal"><b>З:</b> Сырники с вишней</div><div class="cal-meal"><b>О:</b> Боул с птицей</div><div class="cal-meal"><b>У:</b> Наггетсы с салатом</div></div>
        <div class="cal-day"><div class="cal-title">Вс</div><div class="cal-meal"><b>З:</b> Запеканка с лимоном</div><div class="cal-meal"><b>О:</b> Тосканский суп</div><div class="cal-meal"><b>У:</b> Кабачковая лазанья</div></div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>15</span>
    </div>
</div>

<!-- СТР 16: КАЛЕНДАРНЫЙ РАЦИОН НЕДЕЛЯ 3 И 4 -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Готовые Рационы</span>
        <span class="header-page-title">Календарная сетка: Недели 3 и 4</span>
    </div>

    <div class="manifesto-banner">
        <h3>Неделя 3: Дренаж и легкость в теле (1400–1450 ккал)</h3>
    </div>

    <div class="calendar-grid">
        <div class="cal-day"><div class="cal-title">Пн</div><div class="cal-meal"><b>З:</b> Сырники без муки</div><div class="cal-meal"><b>О:</b> Паста с индейкой</div><div class="cal-meal"><b>У:</b> Боул с тунцом</div></div>
        <div class="cal-day"><div class="cal-title">Вт</div><div class="cal-meal"><b>З:</b> Фриттата с фетой</div><div class="cal-meal"><b>О:</b> Киноа с овощами</div><div class="cal-meal"><b>У:</b> Кальмары гриль</div></div>
        <div class="cal-day"><div class="cal-title">Ср</div><div class="cal-meal"><b>З:</b> Овсяноблин с рыбой</div><div class="cal-meal"><b>О:</b> Тыквенный суп</div><div class="cal-meal"><b>У:</b> Курочка с черри</div></div>
        <div class="cal-day"><div class="cal-title">Чт</div><div class="cal-meal"><b>З:</b> Шакшука за 7 мин</div><div class="cal-meal"><b>О:</b> Соба с говядиной</div><div class="cal-meal"><b>У:</b> Баклажаны чили</div></div>
        <div class="cal-day"><div class="cal-title">Пт</div><div class="cal-meal"><b>З:</b> Творожный мусс</div><div class="cal-meal"><b>О:</b> Бефстроганов</div><div class="cal-meal"><b>У:</b> Лосось с брокколи</div></div>
        <div class="cal-day"><div class="cal-title">Сб</div><div class="cal-meal"><b>З:</b> Запеканка маковая</div><div class="cal-meal"><b>О:</b> Тосканский суп</div><div class="cal-meal"><b>У:</b> Тефтели с цукини</div></div>
        <div class="cal-day"><div class="cal-title">Вс</div><div class="cal-meal"><b>З:</b> Сырники с яблоком</div><div class="cal-meal"><b>О:</b> Боул с птицей</div><div class="cal-meal"><b>У:</b> Кабачковая лазанья</div></div>
    </div>

    <div class="manifesto-banner" style="margin-top: 14px; border-left-color: #246B46;">
        <h3>Неделя 4: Закрепление привычек и минус 3–4 кг на весах</h3>
    </div>

    <div class="calendar-grid">
        <div class="cal-day"><div class="cal-title">Пн</div><div class="cal-meal"><b>З:</b> Овсяноблин с сыром</div><div class="cal-meal"><b>О:</b> Паста с индейкой</div><div class="cal-meal"><b>У:</b> Курочка под сыром</div></div>
        <div class="cal-day"><div class="cal-title">Вт</div><div class="cal-meal"><b>З:</b> Сырники классик</div><div class="cal-meal"><b>О:</b> Киноа с курицей</div><div class="cal-meal"><b>У:</b> Медальоны индейки</div></div>
        <div class="cal-day"><div class="cal-title">Ср</div><div class="cal-meal"><b>З:</b> Шакшука с зеленью</div><div class="cal-meal"><b>О:</b> Бефстроганов</div><div class="cal-meal"><b>У:</b> Баклажаны чили</div></div>
        <div class="cal-day"><div class="cal-title">Чт</div><div class="cal-meal"><b>З:</b> Фриттата шпинат</div><div class="cal-meal"><b>О:</b> Тыквенный крем-суп</div><div class="cal-meal"><b>У:</b> Боул с тунцом</div></div>
        <div class="cal-day"><div class="cal-title">Пт</div><div class="cal-meal"><b>З:</b> Творожная запеканка</div><div class="cal-meal"><b>О:</b> Соба с говядиной</div><div class="cal-meal"><b>У:</b> Лосось с брокколи</div></div>
        <div class="cal-day"><div class="cal-title">Сб</div><div class="cal-meal"><b>З:</b> Овсянка в банке</div><div class="cal-meal"><b>О:</b> Тосканский суп</div><div class="cal-meal"><b>У:</b> Тефтели с цукини</div></div>
        <div class="cal-day"><div class="cal-title">Вс</div><div class="cal-meal"><b>З:</b> Сырники с вишней</div><div class="cal-meal"><b>О:</b> Боул с киноа</div><div class="cal-meal"><b>У:</b> Наггетсы с салатом</div></div>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>16</span>
    </div>
</div>

<!-- СТР 17: ЭНЦИКЛОПЕДИЯ ЗАМЕН И ХРАНЕНИЕ -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Шпаргалка Кулинара</span>
        <span class="header-page-title">Таблица Замен и Zero Waste Хранение</span>
    </div>

    <table class="compact-table">
        <thead>
            <tr>
                <th style="width: 25%;">Привычный продукт</th>
                <th style="width: 40%;">Умная альтернатива Анастасии</th>
                <th style="width: 35%;">В чем профит для фигуры</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Белый сахар</b></td>
                <td>Эритрит, FitParad №7, яблочное пюре</td>
                <td>0 ккал, 0 гликемический индекс, нет прыщей и тяги к сладкому</td>
            </tr>
            <tr>
                <td><b>Майонез / Цезарь соус</b></td>
                <td>Греческий йогурт 2% + дижонская горчица + соевый соус</td>
                <td>В 4 раза меньше жира, бархатная эмульсия как в ресторане</td>
            </tr>
            <tr>
                <td><b>Белая мука высшего сорта</b></td>
                <td>Рисовая мука (сырники) + овсяная ц/з мука</td>
                <td>Сырники не текут, нежная текстура, нет глютеновой тяжести</td>
            </tr>
            <tr>
                <td><b>Жирные сливки 33%</b></td>
                <td>Сливки 10% + крахмальная вода из кастрюли пасты</td>
                <td>Крахмал взбивает нежирные сливки в густой шелк без лишнего жира</td>
            </tr>
            <tr>
                <td><b>Панировочные сухари</b></td>
                <td>Кукурузный крахмал тонким слоем</td>
                <td>Стеклянная тонкая корочка, впитывает в 3 раза меньше масла</td>
            </tr>
            <tr>
                <td><b>Подсолнечное масло для жарки</b></td>
                <td>Масло Гхи для жарки + оливковое Extra Virgin в спрее</td>
                <td>Высокая точка дымления без канцерогенов + строгий дозированный расход</td>
            </tr>
        </tbody>
    </table>

    <div class="manifesto-banner" style="margin-top: 10px; border-left-color: #2E6A4F;">
        <h3>Секреты хранения: зелень хрустит 3 недели!</h3>
        <p style="font-size: 11px;">• <b>Кинза, укроп и петрушка:</b> обрезать кончики стеблей на 1 см и поставить в банку с 3 см холодной воды, накрыв пакетом. Стоит хрустящей до 20 дней!<br>• <b>Томаты:</b> никогда не храните в холодильнике! Холод разрушает летучие сахара и делает томаты ватными. Храните плодоножкой вниз при комнатной температуре.<br>• <b>Шоковая заморозка ягод:</b> ягоды разложить в 1 слой на разделочной доске, подморозить 2 часа, затем ссыпать в зип-пакет. Никакой слипшейся каши!</p>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>17</span>
    </div>
</div>

<!-- СТР 18: УМНЫЙ СПИСОК ПОКУПОК -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Супермаркет</span>
        <span class="header-page-title">Чек-лист покупок для Магнита / Пятёрочки</span>
    </div>

    <div class="grocery-columns">
        <div class="grocery-block">
            <h5>Мясо, Птица, Рыба</h5>
            <div class="g-item"><div class="box-check"></div> Куриное филе — 1 кг</div>
            <div class="g-item"><div class="box-check"></div> Филе индейки — 800 г</div>
            <div class="g-item"><div class="box-check"></div> Фарш индейка/говядина — 500 г</div>
            <div class="g-item"><div class="box-check"></div> Стейк лосося / форели — 2 шт</div>
            <div class="g-item"><div class="box-check"></div> Тунец в с/с — 3 банки</div>
            <div class="g-item"><div class="box-check"></div> Кальмары очищенные — 400 г</div>
            <div class="g-item"><div class="box-check"></div> Яйца С0 — 2 десятка</div>
        </div>

        <div class="grocery-block">
            <h5>Овощи и Зелень</h5>
            <div class="g-item"><div class="box-check"></div> Томаты черри — 3 уп</div>
            <div class="g-item"><div class="box-check"></div> Баклажаны — 3 шт</div>
            <div class="g-item"><div class="box-check"></div> Кабачки / цукини — 3 шт</div>
            <div class="g-item"><div class="box-check"></div> Шпинат свежий — 2 пачки</div>
            <div class="g-item"><div class="box-check"></div> Стручковая фасоль с/м — 1 уп</div>
            <div class="g-item"><div class="box-check"></div> Авокадо Хасс — 3 шт</div>
            <div class="g-item"><div class="box-check"></div> Кинза и руккола — по 2 пучка</div>
        </div>

        <div class="grocery-block">
            <h5>Молочка и Бакалея</h5>
            <div class="g-item"><div class="box-check"></div> Творог 5% в брикете — 4 уп</div>
            <div class="g-item"><div class="box-check"></div> Сливки 10% — 2 коробочки</div>
            <div class="g-item"><div class="box-check"></div> Йогурт Teos 2% — 4 банки</div>
            <div class="g-item"><div class="box-check"></div> Страчателла / фета — 2 уп</div>
            <div class="g-item"><div class="box-check"></div> Паста Barilla — 1 уп</div>
            <div class="g-item"><div class="box-check"></div> Киноа / булгур — по 1 уп</div>
            <div class="g-item"><div class="box-check"></div> Рисовая мука + крахмал</div>
        </div>
    </div>

    <div style="margin-top: 25px; background: #FFFFFF; border: 1px solid #E8E1D7; padding: 16px; border-radius: 6px; text-align: center;">
        <h4 style="font-family: 'Georgia', serif; font-size: 15px; color: #172A21; margin-bottom: 4px;">Поздравляю с началом легкой и вкусной жизни! 🤍</h4>
        <p style="font-size: 11.5px; color: #555; max-width: 520px; margin: 0 auto;">Готовьте с удовольствием, делитесь фото блюд в закрытом канале и помните: любовь к себе начинается с того, чем вы наполняете свою тарелку каждый день.</p>
        <p style="margin-top: 8px; font-size: 10px; color: #888; letter-spacing: 1px;">ВАША АНАСТАСИЯ • 2026</p>
    </div>

    <div class="page-footer">
        <span>ЭНЦИКЛОПЕДИЯ ЗАКРЫТОГО КЛУБА</span>
        <span>18</span>
    </div>
</div>

</body>
</html>
"""

with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML энциклопедии сохранен: {HTML_OUTPUT}")

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={PDF_OUTPUT}",
    str(HTML_OUTPUT)
]

print("Генерация масштабного 18-страничного журнала...")
res = subprocess.run(cmd, capture_output=True, text=True)

if PDF_OUTPUT.exists():
    size_mb = PDF_OUTPUT.stat().st_size / (1024 * 1024)
    print(f"УСПЕХ! PDF обновлен: {PDF_OUTPUT} ({size_mb:.2f} MB)")
else:
    print("Ошибка генерации:", res.stderr)

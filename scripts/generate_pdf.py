"""
Генератор журнального руководства для Закрытого Клуба Анастасии.
Формат: Стильный журнал A4 на 6 страниц.
Ветки:
1. Сытное похудение (для себя)
2. Семейные блюда-трансформеры (ест муж и дети, без готовки в 2 котла)
3. Meal Prep заготовки на 3 дня
4. Шпаргалка замен и список продуктов из Магнита/Пятерочки
"""

import base64
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
PHOTO_PATH = ASSETS_DIR / "welcome.jpg"
HTML_OUTPUT = ASSETS_DIR / "magazine_guide.html"
PDF_OUTPUT = ASSETS_DIR / "База_Рецептов_и_Рационов_Анастасии.pdf"

photo_b64 = ""
if PHOTO_PATH.exists():
    with open(PHOTO_PATH, "rb") as f:
        photo_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
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
        font-size: 13px;
        line-height: 1.5;
    }}

    /* СТРАНИЦА A4 — ФИКСИРОВАННЫЙ РАЗМЕР БЕЗ СЪЕЗЖАНИЯ */
    .page {{
        width: 210mm;
        height: 297mm;
        padding: 20mm 18mm 16mm 18mm;
        page-break-after: always;
        break-after: page;
        position: relative;
        overflow: hidden;
        background-color: #FAF8F5;
    }}

    /* СТИЛЬ ОБЛОЖКИ */
    .cover-page {{
        padding: 0;
        background: #172A21;
        color: #FFFFFF;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .cover-top {{
        padding: 24mm 22mm 0 22mm;
    }}

    .cover-tag {{
        display: inline-block;
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #E2BA82;
        font-weight: 600;
        margin-bottom: 12px;
    }}

    .cover-title {{
        font-family: 'Georgia', serif;
        font-size: 38px;
        line-height: 1.15;
        color: #FFFFFF;
        font-weight: 700;
        margin-bottom: 14px;
        letter-spacing: -0.5px;
    }}

    .cover-desc {{
        font-size: 14px;
        line-height: 1.6;
        color: rgba(255, 255, 255, 0.8);
        max-width: 520px;
    }}

    .cover-image-container {{
        width: 100%;
        height: 120mm;
        margin: 15px 0;
        padding: 0 22mm;
    }}

    .cover-photo {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 8px;
        border: 1px solid rgba(226, 186, 130, 0.3);
    }}

    .cover-bottom {{
        padding: 0 22mm 20mm 22mm;
    }}

    .cover-features {{
        display: flex;
        gap: 10px;
        margin-bottom: 18px;
    }}

    .feature-pill {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(226, 186, 130, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        color: #FFFFFF;
        font-weight: 500;
    }}

    .cover-meta {{
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding-top: 14px;
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 1px;
    }}

    /* ВНУТРЕННИЕ СТРАНИЦЫ */
    .page-header {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        border-bottom: 1.5px solid #242424;
        padding-bottom: 8px;
        margin-bottom: 18px;
    }}

    .header-category {{
        font-size: 10px;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #C25E3E;
        font-weight: 700;
    }}

    .header-page-title {{
        font-family: 'Georgia', serif;
        font-size: 22px;
        color: #172A21;
        font-weight: 700;
    }}

    .page-footer {{
        position: absolute;
        bottom: 12mm;
        left: 18mm;
        right: 18mm;
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #E6DFD5;
        padding-top: 8px;
        font-size: 10px;
        color: #8C8275;
        letter-spacing: 0.5px;
    }}

    /* МАНИФЕСТ И БЛОКИ */
    .manifesto-banner {{
        background: #FFFFFF;
        border: 1px solid #E8E1D7;
        border-left: 4px solid #C25E3E;
        padding: 16px 20px;
        border-radius: 4px;
        margin-bottom: 18px;
    }}

    .manifesto-banner h3 {{
        font-family: 'Georgia', serif;
        font-size: 17px;
        color: #172A21;
        margin-bottom: 6px;
    }}

    .dual-columns {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 18px;
    }}

    .info-card {{
        background: #FFFFFF;
        border: 1px solid #E8E1D7;
        padding: 16px;
        border-radius: 6px;
    }}

    .info-card h4 {{
        font-family: 'Georgia', serif;
        font-size: 15px;
        color: #172A21;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .tag-badge {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 9px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .tag-slimming {{
        background: #EAF4EE;
        color: #246B46;
    }}

    .tag-family {{
        background: #FDF1EB;
        color: #B8502E;
    }}

    /* КАРТОЧКИ РЕЦЕПТОВ */
    .recipe-row {{
        background: #FFFFFF;
        border: 1px solid #E8E1D7;
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 14px;
    }}

    .recipe-head {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }}

    .recipe-title {{
        font-family: 'Georgia', serif;
        font-size: 16px;
        font-weight: 700;
        color: #172A21;
    }}

    .recipe-badge-time {{
        font-size: 10px;
        background: #F3EFE9;
        padding: 3px 8px;
        border-radius: 10px;
        color: #61594F;
        font-weight: 600;
    }}

    .recipe-macros {{
        display: flex;
        gap: 12px;
        font-size: 11px;
        background: #F8F6F2;
        padding: 5px 12px;
        border-radius: 4px;
        margin-bottom: 10px;
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
        gap: 14px;
        font-size: 11.5px;
    }}

    .subhead {{
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #8C8275;
        font-weight: 700;
        margin-bottom: 4px;
    }}

    .ing-list {{
        list-style: none;
    }}

    .ing-list li {{
        margin-bottom: 2px;
        padding-left: 10px;
        position: relative;
    }}

    .ing-list li::before {{
        content: "–";
        position: absolute;
        left: 0;
        color: #C25E3E;
    }}

    .steps-list {{
        padding-left: 15px;
    }}

    .steps-list li {{
        margin-bottom: 4px;
    }}

    .secret-box {{
        background: #FFFDF9;
        border-left: 3px solid #E2BA82;
        padding: 6px 10px;
        margin-top: 8px;
        font-size: 11px;
        color: #614D2E;
    }}

    /* ТРАНСФОРМЕР БЛОК ДЛЯ СЕМЬИ */
    .transform-split {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        background: #FAF7F2;
        padding: 8px 10px;
        border-radius: 4px;
        margin-top: 8px;
        font-size: 11px;
    }}

    .transform-col b {{
        display: block;
        font-size: 10px;
        text-transform: uppercase;
        margin-bottom: 2px;
    }}

    .col-husband b {{
        color: #B8502E;
    }}

    .col-diet b {{
        color: #246B46;
    }}

    /* СЕТКА ШПАРГАЛКИ ЗАМЕН */
    table.compact-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 11.5px;
        background: #FFFFFF;
        border-radius: 4px;
        overflow: hidden;
        border: 1px solid #E8E1D7;
        margin-bottom: 14px;
    }}

    table.compact-table th {{
        background: #172A21;
        color: #FFFFFF;
        text-align: left;
        padding: 8px 12px;
        font-size: 10px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    table.compact-table td {{
        padding: 8px 12px;
        border-bottom: 1px solid #F0ECE4;
        vertical-align: top;
    }}

    /* СПИСОК ПОКУПОК */
    .grocery-columns {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
    }}

    .grocery-block {{
        background: #FFFFFF;
        border: 1px solid #E8E1D7;
        padding: 12px;
        border-radius: 4px;
    }}

    .grocery-block h5 {{
        font-family: 'Georgia', serif;
        font-size: 13px;
        color: #172A21;
        border-bottom: 1px solid #E8E1D7;
        padding-bottom: 4px;
        margin-bottom: 6px;
    }}

    .g-item {{
        font-size: 11px;
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .box-check {{
        width: 10px;
        height: 10px;
        border: 1px solid #C25E3E;
        border-radius: 2px;
    }}
</style>
</head>
<body>

<!-- СТРАНИЦА 1: ГЛЯНЦЕВАЯ ОБЛОЖКА -->
<div class="page cover-page">
    <div class="cover-top">
        <span class="cover-tag">Анастасия • Закрытый кулинарный клуб</span>
        <h1 class="cover-title">Кулинарный<br>Конструктор</h1>
        <p class="cover-desc">Флагманское руководство: сытное похудение без голодовок, семейные блюда-трансформеры (ест муж и дети), система Meal Prep на 3 дня и точный список продуктов из супермаркета.</p>
    </div>

    <div class="cover-image-container">
        <img class="cover-photo" src="data:image/jpeg;base64,{photo_b64}" alt="Анастасия">
    </div>

    <div class="cover-bottom">
        <div class="cover-features">
            <span class="feature-pill">🥗 Сытное похудение</span>
            <span class="feature-pill">👨‍👩‍👧‍👦 Еда для всей семьи</span>
            <span class="feature-pill">🥡 Meal Prep на 3 дня</span>
            <span class="feature-pill">🛒 Чек-лист для супермаркета</span>
        </div>
        <div class="cover-meta">
            <span>ЗАКРЫТЫЕ МАТЕРИАЛЫ КЛУБА</span>
            <span>2026 • АВТОРСКАЯ СИСТЕМА</span>
        </div>
    </div>
</div>

<!-- СТРАНИЦА 2: МАНИФЕСТ + ФИЛОСОФИЯ 2 ВЕТОК -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Концепция и принципы</span>
        <span class="header-page-title">Хватит готовить в два котла</span>
    </div>

    <div class="manifesto-banner">
        <h3>Главная боль: почему диеты рушат отношения и силы?</h3>
        <p>Каждая девушка, начиная худеть, попадает в ловушку: <i>«Себе варю сухую грудку и брокколи, а мужу и детям жарю котлеты с пюре»</i>. Через неделю наступает выгорание от бесконечной посуды, а в субботу случается неизбежный срыв на семейный ужин.</p>
        <p style="margin-top: 6px;"><b>Мое золотое правило:</b> Мы готовим <u>одно базовое блюдо на всех</u>. Но благодаря умной системе сборки («трансформер»), муж получает плотный калорийный ужин, а вы — легкую порцию с дефицитом калорий и плоским животом на утро!</p>
    </div>

    <div class="dual-columns">
        <div class="info-card">
            <h4><span class="tag-badge tag-slimming">Ветка 1</span> Сытное похудение</h4>
            <p><b>Формула «35г белка + объём»:</b> Никаких голодных салатиков из листьев! Мы едим сочное мясо, рыбу, теплые сытные овощи и морепродукты.</p>
            <p style="margin-top: 6px; color: #555;">Чистый белок и медленные углеводы выключают вечерний жор и непреодолимую тягу к сладкому.</p>
        </div>
        <div class="info-card">
            <h4><span class="tag-badge tag-family">Ветка 2</span> Блюда для всей семьи</h4>
            <p><b>Метод «Основа + Топпинг»:</b> Готовится богатая мясная основа (томленая индейка, запеченная курочка, сочные тефтели).</p>
            <p style="margin-top: 6px; color: #555;">Муж добирает энергию гарниром (паста/картофель), а вы — хрустящей спаржей, черри и свежей зеленью.</p>
        </div>
    </div>

    <div class="manifesto-banner" style="border-left-color: #246B46;">
        <h3>3 правила, чтобы худеть без чувства голода</h3>
        <ul style="padding-left: 18px; margin-top: 6px; font-size: 12px;">
            <li><b>Белок в каждом приеме:</b> 30–35 г белка защищают мышцы от дряблости и разгоняют метаболизм на 25%.</li>
            <li><b>Секрет крахмала:</b> кукурузный крахмал вместо муки и сухарей дает хрустящую корочку и впитывает в 3 раза меньше масла.</li>
            <li><b>Соусы без майонеза:</b> греческий йогурт + дижонская горчица + лимон делают вкус как в ресторане без лишних калорий.</li>
        </ul>
    </div>

    <div class="page-footer">
        <span>КОНСТРУКТОР ПИТАНИЯ АНАСТАСИИ</span>
        <span>02</span>
    </div>
</div>

<!-- СТРАНИЦА 3: ВЕТКА 1 — СЫТНОЕ ПОХУДЕНИЕ -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Ветка 1: Для Себя</span>
        <span class="header-page-title">Сытное похудение: Экспресс-ужины</span>
    </div>

    <!-- РЕЦЕПТ 1 -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">1. Нежное филе в сливочно-томатном соусе с черри</span>
            <span class="recipe-badge-time">⏱ 18 минут</span>
        </div>
        <div class="recipe-macros">
            <span>320 ккал</span>
            <span>Белки: 38 г</span>
            <span>Жиры: 11 г</span>
            <span>Углеводы: 7 г</span>
            <span class="macros-check">Чек в Магните: ~148 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Куриное филе — 180 г</li>
                    <li>Черри свежие — 80 г</li>
                    <li>Сливки 10% питьевые — 60 мл</li>
                    <li>Чеснок 1 зуб., паприка, базилик</li>
                    <li>Оливковое масло — 1 ч. л.</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Филе нарезать ломтиками, обжарить на сильном огне 3 мин до золотистости.</li>
                    <li>Бросить половинки черри и чеснок, тушить 2 мин до ароматного сока.</li>
                    <li>Влить 10% сливки, убавить огонь и томить 5 мин до бархатного соуса.</li>
                </ol>
            </div>
        </div>
        <div class="secret-box">
            💡 <b>Лайфхак:</b> Нежирные 10% сливки связываются с кислотой томатов черри и дают густой соус без муки!
        </div>
    </div>

    <!-- РЕЦЕПТ 2 -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">2. Хрустящие баклажаны со страчателлой и чили</span>
            <span class="recipe-badge-time">⏱ 15 минут</span>
        </div>
        <div class="recipe-macros">
            <span>280 ккал</span>
            <span>Белки: 12 г</span>
            <span>Жиры: 14 г</span>
            <span>Углеводы: 24 г</span>
            <span class="macros-check">Чек в Магните: ~160 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Баклажан средний — 180 г</li>
                    <li>Томаты спелые — 120 г</li>
                    <li>Страчателла / легкий сыр — 50 г</li>
                    <li>Кукурузный крахмал — 1.5 ст. л.</li>
                    <li>Соус сладкий чили, кинза, кунжут</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Баклажан очистить полосками, нарезать кубиком 3 см, сбрызнуть водой и обвалять в крахмале.</li>
                    <li>Обжарить в горячем масле 3 мин до звонкого хруста.</li>
                    <li>На ломтики томатов выложить горячие баклажаны, сыр, полить чили и кинзой.</li>
                </ol>
            </div>
        </div>
        <div class="secret-box">
            💡 <b>Лайфхак:</b> Контраст горячих баклажанов и холодного сыра дает ресторанный дофамин без срывов на фастфуд.
        </div>
    </div>

    <!-- РЕЦЕПТ 3 -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">3. Протеиновый боул с тунцом, яйцом и стручковой фасолью</span>
            <span class="recipe-badge-time">⏱ 10 минут</span>
        </div>
        <div class="recipe-macros">
            <span>340 ккал</span>
            <span>Белки: 36 г</span>
            <span>Жиры: 12 г</span>
            <span>Углеводы: 18 г</span>
            <span class="macros-check">Чек в Магните: ~171 ₽</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Ингредиенты:</div>
                <ul class="ing-list">
                    <li>Тунец в с/с (банка) — 130 г</li>
                    <li>Яйцо С0 всмятку — 1 шт</li>
                    <li>Стручковая фасоль — 120 г</li>
                    <li>Свежий огурец — 80 г</li>
                    <li>Заправка: лимон + горчица + масло</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Фасоль отварить 4 мин в подсоленной воде и обдать ледяной водой.</li>
                    <li>В чашу выложить фасоль, тунец, огурец и яйцо с жидким желтком.</li>
                    <li>Сбрызнуть лимонно-горчичной заправкой. Рекордная сытость за 10 минут!</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>КОНСТРУКТОР ПИТАНИЯ АНАСТАСИИ</span>
        <span>03</span>
    </div>
</div>

<!-- СТРАНИЦА 4: ВЕТКА 2 — СЕМЕЙНЫЕ БЛЮДА-ТРАНСФОРМЕРЫ -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Ветка 2: Для Всей Семьи</span>
        <span class="header-page-title">Блюда-трансформеры (ест муж и дети)</span>
    </div>

    <!-- СЕМЕЙНЫЙ РЕЦЕПТ 1 -->
    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">1. Нежнейшие тефтели в томатно-сливочном соусе с цукини</span>
            <span class="recipe-badge-time">⏱ 25 минут</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Секретная основа:</div>
                <ul class="ing-list">
                    <li>Фарш индейка/говядина — 500 г</li>
                    <li>Кабачок/цукини тертый — 150 г (сочность!)</li>
                    <li>Томаты протертые (passata) — 300 мл</li>
                    <li>Сливки 10% — 70 мл, чеснок, базилик</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Кабачок натереть на мелкой терке, отжать и вмешать в фарш без хлеба!</li>
                    <li>Сформировать тефтели, обжарить 4 мин, залить томатами и сливками.</li>
                    <li>Томить под крышкой 15 минут. Тефтели тают во рту.</li>
                </ol>
            </div>
        </div>
        <div class="transform-split">
            <div class="transform-col col-husband">
                <b>👨 Подача для мужа и детей:</b>
                Щедрая порция тефтелей с макаронами или картофельным пюре, густо политая соусом и посыпанная сыром.
            </div>
            <div class="transform-col col-diet">
                <b>💃 Подача для себя (похудение):</b>
                3 тефтели с соусом на подушке из свежей рукколы, шпината или брокколи на пару. Всего 330 ккал и 34г белка!
            </div>
        </div>
    </div>

    <!-- СЕМЕЙНЫЙ РЕЦЕПТ 2 -->
    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">2. Сочная куриная грудка под сырно-овощной шубкой (Sheet Pan)</span>
            <span class="recipe-badge-time">⏱ 25 минут в духовке</span>
        </div>
        <div class="recipe-content-grid">
            <div>
                <div class="subhead">Основа на противень:</div>
                <ul class="ing-list">
                    <li>Филе грудки — 4 шт (по 180 г)</li>
                    <li>Томаты спелые кольцами — 2 шт</li>
                    <li>Сладкий перец соломкой — 1 шт</li>
                    <li>Сыр сулугуни/моцарелла — 80 г</li>
                    <li>Сметана 10% + чеснок + укроп</li>
                </ul>
            </div>
            <div>
                <div class="subhead">Приготовление:</div>
                <ol class="steps-list">
                    <li>Филе слегка надрезать сеткой, смазать соусом из сметаны и чеснока.</li>
                    <li>Выложить кружочки томатов, сладкий перец и присыпать сыром.</li>
                    <li>Запекать при 190°C ровно 22–24 минуты. Никакой сухости!</li>
                </ol>
            </div>
        </div>
        <div class="transform-split">
            <div class="transform-col col-husband">
                <b>👨 Подача для мужа и детей:</b>
                Филе под сыром с запеченными дольками картофеля по-деревенски со сливочным маслом.
            </div>
            <div class="transform-col col-diet">
                <b>💃 Подача для себя (похудение):</b>
                Филе под сыром с большой порцией теплого салата из свежих огурцов и зелени. Чистый белок без лишнего жира!
            </div>
        </div>
    </div>

    <div class="page-footer">
        <span>КОНСТРУКТОР ПИТАНИЯ АНАСТАСИИ</span>
        <span>04</span>
    </div>
</div>

<!-- СТРАНИЦА 5: MEAL PREP НА 3 ДНЯ + ПЯТИМИНУТКИ -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Организация и скорость</span>
        <span class="header-page-title">Meal Prep на 3 дня & Экспресс-пятиминутки</span>
    </div>

    <div class="manifesto-banner" style="margin-bottom: 14px;">
        <h3>Воскресный Sheet Pan: 1 противень = 3 дня свободы</h3>
        <p>Застелите большой противень пергаментом. Слева выложите филе индейки в травах, справа — крупно нарезанные овощи (кабачок, тыква, перец, цветная капуста). Запекайте 35 минут при 180°C. <b>У вас готова сочная белковая база и гарнир на 3 дня!</b></p>
    </div>

    <h4 style="font-family: 'Georgia', serif; font-size: 16px; margin-bottom: 10px; color: #172A21;">⚡ Топ-3 экспресс-пятиминутки (когда совсем нет сил)</h4>

    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">1. Шакшука за 7 минут в одной сковороде</span>
            <span class="recipe-badge-time">285 ккал • Б: 22 г</span>
        </div>
        <p style="font-size: 11.5px; color: #444;">В сковороде прогреть 3 ложки протертых томатов passata с чесноком и паприкой (1 мин). Разбить 2 яйца, бросить горсть черри и кубики брынзы. Накрыть крышкой на 4 минуты. Есть прямо из сковороды с зеленью!</p>
    </div>

    <div class="recipe-row">
        <div class="recipe-head">
            <span class="recipe-title">2. ПП-шаурма в лаваше с сочной индейкой из заготовок</span>
            <span class="recipe-badge-time">310 ккал • Б: 32 г</span>
        </div>
        <p style="font-size: 11.5px; color: #444;">Тонкий лаваш смазать соусом из греческого йогурта с горчицей. Выложить нарезанную запеченную индейку, хрустящий огурец, томат и пекинскую капусту. Свернуть и прогреть на сухой сковороде по 1.5 мин до хруста.</p>
    </div>

    <div class="recipe-row" style="margin-bottom: 0;">
        <div class="recipe-head">
            <span class="recipe-title">3. Творожный мусс «Пломбир» с ягодами за 3 минуты</span>
            <span class="recipe-badge-time">220 ккал • Б: 28 г</span>
        </div>
        <p style="font-size: 11.5px; color: #444;">Пачку мягкого творога 5% взбить погружным блендером с 1 саше FitParad, ванилином и 30 мл молока. Получается текстура растаявшего мороженого! Полить теплым ягодным пюре из микроволновки.</p>
    </div>

    <div class="page-footer">
        <span>КОНСТРУКТОР ПИТАНИЯ АНАСТАСИИ</span>
        <span>05</span>
    </div>
</div>

<!-- СТРАНИЦА 6: ТАБЛИЦА ЗАМЕН И СПИСОК ПОКУПОК -->
<div class="page">
    <div class="page-header">
        <span class="header-category">Шпаргалка Супермаркета</span>
        <span class="header-page-title">Замены продуктов и список покупок</span>
    </div>

    <table class="compact-table">
        <thead>
            <tr>
                <th style="width: 28%;">Вредный продукт</th>
                <th style="width: 37%;">Умная замена Анастасии</th>
                <th style="width: 35%;">Почему это работает</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Белый сахар</b></td>
                <td>Эритрит или FitParad №7</td>
                <td>0 калорий, нет инсулиновых качелей и чистая кожа</td>
            </tr>
            <tr>
                <td><b>Майонез / Цезарь соус</b></td>
                <td>Йогурт Teos + дижонская горчица + соевый</td>
                <td>В 4 раза меньше жира, богатый шелковистый вкус</td>
            </tr>
            <tr>
                <td><b>Белая мука в сырниках</b></td>
                <td>Рисовая мука (1.5 ст. л.)</td>
                <td>Сырники держат форму, нет глютеновой тяжести</td>
            </tr>
            <tr>
                <td><b>Панировочные сухари</b></td>
                <td>Кукурузный крахмал тонким слоем</td>
                <td>Стеклянный хруст в баклажанах и мясе без лишнего масла</td>
            </tr>
        </tbody>
    </table>

    <h4 style="font-family: 'Georgia', serif; font-size: 15px; margin-bottom: 10px; color: #172A21;">🛒 Базовый список продуктов на неделю (Пятёрочка / Магнит)</h4>

    <div class="grocery-columns">
        <div class="grocery-block">
            <h5>Мясо и Птица</h5>
            <div class="g-item"><div class="box-check"></div> Куриное филе — 800 г</div>
            <div class="g-item"><div class="box-check"></div> Фарш индейки — 500 г</div>
            <div class="g-item"><div class="box-check"></div> Тунец в с/с — 2 банки</div>
            <div class="g-item"><div class="box-check"></div> Яйца С0 — 1 десяток</div>
        </div>

        <div class="grocery-block">
            <h5>Овощи и Зелень</h5>
            <div class="g-item"><div class="box-check"></div> Томаты черри — 2 уп</div>
            <div class="g-item"><div class="box-check"></div> Баклажаны — 2 шт</div>
            <div class="g-item"><div class="box-check"></div> Кабачок / цукини — 2 шт</div>
            <div class="g-item"><div class="box-check"></div> Шпинат / кинза — 2 уп</div>
            <div class="g-item"><div class="box-check"></div> Стручковая фасоль — 1 уп</div>
        </div>

        <div class="grocery-block">
            <h5>Молочка и Бакалея</h5>
            <div class="g-item"><div class="box-check"></div> Творог 5% в брикете — 2 уп</div>
            <div class="g-item"><div class="box-check"></div> Сливки 10% — 200 мл</div>
            <div class="g-item"><div class="box-check"></div> Греческий йогурт Teos — 2 шт</div>
            <div class="g-item"><div class="box-check"></div> Сыр страчателла/сулугуни</div>
            <div class="g-item"><div class="box-check"></div> Крахмал кукурузный</div>
        </div>
    </div>

    <div style="margin-top: 25px; text-align: center; border-top: 1px solid #E8E1D7; padding-top: 14px; font-size: 11px; color: #777;">
        <i>Материалы созданы эксклюзивно для резидентов закрытого кулинарного клуба Анастасии. Приятного аппетита и легкой готовки! 🤍</i>
    </div>

    <div class="page-footer">
        <span>КОНСТРУКТОР ПИТАНИЯ АНАСТАСИИ</span>
        <span>06</span>
    </div>
</div>

</body>
</html>
"""

with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML сохранен: {HTML_OUTPUT}")

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={PDF_OUTPUT}",
    str(HTML_OUTPUT)
]

print("Генерация чистого журнального PDF...")
res = subprocess.run(cmd, capture_output=True, text=True)

if PDF_OUTPUT.exists():
    size_mb = PDF_OUTPUT.stat().st_size / (1024 * 1024)
    print(f"УСПЕХ! PDF обновлен: {PDF_OUTPUT} ({size_mb:.2f} MB)")
else:
    print("Ошибка генерации:", res.stderr)

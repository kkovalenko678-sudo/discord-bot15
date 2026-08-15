import disnake
from disnake.ext import commands
import aiohttp
import csv
import asyncio
from io import StringIO
from datetime import datetime
from disnake.ui import Container, TextDisplay, Separator, MediaGallery

# ==========================================
# ⚙️ НАСТРОЙКИ
# ==========================================
BOT_TOKEN = "код токен"
GUILD_ID = 1522482131211784364

# 🖼️ БАННЕРЫ (появляются автоматически)
BANNER_EXPIRED = "https://cdn.discordapp.com/attachments/1115031349208817765/1535534471833460837/file_0000000091e481faabc9a868979cefab.png?ex=6a781d6a&is=6a76cbea&hm=b86501d91a14388c38b8a581db8072a9cdc4538be2199ef3d6738a121592557f"
BANNER_ACTIVE = "https://cdn.discordapp.com/attachments/1115031349208817765/1535534341634134036/file_00000000c07881fba7eef0308867291d.png?ex=6a781d4b&is=6a76cbcb&hm=2690ee6b94fc572111ed7cca1b76391a1a41752b9d473d9dac1973248ee71ae5"
BANNER_CURATORS = "https://cdn.discordapp.com/attachments/1115031349208817765/1535534519128686622/file_000000006b9082098b09be9d768b832e.png?ex=6a781d76&is=6a76cbf6&hm=016147ef724d55c6e06d42e6904b5e5a6be2813ddc654854eee082174abf34e0"
BANNER_LEADERS_ALL = "https://cdn.discordapp.com/attachments/1115031349208817765/1535534534387437598/file_0000000014ac8209a9211ec4eb68d372.png?ex=6a781d79&is=6a76cbf9&hm=6b48be4b506d7225dc526a141db9da6f28eb52fb6a6caaa9c50877aa3c9cccd7"
BANNER_LEADER_ONE = "https://cdn.discordapp.com/attachments/1115031349208817765/1535534543820427294/file_0000000083c88209b07bc5586b9f451a.png?ex=6a781d7c&is=6a76cbfc&hm=2a4fadc9fc4a9c913270ca11db4928af8d8db6dd03c4b370c9149688133c8300"
BANNER_HELP = "https://cdn.discordapp.com/attachments/1115031349208817765/1535534601026404372/file_0000000097dc822f89404c2fa353e0af.png?ex=6a781d89&is=6a76cc09&hm=f60f9ae2b99a1e37f012ab49e125cd76f8832167f1b3ac81f3bd70a691ad57e6"
BANNER_HISTORY = "https://cdn.discordapp.com/attachments/1115031349208817765/1535534589890531431/file_00000000326081fbae117c71d9423a8d.png?ex=6a781d87&is=6a76cc07&hm=19af55a88df851f89619bc173ded80c8affa9af2ca8f8d497b55e8c56c91cc1d"

# ====== НАШИ КАСТОМНЫЕ ЭМОДЗИ ======
EMOJI_MAIN = 1523209690002100334      # главный (волк)
EMOJI_PUNISH = 1527884401374134403    # ОПГ
EMOJI_INFO = 1527610926641971324      # информация / ГОС
EMOJI_MEMBER = 1527612074484695152    # участники
EMOJI_NAV = 1527612223944392818       # даты / навигация

CSV_GOS = "https://docs.google.com/spreadsheets/d/1VhSPzPa5Q2raeZ4Tlp8wbxdTPEhKjP6ZLdYgp91wzA4/export?format=csv&gid=0"
CSV_OPG = "https://docs.google.com/spreadsheets/d/1VhSPzPa5Q2raeZ4Tlp8wbxdTPEhKjP6ZLdYgp91wzA4/export?format=csv&gid=2021514554"
CSV_LEADERS_ACT = "https://docs.google.com/spreadsheets/d/1oTNUKuuRz3oBqJ0d_i-rfYviUmSMmrkv58PVrc2EQL8/export?format=csv&gid=717127754"
CSV_CURATORS = "https://docs.google.com/spreadsheets/d/1oTNUKuuRz3oBqJ0d_i-rfYviUmSMmrkv58PVrc2EQL8/export?format=csv&gid=0"
CSV_CURATORS_OPG = "https://docs.google.com/spreadsheets/d/1oTNUKuuRz3oBqJ0d_i-rfYviUmSMmrkv58PVrc2EQL8/export?format=csv&gid=438685093"
CSV_HISTORY = "https://docs.google.com/spreadsheets/d/1vyxH8GgMY1Xeh2g4yUgnu5zSh4yPfMyiXf_-JLUfx4Y/export?format=csv"

DM_TEXT = (
    "👋 Приветствую!\n"
    "Этот бот разработан для нужд Кураторов Организаций и ОПГ.\n"
    "Если есть вопросы — обратитесь к администрации."
)

cache = {}

intents = disnake.Intents.default()
intents.message_content = True
# Замени старую строку на эту:
bot = commands.Bot(
    command_prefix="!", 
    intents=intents, 
    test_guilds=[1522482131211784364, 1493562064806084678]
)

# ==========================================
# ФУНКЦИИ
# ==========================================
def banner(url):
    if not url:
        return []
    try:
        return [MediaGallery(disnake.MediaGalleryItem(media=url))]
    except Exception:
        return []

def emj(emoji_id, fallback):
    e = bot.get_emoji(emoji_id)
    return str(e) if e else fallback

async def load_rows(url, retries=3):
    for attempt in range(retries):
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    return list(csv.reader(StringIO(await resp.text())))
        except Exception as e:
            print(f"⚠️ Попытка {attempt + 1} не удалась: {e}")
            await asyncio.sleep(2)
    return []

async def load_dict(url, retries=3):
    for attempt in range(retries):
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    return list(csv.DictReader(StringIO(await resp.text())))
        except Exception as e:
            print(f"⚠️ Попытка {attempt + 1} не удалась: {e}")
            await asyncio.sleep(2)
    return []

async def safe_defer(inter):
    try:
        await inter.response.defer()
        return True
    except Exception as e:
        print(f"⚠️ defer не удался: {e}")
        return False

async def update_cache():
    print("🔄 Обновление кэша...")
    cache["gos"] = await load_rows(CSV_GOS)
    cache["opg"] = await load_dict(CSV_OPG)
    cache["leaders_act"] = await load_rows(CSV_LEADERS_ACT)
    cache["curators"] = await load_rows(CSV_CURATORS)
    cache["curators_opg"] = await load_rows(CSV_CURATORS_OPG)
    cache["history"] = await load_rows(CSV_HISTORY)
    print(f"✅ Кэш: ГОС={len(cache.get('gos', []))}, ОПГ={len(cache.get('opg', []))}, Лидеры={len(cache.get('leaders_act', []))}")

async def cache_loop():
    while True:
        await asyncio.sleep(7200)
        await update_cache()

async def get_rows(key, url):
    if cache.get(key):
        return cache[key]
    rows = await load_rows(url)
    if rows:
        cache[key] = rows
    return rows

async def get_dict(key, url):
    if cache.get(key):
        return cache[key]
    rows = await load_dict(url)
    if rows:
        cache[key] = rows
    return rows

def normalize(text):
    return text.lower().replace("_", "").replace(" ", "").strip()

def get_transfers_safe(row):
    if len(row) > 7 and row[7].strip():
        return row[7]
    return "0"

def calc_time(start, end):
    try:
        d1 = datetime.strptime(start.strip(), "%d.%m.%Y")
        d2 = datetime.strptime(end.strip(), "%d.%m.%Y")
        delta = d2 - d1
        days = delta.days
        months = days // 30
        years = months // 12
        return f"{years} г. {months % 12} мес. {days % 30} дн."
    except Exception:
        return "неизвестно"

def get_status(end_date):
    try:
        end = datetime.strptime(end_date.strip(), "%d.%m.%Y")
        return "🟢 Активен" if end >= datetime.now() else "🔴 Истёк"
    except Exception:
        return "⚠️ Неизвестно"

@bot.event
async def on_ready():
    print(f"✅ Бот онлайн: {bot.user}")
    await update_cache()
    bot.loop.create_task(cache_loop())
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="за ЧС 15 сервера"))

# ==========================================
# 🔴 ЧС ГОС
# ==========================================
@bot.slash_command(name="check_org", description="Проверка ЧС ГОС")
async def check_org(inter: disnake.ApplicationCommandInteraction, nickname: str):
    if inter.guild is None:
        return await inter.response.send_message(DM_TEXT)
    if not await safe_defer(inter):
        return

    rows = await get_rows("gos", CSV_GOS)
    s = normalize(nickname)
    found = [row for row in rows[1:] if row and s in normalize(row[0])]

    if not found:
        panel = Container(
            TextDisplay(content="🔴 **ЧС ГОС**"),
            Separator(),
            TextDisplay(content=f"❌ Игрок **{nickname}** не найден"),
            Separator(),
            TextDisplay(content="*Проверка ЧС ГОС*")
        )
        return await inter.edit_original_response(components=[panel])

    for i, row in enumerate(found, start=1):
        status = get_status(row[3])
        ban = BANNER_ACTIVE if "Активен" in status else BANNER_EXPIRED
        components = banner(ban) + [
            TextDisplay(content=f"🔴 **ЧС ГОС** #{i}"),
            Separator(),
            TextDisplay(content=f"👤 **Игрок:** {row[0]}"),
            TextDisplay(content=f"📅 **Дата подачи — Дата выхода:** {row[2]} — {row[3]}"),
            TextDisplay(content=f"⏳ **Срок:** {calc_time(row[2], row[3])}\n{status}"),
            Separator(),
            TextDisplay(content=f"📌 **Причина:** {row[4]}"),
            TextDisplay(content=f"🏛️ **Фракция:** {row[5]}  |  ⚖️ **Степень:** {row[6]}"),
        ]
        if len(row) > 7 and row[7]:
            components.append(TextDisplay(content=f"📎 **Дополнительно:** {row[7]}"))
        components += [Separator(), TextDisplay(content="*Проверка ЧС ГОС*")]

        if i == 1:
            await inter.edit_original_response(components=[Container(*components)])
        else:
            await inter.followup.send(components=[Container(*components)])

# ==========================================
# 🔵 ЧС ОПГ
# ==========================================
@bot.slash_command(name="check_opg", description="Проверка ЧС ОПГ")
async def check_opg(inter: disnake.ApplicationCommandInteraction, nickname: str):
    if inter.guild is None:
        return await inter.response.send_message(DM_TEXT)
    if not await safe_defer(inter):
        return

    rows = await get_dict("opg", CSV_OPG)
    s = normalize(nickname)
    found = [row for row in rows if s in normalize(row.get("Игровой ник / Номер аккаунта", ""))]

    if not found:
        panel = Container(
            TextDisplay(content="🔵 **ЧС ОПГ**"),
            Separator(),
            TextDisplay(content=f"❌ Игрок **{nickname}** не найден"),
            Separator(),
            TextDisplay(content="*Проверка ЧС ОПГ*")
        )
        return await inter.edit_original_response(components=[panel])

    for i, row in enumerate(found, start=1):
        start = row.get("Дата подачи", "-")
        end = row.get("Дата выноса", "-")
        panel = Container(
            *banner(BANNER_ACTIVE),
            TextDisplay(content=f"🔵 **ЧС ОПГ** #{i}"),
            Separator(),
            TextDisplay(content=f"👤 **Игрок:** {row.get('Игровой ник / Номер аккаунта', '-')}"),
            TextDisplay(content=f"📅 **Дата:** {start} — {end}"),
            TextDisplay(content=f"⏳ **Срок:** {calc_time(start, end)}"),
            Separator(),
            TextDisplay(content=f"📌 **Причина:** {row.get('Причина', '-')}"),
            TextDisplay(content=f"👮 **Кем занесен:** {row.get('Кем занесен', '-')}"),
            Separator(),
            TextDisplay(content="*Проверка ЧС ОПГ*")
        )

        if i == 1:
            await inter.edit_original_response(components=[panel])
        else:
            await inter.followup.send(components=[panel])
# ==========================================
# 🟢 ДЕЙСТВУЮЩИЕ ЛИДЕРЫ (ПОИСК ПО НИКУ + ФРАКЦИИ)
# ==========================================
@bot.slash_command(name="check_leaders_act", description="Действующие лидеры")
async def check_leaders_act(inter: disnake.ApplicationCommandInteraction, query: str):
    if inter.guild is None:
        return await inter.response.send_message(DM_TEXT)
    if not await safe_defer(inter):
        return

    rows = await get_rows("leaders_act", CSV_LEADERS_ACT)
    if not rows:
        return await inter.edit_original_response(content="❌ Не удалось загрузить таблицу лидеров")

    q = normalize(query)

    if q == "all":
        gos_list, opg_list = [], []
        gos_factions = ["Правительство", "ФСБ", "Полиция Южного", "Полиция Арзамаса",
                        "МЗ Южного", "МЗ Арзамаса", "Воинская часть", "Новостная сеть"]
        for row in rows[3:]:
            if not row or not row[0].strip():
                continue
            name, faction, start, end = row[0], row[1], row[2], row[4]
            leave = row[3] if len(row) > 3 and row[3] else "0"
            tag = row[5] if len(row) > 5 and row[5] else "-"
            transfers = get_transfers_safe(row)
            line = (
                f"{emj(EMOJI_MEMBER, '👤')} **{name}** — {faction}\n"
                f"{emj(EMOJI_NAV, '📅')} {start} → {end}\n"
                f"{emj(EMOJI_INFO, '🏖️')} Отгулы: **{leave}**  |  Передачи: **{transfers}**\n"
                f"💬 {tag}"
            )
            if faction in gos_factions:
                gos_list.append(line)
            else:
                opg_list.append(line)

        components = banner(BANNER_LEADERS_ALL) + [
            TextDisplay(content=f"{emj(EMOJI_MAIN, '📊')} **ВСЕ ДЕЙСТВУЮЩИЕ ЛИДЕРЫ**"),
            Separator(),
        ]
        if gos_list:
            components += [
                TextDisplay(content=f"{emj(EMOJI_INFO, '🏛️')} **ГОСУДАРСТВЕННЫЕ ОРГАНИЗАЦИИ** — {len(gos_list)}"),
                Separator(),
                TextDisplay(content="\n\n".join(gos_list)),
                Separator(),
            ]
        if opg_list:
            components += [
                TextDisplay(content=f"{emj(EMOJI_PUNISH, '🔫')} **ОПГ** — {len(opg_list)}"),
                Separator(),
                TextDisplay(content="\n\n".join(opg_list)),
                Separator(),
            ]
        components.append(TextDisplay(content="*BotChekerz • Действующие лидеры*"))
        return await inter.edit_original_response(components=[Container(*components)])

        # 🔍 ПОИСК ПО НИКУ ИЛИ ФРАКЦИИ
    found = []
    for row in rows[3:]:
        if not row or not row[0].strip():
            continue
        name = row[0]
        faction = row[1] if len(row) > 1 else ""
        if q in normalize(name) or q in normalize(faction):
            found.append(row)

    if not found:
        panel = Container(
            *banner(BANNER_LEADER_ONE),
            TextDisplay(content=f"{emj(EMOJI_MAIN, '🟢')} **ДЕЙСТВУЮЩИЕ ЛИДЕРЫ**"),
            Separator(),
            TextDisplay(content=f"❌ По запросу **{query}** ничего не найдено"),
            Separator(),
            TextDisplay(content="*BotChekerz • Действующие лидеры*")
        )
        return await inter.edit_original_response(components=[panel])

    # Если найден ровно один — красивая карточка
    if len(found) == 1:
        row = found[0]
        panel = Container(
            *banner(BANNER_LEADER_ONE),
            TextDisplay(content=f"{emj(EMOJI_MAIN, '🟢')} **ДЕЙСТВУЮЩИЙ ЛИДЕР**"),
            Separator(),
            TextDisplay(content=f"{emj(EMOJI_MEMBER, '👤')} **Игрок:** {row[0]}"),
            TextDisplay(content=f"{emj(EMOJI_INFO, '🏛️')} **Фракция:** {row[1]}"),
            TextDisplay(content=f"{emj(EMOJI_NAV, '📅')} **Назначен:** {row[2]}  →  **Конец срока:** {row[4] if len(row) > 4 else '-'}"),
            TextDisplay(content=f"{emj(EMOJI_INFO, '🏖️')} **Отгулы:** {row[3] if len(row) > 3 else '-'}  |  **Передачи:** {get_transfers_safe(row)}"),
            TextDisplay(content=f"💬 **Discord:** {row[5] if len(row) > 5 else '-'}"),
            Separator(),
            TextDisplay(content="*BotChekerz • Действующие лидеры*")
        )
        return await inter.edit_original_response(components=[panel])

    # Если найдено несколько (поиск по фракции) — список
    lines = []
    for row in found:
        name = row[0]
        faction = row[1] if len(row) > 1 else "-"
        start = row[2] if len(row) > 2 else "-"
        end = row[4] if len(row) > 4 else "-"
        leave = row[3] if len(row) > 3 and row[3] else "0"
        tag = row[5] if len(row) > 5 and row[5] else "-"
        transfers = get_transfers_safe(row)
        lines.append(
            f"{emj(EMOJI_MEMBER, '👤')} **{name}** — {faction}\n"
            f"{emj(EMOJI_NAV, '📅')} {start} → {end}\n"
            f"{emj(EMOJI_INFO, '🏖️')} Отгулы: **{leave}**  |  Передачи: **{transfers}**\n"
            f"💬 {tag}"
        )

    panel = Container(
        *banner(BANNER_LEADERS_ALL),
        TextDisplay(content=f"{emj(EMOJI_MAIN, '')} **ЛИДЕРЫ ПО ЗАПРОСУ «{query}»** — {len(found)}"),
        Separator(),
        TextDisplay(content="\n\n".join(lines)),
        Separator(),
        TextDisplay(content="*BotChekerz • Действующие лидеры*")
    )
    await inter.edit_original_response(components=[panel])
# ==========================================
# 🟠 КУРАТОРЫ ГОС
# ==========================================
@bot.slash_command(name="check_curator_org", description="Кураторы ГОС")
async def check_curator_org(inter: disnake.ApplicationCommandInteraction, org: str):
    if inter.guild is None:
        return await inter.response.send_message(DM_TEXT)
    if not await safe_defer(inter):
        return

    rows = await get_rows("curators", CSV_CURATORS)
    result = []
    for row in rows[5:]:
        for i, cell in enumerate(row):
            if org.lower() in cell.lower() and i + 1 < len(row) and row[i + 1]:
                result.append(f"• **{row[i + 1]}** — {cell}")

    components = banner(BANNER_CURATORS) + [TextDisplay(content=f"🟠 **КУРАТОРЫ {org.upper()}**"), Separator()]
    if result:
        components += [TextDisplay(content="\n".join(result)), Separator(),
                       TextDisplay(content=f"📊 **Всего кураторов:** {len(result)}")]
    else:
        components.append(TextDisplay(content=f"❌ Кураторы для **{org}** не найдены"))
    components += [Separator(), TextDisplay(content="*BotChekerz • Кураторы ГОС*")]

    await inter.edit_original_response(components=[Container(*components)])

# ==========================================
# 🟠 КУРАТОРЫ ОПГ
# ==========================================
@bot.slash_command(name="check_curator_opg", description="Кураторы ОПГ")
async def check_curator_opg(inter: disnake.ApplicationCommandInteraction, org: str):
    if inter.guild is None:
        return await inter.response.send_message(DM_TEXT)
    if not await safe_defer(inter):
        return

    mapping = {
        "курганской": ("Курган", "🟡"),
        "ореховской": ("Орехов", "🟣"),
        "тамбовской": ("Тамбов", "🟢"),
        "кавказской": ("Кавказ", "🔵"),
    }
    org_lower = org.lower()
    if org_lower not in mapping:
        return await inter.edit_original_response(content="❌ Используйте: Курганской / Ореховской / Тамбовской / Кавказской")

    keyword, emoji = mapping[org_lower]
    rows = await get_rows("curators_opg", CSV_CURATORS_OPG)
    result = []
    for row in rows:
        for i, cell in enumerate(row):
            if cell and keyword.lower() in cell.lower() and i + 1 < len(row) and row[i + 1]:
                result.append(f"• **{row[i + 1]}** — {cell}")

    components = banner(BANNER_CURATORS) + [TextDisplay(content=f"{emoji} **КУРАТОРЫ {org.capitalize()} ОПГ**"), Separator()]
    if result:
        components += [TextDisplay(content="\n".join(result)), Separator(),
                       TextDisplay(content=f"📊 **Всего кураторов:** {len(result)}")]
    else:
        components.append(TextDisplay(content="❌ Кураторы не найдены"))
    components += [Separator(), TextDisplay(content="*BotChekerz • Кураторы ОПГ*")]

    await inter.edit_original_response(components=[Container(*components)])

# ==========================================
# 📜 ИСТОРИЯ ЛИДЕРОВ
# ==========================================
@bot.slash_command(name="history_leaders", description="История лидеров")
async def history_leaders(inter: disnake.ApplicationCommandInteraction, org: str):
    if inter.guild is None:
        return await inter.response.send_message(DM_TEXT)
    if not await safe_defer(inter):
        return

    rows = await get_rows("history", CSV_HISTORY)
    org_map = {"правительство": 0, "сми": 1, "фсб": 2, "мвд-а": 3, "мвд-ю": 4, "вч": 5, "мз-а": 6, "мз-ю": 7}
    org_lower = org.lower()
    if org_lower not in org_map:
        return await inter.edit_original_response(content="❌ Используй: Правительство, СМИ, ФСБ, МВД-А, МВД-Ю, ВЧ, МЗ-А, МЗ-Ю")

    col = org_map[org_lower]
    result = [row[col] for row in rows[1:] if len(row) > col and row[col].strip()]

    if not result:
        panel = Container(
            *banner(BANNER_HISTORY),
            TextDisplay(content="📜 **ИСТОРИЯ ЛИДЕРОВ**"),
            Separator(),
            TextDisplay(content=f"❌ Нет данных по **{org.upper()}**"),
            Separator(),
            TextDisplay(content="*BotChekerz • История лидеров*")
        )
        return await inter.edit_original_response(components=[panel])

    chunks = [result[i:i + 45] for i in range(0, len(result), 45)]
    first = True
    for page, chunk in enumerate(chunks, start=1):
        numbered = "\n".join(f"**{n}.** {item}" for n, item in enumerate(chunk, start=(page - 1) * 45 + 1))
        panel = Container(
            *banner(BANNER_HISTORY),
            TextDisplay(content=f"📜 **ИСТОРИЯ ЛИДЕРОВ — {org.upper()}**"),
            TextDisplay(content=f"Страница {page}/{len(chunks)}"),
            Separator(),
            TextDisplay(content=numbered),
            Separator(),
            TextDisplay(content="ℹ️ Список может быть неточным из-за устаревших данных, ухода участников или смены никнеймов. В списке указан либо ник, либо Discord-тег."),
            Separator(),
            TextDisplay(content="*BotChekerz • История лидеров*")
        )

        if first:
            await inter.edit_original_response(components=[panel])
            first = False
        else:
            await inter.followup.send(components=[panel])

# ==========================================
# 📘 ПОМОЩЬ
# ==========================================
@bot.slash_command(name="help", description="Список команд")
async def help_command(inter: disnake.ApplicationCommandInteraction):
    if inter.guild is None:
        return await inter.response.send_message(DM_TEXT)
    if not await safe_defer(inter):
        return

    panel = Container(
        *banner(BANNER_HELP),
        TextDisplay(content="📘 **КОМАНДЫ БОТА**"),
        TextDisplay(content="Ниже список всех доступных команд:"),
        Separator(),
        TextDisplay(content="🔍 **ПРОВЕРКИ ЧС**\n`/check_org nickname` — ЧС ГОС\n`/check_opg nickname` — ЧС ОПГ"),
        Separator(),
        TextDisplay(content="🟢 **ЛИДЕРЫ**\n`/check_leaders_act query` — действующие лидеры\n• ник → информация о лидере\n• `all` → все лидеры"),
        Separator(),
        TextDisplay(content="📜 **ИСТОРИЯ**\n`/history_leaders org` — история лидеров"),
        Separator(),
        TextDisplay(content="🟠 **КУРАТОРЫ**\n`/check_curator_org org` — кураторы ГОС\n`/check_curator_opg org` — кураторы ОПГ"),
        Separator(),
        TextDisplay(content="*BotChekerz • Используй команды через /*")
    )
    await inter.edit_original_response(components=[panel])

# ==========================================
# 👑 СТАК РУКОВОДСТВА
# ==========================================
@bot.slash_command(name="stak_rukovodstvo", description="Зона ответственных кураторов")
async def stak_rukovodstvo(inter: disnake.ApplicationCommandInteraction):
    if inter.guild is None:
        return await inter.response.send_message(DM_TEXT)
    if not await safe_defer(inter):
        return

    LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    panel = Container(
        TextDisplay(content="# ✦ ЗОНА ОТВЕТСТВЕННЫХ КУРАТОРОВ"),
        TextDisplay(content="> **РУКОВОДСТВО · КООРДИНАЦИЯ · КОНТРОЛЬ**"),
        Separator(),

        TextDisplay(content="### 👑 РУКОВОДСТВО 15 СЕРВЕРА"),
        TextDisplay(content="**Главный администратор 15 сервера**\n> <@521649327224127499>"),
        TextDisplay(content="**Заместитель главного администратора**\n> <@1141900701891571812>"),
        Separator(),

        TextDisplay(
            content=(
                "> **ЦЕНТР КООРДИНАЦИИ АДМИНИСТРАЦИИ**\n>\n"
                "> В данном разделе представлен актуальный состав ответственных лиц, осуществляющих кураторство и контроль ключевых направлений проекта.\n>\n"
                "> Перед обращением внимательно определите категорию вашего вопроса и свяжитесь с ответственным куратором соответствующего направления.\n>\n"
                "> **По вопросам, выходящим за рамки конкретной категории, обращайтесь к руководству сервера.**"
            )
        ),
        Separator(),

        TextDisplay(content="### 〔01〕 🏛️ ГОСУДАРСТВЕННЫЕ ОРГАНИЗАЦИИ"),
        TextDisplay(content="**СТАРШИЙ КУРАТОР**\n> <@1282425604616228865>"),
        TextDisplay(content="**ЗАМЕСТИТЕЛЬ СТАРШЕГО КУРАТОРА**\n> <@814487893019983912>"),
        Separator(),

        TextDisplay(content="### 〔02〕 ⚔️ ОРГАНИЗОВАННЫЕ ПРЕСТУПНЫЕ ГРУППИРОВКИ"),
        TextDisplay(content="**СТАРШИЙ КУРАТОР ОПГ**\n> <@1327734598200983726>"),
        TextDisplay(content="**ЗАМЕСТИТЕЛЬ СТАРШЕГО КУРАТОРА ОПГ**\n> <@999004653620576257>"),
        Separator(),

        TextDisplay(content="### 〔03〕 🛡️ DISCORD-МОДЕРАЦИЯ"),
        TextDisplay(content="**СТАРШИЙ DISCORD-МОДЕРАТОР**\n> <@814487893019983912>"),
        TextDisplay(content="**ЗАМЕСТИТЕЛЬ СТАРШЕГО DISCORD-МОДЕРАТОРА**\n> <@1259234515042435105>"),
        Separator(),

        TextDisplay(content="### 〔04〕 🎪 МЕРОПРИЯТИЯ"),
        TextDisplay(content="**СТАРШИЙ КУРАТОР МЕРОПРИЯТИЙ**\n> <@1282425604616228865>"),
        TextDisplay(content="**ЗАМЕСТИТЕЛЬ СТАРШЕГО КУРАТОРА МЕРОПРИЯТИЙ**\n> <@1348279588739878932>"),
        Separator(),

        TextDisplay(content="### 〔05〕 🏢 НЕОФИЦИАЛЬНЫЕ ОРГАНИЗАЦИИ"),
        TextDisplay(content="**СТАРШИЙ КУРАТОР**\n> <@1088906854630969425>"),
        TextDisplay(content="**ЗАМЕСТИТЕЛЬ СТАРШЕГО КУРАТОРА**\n> <@1154806754979369011>"),
        Separator(),

        TextDisplay(content="### 〔06〕 👥 МЛАДШАЯ АДМИНИСТРАЦИЯ"),
        TextDisplay(content="**СТАРШИЙ КУРАТОР**\n> <@1280624156030799883>"),
        TextDisplay(content="**ЗАМЕСТИТЕЛЬ СТАРШЕГО КУРАТОРА**\n> <@1502649700602613910>"),
        Separator(),

        TextDisplay(content="### ✦ ПОРЯДОК ОБРАЩЕНИЯ"),
        TextDisplay(
            content=(
                "> **01** ◈ Определите направление, к которому относится ваш вопрос.\n"
                "> **02** ◈ Обратитесь к старшему куратору соответствующего направления.\n"
                "> **03** ◈ При необходимости обратитесь к его заместителю.\n"
                "> **04** ◈ Вопросы общего характера передавайте руководству сервера."
            )
        ),
        TextDisplay(content="> <a:Cute_kitty:1309599235284668436> **Просьба соблюдать уважительный и корректный формат общения с представителями администрации.**"),
        Separator(),

        TextDisplay(content="**15 SERVER · ADMINISTRATION DEPARTMENT**"),
        TextDisplay(content="*Система кураторства · Координация · Актуальная информация*"),
    )

    await inter.edit_original_response(components=[panel])

# ==========================================
bot.run("код токен")
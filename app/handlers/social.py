from __future__ import annotations

import time
from telebot import types

from app.context import AppContext
from app.data import RARITY_ALIASES, RARITY_LABELS
from app.handlers.common import antispam_callback, edit_or_send_text, ensure_player
from app.keyboards import build_collection_keyboard, build_social_keyboard
from app.utils.formatters import format_cooldown

SOCIAL_TEXT = '🤝 <b>Социальное</b>\n\nЗдесь живут кланы, аукцион и обмен.'
AUCTION_PICK_STATE: dict[int, dict] = {}


# ---------- keyboards ----------
def _build_clan_keyboard(clan, clans: list) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if clan:
        keyboard.add(types.InlineKeyboardButton('🚪 Выйти из клана', callback_data='clan_leave'))
    else:
        keyboard.add(types.InlineKeyboardButton('➕ Создать свой клан', callback_data='clan_create'))
        for item in clans:
            keyboard.add(types.InlineKeyboardButton(f'👥 [{item["tag"]}] {item["name"]}', callback_data=f'clan_join_{item["id"]}'))
    keyboard.add(types.InlineKeyboardButton('🏆 Топ кланов', callback_data='clan_top'))
    keyboard.add(types.InlineKeyboardButton('🔄 Обновить', callback_data='social_clans'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад в социальное', callback_data='menu_social'))
    return keyboard


def _build_auction_keyboard(auctions: list) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔨 Запустить аукцион', callback_data='auction_sell'))
    for item in auctions:
        keyboard.add(types.InlineKeyboardButton(f'📣 Аукцион #{item["id"]} — {item["current_price"]} coins', callback_data=f'a_view_{item["id"]}'))
    keyboard.add(types.InlineKeyboardButton('🔄 Обновить', callback_data='social_auction'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад в социальное', callback_data='menu_social'))
    return keyboard


def _build_pick_keyboard(prefix: str, index: int, total: int, card_id: int) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    row = []
    if index > 0:
        row.append(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'{prefix}_prev'))
    if index < total - 1:
        row.append(types.InlineKeyboardButton('➡️ Вперёд', callback_data=f'{prefix}_next'))
    if row:
        keyboard.row(*row)
    keyboard.add(types.InlineKeyboardButton('✅ Выбрать карту', callback_data=f'{prefix}_select_{card_id}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ К выбору редкости', callback_data=f'{prefix}_pick_back'))
    keyboard.add(types.InlineKeyboardButton('🤝 Социальное', callback_data='menu_social'))
    return keyboard


def _build_auction_price_keyboard(card_id: int) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for price in (400, 800, 1200, 2000):
        keyboard.add(types.InlineKeyboardButton(f'{price} coins', callback_data=f'a_price_{card_id}_{price}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад к аукциону', callback_data='social_auction'))
    return keyboard


def _build_auction_view_keyboard(auction_id: int, current_price: int) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for step in (100, 300, 500):
        keyboard.add(types.InlineKeyboardButton(f'+{step}', callback_data=f'a_bid_{auction_id}_{current_price + step}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад к аукционам', callback_data='social_auction'))
    return keyboard


# ---------- rendering ----------
def _send_social_menu(ctx: AppContext, target, user) -> None:
    ensure_player(ctx, user)
    edit_or_send_text(ctx, target, SOCIAL_TEXT, build_social_keyboard())


def _clan_tag_for(user) -> str:
    if getattr(user, 'username', None):
        raw = ''.join(ch for ch in user.username.upper() if ch.isalnum())
    else:
        raw = f'U{user.id}'
    return (raw[:6] or f'U{user.id}')


def _render_clans(ctx: AppContext, target, user) -> None:
    ensure_player(ctx, user)
    clan = ctx.db.get_user_clan(user.id)
    clans = ctx.db.list_clans(limit=6)
    if clan:
        lines = [
            '👥 <b>Кланы</b>',
            '',
            f'Твой клан: [{clan["tag"]}] {clan["name"]}',
            f'Роль: {clan["role"]}',
            f'Клановый XP: {clan["xp"]}',
            '',
            'Можешь остаться, посмотреть топ или выйти из клана.',
        ]
    else:
        lines = ['👥 <b>Кланы</b>', '', 'Ты пока не состоишь в клане.']
        if clans:
            lines.append('Открытые кланы:')
            for item in clans:
                lines.append(f'• [{item["tag"]}] {item["name"]} — {item["members_count"]} уч. / {item["xp"]} XP')
        else:
            lines.append('Пока нет ни одного клана. Создай первый!')
    edit_or_send_text(ctx, target, '\n'.join(lines), _build_clan_keyboard(clan, clans))


def _render_clan_top(ctx: AppContext, target) -> None:
    clans = ctx.db.list_clans(limit=10)
    lines = ['🏆 <b>Топ кланов</b>', '']
    if clans:
        for idx, clan in enumerate(clans, start=1):
            lines.append(f'{idx}. [{clan["tag"]}] {clan["name"]} — {clan["xp"]} XP • {clan["members_count"]} уч.')
    else:
        lines.append('Кланов пока нет.')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад к кланам', callback_data='social_clans'))
    edit_or_send_text(ctx, target, '\n'.join(lines), keyboard)


def _render_auction(ctx: AppContext, target, user) -> None:
    ensure_player(ctx, user)
    stats = ctx.db.get_stats(user.id)
    auctions = ctx.db.list_auctions(limit=8)
    lines = ['🔨 <b>Аукцион</b>', '', f'Твой баланс: {stats["coins"]} coins', '']
    if auctions:
        now = time.time()
        for item in auctions:
            remaining = max(0, int(float(item['ends_at']) - now))
            lines.append(f'#{item["id"]} — <b>{item["artist"]}</b> / {item["name"]} • {item["current_price"]} coins • {format_cooldown(remaining)}')
    else:
        lines.append('Активных аукционов нет.')
    edit_or_send_text(ctx, target, '\n'.join(lines), _build_auction_keyboard(auctions))


def _show_pick_card(ctx: AppContext, chat_id: int, user_id: int, state: dict, prefix: str) -> None:
    cards_list = state['cards_list']
    index = state['index']
    card = cards_list[index]
    text = (
        f'<b>ID:</b> {card["id"]}\n'
        f'🎤 <b>{card["artist"]}</b>\n'
        f'💿 {card["name"]}\n'
        f'✨ {RARITY_LABELS.get(card["rarity"], card["rarity"])}\n\n'
        f'Карта {index + 1} из {len(cards_list)}\n\n'
        'Выбери карту для аукциона.'
    )
    ctx.bot.send_message(chat_id, text, reply_markup=_build_pick_keyboard(prefix, index, len(cards_list), card['id']))


# ---------- handlers ----------
def register_social_handlers(ctx: AppContext) -> None:
    bot = ctx.bot

    @bot.callback_query_handler(func=lambda c: c.data == 'menu_social')
    def open_social(call):
        if not antispam_callback(ctx, call, 'menu_social'):
            return
        _send_social_menu(ctx, call.message, call.from_user)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data == 'social_clans')
    def social_clans(call):
        if not antispam_callback(ctx, call, 'social_clans'):
            return
        _render_clans(ctx, call.message, call.from_user)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data == 'clan_top')
    def clan_top(call):
        if not antispam_callback(ctx, call, 'clan_top'):
            return
        _render_clan_top(ctx, call.message)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data == 'clan_create')
    def clan_create(call):
        if not antispam_callback(ctx, call, 'clan_create'):
            return
        ensure_player(ctx, call.from_user)
        base_tag = _clan_tag_for(call.from_user)
        tag = base_tag
        existing_tags = {str(item['tag']) for item in ctx.db.list_clans(limit=200)}
        suffix = 1
        while tag in existing_tags:
            suffix += 1
            tag = f'{base_tag[:4]}{suffix}'[:10]
        clan_name = f'Клан {call.from_user.username or call.from_user.id}'
        ok, message = ctx.db.create_clan(call.from_user.id, tag, clan_name)
        if ok:
            ctx.db.log_event(call.from_user.id, 'clan_created', {'tag': tag})
        bot.answer_callback_query(call.id, message)
        _render_clans(ctx, call.message, call.from_user)

    @bot.callback_query_handler(func=lambda c: c.data.startswith('clan_join_'))
    def clan_join(call):
        if not antispam_callback(ctx, call, 'clan_join'):
            return
        clan_id = int(call.data.split('_')[2])
        ok, message = ctx.db.join_clan(call.from_user.id, clan_id)
        if ok:
            clan = ctx.db.get_user_clan(call.from_user.id)
            if clan:
                ctx.db.log_event(call.from_user.id, 'clan_joined', {'tag': clan['tag']})
        bot.answer_callback_query(call.id, message)
        _render_clans(ctx, call.message, call.from_user)

    @bot.callback_query_handler(func=lambda c: c.data == 'clan_leave')
    def clan_leave(call):
        if not antispam_callback(ctx, call, 'clan_leave'):
            return
        ok, message = ctx.db.leave_clan(call.from_user.id)
        bot.answer_callback_query(call.id, message)
        _render_clans(ctx, call.message, call.from_user)

    @bot.callback_query_handler(func=lambda c: c.data == 'social_auction')
    def social_auction(call):
        if not antispam_callback(ctx, call, 'social_auction'):
            return
        _render_auction(ctx, call.message, call.from_user)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data == 'auction_sell')
    def auction_sell(call):
        if not antispam_callback(ctx, call, 'auction_sell'):
            return
        ensure_player(ctx, call.from_user)
        edit_or_send_text(ctx, call.message, '🔨 <b>Запустить аукцион</b>\n\nСначала выбери редкость карты:', build_collection_keyboard(prefix='auction_collection'))
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data.startswith('auction_collection_'))
    def auction_collection(call):
        if not antispam_callback(ctx, call, 'auction_collection', limit=8, window_seconds=3):
            return
        rarity_key = call.data.split('_', maxsplit=2)[2]
        rarity = RARITY_ALIASES.get(rarity_key, 'single')
        cards = ctx.db.get_user_cards_by_rarity(call.from_user.id, rarity)
        if not cards:
            bot.answer_callback_query(call.id, '📭 В этой коллекции нет карт.')
            return
        AUCTION_PICK_STATE[call.from_user.id] = {'cards_list': cards, 'index': 0}
        _show_pick_card(ctx, call.message.chat.id, call.from_user.id, AUCTION_PICK_STATE[call.from_user.id], 'auction')
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data in {'auction_prev', 'auction_next'})
    def auction_nav(call):
        if not antispam_callback(ctx, call, 'auction_nav', limit=10, window_seconds=3):
            return
        state = AUCTION_PICK_STATE.get(call.from_user.id)
        if not state:
            bot.answer_callback_query(call.id, 'Сначала выбери редкость.')
            return
        state['index'] = min(state['index'] + 1, len(state['cards_list']) - 1) if call.data.endswith('next') else max(state['index'] - 1, 0)
        _show_pick_card(ctx, call.message.chat.id, call.from_user.id, state, 'auction')
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data == 'auction_pick_back')
    def auction_back(call):
        if not antispam_callback(ctx, call, 'auction_back'):
            return
        edit_or_send_text(ctx, call.message, '🔨 <b>Запустить аукцион</b>\n\nСначала выбери редкость карты:', build_collection_keyboard(prefix='auction_collection'))
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data.startswith('auction_select_'))
    def auction_select(call):
        if not antispam_callback(ctx, call, 'auction_select', limit=6, window_seconds=3):
            return
        card_id = int(call.data.split('_')[2])
        card = ctx.db.get_user_card(call.from_user.id, card_id)
        if not card:
            bot.answer_callback_query(call.id, 'Карта не найдена.')
            return
        text = (
            f'<b>ID:</b> {card["id"]}\n🎤 <b>{card["artist"]}</b>\n💿 {card["name"]}\n✨ {RARITY_LABELS.get(card["rarity"], card["rarity"])}\n\nВыбери стартовую цену аукциона (длительность 12 часов).'
        )
        edit_or_send_text(ctx, call.message, text, _build_auction_price_keyboard(card_id))
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data.startswith('a_price_'))
    def auction_price(call):
        if not antispam_callback(ctx, call, 'auction_price', limit=5, window_seconds=3):
            return
        _, _, card_id_raw, price_raw = call.data.split('_')
        ok, message = ctx.db.create_auction(call.from_user.id, int(card_id_raw), int(price_raw), duration_hours=12)
        if ok:
            ctx.db.log_event(call.from_user.id, 'auction_created', {'card_id': int(card_id_raw), 'price': int(price_raw)})
        bot.answer_callback_query(call.id, message)
        _render_auction(ctx, call.message, call.from_user)

    @bot.callback_query_handler(func=lambda c: c.data.startswith('a_view_'))
    def auction_view(call):
        if not antispam_callback(ctx, call, 'auction_view'):
            return
        auction_id = int(call.data.split('_')[2])
        auction = ctx.db.get_auction(auction_id)
        if not auction or auction['status'] != 'active':
            bot.answer_callback_query(call.id, 'Аукцион уже недоступен.')
            _render_auction(ctx, call.message, call.from_user)
            return
        remaining = max(0, int(float(auction['ends_at']) - time.time()))
        bidder = auction['highest_bidder_id'] or 'пока нет'
        text = (
            '🔨 <b>Аукцион</b>\n\n'
            f'Лот #{auction["id"]}\n'
            f'🎤 <b>{auction["artist"]}</b>\n'
            f'💿 {auction["name"]}\n'
            f'✨ {RARITY_LABELS.get(auction["rarity"], auction["rarity"])}\n\n'
            f'Текущая ставка: {auction["current_price"]} coins\n'
            f'Лидер: {bidder}\n'
            f'До конца: {format_cooldown(remaining)}'
        )
        edit_or_send_text(ctx, call.message, text, _build_auction_view_keyboard(auction_id, int(auction['current_price'])))
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda c: c.data.startswith('a_bid_'))
    def auction_bid(call):
        if not antispam_callback(ctx, call, 'auction_bid', limit=5, window_seconds=3):
            return
        _, _, auction_id_raw, amount_raw = call.data.split('_')
        ok, message = ctx.db.place_bid(call.from_user.id, int(auction_id_raw), int(amount_raw))
        if ok:
            ctx.db.log_event(call.from_user.id, 'auction_bid', {'auction_id': int(auction_id_raw), 'amount': int(amount_raw)})
        bot.answer_callback_query(call.id, message)
        auction = ctx.db.get_auction(int(auction_id_raw))
        if auction and auction['status'] == 'active':
            remaining = max(0, int(float(auction['ends_at']) - time.time()))
            bidder = auction['highest_bidder_id'] or 'пока нет'
            text = (
                '🔨 <b>Аукцион</b>\n\n'
                f'Лот #{auction["id"]}\n'
                f'🎤 <b>{auction["artist"]}</b>\n'
                f'💿 {auction["name"]}\n'
                f'✨ {RARITY_LABELS.get(auction["rarity"], auction["rarity"])}\n\n'
                f'Текущая ставка: {auction["current_price"]} coins\n'
                f'Лидер: {bidder}\n'
                f'До конца: {format_cooldown(remaining)}'
            )
            edit_or_send_text(ctx, call.message, text, _build_auction_view_keyboard(int(auction_id_raw), int(auction['current_price'])))
        else:
            _render_auction(ctx, call.message, call.from_user)

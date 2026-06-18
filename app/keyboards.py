from __future__ import annotations

from telebot import types


def build_main_menu() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🎴 Получить карту')
    keyboard.row('📋 Меню')
    keyboard.row('ℹ️ Помощь')
    return keyboard


def build_inline_menu() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('👤 Профиль', callback_data='menu_profile'),
        types.InlineKeyboardButton('📚 Мои карты', callback_data='menu_collection'),
    )
    keyboard.add(
        types.InlineKeyboardButton('🎁 Ежедневная награда', callback_data='menu_daily'),
        types.InlineKeyboardButton('🏆 Топ', callback_data='menu_top'),
    )
    keyboard.add(
        types.InlineKeyboardButton('🛒 Магазин', callback_data='menu_shop'),
        types.InlineKeyboardButton('🎰 Рулетка', callback_data='menu_roulette'),
    )
    keyboard.add(types.InlineKeyboardButton('🤝 Социальное', callback_data='menu_social'))
    keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data='menu_close'))
    return keyboard


def build_social_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton('👥 Кланы', callback_data='social_clans'))
    keyboard.add(types.InlineKeyboardButton('🔨 Аукцион', callback_data='social_auction'))
    keyboard.add(types.InlineKeyboardButton('🔄 Обменять карту', callback_data='menu_trade'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад в меню', callback_data='menu_back'))
    return keyboard


def build_collection_keyboard(prefix: str = 'show') -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🎴 Single', callback_data=f'{prefix}_single'))
    keyboard.add(types.InlineKeyboardButton('💿 Album', callback_data=f'{prefix}_album'))
    keyboard.add(types.InlineKeyboardButton('✨ Limited Edition', callback_data=f'{prefix}_limited'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад в меню', callback_data='menu_back'))
    return keyboard


def build_shop_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🎴 Случайная карта (500 XP)', callback_data='shop_buy_card'))
    keyboard.add(types.InlineKeyboardButton('📦 Basic Pack (900 XP)', callback_data='shop_pack_basic'))
    keyboard.add(types.InlineKeyboardButton('🚀 Premium Pack (1800 XP)', callback_data='shop_pack_premium'))
    keyboard.add(types.InlineKeyboardButton('⏱ Снять кулдаун (250 XP)', callback_data='shop_remove_cooldown'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад в меню', callback_data='menu_back'))
    return keyboard

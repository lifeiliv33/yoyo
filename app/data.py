from __future__ import annotations

CARD_POOL = {
    'single': [
        {'artist': '9mice', 'name': 'Anora'},
        {'artist': '17 SEVENTEEN', 'name': 'Конфетка'},
        {'artist': 'Sqwore', 'name': 'Life of a emorapstar'},
        {'artist': 'madk1d', 'name': 'Толпы'},
        {'artist': 'madk1d', 'name': 'Круче чем вы'},
        {'artist': 'rizza', 'name': 'Quinn'},
        {'artist': 'rizza', 'name': 'punkthed'},
        {'artist': 'rizza', 'name': 'Лучший друг'},
        {'artist': 'rizza', 'name': 'lifeilive'},
        {'artist': 'rizza', 'name': 'Одуванчик'},
        {'artist': 'rizza', 'name': 'void'},
        {'artist': 'Sqwore, rizza', 'name': 'Плачь'},
        {'artist': 'Sqwore, rizza', 'name': 'Холодное оружие'},
        {'artist': 'Kai Angel', 'name': 'limousine music'},
        {'artist': 'Kai Angel', 'name': 'lovesong'},
        {'artist': 'Kai Angel', 'name': 'quiet turn up'},
        {'artist': '17 SEVENTEEN', 'name': 'Конфетка'},
        
    ],
    'album': [
        {'artist': 'Kai Angel, 9mice', 'name': 'HEAVY METAL'},
        {'artist': 'Kai Angel', 'name': 'GOD SYSTEM'},
        {'artist': 'Kai Angel, 9mice', 'name': 'HEAVY METAL 2'},
        {'artist': 'Kai Angel', 'name': 'damage'},
        {'artist': '9mice, Kai Angel', 'name': 'HEAVY METAL'},
        {'artist': '9mice, Kai Angel', 'name': 'HEAVY METAL 2'},
        {'artist': 'zavet', 'name': 'doom'},
        {'artist': 'zavet', 'name': 'velvet heaven'},
        {'artist': '17 SEVENTEEN', 'name': 'Песочный Человек'},
        {'artist': '17 SEVENTEEN', 'name': 'Две тысячи семнадцатый'},
        {'artist': 'Sqwore', 'name': 'eve'},
        {'artist': 'Sqwore', 'name': 'eve 2'},
        {'artist': 'madk1d', 'name': 'Он сказал поехали!'},
        {'artist': 'madk1d', 'name': 'мир, труд, май'},
        {'artist': 'rizza', 'name': '626'},
        {'artist': '17 SEVENTEEN', 'name': 'Мы Смеялись Никто Не Понял'},
        {'artist': '17 SEVENTEEN', 'name': 'Поцелуи между барами'},
        {'artist': '17 SEVENTEEN', 'name': 'Гипнофобия'},
        {'artist': 'rizza', 'name': 'Мёртвые мысли'},
        {'artist': 'rizza', 'name': 'Плохая концовка'},
        {'artist': 'rizza', 'name': 'Безумия бездны'},
        {'artist': '17 SEVENTEEN, Sqwore', 'name': 'BOO!'},
        
    ],
    'limited edition': [
        {'artist': 'Kai Angel', 'name': 'are you happy'},
        {'artist': '9mice', 'name': 'u+me/stranger'},
        {'artist': 'zavet', 'name': 'goth tv'},
        {'artist': '17 SEVENTEEN, Sqwore', 'name': 'Как я провела лето'},
        {'artist': 'Sqwore, 17 SEVENTEEN', 'name': 'Как я провела лето'},
        {'artist': 'rizza', 'name': 'welcome to limbo'},
    ],
}

RARITY_LABELS = {
    'single': '🎴 Single',
    'album': '💿 Album',
    'limited edition': '✨ Limited Edition',
}

RARITY_ALIASES = {
    'single': 'single',
    'album': 'album',
    'limited': 'limited edition',
    'limited_edition': 'limited edition',
}

RARITY_ORDER = ['single', 'album', 'limited edition']

XP_VALUES = {
    'single': 25,
    'album': 50,
    'limited edition': 100,
}

RARITY_WEIGHTS = [
    ('single', 60),
    ('album', 30),
    ('limited edition', 10),
]

PACKS = {
    'basic': {
        'title': '📦 Basic Pack',
        'cost': 900,
        'cards_count': 3,
        'guaranteed': 'album',
    },
    'premium': {
        'title': '🚀 Premium Pack',
        'cost': 1800,
        'cards_count': 5,
        'guaranteed': 'limited edition',
    },
}

CARD_IMAGES: dict[tuple[str, str], str] = {
    ('9mice', 'Anora'): 'assets/anora.png',
    ('Kai Angel, 9mice', 'HEAVY METAL 2'): 'assets/hm2.png',
    ('9mice, Kai Angel', 'HEAVY METAL 2'): 'assets/hm2.png',
    ('9mice, Kai Angel', 'HEAVY METAL'): 'assets/hm.png',
    ('Kai Angel, 9mice', 'HEAVY METAL'): 'assets/hm.png',
    ('zavet', 'doom'): 'assets/doom.png',
    ('Kai Angel', 'damage'): 'assets/damage.png',
    ('Sqwore', 'Life of a emorapstar'): 'assets/emorapstar.png',
    ('Sqwore', 'eve'): 'assets/eve.png',
    ('Sqwore', 'eve 2'): 'assets/eve2.png',
    ('Sqwore', 'Холодное оружие'): 'assets/holodgun.png',
    ('Kai Angel', 'GOD SYSTEM'): 'assets/godsystem.png',
    ('madk1d', 'Он сказал поехали!'): 'assets/poekhali.png',
    ('madk1d', 'Толпы'): 'assets/tolpy.png',
    ('madk1d', 'мир, труд, май'): 'assets/mirtrudmay.png',
    ('9mice', 'u+me/stranger'): 'assets/ume.png',
    ('zavet', 'velvet heaven'): 'assets/velvet.png',
    ('Kai Angel', 'are you happy'): 'assets/damage.png',
    ('Kai Angel', 'quiet turn up'): 'assets/quietturnup.png',
    ('Kai Angel', 'lovesong'): 'assets/lovesong.jpg',
    ('Kai Angel', 'limousine music'): 'assets/limousine.png',
    ('Kai Angel', 'quiet turn up'): 'assets/quietturnup.png',
    ('madk1d', 'Круче чем вы'): 'assets/kruche.png',
    ('Kai Angel', 'quiet turn up'): 'assets/quietturnup.png',
    ('rizza', 'Мёртвые мысли'): 'assets/mertivemisly.png',
    ('rizza', '626'): 'assets/626.png',
    ('rizza', 'Лучший друг'): 'assets/luchidrug.png',
    ('rizza', 'Плохая концовка'): 'assets/plohaya.png',
    ('rizza', 'Безумия бездны'): 'assets/bezumiya.png',
    ('rizza', 'Одуванчик'): 'assets/oduvanchik.png',
    ('rizza', 'Лучший друг'): 'assets/luchiydrug.jpg',
    ('rizza', 'welcome to limbo'): 'assets/welcometolimbo.jpg',
    ('rizza', 'punkthed'): 'assets/phunkted.png',
    ('rizza', 'void'): 'assets/void.jpg',
    ('rizza', 'Quinn'): 'assets/queen.jpg',
    ('rizza', 'lifeilive'): 'assets/livealife.png',
    ('Sqwore, rizza', 'Плачь'): 'assets/plach.png',
    ('Sqwore, rizza', 'Холодное оружие'): 'assets/holodgun.png',
    ('17 SEVENTEEN', 'Поцелуи между барами'): 'assets/pochelui.png',
    ('17 SEVENTEEN', 'Две тысячи семнадцатый'): 'assets/2017.png',
    ('17 SEVENTEEN, Sqwore', 'BOO!'): 'assets/boo.png',
    ('17 SEVENTEEN', 'Гипнофобия'): 'assets/gipnofobia.png',
    ('17 SEVENTEEN', 'Конфетка'): 'assets/konfetka.jpg',
    ('17 SEVENTEEN', 'Мы Смеялись Никто Не Понял'): 'assets/msmeyalis.png',
    ('17 SEVENTEEN', 'Песочный человек'): 'assets/peshocniy.png',
    ('17 SEVENTEEN, Sqwore', 'Как я провела лето'): 'assets/kakyaleto.jpg',
    ('Sqwore, 17 SEVENTEEN', 'Как я провела лето'): 'assets/kakyaleto.jpg',
}

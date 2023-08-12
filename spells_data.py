from PIL import Image, ImageTk
import tkinter as tk


def get_spell_function(spell):
    spell_cooldowns = {
        'Barrier': 180,  # 屏障
        'Clarity': 240,  # 清晰术
        'Cleanse': 210,  # 净化
        'Exhaust': 210,  # 虚弱
        'Flash': 300,  # 闪现
        'Ghost': 210,  # 疾跑
        'Heal': 240,  # 治疗术
        'Ignite': 180,  # 点燃
        'Mark': 80,  # 雪球
        'Smite': 90,  # 惩戒
        'Teleport': 360,  # 传送
    }
    cooldown = spell_cooldowns.get(spell)

    return cooldown


class SpellSetup:
    def __init__(self):
        self.spells = [
            ('Barrier', 'summoner_spells/Barrier.jpg', (0.1428, 0.4), get_spell_function('Barrier')),
            ('Clarity', 'summoner_spells/Clarity.jpg', (0.2856, 0.4), get_spell_function('Clarity')),
            ('Cleanse', 'summoner_spells/Cleanse.jpg', (0.4284, 0.4), get_spell_function('Cleanse')),
            ('Exhaust', 'summoner_spells/Exhaust.jpg', (0.5712, 0.4), get_spell_function('Exhaust')),
            ('Flash', 'summoner_spells/Flash.jpg', (0.714, 0.4), get_spell_function('Flash')),
            ('Ghost', 'summoner_spells/Ghost.jpg', (0.8568, 0.4), get_spell_function('Ghost')),
            ('Heal', 'summoner_spells/Heal.jpg', (0.1428, 0.6), get_spell_function('Heal')),
            ('Ignite', 'summoner_spells/Ignite.jpg', (0.2856, 0.6), get_spell_function('Ignite')),
            ('Mark', 'summoner_spells/Mark.jpg', (0.4284, 0.6), get_spell_function('Mark')),
            ('Smite', 'summoner_spells/Smite.jpg', (0.5712, 0.6), get_spell_function('Smite')),
            ('Teleport', 'summoner_spells/Teleport.jpg', (0.714, 0.6), get_spell_function('Teleport')),
        ]

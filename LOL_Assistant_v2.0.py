"""pyinstaller -F -w LOL_Assistant_v2.0.py"""

import speech_recognition as sr
import threading

from legends_data import *
from spells_data import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("英雄联盟助手")
        self.geometry("800x500")
        # self.iconbitmap('ico/favicon.ico')
        self['background'] = '#000000'
        self.current_role = None

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # grid行列的权重配置
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, HeroSelect, SpellsSelect):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont, role=None, index=None):
        frame = self.frames[cont]
        frame.tkraise()
        # 如果提供了角色，则将其存储为当前角色
        if role is not None:
            self.current_role = role
        # 选择变换的召唤师技能位置
        if index is not None:
            frame.current_index = index

    def update_role_image(self, role_name, img_path):
        self.frames[HomePage].roles[role_name].update_image(img_path)

    def update_role_function(self, role, function):
        self.frames[HomePage].roles[role].legends_function = function


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg='#000000')

        Page1_label = tk.Label(self, text='LOL助手', font=('楷体', 15), fg='#FFFFFF', bg="#000000")
        Page1_label.place(relx=0.5, rely=0.08, anchor='center')

        # Create Roles
        self.roles = {}
        self.roles['TOP'] = Role(self, controller, 'TOP', 'legends_portrait/Aatrox.jpg', 0.21,
                                 get_legends_function('Aatrox'), get_spell_function('Flash'),
                                 get_spell_function('Ignite'))
        self.roles['JG'] = Role(self, controller, 'JG', 'legends_portrait/Belveth.jpg', 0.38,
                                get_legends_function('Belveth'), get_spell_function('Flash'),
                                get_spell_function('Ignite'))
        self.roles['MID'] = Role(self, controller, 'MID', 'legends_portrait/Ahri.jpg', 0.55,
                                 get_legends_function('Ahri'), get_spell_function('Flash'),
                                 get_spell_function('Ignite'))
        self.roles['ADC'] = Role(self, controller, 'ADC', 'legends_portrait/Jinx.jpg', 0.72,
                                 get_legends_function('Jinx'), get_spell_function('Flash'),
                                 get_spell_function('Ignite'))
        self.roles['SUP'] = Role(self, controller, 'SUP', 'legends_portrait/Milio.jpg', 0.89,
                                 get_legends_function('Milio'), get_spell_function('Flash'),
                                 get_spell_function('Ignite'))


class Role(tk.Frame):
    def __init__(self, root, controller, role_name, img_path, rel_y, legends_function, spell_function_1,
                 spell_function_2):
        self.root = root
        self.role_name = role_name
        self.img_path = img_path
        self.legends_function = legends_function
        self.spell_function_1 = spell_function_1
        self.spell_function_2 = spell_function_2

        # 创建角色画布
        self.canvas = tk.Canvas(self.root, width=750, height=70, bg="#A9A9A9")
        self.canvas.place(relx=0.5, rely=rel_y, anchor='center')

        # 选择角色按钮
        self.img = Image.open(self.img_path)
        self.img = self.img.resize((50, 50), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)
        self.button = tk.Button(self.canvas, image=self.img,
                                command=lambda: controller.show_frame(HeroSelect, self.role_name))
        self.button.place(relx=0.05, rely=0.5, anchor='center')

        # 等级
        level_label = tk.Label(self.canvas, text="Level:", font=('楷体', 14), fg='#000000', bg='#A9A9A9')
        level_label.place(relx=0.14, rely=0.4, anchor='center')
        self.level_var = tk.StringVar()
        self.level_var.set('1')  # 初始等级为1
        level = tk.Label(self.canvas, textvariable=self.level_var, font=('楷体', 14), fg='#000000', bg='#A9A9A9')
        level.place(relx=0.2, rely=0.4, anchor='center')
        # 等级上升
        level_up = tk.Button(self.canvas, text='+', font=('楷体', 10), width=1, height=1,
                             fg='#000000', bg='#A9A9A9', command=lambda: self.increase_level('base', 18))
        level_up.place(relx=0.23, rely=0.4, anchor='center')
        # 等级下降
        level_down = tk.Button(self.canvas, text='-', font=('楷体', 10), width=1, height=1,
                               fg='#000000', bg='#A9A9A9', command=lambda: self.decrease_level('base'))
        level_down.place(relx=0.26, rely=0.4, anchor='center')

        # Q技能等级
        self.ico_Q = Image.open('ico/Q.png')
        self.ico_Q = self.ico_Q.resize((20, 20), Image.LANCZOS)
        self.ico_Q = ImageTk.PhotoImage(self.ico_Q)
        self.Q_level_button = tk.Button(self.canvas, image=self.ico_Q, command=lambda: self.start('Q'))
        self.Q_level_button.place(relx=0.32, rely=0.4, anchor='center')
        self.Q_time_label = tk.Label(self.canvas, text='', font=('Helvetica', 10), bg='#A9A9A9')
        self.Q_time_label.place(relx=0.36, rely=0.8, anchor='center')

        self.Q_level_var = tk.StringVar()
        self.Q_level_var.set('1')  # 初始等级为1
        Q_level = tk.Label(self.canvas, textvariable=self.Q_level_var, font=('楷体', 14), fg='#000000',
                           bg='#A9A9A9')
        Q_level.place(relx=0.35, rely=0.4, anchor='center')
        # Q技能等级上升
        Q_level_up = tk.Button(self.canvas, text='+', font=('楷体', 10), width=1, height=1,
                               fg='#000000', bg='#A9A9A9', command=lambda: self.increase_level('Q', 5))
        Q_level_up.place(relx=0.38, rely=0.4, anchor='center')
        # Q技能等级下降
        Q_level_down = tk.Button(self.canvas, text='-', font=('楷体', 10), width=1, height=1,
                                 fg='#000000', bg='#A9A9A9', command=lambda: self.decrease_level('Q'))
        Q_level_down.place(relx=0.41, rely=0.4, anchor='center')

        # W技能等级
        self.ico_W = Image.open('ico/W.png')
        self.ico_W = self.ico_W.resize((20, 20), Image.LANCZOS)
        self.ico_W = ImageTk.PhotoImage(self.ico_W)
        self.W_level_button = tk.Button(self.canvas, image=self.ico_W, command=lambda: self.start('W'))
        self.W_level_button.place(relx=0.47, rely=0.4, anchor='center')
        self.W_time_label = tk.Label(self.canvas, text='', font=('Helvetica', 10), bg='#A9A9A9')
        self.W_time_label.place(relx=0.51, rely=0.8, anchor='center')

        self.W_level_var = tk.StringVar()
        self.W_level_var.set('1')  # 初始等级为1
        W_level = tk.Label(self.canvas, textvariable=self.W_level_var, font=('楷体', 14), fg='#000000',
                           bg='#A9A9A9')
        W_level.place(relx=0.5, rely=0.4, anchor='center')
        # W技能等级上升
        W_level_up = tk.Button(self.canvas, text='+', font=('楷体', 10), width=1, height=1,
                               fg='#000000', bg='#A9A9A9', command=lambda: self.increase_level('W', 5))
        W_level_up.place(relx=0.53, rely=0.4, anchor='center')
        # W技能等级下降
        W_level_down = tk.Button(self.canvas, text='-', font=('楷体', 10), width=1, height=1,
                                 fg='#000000', bg='#A9A9A9', command=lambda: self.decrease_level('W'))
        W_level_down.place(relx=0.56, rely=0.4, anchor='center')

        # E技能等级
        self.ico_E = Image.open('ico/E.png')
        self.ico_E = self.ico_E.resize((20, 20), Image.LANCZOS)
        self.ico_E = ImageTk.PhotoImage(self.ico_E)
        self.E_level_button = tk.Button(self.canvas, image=self.ico_E, command=lambda: self.start('E'))
        self.E_level_button.place(relx=0.62, rely=0.4, anchor='center')
        self.E_time_label = tk.Label(self.canvas, text='', font=('Helvetica', 10), bg='#A9A9A9')
        self.E_time_label.place(relx=0.66, rely=0.8, anchor='center')

        self.E_level_var = tk.StringVar()
        self.E_level_var.set('1')  # 初始等级为1
        E_level = tk.Label(self.canvas, textvariable=self.E_level_var, font=('楷体', 14), fg='#000000',
                           bg='#A9A9A9')
        E_level.place(relx=0.65, rely=0.4, anchor='center')
        # E技能等级上升
        E_level_up = tk.Button(self.canvas, text='+', font=('楷体', 10), width=1, height=1,
                               fg='#000000', bg='#A9A9A9', command=lambda: self.increase_level('E', 5))
        E_level_up.place(relx=0.68, rely=0.4, anchor='center')
        # E技能等级下降
        E_level_down = tk.Button(self.canvas, text='-', font=('楷体', 10), width=1, height=1,
                                 fg='#000000', bg='#A9A9A9', command=lambda: self.decrease_level('E'))
        E_level_down.place(relx=0.71, rely=0.4, anchor='center')

        # R技能等级
        self.ico_R = Image.open('ico/R.png')
        self.ico_R = self.ico_R.resize((20, 20), Image.LANCZOS)
        self.ico_R = ImageTk.PhotoImage(self.ico_R)
        self.R_level_button = tk.Button(self.canvas, image=self.ico_R, command=lambda: self.start('R'))
        self.R_level_button.place(relx=0.77, rely=0.4, anchor='center')
        self.R_time_label = tk.Label(self.canvas, text='', font=('Helvetica', 10), bg='#A9A9A9')
        self.R_time_label.place(relx=0.81, rely=0.8, anchor='center')

        self.R_level_var = tk.StringVar()
        self.R_level_var.set('1')  # 初始等级为1
        R_level = tk.Label(self.canvas, textvariable=self.R_level_var, font=('楷体', 14), fg='#000000',
                           bg='#A9A9A9')
        R_level.place(relx=0.8, rely=0.4, anchor='center')
        # R技能等级上升
        R_level_up = tk.Button(self.canvas, text='+', font=('楷体', 10), width=1, height=1,
                               fg='#000000', bg='#A9A9A9', command=lambda: self.increase_level('R', 3))
        R_level_up.place(relx=0.83, rely=0.4, anchor='center')
        # R技能等级下降
        R_level_down = tk.Button(self.canvas, text='-', font=('楷体', 10), width=1, height=1,
                                 fg='#000000', bg='#A9A9A9', command=lambda: self.decrease_level('R'))
        R_level_down.place(relx=0.86, rely=0.4, anchor='center')

        # 召唤师技能冷却时间
        self.spell1_cooldown = 0
        self.spell2_cooldown = 0

        # 召唤师技能1
        summoner_spells_1 = Image.open('summoner_spells/Flash.jpg')
        summoner_spells_resized_1 = summoner_spells_1.resize((25, 25), Image.LANCZOS)
        self.summoner_spells_1 = ImageTk.PhotoImage(summoner_spells_resized_1)
        self.summoner_spells_choose_btn_1 = tk.Button(self.canvas, image=self.summoner_spells_1,
                                                      command=self.get_summoner_spells_function(controller, 1))
        self.summoner_spells_choose_btn_1.place(relx=0.92, rely=0.27, anchor='center')
        # 计时器
        self.spells_1_time_button = tk.Button(self.canvas, bg='#A9A9A9', height=1, width=4,
                                              command=lambda: self.start_cooldown(1))
        self.spells_1_time_button.place(relx=0.97, rely=0.27, anchor='center')
        self.spells_1_time_label = tk.Label(self.canvas, text='', font=('Helvetica', 10), bg='#A9A9A9')
        self.spells_1_time_label.place(relx=0.97, rely=0.27, anchor='center')

        # 召唤师技能2
        summoner_spells_2 = Image.open('summoner_spells/Ignite.jpg')
        summoner_spells_resized_2 = summoner_spells_2.resize((25, 25), Image.LANCZOS)
        self.summoner_spells_2 = ImageTk.PhotoImage(summoner_spells_resized_2)
        self.summoner_spells_choose_btn_2 = tk.Button(self.canvas, image=self.summoner_spells_2,
                                                      command=self.get_summoner_spells_function(controller, 2))
        self.summoner_spells_choose_btn_2.place(relx=0.92, rely=0.73, anchor='center')
        # 计时器
        self.spells_2_time_button = tk.Button(self.canvas, bg='#A9A9A9', height=1, width=4,
                                              command=lambda: self.start_cooldown(2))
        self.spells_2_time_button.place(relx=0.97, rely=0.73, anchor='center')
        self.spells_2_time_label = tk.Label(self.canvas, text='', font=('Helvetica', 10), bg='#A9A9A9')
        self.spells_2_time_label.place(relx=0.97, rely=0.73, anchor='center')

        self.level_vars = {
            'base': self.level_var,
            'Q': self.Q_level_var,
            'W': self.W_level_var,
            'E': self.E_level_var,
            'R': self.R_level_var
        }

        self.ability_dict = {
            'Q': {'cooldown': 0, 'cooldown_spare': 0, 'is_running': False, 'label': self.Q_time_label},
            'W': {'cooldown': 0, 'cooldown_spare': 0, 'is_running': False, 'label': self.W_time_label},
            'E': {'cooldown': 0, 'cooldown_spare': 0, 'is_running': False, 'label': self.E_time_label},
            'R': {'cooldown': 0, 'cooldown_spare': 0, 'is_running': False, 'label': self.R_time_label},
        }

    def update_image(self, img_path):
        """更新英雄头像"""
        self.img_path = img_path
        img = Image.open(self.img_path)
        img = img.resize((50, 50), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(img)
        self.button.config(image=self.img)

    def increase_level(self, level_key, max_level):
        """英雄技能等级上升"""
        current_level = int(self.level_vars[level_key].get())
        if current_level < max_level:
            self.level_vars[level_key].set(str(current_level + 1))

    def decrease_level(self, level_key):
        """英雄技能等级下降"""
        current_level = int(self.level_vars[level_key].get())
        if current_level > 1:
            self.level_vars[level_key].set(str(current_level - 1))

    def start(self, ability):
        """英雄技能进入冷却"""
        Q_level = int(self.Q_level_var.get())
        W_level = int(self.W_level_var.get())
        E_level = int(self.E_level_var.get())
        R_level = int(self.R_level_var.get())
        self.Q_cooldown, self.W_cooldown, self.E_cooldown, self.R_cooldown = self.legends_function(Q_level, W_level,
                                                                                                   E_level, R_level, 0)
        if ability == 'Q':
            self.ability_dict[ability]['cooldown'] = self.Q_cooldown
        if ability == 'W':
            self.ability_dict[ability]['cooldown'] = self.W_cooldown
        if ability == 'E':
            self.ability_dict[ability]['cooldown'] = self.E_cooldown
        if ability == 'R':
            self.ability_dict[ability]['cooldown'] = self.R_cooldown

        self.ability_dict[ability]['cooldown_spare'] = self.ability_dict[ability]['cooldown']

        if not self.ability_dict[ability]['is_running']:
            self.ability_dict[ability]['is_running'] = True
            self.update_cooldown(ability)
        else:
            self.ability_dict[ability]['is_running'] = False
            self.ability_dict[ability]['cooldown_spare'] = self.ability_dict[ability]['cooldown']
            self.ability_dict[ability]['label'].configure(text='')

    def update_cooldown(self, ability):
        """英雄技能冷却倒计时"""
        if self.ability_dict[ability]['is_running']:
            self.ability_dict[ability]['label'].configure(text=self.ability_dict[ability]['cooldown_spare'])
            if self.ability_dict[ability]['cooldown_spare'] > 0:
                self.ability_dict[ability]['cooldown_spare'] -= 1
                self.root.after(1000, lambda: self.update_cooldown(ability))
            else:
                self.ability_dict[ability]['label'].configure(text='Time\'s up!')

    def get_summoner_spells_function(self, controller, index):
        """获取召唤师技能函数"""
        return lambda: controller.show_frame(SpellsSelect, self.role_name, index)

    def update_spell_image(self, spell_img_path, index=1):
        """更新召唤师技能图片"""
        spell_img = Image.open(spell_img_path)
        spell_img = spell_img.resize((25, 25), Image.LANCZOS)

        if index == 1:
            self.summoner_spells_img_1 = ImageTk.PhotoImage(spell_img)
            self.summoner_spells_choose_btn_1.config(image=self.summoner_spells_img_1)
        else:
            self.summoner_spells_img_2 = ImageTk.PhotoImage(spell_img)
            self.summoner_spells_choose_btn_2.config(image=self.summoner_spells_img_2)

    def update_spell_function(self, spell_function, index=1):
        """更新召唤师技能函数"""
        if index == 1:
            self.spell_function_1 = spell_function
        else:
            self.spell_function_2 = spell_function

    def start_cooldown(self, spell_number):
        """召唤师技能进入冷却"""
        # setattr函数用于将指定法术的冷却时间（由spell_function_{spell_number}属性给出）设置为法术的初始冷却时间
        setattr(self, f'spell{spell_number}_cooldown', getattr(self, f'spell_function_{spell_number}'))
        self.cooldown_counter(spell_number)

    def cooldown_counter(self, spell_number):
        """召唤师技能冷却倒计时"""
        spell_cooldown = getattr(self, f'spell{spell_number}_cooldown')  # 获得召唤师技能冷却时间
        if spell_cooldown > 0:
            setattr(self, f'spell{spell_number}_cooldown', spell_cooldown - 1)  # 冷却时间-1
            getattr(self, f'spells_{spell_number}_time_label')['text'] = str(spell_cooldown - 1)
            self.root.after(1000, self.cooldown_counter, spell_number)  # 在1秒后再次调用cooldown_counter函数
        else:
            getattr(self, f'spells_{spell_number}_time_label')['text'] = ''  # 如果冷却时间小于0，则清空标签


class HeroSelect(tk.Frame):
    """英雄选择界面"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.config(bg='#000000')

        self.frame2 = tk.Frame(self, width=800, height=500, bg='#000000')
        self.frame2.pack()

        Page2_label = tk.Label(self.frame2, text='英雄选择', font=('楷体', 15), fg='#FFFFFF', bg="#000000")
        Page2_label.place(relx=0.5, rely=0.08, anchor='center')

        self.button_names = ['TOP', 'JG', 'MID', 'ADC', 'SUP']
        self.buttons = []
        self.canvases = []

        for i, name in enumerate(self.button_names):
            button = tk.Button(self.frame2, text=name, font=('Times New Roman', 12), width=6, height=1,
                               bg="#696969", command=lambda i=i: self.show_canvas(i))
            button.place(relx=0.15 + i * 0.09, rely=0.17, anchor='center')
            self.buttons.append(button)

            canvas = tk.Canvas(self.frame2, width=700, height=360, bg="#A9A9A9")
            canvas.place(relx=0.5, rely=0.57, anchor='center')
            if i != 0:  # 隐藏其他四个界面
                canvas.place_forget()
            self.canvases.append(canvas)

        # 上单英雄
        TOP_hero_setup = TopHeroSetup()
        for hero_name, img_path, (relx, rely), legends_function in TOP_hero_setup.heroes:
            self.add_hero_button(self.canvases[0], img_path, relx, rely, legends_function)

        # 打野英雄
        JG_hero_setup = JgHeroSetup()
        for hero_name, img_path, (relx, rely), legends_function in JG_hero_setup.heroes:
            self.add_hero_button(self.canvases[1], img_path, relx, rely, legends_function)

        # 中单英雄
        MID_hero_setup = MidHeroSetup()
        for hero_name, img_path, (relx, rely), legends_function in MID_hero_setup.heroes:
            self.add_hero_button(self.canvases[2], img_path, relx, rely, legends_function)

        # ADC英雄
        ADC_hero_setup = AdcHeroSetup()
        for hero_name, img_path, (relx, rely), legends_function in ADC_hero_setup.heroes:
            self.add_hero_button(self.canvases[3], img_path, relx, rely, legends_function)

        # 辅助英雄
        SUP_hero_setup = SupHeroSetup()
        for hero_name, img_path, (relx, rely), legends_function in SUP_hero_setup.heroes:
            self.add_hero_button(self.canvases[4], img_path, relx, rely, legends_function)

    def show_canvas(self, i):
        """放置不同位置的canvas"""
        for canvas in self.canvases:
            canvas.place_forget()
        self.canvases[i].place(relx=0.5, rely=0.57, anchor='center')

    def add_hero_button(self, root, img_path, relx, rely, legends_function):
        """添加英雄头像按钮"""
        img = Image.open(img_path)
        img = img.resize((50, 50), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        button = tk.Button(root, image=img, command=self.get_update_role_function(img_path, legends_function))
        button.place(relx=relx, rely=rely, anchor='center')
        # 保留对图像对象的引用，以防止其被垃圾收集
        button.image = img

    def get_update_role_function(self, img_path, legends_function):
        """更新英雄技能函数"""
        return lambda: (self.controller.update_role_image(self.controller.current_role, img_path),
                        self.controller.update_role_function(self.controller.current_role, legends_function),
                        self.controller.show_frame(HomePage))


class SpellsSelect(tk.Frame):
    """召唤师技能选择界面"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.config(bg='#000000')
        self.current_index = 1

        self.frame3 = tk.Frame(self, width=800, height=500, bg='#000000')
        self.frame3.pack()

        Page3_label = tk.Label(self.frame3, text='召唤师技能选择', font=('楷体', 15), fg='#FFFFFF', bg="#000000")
        Page3_label.place(relx=0.5, rely=0.08, anchor='center')

        spell_setup = SpellSetup()
        for hero_name, img_path, (relx, rely), legends_function in spell_setup.spells:
            self.add_spell_button(self.frame3, img_path, relx, rely, legends_function)

    def add_spell_button(self, root, img_path, relx, rely, legends_function):
        """添加召唤师技能按钮"""
        img = Image.open(img_path)
        img = img.resize((50, 50), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        button = tk.Button(root, image=img, command=self.get_update_spell_function(img_path, legends_function))
        button.place(relx=relx, rely=rely, anchor='center')
        # 保留对图像对象的引用，以防止其被垃圾收集
        button.image = img

    def get_update_spell_function(self, img_path, spell_function):
        """更新召唤师技能函数"""
        return lambda: (
            self.controller.frames[HomePage].roles[self.controller.current_role].update_spell_image(img_path,
                                                                                                    self.current_index),
            self.controller.frames[HomePage].roles[self.controller.current_role].update_spell_function(spell_function,
                                                                                                       self.current_index),
            self.controller.show_frame(HomePage)
        )


def listen_commands():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio, language='zh-CN')
            print("You said: " + command)

            if '上单的召唤师技能1' in command:
                app.frames[HomePage].roles['TOP'].start_cooldown(1)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


if __name__ == '__main__':
    app = App()
    threading.Thread(target=listen_commands).start()
    app.mainloop()

import random
import time
import tkinter as tk
import os
import threading
from pygame import mixer
import math

# 抑制libpng警告
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# 播放背景音乐
def play_music():
    mixer.init()
    music_file = "background.mp3"
    if os.path.exists(music_file):
        mixer.music.load(music_file)
        mixer.music.play(-1)
    else:
        print("未找到背景音乐文件 background.mp3（可选）")

def stop_music():
    try:
        mixer.music.stop()
    except:
        pass

# 创建淡入淡出的窗口
def create_beautiful_tip(root, x=None, y=None):
    window = tk.Toplevel(root)
    window_width, window_height = 300, 120
    screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()

    if x is None or y is None:
        x = random.randint(100, screen_width - window_width - 100)
        y = random.randint(100, screen_height - window_height - 100)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.resizable(False, False)
    window.attributes('-topmost', True)
    window.attributes('-alpha', 0.0)

    schemes = [
        {'bg': '#FFE4E6', 'fg': '#BE123C', 'accent': '#FB7185'},
        {'bg': '#F0F9FF', 'fg': '#0369A1', 'accent': '#0EA5E9'},
        {'bg': '#F0FDF4', 'fg': '#15803D', 'accent': '#22C55E'},
        {'bg': '#FEF7CD', 'fg': '#854D0E', 'accent': '#EAB308'},
        {'bg': '#FAF5FF', 'fg': '#7C3AED', 'accent': '#A855F7'},
    ]
    s = random.choice(schemes)
    window.configure(bg=s['bg'])

    tips = [
        '💧 记得多喝水哦~', '😊 保持微笑，好运自然来', '✨ 今天也要元气满满！',
        '🌙 早点休息别熬夜', '🍀 今天过得开心吗？', '💪 你是最棒的！',
        '🎶 听首喜欢的歌吧', '🌈 一切都会好起来', '🍫 奖励一下自己吧~'
    ]
    icons = ['💕', '✨', '🌟', '🎀', '🌷', '🌸', '🍀']

    tk.Label(window, text=random.choice(icons), bg=s['bg'], fg=s['accent'], font=('Arial', 22)).place(x=20, y=30)
    tk.Label(window, text=random.choice(tips), bg=s['bg'], fg=s['fg'],
             font=('微软雅黑', 12), wraplength=200, justify='left').place(x=60, y=35)

    tk.Button(window, text='关闭', bg=s['accent'], fg='white', font=('微软雅黑', 9),
              command=window.destroy, relief='flat').place(
        x=window_width - 60, y=window_height - 30, width=50, height=25
    )

    fade_in(window)

def fade_in(window):
    alpha = 0.0
    while alpha < 1.0:
        alpha += 0.05
        window.attributes('-alpha', alpha)
        window.update()
        time.sleep(0.03)

def heart_positions(center_x, center_y, scale=25, num_points=20):

    positions = []
    for t in [i * 2*math.pi/num_points for i in range(num_points)]:
        x = scale * 16 * math.sin(t)**3 + center_x
        y = -scale * (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)) + center_y
        positions.append((int(x), int(y)))
    return positions

def main():
    root = tk.Tk()
    root.withdraw()
    root.title("温馨提示程序")

    def quit_all(event=None):
        print("🎈 程序结束，再见！")
        stop_music()
        for w in root.winfo_children():
            if isinstance(w, tk.Toplevel):
                w.destroy()
        root.destroy()

    root.bind("<space>", quit_all)

    threading.Thread(target=play_music, daemon=True).start()

    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    # 心形窗口先排列
    heart_pos = heart_positions(screen_width//2 - 150, screen_height//2 - 100, scale=25, num_points=20)
    for x, y in heart_pos:
        create_beautiful_tip(root, x, y)
        root.update()
        time.sleep(0.05)

    # 再随机出现窗口
    MAX_WINDOWS = 8
    for i in range(100):
        create_beautiful_tip(root)
        root.update()
        time.sleep(0.8)
        windows = [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)]
        if len(windows) > MAX_WINDOWS:
            windows[0].destroy()

    root.mainloop()

if __name__ == "__main__":
    main()

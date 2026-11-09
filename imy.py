import tkinter as tk
import pygame
import time


LYRICS = [
    (0, "Dear Mamabear,"),
    (5, "I just want to take this chance to tell you how much I love you and how thankful I am to have you as my mom."),
    (17, "I know we didn't get to spend most of my childhood together because you had to work far away just to give me a better life, and I know that wasn't easy for you either."),
    (34, "Even though you weren't always physically here, I want you to know that I appreciate every little and big thing you did for me."),
    (48, "I may not have fully understood your sacrifices when I was younger, but as I grow older, I realize just how much love it took for you to make those choices."),
    (65, "You had to miss so many little moments just so I could have a better future, and I will always be thankful for that."),
    (78, "Thank you, Ma, for everything."),
    (85, "I hope you know that all your hard work means so much to me."),

    (99, "I know there were many moments when you wished you could be here with me, especially during birthdays, school events, and other little milestones."),
    (114, "I can only imagine how hard it must have been to watch me grow up from miles away instead of being here to experience those moments with me."),
    (131, "But I hope you know that I understand why you had to make that choice, and I will never blame you for it."),
    (144, "You worked hard and spent so much time away from home just to make sure I could have the things I needed and a better future."),
    (159, "I may not have been able to spend every childhood memory with you, but I will always appreciate the love and care you gave me in every way you could."),
    (176, "Thank you for choosing to give me a better life, even when it meant making things harder for yourself."),

    (192, "Thank you for being strong for me and Mama Nia, for continuing to work hard even when things get tiring."),
    (205, "Thank you for every sacrifice, every reminder, every little treat, and every time you make sure I have what I need."),
    (218, "Thank you for providing all of my needs and wants, no matter how much they cost."),
    (230, "Thank you for everything, Mama."),
    (238, "I hope you also remember to take care of yourself too."),
    (248, "You spend so much time thinking about my future that I hope you don't forget to enjoy your own life too."),
    (263, "You deserve to rest, be happy, and live life to the fullest too."),
    (275, "I want you to know that I am always proud of you, Ma, and I hope I can make you proud as well."),
  
    (290, "I hope you know that no matter how many miles were between us, you have always been and will always be my mom, my home, and my wondermom!"),
    (306, "I know I can never give back all the things you've sacrificed just to give me a better future, but I hope that someday, I can make life a little easier for you, the same way you've always tried to make life better for me."),
    (329, "I want to see you happy, enjoy the things you love, and finally have more time for yourself after all those years of working so hard."),
    (344, "You deserve all the good things in this world, Ma."),
    (353, "I may not always say it, and I may still be your maldita na anak who sometimes gives you a headache, but please never doubt how much I love you."),
    (370, "Thank you for everything, Ma."),
    (380, "I love you so much, and I hope I get to make you feel as loved as you have always made me feel."),

    (400, "With love,"),
    (408, "Yanisupercute"),
]

BOX_W, BOX_H = 350, 300
FONT = ("Helvetica", 25, "bold")
BG_COLOR = "#fdfdf5"
FG_COLOR = "#111111"

RISE_SPEED = 125
BOTTOM_SPAWN_OFFSET = 0
GAP = 40

class LyricCard:
    def __init__(self, parent, text, x, y):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=BG_COLOR)
        self.win.geometry(f"{BOX_W}x{BOX_H}+{int(x)}+{int(y)}")
        self.win.resizable(False, False)
        self.full_text = text
        self.label = tk.Label(
            self.win,
            text="",
            font=FONT,
            bg=BG_COLOR,
            fg=FG_COLOR,
            wraplength=BOX_W - 25,
            justify="center"
        )
        self.label.pack(expand=True, fill="both", padx=15, pady=15)
        self.typewriter_index = 0
        self.x = x
        self.y = float(y)
        self.flip_state = False
        self.typewriter()

    def typewriter(self):
        if self.typewriter_index <= len(self.full_text):
            self.label.config(text=self.full_text[:self.typewriter_index])
            self.typewriter_index += 1
            self.win.after(75, self.typewriter)

    def rise(self, dy):
        self.y -= dy
        self.win.geometry(f"{BOX_W}x{BOX_H}+{int(self.x)}+{int(self.y)}")

    def is_offscreen(self):
        return self.y + BOX_H < -50

class LyricFloatApp:
    def __init__(self, root):
        self.root = root
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        self.next_lyric_idx = 0
        self.boxes = []
        self.last_frame_time = None
        self.current_side = "left"
        self.start()

    def random_safe_x(self):
        center_x = self.screen_w // 2
        spacing = BOX_W + 60
        left_x = center_x - spacing
        right_x = center_x + 60
        if self.current_side == "left":
            self.current_side = "right"
            return left_x
        else:
            self.current_side = "left"
            return right_x

    def start(self):
        self.root.iconify()
        self.start_time = time.time()
        self.last_frame_time = self.start_time
        self.tick()
        self.flip_all()
        pygame.mixer.music.play()

    def flip_all(self):
        for box in self.boxes:
            if box.flip_state:
                box.win.config(bg="white")
                box.label.config(bg="white", fg="black")
            else:
                box.win.config(bg="black")
                box.label.config(bg="black", fg="white")
            box.flip_state = not box.flip_state
        self.root.after(150, self.flip_all)

    def tick(self):
        now = time.time()
        elapsed = now - self.start_time
        dt = now - self.last_frame_time
        self.last_frame_time = now

        while (self.next_lyric_idx < len(LYRICS) and
               LYRICS[self.next_lyric_idx][0] <= elapsed):
            t, text = LYRICS[self.next_lyric_idx]
            x = self.random_safe_x()
            if self.boxes:
                y = self.boxes[-1].y + BOX_H + GAP
            else:
                y = self.screen_h - BOX_H - BOTTOM_SPAWN_OFFSET
            box = LyricCard(self.root, text, x, y)
            self.boxes.append(box)
            self.next_lyric_idx += 1

        dy = RISE_SPEED * dt

        for box in self.boxes:
            box.rise(dy)

        still_visible = []

        for box in self.boxes:
            if box.is_offscreen():
                try:
                    box.win.destroy()
                except tk.TclError:
                    pass
            else:
                still_visible.append(box)

        self.boxes = still_visible

        if self.next_lyric_idx < len(LYRICS) or self.boxes:
            self.root.after(16, self.tick)

if __name__ == "__main__":
    root = tk.Tk()
    app = LyricFloatApp(root)
    root.mainloop()

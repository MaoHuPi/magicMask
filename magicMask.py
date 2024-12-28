import os
import random
import tkinter as tk
import PIL.Image, PIL.ImageTk, PIL.ImageGrab
import keyboard
path = '.' if os.path.isfile('./'+os.path.basename(__file__)) else os.path.dirname(os.path.abspath(__file__))
run = True
width, height = 200, 200
transparent = '#171300'
aniFrame = 300
win = tk.Tk()
win.attributes("-alpha", 0.5)
win.attributes("-disabled", False) # 是否可被系統工具列遮住
win.attributes("-topmost", True)
win.attributes("-toolwindow", True)
win.attributes('-transparentcolor', transparent)
win.resizable(0, 0)
win.overrideredirect(True) # 是否隱藏視窗框
os.environ['SDL_WINDOWID'] = str(win.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
screenWidth, screenHeight = win.winfo_screenwidth(), win.winfo_screenheight()
win.geometry("{w}x{h}+{x}+{y}".format(w = int(screenWidth), h = int(screenHeight), x = int(0), y = int(0)))
win.configure(bg = transparent)

cvs = tk.Canvas(win, width = int(screenWidth), height = int(screenHeight), highlightthickness = 0) # highlightthickness 為 canvas 的 bolder-width
cvs.pack(fill = 'both')
cvs.configure(bg = transparent)
# cvs.create_text(100, 50, text='Hello World') # 文字
# cvs.create_oval(10, 10, 100, 100, fill='red') # 圓形
# img = PIL.Image.open(path+'/../../../image/logo.png')
# img = img.resize((100, 100), PIL.Image.ANTIALIAS)
# img = PIL.ImageTk.PhotoPIL.Image(img)
# cvs.create_image(int(screenWidth-100-50), int(screenHeight-100-50), anchor = tk.NW, image = img) # 圖片

win.update()

colors = {'red':'red', 'orange':'orange', 'yellow':'yellow', 'green':'green', 'blue':'blue', 'purple':'purple'}
colorNames = [name for name in colors]
class magicDot:
    def __init__(self, x = random.randint(0, screenWidth), y = random.randint(0, screenHeight), speed = 5):
        self.x = x
        self.y = y
        self.Dx = random.randrange(1, 2)*random.choice([1, -1])
        self.Dy = random.randrange(1, 2)*random.choice([1, -1])
        self.speed = speed
    def update(self):
        if self.x < 0 or self.x > screenWidth:
            self.Dx = -self.Dx
        if self.y < 0 or self.y > screenHeight:
            self.Dy = -self.Dy
        self.x += self.Dx*self.speed
        self.y += self.Dy*self.speed
class magicShape:
    def __init__(self, point = 4, color = '', speed = 5):
        self.dots = [magicDot(random.randint(0, screenWidth), random.randint(0, screenHeight), speed = speed) for _ in range(point)]
        self.color = color if color != '' else colors[random.choice(colorNames)]
    def update(self):
        for dot in self.dots:
            dot.update()
    def draw(self, isShadow = False):
        points = []
        for dot in self.dots:
            points.append(dot.x)
            points.append(dot.y)
        if isShadow:
            cvs.create_polygon(*points, fill='', outline = 'white', width = screenWidth*0.02, joinstyle = 'round')
        else:
            cvs.create_polygon(*points, fill='', outline = self.color, width = screenWidth*0.01, joinstyle = 'round')
            # cvs.create_polygon(*points, fill='', outline = self.color, width = screenWidth*0.01, joinstyle = 'round', dash = (200, 1, 1, 1))
            # cvs.create_polygon(*points, fill='', outline = self.color, width = screenWidth*0.01, joinstyle = 'round', smooth = 1)
def creatMagicShape(shapeNumber):
    global colors
    useableColors = []
    shapes = []
    for _ in range(shapeNumber):
        if len(useableColors) < 1:
            useableColors = [*colorNames]
        color = random.choice(useableColors)
        shapes.append(magicShape(color = colors[color], speed = 3))
        useableColors.remove(color)
    return(shapes)
shapes = creatMagicShape(2)
mask = 0
maskMode = 'none'
shot = False
def maskOpen():
    global maskMode, shapes
    maskMode = 'open'
    shapes = creatMagicShape(2)
def maskClose():
    global maskMode
    maskMode = 'close'
def quit():
    global run
    run = False
def screenShot():
    global shot
    shot = True

keyboard.add_hotkey('alt+ctrl+m', maskOpen)
keyboard.add_hotkey('alt+ctrl+u', maskClose)
keyboard.add_hotkey('alt+ctrl+q', quit)
keyboard.add_hotkey('alt+ctrl+s', screenShot)

while run:
    # r_w = random.randint(0, screenWidth)
    # r_h = random.randint(0, screenHeight)
    # win.geometry("+"+str(r_w)+"+"+str(r_h))
    # print(screenWidth, screenHeight)
    if maskMode != 'none':
        if maskMode == 'open' and mask < aniFrame:
            cvs.delete("all")
            mask += 1
        elif maskMode == 'close' and mask > 0:
            cvs.delete("all")
            mask -= 1
        else:
            maskMode = 'none'
        maskSize = mask/aniFrame
        cvs.create_rectangle(int(screenWidth*(1-maskSize)/2), int(screenHeight*(1-maskSize)/2), int(screenWidth*(1+maskSize)/2), int(screenHeight*(1+maskSize)/2), fill = 'black')
    if mask == aniFrame:
        cvs.delete("all")
        cvs.create_rectangle(0, 0, int(screenWidth), int(screenHeight), fill = 'black')
        for shape in shapes:
            cvs.scale(1, 0, 0, 0.5, 1)
            shape.draw(isShadow = True)
        for shape in shapes:
            cvs.scale(1, 0, 0, 1, 1)
            shape.update()
            shape.draw()
    win.update()
    if shot:
        shotName = '/cvsShot.eps'
        cvs.postscript(file = path+shotName, colormode = 'color')
        # shotImg = PIL.Image.open(path+shotName)
        # shotImg.convert('RGBA')
        # shotName.split('.')
        # shotName[-1] = '.png'
        # shotName = '.'.join(shotName)
        # shotImg.save(path+shotName)
        shot = False
win.destroy()
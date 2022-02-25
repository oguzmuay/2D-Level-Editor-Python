import pygame as pg


class Canvas(pg.Rect):
    def __init__(self, x, y, w, h):
        pg.Rect.__init__(self, x, y, w, h)

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class Panel(pg.Rect):
    def __init__(self, master, x, y, w, h, screen, color, borderRadius=0):
        pg.Rect.__init__(self, master.getX() + x, master.getY() + y, w, h)
        self.leftX = x
        self.topY = y
        self.master = master
        self.screen = screen
        self.color = color
        self.borderRadius = borderRadius

    def Draw(self):
        self.left = self.master.getX() + self.leftX
        self.top = self.master.getY() + self.topY
        pg.draw.rect(self.screen, self.color, self, border_radius=self.borderRadius)

    def getX(self):
        return self.left

    def getY(self):
        return self.top


class Button(pg.Rect):
    def __init__(self, master, x, y, w, h, text, screen, color, clickAction=[], clickArg=[], hoverAction=[],
                 hoverArg=[], hoverColor=(120, 120, 120), clickColor=(140, 140, 140),
                 textColor=(255, 255, 255), borderRadius=0):
        pg.Rect.__init__(self, master.getX() + x, master.getY() + y, w, h)
        self.master = master
        self.leftX = x
        self.topY = y
        self.text = text
        self.clickAction = clickAction
        self.clickArg = clickArg
        self.hoverAction = hoverAction
        self.hoverArg = hoverArg
        self.screen = screen
        self.clicked = False
        self.normalColor = color
        self.hoverColor = hoverColor
        self.clickColor = clickColor
        self.textColor = textColor
        self.borderRadius = borderRadius
        self.textObj = pg.font.SysFont(None, 20).render(self.text, 1, self.textColor)

    def Click(self):
        if len(self.clickAction) > 0:
            self.clicked = False
            for i in range(len(self.clickAction)):
                self.clickAction[i](self.clickArg[i])

    def Hover(self):
        for i in range(len(self.hoverAction)):
            self.hoverAction[i](self.hoverArg[i])
        if pg.mouse.get_pressed()[0] == 1:
            pg.draw.rect(self.screen, self.clickColor, self, border_radius=self.borderRadius)
            self.clicked = True
        else:
            if self.clicked:
                self.Click()
            pg.draw.rect(self.screen, self.hoverColor, self, border_radius=self.borderRadius)

    def ChangeText(self, text):
        self.text = text
        self.textObj = pg.font.SysFont(None, 20).render(self.text, True, self.textColor)

    def Update(self, mousePos):
        textRect = self.textObj.get_rect()
        textRect.midtop = (self.x + (self.width / 2), self.y + (self.height / 4))
        self.left = self.master.getX() + self.leftX
        self.top = self.master.getY() + self.topY
        if self.collidepoint(mousePos):
            self.Hover()
        else:
            self.clicked = False
            pg.draw.rect(self.screen, self.normalColor, self, border_radius=self.borderRadius)
        self.screen.blit(self.textObj, textRect)


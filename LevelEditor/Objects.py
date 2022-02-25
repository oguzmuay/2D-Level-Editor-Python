import UI.UI as UI
import UI.Color as Color
import glob
import pygame as pg


# This Module Created For Objects(Chest etc.)

class AssetsMenu(UI.Panel):
    def __init__(self, master, x, y, w, h, screen, color, tileSize):
        super().__init__(master, x, y, w, h, screen, color)
        self.menuIndex = 0
        self.slotFrameIndex = -1
        self.tileMenu = []
        self.propsMenu = []
        self.tileSize = tileSize
        self.selectedSlot = [-1, -1]
        self.informationPanel = UI.Panel(master, 0, 0, 100, 56, screen, Color.Grey())
        self.tileButton = UI.Button(self, 16, 13, 175, 32, "TILES", screen, Color.Black(),
                                    [self.ChangeMenuIndex], [0], borderRadius=4)
        self.propsButton = UI.Button(self, 207, 13, 175, 32, "PROPS", screen, Color.Black(),
                                     [self.ChangeMenuIndex], [1], borderRadius=4)

    def SelectedSlotChange(self, index):
        self.selectedSlot[0] = self.menuIndex
        self.selectedSlot[1] = index

    def ShowInfPanel(self, tile):
        textObject = pg.font.SysFont(None, 20).render(f"RealSize: {tile.realRect.w}X{tile.realRect.h}", 1,
                                                      Color.White())
        self.informationPanel.left = tile.left + 32
        self.informationPanel.top = tile.top + 32
        self.informationPanel.w = 68 + textObject.get_rect().w
        pg.draw.rect(self.screen, self.informationPanel.color, self.informationPanel,
                     self.informationPanel.borderRadius)
        self.screen.blit(tile.image, (self.informationPanel.left + 12, self.informationPanel.top + 12))
        self.screen.blit(textObject, (self.informationPanel.left + 56, self.informationPanel.top + (
                self.informationPanel.h - textObject.get_rect().h) / 2))

    def LoadAssets(self, screen):
        slots = glob.glob("../Assets/tiles/*.png")
        for i in range(len(slots)):
            tile = pg.image.load(slots[i])
            slot = Slot(self, 39 * (i % 10) + 10, 64 * (i // 10) + 72, 32, 32, "", screen, Color.White(), i,
                        pg.transform.scale(tile, (self.tileSize, self.tileSize)), tile.get_rect(),
                        clickAction=[self.SelectedSlotChange],
                        clickArg=[i])
            self.tileMenu.append(slot)
        slots = glob.glob("../Assets/props/*.png")
        for i in range(len(slots)):
            prop = pg.image.load(slots[i])
            slot = Slot(self, 39 * (i % 10) + 10, 64 * (i // 10) + 60, 32, 32, "", screen, Color.White(), i,
                        pg.transform.scale(prop, (self.tileSize, self.tileSize)), prop.get_rect(),
                        clickAction=[self.SelectedSlotChange],
                        clickArg=[i])
            self.propsMenu.append(slot)

    def Start(self):
        self.LoadAssets(self.screen)

    def Update(self, mousePos):
        self.Draw()
        self.tileButton.Update(mousePos)
        self.propsButton.Update(mousePos)
        if self.menuIndex == 0:
            for tile in reversed(self.tileMenu):
                tile.Blit(mousePos)
                if self.slotFrameIndex == tile.slotId:
                    pg.draw.rect(self.screen, Color.Black(), pg.Rect(tile.left, tile.top, tile.w, tile.h), 2)
                    self.ShowInfPanel(tile)
        elif self.menuIndex == 1:
            for prop in reversed(self.propsMenu):
                prop.Blit(mousePos)
                if self.slotFrameIndex == prop.slotId:
                    pg.draw.rect(self.screen, Color.Black(), pg.Rect(prop.left, prop.top, prop.w, prop.h), 2)
                    self.ShowInfPanel(prop)

    def SetSlotFrameIndex(self, mousePos, slotList):
        index = -1
        for i in range(len(slotList)):
            if slotList[i].left <= mousePos[0] <= slotList[i].left + 32 and (
                    slotList[i].top <= mousePos[1] <= slotList[i].top + 32):
                index = i
        self.slotFrameIndex = index

    def MouseMove(self, mousePos):
        if self.menuIndex == 0:
            self.SetSlotFrameIndex(mousePos, self.tileMenu)
        elif self.menuIndex == 1:
            self.SetSlotFrameIndex(mousePos, self.propsMenu)
        elif self.menuIndex == 2:
            self.SetSlotFrameIndex(mousePos, self.specialMenu)

    def ChangeMenuIndex(self, index):
        self.menuIndex = index


class Slot(UI.Button):
    """
    This is a Slot...........
    """
    # Change Blit Function
    def __init__(self, master, x, y, w, h, text, screen, color, index, image, Rect, hoverAction=None, hoverArg=None,
                 clickAction=None, clickArg=None):
        super().__init__(master, x, y, w, h, text, screen, color)
        if hoverAction is None:
            hoverAction = []
        if hoverArg is None:
            hoverArg = []
        if clickAction is None:
            clickAction = []
        if clickArg is None:
            clickArg = []
        self.slotId = index
        self.image = image
        self.realRect = Rect
        self.hoverAction = hoverAction
        self.hoverArg = hoverArg
        self.clickAction = clickAction
        self.clickArg = clickArg

    def Blit(self, mousePos):
        self.left = self.master.getX() + self.leftX
        self.top = self.master.getY() + self.topY
        self.screen.blit(pg.transform.scale(self.image, (32, 32)), (self.left, self.top))
        if self.collidepoint(mousePos):
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
            else:
                if self.clicked:
                    self.Click()
        else:
            self.clicked = False


class Chunk:
    def __init__(self, tileSize, assetMenu, index):
        self.layers = []
        self.colliders = []
        self.propsNDecorations = []
        self.tileSize = tileSize
        self.assetMenu = assetMenu
        self.ChunkIndex = index

    def AddLayer(self):
        self.layers.append([])
        for layer in self.layers:
            for height in range(32):
                layer.append([])
                for width in range(32):
                    layer[height].append((-1, -1))

    def DrawChunk(self, screen, selectedLayer):
        for layer in range(len(self.layers)):
            for y in range(len(self.layers[layer])):
                for x in range(len(self.layers[layer][y])):
                    if self.layers[layer][y][x][0] == 0:
                        image = self.assetMenu.tileMenu[self.layers[layer][y][x][1]].image.copy()
                        if layer != selectedLayer:
                            image.set_alpha(100)
                        else:
                            image.set_alpha(255)
                        screen.blit(image, (
                            x * self.tileSize + 400 + (self.ChunkIndex[0] * self.tileSize * 32),
                            y * self.tileSize + (self.tileSize * 32 * self.ChunkIndex[1])))
                    elif self.layers[layer][y][x][0] == 1:
                        image = self.assetMenu.propsMenu[self.layers[layer][y][x][1]].image.copy()
                        if layer != selectedLayer:
                            image.set_alpha(100)
                        else:
                            image.set_alpha(255)
                        screen.blit(image, (
                            x * self.tileSize + 400 + (self.ChunkIndex[0] * self.tileSize * 32),
                            y * self.tileSize + (self.tileSize * 32 * self.ChunkIndex[1])))

    def GetColliders(self):
        return self.colliders

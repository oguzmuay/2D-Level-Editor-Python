import json
import sys
import pygame as pg
import UI.Color as Color
import Objects as Objects
import UI.UI as UI


def Erase(arg):
    assetsMenu.selectedSlot = [-1, -1]


mainClock = pg.time.Clock()
pg.init()
pg.display.set_caption("Level Editor")
windowIcon = pg.image.load("WindowIcon.png")
pg.display.set_icon(windowIcon)
screen = pg.display.set_mode((1280, 720), 0, 32)

hoveredSlot = -1

tileSize = 16

world = []
worldSize = [32, 32]
chunkCount = [(worldSize[0] // 32), (worldSize[1] // 32)]
mapPixels = [worldSize[0] * tileSize, worldSize[1] * tileSize]  # Bunu ekranin kac pixelini gosterdigimi hesaplarken
settingsMenuSwitch = False
# kullanicam.

"""
Collider = [[0,0],[0,0]]
ColliderIndex = 0
"""
font = pg.font.SysFont(None, 20)
Canvas = UI.Canvas(0, 0, 1280, 720)


# -------------- Bottom Navigation Bar Begin -----------------

# -------------------- Layers Begin --------------------------

# Functions Begin --------------------------------------------

def AddLayer(arg):
    for chunkY in range(chunkCount[1]):
        for chunkX in range(chunkCount[0]):
            world[chunkY][chunkX].layers.append([])
            for height in range(32):
                world[chunkY][chunkX].layers[len(world[chunkY][chunkX].layers) - 1].append([])
                for width in range(32):
                    world[chunkY][chunkX].layers[len(world[chunkY][chunkX].layers) - 1][height].append([-1, -1])


def DeleteLayer(arg):
    global selectedLayer
    if selectedLayer + 1 != len(world[0][0].layers):
        reset = False
        if selectedLayer + 1 == len(world[0][0].layers):
            reset = True
        for chunkY in range(chunkCount[1]):
            for chunkX in range(chunkCount[0]):
                del world[chunkY][chunkX].layers[selectedLayer]
        if reset:
            selectedLayer = 0


def SaveMap(arg):
    print("Map Saved")
    saveMap = {}
    for yChunk in range(len(world)):
        for xChunk in range(len(world[yChunk])):
            saveMap[f"{xChunk}-{yChunk}"] = world[yChunk][xChunk].layers
    with open("world.txt", "w") as file:
        save = {"World": saveMap, "WorldSize": worldSize}
        json.dump(save, file)


def LoadMap(arg):
    global world
    global worldSize
    global chunkCount
    try:
        with open("world.txt") as file:
            save = json.load(file)
            saveWorld = save["World"]
            world = []
            worldSize = save["WorldSize"]
            chunkCount = [(worldSize[0] // 32), (worldSize[1] // 32)]
            for y in range(chunkCount[1]):
                world.append([])
                for x in range(chunkCount[0]):
                    world[y].append(Objects.Chunk(tileSize, assetsMenu, [x, y]))
                    world[y][x].layers = saveWorld[f"{x}-{y}"]
            print("Map Loaded")
            # colliders = save["Collider"]
    except:
        print("New Map Created")
        for chunkY in range(chunkCount[1]):
            world.append([])
            for chunkX in range(chunkCount[0]):
                world[chunkY].append(Objects.Chunk(tileSize, assetsMenu, [chunkX, chunkY]))
                world[chunkY][chunkX].AddLayer()


def OpenSettingsMenu(arg):
    global settingsMenuSwitch
    settingsMenuSwitch = not settingsMenuSwitch


def ResizeMap(newSize):
    global world
    global worldSize
    if newSize[0] != worldSize[0] or newSize[1] != worldSize[1]:
        chunkCount[0] = (newSize[0] // 33) + 1
        chunkCount[1] = (newSize[1] // 33) + 1
        newWorld = []
        for chunkY in range(chunkCount[1]):
            newWorld.append([])
            for chunkX in range(chunkCount[0]):
                newWorld[chunkY].append(Objects.Chunk(tileSize, assetsMenu, [chunkX, chunkY]))
                newWorld[chunkY][chunkX].layers.append([])
                for height in range(32):
                    newWorld[chunkY][chunkX].layers[len(newWorld[chunkY][chunkX].layers) - 1].append([])
                    for width in range(32):
                        newWorld[chunkY][chunkX].layers[len(newWorld[chunkY][chunkX].layers) - 1][height].append(
                            [-1, -1])

        if len(world) < len(newWorld):
            chunkXLen = len(world)
        else:
            chunkXLen = len(newWorld)
        if len(world[0]) < len(newWorld[0]):
            chunkYLen = len(world[0])
        else:
            chunkYLen = len(newWorld[0])

        for chunkX in range(chunkYLen):
            for chunkY in range(chunkXLen):
                newWorld[chunkY][chunkX].layers = world[chunkY][chunkX].layers.copy()

        world = newWorld.copy()
        worldSize = newSize.copy()


# Functions End ----------------------------------------------

# Variables Begin --------------------------------------------

selectedLayer = 0

settingsMenuMapSize = worldSize.copy()

# Variables End ----------------------------------------------

# Objects Begin ----------------------------------------------

BottomNavigationBar = UI.Panel(Canvas, 400, 652, 880, 68, screen, Color.LightGrey())

LayerBackground = UI.Panel(Canvas, 566, 664, 400, 44, screen, Color.DarkGrey(), borderRadius=4)

# Objects End ------------------------------------------------

# -----------------------Layers End---------------------------

# --------------------- Buttons Begin ------------------------

layerAddButton = UI.Button(Canvas, 1000, 670, 30, 30, "+", screen, Color.Black(), clickAction=[AddLayer], clickArg=[0]
                           , borderRadius=4)
layerEraseButton = UI.Button(Canvas, 1040, 670, 30, 30, "-", screen, Color.Black(), clickAction=[DeleteLayer],
                             clickArg=[0], borderRadius=4)
layerRightButton = UI.Button(Canvas, 968, 678, 16, 16, ">", screen, Color.Black(), clickAction=[],
                             clickArg=[], borderRadius=4)
layerLeftButton = UI.Button(Canvas, 548, 678, 16, 16, "<", screen, Color.Black(), clickAction=[],
                            clickArg=[], borderRadius=4)
tileEraseButton = UI.Button(Canvas, 1080, 670, 30, 30, "Erase", screen, Color.Black(), clickAction=[Erase],
                            clickArg=[0], borderRadius=4)
colliderAddButton = UI.Button(Canvas, 1120, 670, 30, 30, "CAdd", screen, Color.Black(), clickAction=[Erase],
                              clickArg=[0], borderRadius=4)
colliderEraseButton = UI.Button(Canvas, 1160, 670, 30, 30, "CErase", screen, Color.Black(), clickAction=[Erase],
                                clickArg=[0], borderRadius=4)
SettingsButton = UI.Button(Canvas, 1200, 670, 30, 30, "Settings", screen, Color.Black(), clickAction=[OpenSettingsMenu],
                           clickArg=[0], borderRadius=4)
SaveButton = UI.Button(Canvas, 412, 671, 60, 30, "SAVE", screen, Color.Black(), clickAction=[SaveMap],
                       clickArg=[0], borderRadius=4)

LoadButton = UI.Button(Canvas, 484, 671, 60, 30, "LOAD", screen, Color.Black(), clickAction=[LoadMap],
                       clickArg=[0], borderRadius=4)

# --------------------- Buttons End --------------------------

# -------------- Bottom Navigation Bar End -------------------

# -------------------- Asset Menu Begin ----------------------

assetsMenu = Objects.AssetsMenu(Canvas, 0, 0, 400, 720, screen, Color.LightGrey(), tileSize)

# -------------------- Asset Menu End ------------------------

# --------------------Settings Menu Begin --------------------

SettingPanel = UI.Panel(Canvas, 500, 200, 400, 300, screen, Color.LightGrey(), borderRadius=4)

WorldSizeXText = font.render(f"X Size: {worldSize[0]}", True, Color.Black())

WorldSizeXPlus = UI.Button(SettingPanel, 25, 25, 32, 32, "+", screen, Color.Black(), borderRadius=4)

WorldSizeXMinus = UI.Button(SettingPanel, 57, 25, 32, 32, "-", screen, Color.Black(), borderRadius=4)

WorldSizeYText = font.render(f"Y Size: {worldSize[1]}", True, Color.Black())

WorldSizeYPlus = UI.Button(SettingPanel, 25, 75, 32, 32, "+", screen, Color.Black(), borderRadius=4)

WorldSizeYMinus = UI.Button(SettingPanel, 57, 75, 32, 32, "-", screen, Color.Black(), borderRadius=4)

SettingsSaveButton = UI.Button(SettingPanel, 57, 125, 50, 30, "Save", screen, Color.Black(), borderRadius=4,
                               clickAction=[ResizeMap], clickArg=[])

SettingsBackButton = UI.Button(SettingPanel, 107, 125, 50, 30, "Back", screen, Color.Black(), borderRadius=4,
                               clickAction=[OpenSettingsMenu], clickArg=[0])


# --------------------Settings Menu End ----------------------


def DrawGrids():
    for yChunk in range(len(world)):
        for xChunk in range(len(world[yChunk])):
            for x in range(worldSize[0] + 1):
                pg.draw.line(screen, Color.White(),
                             (tileSize * x + (tileSize * 32 * xChunk) + 400, (tileSize * 32 * yChunk)), (
                                 tileSize * x + (tileSize * 32 * xChunk) + 400,
                                 tileSize * worldSize[1] + (tileSize * 32 * yChunk)))
            for y in range(worldSize[1] + 1):
                pg.draw.line(screen, Color.White(),
                             (400 + (tileSize * 32 * xChunk), tileSize * y + (tileSize * 32 * yChunk)), (
                                 tileSize * worldSize[0] + 400 + (tileSize * 32 * xChunk),
                                 tileSize * y + (tileSize * 32 * yChunk)))


def DrawGridPointer(surface):
    left = tileSize * ((pg.mouse.get_pos()[0] - 400) // tileSize) + 400
    top = tileSize * (pg.mouse.get_pos()[1] // tileSize)
    if ((pg.mouse.get_pos()[0]) - 400) // tileSize < worldSize[0] * chunkCount[0] and (
            pg.mouse.get_pos()[1]) // tileSize < worldSize[1] * chunkCount[1]:
        if assetsMenu.selectedSlot[0] == 0:
            screen.blit(assetsMenu.tileMenu[assetsMenu.selectedSlot[1]].image, (left, top))
        elif assetsMenu.selectedSlot[0] == 1:
            screen.blit(assetsMenu.propsMenu[assetsMenu.selectedSlot[1]].image, (left, top))
        pg.draw.rect(surface, Color.LightGrey(), pg.Rect(left, top, tileSize, tileSize), 2)


def DrawPointerCoordinates(surface):
    textObject = font.render(f"X:{((pg.mouse.get_pos()[0]) - 400) // tileSize}/Y:{pg.mouse.get_pos()[1] // tileSize}",
                             True,
                             (255, 255, 255))
    rect = textObject.get_rect()
    rect.topright = (1280, 0)
    surface.blit(textObject, pg.Rect(rect))


def DrawMenus(mousePos):
    global selectedLayer
    assetsMenu.Update(mousePos)
    if len(world[0][0].layers) > 10:
        drawLayerLen = 10
    else:
        drawLayerLen = len(world[0][0].layers)
    for i in range(drawLayerLen):  # Layer cizme olayi
        left = 573 + 38 * i
        if left < mousePos[0] < left + 32 and 670 < mousePos[1] < 702:
            if pg.mouse.get_pressed()[0] == 1:
                selectedLayer = i
        if i == selectedLayer:
            pg.draw.rect(screen, Color.Red(), pg.Rect(573 + (38 * i), 670, 32, 32), 2, border_radius=4)
        else:
            pg.draw.rect(screen, Color.Grey(), pg.Rect(573 + (38 * i), 670, 32, 32), 2, border_radius=4)
        screen.blit(font.render(f"{i}", True, Color.Black()), (580 + (38 * i), 675))


def UpdateMap(mousePos, selectedSlot):
    global world
    left = (mousePos[0] - 400) // tileSize
    top = mousePos[1] // tileSize
    chunkIndex = (left // 32, top // 32)
    print("Left: ", left, "Top: ", top)
    print(chunkIndex)
    if 0 <= left < worldSize[0] and 0 <= top < worldSize[1]:
        print(len(world))
        print(len(world[0]))
        world[chunkIndex[1]][chunkIndex[0]].layers[selectedLayer][top - 32 * chunkIndex[1]][
            left - 32 * chunkIndex[0]] = selectedSlot.copy()


def DrawMap():
    # Sadece ekranda gorulen chunklar renderlanacak sekilde degistirilmeli.
    maxChunkView = [(880 // tileSize) // 32 + 1, (652 // tileSize) // 32 + 1]
    chunkView = [1, 1]
    if maxChunkView[0] > chunkCount[0] or maxChunkView[1] > chunkCount[1]:
        chunkView[0] = chunkCount[0]
        chunkView[1] = chunkCount[1]
    for yChunk in range(chunkView[1]+1):
        for xChunk in range(chunkView[0]+1):
            world[yChunk][xChunk].DrawChunk(screen, selectedLayer)


def Start():
    """
    This Function Called Once When Programs Is Started.
    """
    LoadMap(0)
    ResizeMap([40, 40])
    assetsMenu.Start()


def DrawColliderPreview():
    """This function draw collider preview."""
    pass


def MouseMotionUpdate():
    # DrawColliderPreview()
    pass


def Update():
    """
    This Function Is Called Every Frame.
    """
    while True:
        screen.fill((0, 0, 0))
        mousePositions = pg.mouse.get_pos()
        DrawMap()
        DrawGrids()
        DrawGridPointer(screen)
        DrawPointerCoordinates(screen)
        BottomNavigationBar.Draw()
        LayerBackground.Draw()
        if settingsMenuSwitch:
            SettingPanel.Draw()
            WorldSizeXPlus.Update(mousePositions)
            WorldSizeXMinus.Update(mousePositions)
            screen.blit(WorldSizeXText, (670, 250))
            WorldSizeYPlus.Update(mousePositions)
            WorldSizeYMinus.Update(mousePositions)
            screen.blit(WorldSizeYText, (670, 300))
            SettingsSaveButton.Update(mousePositions)
            SettingsBackButton.Update(mousePositions)
        layerAddButton.Update(mousePositions)
        layerEraseButton.Update(mousePositions)
        tileEraseButton.Update(mousePositions)
        colliderAddButton.Update(mousePositions)
        colliderEraseButton.Update(mousePositions)
        SettingsButton.Update(mousePositions)
        layerRightButton.Update(mousePositions)
        layerLeftButton.Update(mousePositions)
        SaveButton.Update(mousePositions)
        LoadButton.Update(mousePositions)
        DrawMenus(mousePositions)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                # if event.key == KeyCode.InventoryOpen
            if event.type == pg.MOUSEMOTION:
                assetsMenu.MouseMove(mousePositions)
                MouseMotionUpdate()
                if pg.mouse.get_pressed()[2]:
                    UpdateMap(mousePositions, assetsMenu.selectedSlot)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    """
                    if selectedSlot[0] == -2:
                         if ColliderIndex == 0:
                            Collider[0][0] = mousePosition[0]
                            Collider[0][1] = mousePosition[1]
                         elif ColliderIndex == 1:
                            Collider[1][0] = mousePosition[0]-Collider[0][0]
                            Collider[1][1] = mousePosition[1]-Collider[0][1]
                            colliders[chunkY][chunkX].append(pg.Rect(Collider[0],Collider[1],Color.White()))
                            Collider = [[0,0],[0,0]] 
                    """
                    UpdateMap(mousePositions, assetsMenu.selectedSlot)
                if event.button == 2:
                    pass

        pg.display.update()
        mainClock.tick(30)


def Main():
    Start()
    Update()


Main()

"""
Yapilacaklar:
-Her Button icin kendi fontunu olusturma eklenecek.
-Collider ekleme eklenecek(Collider ekleme shift tusuna basiliyorsa tilesize boyutunda bir kare seklinde eklenebilir ama
 shift tusuna basilmiyorsa ilk tiklamada baslangic ikinci tiklamadada bitis adresini alir.).
-Colliderlar yesil renkte ve ince bir sekilde gosterilecek(Sadece collider ekleme modunda yada bir tus sayesinde ac-kapa
 seklinde olacak) 
-Tile resize eklenecek.
-World resize eklencek.
-Asset menudeki slotlarin imageleri tilesize i kucultunce kuculuyor onu duzeltmem lazim.
LevelEditor Cikti Tasarimi (Json):
{"World":{"0-0":[[[Dunya]]]},
 "PropsNDecorations":{"0-0":[Burada kac tane esya varsa o kadar uzunluk olucak.]},
 "Colliders":{"0-0":[]}
}
"""

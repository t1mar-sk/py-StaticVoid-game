import pygame

# -- Settings --
screen_val = (1000,600) #y #x
FPS = 60
name = "StaticVoid"
whereim = 'menu'

pygame.init()

# -- Configuration --
clock = pygame.time.Clock()

screen = pygame.display.set_mode(screen_val)
pygame.display.set_caption(name)
pygame.display.set_icon(pygame.image.load('icon.png'))

# -- Engine --

class Logo:
    def __init__(self, x, y, image_path, scale=1.0):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        if scale != 1.0:
            w = int(self.image.get_width() * scale)
            h = int(self.image.get_height() * scale)
            self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Text:
    def __init__(self, x, y, text, font_size=24, color=(255, 255, 255), font_path=None):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font_size = font_size

        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.SysFont("Arial", font_size)

    def draw_(self, screen, center_pos=None):

        text_surf = self.font.render(self.text, True, self.color)

        if center_pos:
            text_rect = text_surf.get_rect(center=center_pos)
        else:
            text_rect = text_surf.get_rect(topleft=(self.x, self.y))

        screen.blit(text_surf, text_rect)

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pass

class Box(Shape):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Triangle(Shape):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, color)
        self.size = size

    def draw(self, screen):
        points = [
            (self.x, self.y - self.size),
            (self.x - self.size, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ]
        pygame.draw.polygon(screen, self.color, points)

class Button(Text):
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), font_size=24, font_path=None, transparency=255,
                 text_only_trans=False):
        super().__init__(x, y, text, font_size, (255, 255, 255), font_path)
        self.rect = pygame.Rect(x, y, width, height)
        self.btn_color = color
        self.hover_color = (150, 150, 150)

        self.transparency = transparency
        self.text_only_trans = text_only_trans

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hovered else self.btn_color

        temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shape_color = (*current_color, self.transparency)
        pygame.draw.rect(temp_surface, shape_color, (0, 0, self.rect.width, self.rect.height))
        pygame.draw.rect(temp_surface, (255, 255, 255, self.transparency), (0, 0, self.rect.width, self.rect.height), 2)

        screen.blit(temp_surface, (self.rect.x, self.rect.y))

        if self.text_only_trans:
            super().draw_(screen, center_pos=self.rect.center)
        else:
            original_color = self.color
            self.color = (*original_color[:3], self.transparency)
            super().draw_(screen, center_pos=self.rect.center)
            self.color = original_color

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# -- Menu Configurate --
glogo = Logo(50, 50 , 'icon_ingame.png', 0.1)
gname = Text(150, 50, 'StaticVoid', 36, (255,255,255), 'basicfont.ttf')
gpanel = Box(0, 550, 1000, 50, (255, 69, 69))

# -- Buttons --
playb = Button(50, 180, 28.5 * 4, 50, "PLAY", (114, 31, 166), 36, 'basicfont.ttf', 0)
inventoryb = Button(50, 240, 28.5 * 9 - 1, 50, "INVENTORY", (114, 31, 166), 36, 'basicfont.ttf', 0)
exitb = Button(50, 300, 28.5 * 4 - 17, 50, "EXIT", (114, 31, 166), 36, 'basicfont.ttf', 0)

# -- Game --
class Player(Box):
    def __init__(self, accountName, accountID):
        super().__init__(screen_val[0]//2, screen_val[1]//2, 20,20,(117, 13, 0) )
        self.hp = 0 # max 100
        self.hunger = 0 # max 250
        self.water = 0 #max 250
        self.bleeding = 0 # unlimited
        self.vel = 5

        #Camera x,y
        self.cx = 0
        self.cy = 0

        #Account details
        self.name = accountName
        self.ID = accountID
        self.alive = True

    def get_info(self):
        return self.name, self.ID

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.cx -= self.vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.cx += self.vel
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.cy -= self.vel
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.cy += self.vel

    def init(self):
        super().draw(screen)
        self.handle_input()
        print(f"cx [{self.cx}] \n cy [{self.cy}]")

player = Player("t1mar", "01")

class Map()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 20, 20))

    match whereim:
        case 'menu':
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if playb.check_click(mouse_pos):
                        whereim = 'ingame'
                    if inventoryb.check_click(mouse_pos):
                        whereim = 'inventory'
                    if exitb.check_click(mouse_pos):
                        running = False

            # -- Drawing --
            glogo.draw(screen)
            gname.draw_(screen)
            gpanel.draw(screen)

            playb.draw(screen)
            inventoryb.draw(screen)
            exitb.draw(screen)

        case 'ingame':
            player.init()
        case 'inventory':
            class Inventory(Box, Logo):
                # itemImgConf are not used in newer versions, they will load from the server. itemImgConf = ('image_path.png', scale)
                # skins (list) also are not used in newer version, they will load form the server.
                def __init__(self, screen, itemName, itemID, itemImgConf, x, y, w, h, color=(20, 20, 20)):
                    Box.__init__(self, x, y, w +10, h +10 , color)
                    Logo.__init__(self, x + 10, y + 10, itemImgConf[0], itemImgConf[1])

                    self.itemName = itemName
                    self.itemID = itemID
                    self.screen = screen

                def draw_(self):
                    Box.draw(self, self.screen)
                    Logo.draw(self, self.screen)

            exitB = Button(5, 5, 30,30, "<", (0,0,0), 32, 'basicfont.ttf', 255)

            skins = [
                Inventory(screen, "AK-47 Test load skin", 1, ('skins/AK47_N1.png', 0.17), 0, 50, 50, 50, (20,20,255))
            ]

            for skin in skins:
                skin.draw_()
            exitB.draw_(screen)

            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if exitB.check_click(mouse_pos):
                        whereim = 'menu'


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
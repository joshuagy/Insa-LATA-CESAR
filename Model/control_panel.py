import pygame
from Model.constants import *


# === CLASSES === 
class ButtonCtrlPnl():

    def __init__(self, controls, function, text: str = None, x : int =0, y : int =0, image_normal=None, image_hovered=None, image_clicked=None, image_locked=None, state: str = 'default'):
        """Create a button. Set the images to their path or to None if you don't want to have a hovered and clicked version of your button."""
        # list_of_buttons.append(self)
        self.controls = controls
        self.func = function
        self.state = state
        self.text = text

        self.soundMixer = self.controls.soundMixer

        self.textsurface = pygame.font.SysFont('default_font', 20).render(self.text, False, BLACK, WHITE)

        self.image_normal =  pygame.image.load(image_normal)
        self.dim = (self.image_normal.get_rect().size[0]*SCL,self.image_normal.get_rect().size[1]*SCL) #dim[0] is the width of the sprite, dim[1] the height
        self.image_normal = pygame.transform.scale(self.image_normal,self.dim)
        self.hide = False

        
        if(image_hovered!=None):
            self.image_hovered_exists = True
            self.image_hovered = pygame.image.load(image_hovered)
            self.image_hovered = pygame.transform.scale(self.image_hovered,self.dim)
        else:
            self.image_hovered_exists = False
            
        if(image_clicked!=None):
            self.image_clicked_exists = True
            self.image_clicked = pygame.image.load(image_clicked)
            self.image_clicked = pygame.transform.scale(self.image_clicked,self.dim)
        else:
            self.image_clicked_exists = False

        if(image_locked!=None):
            self.unlocked=False
            self.image_locked_exists = True
            self.image_locked = pygame.image.load(image_locked)
            self.image_locked = pygame.transform.scale(self.image_locked,self.dim)
        else:
            self.image_locked_exists = False
            self.unlocked=True
               
        self.image = self.image_normal
        self.rect = self.image.get_rect()

        # you can't use it before `blit` 
        self.rect.topleft = (x, y)

        self.hovered = False
        self.clicked = False

    def change_image(self, path):
        """ Change the actual sprite of the button"""
        self.image_normal =  pygame.image.load(path)
        self.dim = (self.image_normal.get_rect().size[0]*SCL,self.image_normal.get_rect().size[1]*SCL) #dim[0] is the width of the sprite, dim[1] the height
        self.image_normal = pygame.transform.scale(self.image_normal,self.dim)
        self.hide = False

        self.image_hovered_exists = False
        self.image_clicked_exists = False
        self.unlocked=True
               
        self.image = self.image_normal
        self.update()

    def unlock(self):
        """Unlock the functionality of the button"""
        self.unlocked=True

    def call_func(self, *args, **kwargs):
        """Action realized by the button"""
        return self.func(*args, **kwargs)

    def change_pos(self,x,y):    
        """Change the position of the button"""
        self.rect.topleft = (x, y)

    def update(self):
        """Update the button's image"""
        if self.hide is False:
            if self.unlocked==True:
                if self.image_clicked_exists and self.clicked:
                    self.image = self.image_clicked
                elif self.image_hovered_exists and self.hovered:
                    self.image = self.image_hovered
                else:
                    self.image = self.image_normal
            else:
                self.image = self.image_locked

    def show_tip(self, display):
        """Show the tip of the button when hovered"""
        if self.hovered and self.hide is False:
            mouse_pos = pygame.mouse.get_pos()
            display.blit(self.textsurface, (mouse_pos[0]-100, mouse_pos[1]+20)) #affiche le message à gauchenet en dessous du curseur
                
    def draw(self, surface):
        """Draw the button on the surface"""
        if self.hide is False:
            surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)                                                                      
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #We consider that the button is in the clicked state until we click again
            if self.hovered:
                if self.clicked:
                    self.clicked = False
                    self.controls.setCurrentState('default')
                    if self.text == "Select a city overlay report":
                       self.call_func()

                else:
                    for button in self.controls.listOfButtons:
                        button.clicked = False
                    self.clicked = True
                    self.soundMixer.playEffect('clickEffect')
                    self.controls.setCurrentState(self.state)
                    if self.unlocked and callable(self.call_func):
                       self.call_func()


class Sprite:   
    def __init__(self, source):
        self.source=source
        self.img = pygame.image.load(source)
        self.dim = (self.img.get_rect().size[0]*SCL,self.img.get_rect().size[1]*SCL) #dim[0] is the width of the sprite, dim[1] is the height"""
        self.img_scaled=pygame.transform.scale(self.img,self.dim)

class TextRender:
    def __init__(self, text, size, colour = (255,255,255), bg = None) :
        self.colour = colour
        self.size=size
        self.police = pygame.font.SysFont("monospace" ,15)
        self.text_image = self.police.render ( text, 1 , self.colour, bg)
        self.img_scaled = pygame.transform.scale(self.text_image,size)

class ButtonWithImmediatEffect(ButtonCtrlPnl):
    def __init__(self, controls, function, state: str,  text: str = None, x : int =0, y : int =0, image_normal=None, image_hovered=None, image_clicked=None, image_locked=None):
        self.soundMixer = controls.soundMixer
        super().__init__(controls, function, state, text, x, y, image_normal, image_hovered, image_clicked, image_locked)

    def show_tip(self, *arg):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)                                                                      
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.clicked = True
                self.soundMixer.playEffect('clickEffect')
                if self.unlocked and callable(self.call_func):
                        self.call_func()

        elif event.type == pygame.MOUSEBUTTONUP:
            #We consider that the button is in the clicked state until we click again
            if self.hovered:
                self.clicked = not self.clicked
                
# === VARIABLES === 
state_control_panel = "full" # "full" or "reduced"

# === FUNCTIONS === 

def display_full_ctrl_panel():
    """Display the full control panel"""
    #global state_control_panel
    #state_control_panel = "full"
    print("i'm in display_full_ctrl_panel")

def display_reduced_ctrl_panel():
    """Display the reduced control panel"""
    print("i'm in display_reduced_ctrl_panel")

def build_housing():
    """Build housing"""
    print("i'm in build_housing")

def clear_land():
    """Clear land aka la pelle"""
    print("i'm in clear_land")

def build_roads():
    """Build roads"""
    print("i'm in build_roads")

def build_prefecture():
    """Build Prefecture"""
    print("i'm in build_prefecture")

def build_water_related_structures():
    """Build water related structures"""
    print("i'm in build_water_related_structures")

def build_engineer_post():
    print("i'm in build_engineer_post")

def not_implemented_func():
    """Not implemented function"""
    print("i'm in not_implemented_func")

def build_colosseum_func():
    """Not implemented function"""
    print("i'm in not_implemented_func")


        

#Create buttons
#fire_overlay = ButtonCtrlPnl(not_implemented_func,"Show the risk of the structure to catch fire", 0, 0,"image/UI/menu/menu_fire_button.png","image/UI/menu/menu_fire_button_clicked.png","image/UI/menu/menu_fire_button_clicked.png")
#damage_overlay = ButtonCtrlPnl(not_implemented_func,"Show the risk of the structure to collapse", 0, 0,"image/UI/menu/menu_damage_button.png","image/UI/menu/menu_damage_button_clicked.png","image/UI/menu/menu_damage_button_clicked.png")
#entertainment_overlay = ButtonCtrlPnl(not_implemented_func,"Show the level of entertainment of each case", 0, 0,"image/UI/menu/menu_entertainment_button.png","image/UI/menu/menu_entertainment_button_clicked.png","image/UI/menu/menu_entertainment_button_clicked.png")
#water_overlay = ButtonCtrlPnl(not_implemented_func,"Show the water level of each case", 0, 0,"image/UI/menu/menu_water_button.png","image/UI/menu/menu_water_button_clicked.png","image/UI/menu/menu_water_button_clicked.png")
#fire_overlay.hide = True
#damage_overlay.hide = True
#entertainment_overlay.hide = True
#water_overlay.hide = True
# overlays_button = ButtonCtrlPnl(not_implemented_func,"Select a city overlay report", 0, 0,"image/C3/paneling_00234.png","image/C3/paneling_00235.png","image/C3/paneling_00236.png")
# hide_control_panel_button = ButtonCtrlPnl(display_reduced_ctrl_panel,"Hide the Control Panel to see a wider playing area", 0, 0,"image/C3/paneling_00097.png","image/C3/paneling_00098.png","image/C3/paneling_00099.png")
# display_control_panel_button = ButtonCtrlPnl(display_full_ctrl_panel,"Display the Control Panel", 0, 0,"image/C3/paneling_00101.png","image/C3/paneling_00102.png","image/C3/paneling_00103.png") #1238, 28?

# advisors_button= ButtonCtrlPnl(not_implemented_func,"Visit your advisors", 0, 0,"image/C3/paneling_00079.png","image/C3/paneling_00080.png","image/C3/paneling_00081.png")
# empire_map_button = ButtonCtrlPnl(not_implemented_func,"Go to the map of the Empire", 0, 0,"image/C3/paneling_00082.png","image/C3/paneling_00083.png","image/C3/paneling_00084.png")
# assignement_button = ButtonCtrlPnl(not_implemented_func,"Review your assignement", 0, 0,"image/C3/paneling_00085.png","image/C3/paneling_00086.png","image/C3/paneling_00087.png")
# compass_button = ButtonCtrlPnl(not_implemented_func,"Re_orient your view to Due North", 0, 0,"image/C3/paneling_00088.png","image/C3/paneling_00089.png","image/C3/paneling_00090.png")
# arrow_rotate_counterclockwise = ButtonCtrlPnl(not_implemented_func,"Rotate the map counterclockwise", 0, 0,"image/C3/paneling_00091.png","image/C3/paneling_00092.png","image/C3/paneling_00093.png")
# arrow_rotate_clockwise = ButtonCtrlPnl(not_implemented_func,"Rotate the map clockwise", 0, 0,"image/C3/paneling_00094.png","image/C3/paneling_00095.png","image/C3/paneling_00096.png")

#build_housing_button = ButtonCtrlPnl(build_housing,"Build housing", 0, 0,"image/C3/paneling_00123.png","image/C3/paneling_00124.png","image/C3/paneling_00125.png")
#clear_land_button = ButtonCtrlPnl(clear_land,"Clear land", 0, 0, "image/C3/paneling_00131.png", "image/C3/paneling_00132.png","image/C3/paneling_00133.png")
# build_roads_button = ButtonCtrlPnl(build_roads,"Build roads", 0, 0,"image/C3/paneling_00135.png","image/C3/paneling_00136.png","image/C3/paneling_00137.png")
# water_related_structures = ButtonCtrlPnl(build_water_related_structures, "Water related structure", 0, 0,"image/C3/paneling_00127.png","image/C3/paneling_00128.png","image/C3/paneling_00129.png")
# health_related_structures= ButtonCtrlPnl(not_implemented_func, "Health related structures", 0, 0, "image/C3/paneling_00163.png", "image/C3/paneling_00164.png", "image/C3/paneling_00165.png","image/C3/paneling_00166.png")
# religious_structures = ButtonCtrlPnl(not_implemented_func,"Religious Structures", 0, 0,"image/C3/paneling_00151.png","image/C3/paneling_00152.png","image/C3/paneling_00153.png","image/C3/paneling_00154.png")
# education_structures = ButtonCtrlPnl(not_implemented_func,"Education Structures", 0, 0,"image/C3/paneling_00147.png","image/C3/paneling_00148.png","image/C3/paneling_00149.png","image/C3/paneling_00150.png")
# entertainment_structures= ButtonCtrlPnl(not_implemented_func,"Entertainment_structures", 0, 0,"image/C3/paneling_00143.png","image/C3/paneling_00144.png","image/C3/paneling_00145.png","image/C3/paneling_00146.png")      
# administration_or_government_structures = ButtonCtrlPnl(not_implemented_func,"Administration or Government Structures", 0, 0,"image/C3/paneling_00139.png","image/C3/paneling_00140.png","image/C3/paneling_00141.png")
# engineering_structures = ButtonCtrlPnl(build_engineer_post, "Engineering function", 0, 0,"image/C3/paneling_00167.png","image/C3/paneling_00168.png","image/C3/paneling_00169.png")
# security_structures = ButtonCtrlPnl(build_prefecture,"Security Structures", 0, 0,"image/C3/paneling_00159.png","image/C3/paneling_00160.png","image/C3/paneling_00161.png")
# industrial_structures = ButtonCtrlPnl(not_implemented_func,"Industrial Structures", 0, 0,"image/C3/paneling_00155.png","image/C3/paneling_00156.png","image/C3/paneling_00157.png","image/C3/paneling_00158.png")
# undo_button = ButtonCtrlPnl(not_implemented_func,"Undo", 0, 0,"image/C3/paneling_00171.png","image/C3/paneling_00172.png","image/C3/paneling_00173.png","image/C3/paneling_00174.png")
# message_view_button = ButtonCtrlPnl(not_implemented_func,"Message View", 0, 0,"image/C3/paneling_00115.png","image/C3/paneling_00116.png","image/C3/paneling_00117.png","image/C3/paneling_00118.png")
# see_recent_troubles_button = ButtonCtrlPnl(not_implemented_func,"See recent troubles", 0, 0,"image/C3/paneling_00119.png","image/C3/paneling_00120.png","image/C3/paneling_00121.png","image/C3/paneling_00122.png")



#Create sprites
big_gap_menu=Sprite("image/C3/paneling_00017.png")
small_gap_menu=Sprite("image/C3/paneling_00016.png")

deco_bas_small_menu = Sprite("image/C3/paneling_00021.png")
deco_bas_full_menu = Sprite("image/C3/map_panels_00003.png")
deco_milieu_menu_default = Sprite("image/C3/panelwindows_00013.png")   #Image du milieu devra changer en fonction du bouton cliqué, à voir comment gérer ça plus tard


#panels du menu top bar

pnl_1=Sprite("image/C3/paneling_00001.png")
pnl_2=Sprite("image/C3/paneling_00002.png")
pnl_3=Sprite("image/C3/paneling_00003.png")
pnl_4=Sprite("image/C3/paneling_00004.png")
pnl_5=Sprite("image/C3/paneling_00005.png")
pnl_6=Sprite("image/C3/paneling_00006.png")
pnl_7=Sprite("image/C3/paneling_00007.png")
pnl_8=Sprite("image/C3/paneling_00008.png")

bloc_top_menu=Sprite("image/C3/paneling_00015.png")

#panels du control panel en bas à droite
pnl_479=Sprite("image/C3/paneling_00479.png")
pnl_480=Sprite("image/C3/paneling_00480.png")
pnl_481=Sprite("image/C3/paneling_00481.png")
pnl_482=Sprite("image/C3/paneling_00482.png")
pnl_483=Sprite("image/C3/paneling_00483.png")
pnl_484=Sprite("image/C3/paneling_00484.png")
pnl_485=Sprite("image/C3/paneling_00485.png")
pnl_486=Sprite("image/C3/paneling_00486.png")
pnl_487=Sprite("image/C3/paneling_00487.png")
pnl_488=Sprite("image/C3/paneling_00488.png")
pnl_489=Sprite("image/C3/paneling_00489.png")
pnl_490=Sprite("image/C3/paneling_00490.png")
pnl_491=Sprite("image/C3/paneling_00491.png")
pnl_492=Sprite("image/C3/paneling_00492.png")
pnl_493=Sprite("image/C3/paneling_00493.png")
pnl_494=Sprite("image/C3/paneling_00494.png")
pnl_495=Sprite("image/C3/paneling_00495.png")
pnl_496=Sprite("image/C3/paneling_00496.png")
pnl_497=Sprite("image/C3/paneling_00497.png")
pnl_498=Sprite("image/C3/paneling_00498.png")
pnl_499=Sprite("image/C3/paneling_00499.png")
pnl_500=Sprite("image/C3/paneling_00500.png")
pnl_501=Sprite("image/C3/paneling_00501.png")
pnl_502=Sprite("image/C3/paneling_00502.png")
pnl_503=Sprite("image/C3/paneling_00503.png")
pnl_504=Sprite("image/C3/paneling_00504.png")
pnl_505=Sprite("image/C3/paneling_00505.png")
pnl_506=Sprite("image/C3/paneling_00506.png")
pnl_507=Sprite("image/C3/paneling_00507.png")
pnl_508=Sprite("image/C3/paneling_00508.png")
pnl_509=Sprite("image/C3/paneling_00509.png")
pnl_510=Sprite("image/C3/paneling_00510.png")
pnl_511=Sprite("image/C3/paneling_00511.png")
pnl_512=Sprite("image/C3/paneling_00512.png")
pnl_513=Sprite("image/C3/paneling_00513.png")
pnl_514=Sprite("image/C3/paneling_00514.png")
pnl_515=Sprite("image/C3/paneling_00515.png")
pnl_516=Sprite("image/C3/paneling_00516.png")
pnl_517=Sprite("image/C3/paneling_00517.png")
pnl_518=Sprite("image/C3/paneling_00518.png")
pnl_519=Sprite("image/C3/paneling_00519.png")
pnl_520=Sprite("image/C3/paneling_00520.png")
pnl_521=Sprite("image/C3/paneling_00521.png")
pnl_522=Sprite("image/C3/paneling_00522.png")
pnl_523=Sprite("image/C3/paneling_00523.png")
pnl_524=Sprite("image/C3/paneling_00524.png")
pnl_525=Sprite("image/C3/paneling_00525.png")
pnl_526=Sprite("image/C3/paneling_00526.png")
pnl_527=Sprite("image/C3/paneling_00527.png")

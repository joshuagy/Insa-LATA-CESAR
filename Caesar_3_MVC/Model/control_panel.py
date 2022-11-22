import pygame

SCL = 1/2 # Scale to redimension the sprites
class Sprite:
     
    def __init__(self, source):
        self.source=source
        self.img = pygame.image.load(source)
        self.dim = (self.img.get_rect().size[0]*SCL,self.img.get_rect().size[1]*SCL) #dim[0] is the width of the sprite, dim[1] is the height"""
        self.img_scaled=pygame.transform.scale(self.img,self.dim)

     
state_control_panel = "full" # "full" or "reduced"

big_gap_menu=Sprite("image/C3/paneling_00017.png")
small_gap_menu=Sprite("image/C3/paneling_00016.png")
overlays_button =Sprite("image/C3/paneling_00234.png")
advisors=Sprite("image/C3/paneling_00079.png")

empire_map = Sprite("image/C3/paneling_00082.png")
assignement_scroll = Sprite("image/C3/paneling_00085.png")
compass = Sprite("image/C3/paneling_00088.png")
arrow_rotate_counterclockwise = Sprite("image/C3/paneling_00091.png")
arrow_rotate_clockwise = Sprite("image/C3/paneling_00094.png")
build_housing = Sprite("image/C3/paneling_00123.png")
clear_land = Sprite("image/C3/paneling_00131.png")
build_roads = Sprite("image/C3/paneling_00135.png")
water_related_structures = Sprite("image/C3/paneling_00127.png")
health_related_structures = Sprite("image/C3/paneling_00163.png")
religious_structures = Sprite("image/C3/paneling_00151.png")            
education_structures = Sprite("image/C3/paneling_00147.png")
entertainment_structures = Sprite("image/C3/paneling_00143.png" )
administration_or_government_structures = Sprite("image/C3/paneling_00139.png")
engineering_structures = Sprite("image/C3/paneling_00167.png")
security_structures = Sprite("image/C3/paneling_00159.png")
industrial_structures = Sprite("image/C3/paneling_00155.png")
undo_button= Sprite("image/C3/paneling_00171.png")
message_view_button = Sprite("image/C3/paneling_00115.png")
see_recent_troubles_button = Sprite("image/C3/paneling_00119.png")
deco_bas_small_menu = Sprite("image/C3/paneling_00021.png")
deco_bas_full_menu = Sprite("image/C3/paneling_00018.png")
deco_milieu_menu_default = Sprite("image/C3/panelwindows_00013.png")   #Image du milieu devra changer en fonction du bouton cliqué, à voir comment gérer ça plus tard

display_control_panel_button = Sprite("image/C3/paneling_00101.png")
hide_control_panel_button=Sprite("image/C3/paneling_00097.png")

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




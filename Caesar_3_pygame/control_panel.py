import pygame


class sprite:

    big_gap_menu = "C3/paneling_00017.png"
    small_gap_menu = "C3/paneling_00016.png"
    overlays_button = "C3/paneling_00234.png"
    advisors = "C3/paneling_00079.png"
    empire_map = "C3/paneling_00082.png"
    assignement_scroll = "C3/paneling_00085.png"
    compass = "C3/paneling_00088.png"
    arrow_rotate_counterclockwise = "C3/paneling_00091.png"
    arrow_rotate_clockwise = "C3/paneling_00094.png"
    build_housing = "C3/paneling_00123.png"
    clear_land = "C3/paneling_00131.png"
    build_roads = "C3/paneling_00135.png" 
    water_related_structures = "C3/paneling_00127.png"
    health_related_structures = "C3/paneling_00163.png" 
    religious_structures = "C3/paneling_00151.png"            
    education_structures = "C3/paneling_00147.png"
    entertainment_structures = "C3/paneling_00143.png" 
    administration_or_government_structures = "C3/paneling_00139.png"
    engineering_structures = "C3/paneling_00167.png"
    security_structures = "C3/paneling_00159.png"
    industrial_structures = "C3/paneling_00155.png"
    undo_button= "C3/paneling_00171.png"
    message_view_button = "C3/paneling_00115.png"
    see_recent_troubles_button = "C3/paneling_00119.png" 
    deco_bas_small_menu = "C3/paneling_00021.png"
    deco_bas_full_menu = "C3/paneling_00018.png"
    deco_milieu_menu_default = "C3/panelwindows_00013.png"     #Image du milieu devra changer en fonction du bouton cliqué, à voir comment gérer ça plus tard

    display_control_panel_button = "C3/paneling_00101.png"
    hide_control_panel_button="C3/paneling_00097.png"

    state_control_panel = "full" # "full" or "reduced"





    def _get_size_of_(self,width_or_height="both"):
        """Return the dimensions of an image, by default both width and height. Specify "width" or "height" to return only one of the two."""
        if width_or_height=="both":
            return pygame.image.load(self).get_rect().size
        elif width_or_height == "width":
            return pygame.image.load(self).get_rect().size[0]
        elif width_or_height == "height":
            return pygame.image.load(self).get_rect().size[1]

   
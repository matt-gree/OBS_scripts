import obspython as S

canvas_width = 1280
canvas_height = 720
HUD_width = int(canvas_width*.25)
HUD_height = int(canvas_height*.25)

color_source1 = "Scoreboard Base"

color_default = 0xFF4fee4f

def script_defaults (settings):
    S.obs_data_set_int(settings, "scoreboard_base_color", color_default)

class HUD:
    def __init__(self):
        #set the intitial position of to be 0,0
        pos = S.vec2()
        self.location = pos
        self.location.x = 0
        self.location.y = 0

    def create_text_source(self):

        current_scene = S.obs_frontend_get_current_scene()
        scene = S.obs_scene_from_source(current_scene)
        settings = S.obs_data_create()

        props = S.obs_properties_create()


        S.obs_data_set_int(settings, "width", HUD_width)
        S.obs_data_set_int(settings, "height", HUD_height)
        S.obs_data_set_int(settings, "color", color_default)
        source = S.obs_source_create("color_source", color_source1, settings, None)
        S.obs_scene_add(scene, source)

        group = S.obs_scene_add_group2(scene, "HUD", signal = True)
        color1_source_item = S.obs_scene_find_source(scene, color_source1)
        print(color1_source_item)
        S.obs_sceneitem_group_add_item(group, color1_source_item)

    def update_location(self):
        # For some reason, the source always thinks it is at 0,0 no matter its location on the canvas.
        # To move the source around on the canvas, I have stored the postion seperately.
        # This allows the slider values to be subtracted from the true current location.
        # The then true location is updated accordingly
        # This section cannot be added to the script update to update in real time,
        # because the self.location gets messed up and the source does not end up in the
        # correct location

        current_scene = S.obs_frontend_get_current_scene()
        scene = S.obs_scene_from_source(current_scene)
        color1_source_item2 = S.obs_scene_find_source_recursive(scene, color_source1)
        position = S.vec2()

        S.vec2_set(position, int(((canvas_width - HUD_width) * (hpositionslider / 1000))-self.location.x),
                   int(((canvas_height - HUD_height) * (vpositionslider / 1000)))-self.location.y)
        S.obs_sceneitem_set_pos(color1_source_item2, position)
        self.location.x = int((canvas_width - HUD_width) * (hpositionslider / 1000))
        self.location.y = int((canvas_height - HUD_height) * (vpositionslider / 1000))

graphics = HUD()


def script_update(settings):
    global hpositionslider
    global vpositionslider
    hpositionslider = S.obs_data_get_int(settings, "_hslider")
    vpositionslider = S.obs_data_get_int(settings, "_vslider")

    source = S.obs_get_source_by_name(color_source1)
    scoreboard_base_color = S.obs_data_get_int(settings, "scoreboard_base_color")
    S.obs_data_set_int(settings, "color", scoreboard_base_color)
    S.obs_source_update(source, settings)


def refresh_pressed(props, prop):
    graphics.update_location()

def add_pressed(props, prop):
    graphics.create_text_source()


def script_description():
    return "Better Mario Baseball Game HUD \nBy MattGree and PeacockSlayer (and Rio Dev team)"


def script_properties():  # ui
    props = S.obs_properties_create()

    p = S.obs_properties_add_list(props, "selection", "Choose", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(p, "Location", "location")
    S.obs_property_list_add_string(p, "Stats", "stats")

    S.obs_properties_add_button(props, "button", "Add color source", add_pressed)
    S.obs_properties_add_int_slider(props, "_hslider", "Horizontal Location", 0, 1000, 1)
    S.obs_properties_add_int_slider(props, "_vslider", "Vertical Location", 0, 1000, 1)
    bool = S.obs_properties_add_bool(props, "_bool", "_bool:")
    S.obs_properties_add_button(props, "button2", "Refresh", refresh_pressed)
    S.obs_properties_add_color(props, "scoreboard_base_color", "")

    S.obs_property_set_visible(bool, False)
    S.obs_property_set_modified_callback(p, callback)

    return props


def callback(props, prop, settings):
    # Return true is needed for the callback function to complete properly
    selection = S.obs_data_get_string(settings, "selection")
    print(selection, "Selection update")
    boolprop = S.obs_properties_get(props, "_bool")

    if str(selection) == "location":
        S.obs_property_set_visible(boolprop, True)
        return True
    else:
        S.obs_property_set_visible(boolprop, False)
        return True

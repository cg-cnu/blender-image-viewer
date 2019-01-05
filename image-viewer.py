bl_info = {
    "name": "Image Viewer",
    "description": "A simple image viewer",
    "author": "Sreenivas Alapati",
    "version": (0, 0, 1),
    "blender": (2, 7, 8),
    "location": "UV/Image Editor > Toolshelf > Image Viewer",
    "category": "Scene",
}

import bpy
import os
import subprocess

# from bpy.types import Panel, EnumProperty, WindowManager
# from bpy.props import StringProperty

# custom icons
import bpy.utils.previews
# increase the button size ? 

# icons_dict = bpy.utils.previews.new()
# # this will work for addons 
# icons_dir = os.path.join(os.path.dirname(__file__), "icons")
# # but it won't give you usefull path when you opened a file in text editor and hit run.
# # this will work in that case:
# # script_path = bpy.context.space_data.text.filepath
# # icons_dir = os.path.join(os.path.dirname(script_path), "icons")
# icons_dict.load("right-arrow", os.path.join(icons_dir, "right-arrow.png"), 'IMAGE')
# print (icons_dict)

# icon_value=icons_dict["right-arrow"].icon_id
# print (icons_dict["right-arrow"])
# print (icons_dict["right-arrow"].icon_id)
# IDEA: logged by admin @ 2017-10-28 14:53:07
# show the list of images on the right ?
# change the tool name to image viewer

# recursive ? 
# filter images

# map keys to move between prev and next images
# show images name in the opengl ?
# show  zoom percentage ?  

# each image won't load into blender.
# do a load option to actually load and keep it ?

# remember the fit and zoom on each image ? 
 
# metadata: a new panel to show meta of the current image
# class Image_Manager_Metadata(bpy.types.Panel):
# 	"""
# 	show image metadata
# 	"""

IMG_TRAY = []
IMG_TRAY_POSITION = 0

class Image_Info_Panel(bpy.types.Panel):
    """ Show Image Info
    """
    bl_label = " "
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "ImageViewer"

    def draw_header(self, _):
        layout = self.layout
        layout.label(text= "current image" or "Image Info Panel" )

    def draw(self, context):
        layout = self.layout
        column = layout.column(True)

        # open
        row = column.row(True)
        # rename ? 
        row.label('name')
        row.label('size')
        row.label()

# preview_icons = bpy.utils.previews.new()

# def icon_register(fileName):
#     name = fileName.split('.')[0]   # Don't include file extension
#     icons_dir = os.path.join(os.path.dirname(__file__), "icons")
#     preview_icons.load(name, os.path.join(icons_dir, fileName), 'IMAGE')

# icon_register('right-arrow.png')

def get_icon(name):
    return custom_icons[name].icon_id

# def generate_previews():
#     # We are accessing all of the information that we generated in the register function below
#     preview_collection = preview_collections["thumbnail_previews"]
#     image_location = preview_collection.images_location
#     VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg')
    
#     enum_items = []
    
#     # Generate the thumbnails
#     for i, image in enumerate(os.listdir(image_location)):
#         if image.endswith(VALID_EXTENSIONS):
#             filepath = os.path.join(image_location, image)
#             thumb = preview_collection.load(filepath, filepath, 'IMAGE')
#             enum_items.append((image, image, "", thumb.icon_id, i))
            
#     return enum_items

# class op_popup(bpy.types.Operator):
#     # bl_idname = "ui.imageviewer_popup"
#     bl_label = "Message"

#     message = StringProperty()
 
#     def execute(self, context):
#         self.report({'INFO'}, self.message)
#         print(self.message)
#         return {'FINISHED'}
 
#     def invoke(self, context, event):
#         wm = context.window_manager
#         return wm.invoke_popup(self, width=200, height=200)
 
#     def draw(self, context):
#         self.layout.label(self.message)



# def register():
#     from bpy.types import Scene
#     from bpy.props import StringProperty, EnumProperty
    
#     print("_______REgister previews")

#     # Operators
#     # bpy.utils.register_class(op_popup)

#     # global preview_icons
#     # preview_icons = bpy.utils.previews.new()

#     # Create a new preview collection (only upon register)
#     preview_collection = bpy.utils.previews.new()
#     preview_collection.images_location = os.path.join(os.path.dirname(__file__), "./icons")
#     preview_collections["thumbnail_previews"] = preview_collection
    
#     # This is an EnumProperty to hold all of the images
#     # You really can save it anywhere in bpy.types.*  Just make sure the location makes sense
#     bpy.types.Scene.IM_image_previews = EnumProperty(
#         items=generate_previews(),
#     )
    
# def unregister():

#     print("_______UNregister previews")

#     from bpy.types import WindowManager
#     for preview_collection in preview_collections.values():
#         bpy.utils.previews.remove(preview_collection)
#     preview_collections.clear()
    

#     # Unregister icons
#     # global preview_icons
#     bpy.utils.previews.remove(preview_icons)


#     del bpy.types.Scene.IM_image_previews


class Image_Viewer_Panel(bpy.types.Panel):
    """ image viewer panel
    """
    bl_label = "Image Viewer Panel"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "ImageViewer"

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)

        # open
        row = column.row(align=True)
        row.prop(context.scene,
                 'IM_folder_path')

        # rename
        row = column.row(align=True)
        op = row.label("{}".format("current Image name"))

        # move
        box = layout.box()

        row = box.row(True)
        op = row.operator("scene.im_change_image",
                          text="Previous Image",
                          icon_value=get_icon("direction_left")).direction = 'left'
                
        op = row.operator("scene.im_change_image",
                          text="Next Image",
                          icon_value=get_icon("direction_right")).direction = 'right'

        # rotate
        row = box.row(True)
        op = row.operator("scene.im_rotate_image",
                          text="Rotate Left",
                          icon_value=get_icon('rotate_left')).rotate_value = "rotate left"

        op = row.operator("scene.im_rotate_image",
                          text="Rotate right",
                          icon_value=get_icon('rotate_right')).rotate_value = "rotate right"

        # flip
        row = box.row(True)
        op = row.operator("scene.im_flip_image",
                          text='Flip Horizontal',
                          icon_value=get_icon('flip_horizontal')).flip_value = "flip horizontal"

        op = row.operator("scene.im_flip_image",
                          text='Flip Vertical',
                          icon_value=get_icon('flip_vertical')).flip_value = "flip vertical"

        # view
        row = box.row(True)
        row.operator("image.view_all",
                     text="Fit",
                     icon_value=get_icon('view_fit')).fit_view = True
        # row.operator("image.view_zoom_ratio",
        #              text="All")
        row.operator("image.view_zoom_ratio",
                     text="Actual",
                     icon_value=get_icon('view_actual')).ratio = 1

        # zoom
        row = box.row(True)
        row.operator("image.view_zoom_out",
                     text="Zoom Out",
                     icon_value=get_icon('zoom_out'))
        row.operator("image.view_zoom_in",
                     text="Zoom In",
                     icon_value=get_icon('zoom_in'))

        # save/saveas
        row = box.row(True)
        row.operator("image.reload",
                     text="Reload",
                     icon_value=get_icon('reload'))
        row.operator('image.save',
                     text="save",
                     icon_value=get_icon('save'))
        row.operator('image.save_as',
                     text="save as",
                     icon_value=get_icon('save_as'))

        # copy path
        # TODO: created by salapati @ 2018-3-4 13:50:25
        # active only if image is there...
        row = box.row(True)
        row.operator('scene.im_copy_image_path',
                     text="Path",
                     icon_value=get_icon('copy_path'))

        row.operator('scene.im_copy_image_path',
                     text="Image",
                     icon_value=get_icon('copy_image'))

        # slide show
        row = box.row(True)
        row.prop(context.scene,
                 'IM_slide_show_speed',
                 text="Slide Show Speed")
        row.operator('scene.im_slide_show',
                     text="",
                     icon="PLAY")

        # background color
        row = box.row(True)
        row.prop(context.user_preferences.themes[0].image_editor.space,
                 "back",
                 text="Background Color")
        row.operator('scene.im_reset_bg_color',
                     text="",
                     icon_value=get_icon('reload'))

        # TODO: created by salapati @ 2017-10-30 12:25:16
        # reset the value to the theme default
        
        row = box.row(True)
        # make this a dropdown of applicaitons 
        # which are linked to it;
        size_dropdown = bpy.props.EnumProperty(
            items = utilities_ui.size_textures,
            name = "Texture Size",
            update = on_dropdown_size, 
            default = '512'
        )

        row.operator('scene.im_open_image_external',
                     text="",
                     icon_value=get_icon('open_file_external')).app = 'ps'

        row = box.row(True)
        row.operator("wm.url_open", text="Source", icon='INFO').url = "https://github.com/cg-cnu/blender-image-viewer/"

        

class IM_Open_Image_External(bpy.types.Operator):
    """ Open image in external
    """
    bl_idname = "scene.im_open_image_external"
    bl_label = "open image external"
    bl_options = {'REGISTER', 'UNDO'}
    app = bpy.props.StringProperty()

    def execute(self, context):
        self.report({'INFO'}, 'Open in {}'.format(self.app))
        return {'FINISHED'}


# TODO: created by admin @ 2017-10-28 17:42:07
# change the icon on click ; its a toggle
class IM_Slide_Show(bpy.types.Operator):
    """ Save all modified images
    """
    bl_idname = "scene.im_slide_show"
    bl_label = "Slide Show"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # IM_slide_show_speed
        # for every n seconds go to next image

        self.report({'INFO'}, 'Slide show started')

        return {'FINISHED'}


# class IM_Save_All_Images(bpy.types.Operator):
#     """ Save all modified images
#     """
#     bl_idname = "scene.im_save_all_images"
#     bl_label = "Save all images"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self, context):
#         # get all the modified images
#         # then save them on to the original one by one

#         self.report({'INFO'}, ' Saved all the images.')

#         return {'FINISHED'}


class IM_Copy_Image_Path(bpy.types.Operator):
    """ Copy image path
    """
    bl_idname = "scene.im_copy_image_path"
    bl_label = "Copy Image Path"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                path = area.spaces.active.image.filepath_from_user()
                bpy.context.window_manager.clipboard = path
                self.report({'INFO'}, 'Image path {} copied.'.format(path))

        return {'FINISHED'}


def get_images(path):
    """ get all the images in the given path
    """
    return [img for img in os.listdir(path) if img.endswith('.png')]

def get_next_element(array, index):
    """ get the next element in the array
    """
    if( index == len(array) - 1):
        return 0
    return index + 1


def get_prev_element(array, index):
    """ get the prev element in the array
    """
    if( index == 0 ):
        return len(array) - 1
    return index-1

class IM_Change_Image(bpy.types.Operator):
    """ Change current image
    """
    bl_idname = "scene.im_change_image"
    bl_label = "change current image"
    bl_options = {'REGISTER', 'UNDO'}
    direction = bpy.props.StringProperty()
    # image_position = 0

    def execute(self, context):
        # set that image as the current image
        # get current image
        #
        self.report({'INFO'}, '{0} Image'.format(self.direction))
        root_path = context.scene.IM_folder_path
        img_tray = context.scene['IM_Image_Tray']
        # img_position = context.scene.IM_Image_Tray_Position
        # image_tray = context.scene.IM_Image_Tray
        # print(context.scene.IM_folder_path)
        if self.direction == 'left':
            context.scene.IM_Image_Tray_Position = get_prev_element(img_tray, context.scene.IM_Image_Tray_Position )
        # print (self.direction)    
        if self.direction == 'right':
            context.scene.IM_Image_Tray_Position = get_next_element(img_tray, context.scene.IM_Image_Tray_Position )

        img_path = os.path.join(
            root_path, img_tray[context.scene.IM_Image_Tray_Position])
        # self.report( {'INFO'}, ' '.join(context.scene['IMG_TRAY'] ) )
        # self.report( {'INFO'}, img_path )
        # self.report( {'INFO'}, str( context.scene.IM_Image_Tray_Position ) )
        # self.report( {'INFO'}, str( img_path ) )
        print("img_path", img_path)
        print("root_path", root_path)
        if(os.path.exists(img_path)):
            # load the image
            print(img_path)
            new_image = bpy.data.images.load(img_path,
                                             check_existing=True)
            # set image as current image after loading...
            for area in bpy.context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    area.spaces.active.image = new_image

        return {'FINISHED'}


class IM_Flip_Image(bpy.types.Operator):
    """ Flip Image
    """
    bl_idname = "scene.im_flip_image"
    bl_label = "Flip image"
    bl_options = {'REGISTER', 'UNDO'}
    flip_value = bpy.props.StringProperty()

    def execute(self, context):
        self.report({"INFO"}, "%s" % (self.flip_value))
        return {'FINISHED'}


class IM_Rotate_Image(bpy.types.Operator):
    """ Rotate Image
    """
    bl_idname = "scene.im_rotate_image"
    bl_label = "Rotate image"
    bl_options = {'REGISTER', 'UNDO'}
    rotate_value = bpy.props.StringProperty()

    def execute(self, context):
        self.report({"INFO"}, "%s" % (self.rotate_value))
        return {'FINISHED'}


def update_folder_path(self, context):
    root_path = context.scene.IM_folder_path

    # get all the images
    context.scene['IM_Image_Tray'] = get_images(root_path)
    # set the position to first image
    context.scene.IM_Image_Tray_Position = 0

    # load the first image in the folder
    new_image = bpy.data.images.load(os.path.join(root_path,
                                                  context.scene['IM_Image_Tray'][0]),
                                     check_existing=True)

    # set image as current image after loading...
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            area.spaces.active.image = new_image

    self.report({"INFO"}, "Image %s loaded" % (self.IM_folder_path))


# TODO: created by admin @ 2017-10-31 10:26:38
# fix even if relative path is not enabled
# def get_folder_path(self, context):
    # os.path.realpath(bpy.path.abspath(self.))


def register():
    bpy.utils.register_class(Image_Viewer_Panel)
    # FIXME: noticed by admin @ 2017-10-30 14:03:20
    #  change the input to aboslute path on load
    # bpy.path.abspath(path)
    bpy.types.Scene.IM_Image_Tray_Position = bpy.props.IntProperty(
        name="")
    bpy.types.Scene.IM_folder_path = bpy.props.StringProperty(
        name="",
        default="",
        description="Folder path to load images",
        update=update_folder_path,
        # get=get_folder_path,
        subtype='DIR_PATH')

    bpy.types.Scene.IM_slide_show_speed = bpy.props.IntProperty(
        name="",
        description="Slide Show Speed",
        default=2)

    bpy.utils.register_class(IM_Change_Image)
    bpy.utils.register_class(IM_Flip_Image)
    bpy.utils.register_class(IM_Rotate_Image)
    bpy.utils.register_class(IM_Copy_Image_Path)
    bpy.utils.register_class(IM_Slide_Show)
    bpy.utils.register_class(IM_Open_Image_External)

    global custom_icons
    custom_icons = bpy.utils.previews.new()
    # script_path = bpy.context.space_data.text.filepath
    # icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    icons_dir = '/Users/salapati/Documents/codemonk/cg-cnu/addons/blender-image-viewer/icons'
    # print ("icons_dir", icons_dir)
    # get all the png files in the icons_dir
    for icon in os.listdir(icons_dir):
        name = icon.split('.')[0]
        custom_icons.load(name, os.path.join(icons_dir, icon), 'IMAGE')
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_class(Image_Viewer_Panel)

    del bpy.types.Scene.IM_folder_path
    del bpy.types.Scene.IM_slide_show_speed
    del bpy.types.Scene.IM_Image_Tray_Position

    bpy.utils.unregister_class(IM_Change_Image)
    bpy.utils.unregister_class(IM_Flip_Image)
    bpy.utils.unregister_class(IM_Rotate_Image)
    bpy.utils.unregister_class(IM_Copy_Image_Path)
    bpy.utils.unregister_class(IM_Slide_Show)
    bpy.utils.unregister_class(IM_Open_Image_External)

    global custom_icons
    bpy.utils.previews.remove(custom_icons)
    bpy.utils.unregister_module(__name__)

    # bpy.utils.previews.remove(preview_icons)

custom_icons = None

if __name__ == "__main__":
    register()

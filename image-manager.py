bl_info = {
	"name": "Image Manager",
	"description": "A simple image manager",
	"author": "Sreenivas Alapati",
	"version": (0, 0, 1),
	"blender": (2, 7, 8),
	"location": "UV/Image Editor > Toolshelf > Image Manager",
	"category": "Scene",
}

import bpy
import subprocess

# IDEA: logged by admin @ 2017-10-28 14:53:07
# show the list of images on the right ?

# Change background color to black ?

# open with
# multiple items ? 

# metadata
# class Image_Manager_Metadata(bpy.types.Panel):
# 	"""
# 	show image metadata
# 	"""

class Image_Manager_Panel(bpy.types.Panel):
	"""
	 Resize Texutres
	"""
	bl_label = "Image Manager"
	bl_space_type = "IMAGE_EDITOR"
	bl_region_type = "TOOLS"

	def draw(self, context):
		layout = self.layout
		column = layout.column(True)

		# open
		row = column.row(True)
		row.prop(context.scene, 'IM_folder_path')
		row = column.row(True)
		row.label('Image Manager')

		# move
		row = column.row(True)
		row.label('Load:')
		op = row.operator("scene.im_change_image", '<')
		op.direction = 'left'

		op = row.operator("scene.im_change_image", '>')
		op.direction = 'right'

		# rotate
		row = column.row(True)
		row.label('Rotate:')

		op = row.operator("scene.im_rotate_image", 'L')
		op.rotate_value = "90"

		op = row.operator("scene.im_rotate_image", 'R')
		op.rotate_value = "-90"

		# flip
		row = column.row(True)
		row.label('Flip:')

		op = row.operator("scene.im_flip_image", 'H')
		op.flip_value = "90"

		op = row.operator("scene.im_flip_image", 'V')
		op.flip_value = "-90"

		# view
		row = column.row(True)
		row.operator("image.view_all", text="Fit").fit_view = True
		row.operator("image.view_zoom_ratio", text="All")
		row.operator("image.view_zoom_ratio", text="Actual").ratio = 1
		# zoom
		row = column.row(True)
		row.operator("image.view_zoom_out", text="", icon="ZOOM_OUT")
		row.operator("image.view_zoom_in", text="", icon="ZOOM_IN")
		# reload image
		row = column.row(True)
		row.operator("image.reload", text="", icon="FILE_REFRESH")
		# save/saveas
		row = column.row(True)
		row.operator('image.save', text="save", icon="SAVE_AS")
		row.operator('image.save', text="save all", icon="SAVE_AS")
		row.operator('image.save_as', text="save as", icon="SAVE_AS")
		# copy path
		row = column.row(True)
		row.operator('scene.im_copy_image_path', "Copy Path")

		# slide show
		row = column.row(True)
		row.operator('scene.im_slide_show', "Slide Show")


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


class IM_Save_All_Images(bpy.types.Operator):
	""" Save all modified images
	"""
	bl_idname = "scene.im_save_all_images"
	bl_label = "Save all images"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		# get all the modified images
		# then save them on to the original one by one

		self.report({'INFO'}, ' Saved all the images.')

		return {'FINISHED'}


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


class IM_Change_Image(bpy.types.Operator):
	""" next image
	"""
	bl_idname = "scene.im_change_image"
	bl_label = "Next image"
	bl_options = {'REGISTER', 'UNDO'}
	direction = bpy.props.StringProperty()

	def execute(self, context):
		self.report({'INFO'}, '{0} Image'.format(self.direction))
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
	""" Flip Image
	"""
	bl_idname = "scene.im_rotate_image"
	bl_label = "Flip image"
	bl_options = {'REGISTER', 'UNDO'}
	rotate_value = bpy.props.StringProperty()

	def execute(self, context):
		self.report({"INFO"}, "%s" % (self.rotate_value))
		return {'FINISHED'}


def register():
	bpy.utils.register_class(Image_Manager_Panel)

	bpy.types.Scene.IM_folder_path = bpy.props.StringProperty(
		name="",
		description="Folder path",
		default="")

	bpy.types.Scene.IM_slide_show_speed = bpy.props.StringProperty(
		name="",
		description="Slide Show Speed",
		default="")

	bpy.utils.register_class(IM_Change_Image)
	bpy.utils.register_class(IM_Flip_Image)
	bpy.utils.register_class(IM_Rotate_Image)
	bpy.utils.register_class(IM_Copy_Image_Path)
	bpy.utils.register_class(IM_Slide_Show)


def unregister():
	bpy.utils.unregister_class(Image_Manager_Panel)

	del bpy.types.Scene.IM_folder_path
	del bpy.types.Scene.IM_slide_show_speed

	bpy.utils.unregister_class(IM_Change_Image)
	bpy.utils.unregister_class(IM_Flip_Image)
	bpy.utils.unregister_class(IM_Rotate_Image)
	bpy.utils.unregister_class(IM_Copy_Image_Path)
	bpy.utils.register_class(IM_Slide_Show)


if __name__ == "__main__":
	register()

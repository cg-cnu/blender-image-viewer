bl_info = {
	"name": "Image Manager",
	"description": "Simple Image Manager",
	"author": "Sreenivas Alapati",
	"version": (0, 0, 1),
	"blender": (2, 7, 8),
	"location": "UV/Image Editor > Toolshelf > Image Manager",
	"category": "Scene",
}

import bpy
import subprocess


class RM_Image_Manager_Panel(bpy.types.Panel):
	"""
	 Resize Texutres
	"""
	bl_label = "Image Manager"
	bl_space_type = "IMAGE_EDITOR"
	bl_region_type = "TOOLS"

	def draw(self, context):
		layout = self.layout
		column = layout.column(True)

		# type
		row = column.row(True)
		row.template_icon_view(context.window_manager, "images_enum")


class RM_Prev_Image(bpy.types.Operator):
	""" prev image
	"""
	bl_idname = "scene.rm_prev_image"
	bl_label = "Previous image"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		self.report({'INFO'}, 'Previous images')


class RM_Next_Image(bpy.types.Operator):
	""" next image
	"""
	bl_idname = "scene.rm_prev_image"
	bl_label = "Next image"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		self.report({'INFO'}, 'Next Image')

def register():
	bpy.utils.register_class(RM_Reference_Manager_Panel)
	bpy.utils.register_class(RM_Prev_Image)
	bpy.utils.register_class(RM_Next_Image)

def unregister():
	bpy.utils.unregister_class(RM_Reference_Manager_Panel)
	bpy.utils.unregister_class(RM_Prev_Image)
	bpy.utils.unregister_class(RM_Next_Image)

if __name__ == "__main__":
	register()


Path = "E:\\Eastshade\\Assets\\Models\\" # absolute path with double backslashes between directory names. Blank quotes ("") will dump into the current .blend path.


"""
================================
Unity Simple Export v1.4 for Blender
by Daniel Weinbaum
www.eastshade.com

Description:
Exports one .dae for each empty with mesh children in your scene.
#================================
"""

bl_info = {
	"name": "UnitySimpleExport",
	"description": "Exports one .dae for each empty with mesh children in your scene.",
	"author": "Daniel Weinbaum",
	"version": (1, 4),
	"blender": (2, 70),
	"location": "View3d > Tool Panel",
	"category": "Import-Export"}

import bpy
import math

class UnitySimpleExport(bpy.types.Operator):
	'''Exports one .dae for each empty with mesh children in your scene.'''
	bl_idname = "object.unity_simple_export"
	bl_label = "Unity Simple Export"
	def execute(self, context):
		
		bpy.ops.wm.save_mainfile() #simply saves
		
		oldlayers = [False] * 20 #list of 20 false values
		
		for i in range(0, 20): #store all original layers
			oldlayers[i] = bpy.context.scene.layers[i]
		
		for i in range(0, 20): #show all layers
			bpy.context.scene.layers[i] = True

		bpy.ops.object.hide_view_clear()

		def ObNames():
			names = []
			for i in bpy.data.objects:
				names.append(i.name)
			return names

		def ExportProp(empty):
			
			succeeded = False
			
			if (len(bpy.context.selected_objects) != 1) or (bpy.context.selected_objects[0].type != 'EMPTY'):
				print('Script failed to select one empty object')
			else:
				parentempty = bpy.context.selected_objects[0]
				bpy.context.scene.objects.active = parentempty
				initloc = parentempty.location.copy()
				bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
				
				parentempty.location = (0,0,0)
				
				bpy.ops.object.duplicate(linked=False)
				bpy.ops.object.duplicates_make_real()
				obs = bpy.context.selected_objects #store new selection of duplicates
				bpy.ops.object.move_to_layer(layers=(False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False))
				bpy.context.scene.layers[8] = True

				for i in obs:
					bpy.ops.object.select_all(action="DESELECT")
					if i.name in ObNames()  : #if name is found in scene
						i.select = True
						bpy.context.scene.objects.active = i
						
				for i in obs:
					if i.type == 'MESH' :
						i.select = True
						bpy.context.scene.objects.active = i
				
				#apply modifiers, join all to one mesh and rename it, place its pivot at origin
				bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True, material=False, texture=False, animation=False)
				bpy.ops.object.convert(target='MESH')
				bpy.ops.object.join()
				bpy.context.selected_objects[0].name = parentempty.name + "_mesh"
				bpy.ops.view3d.snap_cursor_to_center()
				bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
				
				#apply rot and scale, do the stupid -90 on x thang
				bpy.context.space_data.use_pivot_point_align = False #make sure affect pivot only is off
				bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
				bpy.ops.transform.rotate(value=-math.pi / 2.0, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
				bpy.ops.transform.rotate(value=math.pi / 2.0, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
				
				
				if Path != "":
					exportpath = Path
				else:
					exportpath = bpy.path.abspath("//")
				exportname = parentempty.name
				fileextension = '' #.dae automatically adds the extension
				fullpath = exportpath + exportname + fileextension
				
				bpy.ops.wm.collada_export(
				filepath=fullpath, 
				check_existing=True, 
				apply_modifiers=True,
				export_mesh_type_selection='view', 
				selected=True, 
				include_children=False, 
				include_armatures=False, 
				include_shapekeys=False,
				active_uv_only=False, 
				include_uv_textures=False, 
				include_material_textures=True, 
				use_texture_copies=False,
				deform_bones_only=False,
				open_sim=False,
				triangulate=False,
				use_object_instantiation=False,
				export_transformation_type_selection='matrix',
				sort_by_name=False
				)
				
				#Clean up the mess
				bpy.ops.object.select_all(action="DESELECT")
				for i in obs:
					i.select = True
				
				bpy.ops.object.delete()
				succeeded = True
				print("This prop exported successfully")
					
				parentempty.select = True
				parentempty.location = initloc
			
			print("")
			
			return succeeded

		props = []
		iprops = 0

		for x in bpy.data.objects: #add all the empties to the props list
			if (x.type == 'EMPTY') and (x.dupli_type == 'NONE') and (x.empty_draw_type == 'CUBE') :
				props.append(x)
		
		for prop in props:
			bpy.ops.object.select_all(action="DESELECT")
			prop.select = True
			succeeded = ExportProp(prop)
			if succeeded:
				iprops += 1

		print( str(iprops) + " out of " + str(len(props) ) + " props have exported" )
		
		for i in range(0, 20): #set the layers back to how they were
			bpy.context.scene.layers[i] = oldlayers[i]
		
		print('') #skip a line
		print('') #skip a line
		
		return{'FINISHED'}

def register():
	bpy.utils.register_class(UnitySimpleExport)

def unregister():
	bpy.utils.unregister_class(UnitySimpleExport)

if __name__ == "__main__":
	register()
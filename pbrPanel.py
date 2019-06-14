import bpy
from bpy.props import BoolProperty


# Custom Properties
bpy.types.Object.mapNodes = BoolProperty(name="mapnode", description="Attribute Replacer Flag")
bpy.types.Object.normalHeights = BoolProperty(name="nomralheights", description="Normal and Heightmap Flag")
bpy.types.Object.levelControllers = BoolProperty(name="levelcontrollers", description="Adds Brightness and Contrast Nodes for all non color data maps")
#bpy.types.Object.invertGloss = BoolProperty(name="invertgloss", description="Adds Invert node to support Glossy Maps")
bpy.types.Object.materialName = bpy.props.StringProperty(name = "PBR Material Name", description = "My description",default = "default")

# UI Panel Class
class PbrifyInterface(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'      
    bl_label = 'Quick PBR Generator: PBRify'
    
    @classmethod
    def poll(self, context):
        return True
        
    def draw(self, context):
        layout = self.layout
        currentObject = context.object
        layout.label(text='Advance PBR Material Settings', text_ctxt='', translate=True, icon='NONE', icon_value=0)
        layout.prop(currentObject,'normalHeights',text='Normal + Height Map (Bumps)')
        layout.prop(currentObject,'mapNodes',text='Use Attribute Nodes instead of Mapping Nodes') 
        layout.prop(currentObject,'levelControllers',text='Add Brightness/Contrast Controllers') 
        #layout.prop(currentObject,"invertGloss",text='Invert Glossiness Map') 
        layout.prop(currentObject, "materialName")

        row = layout.row()
        row.scale_y = 2.0
        row.operator('material.pbrify', text='Create PBR Material', text_ctxt='', translate=True, icon='NONE', emboss=True, icon_value=0)


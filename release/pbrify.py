# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.props import BoolProperty
from mathutils import Vector

# Addon Description
bl_info = {
    "name" : "pbrify",
    "author" : "Raghav Venkat",
    "description" : "Quick PBR Node Setup Generator for Blender Cycles and EEVEE engine",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "Properties > Material > Quick PBR Generator: PBRify",
    "warning" : "",
    "category" : "Material",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/RaghavVenkat/pbrify",
    "tracker_url": "https://github.com/RaghavVenkat/pbrify/issues"
}

# Core Operator Class
class PbrifyCreate(bpy.types.Operator):
    """Creates a new PBR Material and adds it to the current active object"""
    bl_idname = 'material.pbrify'
    bl_label = 'PBR Material Creator'
    bl_description = 'Creates a new PBR Material and adds it to the current active object'
    bl_category = 'pbrify'
    
    def execute(self, context):
        
        notRc = None

        # Blender version check
        if(bpy.app.version[0] == 2):
            if(bpy.app.version_string[:3] == '2.8'  or bpy.app.version_string[:3] == '2.7'):
            
                # Check engine mode 
                if(bpy.context.scene.render.engine != 'CYCLES'):
                    bpy.context.scene.render.engine = 'CYCLES'

                # Check object type
                if(bpy.context.selected_objects[0].type == 'MESH'): 
                    obj = bpy.context.selected_objects[0]
                    
                    # Material init 
                    bpy.context.object.materialName = bpy.context.object.materialName.lstrip()
                    bpy.context.object.materialName = bpy.context.object.materialName.rstrip()
                    if not bpy.context.object.materialName:
                        matPBR = bpy.data.materials.new(name='Unnamed PBR Material')
                    else:
                        matPBR = bpy.data.materials.new(name=bpy.context.object.materialName)
                    matPBR.use_nodes = True
                    nodes = matPBR.node_tree.nodes

                    # Node Group Cleaner
                    for node in nodes:
                        nodes.remove(node)

                    # PBR Nodes Creator
                    albedo = nodes.new(type='ShaderNodeTexImage')
                    roughness = nodes.new(type='ShaderNodeTexImage')
                    specular = nodes.new(type='ShaderNodeTexImage')
                    normal = nodes.new(type='ShaderNodeTexImage')
                    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
                    materialOutput = nodes.new(type='ShaderNodeOutputMaterial')
                    
                    #2.80rc+ version support
                    if(bpy.app.version_cycle == 'rc'):
                        # Add a dummy image 
                        bpy.ops.image.new()

                        albedo.image = bpy.data.images[-1]
                        roughness.image = bpy.data.images[-1]
                        specular.image = bpy.data.images[-1]
                        normal.image = bpy.data.images[-1]

                        # Set Color Space
                        albedo.image.colorspace_settings.name = 'sRGB'
                        roughness.image.colorspace_settings.name = 'Non-Color'
                        specular.image.colorspace_settings.name = 'Non-Color'
                        normal.image.colorspace_settings.name = 'Non-Color'
                    else:

                        # Set Color Space
                        albedo.color_space = 'COLOR'
                        roughness.color_space = 'NONE'
                        specular.color_space = 'NONE'
                        normal.color_space = 'NONE'

                    # Map converters
                    normalMap = nodes.new(type='ShaderNodeNormalMap')
                                    
                    # Add Frames
                    pbrImageFrame = nodes.new(type='NodeFrame')
                    pbrImageFrame.name = 'Image-Textures'
                    pbrImageFrame.label = 'Image-Textures'
                    albedo.parent = pbrImageFrame
                    roughness.parent = pbrImageFrame
                    specular.parent = pbrImageFrame
                    normal.parent = pbrImageFrame

                    # locator
                    specular.location = Vector((albedo.location[0], albedo.location[1] - 250))
                    roughness.location = Vector((specular.location[0], specular.location[1] - 250))
                    normal.location = Vector((roughness.location[0], roughness.location[1] - 250))
                    normalMap.location = Vector((pbrImageFrame.location[0]+480, pbrImageFrame.location[1]-650))
                    bsdf.location = Vector((pbrImageFrame.location[0]+650, pbrImageFrame.location[1]))
                    materialOutput.location = Vector((pbrImageFrame.location[0]+1000, pbrImageFrame.location[1]))
                                
                    # linker init
                    links = matPBR.node_tree.links

                    # Attribute Mapping or Coordinate Mapping
                    if(bpy.context.object.mapNodes==False):
                        txcoordinate = nodes.new(type='ShaderNodeTexCoord')
                        mapping = nodes.new(type='ShaderNodeMapping')
                        txCoordLink = links.new(txcoordinate.outputs[0], mapping.inputs[0])
                        mappingLink = links.new(mapping.outputs[0], albedo.inputs[0])
                        mappingLink = links.new(mapping.outputs[0], roughness.inputs[0])
                        mappingLink = links.new(mapping.outputs[0], specular.inputs[0])
                        mappingLink = links.new(mapping.outputs[0], normal.inputs[0])
                        txcoordinate.location = Vector((albedo.location[0]-700, albedo.location[1]))
                        mapping.location = Vector((albedo.location[0]-450, albedo.location[1]))

                        # Add Frame
                        mappingFrame = nodes.new(type='NodeFrame')
                        mappingFrame.location = Vector((normalMap.location[0]-100,normalMap.location[1]))
                        mappingFrame.name = 'Mapping'
                        mappingFrame.label = 'Mapping'
                        txcoordinate.parent = mappingFrame
                        mapping.parent = mappingFrame

                    else:
                        attributeNodeA = nodes.new(type='ShaderNodeAttribute')
                        attributeNodeR = nodes.new(type='ShaderNodeAttribute')
                        attributeNodeS = nodes.new(type='ShaderNodeAttribute')
                        attributeNodeN = nodes.new(type='ShaderNodeAttribute')
                        atrNodeALink = links.new(attributeNodeA.outputs[1],albedo.inputs[0])    
                        atrNodeRLink = links.new(attributeNodeR.outputs[1],roughness.inputs[0])
                        atrNodeSLink = links.new(attributeNodeS.outputs[1],specular.inputs[0])
                        atrNodeNLink = links.new(attributeNodeN.outputs[1],normal.inputs[0])
                        attributeNodeA.location = Vector((albedo.location[0]-450, albedo.location[1]))
                        attributeNodeS.location = Vector((albedo.location[0]-450, albedo.location[1]-150))
                        attributeNodeR.location = Vector((albedo.location[0]-450, albedo.location[1]-300))
                        attributeNodeN.location = Vector((albedo.location[0]-450, albedo.location[1]-450))

                        # Add Frame
                        mappingFrame = nodes.new(type='NodeFrame')
                        mappingFrame.location = Vector((normalMap.location[0]-50,normalMap.location[1]))
                        mappingFrame.name = 'Mapping'
                        mappingFrame.label = 'Mapping'
                        attributeNodeA.parent = mappingFrame
                        attributeNodeR.parent = mappingFrame
                        attributeNodeS.parent = mappingFrame
                        attributeNodeN.parent = mappingFrame

                    pbrImageFrame.location = Vector((-50.0,0.0))
                    mappingFrame.location = Vector((mappingFrame.location[0]-100,mappingFrame.location[1]))
                    pbrImageFrame.location = Vector((-50,0))

                    # Brightness/Contrast controller
                    if(bpy.context.object.levelControllers == True):
                        bcNodeA = nodes.new(type='ShaderNodeBrightContrast')
                        bcNodeR = nodes.new(type='ShaderNodeBrightContrast')
                        bcNodeS = nodes.new(type='ShaderNodeBrightContrast')
                        bcNodeN = nodes.new(type='ShaderNodeBrightContrast')
                        albedoBCLink = links.new(albedo.outputs[0], bcNodeA.inputs[0])
                        roughnessBCLink = links.new(roughness.outputs[0], bcNodeR.inputs[0])
                        specularBCLink = links.new(specular.outputs[0], bcNodeS.inputs[0])
                        normalImgBCLink = links.new(normal.outputs[0], bcNodeN.inputs[0])
                        bcNodeAbsdfLink = links.new(bcNodeA.outputs[0], bsdf.inputs[0])
                        bcNodeRbsdfLink = links.new(bcNodeR.outputs[0], bsdf.inputs[7])
                        bcNodeSbsdfLink = links.new(bcNodeS.outputs[0], bsdf.inputs[5])
                        bcNodeNnrmLink = links.new(bcNodeN.outputs[0], normalMap.inputs[1])
                        bcNodeA.location = Vector((bsdf.location[0]-250, bsdf.location[1]))
                        bcNodeR.location = Vector((bsdf.location[0]-250, bcNodeA.location[1]-400))
                        bcNodeS.location = Vector((bsdf.location[0]-250, bcNodeA.location[1]-200))
                        bcNodeN.location = Vector((bsdf.location[0]-350, bcNodeA.location[1]-600))
                    else:
                        albedoLink = links.new(albedo.outputs[0], bsdf.inputs[0])
                        roughnessLink = links.new(roughness.outputs[0], bsdf.inputs[7])
                        specularLink = links.new(specular.outputs[0], bsdf.inputs[5])
                        normalImgLink = links.new(normal.outputs[0], normalMap.inputs[1])

                    normalConverterLink = links.new(normalMap.outputs[0], bsdf.inputs[17])
                    outputLink = links.new(bsdf.outputs[0], materialOutput.inputs[0])

                    # Append Material
                    obj.data.materials.append(matPBR)

                else:
                    print('Materials can be applied only on Meshes')
                
        return {'FINISHED'}

# Custom Properties
bpy.types.Object.mapNodes = BoolProperty(name="mapnode", description="Attribute Replacer Flag")
#bpy.types.Object.normalHeights = BoolProperty(name="nomralheights", description="Normal and Heightmap Flag")
bpy.types.Object.levelControllers = BoolProperty(name="levelcontrollers", description="Adds Brightness and Contrast Nodes for all non color data maps")
#bpy.types.Object.invertGloss = BoolProperty(name="invertgloss", description="Adds Invert node to support Glossy Maps")
bpy.types.Object.materialName = bpy.props.StringProperty(name = "Name", description = "PBR Material Name",default = "PBR Material")

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
        #layout.prop(currentObject,'normalHeights',text='Normal + Height Map (Bumps)')
        layout.prop(currentObject,'mapNodes',text='Use Attribute Nodes instead of Mapping Nodes') 
        layout.prop(currentObject,'levelControllers',text='Add Brightness/Contrast Controllers') 
        #layout.prop(currentObject,"invertGloss",text='Invert Glossiness Map') 
        layout.prop(currentObject, "materialName")

        row = layout.row()
        row.scale_y = 2.0
        row.operator('material.pbrify', text='Click to Create PBR Material', text_ctxt='', translate=True, icon='NONE', emboss=True, icon_value=0)

# Registration
#classes = (PbrifyCreate, PbrifyInterface)
#register, unregister = bpy.utils.register_classes_factory(classes)  

def register():
    bpy.utils.register_class(PbrifyCreate)
    bpy.utils.register_class(PbrifyInterface)

def unregister():
    bpy.utils.unregister_class(PbrifyInterface)
    bpy.utils.unregister_class(PbrifyCreate)

if __name__ == "__main__":
    register()

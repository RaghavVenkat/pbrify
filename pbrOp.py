import bpy
from mathutils import Vector

# Core Operator Class
class PbrifyCreate(bpy.types.Operator):
    """Creates a new PBR Material and adds it to the current active object"""
    bl_idname = "material.pbrify"
    bl_label = "PBR Material Creator"
    bl_description = "Creates a new PBR Material and adds it to the current active object"
    bl_category = 'pbrify'

    def execute(self, context):
        
        # Check engine mode 
        if(bpy.context.scene.render.engine != 'CYCLES'):
            bpy.context.scene.render.engine = 'CYCLES'

        # Check object type
        if(bpy.context.selected_objects[0].type == 'MESH'): 
            obj = bpy.context.selected_objects[0]
            
            # Material init 
            matPBR = bpy.data.materials.new(name="PBR Material")
            matPBR.use_nodes = True
            nodes = matPBR.node_tree.nodes

            # Node Group Cleaner
            for node in nodes:
                nodes.remove(node)

            # PBR Node Group Creator
            albedo = nodes.new(type='ShaderNodeTexImage')
            roughness = nodes.new(type='ShaderNodeTexImage')
            specular = nodes.new(type='ShaderNodeTexImage')
            normal = nodes.new(type='ShaderNodeTexImage')
            bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
            materialOutput = nodes.new(type='ShaderNodeOutputMaterial')
            
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

            # Attribute Mapping or  Coordinate Mapping
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

                # Add Frames
                mappingFrame = nodes.new(type='NodeFrame')
                mappingFrame.location = Vector((normalMap.location[0]-50,normalMap.location[1]))
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

                # Add Frames
                mappingFrame = nodes.new(type='NodeFrame')
                mappingFrame.location = Vector((normalMap.location[0]-50,normalMap.location[1]))
                mappingFrame.name = 'Mapping'
                mappingFrame.label = 'Mapping'
                attributeNodeA.parent = mappingFrame
                attributeNodeR.parent = mappingFrame
                attributeNodeS.parent = mappingFrame
                attributeNodeN.parent = mappingFrame

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

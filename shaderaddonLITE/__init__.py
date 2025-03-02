import bpy
import os

bl_info = {
    "name": "Blender三渲二资产套件",
    "author": "本插件由B站UP主-记忆面包拯救我-汉化制作 <https://space.bilibili.com/3546571046128187?spm_id_from=333.1007.0.0>",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "category": "Object",
    "description": "本插件由B站UP主-记忆面包拯救我-汉化制作",
}

import addon_utils
import random
from bpy.app.handlers import persistent
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, PointerProperty, FloatProperty
import time
import webbrowser

#add effect enum items
def operator_items(self, context):
    return [
        ('CT_LIGHTING', "----光照与阴影----", "光照类别"),
        ('DIFFUSELIGHTING', "风格化3D光照 (主要) (动态) (EEVEE)", "添加漫反射光照。如果你想在Cycles中使用它，请烘焙"),
        # ('SPECULAR', "Add Specular Reflection (Dynamic) (EEVEE)", "Add Specular Reflection. bake if you would like to use it in cycles"),
        # ('MOODLIGHT', "Add Colored Circular Light", "Add a Colored Circular Light"),
        # ('CIRCULARLIGHTING', "Add Circular Lighting", "Add Circular Lighting"),
        ('FAKELIGHT', "添加风格化3D光 (每个对象)", "添加风格化3D光照 (Eevee+Cycles) (轻松烘焙)"),
        ('AO', "添加环境光遮蔽", "添加环境光遮蔽"),
        ('CURVATURE', "添加曲率", "添加曲率效果"),
        ('CROSSHATCHING', "交叉阴影光照 (EEVEE)", "添加交叉阴影光照"),
        # ('FAKESUNLIGHT', "Add Stylized 3D Sun Lighting (Experimental, Old)", "Add Stylized 3D Sun Lighting (Eevee+Cycles)"),
        # ('HAIRCURVES', "Add Anisotropic Hair Reflection (For Curves)", "Add Anisotropic Hair Reflection (For Curves)"),

        (' ', " ", " "),
        ('CT_SPLS', "风格化点光源", "风格化点光源 category"),
        ('SPLRed', "添加风格化点光源 #1", "Add 风格化点光源 #1"),

        (' ', " ", " "),
        ('CT_TEXTURING', "----手绘纹理----", "纹理类别"),
        ('DRAWPAINT', "纹理绘画 / 绘制 (所有颜色)", "在你的模型上绘画 / 绘制 (UV，纹理绘画)"),
        ('DRAWONECOLOR', "用单一颜色绘制/绘画", "用单一颜色绘制/绘画"),
        ('WORLDSTROKES', "添加简单透明度 / 笔触", "添加简单透明度 / 笔触"),
        # ('VERTEXPAINT', "Draw with Vertex Paint", "Paint/Draw on your Model (Vertex Paint)"),
        ('TRANSPARENTPAINT', "添加水彩/炭笔效果", "添加水彩/炭笔效果"),

        

        (' ', " ", " "),
        (' ', " ", " "),
        ('CT_OUTLINING', "----轮廓描边----", "纹理类别"),

        ('SOLIDIFYOUTLINE', "添加对象轮廓", "添加对象轮廓"),
        # ('EDGEDETECT', "Add Edge Detect", "Add Edge Detect"),
        # ('COLOREDEDGES', "添加彩色边缘", "添加彩色边缘"),
        
        (' ', " ", " "),
        ('CT_GRADIENTS', "----纹理----", "纹理类别"),

        ('LOCALGRADIENT', "局部渐变 (矩形)", "添加局部渐变"),
        ('INSTANTWATERCOLOR', "风格化污渍", "Add 风格化污渍 Effect"),
        ('EASYDT', "添加动态纹理 (简单)", "添加动态纹理 (简单)"),
        # ('NOISETEXTURE', "Add Dynamic Texture", "Add Dynamic Texture"),
        ('OVERALLTEXTURE', "添加纹理覆盖", "添加纹理覆盖"),
        # ('BRUSHSTROKES', "Add Dynamic Brush Strokes", "Add Dynamic Brush Strokes"),
        # ('STYLIZEDFOAM', "Add Stylized Foam", "Add Stylized Foam"),
        # ('TRANSPARENTNOISE', "Add Dynamic Texture (Transparent)", "Add Dynamic Texture (Transparent)"),

        (' ', " ", " "),
        (' ', " ", " "),
        ('CT_ADJUSTING', "----调整----", "纹理类别"),
        ('CONTRAST', "添加对比度", "添加对比度"),
        ('HSL', "添加HSL效果", "添加色相/饱和度/亮度调整"),
        ('OBJECTRANDOMIZE', "添加对象随机化", "添加对象随机化"),

        # (' ', " ", " "),
        # ('CT_OBJECTS', "----OBJECTS----", "纹理类别"),
        # ('FOG', "Add a Fog Object", "Add a Fog Object"),
        # ('STEAM', "Add a Steam Object", "Add a Steam Object"),
        # ('GODRAYS', "Add Godray Effect", "Add a Godray Effect"),


        
        # ('DISPLACE', "Add a Displace Effect", "Add a Displace Effect"),
        
        
        (' ', " ", " "),
        ('CT_EXPORTING', "----烘焙/导出----", "Export category"),
        # ('BAKE', "Bake Your Shader", "Bake Shader"),
        # ('BAKEANIMATED', "Bake Your Shader (Animated)", "Bake Your Shader (Animated)"),
        ('BAKENORMALS', "烘焙法线", "烘焙法线"),
    ]

bpy.types.Scene.my_directory_enum = bpy.props.StringProperty(
    name="Directory",
    description="选择一个目录:",
    default="",
    maxlen=1024,
    subtype='DIR_PATH'
)


bpy.types.Scene.processing_speed = bpy.props.FloatProperty(
    name = "设置动画烘焙的处理速度",
    description = "",
    default = 8.0,
    min = 1.0
)


#enum for the add effect enum
bpy.types.Scene.my_operator_enum = bpy.props.EnumProperty(
    name="Operator",
    description="Choose an operator",
    items=operator_items,
)

#enum for bake resolution
bpy.types.Scene.user_input_number = bpy.props.IntProperty(
    name="用户输入数字",
    description="输入一个数值",
    default=2048
)

#enum for user naming of bake textures
bpy.types.Scene.bake_name = bpy.props.StringProperty(
    name="用户输入烘焙名称",
    description="输入一个字符串值",
    default=""
)

def mask_items(self, context):
    return [
        ('GRADIENTSPHERE', "Edit Sphere Gradient Mask", "Edit Sphere Gradient Mask"),
        ('GRADIENTRECT', "Edit Rectangle Gradient Mask", "Edit Rectangle Gradient Mask"),
        ('NOISE', "Edit Noise Mask", "Edit Noise Mask"),
        ('WAVE', "Edit Wave Mask", "Edit Wave Mask"),
        ('WAVE2', "Edit Wave 2 Mask", "Edit Wave 2 Mask"),
        ("VORONOI", "Edit Voronoi Mask", "Edit Voronoi Mask"),
        ('FOAM', "Edit Foam Tiles Mask", "Edit Foam Tiles Mask"),
        ('TILES', "Tiles/Brick Mask", "Edit Tiles/Brick Mask"),
    ]

#Masks
bpy.types.Scene.my_mask_enum = bpy.props.EnumProperty(
    name="Mask",
    description="选择要编辑的蒙版",
    items=mask_items,
)

bpy.types.Scene.light_animate_enum = bpy.props.BoolProperty(
    name="布尔1",
    description="选择是否动画光照",
    default=False
)

bpy.types.Scene.curvaturelevels = bpy.props.IntProperty(
    name="用户输入数字",
    description="输入一个数值",
    default=2
)

bpy.types.Scene.hardsurface = bpy.props.BoolProperty(
    name="布尔1.2",
    description="Is your model harder surface",
    default=False
)

bpy.types.Scene.applied_sld = bpy.props.BoolProperty(
    name="布尔1.5",
    description="Select whether or not you want stylized light dynamic applied.",
    default=False
)

bpy.types.Scene.specular_animate_enum = bpy.props.BoolProperty(
    name="Bool2",
    description="Select whether or not you animated speculars",
    default=False
)

bpy.types.Scene.transparent_map = bpy.props.BoolProperty(
    name="Bool2",
    description="选择是否导出透明贴图",
    default=False
)

bpy.types.Scene.painterlyfilter = bpy.props.FloatProperty(
    name="PainterlyFilter",
    description="选择是否在反射光上应用绘画滤镜。你也可以手动绘制反射光纹理",
    default=0.0,
    min=0.0,
    max=1.0
)

#for the delete feature
def get_node_group_items():
    try:
        obj = bpy.context.object
    except:
        return []
    
    items = []
    obj = bpy.context.object

    if not obj:
        return items

    tempobj = None
    if obj.type == 'EMPTY' and obj.name.startswith("SB"):
        tempobj = obj.parent
        obj = tempobj
    elif obj.type == 'MESH' and obj.name.startswith("SB"):
        tempobj = obj.parent
        obj = tempobj

    if obj and obj.active_material and obj.active_material.use_nodes:
        node_tree = obj.active_material.node_tree
        for node in node_tree.nodes:
            if node.name == "Base Color":
                continue
            if node.type == 'GROUP':
                items.append((node.name, node.name, ""))

    return items

#for the view feature instead of delete
def get_node_group_items_view():
    try:
        obj = bpy.context.object
    except:
        return []
    
    items = []
    obj = bpy.context.object

    if not obj:
        return items
    
    items.append(('SHOWALL', "Show all Items", "Show all Effects"))

    tempobj = None
    if obj.type == 'EMPTY' and obj.name.startswith("SB"):
        tempobj = obj.parent
        obj = tempobj
    elif obj.type == 'MESH' and obj.name.startswith("SB"):
        tempobj = obj.parent
        obj = tempobj

    if obj and obj.active_material and obj.active_material.use_nodes:
        node_tree = obj.active_material.node_tree
        for node in node_tree.nodes:
            if node.type == 'GROUP':
                items.append((node.name, node.name, ""))

    return items

@persistent
def timer_function():
    try:
        obj = bpy.context.object
    except:
        kasou = False


    if bpy.data.materials.get("layerednodegroups") is None:
            current_directory = ''
            for mod in addon_utils.modules():
                if mod.bl_info['name'] == "Blender三渲二资产套件":
                    filepath = mod.__file__
                    current_directory = (os.path.dirname(filepath))
                else:
                    pass
            
            shader_builder_file_path = os.path.join(current_directory, "nodegroups.blend")
            print("Shader Builder File Path:", shader_builder_file_path)

            bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/Material/", filename="layerednodegroups")
            bpy.data.materials.get("layerednodegroups").use_fake_user = True
            if bpy.data.materials.get("solidifyoutline") is None:
                bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/Material/", filename="solidifyoutline")
                bpy.data.materials.get("solidifyoutline").use_fake_user = True
            if bpy.data.materials.get("SBfullblank") is None:
                bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/Material/", filename="SBfullblank")
                bpy.data.materials.get("SBfullblank").use_fake_user = True

    # if bpy.data.node_groups.get("InstantWatercolor") is None:
    #     bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/NodeTree/", filename="InstantWatercolor")
    # if bpy.data.node_groups.get("AddCurvature") is None:
    #     bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/NodeTree/", filename="AddCurvature")
    # if bpy.data.node_groups.get("RedLightSAS") is None:
    #     bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/NodeTree/", filename="AddCurvature")

    if bpy.data.node_groups.get("SB Light Creation") is None:
        current_directory = ''
        for mod in addon_utils.modules():
            if mod.bl_info['name'] == "Blender三渲二资产套件":
                filepath = mod.__file__
                current_directory = (os.path.dirname(filepath))
            else:
                pass
            
        shader_builder_file_path = os.path.join(current_directory, "nodegroups.blend")
        print("Shader Builder File Path:", shader_builder_file_path)

        bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/NodeTree/", filename="SB Light Creation")
        bpy.data.node_groups.get("SB Light Creation").use_fake_user = True
        bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/NodeTree/", filename="SunPower")
        bpy.data.node_groups.get("SunPower").use_fake_user = True


    items = []

    if not obj:
        return items
    
    items.append(('SHOWALL', "Show all Items", "Show all Effects"))

    tempobj = None
    if obj.type == 'EMPTY' and obj.name.startswith("SB"):
        tempobj = obj.parent
        obj = tempobj
    elif obj.type == 'MESH' and obj.name.startswith("SB"):
        tempobj = obj.parent
        obj = tempobj
    

    if obj and obj.active_material and obj.active_material.use_nodes:
        node_tree = obj.active_material.node_tree
        for node in node_tree.nodes:
            if node.type == 'GROUP':
                items.append((node.name, node.name, ""))

    newlist = []
    newlistview = []
    newlistswap1 = []
    newlistswap2 = []
    newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

    if obj and obj.active_material and obj.active_material.use_nodes:
        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
                newlistswap1.append((node.name, node.name, ""))
                newlistswap2.append((node.name, node.name, ""))
        #heres where we look for displace and add it to the enum
        for modifier in obj.modifiers:
            if modifier.name.startswith("SB") and not modifier.name.startswith("SB Geono") and not modifier.name.startswith("SB Sun"):
                newlist.append((modifier.name, modifier.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlistswap2
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlistswap1,
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

    return 1.0

bpy.app.timers.register(timer_function)

bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
    name="Node Groups",
    description = "节点组列表",
    items = get_node_group_items(),
)

bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
    name="Node Groups",
    description = "节点组列表",
    items = get_node_group_items(),
)

bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
    name="Node Groups",
    description = "节点组列表",
    items = get_node_group_items(),
)

# bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
#     name="Node Groups View",
#     description = "节点组列表 for effect viewer",
#     items = get_node_group_items_view(),
# )

bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
    name="要复制的组",
    description = "选择要复制的效果",
    items = get_node_group_items(),
)

class AppendBrushes(bpy.types.Operator):
    bl_idname = "shaderaddon.appendbrushes"
    bl_label = "将画笔包附加到场景"

    def execute(self, context):
        current_directory = ''
        for mod in addon_utils.modules():
            if mod.bl_info['name'] == "Blender三渲二资产套件":
                filepath = mod.__file__
                current_directory = (os.path.dirname(filepath))
            else:
                pass

        brushes_file_path = os.path.join(current_directory, "watercolorpainttest.blend")

        bpy.ops.wm.append(filepath="watercolorpainttest.blend", directory=brushes_file_path+"/Brush/", filename="Chalk")
        bpy.ops.wm.append(filepath="watercolorpainttest.blend", directory=brushes_file_path+"/Brush/", filename="Caligraphy Ink 1")
        bpy.ops.wm.append(filepath="watercolorpainttest.blend", directory=brushes_file_path+"/Brush/", filename="Caligraphy Ink Rake")
        bpy.ops.wm.append(filepath="watercolorpainttest.blend", directory=brushes_file_path+"/Brush/", filename="Gouache (Textured)")
        bpy.ops.wm.append(filepath="watercolorpainttest.blend", directory=brushes_file_path+"/Brush/", filename="Pastel")
        bpy.ops.wm.append(filepath="watercolorpainttest.blend", directory=brushes_file_path+"/Brush/", filename="Dotty Watercolor")
        
        try:
            brushes = bpy.data.brushes
        
            # First unmark all brushes as asset
            for brush in brushes:
                if brush.asset_data is not None:
                    brush.asset_clear()
                
            # Then mark them all as asset again
            for brush in brushes:
                brush.asset_mark()
        except:
            print("NO")


        return {'FINISHED'}

#Set up Fog








class WorldSetup(bpy.types.Operator):
    bl_idname = "shaderaddon.worldsetup"
    bl_label = "设置背景颜色"

    def execute(self, context):
        bpy.context.scene.view_settings.view_transform = 'Standard'

        if bpy.data.worlds.get("layeredworld") is None:
            current_directory = ''
            for mod in addon_utils.modules():
                if mod.bl_info['name'] == "Blender三渲二资产套件":
                    filepath = mod.__file__
                    current_directory = (os.path.dirname(filepath))
                else:
                    pass
            
            shader_builder_file_path = os.path.join(current_directory, "nodegroups.blend")
            print("Shader Builder File Path:", shader_builder_file_path)

            bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/World/", filename="layeredworld")

        bpy.context.scene.world = bpy.data.worlds.get("layeredworld")

        return {'FINISHED'}




#Set up shader button
class ShaderSetup(bpy.types.Operator):
    bl_idname = "shaderaddon.objectsetup"
    bl_label = "设置基础着色器"

    def execute(self, context):

        if bpy.data.brushes.get("Thick Dry Oil Paint") is None:
            bpy.context.scene.view_settings.view_transform = 'Standard'

        if bpy.data.materials.get("layerednodegroups") is None:
            current_directory = ''
            for mod in addon_utils.modules():
                if mod.bl_info['name'] == "Blender三渲二资产套件":
                    filepath = mod.__file__
                    current_directory = (os.path.dirname(filepath))
                else:
                    pass
            
            shader_builder_file_path = os.path.join(current_directory, "nodegroups.blend")
            print("Shader Builder File Path:", shader_builder_file_path)

            bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/Material/", filename="layerednodegroups")
            bpy.data.materials.get("layerednodegroups").use_fake_user = True
            if bpy.data.materials.get("solidifyoutline") is None:
                bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/Material/", filename="solidifyoutline")
                bpy.data.materials.get("solidifyoutline").use_fake_user = True
            if bpy.data.materials.get("SBfullblank") is None:
                bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/Material/", filename="SBfullblank")
                bpy.data.materials.get("SBfullblank").use_fake_user = True

        if bpy.data.node_groups.get("SB Light Creation") is None:
            current_directory = ''
            for mod in addon_utils.modules():
                if mod.bl_info['name'] == "Blender三渲二资产套件":
                    filepath = mod.__file__
                    current_directory = (os.path.dirname(filepath))
                else:
                    pass
            
            shader_builder_file_path = os.path.join(current_directory, "nodegroups.blend")
            print("Shader Builder File Path:", shader_builder_file_path)

            bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/NodeTree/", filename="SB Light Creation")
            bpy.data.node_groups.get("SB Light Creation").use_fake_user = True
            bpy.ops.wm.append(filepath="nodegroups.blend", directory=shader_builder_file_path+"/NodeTree/", filename="SunPower")
            bpy.data.node_groups.get("SunPower").use_fake_user = True

        if bpy.data.brushes.get("Chalk") is None:
            bpy.ops.shaderaddon.appendbrushes()

        new_material = bpy.data.materials.new(name="NewMaterial")
        new_material.use_nodes = True
        new_material.surface_render_method = 'BLENDED'

        new_material.node_tree.nodes.clear()

        basecolor_group = bpy.data.node_groups.get("basecolor")

        selected_obj = bpy.context.active_object

        if selected_obj.type != 'MESH' and selected_obj.type != 'EMPTY' and selected_obj.type != 'CURVE':
            return {'FINISHED'}

        tempobj = None
        if selected_obj.type == 'EMPTY' and selected_obj.name.startswith("SB"):
            tempobj = selected_obj.parent
            selected_obj = tempobj
        elif selected_obj.type == 'MESH' and selected_obj.name.startswith("SB"):
            tempobj = obj.parent
            selected_obj = tempobj

        if selected_obj.data.materials:
            selected_obj.data.materials[selected_obj.active_material_index] = new_material
        else:
            selected_obj.data.materials.append(new_material)
    
        nodes = new_material.node_tree.nodes
        links = new_material.node_tree.links

        basecolor_group_copy = basecolor_group.copy()

        node_group = nodes.new(type='ShaderNodeGroup')
        node_group.node_tree = basecolor_group_copy
        node_group.location = (0,0)
        node_group.name = "Base Color"

        material_output = nodes.new(type='ShaderNodeOutputMaterial')
        material_output.location = (200,0)
        links.new(node_group.outputs[0], material_output.inputs[0])

        scene = bpy.context.scene

        if scene.eevee.use_gtao == False:
            scene.eevee.use_gtao = True
            print("Ambient Occlusion enabled.")
        else:
            print("Ambient Occlusion was already enabled")

        try:
            if scene.eevee.use_bloom == False:
                scene.eevee.use_bloom = True
        except:
            print("AO")

        

        return {'FINISHED'}






class BakeCurvature(bpy.types.Operator):
    bl_idname = "shaderaddon.bakecurvature"
    bl_label = "烘焙曲率"

    def execute(self, context):
        try:
            #disable in renders all hidden objects
            for obj in bpy.context.scene.objects:
                # Check if the object is hidden in the viewport
                if obj.hide_get():
                    # If hidden, disable it in render
                    obj.hide_render = True
                else:
                    # If not hidden, enable it in render
                    obj.hide_render = False
        except:
            joe = "lasoutis"

        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        try:
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        except:
            joe = None
        
        prevobj = obj
        bpy.ops.object.duplicate()
        obj = bpy.context.active_object
        subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        if bpy.context.scene.hardsurface == True:
            subsurf.subdivision_type = 'SIMPLE'
        subsurf.levels = bpy.context.scene.curvaturelevels
        if obj and obj.data.shape_keys:
            obj.shape_key_clear()
        bpy.ops.object.modifier_apply(modifier=subsurf.name)

        node_tree = obj.active_material.node_tree


        diffuse_light_group = None
        for node in node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("AddCurvature"):
                diffuse_light_group = node
                break
        
        diffuse_light_group.node_tree.nodes.get("Color Attribute").layer_name = 'Color'

        # dirty vertex calculate
        color_attr = obj.data.color_attributes.new(
            name='Color',
            type='FLOAT_COLOR',
            domain='POINT'
        )

        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        obj.data.color_attributes.active_color = obj.data.color_attributes['Color']
        bpy.ops.paint.vertex_color_dirt()

        bpy.ops.object.mode_set(mode='OBJECT')

        # re_enable = []
        try:
            for modifier in obj.modifiers:
                if modifier.type == 'SOLIDIFY' and modifier.name.startswith("SB Out"):
                    #modifier.show_viewport = False
                    modifier.show_render = False
                    # re_enable.append(modifier)
                elif modifier.type == 'SOLIDIFY':
                    modifier.show_render = False
                    # re_enable.append(modifier)
        except:
            joe = None

        original_render_engine = bpy.context.scene.render.engine
        if original_render_engine != 'CYCLES':
            bpy.context.scene.render.engine = 'CYCLES'

        bpy.context.scene.cycles.samples = 4

        # Get the active material
        material = obj.active_material
        if not material:
            raise ValueError("The active object does not have a material.")

        # Get the node tree of the material
        
            
        diffuse_bsdf_node = None
        for node in diffuse_light_group.node_tree.nodes:
            if node.name == 'Diffuse BSDF':
                diffuse_bsdf_node = node
                break
        
        material_output_node = None
        current_output_node = None
        for node in node_tree.nodes:
            if node.name == 'Material Output':
                material_output_node = node
                for link in node.inputs['Surface'].links:
                    current_output_node = link.from_node
                break
        
        node_tree.links.new(diffuse_light_group.outputs['BSDF'], material_output_node.inputs['Surface'])


        image_texture_node = node_tree.nodes.new('ShaderNodeTexImage')

        tempimage = bpy.data.images.get(f"{obj.name} - Curvature")
        if tempimage is not None:
            tempimage.user_clear()
            bpy.data.images.remove(tempimage)

        new_image = bpy.data.images.new(f"{obj.name} - Curvature", width=bpy.context.scene.user_input_number, height=bpy.context.scene.user_input_number)
        image_texture_node.image = new_image

        bpy.context.view_layer.objects.active = obj
        bpy.context.object.active_material.node_tree.nodes.active = image_texture_node

        bpy.context.scene.cycles.bake_type = 'DIFFUSE'
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False
        bpy.context.scene.render.bake.use_pass_color = True

        # if diffuse_light_group.inputs[31].default_value > 0.75:
        #     diffuse_light_group.node_tree.nodes["quickmaths"].inputs[1].default_value = 0.09

        # Bake the texture
        bpy.ops.object.bake(type='DIFFUSE')

        # if diffuse_light_group.inputs[31].default_value > 0.75:
        #     diffuse_light_group.node_tree.nodes["quickmaths"].inputs[1].default_value = 0.00

        image_texture_node_group = None
        if diffuse_light_group.node_tree.nodes.get('CurvatureHelper') is None:
            image_texture_node_group = diffuse_light_group.node_tree.nodes.new('ShaderNodeTexImage')
        else:
            image_texture_node_group = diffuse_light_group.node_tree.nodes.get('CurvatureHelper')
        
        image_texture_node_group.image = new_image
        

        # map_range_node = None
        # for node in diffuse_light_group.node_tree.nodes:
        #     if node.type == 'MAP_RANGE' and node.name == 'ImportantRange':
        #         map_range_node = node
        #         break


            
        # map_range_node.inputs[2].default_value = 1.25
        
        # Connect the output of the image texture node to the 'Value' input of the 'Map Range' node
        # diffuse_light_group.node_tree.links.new(image_texture_node_group.outputs['Color'], map_range_node.inputs['Value'])
        # diffuse_light_group.node_tree.links.new(image_texture_node_group.outputs['Color'], diffuse_light_group.node_tree.nodes.get("ExtraRange").inputs[0])

        #restore painterly
        # diffuse_light_group.inputs[31].default_value = prevpainterly

        # Restore the original node connected to the material output
        if current_output_node:
            node_tree.links.new(current_output_node.outputs[0], material_output_node.inputs['Surface'])

        if original_render_engine != 'CYCLES':
            bpy.context.scene.render.engine = original_render_engine
        
        # diffuse_light_group.node_tree.nodes.remove(diffuse_bsdf_node)

        node_tree.nodes.remove(image_texture_node)

        bpy.ops.object.delete()
        bpy.context.view_layer.objects.active = prevobj
        prevobj.select_set(True)

        try:
            bpy.ops.image.save_all_modified()
        except:
            joe = 'KAsoutis'

        return {'FINISHED'}


class BakeNormals(bpy.types.Operator):
    bl_idname = "shaderaddon.bakenormals"
    bl_label = "烘焙法线贴图"

    def execute(self, context):
        try:
            #disable in renders all hidden objects
            for obj in bpy.context.scene.objects:
                # Check if the object is hidden in the viewport
                if obj.hide_get():
                    # If hidden, disable it in render
                    obj.hide_render = True
                else:
                    # If not hidden, enable it in render
                    obj.hide_render = False
        except:
            joe = "lasoutis"
        
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        try:
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        except:
            joe = None


        #disable other materials
        for material in bpy.data.materials:
            if material.name == obj.active_material.name:
                continue
            if material.use_nodes:
                # Get the node tree of the material
                nodes = material.node_tree.nodes
                
                # Loop through all nodes in the material
                for node in nodes:
                    # Exclude output nodes
                    if not node.name == 'Material Output':
                        if node.mute == False:
                            node.mute = True
                        else:
                            node.mute = False

        original_render_engine = bpy.context.scene.render.engine
        if original_render_engine != 'CYCLES':
            bpy.context.scene.render.engine = 'CYCLES'

        bpy.context.scene.cycles.samples = 2

        # Get the active material
        material = obj.active_material
        if not material:
            raise ValueError("The active object does not have a material.")

        # Get the node tree of the material
        node_tree = material.node_tree

        diffuse_light_group = None
        for node in node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("DiffuseL"):
                diffuse_light_group = node
                break
        

        #link stuff up
        
        

        #what does this even do??
        # diffuse_bsdf_node = None
        # for node in diffuse_light_group.node_tree.nodes:
        #     if node.name == 'Visibility':
        #         diffuse_bsdf_node = node
        #         break
        
        material_output_node = None
        current_output_node = None
        for node in node_tree.nodes:
            if node.name == 'Material Output':
                material_output_node = node
                for link in node.inputs['Surface'].links:
                    current_output_node = link.from_node
                break
        
        nodes = node_tree.nodes
        normalshelpergroup = bpy.data.node_groups.get("normalshelper")
        #Add the "bsdf" node to the material
        joekasou = normalshelpergroup
        normals_node = nodes.new(type='ShaderNodeGroup')
        normals_node.node_tree = joekasou

        node_tree = material.node_tree
        links = node_tree.links

        incoming_link = None
        for link in links:
            if link.to_node == material_output_node:
                incoming_link = link
                break

        #link up normals node
        links.new(diffuse_light_group.outputs[2], normals_node.inputs[0])
        links.new(normals_node.outputs[0], material_output_node.inputs[0])


        image_texture_node = node_tree.nodes.new('ShaderNodeTexImage')

        tempimage = bpy.data.images.get(f"{bpy.context.scene.bake_name} - Normals")
        if tempimage is not None:
            tempimage.user_clear()
            bpy.data.images.remove(tempimage)

        new_image = bpy.data.images.new(f"{bpy.context.scene.bake_name} - Normals", width=bpy.context.scene.user_input_number, height=bpy.context.scene.user_input_number)
        image_texture_node.image = new_image
        image_texture_node.image.use_fake_user = True
        image_texture_node.image.colorspace_settings.name = 'Non-Color'

        bpy.context.view_layer.objects.active = obj
        bpy.context.object.active_material.node_tree.nodes.active = image_texture_node

        bpy.context.scene.cycles.bake_type = 'NORMAL'
        bpy.context.scene.render.bake.normal_space = 'OBJECT'

        # Bake the texture
        bpy.ops.object.bake(type='NORMAL')

        # image_texture_node_group = node_tree.nodes.new('ShaderNodeTexImage')
        # image_texture_node_group.image = new_image
        # image_texture_node_group.name = "BakeAlpha"
        obj.active_material.node_tree.nodes.remove(image_texture_node)


        # Restore the original node connected to the material output
        if current_output_node:
            node_tree.links.new(current_output_node.outputs[0], material_output_node.inputs['Surface'])

        material.node_tree.nodes.remove(normals_node)

        if original_render_engine != 'CYCLES':
            bpy.context.scene.render.engine = original_render_engine

        #re enable all other materials.
        for material in bpy.data.materials:
            if material.name == obj.active_material.name:
                continue
            if material.use_nodes:
                # Get the node tree of the material
                nodes = material.node_tree.nodes
                
                # Loop through all nodes in the material
                for node in nodes:
                    # Exclude output nodes
                    if not node.name == 'Material Output':
                        if node.mute == False:
                            node.mute = True
                        else:
                            node.mute = False

        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        if nodes.get('NormalsTextureHelper') is None:
            tex_node = nodes.new('ShaderNodeTexImage')
            tex_node.name = 'NormalsTextureHelper'
            tex_node.image = new_image
        else:
            tex_node = nodes.get('NormalsTextureHelper')
            tex_node.image = new_image

        try:
            bpy.ops.image.save_all_modified()
        except:
            joe = 'KAsoutis'

        return {'FINISHED'}



class BakeAlphaAnimated(bpy.types.Operator):
    bl_idname = "shaderaddon.bakealphaanimated"
    bl_label = "烘焙动画透明贴图"

    def execute(self, context):
        try:
            #disable in renders all hidden objects
            for obj in bpy.context.scene.objects:
                # Check if the object is hidden in the viewport
                if obj.hide_get():
                    # If hidden, disable it in render
                    obj.hide_render = True
                else:
                    # If not hidden, enable it in render
                    obj.hide_render = False
        except:
            joe = "lasoutis"
        
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        try:
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        except:
            joe = None

        setto = True
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and (node.node_tree.name.startswith("TransparentNoise") or node.node_tree.name.startswith("TransparentWorldStrokes")):
                setto = False

        if setto:
            return {'FINISHED'}

        #disable other materials
        for material in bpy.data.materials:
            if material.name == obj.active_material.name:
                continue
            if material.use_nodes:
                # Get the node tree of the material
                nodes = material.node_tree.nodes
                
                # Loop through all nodes in the material
                for node in nodes:
                    # Exclude output nodes
                    if not node.name == 'Material Output':
                        if node.mute == False:
                            node.mute = True
                        else:
                            node.mute = False

        original_render_engine = bpy.context.scene.render.engine
        if original_render_engine != 'CYCLES':
            bpy.context.scene.render.engine = 'CYCLES'

        bpy.context.scene.cycles.samples = 2

        # Get the active material
        material = obj.active_material
        if not material:
            raise ValueError("The active object does not have a material.")

        # Get the node tree of the material
        node_tree = material.node_tree

        diffuse_light_group = None
        for node in node_tree.nodes:
            if node.type == 'GROUP' and (node.node_tree.name.startswith("TransparentNoise") or node.node_tree.name.startswith("TransparentWorld")):
                diffuse_light_group = node
                break

        #math maximize trick----
        node1 = node_tree.nodes.get("Base Color")
        noiselist = []
        maxlist = []
        index = 0
        while node1:
            if (node1.type == 'GROUP' and node1.node_tree.name.startswith("TransparentNoise")) or (node1.type == 'GROUP' and node1.node_tree.name.startswith("TransparentNoise")):
                noiselist.append(node1)
                index += 1
                if index > 1:
                    math_node = node_tree.nodes.new(type='ShaderNodeMath')
                    math_node.operation = 'MAXIMUM'
                    math_node.name = f"Max #{index-1}"
                    maxlist.append(math_node)
                    #set 'diffuse light group' to be whatever the final mathnode is. 'diffuse light group' was normally what we were using as the thing that gets connected to the diffuse bsdf bake node
                    diffuse_light_group = math_node
                    if index == 2:
                        node_tree.links.new(math_node.inputs[0], node1.outputs['Result'])
                        node_tree.links.new(math_node.inputs[1], noiselist[0].outputs['Result'])
                    if index > 2:
                        node_tree.links.new(math_node.inputs[1], node1.outputs['Result'])
                        node_tree.links.new(maxlist[index-3].outputs[0], math_node.inputs[0])
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break
        

        #link stuff up
        
        

        #what does this even do??
        # diffuse_bsdf_node = None
        # for node in diffuse_light_group.node_tree.nodes:
        #     if node.name == 'Visibility':
        #         diffuse_bsdf_node = node
        #         break
        
        material_output_node = None
        current_output_node = None
        for node in node_tree.nodes:
            if node.name == 'Material Output':
                material_output_node = node
                for link in node.inputs['Surface'].links:
                    current_output_node = link.from_node
                break
        
        nodes = node_tree.nodes
        #Add the "bsdf" node to the material
        joekasou = nodes.new(type='ShaderNodeBsdfDiffuse')
        diffuse_node = joekasou

        node_tree = material.node_tree
        links = node_tree.links

        incoming_link = None
        for link in links:
            if link.to_node == material_output_node:
                incoming_link = link
                break


        #check if we have one or multiple transparent noise nodes. if we have multiple, its the max node
        if diffuse_light_group.type == 'GROUP':
            links.new(diffuse_light_group.outputs['Result'], diffuse_node.inputs[0])
        else:
            links.new(diffuse_light_group.outputs[0], diffuse_node.inputs[0])
        links.new(diffuse_node.outputs[0], material_output_node.inputs[0])


        image_texture_node = node_tree.nodes.new('ShaderNodeTexImage')

        tempimage = bpy.data.images.get(f"{bpy.context.scene.bake_name} - Alpha Frame #{bpy.context.scene.frame_current}")
        if tempimage is not None:
            tempimage.user_clear()
            bpy.data.images.remove(tempimage)

        new_image = bpy.data.images.new(f"{bpy.context.scene.bake_name} - Alpha Frame #{bpy.context.scene.frame_current}", width=bpy.context.scene.user_input_number, height=bpy.context.scene.user_input_number)
        image_texture_node.image = new_image
        image_texture_node.image.use_fake_user = True

        bpy.context.view_layer.objects.active = obj
        bpy.context.object.active_material.node_tree.nodes.active = image_texture_node

        bpy.context.scene.cycles.bake_type = 'DIFFUSE'
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False
        bpy.context.scene.render.bake.use_pass_color = True

        # Bake the texture
        bpy.ops.object.bake(type='DIFFUSE')

        # image_texture_node_group = node_tree.nodes.new('ShaderNodeTexImage')
        # image_texture_node_group.image = new_image
        # image_texture_node_group.name = "BakeAlpha"
        obj.active_material.node_tree.nodes.remove(image_texture_node)


        # Restore the original node connected to the material output
        if current_output_node:
            node_tree.links.new(current_output_node.outputs[0], material_output_node.inputs['Surface'])

        material.node_tree.nodes.remove(diffuse_node)
        for node in material.node_tree.nodes:
            if node.name.startswith("Max #"):
                material.node_tree.nodes.remove(node)

        if original_render_engine != 'CYCLES':
            bpy.context.scene.render.engine = original_render_engine

        #re enable all other materials.
        for material in bpy.data.materials:
            if material.name == obj.active_material.name:
                continue
            if material.use_nodes:
                # Get the node tree of the material
                nodes = material.node_tree.nodes
                
                # Loop through all nodes in the material
                for node in nodes:
                    # Exclude output nodes
                    if not node.name == 'Material Output':
                        if node.mute == False:
                            node.mute = True
                        else:
                            node.mute = False

        try:
            bpy.ops.image.save_all_modified()
        except:
            joe = 'KAsoutis'

        return {'FINISHED'}


#BakingEEVEE test



#Remove material
class DeleteMaterial(bpy.types.Operator):
    bl_idname = "shaderaddon.deletematerial"
    bl_label = "删除/移除着色器"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        if not obj.active_material:
            return {'FINISHED'}

        material = obj.active_material
        nodes = material.node_tree.nodes

        #handle empties and delete them for Rectangular Gradients
        for node in nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("LocalGradient"):
                delobj = node.node_tree.nodes["ZhaTexture Coordinate"].object
                if delobj is None:
                    continue

                delobj.hide_viewport = False
                delobj.hide_set(False)

                bpy.ops.object.select_all(action="DESELECT")
                try:
                    delobj.select_set(True)
                except:
                    continue
                bpy.context.view_layer.objects.active = delobj
                try:
                    bpy.context.view_layer.objects.active = delobj
                except:
                    break
                if bpy.context.active_object.name == delobj.name:
                    bpy.ops.object.delete()
            elif node.type == 'GROUP' and node.node_tree.name.startswith("ColoredCircular"):
                delobj = node.node_tree.nodes["ZhaTexture Coordinate"].object
                if delobj is None:
                    continue

                delobj.hide_viewport = False
                delobj.hide_set(False)

                bpy.ops.object.select_all(action="DESELECT")
                try:
                    delobj.select_set(True)
                except:
                    continue
                bpy.context.view_layer.objects.active = delobj
                try:
                    bpy.context.view_layer.objects.active = delobj
                except:
                    break
                if bpy.context.active_object.name == delobj.name:
                    bpy.ops.object.delete()
            elif node.type == 'GROUP' and node.node_tree.name.startswith("NoiseTexture"):
                delobj = node.node_tree.nodes["ZhaTexture Coordinate"].object
                if delobj is None:
                    continue

                delobj.hide_viewport = False
                delobj.hide_set(False)

                bpy.ops.object.select_all(action="DESELECT")
                try:
                    delobj.select_set(True)
                except:
                    continue
                bpy.context.view_layer.objects.active = delobj
                try:
                    bpy.context.view_layer.objects.active = delobj
                except:
                    break
                if bpy.context.active_object.name == delobj.name:
                    bpy.ops.object.delete()
            elif node.type == 'GROUP' and node.node_tree.name.startswith("TransparentNoiseTexture"):
                delobj = node.node_tree.nodes["ZhaTexture Coordinate"].object
                if delobj is None:
                    continue

                delobj.hide_viewport = False
                delobj.hide_set(False)

                bpy.ops.object.select_all(action="DESELECT")
                try:
                    delobj.select_set(True)
                except:
                    continue
                bpy.context.view_layer.objects.active = delobj
                try:
                    bpy.context.view_layer.objects.active = delobj
                except:
                    break
                if bpy.context.active_object.name == delobj.name:
                    bpy.ops.object.delete()


        #handle empties and delete them for Circular Lighting
        for node in nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("CircularLight"):
                delobj = node.node_tree.nodes["ZhaTexture Coordinate"].object
                if delobj is None:
                    continue

                delobj.hide_viewport = False
                delobj.hide_set(False)

                bpy.ops.object.select_all(action="DESELECT")
                try:
                    delobj.select_set(True)
                except:
                    continue
                bpy.context.view_layer.objects.active = delobj
                try:
                    bpy.context.view_layer.objects.active = delobj
                except:
                    break
                if bpy.context.active_object.name == delobj.name:
                    bpy.ops.object.delete()

        #handle fakelight
        for modifier in obj.modifiers:
            if modifier.type == 'NODES' and modifier.name.startswith("SB Geono"):
                delobj = modifier.node_group.nodes["Object Info"].inputs[0].default_value
                if delobj is None:
                    continue

                #check if any other objects are using this fakelight sphere
                timetobreak = False
                for objeto in bpy.data.objects:
                    if objeto == obj:
                        continue
                    if objeto.active_material and objeto.active_material == obj.active_material:
                        continue
                    if objeto.modifiers:
                        for mod in objeto.modifiers:
                            if mod.type == 'NODES' and mod.name.startswith("SB Geono"):
                                if mod.node_group.nodes["Object Info"].inputs[0].default_value == delobj:
                                    timetobreak = True

                if timetobreak:
                    continue

                delobj.hide_viewport = False
                delobj.hide_set(False)

                bpy.ops.object.select_all(action="DESELECT")
                try:
                    delobj.select_set(True)
                except:
                    continue
                bpy.context.view_layer.objects.active = delobj
                try:
                    bpy.context.view_layer.objects.active = delobj
                except:
                    break
                if bpy.context.active_object.name == delobj.name:
                    bpy.ops.object.delete()

        for modifier in obj.modifiers:
            if modifier.type == 'NODES' and modifier.name.startswith("SB") and not material.name.startswith("Outline for"):
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_remove(modifier=modifier.name)

        #handle solidify outline
        for node in nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("basecolor_solidify"):
                for modifier in obj.modifiers:
                    if modifier.name.startswith("SB Outline"):
                        obj.select_set(True)
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.modifier_remove(modifier=modifier.name)
                        break




        if obj and obj.active_material:
            material_name = obj.active_material.name
            # Unlink the material from the object
            obj.active_material = None
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.material_slot_remove()
        
            # Delete the material from bpy.data.materials
        if material_name in bpy.data.materials:
            #bpy.data.materials.remove(bpy.data.materials[material_name])
            print(f"Material '{material_name}' deleted.")
        else:
            print("No active object or no material found.")


        
        return {'FINISHED'}

class OpenURLOperator(bpy.types.Operator):
    bl_idname = "shaderaddon.opensite"
    bl_label = "打开URL"
    
    
    def execute(self, context):
        webbrowser.open('https://space.bilibili.com/3546571046128187?spm_id_from=333.1007.0.0')
        return {'FINISHED'}

class SwapNodes(bpy.types.Operator):
    bl_idname = "shaderaddon.swapnodesold"
    bl_label = "交换两个节点的位置"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        node1 = nodes.get(obj.node_groups_enum_swap2)
        node2 = nodes.get(obj.node_groups_enum_swap1)

        if node1.node_tree.name.startswith("Transparent") or node2.node_tree.name.startswith("Transparent"):
            return {'FINISHED'}

        if node1 == node2:
            return {'FINISHED'}

        node1name = nodes.get(obj.node_groups_enum_swap2).name
        node2name = nodes.get(obj.node_groups_enum_swap1).name

        node1inputs = []
        node2inputs = []

        try:
            for index, input in enumerate(node1.inputs, start=1):
                if index == len(node1.inputs):
                    break
                node1inputs.append(node1.inputs[index].default_value)
            
            for index, input in enumerate(node2.inputs, start=1):
                if index == len(node2.inputs):
                    break
                node2inputs.append(node2.inputs[index].default_value)
        except:
            joe = "kasou"

        temptree = node1.node_tree
        tempname = node1name

        node2.name = "timmytimmytimmyturner"
        node1.name = node2name
        node1.node_tree = node2.node_tree

        node2.name = tempname
        node2.node_tree = temptree

        try:
            for index, input in enumerate(node1.inputs, start=1):
                if index == len(node1.inputs):
                    break
                node1.inputs[index].default_value = node2inputs[index-1]

            for index, input in enumerate(node2.inputs, start=1):
                if index == len(node2.inputs):
                    break
                node2.inputs[index].default_value = node1inputs[index-1]
        except:
            joe = "kasou"

        timer_function()

        return {'FINISHED'}
        

class SwapNodes2(bpy.types.Operator):
    bl_idname = "shaderaddon.swapnodes"
    bl_label = "交换两个节点的位置"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        node1 = nodes.get(obj.node_groups_enum_swap1)
        node2 = nodes.get(obj.node_groups_enum_swap2)

        if node1.node_tree.name.startswith('RedL') or node2.node_tree.name.startswith('RedL') or node1.node_tree.name.startswith('GreenL') or node2.node_tree.name.startswith('GreenL') or node1.node_tree.name.startswith('BlueL') or node2.node_tree.name.startswith('BlueL'):
            trav = nodes.get('Base Color')
            seenDiffuse = False
            while trav:
                if trav == node1 or trav == node2:
                    if not seenDiffuse:
                        return {'FINISHED'}
                    else:
                        break
                else:
                    if trav.node_tree.name.startswith('DiffuseL'):
                        seenDiffuse = True
                    if trav.outputs and trav.outputs[0].is_linked:
                        trav = trav.outputs[0].links[0].to_node
                    else:
                        break

        if node1.node_tree.name.startswith("Transparent"):
            if node2.node_tree.name.startswith("Transparent"):
                print("do nothing")
            else:
                return {'FINISHED'}
        if node2.node_tree.name.startswith("Transparent"):
            if node1.node_tree.name.startswith("Transparent"):
                print("do nothing")
            else:
                return {'FINISHED'}

        if node1 == node2:
            return {'FINISHED'}


        links = obj.active_material.node_tree.links

        adjacent = False
        adjacentNode = None
        if node1.outputs[0].is_linked and node1.outputs[0].links[0].to_node == node2:
            adjacent = True
            adjacentNode = node1
            secondNode = node2
        if node2.outputs[0].is_linked and node2.outputs[0].links[0].to_node == node1:
            adjacent = True
            adjacentNode = node2
            secondNode = node1

        node1locationtemp = node1.location.copy()
        node1.location = node2.location
        node2.location = node1locationtemp
        #swap adjacent nodes
        if adjacent:
            adjacent_input_link = adjacentNode.inputs[0].links[0].from_socket
            adjacentPrev = adjacentNode.inputs[0].links[0].from_node
            secondNext = secondNode.outputs[0].links[0].to_node
            links.new(secondNode.outputs[0], adjacentNode.inputs[0])
            links.new(adjacentPrev.outputs[0], secondNode.inputs[0])
            links.new(adjacentNode.outputs[0], secondNext.inputs[0])
            
        if adjacent == False:
            node1Prev = node1.inputs[0].links[0].from_node
            node1Next = node1.outputs[0].links[0].to_node
            node2Prev = node2.inputs[0].links[0].from_node
            node2Next = node2.outputs[0].links[0].to_node
            links.new(node2Prev.outputs[0], node1.inputs[0])
            links.new(node1.outputs[0], node2Next.inputs[0])
            links.new(node2.inputs[0], node1Prev.outputs[0])
            links.new(node2.outputs[0], node1Next.inputs[0])
        

        timer_function()

        return {'FINISHED'}


class DeleteEffect(bpy.types.Operator):
    bl_idname = "shaderaddon.deleteeffect"
    bl_label = "删除一个效果"

    arg1: bpy.props.StringProperty(name="Argument 1", default="Hello")

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        mat = obj.active_material

        if mat.name.startswith("Outline for"):
            bpy.ops.shaderaddon.deletematerial()
            return {'FINISHED'}

        if mat and mat.use_nodes:
            node_tree = mat.node_tree
            #get the enum value for deleting the object
            if self.arg1 == 'Hello':
                node_name = obj.node_groups_enum
            else:
                try:
                    node_name = self.arg1
                except:
                    node_name = obj.node_groups_enum

            # node_name = obj.node_groups_enum
            if node_name.startswith("SB Disp"):
                to_remove = obj.modifiers.get(node_name)
                object_to_delete = to_remove.texture_coords_object
                try: 
                    object_to_delete.hide_viewport = False
                    object_to_delete.hide_set(False)
                    bpy.ops.object.select_all(action="DESELECT")
                    object_to_delete.select_set(True)
                    bpy.context.view_layer.objects.active = object_to_delete
                    bpy.ops.object.delete()
                except:
                    joe = "kasou"
                obj.modifiers.remove(to_remove)
                return {'FINISHED'}
            if node_name.startswith("SB Out"):
                to_remove = obj.modifiers.get(node_name)
                obj.modifiers.remove(to_remove)
                return {'FINISHED'}
            node_to_delete = node_tree.nodes.get(node_name)

            if node_to_delete:
                # Store links to be reconnected
                input_link = node_to_delete.inputs[0].links[0].from_socket if node_to_delete.inputs[0].is_linked else None
                output_link = node_to_delete.outputs[0].links[0].to_socket if node_to_delete.outputs[0].is_linked else None
                
                # Remove any associated empties (fakelights), rename fakelight nodes
                if node_to_delete.node_tree.name.startswith("LightObject"):
                    # last_character = node_to_delete.name[-1]
                    # number = int(last_character)
                    for modifier in obj.modifiers:
                        if modifier.name.startswith("SB Geono"):
                            if node_to_delete.node_tree.nodes["Attribute"].attribute_name != modifier.node_group.nodes["Store Named Attribute"].inputs[2].default_value:
                                continue
                            number = 0
                            if number == 0:
                                delobj = modifier.node_group.nodes["Object Info"].inputs[0].default_value
                                #check if theres any other objects using the empty sphere
                                flag = True
                                remove_from_all_list = []
                                for objeto in bpy.data.objects:
                                    if objeto == obj:
                                        continue
                                    if objeto.modifiers:
                                        for mod in objeto.modifiers:
                                            if mod.type == 'NODES' and mod.name.startswith("SB Geono") and obj.active_material != objeto.active_material:
                                                if mod.node_group.nodes["Object Info"].inputs[0].default_value == delobj:
                                                    flag = False
                                            if mod.type == 'NODES' and mod.name.startswith("SB Geono") and obj.active_material == objeto.active_material:
                                                remove_from_all_list.append(objeto)
                                if flag:
                                    if delobj is not None:
                                        try:
                                            delobj.hide_viewport = False
                                            delobj.hide_set(False)
                                            bpy.ops.object.select_all(action="DESELECT")
                                            delobj.select_set(True)
                                            bpy.context.view_layer.objects.active = delobj
                                            if bpy.context.active_object.name == delobj.name:
                                                bpy.ops.object.delete()
                                        except:
                                            joe = "kasou"
                                for removable in remove_from_all_list:
                                    removable.select_set(True)
                                    bpy.context.view_layer.objects.active = removable
                                    bpy.ops.object.modifier_remove(modifier=modifier.name)
                                    
                                obj.select_set(True)
                                bpy.context.view_layer.objects.active = obj
                                bpy.ops.object.modifier_remove(modifier=modifier.name)
                                #rename fakelight nodes -- this style could be problematic now that i switched the menu compilation to a while(node)
                                light_object_count = 1
                                for node in obj.active_material.node_tree.nodes:
                                    if node.type == 'GROUP' and node.node_tree.name.startswith("LightObject"):
                                        node.name = f"Light Object #{light_object_count}"
                                        light_object_count += 1
                
                #Remove modifiers for sunobject
                if node_to_delete.node_tree.name.startswith("SunObject"):
                    # last_character = node_to_delete.name[-1]
                    # number = int(last_character)
                    for modifier in obj.modifiers:
                        if modifier.name.startswith("SB Sun"):
                            if node_to_delete.node_tree.nodes["Attribute"].attribute_name != modifier.node_group.nodes["Store Named Attribute"].inputs[2].default_value:
                                continue
                            number = 0
                            if number == 0:
                                obj.select_set(True)
                                bpy.context.view_layer.objects.active = obj
                                bpy.ops.object.modifier_remove(modifier=modifier.name)
                                #rename fakelight nodes
                                light_object_count = 1
                                for node in obj.active_material.node_tree.nodes:
                                    if node.type == 'GROUP' and node.node_tree.name.startswith("SunObject"):
                                        node.name = f"Baked Sun Light #{light_object_count}"
                                        light_object_count += 1
                


                # Remove any associated empties (everything except fakelights) -- if ur adding a new effect with empty just set text to "zhatexturecoordinate"
                for node in node_to_delete.node_tree.nodes:
                    if node.name == "ZhaTexture Coordinate":
                        delobj = node.object
                        if delobj is None:
                            continue

                        delobj.hide_viewport = False
                        delobj.hide_set(False)

                        bpy.ops.object.select_all(action="DESELECT")
                        try:
                            delobj.select_set(True)
                        except:
                            continue
                        bpy.context.view_layer.objects.active = delobj
                        try:
                            bpy.context.view_layer.objects.active = delobj
                        except:
                            break
                        if bpy.context.active_object.name == delobj.name:
                            bpy.ops.object.delete()
                


                # Remove the node group
                node_tree.nodes.remove(node_to_delete)

                # Reconnect links
                if input_link and output_link:
                    node_tree.links.new(input_link, output_link)

                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                #update counts for transparent nodes
                tp_count = 1
                tn_count = 1
                for node in obj.active_material.node_tree.nodes:
                    if node.type == 'GROUP' and node.node_tree.name.startswith("TransparentPaint"):
                        node.name = f"Charcoal/Watercolor #{tp_count}"
                        tp_count += 1
                    if node.type == 'GROUP' and node.node_tree.name.startswith("TransparentNoi"):
                        node.name = f"Transparent Dynamic Texture #{tn_count}"
                        tn_count += 1

                #setup enums for the view and delete effects
                newlist = []
                newlistview = []
                newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

                for node in node_tree.nodes:
                    if node.name == "Base Color":
                        newlistview.append((node.name, node.name, ""))
                        continue
                    if node.type == 'GROUP':
                        newlist.append((node.name, node.name, ""))
                        newlistview.append((node.name, node.name, ""))
                bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
                    name="Node Groups",
                    description = "节点组列表",
                    items = newlist
                )
                # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
                #     name="Node Groups View",
                #     description = "节点组列表 for effect viewer",
                #     items = newlistview
                # )
                bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
                    name="Node Groups",
                    description = "节点组列表",
                    items = newlist
                )

        timer_function()

        return {'FINISHED'}


class RefreshMaterial(bpy.types.Operator):
    bl_idname = "shaderaddon.refreshmaterial"
    bl_label = "刷新材质"

    def execute(self, context):
        try:
            bpy.app.timers.unregister(timer_function)
        except:
            joe = "kasou"
        
        bpy.app.timers.register(timer_function)

        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}
        


class AddTransparentPaint(bpy.types.Operator):
    bl_idname = "shaderaddon.addtransparentpaint"
    bl_label = "添加水彩/炭笔效果"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        material.blend_method = 'HASHED'
        material.show_transparent_back = False

        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return
        
        # Create the "TransparentPaint" node group
        transparent_paint_group = bpy.data.node_groups.get("TransparentPaint")
        if not transparent_paint_group:
            print("Node group 'Transparent Paint' not found.")
            return
        
        # Add the "TransparentPaint" node to the material
        output_node.location.x += 400
        joekasou = transparent_paint_group.copy()
        transparent_paint_node = nodes.new(type='ShaderNodeGroup')
        transparent_paint_node.node_tree = joekasou
        transparent_paint_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], transparent_paint_node.inputs[0])
        links.new(transparent_paint_node.outputs[0], output_node.inputs[0])

        print("Transparent Paint Node node group added and connected.")

        output_node.location.x += 200

        tp_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("TransparentPaint"):
                node.name = f"Charcoal/Watercolor #{tp_count}"
                tp_count += 1
        
        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}




class SaveImageTextures(bpy.types.Operator):
    bl_idname = "shaderaddon.saveimagetextures"
    bl_label = "外部保存图像纹理"

    def execute(self, context):

        for image in bpy.data.images:
            try:
                if image.name.startswith(f"{bpy.context.scene.bake_name}") and not image.name.endswith("Diffuse") and not image.name.endswith("AO") and not image.name.endswith("Specular"):
                    bpy.ops.file.unpack_item(method='WRITE_LOCAL', id_name=f"{image.name}", id_type=19785)
                    # image.use_fake_user = False
            except:
                joe = 'kasoutis'

        return {'FINISHED'}







class AddOverallTexture(bpy.types.Operator):
    bl_idname = "shaderaddon.addoveralltexture"
    bl_label = "添加一个整体纹理作为覆盖"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "OverallTexture" node group
        overall_texture_group = bpy.data.node_groups.get("OverallTexture")
        if not overall_texture_group:
            print("Node group 'Overall Texture' not found.")
            return
        
        # Add the "TransparentPaint" node to the material
        output_node.location.x += 400
        joekasou = overall_texture_group.copy()
        overall_texture_node = nodes.new(type='ShaderNodeGroup')
        overall_texture_node.node_tree = joekasou
        overall_texture_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], overall_texture_node.inputs[0])
        links.new(overall_texture_node.outputs[0], output_node.inputs[0])

        print("Texture Paint Node node group added and connected.")

        output_node.location.x += 200

        overall_texture_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("OverallTexture"):
                node.name = f"Texture Overlay #{overall_texture_count}"
                overall_texture_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )


        return {'FINISHED'}


class AddVertexPaint(bpy.types.Operator):
    bl_idname = "shaderaddon.addvertexpaint"
    bl_label = "添加顶点绘画节点"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "VertexPaint" node group
        vertex_paint_group = bpy.data.node_groups.get("VertexPaint")
        if not vertex_paint_group:
            print("Node group 'Vertex Paint' not found.")
            return
        
        # Add the "TransparentPaint" node to the material
        output_node.location.x += 400
        joekasou = vertex_paint_group.copy()
        vertex_paint_node = nodes.new(type='ShaderNodeGroup')
        vertex_paint_node.node_tree = joekasou
        vertex_paint_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], vertex_paint_node.inputs[0])
        links.new(vertex_paint_node.outputs[0], output_node.inputs[0])

        print("vertex Paint Node node group added and connected.")

        output_node.location.x += 200

        vertex_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("VertexPaint"):
                node.name = f"Vertex Paint #{vertex_count}"
                vertex_count += 1


        #handle enums (not necessary because now we have a timer function)
        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )


        return {'FINISHED'}


class AddSingleColor(bpy.types.Operator):
    bl_idname = "shaderaddon.addsinglecolor"
    bl_label = "用单一颜色绘制/绘画"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "SingleColor" node group
        texture_paint_group = bpy.data.node_groups.get("SingleColor")
        if not texture_paint_group:
            print("Node group 'Texture Paint' not found.")
            return
        
        # Add the "TransparentPaint" node to the material
        output_node.location.x += 400
        joekasou = texture_paint_group.copy()
        texture_paint_node = nodes.new(type='ShaderNodeGroup')
        texture_paint_node.node_tree = joekasou
        texture_paint_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], texture_paint_node.inputs[0])
        links.new(texture_paint_node.outputs[0], output_node.inputs[0])

        print("Texture Paint Node node group added and connected.")

        output_node.location.x += 200

        texture_paint_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("SingleColor"):
                node.name = f"Texture Paint (1 Color) #{texture_paint_count}"
                texture_paint_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )


        return {'FINISHED'}

class DuplicateEffect(bpy.types.Operator):
    bl_idname = "shaderaddon.duplicateeffect"
    bl_label = "复制效果"
    
    
    arg1: bpy.props.StringProperty(name="Argument 1", default="Hello")

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return {'FINISHED'}


        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        node_name = self.arg1
        if self.arg1 == 'Hello':
            node_name = obj.node_groups_enum
        else:
            try:
                node_name = self.arg1
            except:
                node_name = obj.node_groups_enum

        duplicate_group = nodes.get(node_name).node_tree
        if duplicate_group.name.startswith("Diffuse"):
            return {'FINISHED'}
        if duplicate_group.name.startswith("LightObject"):
            return {'FINISHED'}
        if duplicate_group.name.startswith("SunObject"):
            return {'FINISHED'}
        if duplicate_group.name.startswith("CrossHatch"):
            return {'FINISHED'}
        if duplicate_group.name.startswith("SpecularRef"):
            return {'FINISHED'}

        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        for node in nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("Transparent"):
                output_node = node

        if not output_node:
            print("No Material Output node found.")
            return {'FINISHED'}

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return {'FINISHED'}

        

        # Duplicate the selected node group
        duplicate_group = nodes.get(obj.duplicate_group_enum).node_tree


        if not duplicate_group:
            print("Node group not found.")
            return {'FINISHED'}

        # Add the "TransparentPaint" node to the material
        output_node.location.x += 400
        joekasou = duplicate_group.copy()
        duplicate_node = nodes.new(type='ShaderNodeGroup')
        duplicate_node.node_tree = joekasou
        duplicate_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], duplicate_node.inputs[0])
        links.new(duplicate_node.outputs[0], output_node.inputs[0])

        print("Texture Paint Node node group added and connected.")

        output_node.location.x += 200


        #rename
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name == duplicate_node.node_tree.name:
                node.name = f"{obj.duplicate_group_enum} Duplicate"

        for node in duplicate_node.node_tree.nodes:
            if node.name == 'ZhaTexture Coordinate':
                if node.object is None:
                    random_offset_x = random.uniform(-5, 5)
                    random_offset_y = random.uniform(-5, 5)
                    random_offset_z = random.uniform(0, 2)

                    bpy.ops.object.empty_add(type='SPHERE')
                    emptysphere = bpy.context.object
                    emptysphere.location.x += random_offset_x
                    emptysphere.location.y += random_offset_y
                    emptysphere.location.z += random_offset_z
                    emptysphere.name = "SB " + f"{duplicate_node.name} " + f"{obj.name}"
                    emptysphere.parent = obj
                else:
                    bpy.ops.object.empty_add(type='SPHERE')
                    emptysphere = bpy.context.object
                    emptysphere.location = node.object.location
                    emptysphere.scale = node.object.scale
                    emptysphere.rotation_quaternion = node.object.rotation_quaternion
                    emptysphere.name = "SB " + f"{duplicate_node.name} " + f"{obj.name}"
                    emptysphere.parent = obj

                duplicate_node.node_tree.nodes["ZhaTexture Coordinate"].object = emptysphere


        #transfer inputs

        node1inputs = []
        node2inputs = []

        node1 = nodes.get(obj.duplicate_group_enum)
        node2 = duplicate_node
        try:
            for index, input in enumerate(node1.inputs, start=1):
                if index == len(node1.inputs):
                    break
                node1inputs.append(node1.inputs[index].default_value)
                node2.inputs[index].default_value = node1.inputs[index].default_value
            
            for index, input in enumerate(node2.inputs, start=1):
                if index == len(node2.inputs):
                    break
                node2inputs.append(node2.inputs[index].default_value)
        except:
            joe = "kasou"

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )


        return {'FINISHED'}

class NormalsPaint(bpy.types.Operator):
    bl_idname = "shaderaddon.normalspaint"
    bl_label = "法线绘画"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
            
        diffusenode = nodes.get('NormalsTextureHelper')
        if not diffusenode:
            return {'FINISHED'}


        node_before_output = output_node.inputs['Surface'].links[0].from_node

        if bpy.context.mode != 'PAINT_TEXTURE' and nodes.get('TempTemp') is None:
            bpy.ops.object.mode_set(mode='TEXTURE_PAINT')

            for i, slot in enumerate(material.texture_paint_images):
                if slot.name == nodes.get('NormalsTextureHelper').image.name:
                    material.paint_active_slot = i
                    print(f"Set paint active slot to")

            links.new(diffusenode.outputs[0], output_node.inputs['Surface'])
            math_node = nodes.new('ShaderNodeMath')
            math_node.name = 'TempTemp'
            math_node.label = node_before_output.name
        elif bpy.context.mode != 'PAINT_TEXTURE' and nodes.get('TempTemp') is not None:
            math_node = nodes.get('TempTemp')
            links.new(nodes.get(math_node.label).outputs[0], output_node.inputs['Surface'])
            nodes.remove(math_node)
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            
            math_node = nodes.get('TempTemp')
            links.new(nodes.get(math_node.label).outputs[0], output_node.inputs['Surface'])
            nodes.remove(math_node)
            

        

        return {'FINISHED'}

class AddBrushStrokes(bpy.types.Operator):
    bl_idname = "shaderaddon.addbrushstrokes"
    bl_label = "添加动态笔触效果节点"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "TexturePaint" node group
        texture_paint_group = bpy.data.node_groups.get("BrushStrokes")
        if not texture_paint_group:
            print("Node group 'Texture Paint' not found.")
            return
        
        # Add the "TransparentPaint" node to the material
        output_node.location.x += 400
        joekasou = texture_paint_group.copy()
        texture_paint_node = nodes.new(type='ShaderNodeGroup')
        texture_paint_node.node_tree = joekasou
        texture_paint_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], texture_paint_node.inputs[0])
        links.new(texture_paint_node.outputs[0], output_node.inputs[0])

        print("Texture Paint Node node group added and connected.")

        output_node.location.x += 200

        texture_paint_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("BrushStrokes"):
                node.name = f"Brush Strokes #{texture_paint_count}"
                texture_paint_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}

class AddObjectRandomize(bpy.types.Operator):
    bl_idname = "shaderaddon.addobjectrandomize"
    bl_label = "添加对象随机化节点"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return
        
        # Create the "TexturePaint" node group
        texture_paint_group = bpy.data.node_groups.get("ObjectRandomize")
        if not texture_paint_group:
            print("Node group 'Texture Paint' not found.")
            return
        
        # Add the "TransparentPaint" node to the material
        output_node.location.x += 400
        joekasou = texture_paint_group.copy()
        texture_paint_node = nodes.new(type='ShaderNodeGroup')
        texture_paint_node.node_tree = joekasou
        texture_paint_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], texture_paint_node.inputs[0])
        links.new(texture_paint_node.outputs[0], output_node.inputs[0])

        print("Texture Paint Node node group added and connected.")

        output_node.location.x += 200

        texture_paint_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("ObjectRandomize"):
                node.name = f"Object Randomize #{texture_paint_count}"
                texture_paint_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )


        return {'FINISHED'}

class AddRGBCurves(bpy.types.Operator):
    bl_idname = "shaderaddon.addrgbcurves"
    bl_label = "添加对比度节点"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return
        
        # Create the "TexturePaint" node group
        texture_paint_group = bpy.data.node_groups.get("RGBContrast")
        if not texture_paint_group:
            print("Node group 'Texture Paint' not found.")
            return
        
        # Add the "TransparentPaint" node to the material
        output_node.location.x += 400
        joekasou = texture_paint_group.copy()
        texture_paint_node = nodes.new(type='ShaderNodeGroup')
        texture_paint_node.node_tree = joekasou
        texture_paint_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], texture_paint_node.inputs[0])
        links.new(texture_paint_node.outputs[0], output_node.inputs[0])

        print("Texture Paint Node node group added and connected.")

        output_node.location.x += 200

        texture_paint_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("RGBContrast"):
                node.name = f"Contrast #{texture_paint_count}"
                texture_paint_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )


        return {'FINISHED'}

class ExternalPaint(bpy.types.Operator):
    bl_idname = "shaderaddon.externalpaint"
    bl_label = "外部绘画"
    
    arg1: bpy.props.StringProperty(name="Argument 1", default="none")
    
    def execute(self, context):
        import bpy

        # Switch to Texture Paint mode
        bpy.ops.object.mode_set(mode='TEXTURE_PAINT')

        material = bpy.context.object.active_material
        node_tree = material.node_tree

        # for node in node_tree.nodes:
        #     # Check if node is a group
        #     if node.type == 'GROUP':
        #         # Check if node group name starts with "TexturePaint"
        #         if node.node_tree.name.startswith("TexturePaint"):
        #             node.node_tree.nodes["Main"].select = True
        #             node.node_tree.nodes.active = node.node_tree.nodes['Main']
        
        for i, slot in enumerate(material.texture_paint_images):
            if slot.name == self.arg1:
                material.paint_active_slot = i
                print(f"Set paint active slot to")
                    
        bpy.ops.image.project_edit()
        
        return {'FINISHED'}

class AddTexturePaint(bpy.types.Operator):
    bl_idname = "shaderaddon.addtexturepaint"
    bl_label = "添加绘画/纹理绘画节点"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return
        
        # Create the "TexturePaint" node group
        texture_paint_group = bpy.data.node_groups.get("TexturePaint")
        if not texture_paint_group:
            print("Node group 'Texture Paint' not found.")
            return
        
        # Add the "TransparentPaint" node to the material
        output_node.location.x += 400
        joekasou = texture_paint_group.copy()
        texture_paint_node = nodes.new(type='ShaderNodeGroup')
        texture_paint_node.node_tree = joekasou
        texture_paint_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], texture_paint_node.inputs[0])
        links.new(texture_paint_node.outputs[0], output_node.inputs[0])

        print("Texture Paint Node node group added and connected.")

        output_node.location.x += 200

        texture_paint_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("TexturePaint"):
                node.name = f"Texture Paint #{texture_paint_count}"
                texture_paint_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )


        return {'FINISHED'}



class AddSolidifyOutline(bpy.types.Operator):
    bl_idname = "shaderaddon.addsolidifyoutline"
    bl_label = "添加实体轮廓"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj:
            print("No active object or no material with nodes found.")
            return {'FINISHED'}
        

        outlinematerial = bpy.data.materials.get("solidifyoutline")
        if not outlinematerial:
            return

        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        duplicate_material = outlinematerial.copy()
        duplicate_material.name = f"Outline for {obj.name}"
        temptree = duplicate_material.node_tree.nodes[0].node_tree.copy()
        duplicate_material.node_tree.nodes[0].node_tree = temptree

        obj.data.materials.append(duplicate_material)

        num_slots = len(obj.material_slots)
        obj.active_material_index = num_slots - 1

        for _ in range(num_slots-1):
            bpy.ops.object.material_slot_move(direction='UP')
        
        solidify_modifier = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        solidify_modifier.name = f"SB Outline for {obj.name}"

        solidify_modifier.offset = 1
        solidify_modifier.use_rim = False
        solidify_modifier.use_flip_normals = True
        solidify_modifier.material_offset = -100

        return {'FINISHED'}
        


class AddColoredEdges(bpy.types.Operator):
    bl_idname = "shaderaddon.addcolorededges"
    bl_label = "添加彩色边缘"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        output_node = None
        material_output_reference = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                material_output_reference = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "ColoredEdges" node group
        colored_edges_group = bpy.data.node_groups.get("ColoredEdges")
        if not colored_edges_group:
            print("Node group 'colored edges' not found.")
            return
        
        # Add the "AmbientOcclusion" node to the material
        output_node.location.x += 400
        joekasou = colored_edges_group.copy()
        colored_edges_node = nodes.new(type='ShaderNodeGroup')
        colored_edges_node.node_tree = joekasou
        colored_edges_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], colored_edges_node.inputs[0])
        links.new(colored_edges_node.outputs[0], output_node.inputs[0])

        print("colored edges Node node group added and connected.")

        output_node.location.x += 200

        if output_node.type == 'GROUP' and output_node.node_tree.name.startswith("Transparent"):
            material_output_reference.location.x += 200

        colored_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("ColoredEdges"):
                node.name = f"Colored Edges #{colored_count}"
                colored_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}
        

class AddRedLight(bpy.types.Operator):
    bl_idname = "shaderaddon.addredlight"
    bl_label = "添加一个点光源"

    def execute(self, context):
        edge_detect_group = bpy.data.node_groups.get("RedLightSAS")
        materiallist = []
        curcount = 0
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
            def draw(self, context):
                self.layout.label(text=message)
                
            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
        for obj in bpy.data.objects:
            try:
                if obj.active_material.node_tree.nodes.get("SAS Point Lights Group #1") is not None:
                    curcount += 1
            except:
                continue
        if curcount >= 25:
            ShowMessageBox(message="Max Objects (25) for using the Stylized Point Light Reached. Please Upgrade to Pro or Join the Masterclass on ukiyogirls.io", title="Message Box", icon='INFO')
            return {'FINISHED'}
        objcount = curcount
        for obj in bpy.context.selected_objects:
            # obj = bpy.context.active_object
            if objcount >= 25:
                ShowMessageBox(message="Max Objects (25) for using the Stylized Point Light Reached. Please Upgrade to Pro or Join the Masterclass on ukiyogirls.io", title="Message Box", icon='INFO')
                return {'FINISHED'}

            tempobj = None
            if obj.type == 'EMPTY' and obj.name.startswith("SB"):
                tempobj = obj.parent
                obj = tempobj
            elif obj.type == 'MESH' and obj.name.startswith("SB"):
                tempobj = obj.parent
                obj = tempobj
            
            if not obj or not obj.active_material or not obj.active_material.use_nodes:
                print("No active object or no material with nodes found.")
                return {'FINISHED'}

            material = obj.active_material
            if material in materiallist:
                continue
            else:
                materiallist.append(material)
            
            nodes = material.node_tree.nodes
            links = material.node_tree.links

            if nodes.get('Base Color') is None:
                continue

            #check if theres a stylized light dynamic effect, if not, we have to continue
            if nodes.get('Stylized Light (Dynamic) - #1') is None:
                continue

            falseflag = False
            for node in nodes:
                if node.type == 'GROUP' and node.node_tree.name.startswith("RedLightSAS"):
                    falseflag = True
                    break

            if falseflag:
                continue

            output_node = None
            material_output_reference = None
            for node in nodes:
                if node.type == 'OUTPUT_MATERIAL':
                    output_node = node
                    material_output_reference = node
                    break
            
            node1 = nodes.get("Base Color")
            while node1:
                if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                    output_node = node1
                    break
                if node1.outputs and node1.outputs[0].is_linked:
                    node1 = node1.outputs[0].links[0].to_node
                else:
                    break

            if not output_node:
                print("No Material Output node found.")
                return



            incoming_link = None
            for link in links:
                if link.to_node == output_node:
                    incoming_link = link
                    break

            if not incoming_link:
                print("No link to the Material Output node found.")
                return

            # Create the "HSL" node group
            
            if not edge_detect_group:
                print("Node group 'edge detect' not found.")
                return
            
            # Add the "AmbientOcclusion" node to the material
            output_node.location.x += 400
            joekasou = edge_detect_group
            edge_detect_node = nodes.new(type='ShaderNodeGroup')
            edge_detect_node.node_tree = joekasou
            edge_detect_node.location = (output_node.location.x - 200, output_node.location.y)

            # Connect the new node
            links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], edge_detect_node.inputs[0])
            links.new(edge_detect_node.outputs[0], output_node.inputs[0])

            print("edge detect Node node group added and connected.")

            output_node.location.x += 200

            if output_node.type == 'GROUP' and output_node.node_tree.name.startswith("Transparent"):
                material_output_reference.location.x += 200

            edge_count = 1
            for node in obj.active_material.node_tree.nodes:
                if node.type == 'GROUP' and node.node_tree.name.startswith("RedLightSAS"):
                    node.name = f"SAS Point Lights Group #1"
                    edge_count += 1

            for node in obj.active_material.node_tree.nodes:
                if node.type == 'GROUP' and node.node_tree.name.startswith("DiffuseL"):
                    links.new(node.outputs['Custom'], edge_detect_node.inputs['Vector'])

            #add the point light
            if not 'SAS Point Light Group #1' in bpy.data.objects:
                bpy.ops.object.light_add(type='POINT')
                bpy.context.active_object.data.color = (1, 0, 0)
                bpy.context.active_object.name = 'SAS Point Light Group #1'
            # bpy.context.active_object.data.name = 'sasred'

            #update object count
            objcount += 1

            newlist = []
            newlistview = []
            newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

            for node in obj.active_material.node_tree.nodes:
                if node.name == "Base Color":
                    newlistview.append((node.name, node.name, ""))
                    continue
                if node.type == 'GROUP':
                    newlist.append((node.name, node.name, ""))
                    newlistview.append((node.name, node.name, ""))
            bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
                name="Node Groups",
                description = "节点组列表",
                items = newlist
            )
            # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
            #     name="Node Groups View",
            #     description = "节点组列表 for effect viewer",
            #     items = newlistview
            # )
            bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
                name="Node Groups",
                description = "节点组列表",
                items = newlist
            )
            bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
                name="Node Groups",
                description = "节点组列表",
                items = newlist
            )
            bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
                name="Node Groups",
                description = "节点组列表",
                items = newlist
            )

        return {'FINISHED'}


class AddHSL(bpy.types.Operator):
    bl_idname = "shaderaddon.addhsl"
    bl_label = "添加HSL效果"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        output_node = None
        material_output_reference = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                material_output_reference = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        
        


        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "HSL" node group
        edge_detect_group = bpy.data.node_groups.get("FinalHSL")
        if not edge_detect_group:
            print("Node group 'edge detect' not found.")
            return
        
        # Add the "AmbientOcclusion" node to the material
        output_node.location.x += 400
        joekasou = edge_detect_group.copy()
        edge_detect_node = nodes.new(type='ShaderNodeGroup')
        edge_detect_node.node_tree = joekasou
        edge_detect_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], edge_detect_node.inputs[0])
        links.new(edge_detect_node.outputs[0], output_node.inputs[0])

        print("edge detect Node node group added and connected.")

        output_node.location.x += 200

        if output_node.type == 'GROUP' and output_node.node_tree.name.startswith("Transparent"):
            material_output_reference.location.x += 200

        edge_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("FinalHSL"):
                node.name = f"Hue/Saturation/Value Shift #{edge_count}"
                edge_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddCurvature(bpy.types.Operator):
    bl_idname = "shaderaddon.addcurvature"
    bl_label = "添加HSL效果"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        material_output_reference = None

        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
            def draw(self, context):
                self.layout.label(text=message)
                
            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

        for node in nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("AddCurva"):
                ShowMessageBox("Max 1 Curvature Effect is possible currently", "My Title", 'ERROR')
                return {'FINISHED'}

        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                material_output_reference = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        
        


        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "HSL" node group
        edge_detect_group = bpy.data.node_groups.get("AddCurvature")
        if not edge_detect_group:
            print("Node group 'edge detect' not found.")
            return
        
        # Add the "AmbientOcclusion" node to the material
        output_node.location.x += 400
        joekasou = edge_detect_group.copy()
        edge_detect_node = nodes.new(type='ShaderNodeGroup')
        edge_detect_node.node_tree = joekasou
        edge_detect_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], edge_detect_node.inputs[0])
        links.new(edge_detect_node.outputs[0], output_node.inputs[0])

        print("edge detect Node node group added and connected.")

        output_node.location.x += 200

        if output_node.type == 'GROUP' and output_node.node_tree.name.startswith("Transparent"):
            material_output_reference.location.x += 200

        edge_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("AddCurvature"):
                node.name = f"Curvature #{edge_count}"
                edge_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}

class AddHairCurves(bpy.types.Operator):
    bl_idname = "shaderaddon.addhaircurves"
    bl_label = "添加头发曲线反射"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        output_node = None
        material_output_reference = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                material_output_reference = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        
        


        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "HSL" node group
        edge_detect_group = bpy.data.node_groups.get("HairCurves")
        if not edge_detect_group:
            print("Node group 'edge detect' not found.")
            return
        
        # Add the "AmbientOcclusion" node to the material
        output_node.location.x += 400
        joekasou = edge_detect_group.copy()
        edge_detect_node = nodes.new(type='ShaderNodeGroup')
        edge_detect_node.node_tree = joekasou
        edge_detect_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], edge_detect_node.inputs[0])
        links.new(edge_detect_node.outputs[0], output_node.inputs[0])

        print("edge detect Node node group added and connected.")

        output_node.location.x += 200

        if output_node.type == 'GROUP' and output_node.node_tree.name.startswith("Transparent"):
            material_output_reference.location.x += 200

        edge_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("HairCurves"):
                node.name = f"Hair Curve Reflect #{edge_count}"
                edge_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddEdgeDetect(bpy.types.Operator):
    bl_idname = "shaderaddon.addedgedetect"
    bl_label = "添加边缘轮廓"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        output_node = None
        material_output_reference = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                material_output_reference = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        
        


        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "EdgeDetect" node group
        edge_detect_group = bpy.data.node_groups.get("EdgeDetect")
        if not edge_detect_group:
            print("Node group 'edge detect' not found.")
            return
        
        # Add the "AmbientOcclusion" node to the material
        output_node.location.x += 400
        joekasou = edge_detect_group.copy()
        edge_detect_node = nodes.new(type='ShaderNodeGroup')
        edge_detect_node.node_tree = joekasou
        edge_detect_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], edge_detect_node.inputs[0])
        links.new(edge_detect_node.outputs[0], output_node.inputs[0])

        print("edge detect Node node group added and connected.")

        output_node.location.x += 200

        if output_node.type == 'GROUP' and output_node.node_tree.name.startswith("Transparent"):
            material_output_reference.location.x += 200

        edge_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("EdgeDetect"):
                node.name = f"Edge Detect #{edge_count}"
                edge_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddAO(bpy.types.Operator):
    bl_idname = "shaderaddon.addao"
    bl_label = "添加环境光遮蔽"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("AmbientOcc"):
                return {'FINISHED'}

        output_node = None
        material_output_reference = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                material_output_reference = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return
        


        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return
        
        # Create the "AmbientOcclusion" node group
        ambient_occlusion_group = bpy.data.node_groups.get("AmbientOcclusion")
        if not ambient_occlusion_group:
            print("Node group 'Ambient Occlusion' not found.")
            return
        
        # Add the "AmbientOcclusion" node to the material
        output_node.location.x += 400
        joekasou = ambient_occlusion_group.copy()
        ambient_occlusion_node = nodes.new(type='ShaderNodeGroup')
        ambient_occlusion_node.node_tree = joekasou
        ambient_occlusion_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], ambient_occlusion_node.inputs[0])
        links.new(ambient_occlusion_node.outputs[0], output_node.inputs[0])

        print("Ambient Occlusion Node node group added and connected.")

        output_node.location.x += 200

        if output_node.type == 'GROUP' and output_node.node_tree.name.startswith("Transparent"):
            material_output_reference.location.x += 200

        ambient_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("AmbientOcclusion"):
                node.name = f"Ambient Occlusion #{ambient_count}"
                ambient_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}




class DuplicateMaterial(bpy.types.Operator):
    bl_idname = "shaderaddon.duplicatematerial"
    bl_label = "复制材质"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        active_material = obj.active_material
        
        active_material_copy = active_material.copy()

        if active_material_copy.use_nodes:
            for node in active_material_copy.node_tree.nodes:
                if node.type == 'GROUP' and not node.node_tree.name.startswith("RedLight"):
                    node.node_tree = node.node_tree.copy()

        obj.active_material = active_material_copy

        #duplicate geonodes
        for modifier in obj.modifiers:
            if modifier.type == 'NODES' and modifier.name.startswith("SB"):
                node_tree = modifier.node_group
                if node_tree:
                    new_node_tree = node_tree.copy()
                    modifier.node_group = new_node_tree

        return {'FINISHED'}


class AddCrossHatch(bpy.types.Operator):
    bl_idname = "shaderaddon.addcrosshatch"
    bl_label = "添加交叉阴影光照"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return {'FINISHED'}

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("Diffuse"):
                return {'FINISHED'}
            if node.type == 'GROUP' and node.node_tree.name.startswith("CrossHatch"):
                return {'FINISHED'}

        # Find the Material Output node
        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        # for node in nodes:
        #     if node.type == 'GROUP' and node.node_tree.name.startswith("Transparent") and node.name.endswith("1"):
        #         output_node = node
        #         break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return {'FINISHED'}

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return {'FINISHED'}
        
        # Create the "DiffuseLight" node group
        diffuse_light_group = bpy.data.node_groups.get("CrossHatch")
        if not diffuse_light_group:
            print("Node group 'Diffuse Light' not found.")
            return {'FINISHED'}
        
        # Add the "DiffuseLight" node to the material
        output_node.location.x += 400
        joekasou = diffuse_light_group.copy()
        diffuse_light_node = nodes.new(type='ShaderNodeGroup')
        diffuse_light_node.node_tree = joekasou
        diffuse_light_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], diffuse_light_node.inputs[0])
        links.new(diffuse_light_node.outputs[0], output_node.inputs[0])

        print("Diffuse Light Node node group added and connected.")

        output_node.location.x += 200

        diffuse_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("CrossHatch"):
                node.name = f"Cross Hatch Lighting (Dynamic)"
                diffuse_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddDiffuseLighting(bpy.types.Operator):
    bl_idname = "shaderaddon.adddiffuselighting"
    bl_label = "add diffuse lighting"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return {'FINISHED'}

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("Diffuse"):
                return {'FINISHED'}
            if node.type == 'GROUP' and node.node_tree.name.startswith("CrossHatch"):
                return {'FINISHED'}

        # Find the Material Output node
        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        # for node in nodes:
        #     if node.type == 'GROUP' and node.node_tree.name.startswith("Transparent") and node.name.endswith("1"):
        #         output_node = node
        #         break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return {'FINISHED'}

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return {'FINISHED'}
        
        # Create the "DiffuseLight" node group
        diffuse_light_group = bpy.data.node_groups.get("DiffuseLight")
        if not diffuse_light_group:
            print("Node group 'Diffuse Light' not found.")
            return {'FINISHED'}
        
        # Add the "DiffuseLight" node to the material
        output_node.location.x += 400
        joekasou = diffuse_light_group.copy()
        diffuse_light_node = nodes.new(type='ShaderNodeGroup')
        diffuse_light_node.node_tree = joekasou
        diffuse_light_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], diffuse_light_node.inputs[0])
        links.new(diffuse_light_node.outputs[0], output_node.inputs[0])

        print("Diffuse Light Node node group added and connected.")

        output_node.location.x += 200

        diffuse_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("DiffuseLight"):
                node.name = f"Stylized Light (Dynamic) - #{diffuse_count}"
                diffuse_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddFakeSun(bpy.types.Operator):
    bl_idname = "shaderaddon.addsunlight"
    bl_label = "Add Sun Light (Easily Bake)"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        for modifier in obj.modifiers:
            if modifier.name.startswith("SB Sun"):
                return {'FINISHED'}

        

        #handle geonodes

        fakesungeonode = bpy.data.node_groups.get("SunPower").copy()

        geomodifier = obj.modifiers.new(name="SB SunNodes", type='NODES')

        geomodifier.node_group = fakesungeonode

        #end geonodes


        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # material.blend_method = 'BLEND'
        # material.show_transparent_back = False

        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "SunObject" node group
        sun_object_group = bpy.data.node_groups.get("SunObject")
        if not sun_object_group:
            print("Node group 'Sun Object' not found.")
            return
        
        # Add the "SunObject" node to the material
        output_node.location.x += 400
        joekasou = sun_object_group.copy()
        sun_object_node = nodes.new(type='ShaderNodeGroup')
        sun_object_node.node_tree = joekasou
        sun_object_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], sun_object_node.inputs[0])
        links.new(sun_object_node.outputs[0], output_node.inputs[0])

        print("Noise Texture Node node group added and connected.")

        output_node.location.x += 200

        currattrname = None
        #renaming
        light_object_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("SunObject"):
                node.name = f"Sun Light #{light_object_count}"
                node.node_tree.nodes["Attribute"].attribute_name = f"Light {light_object_count}"
                currattrname = node.node_tree.nodes["Attribute"].attribute_name
                number = light_object_count
                for modifier in obj.modifiers:
                    if modifier.type == 'NODES' and modifier.name.startswith("SB"):
                        number -= 1
                        if number == 0:
                            modifier.node_group.nodes["Store Named Attribute"].inputs[2].default_value = currattrname
                light_object_count += 1
        
        #add attributes
        
        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}




class AddFakeLight(bpy.types.Operator):
    bl_idname = "shaderaddon.addobjectlight"
    bl_label = "Add Object Light (Easily Bake)"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return


        #handle geonodes

        fakelightgeonode = bpy.data.node_groups.get("SB Light Creation").copy()

        geomodifier = obj.modifiers.new(name="SB Geonodes", type='NODES')

        geomodifier.node_group = fakelightgeonode

        #end geonodes


        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # material.blend_method = 'BLEND'
        # material.show_transparent_back = False

        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "LightObject" node group
        light_object_group = bpy.data.node_groups.get("LightObject")
        if not light_object_group:
            print("Node group 'Light Object' not found.")
            return
        
        # Add the "NoiseTexture" node to the material
        output_node.location.x += 400
        joekasou = light_object_group.copy()
        light_object_node = nodes.new(type='ShaderNodeGroup')
        light_object_node.node_tree = joekasou
        light_object_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], light_object_node.inputs[0])
        links.new(light_object_node.outputs[0], output_node.inputs[0])

        print("Noise Texture Node node group added and connected.")

        output_node.location.x += 200

        currattrname = None
        #renaming
        light_object_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("LightObject"):
                node.name = f"Light (Object) #{light_object_count}"
                node.node_tree.nodes["Attribute"].attribute_name = f"Light {light_object_count}"
                currattrname = node.node_tree.nodes["Attribute"].attribute_name
                number = light_object_count
                for modifier in obj.modifiers:
                    if modifier.type == 'NODES' and modifier.name.startswith("SB"):
                        number -= 1
                        if number == 0:
                            modifier.node_group.nodes["Store Named Attribute"].inputs[2].default_value = currattrname
                light_object_count += 1

        # node1 = nodes.get("Base Color")
        # light_object_count = 1
        # while node1:
        #     if node1.type == 'GROUP' and node1.node_tree.name.startswith("LightObject"):
        #         node1.name = f"Light (Easy Bake) #{light_object_count}"
        #         node1.node_tree.nodes["Attribute"].attribute_name = f"Light {light_object_count}"
        #         currattrname = node1.node_tree.nodes["Attribute"].attribute_name
        #         number = light_object_count
        #         for modifier in obj.modifiers:
        #             if modifier.type == 'NODES' and modifier.name.startswith("SB"):
        #                 number -= 1
        #                 if number == 0:
        #                     modifier.node_group.nodes["Store Named Attribute"].inputs[2].default_value = currattrname
        #         light_object_count += 1
        #     if node1.outputs and node1.outputs[0].is_linked:
        #         node1 = node1.outputs[0].links[0].to_node
        #     else:
        #         break

        
        #check if theres other objects sharing this material
        for objeto in bpy.data.objects:
            if objeto == obj:
                continue
            if objeto.active_material == obj.active_material:
                objeto.modifiers.new(name="aloha", type='NODES')
                objeto.modifiers["aloha"].name = geomodifier.name
                objeto.modifiers[f"{geomodifier.name}"].node_group = geomodifier.node_group

        #add attributes
        

        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        random_offset_z = random.uniform(0, 2)


        bpy.ops.mesh.primitive_uv_sphere_add()
        emptysphere = bpy.context.object
        emptysphere.show_name = True
        emptysphere.display_type = 'BOUNDS'
        emptysphere.display_bounds_type = 'SPHERE'
        emptysphere.location.x += random_offset_x
        emptysphere.location.y += random_offset_y
        emptysphere.location.z += random_offset_z
        emptysphere.name = "SB " + f"{light_object_node.name} " + f"{obj.name}"
        emptysphere.parent = obj
        emptysphere.data.materials.append(None)
        emptysphere.data.materials[0] = bpy.data.materials.get("SBfullblank")

        geomodifier.node_group.nodes["Object Info"].inputs[0].default_value = emptysphere

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class MaskSpeculars(bpy.types.Operator):
    bl_idname = "shaderaddon.maskspeculars"
    bl_label = "mask speculars from dynamic noise"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return {'FINISHED'}
        
        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        specular_group = None

        for node in nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("SpecularRef"):
                specular_group = node

        try:
            for node in nodes:
                if node.type == 'GROUP' and node.node_tree.name.startswith("TransparentNoise"):
                    if node.inputs[70].default_value > 0.5:
                        links.new(specular_group.outputs[2], node.inputs[73])
        except:
            joe = "Kasoiu"

        return {'FINISHED'}


class AddTransparentWorldStrokes(bpy.types.Operator):
    bl_idname = "shaderaddon.addtransparentworldstrokes"
    bl_label = "add simple transparency, can also be used for floating strokes"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        if material.blend_method == 'HASHED':
            joe = "kasou"
        else:
            material.blend_method = 'BLEND'

        material.show_transparent_back = True

        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        # node1 = nodes.get("Base Color")
        # while node1:
        #     if node1.type == 'GROUP' and node1.node_tree.name.startswith("TransparentPa") and node1.name.endswith("1"):
        #         output_node = node1
        #         break
        #     if node1.outputs and node1.outputs[0].is_linked:
        #         node1 = node1.outputs[0].links[0].to_node
        #     else:
        #         break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "NoiseTexture" node group
        noise_texture_group = bpy.data.node_groups.get("TransparentWorldStrokes")
        if not noise_texture_group:
            print("Node group 'Noise Texture' not found.")
            return
        
        # Add the "NoiseTexture" node to the material
        output_node.location.x += 400
        joekasou = noise_texture_group.copy()
        noise_texture_node = nodes.new(type='ShaderNodeGroup')
        noise_texture_node.node_tree = joekasou
        noise_texture_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], noise_texture_node.inputs[0])
        links.new(noise_texture_node.outputs[0], output_node.inputs[0])

        print("Noise Texture Node node group added and connected.")

        output_node.location.x += 200

        noise_texture_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("TransparentWorldStrokes"):
                node.name = f"Simple Transparency #{noise_texture_count}"
                noise_texture_count += 1

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddTransparentNoise(bpy.types.Operator):
    bl_idname = "shaderaddon.addtransparentnoise"
    bl_label = "add transparent noise texture effect"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        if material.blend_method == 'HASHED':
            joe = "kasou"
        else:
            material.blend_method = 'BLEND'

        material.show_transparent_back = False

        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        # node1 = nodes.get("Base Color")
        # while node1:
        #     if node1.type == 'GROUP' and node1.node_tree.name.startswith("TransparentPa") and node1.name.endswith("1"):
        #         output_node = node1
        #         break
        #     if node1.outputs and node1.outputs[0].is_linked:
        #         node1 = node1.outputs[0].links[0].to_node
        #     else:
        #         break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "NoiseTexture" node group
        noise_texture_group = bpy.data.node_groups.get("TransparentNoiseTexture")
        if not noise_texture_group:
            print("Node group 'Noise Texture' not found.")
            return
        
        # Add the "NoiseTexture" node to the material
        output_node.location.x += 400
        joekasou = noise_texture_group.copy()
        noise_texture_node = nodes.new(type='ShaderNodeGroup')
        noise_texture_node.node_tree = joekasou
        noise_texture_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], noise_texture_node.inputs[0])
        links.new(noise_texture_node.outputs[0], output_node.inputs[0])

        print("Noise Texture Node node group added and connected.")

        output_node.location.x += 200

        noise_texture_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("TransparentNoiseTexture"):
                node.name = f"Transparent Dynamic Texture #{noise_texture_count}"
                noise_texture_count += 1

        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        random_offset_z = random.uniform(0, 2)


        bpy.ops.object.empty_add(type='SPHERE')
        emptysphere = bpy.context.object
        emptysphere.location.x += random_offset_x
        emptysphere.location.y += random_offset_y
        emptysphere.location.z += random_offset_z
        emptysphere.name = "SB " + f"{noise_texture_node.name} " + f"{obj.name}"
        emptysphere.parent = obj

        joekasou.nodes["ZhaTexture Coordinate"].object = emptysphere

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}

class AddStylizedFoam(bpy.types.Operator):
    bl_idname = "shaderaddon.addstylizedfoam"
    bl_label = "add stylized foam effect"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "StylizedFoam" node group
        noise_texture_group = bpy.data.node_groups.get("StylizedFoam")
        if not noise_texture_group:
            print("Node group 'Noise Texture' not found.")
            return
        
        # Add the "NoiseTexture" node to the material
        output_node.location.x += 400
        joekasou = noise_texture_group.copy()
        noise_texture_node = nodes.new(type='ShaderNodeGroup')
        noise_texture_node.node_tree = joekasou
        noise_texture_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], noise_texture_node.inputs[0])
        links.new(noise_texture_node.outputs[0], output_node.inputs[0])

        print("Noise Texture Node node group added and connected.")

        output_node.location.x += 200

        noise_texture_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("StylizedFoam"):
                node.name = f"Stylized Foam #{noise_texture_count}"
                noise_texture_count += 1

        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        random_offset_z = random.uniform(0, 2)


        bpy.ops.object.empty_add(type='SPHERE')
        emptysphere = bpy.context.object
        emptysphere.location.x += random_offset_x
        emptysphere.location.y += random_offset_y
        emptysphere.location.z += random_offset_z
        emptysphere.name = "SB " + f"{noise_texture_node.name} " + f"{obj.name}"
        emptysphere.parent = obj

        joekasou.nodes["ZhaTexture Coordinate"].object = emptysphere

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddNoiseTexture(bpy.types.Operator):
    bl_idname = "shaderaddon.addnoisetexture"
    bl_label = "add noise texture effect"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return
        
        # Create the "NoiseTexture" node group
        noise_texture_group = bpy.data.node_groups.get("NoiseTexture")
        if not noise_texture_group:
            print("Node group 'Noise Texture' not found.")
            return
        
        # Add the "NoiseTexture" node to the material
        output_node.location.x += 400
        joekasou = noise_texture_group.copy()
        noise_texture_node = nodes.new(type='ShaderNodeGroup')
        noise_texture_node.node_tree = joekasou
        noise_texture_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], noise_texture_node.inputs[0])
        links.new(noise_texture_node.outputs[0], output_node.inputs[0])

        print("Noise Texture Node node group added and connected.")

        output_node.location.x += 200

        noise_texture_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("NoiseTexture"):
                node.name = f"Dynamic Texture #{noise_texture_count}"
                noise_texture_count += 1

        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        random_offset_z = random.uniform(0, 2)


        bpy.ops.object.empty_add(type='SPHERE')
        emptysphere = bpy.context.object
        emptysphere.location.x += random_offset_x
        emptysphere.location.y += random_offset_y
        emptysphere.location.z += random_offset_z
        emptysphere.name = "SB " + f"{noise_texture_node.name} " + f"{obj.name}"
        emptysphere.parent = obj

        joekasou.nodes["ZhaTexture Coordinate"].object = emptysphere

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}
    

class AddEasyDT(bpy.types.Operator):
    bl_idname = "shaderaddon.addeasydt"
    bl_label = "add simple dynamic texture"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return
        
        # Create the "NoiseTexture" node group
        noise_texture_group = bpy.data.node_groups.get("EasyDT")
        if not noise_texture_group:
            print("Node group 'Noise Texture' not found.")
            return
        
        # Add the "NoiseTexture" node to the material
        output_node.location.x += 400
        joekasou = noise_texture_group.copy()
        noise_texture_node = nodes.new(type='ShaderNodeGroup')
        noise_texture_node.node_tree = joekasou
        noise_texture_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], noise_texture_node.inputs[0])
        links.new(noise_texture_node.outputs[0], output_node.inputs[0])

        print("Noise Texture Node node group added and connected.")

        output_node.location.x += 200

        noise_texture_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("EasyDT"):
                node.name = f"Simple Dynamic Texture #{noise_texture_count}"
                noise_texture_count += 1

        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        random_offset_z = random.uniform(0, 2)


        bpy.ops.object.empty_add(type='SPHERE')
        emptysphere = bpy.context.object
        emptysphere.location.x += random_offset_x
        emptysphere.location.y += random_offset_y
        emptysphere.location.z += random_offset_z
        emptysphere.name = "SB " + f"{noise_texture_node.name} " + f"{obj.name}"
        emptysphere.parent = obj

        joekasou.nodes["ZhaTexture Coordinate"].object = emptysphere

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddInstantWatercolor(bpy.types.Operator):
    bl_idname = "shaderaddon.addinstantwatercolor"
    bl_label = "add instant watercolor effect"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links


        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return
        
        # Create the "NoiseTexture" node group
        noise_texture_group = bpy.data.node_groups.get("InstantWatercolor")
        if not noise_texture_group:
            print("Node group 'Noise Texture' not found.")
            return
        
        # Add the "NoiseTexture" node to the material
        output_node.location.x += 400
        joekasou = noise_texture_group.copy()
        noise_texture_node = nodes.new(type='ShaderNodeGroup')
        noise_texture_node.node_tree = joekasou
        noise_texture_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], noise_texture_node.inputs[0])
        links.new(noise_texture_node.outputs[0], output_node.inputs[0])

        print("Noise Texture Node node group added and connected.")

        output_node.location.x += 200

        noise_texture_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("InstantWatercolor"):
                node.name = f"风格化污渍 #{noise_texture_count}"
                noise_texture_count += 1

        # random_offset_x = random.uniform(-5, 5)
        # random_offset_y = random.uniform(-5, 5)
        # random_offset_z = random.uniform(0, 2)


        # bpy.ops.object.empty_add(type='SPHERE')
        # emptysphere = bpy.context.object
        # emptysphere.location.x += random_offset_x
        # emptysphere.location.y += random_offset_y
        # emptysphere.location.z += random_offset_z
        # emptysphere.name = "SB " + f"{noise_texture_node.name} " + f"{obj.name}"
        # emptysphere.parent = obj

        # joekasou.nodes["ZhaTexture Coordinate"].object = emptysphere

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddDisplace(bpy.types.Operator):
    bl_idname = "shaderaddon.adddisplace"
    bl_label = "add displace to model"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        
        if not obj:
            print("No active object or no material with nodes found.")
            return {'FINISHED'}

        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        displace_modifier = obj.modifiers.new(name="Displace", type='DISPLACE')

        displace_modifier.name = "SB Displace"
        displace_modifier.texture_coords = "OBJECT"

        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        random_offset_z = random.uniform(0, 2)


        bpy.ops.object.empty_add(type='SPHERE')
        emptysphere = bpy.context.object
        emptysphere.location.x += random_offset_x
        emptysphere.location.y += random_offset_y
        emptysphere.location.z += random_offset_z
        emptysphere.name = "SB " + f"Displace Effect " + f"{obj.name}"
        emptysphere.parent = obj

        displace_modifier.texture_coords_object = emptysphere

        timer_function()

        return {'FINISHED'}


# class AddMoodLight(bpy.types.Operator):
#     bl_idname = "shaderaddon.addcoloredcircularlight"
#     bl_label = "add colored circular light"

#     def execute(self, context):
#         obj = bpy.context.active_object

#         tempobj = None
#         if obj.type == 'EMPTY' and obj.name.startswith("SB"):
#             tempobj = obj.parent
#             obj = tempobj
#         elif obj.type == 'MESH' and obj.name.startswith("SB"):
#             tempobj = obj.parent
#             obj = tempobj

#         if not obj or not obj.active_material or not obj.active_material.use_nodes:
#             print("No active object or no material with nodes found.")
#             return

#         material = obj.active_material
#         nodes = material.node_tree.nodes
#         links = material.node_tree.links

#         # Find the Material Output node
#         output_node = None
#         for node in nodes:
#             if node.type == 'OUTPUT_MATERIAL':
#                 output_node = node
#                 break
        
#         node1 = nodes.get("Base Color")
#         while node1:
#             if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
#                 output_node = node1
#                 break
#             if node1.outputs and node1.outputs[0].is_linked:
#                 node1 = node1.outputs[0].links[0].to_node
#             else:
#                 break

#         if not output_node:
#             print("No Material Output node found.")
#             return

#         # Find the node that is currently connected to the Material Output node
#         incoming_link = None
#         for link in links:
#             if link.to_node == output_node:
#                 incoming_link = link
#                 break

#         if not incoming_link:
#             print("No link to the Material Output node found.")
#             return

#         # Create the "MoodLight" node group
#         mood_light_group = bpy.data.node_groups.get("ColoredCircular")
#         if not mood_light_group:
#             print("Node group 'ColoredCircular' not found.")
#             return
        
#         # Add the "LocalGradient" node to the material
#         output_node.location.x += 400
#         joekasou = mood_light_group.copy()
#         mood_light_node = nodes.new(type='ShaderNodeGroup')
#         mood_light_node.node_tree = joekasou
#         mood_light_node.location = (output_node.location.x - 200, output_node.location.y)

#         # Connect the new node
#         links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], mood_light_node.inputs[0])
#         links.new(mood_light_node.outputs[0], output_node.inputs[0])

#         print("Mood Light node group added and connected.")

#         output_node.location.x += 200

#         mood_count = 1
#         for node in obj.active_material.node_tree.nodes:
#             if node.type == 'GROUP' and node.node_tree.name.startswith("ColoredCircular"):
#                 node.name = f"Colored Light #{mood_count}"
#                 mood_count += 1


#         random_offset_x = random.uniform(-5, 5)
#         random_offset_y = random.uniform(-5, 5)
#         random_offset_z = random.uniform(0, 2)


#         bpy.ops.object.empty_add(type='SPHERE')
#         emptysphere = bpy.context.object
#         emptysphere.location.x += random_offset_x
#         emptysphere.location.y += random_offset_y
#         emptysphere.location.z += random_offset_z
#         emptysphere.name = "SB " + f"{mood_light_node.name} " + f"{obj.name}"
#         emptysphere.parent = obj

#         joekasou.nodes["ZhaTexture Coordinate"].object = emptysphere

#         newlist = []
#         newlistview = []
#         newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

#         for node in obj.active_material.node_tree.nodes:
#             if node.name == "Base Color":
#                 newlistview.append((node.name, node.name, ""))
#                 continue
#             if node.type == 'GROUP':
#                 newlist.append((node.name, node.name, ""))
#                 newlistview.append((node.name, node.name, ""))
#         bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
#             name="Node Groups",
#             description = "节点组列表",
#             items = newlist
#         )
#         # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
#         #     name="Node Groups View",
#         #     description = "节点组列表 for effect viewer",
#         #     items = newlistview
#         # )
#         bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
#             name="Node Groups",
#             description = "节点组列表",
#             items = newlist
#         )
#         bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
#             name="Node Groups",
#             description = "节点组列表",
#             items = newlist
#         )
#         bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
#             name="Node Groups",
#             description = "节点组列表",
#             items = newlist
#         )

#         return {'FINISHED'}

class AddCircularLight(bpy.types.Operator):
    bl_idname = "shaderaddon.addcircularlight"
    bl_label = "add circular light"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Find the Material Output node
        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        # Find the node that is currently connected to the Material Output node
        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "LocalGradient" node group
        circular_light_group = bpy.data.node_groups.get("CircularLight")
        if not circular_light_group:
            print("Node group 'CircularLight' not found.")
            return
        
        # Add the "LocalGradient" node to the material
        output_node.location.x += 400
        joekasou = circular_light_group.copy()
        circular_light_node = nodes.new(type='ShaderNodeGroup')
        circular_light_node.node_tree = joekasou
        circular_light_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], circular_light_node.inputs[0])
        links.new(circular_light_node.outputs[0], output_node.inputs[0])

        print("Circular Light node group added and connected.")

        output_node.location.x += 200

        circular_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("CircularLight"):
                node.name = f"Circular Light #{circular_count}"
                circular_count += 1


        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        random_offset_z = random.uniform(0, 2)


        bpy.ops.object.empty_add(type='SPHERE')
        emptysphere = bpy.context.object
        emptysphere.location.x += random_offset_x
        emptysphere.location.y += random_offset_y
        emptysphere.location.z += random_offset_z
        emptysphere.name = "SB " + f"{circular_light_node.name} " + f"{obj.name}"
        emptysphere.parent = obj

        joekasou.nodes["ZhaTexture Coordinate"].object = emptysphere

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}


class AddLocalGradientSphere(bpy.types.Operator):
    bl_idname = "shaderaddon.addlocalgradientsphere"
    bl_label = "add local sphere gradient"

    
    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Find the Material Output node
        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        # Find the node that is currently connected to the Material Output node
        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "LocalGradient" node group
        local_gradient_group = bpy.data.node_groups.get("LocalGradientSphere")
        if not local_gradient_group:
            print("Node group 'LocalGradient' not found.")
            return

        # Add the "LocalGradient" node to the material
        output_node.location.x += 400
        joekasou = local_gradient_group.copy()
        local_gradient_node = nodes.new(type='ShaderNodeGroup')
        local_gradient_node.node_tree = joekasou
        local_gradient_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], local_gradient_node.inputs[0])
        links.new(local_gradient_node.outputs[0], output_node.inputs[0])

        print("LocalGradient node group added and connected.")

        output_node.location.x += 200

        gradient_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("LocalGradientSphere"):
                node.name = f"Sphere Gradient {gradient_count}"
                gradient_count += 1


        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        random_offset_z = random.uniform(0, 2)


        bpy.ops.object.empty_add(type='SPHERE')
        emptysphere = bpy.context.object
        emptysphere.location.x += random_offset_x
        emptysphere.location.y += random_offset_y
        emptysphere.location.z += random_offset_z
        emptysphere.name = "SB " + f"{local_gradient_node.name} " + f"{obj.name}"
        emptysphere.parent = obj

        joekasou.nodes["ZhaTexture Coordinate"].object = emptysphere

        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}

#Add Local Gradient
class AddLocalGradient(bpy.types.Operator):
    bl_idname = "shaderaddon.addlocalgradient"
    bl_label = "add local gradient"

    
    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Find the Material Output node
        output_node = None
        for node in nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        node1 = nodes.get("Base Color")
        while node1:
            if node1.type == 'GROUP' and node1.node_tree.name.startswith("Transparent"):
                output_node = node1
                break
            if node1.outputs and node1.outputs[0].is_linked:
                node1 = node1.outputs[0].links[0].to_node
            else:
                break

        if not output_node:
            print("No Material Output node found.")
            return

        # Find the node that is currently connected to the Material Output node
        incoming_link = None
        for link in links:
            if link.to_node == output_node:
                incoming_link = link
                break

        if not incoming_link:
            print("No link to the Material Output node found.")
            return

        # Create the "LocalGradient" node group
        local_gradient_group = bpy.data.node_groups.get("LocalGradient")
        if not local_gradient_group:
            print("Node group 'LocalGradient' not found.")
            return

        # Add the "LocalGradient" node to the material
        output_node.location.x += 400
        joekasou = local_gradient_group.copy()
        local_gradient_node = nodes.new(type='ShaderNodeGroup')
        local_gradient_node.node_tree = joekasou
        local_gradient_node.location = (output_node.location.x - 200, output_node.location.y)

        # Connect the new node
        links.new(incoming_link.from_node.outputs[incoming_link.from_socket.name], local_gradient_node.inputs[0])
        links.new(local_gradient_node.outputs[0], output_node.inputs[0])

        print("LocalGradient node group added and connected.")

        output_node.location.x += 200

        gradient_count = 1
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree.name.startswith("LocalGradient"):
                node.name = f"Gradient {gradient_count}"
                gradient_count += 1


        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        random_offset_z = random.uniform(0, 2)


        bpy.ops.object.empty_add(type='SPHERE')
        emptysphere = bpy.context.object
        emptysphere.location.x += random_offset_x
        emptysphere.location.y += random_offset_y
        emptysphere.location.z += random_offset_z
        emptysphere.name = "SB " + f"{local_gradient_node.name} " + f"{obj.name}"
        emptysphere.parent = obj

        joekasou.nodes["ZhaTexture Coordinate"].object = emptysphere
       
        newlist = []
        newlistview = []
        newlistview.append(('SHOWALL', "Show all Items", "Show all Effects"))

        for node in obj.active_material.node_tree.nodes:
            if node.name == "Base Color":
                newlistview.append((node.name, node.name, ""))
                continue
            if node.type == 'GROUP':
                newlist.append((node.name, node.name, ""))
                newlistview.append((node.name, node.name, ""))
        bpy.types.Object.node_groups_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        # bpy.types.Object.node_groups_enum_view = bpy.props.EnumProperty(
        #     name="Node Groups View",
        #     description = "节点组列表 for effect viewer",
        #     items = newlistview
        # )
        bpy.types.Object.node_groups_enum_swap2 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.node_groups_enum_swap1 = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )
        bpy.types.Object.duplicate_group_enum = bpy.props.EnumProperty(
            name="Node Groups",
            description = "节点组列表",
            items = newlist
        )

        return {'FINISHED'}

#World Panel

class WorldPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "风格化资产套件"
    bl_label = "背景设置"

    def draw(self, context):
        
        layout = self.layout

        row = layout.row()
        row.operator("shaderaddon.worldsetup", text="更改背景颜色")

        world = bpy.context.scene.world
        if world is not None and world.use_nodes:
            base_gradient_node = world.node_tree.nodes.get("Base Gradient")

            if base_gradient_node is not None:
                box = layout.box()
                row = box.row()
                row.label(text="背景颜色设置")

                material = bpy.data.worlds.get("layeredworld")
                nodes = material.node_tree.nodes

                row = layout.row()
                row.prop(nodes["Base Gradient"].node_tree.nodes["Map Range"], "interpolation_type", text="样式")
                row = layout.row()
                row.prop(nodes["Base Gradient"].node_tree.nodes["Gradient Texture"], "gradient_type", text="渐变类型")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[14], "default_value", text="色阶")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[0], "default_value", text="基准色")
                row = layout.row()
                row.label(text="渐变设置")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[1], "default_value", text="最大值")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[17], "default_value", text="顶部着色")
                row.prop(nodes["Base Gradient"].inputs[18], "default_value", text="影响权重")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[4], "default_value", text="底部值")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[15], "default_value", text="底部着色")
                row.prop(nodes["Base Gradient"].inputs[16], "default_value", text="影响权重")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[8], "default_value", text="渐变位置")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[9], "default_value", text="渐变旋转")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[10], "default_value", text="渐变缩放")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[10], "default_value", text="渐变缩放")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[7], "default_value", text="艺术化扭曲")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[11], "default_value", text="扭曲缩放（均匀）")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[12], "default_value", text="扭曲缩放")
                row = layout.row()
                row.prop(nodes["Base Gradient"].inputs[13], "default_value", text="动态扭曲")




#Panel

class ShaderPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "风格化资产套件"
    bl_label = "添加材质"

    def draw(self, context):
        obj = bpy.context.active_object

        if not obj:
            return
        #check if empty
        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        #check too many redlightsas nodegroups
        count = 0
        for group in bpy.data.node_groups:
            if group.name.startswith("RedLightSAS"):
                count += 1
        if count > 1:
            return
        
        try:
            for node in obj.active_material.node_tree.nodes:
                if node.type == 'GROUP' and node.name.startswith("SAS Point Lights Group #1") and not node.node_tree.name == 'RedLightSAS':
                    return
        except:
            print('hello')

        #check if wisp light
        try:
            layout = self.layout
            if bpy.context.object.name.startswith("SAS Point Light Group #1"):
                row = layout.row()
                box = layout.box()
                row = box.row()
                row.label(text="SAS点光群组 #1")
                node = bpy.data.node_groups['RedLightSAS']
                row = layout.row()
                light_data_name = obj.data.name
                row.prop(bpy.data.lights[light_data_name], "energy", text="强度")
                row = layout.row()
                row.prop(bpy.data.lights[light_data_name], "use_shadow", text="投射阴影?")

                if node.nodes.get("Visibility") is not None:
                    # row = layout.row()
                    # row.prop(node.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    row = layout.row()
                    row.prop(node.nodes['zhaRange'], "interpolation_type", text="混合样式")
                    if node.nodes['zhaRange'].interpolation_type == 'STEPPED':
                        row = layout.row()
                        row.prop(node.nodes['zhaXYZ3'].inputs[0], "default_value", text="色阶")
                    row = layout.row()
                    row.prop(node.nodes['zhaValue'].outputs[0], "default_value", text="亮度")
                    row = layout.row()
                    row.prop(node.nodes['zhaHSV'].inputs[1], "default_value", text="饱和度")
                    row.prop(node.nodes['zhaHSV'].inputs[0], "default_value", text="色相")
                    row = layout.row()
                    row.prop(node.nodes['zhaMix'].inputs[7], "default_value", text="色调叠加")
                    row = layout.row()
                    row.prop(node.nodes['zhaMix'].inputs[0], "default_value", text="色调强度")
                    row = layout.row()
                    row.prop(node.nodes['zhaXYZ1'].inputs[0], "default_value", text="扩散范围")
                    row.prop(node.nodes['zhaXYZ2'].inputs[0], "default_value", text="锐度")
                    row = layout.row()
                    row.prop(node.nodes['zhaRamp'].color_ramp.elements[0], "position", text="暗部遮蔽强化（调高此值）")
                    row = layout.row()
                    row.prop(node.nodes['zhaRamp'].color_ramp.elements[1], "position", text="亮区锐化弱化（调低此值）")
                    return
        except:
            print('none')


        #material slots stuff
        layout = self.layout

        # row = layout.row()
        # row.prop(bpy.context.scene, "my_directory_enum", text="Hello")

        row = layout.row()
        row.template_ID(obj, "active_material", new="shaderaddon.objectsetup")
        row = layout.row()
        row.operator("shaderaddon.duplicatematerial", text="制作材质/效果单用户副本")
        row = layout.row()
        row.operator("object.material_slot_add", text="添加材质槽")
        row.operator("object.material_slot_remove", text="移除材质槽")
        # Material slots management
        row = layout.row()
        row.template_list("MATERIAL_UL_matslots", "", obj, "material_slots", obj, "active_material_index")
        if bpy.context.mode == 'EDIT_MESH' or bpy.context.mode == 'EDIT_CURVE':
            row = layout.row()
            row.operator("object.material_slot_assign", text="指定材质")
            row.operator("object.material_slot_select", text="选择面")
            row.operator("object.material_slot_deselect", text="取消选择面")

        if not obj.active_material:
            return

        try:
            row = layout.row()
            
            # row.prop(obj.active_material, "shadow_method", text="阴影模式")
            version = bpy.app.version
            if version < (4, 2, 0):
                row.prop(obj.active_material, "blend_method", text="混合模式")
                row.prop(obj.active_material, "shadow_method", text="阴影模式")
            else:
                row.prop(obj.active_material, "surface_render_method", text="混合模式")
                row.prop(obj, "visible_shadow", text="投射阴影")
            row.prop(obj.active_material, "show_transparent_back", text="显示背面面片")
        except:
            row = layout.row()
            row.prop(obj.active_material, "blend_method", text="混合模式")
            row.prop(obj.active_material, "shadow_method", text="阴影模式")
            row.prop(obj.active_material, "show_transparent_back", text="显示背面面片")


        #setup, removal
        row = self.layout.row()
        #row.operator("shaderaddon.objectsetup", text="配置SB着色器")
        row = self.layout.row()
        row.operator("shaderaddon.deletematerial", text="完全删除选定着色器", icon='TRASH')
        # row = self.layout.row()
        # row.operator("shaderaddon.refreshmaterial", text="刷新下拉菜单", icon='FILE_REFRESH')


        #check for steam/fog objects

        if bpy.context.object.active_material:
            if bpy.context.object.active_material.node_tree.nodes.get("SB Fog") is not None or bpy.context.object.active_material.name.startswith("SB Fog"):
                row = layout.row()
                box = layout.box()
                row = box.row()
                row.label(text="体积雾")
                row = layout.row()
                fognode = bpy.context.object.active_material.node_tree.nodes.get("SB Fog")
                row.prop(fognode.inputs[0], "default_value", text="均匀缩放‌‌")
                row = layout.row()
                row.prop(fognode.inputs[1], "default_value", text="色标‌‌")
                row = layout.row()
                row.prop(fognode.inputs[7], "default_value", text="位置")
                row = layout.row()
                row.prop(fognode.inputs[9], "default_value", text="细节‌‌")
                row.prop(fognode.inputs[10], "default_value", text="粗糙度‌‌")
                row = layout.row()
                row.prop(fognode.inputs[11], "default_value", text="噪波空隙度")
                row.prop(fognode.inputs[12], "default_value", text="扭曲强度")
                row = layout.row()
                row.prop(fognode.inputs[2], "default_value", text="雾效最小值")
                row = layout.row()
                row.prop(fognode.inputs[3], "default_value", text="雾效最大值")
                row = layout.row()
                row.prop(fognode.inputs[4], "default_value", text="颜色")
                row = layout.row()
                row.prop(fognode.inputs[5], "default_value", text="遮罩作用域")
                row = layout.row()
                row.prop(fognode.inputs[6], "default_value", text="遮罩限制")
                row = layout.row()
                row.prop(fognode.inputs[8], "default_value", text="遮罩扭曲强度")
                row = layout.row()
                row.prop(fognode.inputs[13], "default_value", text="扭曲作用域")
                row = layout.row()
                row.prop(fognode.inputs[13], "default_value", text="扭曲缩放")
            if bpy.context.object.active_material.node_tree.nodes.get("SB Steam") is not None or bpy.context.object.active_material.name.startswith("SB Steam"):
                row = layout.row()
                box = layout.box()
                row = box.row()
                row.label(text="蒸汽效果")
                row = layout.row()
                steamnode = bpy.context.object.active_material.node_tree.nodes.get("SB Steam")
                row.prop(steamnode.inputs[0], "default_value", text="颜色")
                row = layout.row()
                row.prop(steamnode.inputs[9], "default_value", text="安装路径")
                row = layout.row()
                row.prop(steamnode.inputs[4], "default_value", text="均匀缩放‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[3], "default_value", text="色标‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[1], "default_value", text="蒸汽渐变‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[5], "default_value", text="细节‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[6], "default_value", text="粗糙度‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[7], "default_value", text="扩散范围")
                row = layout.row()
                row.prop(steamnode.inputs[8], "default_value", text="底部")
            if bpy.context.object.active_material.node_tree.nodes.get("SB Godrays") is not None or bpy.context.object.active_material.name.startswith("SB Godrays"):
                row = layout.row()
                box = layout.box()
                row = box.row()
                row.label(text="体积光")
                row = layout.row()
                godnode = bpy.context.object.active_material.node_tree.nodes.get("SB Godrays")
                row.prop(godnode.inputs[10], "default_value", text="颜色")
                row = layout.row()
                row.prop(godnode.inputs[0], "default_value", text="底部衰减")
                row.prop(godnode.inputs[7], "default_value", text="顶部衰减")
                row = layout.row()
                row.prop(godnode.inputs[1], "default_value", text="中心定位")
                row = layout.row()
                row.prop(godnode.inputs[5], "default_value", text="密度1")
                row.prop(godnode.inputs[3], "default_value", text="密度2")
                row = layout.row()
                row.prop(godnode.inputs[2], "default_value", text="限制扩散范围")
                row = layout.row()
                row.prop(godnode.inputs[16], "default_value", text="光束细节")
                row = layout.row()
                row.label(text="---尘埃与细节设置---")
                row = layout.row()
                row.prop(godnode.inputs[12], "default_value", text="启用尘埃粒子？")
                if godnode.inputs[12].default_value > 0.01:
                    row = layout.row()
                    row.prop(godnode.inputs[13], "default_value", text="粒子缩放比例")
                    row.prop(godnode.inputs[15], "default_value", text="粒子尺寸")
                    row = layout.row()
                    row.prop(godnode.inputs[14], "default_value", text="粒子分布定位")
                row = layout.row()
                row.label(text="------动画设置-------")
                row = layout.row()
                row.prop(godnode.inputs[8], "default_value", text="动画随机种子")
                row = layout.row()
                row.prop(godnode.inputs[11], "default_value", text="淡入淡出间隔时间")
                row = layout.row()
                row.prop(godnode.inputs[9], "default_value", text="启用动画")




        if not obj or not obj.active_material:
            return
        

        #check nodes in chain
        nodes = obj.active_material.node_tree.nodes
        if not nodes or nodes[0].type != 'GROUP' or not nodes[0].node_tree.name.startswith("basecolor"):
            return
        

        row = layout.row()
        
        
        row.operator("shaderaddon.opensite", text="给up点个一键三连吧", icon='SCENE')
        row = layout.row()
        row.label(text='--------')
        row = layout.row()
        row.label(text="风格化着色器", icon='WORLD_DATA')

        

        if not obj.active_material.name.startswith("Outline for"):
            #delete effect
            # row = layout.row()
            # row.prop(obj, "node_groups_enum", text="删除特效")
            # row.operator("shaderaddon.deleteeffect", text="删除特效")

            #view effect
            # row = layout.row()
            # row.prop(obj, "node_groups_enum_view", text="视图模式")

            # Add the drop-down menu
            row = layout.row()
            row.prop(context.scene, "my_operator_enum", text="选择要添加的效果")

            if context.scene.my_operator_enum == 'SPLRed' or context.scene.my_operator_enum == 'SPLGreen' or context.scene.my_operator_enum == 'SPLBlue':
                if obj.active_material.node_tree.nodes.get("Stylized Light (Dynamic) - #1") is None:
                    row = layout.row()
                    row.label(text="警告：在添加此内容之前，你必须具有样式化的灯光动态效果")

            if context.scene.my_operator_enum == 'BAKE':
                row = layout.row()
                row.label(text="------------")
                row = layout.row()
                row.label(text="确认模型已展开UV")
                row = layout.row()
                row.prop(context.scene, "bake_name", text="烘焙贴图命名")
                row = layout.row()
                row.prop(context.scene, "user_input_number", text="分辨率")
                row = layout.row()
                row.label(text="待执行烘焙任务列表:")
                
                for node in obj.active_material.node_tree.nodes:
                    if node.type == 'GROUP' and (node.node_tree.name.startswith("TransparentNoise") or node.node_tree.name.startswith("TransparentWorldStrokes")):
                            row = layout.row()
                            row.operator("shaderaddon.baketransparent", text="烘焙透明度通道（与最终烘焙分离")
                            break
                breakvar = False
                for node in obj.active_material.node_tree.nodes:
                    if node.type == 'GROUP' and node.node_tree.name.startswith("SpecularRef"):
                        for subnode in node.node_tree.nodes:
                            if subnode.name == 'Glossy BSDF':
                                row = layout.row()
                                row.operator("shaderaddon.bakespecular", text="烘焙高光反射")
                for node in obj.active_material.node_tree.nodes:
                    if node.type == 'GROUP' and node.node_tree.name.startswith("AmbientOcclusion"):
                        for subnode in node.node_tree.nodes:
                            if subnode.name == 'Ambient Occlusion':
                                row = layout.row()
                                row.operator("shaderaddon.bakeao", text="烘焙环境光遮蔽")
                for node in obj.active_material.node_tree.nodes:
                    if node.type == 'GROUP' and node.node_tree.name.startswith("Diffuse"):
                        for subnode in node.node_tree.nodes:
                            if subnode.name == 'Diffuse BSDF':
                                row = layout.row()
                                row.prop(context.scene, "applied_sld", text="烘焙时应用动态风格化光照？‌")
                                row = layout.row()
                                row.operator("shaderaddon.bakediffuse", text="烘焙漫反射光照‌")
                row = layout.row()
                row.operator("shaderaddon.bakeall", text="开始最终烘焙！")
                for node in obj.active_material.node_tree.nodes:
                    if node.type == 'GROUP' and node.node_tree.name.startswith("CrossHatch"):
                        row = layout.row()
                        row.label(text=f"WARNING: {node.name} is unbakeable, will be removed upon baking")
                    if node.type == 'GROUP' and node.node_tree.name.startswith("TransparentPaint"):
                        row = layout.row()
                        row.label(text=f"WARNING: {node.name} is unbakeable, will be removed upon baking")
                row = layout.row()
                row.label(text="---------")
                row = layout.row()
                row.operator("shaderaddon.saveimagetextures", text=f"Save & Export  '{bpy.context.scene.bake_name}'  Image Textures")
            elif context.scene.my_operator_enum == 'BAKEANIMATED':
                row = layout.row()
                row.prop(context.scene, "bake_name", text="烘焙贴图命名")
                row = layout.row()
                row.prop(context.scene, "user_input_number", text="分辨率")
                # row = layout.row()
                # row.label(text="待执行烘焙任务列表:")
                # for node in obj.active_material.node_tree.nodes:
                #     if node.type == 'GROUP' and node.node_tree.name.startswith("SpecularRef"):
                #         for subnode in node.node_tree.nodes:
                #             if subnode.name == 'Glossy BSDF':
                #                 row = layout.row()
                #                 row.operator("shaderaddon.bakespecular", text="烘焙高光反射")
                # for node in obj.active_material.node_tree.nodes:
                #     if node.type == 'GROUP' and node.node_tree.name.startswith("AmbientOcclusion"):
                #         for subnode in node.node_tree.nodes:
                #             if subnode.name == 'Ambient Occlusion':
                #                 row = layout.row()
                #                 row.operator("shaderaddon.bakeao", text="烘焙环境光遮蔽")
                row = layout.row()
                row.label(text="--------------")
                row = layout.row()
                row.prop(context.scene, "frame_start", text="起始帧‌")
                row = layout.row()
                row.prop(context.scene, "frame_end", text="结束帧")
                row = layout.row()
                row.prop(context.scene, "light_animate_enum", text="启用动态漫反射光照？")
                row = layout.row()
                row.prop(context.scene, "specular_animate_enum", text="启用动态镜面反射？")
                row = layout.row()
                row.prop(context.scene, "processing_speed", text="处理速度（CPU性能越差数值越高）")
                row = layout.row()
                row.operator("shaderaddon.bakeanimationprotocol", text="开始最终烘焙！")
                for node in obj.active_material.node_tree.nodes:
                    if node.type == 'GROUP' and node.node_tree.name.startswith("CrossHatch"):
                        row = layout.row()
                        row.label(text=f"WARNING: {node.name} is unbakeable, will be removed upon baking")
                    if node.type == 'GROUP' and node.node_tree.name.startswith("TransparentPaint"):
                        row = layout.row()
                        row.label(text=f"WARNING: {node.name} is unbakeable, will be removed upon baking")
                row = layout.row()
                row.label(text="---------")
                row = layout.row()
                row.operator("shaderaddon.saveimagetextures", text=f"Save & Export  '{bpy.context.scene.bake_name}'  Image Textures")
            elif context.scene.my_operator_enum == 'BAKENORMALS':
                row = layout.row()
                row.prop(context.scene, "bake_name", text="烘焙贴图命名")
                row = layout.row()
                row.prop(context.scene, "user_input_number", text="分辨率")
                row = layout.row()
                row.label(text="烘焙法线 Requires Stylized Light (Main) Effect")
                for node in obj.active_material.node_tree.nodes:
                    if node.type == 'GROUP' and node.node_tree.name.startswith("Diffuse"): 
                        row = layout.row()
                        row.operator("shaderaddon.bakenormals", text="开始最终烘焙！")
                        break

                if nodes.get('NormalsTextureHelper') is not None:
                    row = layout.row()
                    if nodes.get("Material Output").inputs['Surface'].links[0].from_node.name == 'NormalsTextureHelper':
                        row.operator("shaderaddon.normalspaint", text="停止法线绘制")
                    else:
                        row.operator("shaderaddon.normalspaint", text="开始法线绘制")
                
            else:
                # Add a button to execute the selected operator
                row = layout.row()
                row.operator("shaderaddon.execute_operator", text="添加特效‌")


        # is_show = False
        # if obj.node_groups_enum_view == 'SHOWALL':
        #     is_show = True

        #start traversal
        node = nodes[0]
        nodecount = 0
        while node:
            if node.type == 'OUTPUT_MATERIAL':
                break
            if node.type == 'GROUP':
                nodecount += 1
                group_name = node.name
                prop_name = f"show_{group_name}_section"
                box = layout.box()
                row = box.row()
                row.prop(node, "use_custom_color", text="", icon="TRIA_DOWN" if node.use_custom_color else "TRIA_RIGHT", emboss=False)
                row.label(text=group_name)

                if node.name == 'Base Color':
                    if node.use_custom_color:
                        rgb_node = None
                        for nestednode in node.node_tree.nodes:
                            if nestednode.type == 'RGB':
                                rgb_node = nestednode
                                break
                        if rgb_node.outputs[0].links[0].to_node.name != 'Group Output':
                            return
                        row = layout.row()
                        row.prop(rgb_node.outputs[0], "default_value", text="基准色")
                        row = layout.row()
                        

                if node.name == 'Outline Color':
                    if node.use_custom_color:
                        row = layout.row()
                        rgb_node2 = node.node_tree.nodes['RGB']
                        row.prop(rgb_node2.outputs[0], "default_value", text="轮廓线颜色")
                        outlinemodifier = None
                        for modifier in obj.modifiers:
                            if modifier.name.startswith("SB Outline"):
                                outlinemodifier = modifier
                                break

                        row = layout.row()
                        row.prop(outlinemodifier, "thickness", text="轮廓线厚度")
                        row = layout.row()
                        row.prop(outlinemodifier, "vertex_group", text="顶点组")

                if node.node_tree.name.startswith("LocalGradient"):
                    lgdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    lgdupe.arg1 = node.name
                    localgradienttrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    localgradienttrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="渐变颜色‌")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["realmix"], "blend_type", text="混合模式‌")
                        row = layout.row()
                        row.prop(node.inputs[18], "default_value", text="颜色反转？‌")
                        maprange = node.node_tree.nodes["Map Range"]
                        row = layout.row()
                        row.prop(maprange, "interpolation_type", text="渐变类型‌")
                        row = layout.row()
                        row.prop(node.inputs[12], "default_value", text="卡通色阶步数")

                        #painterly stuff
                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="手绘/扭曲效果强度")
                                
                            if node.node_tree.nodes["DropDown1"].use_custom_color:
                                row = layout.row()
                                distortmix = node.node_tree.nodes["DistortMix"]
                                row.prop(node.inputs[8], "default_value", text="手绘/扭曲效果")
                                row = layout.row()
                                row.prop(node.inputs[17], "default_value", text="噪波/沃罗诺伊纹理切换")
                                row = layout.row()
                                row.prop(node.inputs[9], "default_value", text="手绘扭曲强度")
                                row = layout.row()
                                row.prop(node.inputs[16], "default_value", text="手绘效果缩放（均匀）")
                                
                                row = layout.row()
                                row.prop(node.inputs[10], "default_value", text="手绘效果位置‌")
                        except:
                            row = layout.row()
                            distortmix = node.node_tree.nodes["DistortMix"]
                            row.prop(node.inputs[8], "default_value", text="手绘/扭曲效果")
                            row = layout.row()
                            row.prop(node.inputs[17], "default_value", text="噪波/沃罗诺伊纹理切换")
                            row = layout.row()
                            row.prop(node.inputs[9], "default_value", text="手绘扭曲强度")
                            row = layout.row()
                            row.prop(node.inputs[16], "default_value", text="手绘效果缩放（均匀）")
                            
                            row = layout.row()
                            row.prop(node.inputs[10], "default_value", text="手绘效果位置‌")


                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown2"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown2"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="纹理坐标设置‌")
                            if node.node_tree.nodes["DropDown2"].use_custom_color:
                                #COORDINATES stuff
                                row = layout.row()
                                row.prop(node.inputs[13], "default_value", text="渐变位置")
                                row = layout.row()
                                row.prop(node.inputs[14], "default_value", text="渐变旋转")
                                row = layout.row()
                                row.prop(node.inputs[15], "default_value", text="渐变缩放")
                                row = layout.row()
                                row.prop(node.inputs[23], "default_value", text="钳制‌")
                                row = layout.row()
                                row.prop(node.inputs[4], "default_value", text="物体坐标（默认混合比例）%‌")
                                row = layout.row()
                                row.prop(node.inputs[6], "default_value", text="UV坐标混合比例%‌")
                        except:
                            #COORDINATES stuff
                            row = layout.row()
                            row.label(text="------纹理坐标设置-----")
                            row = layout.row()
                            row.prop(node.inputs[13], "default_value", text="渐变位置")
                            row = layout.row()
                            row.prop(node.inputs[14], "default_value", text="渐变旋转")
                            row = layout.row()
                            row.prop(node.inputs[15], "default_value", text="渐变缩放")
                            row = layout.row()
                            row.prop(node.inputs[23], "default_value", text="钳制‌")
                            row = layout.row()
                            row.prop(node.inputs[4], "default_value", text="物体坐标（默认混合比例）%‌")
                            row = layout.row()
                            row.prop(node.inputs[6], "default_value", text="UV坐标混合比例%‌")

                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown3"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown3"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="遮罩设置")
                            if node.node_tree.nodes["DropDown3"].use_custom_color:
                                row = layout.row()
                                row.template_ID(node.node_tree.nodes["Image Texture"], "image", new="image.new", open="image.open", text="遮罩")
                                row = layout.row()
                                row.prop(node.inputs[19], "default_value", text="启用遮罩？")
                                if node.inputs[19].default_value > 0.01:
                                    row = layout.row()
                                    row.prop(node.inputs[21], "default_value", text="遮罩作用域")
                                    row = layout.row()
                                    row.prop(node.inputs[20], "default_value", text="遮罩缩放")
                                    row = layout.row()
                                    row.prop(node.inputs[22], "default_value", text="遮罩旋转")
                        except:
                            row = layout.row()
                            row.template_ID(node.node_tree.nodes["Image Texture"], "image", new="image.new", open="image.open", text="遮罩")
                            row = layout.row()
                            row.prop(node.inputs[19], "default_value", text="启用遮罩？")
                            if node.inputs[19].default_value > 0.01:
                                row = layout.row()
                                row.prop(node.inputs[21], "default_value", text="遮罩作用域")
                                row = layout.row()
                                row.prop(node.inputs[20], "default_value", text="遮罩缩放")
                                row = layout.row()
                                row.prop(node.inputs[22], "default_value", text="遮罩旋转")

                        #find texture coordinate node
                        tex_coord_node = node.node_tree.nodes["ZhaTexture Coordinate"]
                        
                        # row = layout.row()
                        # row.prop(node.inputs[7], "default_value", text="窗口坐标混合比例%‌")
                        row = layout.row()
                        row.prop(tex_coord_node, "object", text="渐变物体‌")
                        
                
                if node.node_tree.name.startswith("CrossHatch"):
                    # chdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    # chdupe.arg1 = node.name
                    crosshatchtrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    crosshatchtrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        maprange2 = node.node_tree.nodes["Map Range"]
                        row = layout.row()
                        row.prop(maprange2, "interpolation_type", text="混合样式")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="光源滑块/控制器‌")
                        row = layout.row()
                        row.prop(node.inputs[6], "default_value", text="卡通色阶步数")
                        row = layout.row()
                        row.label(text="----高光设置----‌")
                        row = layout.row()
                        row.prop(node.inputs[3], "default_value", text="高光亮度‌")
                        row = layout.row()
                        row.prop(node.inputs[21], "default_value", text="高光着色‌")
                        row = layout.row()
                        row.prop(node.inputs[23], "default_value", text="高光着色影响度‌")
                        row = layout.row()
                        row.label(text="----阴影设置----‌")
                        row = layout.row()
                        row.prop(node.inputs[9], "default_value", text="阴影深度")
                        row = layout.row()
                        row.prop(node.inputs[20], "default_value", text="阴影着色")
                        row = layout.row()
                        row.prop(node.inputs[22], "default_value", text="阴影着色影响度")
                        row = layout.row()
                        row.label(text="---交叉线设置---")
                        row = layout.row()
                        row.prop(node.inputs[10], "default_value", text="交叉线强度")
                        row = layout.row()
                        row.prop(node.inputs[12], "default_value", text="均匀缩放‌‌")
                        row = layout.row()
                        row.prop(node.inputs[14], "default_value", text="交叉线位置‌")
                        row = layout.row()
                        row.prop(node.inputs[15], "default_value", text="细节‌‌")
                        row = layout.row()
                        row.prop(node.inputs[16], "default_value", text="粗糙度‌‌")
                        row = layout.row()
                        row.label(text="---点状色调设置---‌")
                        row = layout.row()
                        row.prop(node.inputs[30], "default_value", text="启用点状色调？‌")
                        if node.inputs[30].default_value > 0.01:
                            row = layout.row()
                            row.prop(node.inputs[31], "default_value", text="颜色反转？‌")
                            row = layout.row()
                            row.prop(node.inputs[32], "default_value", text="均匀缩放‌‌")
                            row = layout.row()
                            row.prop(node.inputs[35], "default_value", text="色标‌‌")
                            row = layout.row()
                            row.prop(node.inputs[33], "default_value", text="点状随机度‌‌")
                            row = layout.row()
                            row.prop(node.inputs[34], "default_value", text="细节‌‌")
                            row = layout.row()
                            row.prop(node.inputs[36], "default_value", text="点状密度限制‌‌‌")
                        row = layout.row()
                        row.label(text="------------------")
                        row = layout.row()
                        row.prop(node.inputs[24], "default_value", text="UV坐标‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[25], "default_value", text="窗口坐标‌‌‌")
                        # row = layout.row()
                        # row.template_ID(node.node_tree.nodes["Normal"], "image", new="image.new", open="image.open", text="法线贴图‌‌‌")
                        # row = layout.row()
                        # row.prop(node.inputs[18], "default_value", text="启用法线贴图？")
                        # row = layout.row()
                        # row.prop(node.inputs[19], "default_value", text="法线贴图强度")
                        # row = layout.row()
                        # row.prop(node.inputs[26], "default_value", text="法线贴图位置")
                        # row = layout.row()
                        # row.prop(node.inputs[26], "default_value", text="法线贴图旋转‌")
                        # row = layout.row()
                        # row.prop(node.inputs[26], "default_value", text="法线贴图缩放‌")
                        if node.node_tree.nodes.get("Diffuse BSDF") is None:
                            row = layout.row()
                            row.operator("shaderaddon.unbakediffuse", text="解除烘焙漫反射光照‌‌")

                if node.node_tree.name.startswith("DiffuseLight") or node.node_tree.name.startswith("AppliedDiff"):
                    # dldupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    # dldupe.arg1 = node.name
                    diffusetrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    diffusetrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        maprange2 = node.node_tree.nodes["Map Range"]
                        row = layout.row()
                        row.prop(maprange2, "interpolation_type", text="混合样式")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="光源滑块/控制器‌")
                        try:
                            if maprange2.interpolation_type == 'LINEAR':
                                row = layout.row()
                                row.prop(node.inputs[42], "default_value", text="锐化光源‌‌")
                        except:
                            row = layout.row()
                        if maprange2.interpolation_type != 'LINEAR':
                            row = layout.row()
                            row.prop(node.inputs[6], "default_value", text="卡通色阶步数")
                        
                        if 1+1 == 2:
                            row = layout.row()
                            row.prop(node.inputs[30], "default_value", text="暗化边缘‌‌")
                            row.prop(node.inputs[29], "default_value", text="影响距离‌‌‌")

                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="高光设置‌‌‌")
                            
                            if node.node_tree.nodes["DropDown1"].use_custom_color:
                                row = layout.row()
                                row.label(text="----高光设置----‌")
                                row = layout.row()
                                row.prop(node.inputs[3], "default_value", text="高光亮度‌")
                                row = layout.row()
                                row.prop(node.inputs[21], "default_value", text="高光着色‌")
                                row = layout.row()
                                row.prop(node.inputs[23], "default_value", text="高光着色影响度‌")
                                row = layout.row()
                                row.prop(node.inputs[1], "default_value", text="色相")
                                row.prop(node.inputs[2], "default_value", text="饱和度")
                                row = layout.row()
                                row.prop(node.inputs[44], "default_value", text="次表面散射‌")
                        except:
                            row = layout.row()
                            row.label(text="----高光设置----‌")
                            row = layout.row()
                            row.prop(node.inputs[3], "default_value", text="高光亮度‌")
                            row = layout.row()
                            row.prop(node.inputs[21], "default_value", text="高光着色‌")
                            row = layout.row()
                            row.prop(node.inputs[23], "default_value", text="高光着色影响度‌")
                            row = layout.row()
                            row.prop(node.inputs[1], "default_value", text="色相")
                            row.prop(node.inputs[2], "default_value", text="饱和度")
                        
                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown2"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown2"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="阴影设置")
                            if node.node_tree.nodes["DropDown2"].use_custom_color:
                                row = layout.row()
                                row.prop(node.inputs[9], "default_value", text="阴影深度")
                                row = layout.row()
                                row.prop(node.inputs[20], "default_value", text="阴影着色")
                                row = layout.row()
                                row.prop(node.inputs[22], "default_value", text="阴影着色影响度")
                                row = layout.row()
                                row.prop(node.inputs[7], "default_value", text="色相")
                                row.prop(node.inputs[8], "default_value", text="饱和度")
                        except:
                            row = layout.row()
                            row.label(text="----阴影设置----‌")
                            row = layout.row()
                            row.prop(node.inputs[9], "default_value", text="阴影深度")
                            row = layout.row()
                            row.prop(node.inputs[20], "default_value", text="阴影着色")
                            row = layout.row()
                            row.prop(node.inputs[22], "default_value", text="阴影着色影响度")
                            row = layout.row()
                            row.prop(node.inputs[7], "default_value", text="色相")
                            row.prop(node.inputs[8], "default_value", text="饱和度")

                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown9"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown9"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="反弹光设置")
                            if node.node_tree.nodes["DropDown9"].use_custom_color:
                                row = layout.row()
                                row.operator("shaderaddon.opensite", text="请升级至专业版")
                        except:
                            print('HI')
                        
                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown3"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown3"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="轮廓光设置")
                            if node.node_tree.nodes["DropDown3"].use_custom_color:
                                # row = layout.row()
                                # row.label(text="请升级至专业版")
                                row = layout.row()
                                row.prop(node.inputs[45], "default_value", text="启用轮廓光（仅限动漫风格）")
                                row = layout.row()
                                row.prop(node.inputs[43], "default_value", text="轮廓光颜色")
                                row = layout.row()
                                row.prop(node.inputs[50], "default_value", text="轮廓光尺寸")
                                row = layout.row()
                                row.prop(node.inputs[47], "default_value", text="轮廓光扩散范围")
                                row = layout.row()
                                row.prop(node.inputs[51], "default_value", text="轮廓光柔化程度")
                        except:
                            print("hi")
                            
                        # try:
                        #     row = layout.row()
                        #     row.prop(node.inputs[43], "default_value", text="轮廓光颜色")
                        #     row = layout.row()
                        #     row.prop(node.inputs[44], "default_value", text="次表面散射‌")
                        #     row = layout.row()
                        #     row.prop(node.inputs[45], "default_value", text="启用轮廓光")
                        #     row = layout.row()
                        #     row.prop(node.inputs[46], "default_value", text="启用金属效果")
                        #     row = layout.row()
                        #     row.prop(node.inputs[47], "default_value", text="轮廓光扩散范围")
                        #     row = layout.row()
                        #     row.prop(node.inputs[48], "default_value", text="金属渐变阶数")
                        #     row = layout.row()
                        #     row.prop(node.inputs[49], "default_value", text="金属扩散范围")
                        # except:
                        #     row = layout.row()

                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown4"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown4"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="金属效果设置")
                            if node.node_tree.nodes["DropDown4"].use_custom_color:
                                row = layout.row()
                                row.prop(node.inputs[46], "default_value", text="金属质感比例%")
                                row = layout.row()
                                row.prop(node.inputs[48], "default_value", text="金属渐变阶数")
                                row = layout.row()
                                row.prop(node.inputs[49], "default_value", text="金属扩散范围")
                        except:
                            print("hi")
                        
                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown5"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown5"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="扭曲设置")
                            if node.node_tree.nodes["DropDown5"].use_custom_color:
                                row = layout.row()
                                row.prop(node.inputs[10], "default_value", text="扭曲强度")
                                row = layout.row()
                                row.prop(node.inputs[11], "default_value", text="噪波/沃罗诺伊纹理切换")
                                row = layout.row()
                                row.prop(node.inputs[12], "default_value", text="均匀缩放‌‌")
                                row = layout.row()
                                row.prop(node.inputs[13], "default_value", text="色标‌‌")
                                row = layout.row()
                                row.prop(node.inputs[17], "default_value", text="扭曲旋转")
                                row = layout.row()
                                row.prop(node.inputs[14], "default_value", text="交叉线位置‌")
                                row = layout.row()
                                row.prop(node.inputs[15], "default_value", text="细节‌‌")
                                row = layout.row()
                                row.prop(node.inputs[16], "default_value", text="粗糙度‌‌")
                                row = layout.row()
                                row.prop(node.inputs[24], "default_value", text="使用物体坐标（扭曲）")
                                row = layout.row()
                                row.prop(node.inputs[25], "default_value", text="使用UV坐标（扭曲）")
                        except:
                            row = layout.row()
                            row.label(text="扭曲设置")
                            row = layout.row()
                            row.prop(node.inputs[10], "default_value", text="扭曲强度")
                            row = layout.row()
                            row.prop(node.inputs[11], "default_value", text="噪波/沃罗诺伊纹理切换")
                            row = layout.row()
                            row.prop(node.inputs[12], "default_value", text="均匀缩放‌‌")
                            row = layout.row()
                            row.prop(node.inputs[13], "default_value", text="色标‌‌")
                            row = layout.row()
                            row.prop(node.inputs[17], "default_value", text="扭曲旋转")
                            row = layout.row()
                            row.prop(node.inputs[14], "default_value", text="交叉线位置‌")
                            row = layout.row()
                            row.prop(node.inputs[15], "default_value", text="细节‌‌")
                            row = layout.row()
                            row.prop(node.inputs[16], "default_value", text="粗糙度‌‌")
                            row = layout.row()
                        
                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown6"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown6"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="绘画风格效果设置")
                            if node.node_tree.nodes["DropDown6"].use_custom_color:
                                if 1+1 == 2:
                                    row.label(text="-------绘画效果--------")
                                    row = layout.row()
                                    row.prop(node.inputs[31], "default_value", text="启用绘画效果？")
                                    if node.inputs[31].default_value > 0.01:
                                        row = layout.row()
                                        row.prop(node.inputs[41], "default_value", text="笔触缩放（均匀）")
                                        row = layout.row()
                                        row.prop(node.inputs[33], "default_value", text="笔触缩放")
                                        row = layout.row()
                                        row.prop(node.inputs[34], "default_value", text="扭曲通道#1‌")
                                        row.prop(node.inputs[40], "default_value", text="扭曲通道#2")
                                        row = layout.row()
                                        row.prop(node.inputs[35], "default_value", text="平滑笔触‌")
                                        row.prop(node.inputs[36], "default_value", text="笔触对比度‌‌")
                                        row = layout.row()
                                        row.template_ID(node.node_tree.nodes["Image Texture"], "image", new="image.new", open="image.open", text="笔触贴图‌‌")
                                        row = layout.row()
                                        row.prop(node.inputs[37], "default_value", text="笔触贴图缩放‌‌‌")
                                        try:
                                            row = layout.row()
                                            row.label(text="额外破碎效果‌‌‌")
                                            row.prop(node.inputs[52], "default_value", text=" ")
                                            row.prop(node.inputs[53], "default_value", text=" ")
                                        except:
                                            print('none')
                        except:
                            row.label(text="-------绘画效果--------")
                            row = layout.row()
                            row.prop(node.inputs[31], "default_value", text="启用绘画效果？")
                            if node.inputs[31].default_value > 0.01:
                                row = layout.row()
                                row.prop(node.inputs[41], "default_value", text="笔触缩放（均匀）")
                                row = layout.row()
                                row.prop(node.inputs[33], "default_value", text="笔触缩放")
                                row = layout.row()
                                row.prop(node.inputs[34], "default_value", text="扭曲通道#1‌")
                                row.prop(node.inputs[40], "default_value", text="扭曲通道#2")
                                row = layout.row()
                                row.prop(node.inputs[35], "default_value", text="平滑笔触‌")
                                row.prop(node.inputs[36], "default_value", text="笔触对比度‌‌")
                                row = layout.row()
                                row.template_ID(node.node_tree.nodes["Image Texture"], "image", new="image.new", open="image.open", text="笔触贴图‌‌")
                                row = layout.row()
                                row.prop(node.inputs[37], "default_value", text="笔触贴图缩放‌‌‌")

                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown7"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown7"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="坐标与法线贴图")
                            if node.node_tree.nodes["DropDown7"].use_custom_color:
                                row = layout.row()
                                row.template_ID(node.node_tree.nodes["Normal"], "image", new="image.new", open="image.open", text="法线贴图‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[18], "default_value", text="启用法线贴图？")
                                if node.inputs[18].default_value > 0.01:
                                    row = layout.row()
                                    row.prop(node.inputs[19], "default_value", text="法线贴图强度")
                                    row = layout.row()
                                    row.prop(node.inputs[26], "default_value", text="法线贴图位置")
                                    row = layout.row()
                                    row.prop(node.inputs[27], "default_value", text="法线贴图旋转‌")
                                    row = layout.row()
                                    row.prop(node.inputs[28], "default_value", text="法线贴图缩放‌")
                        except:
                            row = layout.row()
                            row.label(text="----------------------")
                            row = layout.row()
                            row.prop(node.inputs[24], "default_value", text="物体坐标（凹凸）")
                            row = layout.row()
                            row.prop(node.inputs[25], "default_value", text="UV坐标（凹凸）")
                            row = layout.row()
                            row.template_ID(node.node_tree.nodes["Normal"], "image", new="image.new", open="image.open", text="法线贴图‌‌‌")
                            row = layout.row()
                            row.prop(node.inputs[18], "default_value", text="启用法线贴图？")
                            if node.inputs[18].default_value > 0.01:
                                row = layout.row()
                                row.prop(node.inputs[19], "default_value", text="法线贴图强度")
                                row = layout.row()
                                row.prop(node.inputs[26], "default_value", text="法线贴图位置")
                                row = layout.row()
                                row.prop(node.inputs[27], "default_value", text="法线贴图旋转‌")
                                row = layout.row()
                                row.prop(node.inputs[28], "default_value", text="法线贴图缩放‌")
                        
                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown8"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown8"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="遮罩")
                            if node.node_tree.nodes["DropDown8"].use_custom_color:
                                row = layout.row()
                                row.label(text="遮罩")
                                row = layout.row()
                                row.template_ID(node.node_tree.nodes["SubtractLight"], "image", new="image.new", open="image.open", text="移除光源")
                                row.prop(node.inputs[39], "default_value", text="启用？")
                                row = layout.row()
                                row.template_ID(node.node_tree.nodes["AddLight"], "image", new="image.new", open="image.open", text="添加光源")
                                row.prop(node.inputs[38], "default_value", text="启用？")
                        except:
                            row = layout.row()
                            row.label(text="遮罩")
                            row = layout.row()
                            row.template_ID(node.node_tree.nodes["SubtractLight"], "image", new="image.new", open="image.open", text="移除光源")
                            row.prop(node.inputs[39], "default_value", text="启用？")
                            row = layout.row()
                            row.template_ID(node.node_tree.nodes["AddLight"], "image", new="image.new", open="image.open", text="添加光源")
                            row.prop(node.inputs[38], "default_value", text="启用？")
                        
                        if node.node_tree.nodes.get("Diffuse BSDF") is None and not node.node_tree.name.startswith("AppliedDiff"):
                            row = layout.row()
                            row.operator("shaderaddon.unbakediffuse", text="解除烘焙漫反射光照‌‌")

                if node.node_tree.name.startswith("SpecularReflection"):
                    return
                
                
                if node.node_tree.name.startswith("EdgeDetect"):
                    return
                    

                if node.node_tree.name.startswith("ColoredEdges"):
                    return
                    

                if node.node_tree.name.startswith("SunObject"):
                    # sodupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    # sodupe.arg1 = node.name
                    sunobjecttrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    sunobjecttrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.node_tree.nodes["Map Range"], "interpolation_type", text="样式")
                        row = layout.row()
                        row.prop(node.inputs[6], "default_value", text="色阶")
                        # last_character = node.name[-1]
                        # number = int(last_character)
                        for modifier in obj.modifiers:
                            if modifier.name.startswith("SB Sun"):
                                if node.node_tree.nodes["Attribute"].attribute_name != modifier.node_group.nodes["Store Named Attribute"].inputs[2].default_value:
                                    continue
                                number = 0
                                if number == 0:
                                    subd = modifier.node_group.nodes["Subdivision Surface"]
                                    row = layout.row()
                                    row.prop(subd.inputs[1], "default_value", text="表面细分级数")
                                    row = layout.row()
                                    row.prop(modifier.node_group.nodes["Subdivide Mesh"].inputs[1], "default_value", text="细分网格")
                                    row = layout.row()
                                    row.prop(modifier.node_group.nodes["Combine XYZ"].inputs[0], "default_value", text="X 轴太阳方向")
                                    row = layout.row()
                                    row.prop(modifier.node_group.nodes["Combine XYZ"].inputs[1], "default_value", text="Y 轴太阳方向")
                                    row = layout.row()
                                    row.prop(modifier.node_group.nodes["Combine XYZ"].inputs[2], "default_value", text="Z 轴太阳方向")
                        row = layout.row()
                        row.prop(node.inputs[7], "default_value", text="阴影深度")
                        row = layout.row()
                        row.prop(node.inputs[8], "default_value", text="高光亮度值‌")
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="强度（动态）‌")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="强度（稳定）‌")
                        row = layout.row()
                        row.prop(node.inputs[13], "default_value", text="阴影色彩化‌")
                        row = layout.row()
                        row.prop(node.inputs[14], "default_value", text="阴影染色强度‌")
                        row = layout.row()
                        row.prop(node.inputs[15], "default_value", text="高光色彩化‌")
                        row = layout.row()
                        row.prop(node.inputs[16], "default_value", text="高光染色强度‌")
                        row = layout.row()
                        row.prop(node.inputs[9], "default_value", text="阴影色相‌‌")
                        row = layout.row()
                        row.prop(node.inputs[10], "default_value", text="阴影饱和度‌‌")
                        row = layout.row()
                        row.prop(node.inputs[11], "default_value", text="高光色相‌‌")
                        row = layout.row()
                        row.prop(node.inputs[12], "default_value", text="高光饱和度‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[5], "default_value", text="粗糙度‌‌")
                        row.template_ID(node.node_tree.nodes["Image Texture"], "image", new="image.new", open="image.open", text="遮罩")
                        row = layout.row()
                        row.prop(node.inputs[17], "default_value", text="启用遮罩？")


                if node.node_tree.name.startswith("LightObject"):
                    # lodupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    # lodupe.arg1 = node.name
                    lightobjecttrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    lightobjecttrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        # row = layout.row()
                        # row.prop(node.inputs[9], "default_value", text="光照影响范围‌‌‌‌")
                        # last_character = node.name[-1]
                        # number = int(last_character)
                        row = layout.row()
                        row.prop(node.node_tree.nodes["Map Range"], "interpolation_type", text="样式")
                        try:
                            for modifier in obj.modifiers:
                                if modifier.name.startswith("SB Geono"):
                                    if node.node_tree.nodes["Attribute"].attribute_name != modifier.node_group.nodes["Store Named Attribute"].inputs[2].default_value:
                                        continue
                                    number = 0
                                    if number == 0:
                                        row = layout.row()
                                        row.prop(modifier.node_group.nodes["IMPORTANT MATH"].inputs[1], "default_value", text="光源强度滑杆‌")
                                        if node.node_tree.nodes["Map Range"].interpolation_type == 'LINEAR':
                                            row = layout.row()
                                            row.prop(node.inputs[12], "default_value", text="锐度")
                                        else:
                                            row = layout.row()
                                            row.prop(node.inputs[7], "default_value", text="色阶")
                                        row = layout.row()
                                        row.prop(modifier.node_group.nodes["Subdivision Surface"].inputs[1], "default_value", text="表面细分级数‌")
                                        row = layout.row()
                                        row.prop(modifier.node_group.nodes["Subdivide Mesh"].inputs[1], "default_value", text="Subdivide Mesh Levels")
                                        row = layout.row()
                                        row.prop(modifier.node_group.nodes["Object Info"].inputs[0], "default_value", text="光源物体（必须为网格）")
                        except:
                            joe = 'lol'

                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown2"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown2"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="高光设置‌‌‌")
                        if node.node_tree.nodes["DropDown2"].use_custom_color:
                            row = layout.row()
                            row.prop(node.inputs[1], "default_value", text="高光亮度值‌")
                            row = layout.row()
                            row.prop(node.inputs[13], "default_value", text="高光着色‌")
                            row = layout.row()
                            row.prop(node.inputs[14], "default_value", text="高光着色‌")
                            row = layout.row()
                            row.prop(node.inputs[2], "default_value", text="色相")
                            row.prop(node.inputs[3], "default_value", text="饱和度")


                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="阴影设置")
                        if node.node_tree.nodes["DropDown1"].use_custom_color:
                            
                            row = layout.row()
                            row.prop(node.inputs[4], "default_value", text="阴影深度")
                            row = layout.row()
                            row.prop(node.inputs[16], "default_value", text="阴影着色")
                            row = layout.row()
                            row.prop(node.inputs[17], "default_value", text="阴影着色影响度")
                            row = layout.row()
                            row.prop(node.inputs[5], "default_value", text="色相")
                            row.prop(node.inputs[6], "default_value", text="饱和度")

                        
                        
                        # row = layout.row()
                        # row.prop(node.inputs[8], "default_value", text="粗糙度‌‌")
                        # row = layout.row()
                        
                        # row.prop(node.inputs[10], "default_value", text="强度（动态）‌")
                        # last_character = node.name[-1]
                        # number = int(last_character)
                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown3"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown3"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="绘画风格设置‌")
                        if node.node_tree.nodes["DropDown3"].use_custom_color:
                            try:
                                for modifier in obj.modifiers:
                                    if modifier.name.startswith("SB Geono"):
                                        if node.node_tree.nodes["Attribute"].attribute_name != modifier.node_group.nodes["Store Named Attribute"].inputs[2].default_value:
                                            continue
                                        number = 0
                                        if number == 0:
                                            # row = layout.row()
                                            # row.prop(modifier.node_group.nodes["Object Info"].inputs[0], "default_value", text="光源物体（必须为网格）")
                                            # row = layout.row()
                                            # row.prop(modifier.node_group.nodes["Mix"].inputs[0], "default_value", text="扭曲‌")
                                            # row = layout.row()
                                            # row.prop(modifier.node_group.nodes["Noise Texture"].inputs[2], "default_value", text="色标‌‌")
                                            # row = layout.row()
                                            # row.prop(modifier.node_group.nodes["Noise Texture"].inputs[3], "default_value", text="细节‌‌")
                                            # row = layout.row()
                                            # row.prop(modifier.node_group.nodes["Noise Texture"].inputs[4], "default_value", text="粗糙度‌‌")
                                            row = layout.row()
                                            row = layout.row()
                                            row.prop(modifier.node_group.nodes["painterlymix"].inputs[0], "default_value", text="启用绘画效果？")
                                            if modifier.node_group.nodes["painterlymix"].inputs[0].default_value > 0.01:
                                                row = layout.row()
                                                row.label(text="------绘画效果------‌")
                                                row = layout.row()
                                                row.prop(modifier.node_group.nodes["Voronoi Texture"].inputs[2], "default_value", text="色标‌‌")
                                                row = layout.row()
                                                row.prop(modifier.node_group.nodes["Mix.002"].inputs[0], "default_value", text="破碎效果#1‌")
                                                row = layout.row()
                                                row.prop(modifier.node_group.nodes["timmy"].inputs[2], "default_value", text="破碎效果#2‌‌")
                                                row = layout.row()
                                                row.label(text="-----------------------------")
                            except:
                                joe = 'lasoutis'
                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown4"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown4"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="遮罩设置")
                        if node.node_tree.nodes["DropDown4"].use_custom_color:
                            row = layout.row()
                            row.template_ID(node.node_tree.nodes["Image Texture"], "image", new="image.new", open="image.open", text="移除光源")
                            row = layout.row()
                            row.prop(node.inputs[15], "default_value", text="启用遮罩？")
                            try:
                                row = layout.row()
                                row.template_ID(node.node_tree.nodes["ImgTex2"], "image", new="image.new", open="image.open", text="添加光源")
                                row = layout.row()
                                row.prop(node.inputs[18], "default_value", text="启用遮罩？")
                            except:
                                print("DONE")






                if node.node_tree.name.startswith("CircularLight"):
                    return
                
                if node.node_tree.name.startswith("RedLightSAS"):
                    redlightdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    redlightdupe.arg1 = node.name
                    redlighttrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    redlighttrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.node_tree.nodes['zhaRange'], "interpolation_type", text="混合样式")
                        if node.node_tree.nodes['zhaRange'].interpolation_type == 'STEPPED':
                            row = layout.row()
                            row.prop(node.node_tree.nodes['zhaXYZ3'].inputs[0], "default_value", text="色阶")
                        row = layout.row()
                        row.prop(node.node_tree.nodes['zhaValue'].outputs[0], "default_value", text="亮度")
                        row = layout.row()
                        row.prop(node.node_tree.nodes['zhaHSV'].inputs[1], "default_value", text="饱和度")
                        row.prop(node.node_tree.nodes['zhaHSV'].inputs[0], "default_value", text="色相")
                        row = layout.row()
                        row.prop(node.node_tree.nodes['zhaMix'].inputs[7], "default_value", text="色调叠加")
                        row = layout.row()
                        row.prop(node.node_tree.nodes['zhaMix'].inputs[0], "default_value", text="色调强度")
                        row = layout.row()
                        row.prop(node.node_tree.nodes['zhaXYZ1'].inputs[0], "default_value", text="扩散范围")
                        row.prop(node.node_tree.nodes['zhaXYZ2'].inputs[0], "default_value", text="锐度")
                        row = layout.row()
                        row.prop(node.node_tree.nodes['zhaRamp'].color_ramp.elements[0], "position", text="暗部遮蔽强化（调高此值）")
                        row = layout.row()
                        row.prop(node.node_tree.nodes['zhaRamp'].color_ramp.elements[1], "position", text="亮区锐化弱化（调低此值）")
                
                if node.node_tree.name.startswith("ColoredCircular"):
                    return
                    

                if node.node_tree.name.startswith("TransparentPaint"):
                    tpdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    tpdupe.arg1 = node.name
                    transparentpainttrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    transparentpainttrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        overlaytexture = node.node_tree.nodes["Important Texture"]
                        row.template_ID(overlaytexture, "image", open="image.open", text="纹理‌")
                        row = layout.row()
                        row.prop(node.inputs[6], "default_value", text="影响边缘？‌")
                        row = layout.row()
                        row.prop(node.inputs[5], "default_value", text="边缘混合强度‌")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="边缘强度‌")
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="全局透明度‌")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["Important Ramp"].color_ramp.elements[0], "position", text="钳制最小值‌")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["Important Ramp"].color_ramp.elements[1], "position", text="钳制最大值‌")
                        row = layout.row()
                        row.prop(node.inputs[9], "default_value", text="纹理缩放 (X)")
                        row = layout.row()
                        row.prop(node.inputs[10], "default_value", text="纹理缩放 (Y)")
                        row = layout.row()
                        row.prop(node.inputs[11], "default_value", text="纹理缩放 (Z)")
                        row = layout.row()
                        row.prop(node.inputs[7], "default_value", text="纹理位置‌")
                        row = layout.row()
                        row.prop(node.inputs[8], "default_value", text="纹理旋转‌")
                        row = layout.row()
                        row.prop(node.inputs[12], "default_value", text="窗口/UV坐标切换‌")
                        row = layout.row()
                        row.label(text="遮罩：‌")
                        row = layout.row()
                        row.template_ID(node.node_tree.nodes["Mask"], "image", new="image.new", open="image.open")
                        row = layout.row()
                        row.prop(node.inputs[13], "default_value", text="启用遮罩‌")
                        row = layout.row()
                        row.label(text="---毛发设置---")
                        row = layout.row()
                        row.prop(node.inputs[14], "default_value", text="启用毛发？")
                        if node.inputs[14].default_value > 0.01:
                            row = layout.row()
                            row.prop(node.inputs[16], "default_value", text="毛发束缩放")
                            row = layout.row()
                            row.prop(node.inputs[17], "default_value", text="毛发扭曲")
                            row = layout.row()
                            row.prop(node.inputs[15], "default_value", text="毛发束钳制 (1)")
                            row = layout.row()
                            row.prop(node.inputs[24], "default_value", text="毛发束钳制 (2)")
                            row = layout.row()
                            row.prop(node.inputs[25], "default_value", text="毛发束钳制 (3)")
                            row = layout.row()
                            row.prop(node.inputs[26], "default_value", text="毛发束钳制 (4)")
                            row = layout.row()
                            row.prop(node.inputs[18], "default_value", text="启用高光？")
                            row = layout.row()
                            row.prop(node.inputs[23], "default_value", text="高光颜色")
                            row = layout.row()
                            row.prop(node.inputs[19], "default_value", text="粗糙度‌‌")
                            row = layout.row()
                            row.prop(node.inputs[20], "default_value", text="发丝高光缩放‌‌‌")
                            row = layout.row()
                            row.prop(node.inputs[21], "default_value", text="高光强度")
                            row = layout.row()
                            row.prop(node.inputs[22], "default_value", text="发丝高光扭曲‌‌‌")

                

                if node.node_tree.name.startswith("AmbientOcclusion"):
                    aodupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    aodupe.arg1 = node.name
                    aotrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    aotrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        if obj.active_material.blend_method == 'BLEND':
                            row = layout.row()
                            row.label(text="警告：混合模式需切换为Alpha哈希或不透明模式，Alpha混合无法与环境光遮蔽效果协同工作")
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="环境光遮蔽强度")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["ZhaRamp"].color_ramp.elements[1], "position", text="AO渐变控制滑杆")
                        if node.node_tree.nodes.get("Ambient Occlusion") is not None:
                            row = layout.row()
                            row.prop(node.inputs[2], "default_value", text="AO影响距离*")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["ImportantRange"].inputs[1], "default_value", text="锐利度‌")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["ZhaRamp"].color_ramp.elements[0], "color", text="AO颜色")
                        drawmaskAO = node.node_tree.nodes["Mask"]
                        row = layout.row()
                        row.template_ID(drawmaskAO, "image", new="image.new", open="image.open", text="遮罩")
                        row = layout.row()
                        row.prop(node.inputs[3], "default_value", text="环境光遮蔽遮罩影响‌‌‌")
                        if node.node_tree.nodes.get("Ambient Occlusion") is None:
                            row = layout.row()
                            row.operator("shaderaddon.unbakeao", text="清除AO烘焙")

                if node.node_tree.name.startswith("VertexPaint"):
                    vpdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    vpdupe.arg1 = node.name
                    vertextrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    vertextrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.operator("geometry.color_attribute_add", text="添加颜色组‌‌‌")
                        row.prop(node.node_tree.nodes["Color Attribute"], "layer_name", text="颜色属性‌‌‌")
                        row = layout.row()
                        imgtexture = node.node_tree.nodes["ImportantTexture"]
                        row.template_ID(imgtexture, "image", open="image.open", text="选择绘画纹理‌‌‌‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[8], "default_value", text="绘画纹理影响‌‌‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[3], "default_value", text="X 轴缩放")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="Y 轴缩放")
                        row = layout.row()
                        row.prop(node.inputs[5], "default_value", text="Z 轴缩放")
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="交叉线位置‌")
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="扭曲旋转")
                        row = layout.row()
                        row.prop(node.inputs[9], "default_value", text="UV坐标‌‌‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[10], "default_value", text="窗口坐标‌‌‌‌")
                        
                if node.node_tree.name.startswith("SingleColor"):
                    scdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    scdupe.arg1 = node.name
                    singlecolortrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    singlecolortrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.node_tree.nodes["Mix"], "blend_type", text="混合模式")
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="颜色")
                        row = layout.row()
                        row.template_ID(node.node_tree.nodes["Image Texture"], "image", new="image.new", open="image.open", text="绘制")

                if node.node_tree.name.startswith("AddCurvature"):
                    curvdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    curvdupe.arg1 = node.name
                    curvtrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    curvtrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.label(text="确认模型已展开UV")
                        row = layout.row()
                        row.prop(context.scene, "user_input_number", text="分辨率")
                        row = layout.row()
                        row.prop(context.scene, "hardsurface", text="是否为硬表面模型？")
                        row = layout.row()
                        row.prop(context.scene, "curvaturelevels", text="细节层级")
                        if node.node_tree.nodes.get("CurvatureHelper").image is not None:
                            row = layout.row()
                            row.operator("shaderaddon.bakecurvature", text="重新计算曲率‌‌‌‌‌‌‌")
                        else:
                            row = layout.row()
                            row.operator("shaderaddon.bakecurvature", text="计算曲率‌‌")
                        if node.node_tree.nodes.get("CurvatureHelper").image is not None:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="曲率主设置")
                            if node.node_tree.nodes["DropDown1"].use_custom_color:
                                row = layout.row()
                                row.prop(node.inputs[4], "default_value", text="明度（亮部）")
                                row = layout.row()
                                row.prop(node.inputs[1], "default_value", text="明度（暗部）")
                                row = layout.row()
                                row.prop(node.inputs[5], "default_value", text="饱和度")
                                row.prop(node.inputs[6], "default_value", text="色相")
                                row = layout.row()
                                row.prop(node.inputs[7], "default_value", text="扩散范围")
                                row = layout.row()
                                row.prop(node.inputs[8], "default_value", text="锐度")
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown2"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown2"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="艺术化扭曲")
                            if node.node_tree.nodes["DropDown2"].use_custom_color:
                                row = layout.row()
                                row.operator("shaderaddon.opensite", text="请升级专业版")
                                    

                if node.node_tree.name.startswith("ObjectRandomize"):
                    ordupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    ordupe.arg1 = node.name
                    randomizetrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    randomizetrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.label(text="基于此材质的物体HSV随机化")
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="色相 (Min)")
                        row.prop(node.inputs[3], "default_value", text="色相 (Max)")
                        row = layout.row()
                        row.prop(node.inputs[8], "default_value", text="色相随机种子")
                        row = layout.row()
                        row.prop(node.inputs[6], "default_value", text="明度 (Min)")
                        row.prop(node.inputs[7], "default_value", text="明度 (Max)")
                        row = layout.row()
                        row.prop(node.inputs[9], "default_value", text="明度随机种子")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="饱和度 (Min)")
                        row.prop(node.inputs[5], "default_value", text="饱和度 (Max)")
                        row = layout.row()
                        row.prop(node.inputs[10], "default_value", text="饱和度随机种子")

                if node.node_tree.name.startswith("FinalHSL"):
                    hsldupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    hsldupe.arg1 = node.name
                    hsltrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    hsltrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="色相")
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="饱和度")
                        row = layout.row()
                        row.prop(node.inputs[3], "default_value", text="Value")
                        row = layout.row()
                        row.template_ID(node.node_tree.nodes["Image Texture"], "image", new="image.new", open="image.open")
                        row = layout.row()
                        row.prop(node.inputs[5], "default_value", text="启用遮罩？")
                        row = layout.row()
                        row.prop(node.inputs[6], "default_value", text="反转遮罩？")
                        # if node.inputs[5].default_value > 0.0:
                        #     try:
                        #         row = layout.row()
                        #         row.prop(node.node_tree.nodes["Map Range"].inputs[1], "default_value", text="锐利度‌")
                        #     except:
                        #         print("Done")

                if node.node_tree.name.startswith("HairCurves"):
                    return
                    hairtrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    hairtrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.node_tree.nodes["Important Range"], "interpolation_type", text="样式")
                        if node.node_tree.nodes["Important Range"].interpolation_type == 'STEPPED':
                            row = layout.row()
                            row.prop(node.inputs[16], "default_value", text="色阶")
                        row = layout.row()
                        row.prop(node.inputs[15], "default_value", text="扩散范围")
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="位置‌‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="色标‌‌")
                        row = layout.row()
                        row.label(text="颜色组：")
                        row = layout.row()
                        row.prop(node.inputs[5], "default_value", text="亮度")
                        row = layout.row()
                        row.prop(node.inputs[6], "default_value", text="色相")
                        row.prop(node.inputs[7], "default_value", text="饱和度")
                        row = layout.row()
                        if node.node_tree.nodes["Color Ramp"].color_ramp.interpolation == 'CONSTANT':
                            row.prop(node.node_tree.nodes["Color Ramp"].color_ramp.elements[1], "position", text="Clamp Bottom")
                        else:
                            row.prop(node.node_tree.nodes["Color Ramp"].color_ramp.elements[0], "position", text="Clamp Bottom")
                        row.prop(node.node_tree.nodes["Color Ramp"].color_ramp.elements[2], "position", text="Clamp Top")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="扭曲旋转")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="扭曲/线条")
                        if node.node_tree.nodes["DropDown1"].use_custom_color:
                            row = layout.row()
                            row.prop(node.inputs[9], "default_value", text="Line Clamp")
                            row = layout.row()
                            row.prop(node.inputs[11], "default_value", text="色标‌‌")
                            row = layout.row()
                            row.prop(node.inputs[10], "default_value", text="均匀缩放‌‌")
                            row = layout.row()
                            row.prop(node.inputs[12], "default_value", text="细节‌‌")
                            row = layout.row()
                            row.prop(node.inputs[13], "default_value", text="粗糙度‌‌")
                            row = layout.row()
                            row.prop(node.inputs[14], "default_value", text="扭曲强度")


                if node.node_tree.name.startswith("BrushStrokes"):
                    return
                    

                if node.node_tree.name.startswith("RGBContrast"):
                    rgbdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    rgbdupe.arg1 = node.name
                    rgbtrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    rgbtrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="暗部对比度")
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="常规对比度")
                        row = layout.row()
                        row.prop(node.inputs[3], "default_value", text="高亮对比度")

                if node.node_tree.name.startswith("TexturePaint"):
                    paintdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    paintdupe.arg1 = node.name
                    texturepainttrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    texturepainttrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.label(text=("MAKE SURE ALPHA COLOR IS SET TO 0 WHEN ADDING TEXTURE"))
                        drawtexture1 = node.node_tree.nodes["Main"]
                        drawmask1 = node.node_tree.nodes["Mask"]
                        row = layout.row()
                        row.template_ID(drawtexture1, "image", new="image.new", open="image.open", text="绘制纹理")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["ImportantMix"], "blend_type", text="混合模式")
                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="遮罩设置")
                            if node.node_tree.nodes["DropDown1"].use_custom_color:
                                row = layout.row()
                                row.template_ID(drawmask1, "image", new="image.new", open="image.open", text="遮罩")
                                row = layout.row()
                                row.prop(node.inputs[2], "default_value", text="启用遮罩？")
                                # row = layout.row()
                                # row.prop(node.inputs[3], "default_value", text="遮罩作用域")
                                # row = layout.row()
                                # row.prop(node.inputs[4], "default_value", text="遮罩旋转")
                                # row = layout.row()
                                # row.prop(node.inputs[5], "default_value", text="遮罩缩放")
                        except:
                            print("failed")
                            
                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown2"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown2"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="Paint in Softwares")
                            if node.node_tree.nodes["DropDown2"].use_custom_color:
                                row = layout.row()
                                row.prop(context.preferences.filepaths, "image_editor")
                                row = layout.row()
                                row.prop(context.scene.tool_settings.image_paint, "screen_grab_size")
                                row = layout.row()
                                expaint = row.operator("shaderaddon.externalpaint", text="Open Software")
                                expaint.arg1 = node.node_tree.nodes['Main'].image.name
                                row.operator("image.project_apply", text="应用‌‌‌‌‌")
                        except:
                            print("failed")
                                
                
                if node.node_tree.name.startswith("OverallTexture"):
                    otdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    otdupe.arg1 = node.name
                    overalltrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    overalltrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.node_tree.nodes["ImportantMix"], "blend_type", text="混合模式")
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="强度‌‌‌‌‌")
                        row = layout.row()
                        row.template_ID(node.node_tree.nodes["Image Texture"], "image", open="image.open", text="纹理‌")
                        row = layout.row()
                        row.prop(node.inputs[3], "default_value", text="交叉线位置‌")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="扭曲旋转")
                        row = layout.row()
                        row.prop(node.inputs[5], "default_value", text="X Scale")
                        row = layout.row()
                        row.prop(node.inputs[6], "default_value", text="Y Scale")
                        row = layout.row()
                        row.prop(node.inputs[7], "default_value", text="Z Scale")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["Vect"].inputs[0], "default_value", text="UV/窗口坐标切换‌")
                        row = layout.row()
                        row.template_ID(node.node_tree.nodes["ImportantTexture"], "image", new="image.new", open="image.open", text="遮罩")
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="启用遮罩？")

                if node.node_tree.name.startswith("StylizedFoam"):
                    return
                    stfoamdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    stfoamdupe.arg1 = node.name
                    stfoamtrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    stfoamtrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.node_tree.nodes["ImportantRange"], "interpolation_type", text="样式")
                        row = layout.row()
                        row.prop(node.inputs[10], "default_value", text="色阶")
                        row = layout.row()
                        row.prop(node.inputs[8], "default_value", text="泡沫扩散‌‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[6], "default_value", text="泡沫颜色‌‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[9], "default_value", text="设为最大值‌‌‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="泡沫位置‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="泡沫缩放‌‌")
                        row = layout.row()
                        row.prop(node.inputs[3], "default_value", text="泡沫细节‌")
                        row = layout.row()
                        row.prop(node.inputs[12], "default_value", text="绘画扭曲影响")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="扭曲缩放（均匀）")
                        row = layout.row()
                        row.prop(node.inputs[5], "default_value", text="扭曲缩放")
                        row = layout.row()
                        row.prop(node.inputs[7], "default_value", text="动画化绘画扭曲")
                        row = layout.row()
                        row.prop(node.inputs[11], "default_value", text="UV/生成坐标切换")
                        row = layout.row()
                        row.template_ID(node.node_tree.nodes["Image Texture"], "image", new="image.new", open="image.open", text="遮罩")
                        row = layout.row()
                        row.prop(node.inputs[13], "default_value", text="启用遮罩？")
                        row = layout.row()
                        row.prop(node.inputs[14], "default_value", text="遮罩作用域")
                        row = layout.row()
                        row.prop(node.inputs[15], "default_value", text="遮罩旋转")
                        row = layout.row()
                        row.prop(node.inputs[16], "default_value", text="遮罩缩放")

                if node.node_tree.name.startswith("TransparentWorld"):
                    twdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    twdupe.arg1 = node.name
                    twtrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    twtrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="透明度总量‌")
                        row = layout.row()
                        row.prop(node.inputs[3], "default_value", text="颜色反转？‌")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="Masking")
                        if node.node_tree.nodes["DropDown1"].use_custom_color:
                            row = layout.row()
                            row.template_ID(node.node_tree.nodes["Mask"], "image", new="image.new", open="image.open")
                            row = layout.row()
                            row.prop(node.inputs[1], "default_value", text="启用遮罩？")

                if node.node_tree.name.startswith("InstantWatercolor"):
                    iwdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    iwdupe.arg1 = node.name
                    twtrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    twtrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="Dark Areas")
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="Bright Areas")
                        row = layout.row()
                        row.prop(node.inputs[7], "default_value", text="均匀缩放‌‌")
                        row = layout.row()
                        row.prop(node.inputs[18], "default_value", text="Contrast")
                        row = layout.row()
                        row.prop(node.inputs[11], "default_value", text="Use UV Coords Instead?")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="Positioning")
                        if node.node_tree.nodes["DropDown1"].use_custom_color:
                            row = layout.row()
                            row.prop(node.inputs[8], "default_value", text="交叉线位置‌")
                            row = layout.row()
                            row.prop(node.inputs[9], "default_value", text="扭曲旋转")
                            row = layout.row()
                            row.prop(node.inputs[10], "default_value", text="色标‌‌")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown2"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown2"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="Details")
                        if node.node_tree.nodes["DropDown2"].use_custom_color:
                            row = layout.row()
                            row.prop(node.inputs[12], "default_value", text="扭曲强度‌‌‌‌‌‌‌")
                            row = layout.row()
                            row.prop(node.inputs[13], "default_value", text="Overall Detail")
                            row = layout.row()
                            row.prop(node.inputs[14], "default_value", text="Interstitial Scale")
                            row = layout.row()
                            row.prop(node.inputs[15], "default_value", text="间隙细节‌‌‌‌‌‌‌")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown3"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown3"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="样式")
                        if node.node_tree.nodes["DropDown3"].use_custom_color:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["Map Range"], "interpolation_type", text="样式")
                            row = layout.row()
                            row.prop(node.node_tree.nodes["Map Range"].inputs[5], "default_value", text="色阶")

                if node.node_tree.name.startswith("EasyDT"):
                    edtdupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    edtdupe.arg1 = node.name
                    edttrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    edttrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.inputs[13], "default_value", text="Noise Color")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["ImportantMix"], "blend_type", text="混合模式")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["MapRangeMask"], "interpolation_type", text="卡通/线性切换‌‌")
                        row = layout.row()
                        row.prop(node.inputs[14], "default_value", text="色阶")
                        row = layout.row()
                        row.prop(node.inputs[12], "default_value", text="扩散（钳制）‌")
                        row = layout.row()
                        row.prop(node.inputs[15], "default_value", text="颜色反转？‌")
                        row = layout.row()
                        row.prop(node.inputs[5], "default_value", text="噪波缩放（均匀）‌‌‌‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[6], "default_value", text="细节‌‌")
                        row = layout.row()
                        row.prop(node.inputs[7], "default_value", text="粗糙度‌‌")
                        row = layout.row()
                        row.prop(node.inputs[16], "default_value", text="噪波空隙度")
                        row = layout.row()
                        row.prop(node.inputs[17], "default_value", text="扭曲强度")
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="位置‌‌‌‌")
                        row = layout.row()
                        row.prop(node.inputs[4], "default_value", text="色标‌‌")
                        row = layout.row()
                        row.prop(node.inputs[3], "default_value", text="扭曲旋转")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="遮罩扭曲强度")
                        if node.node_tree.nodes["DropDown1"].use_custom_color:
                            row = layout.row()
                            row.prop(node.inputs[8], "default_value", text="遮罩扭曲/绘画风格化‌‌‌")
                            row = layout.row()
                            row.prop(node.inputs[9], "default_value", text="绘画扭曲缩放（均匀）‌‌")
                            row = layout.row()
                            row.prop(node.inputs[19], "default_value", text="绘画扭曲缩放‌‌")
                            row = layout.row()
                            row.prop(node.inputs[18], "default_value", text="绘画扭曲位置‌‌‌")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["DropDown2"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown2"].use_custom_color else "TRIA_RIGHT", emboss=False)
                        row.label(text="坐标设置‌")
                        if node.node_tree.nodes["DropDown2"].use_custom_color:
                            row = layout.row()
                            row.prop(node.inputs[20], "default_value", text="物体坐标")
                            row = layout.row()
                            row.prop(node.inputs[1], "default_value", text="UV坐标")




                if node.node_tree.name.startswith("NoiseTexture") or node.node_tree.name.startswith("TransparentNoise"):
                    return
                    tndupe = row.operator("shaderaddon.duplicateeffect", text="", icon='DUPLICATE')
                    tndupe.arg1 = node.name
                    noisetrash = row.operator("shaderaddon.deleteeffect", text="", icon='TRASH')
                    noisetrash.arg1 = node.name
                    if node.node_tree.nodes.get("Visibility") is not None:
                        row.prop(node.node_tree.nodes.get("Visibility").inputs[0], "default_value", text="可见性")
                    if node.use_custom_color:
                        row = layout.row()
                        row.prop(node.inputs[1], "default_value", text="Noise Color")
                        # row = layout.row()
                        # row.prop(node.node_tree.nodes["Noise Range"], "interpolation_type", text="卡通/线性切换‌‌")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["ImportantMix"], "blend_type", text="混合模式")
                        row = layout.row()
                        row.prop(node.node_tree.nodes["MapRangeMask"], "interpolation_type", text="卡通/线性切换‌‌")
                        row = layout.row()
                        row.prop(node.inputs[29], "default_value", text="色阶")
                        row = layout.row()
                        row.prop(node.inputs[69], "default_value", text="颜色反转？‌")
                        row = layout.row()
                        row.label(text="遮罩选项 - 将纹理限制在指定区域‌‌‌‌‌‌‌".upper())
                        row = layout.row()
                        row = layout.row()
                        row.prop(node.inputs[2], "default_value", text="遮罩影响‌")
                        row = layout.row()
                        row.prop(node.inputs[55], "default_value", text="遮罩钳制最小值‌")
                        row.prop(node.inputs[56], "default_value", text="遮罩钳制最大值‌‌‌‌")
                        if node.node_tree.name.startswith("TransparentNoise"):
                            try:
                                row = layout.row()
                                row.prop(node.node_tree.nodes["AddTransparency"].inputs[0], "default_value", text="透明度总量‌")
                            except:
                                print("err")
                            row = layout.row()
                            row.prop(node.inputs[68], "default_value", text="高光值钳制‌")
                        else:
                            row = layout.row()
                            row.prop(node.inputs[68], "default_value", text="高光值钳制‌")

                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown1"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown1"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="Mask Selector")
                            if node.node_tree.nodes["DropDown1"].use_custom_color:
                                row = layout.row()
                                row.label(text="Mask Selector")
                                row = layout.row()
                                row.prop(node.inputs[3], "default_value", text="渐变（球体）遮罩%‌")
                                row = layout.row()
                                row.prop(node.inputs[4], "default_value", text="渐变（矩形）遮罩%‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[5], "default_value", text="Noise Mask %")
                                row = layout.row()
                                row.prop(node.inputs[6], "default_value", text="Wave Mask %")
                                row = layout.row()
                                row.prop(node.inputs[57], "default_value", text="Wave2 Mask %")
                                row = layout.row()
                                row.prop(node.inputs[7], "default_value", text="沃罗诺伊遮罩%‌")
                                row = layout.row()
                                row.prop(node.inputs[49], "default_value", text="平铺/砖块强度‌")
                                row = layout.row()
                                row.prop(node.inputs[48], "default_value", text="泡沫强度‌")
                                
                                # row.prop(node.inputs[24], "default_value", text="噪波缩放（均匀）‌‌‌‌‌‌")
                                # row = layout.row()
                                # row.prop(node.inputs[25], "default_value", text="Noise Detail")
                                
                                # row.prop(node.inputs[26], "default_value", text="噪波粗糙度‌‌‌")
                                # row = layout.row()
                                # row.prop(node.inputs[27], "default_value", text="Noise Distortion")
                                
                                # row.prop(node.inputs[28], "default_value", text="噪波空隙度‌‌")
                                # row = layout.row()
                                # row.prop(node.inputs[35], "default_value", text="Displace Noise")
                                # row = layout.row()
                                # row.prop(node.inputs[36], "default_value", text="动画化置换‌‌‌")
                                # row = layout.row()
                                # row.prop(node.inputs[38], "default_value", text="置换缩放（均匀）‌")
                                # row = layout.row()
                                # row.prop(node.inputs[39], "default_value", text="Scale of Displace")
                                # row = layout.row()
                                # row.label(text="纹理坐标选项")
                                
                                # row = layout.row()
                                # row.prop(node.inputs[19], "default_value", text="生成坐标‌‌‌‌‌")
                                # row = layout.row()
                                # row.prop(node.inputs[20], "default_value", text="物体坐标‌‌‌‌‌")
                                # row = layout.row()
                                # row.prop(node.inputs[21], "default_value", text="UV坐标‌‌‌")
                                # row = layout.row()
                                # row.prop(node.inputs[22], "default_value", text="窗口坐标‌‌‌")
                                # row = layout.row()
                                # row.prop(node.inputs[13], "default_value", text="噪波位置‌‌‌‌‌‌")
                                # row = layout.row()
                                # row.prop(node.inputs[14], "default_value", text="噪波旋转‌")
                                # row = layout.row()
                                # row.prop(node.inputs[15], "default_value", text="噪波缩放‌‌‌‌‌")
                                row = layout.row()
                                row.label(text="--------------")
                                row = layout.row()
                                row.prop(context.scene, "my_mask_enum", text="选择待编辑遮罩‌‌‌‌")
                                row = layout.row()
                                row.label(text="--------------")
                                if context.scene.my_mask_enum == 'TILES':
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["TileZha"].inputs[2], "default_value", text="均匀缩放‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["TileRange"].inputs[1], "default_value", text="钳制‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["TileZha"].inputs[3], "default_value", text="细节‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["TileZha"].inputs[4], "default_value", text="粗糙度‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["TileZha"].inputs[5], "default_value", text="噪波空隙度")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["TileZha"].inputs[8], "default_value", text="随机度‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[51], "default_value", text="位置‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[50], "default_value", text="色标‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[67], "default_value", text="扭曲旋转")

                                if context.scene.my_mask_enum == 'FOAM':
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["FoamRange"].inputs[1], "default_value", text="钳制‌")
                                    row = layout.row()
                                    row.prop(node.inputs[54], "default_value", text="泡沫细节‌")
                                    row = layout.row()
                                    row.prop(node.inputs[52], "default_value", text="位置‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[53], "default_value", text="色标‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[66], "default_value", text="扭曲旋转")

                                if context.scene.my_mask_enum == 'WAVE':
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha"], "wave_type", text="类型‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha"], "bands_direction", text="带状方向‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[31], "default_value", text="波浪缩放")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveRange"].inputs[1], "default_value", text="钳制‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha"].inputs[2], "default_value", text="扭曲强度")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha"].inputs[3], "default_value", text="细节‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha"].inputs[6], "default_value", text="偏移/位置‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[58], "default_value", text="扭曲旋转")
                                    # row = layout.row()
                                    # row.prop(node.inputs[60], "default_value", text="交叉线位置‌")
                                if context.scene.my_mask_enum == 'WAVE2':
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha2"], "wave_type", text="类型‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha2"], "bands_direction", text="带状方向‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha2"].inputs[1], "default_value", text="色标‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveRange2"].inputs[1], "default_value", text="钳制‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha2"].inputs[2], "default_value", text="扭曲强度")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha2"].inputs[3], "default_value", text="细节‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["WaveZha2"].inputs[6], "default_value", text="偏移/位置‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[59], "default_value", text="扭曲旋转")
                                if context.scene.my_mask_enum == 'NOISE':
                                    row = layout.row()
                                    row.prop(node.inputs[30], "default_value", text="噪波缩放‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["NoiseRange"].inputs[2], "default_value", text="钳制‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["NoiseZha"].inputs[3], "default_value", text="细节‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["NoiseZha"].inputs[4], "default_value", text="粗糙度‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["NoiseZha"].inputs[5], "default_value", text="噪波空隙度")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["NoiseZha"].inputs[6], "default_value", text="扭曲强度")
                                    row = layout.row()
                                    row.prop(node.inputs[42], "default_value", text="位置‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[45], "default_value", text="色标‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[65], "default_value", text="扭曲旋转")
                                    
                                if context.scene.my_mask_enum == 'VORONOI':
                                    row = layout.row()
                                    row.prop(node.inputs[32], "default_value", text="均匀缩放‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["VoronoiRange"].inputs[1], "default_value", text="钳制‌")
                                    row = layout.row()
                                    row.prop(node.inputs[33], "default_value", text="反转‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["VoronoiZha"].inputs[3], "default_value", text="细节‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["VoronoiZha"].inputs[4], "default_value", text="粗糙度‌‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["VoronoiZha"].inputs[5], "default_value", text="噪波空隙度")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["VoronoiZha"].inputs[8], "default_value", text="随机度‌‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[43], "default_value", text="位置‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[44], "default_value", text="色标‌‌")

                                
                                if context.scene.my_mask_enum == 'GRADIENTSPHERE':
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["SphereRange"].inputs[1], "default_value", text="钳制‌")
                                    row = layout.row()
                                    row.prop(node.inputs[47], "default_value", text="色标‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[61], "default_value", text="位置‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[62], "default_value", text="扭曲旋转")

                                if context.scene.my_mask_enum == 'GRADIENTRECT':
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["RectRange"].inputs[1], "default_value", text="钳制‌")
                                    row = layout.row()
                                    row.prop(node.inputs[46], "default_value", text="色标‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[63], "default_value", text="位置‌‌‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[64], "default_value", text="扭曲旋转")
                                    
                                row = layout.row()
                                row.label(text="----------------------")
                        except:
                            row = layout.row()
                            row.label(text="Mask Selector")
                            row = layout.row()
                            row.prop(node.inputs[3], "default_value", text="渐变（球体）遮罩%‌")
                            row = layout.row()
                            row.prop(node.inputs[4], "default_value", text="渐变（矩形）遮罩%‌‌‌")
                            row = layout.row()
                            row.prop(node.inputs[5], "default_value", text="Noise Mask %")
                            row = layout.row()
                            row.prop(node.inputs[6], "default_value", text="Wave Mask %")
                            row = layout.row()
                            row.prop(node.inputs[57], "default_value", text="Wave2 Mask %")
                            row = layout.row()
                            row.prop(node.inputs[7], "default_value", text="沃罗诺伊遮罩%‌")
                            row = layout.row()
                            row.prop(node.inputs[49], "default_value", text="平铺/砖块强度‌")
                            row = layout.row()
                            row.prop(node.inputs[48], "default_value", text="泡沫强度‌")
                            
                            # row.prop(node.inputs[24], "default_value", text="噪波缩放（均匀）‌‌‌‌‌‌")
                            # row = layout.row()
                            # row.prop(node.inputs[25], "default_value", text="Noise Detail")
                            
                            # row.prop(node.inputs[26], "default_value", text="噪波粗糙度‌‌‌")
                            # row = layout.row()
                            # row.prop(node.inputs[27], "default_value", text="Noise Distortion")
                            
                            # row.prop(node.inputs[28], "default_value", text="噪波空隙度‌‌")
                            # row = layout.row()
                            # row.prop(node.inputs[35], "default_value", text="Displace Noise")
                            # row = layout.row()
                            # row.prop(node.inputs[36], "default_value", text="动画化置换‌‌‌")
                            # row = layout.row()
                            # row.prop(node.inputs[38], "default_value", text="置换缩放（均匀）‌")
                            # row = layout.row()
                            # row.prop(node.inputs[39], "default_value", text="Scale of Displace")
                            # row = layout.row()
                            # row.label(text="纹理坐标选项")
                            
                            # row = layout.row()
                            # row.prop(node.inputs[19], "default_value", text="生成坐标‌‌‌‌‌")
                            # row = layout.row()
                            # row.prop(node.inputs[20], "default_value", text="物体坐标‌‌‌‌‌")
                            # row = layout.row()
                            # row.prop(node.inputs[21], "default_value", text="UV坐标‌‌‌")
                            # row = layout.row()
                            # row.prop(node.inputs[22], "default_value", text="窗口坐标‌‌‌")
                            # row = layout.row()
                            # row.prop(node.inputs[13], "default_value", text="噪波位置‌‌‌‌‌‌")
                            # row = layout.row()
                            # row.prop(node.inputs[14], "default_value", text="噪波旋转‌")
                            # row = layout.row()
                            # row.prop(node.inputs[15], "default_value", text="噪波缩放‌‌‌‌‌")
                            row = layout.row()
                            row.label(text="--------------")
                            row = layout.row()
                            row.prop(context.scene, "my_mask_enum", text="选择待编辑遮罩‌‌‌‌")
                            row = layout.row()
                            row.label(text="--------------")
                            if context.scene.my_mask_enum == 'TILES':
                                row = layout.row()
                                row.prop(node.node_tree.nodes["TileZha"].inputs[2], "default_value", text="均匀缩放‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["TileRange"].inputs[1], "default_value", text="钳制‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["TileZha"].inputs[3], "default_value", text="细节‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["TileZha"].inputs[4], "default_value", text="粗糙度‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["TileZha"].inputs[5], "default_value", text="噪波空隙度")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["TileZha"].inputs[8], "default_value", text="随机度‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[51], "default_value", text="位置‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[50], "default_value", text="色标‌‌")
                                row = layout.row()
                                row.prop(node.inputs[67], "default_value", text="扭曲旋转")

                            if context.scene.my_mask_enum == 'FOAM':
                                row = layout.row()
                                row.prop(node.node_tree.nodes["FoamRange"].inputs[1], "default_value", text="钳制‌")
                                row = layout.row()
                                row.prop(node.inputs[54], "default_value", text="泡沫细节‌")
                                row = layout.row()
                                row.prop(node.inputs[52], "default_value", text="位置‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[53], "default_value", text="色标‌‌")
                                row = layout.row()
                                row.prop(node.inputs[66], "default_value", text="扭曲旋转")

                            if context.scene.my_mask_enum == 'WAVE':
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha"], "wave_type", text="类型‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha"], "bands_direction", text="带状方向‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[31], "default_value", text="波浪缩放")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveRange"].inputs[1], "default_value", text="钳制‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha"].inputs[2], "default_value", text="扭曲强度")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha"].inputs[3], "default_value", text="细节‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha"].inputs[6], "default_value", text="偏移/位置‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[58], "default_value", text="扭曲旋转")
                                # row = layout.row()
                                # row.prop(node.inputs[60], "default_value", text="交叉线位置‌")
                            if context.scene.my_mask_enum == 'WAVE2':
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha2"], "wave_type", text="类型‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha2"], "bands_direction", text="带状方向‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha2"].inputs[1], "default_value", text="色标‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveRange2"].inputs[1], "default_value", text="钳制‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha2"].inputs[2], "default_value", text="扭曲强度")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha2"].inputs[3], "default_value", text="细节‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["WaveZha2"].inputs[6], "default_value", text="偏移/位置‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[59], "default_value", text="扭曲旋转")
                            if context.scene.my_mask_enum == 'NOISE':
                                row = layout.row()
                                row.prop(node.inputs[30], "default_value", text="噪波缩放‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["NoiseRange"].inputs[2], "default_value", text="钳制‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["NoiseZha"].inputs[3], "default_value", text="细节‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["NoiseZha"].inputs[4], "default_value", text="粗糙度‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["NoiseZha"].inputs[5], "default_value", text="噪波空隙度")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["NoiseZha"].inputs[6], "default_value", text="扭曲强度")
                                row = layout.row()
                                row.prop(node.inputs[42], "default_value", text="位置‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[45], "default_value", text="色标‌‌")
                                row = layout.row()
                                row.prop(node.inputs[65], "default_value", text="扭曲旋转")
                                
                            if context.scene.my_mask_enum == 'VORONOI':
                                row = layout.row()
                                row.prop(node.inputs[32], "default_value", text="均匀缩放‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["VoronoiRange"].inputs[1], "default_value", text="钳制‌")
                                row = layout.row()
                                row.prop(node.inputs[33], "default_value", text="反转‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["VoronoiZha"].inputs[3], "default_value", text="细节‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["VoronoiZha"].inputs[4], "default_value", text="粗糙度‌‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["VoronoiZha"].inputs[5], "default_value", text="噪波空隙度")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["VoronoiZha"].inputs[8], "default_value", text="随机度‌‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[43], "default_value", text="位置‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[44], "default_value", text="色标‌‌")

                            
                            if context.scene.my_mask_enum == 'GRADIENTSPHERE':
                                row = layout.row()
                                row.prop(node.node_tree.nodes["SphereRange"].inputs[1], "default_value", text="钳制‌")
                                row = layout.row()
                                row.prop(node.inputs[47], "default_value", text="色标‌‌")
                                row = layout.row()
                                row.prop(node.inputs[61], "default_value", text="位置‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[62], "default_value", text="扭曲旋转")

                            if context.scene.my_mask_enum == 'GRADIENTRECT':
                                row = layout.row()
                                row.prop(node.node_tree.nodes["RectRange"].inputs[1], "default_value", text="钳制‌")
                                row = layout.row()
                                row.prop(node.inputs[46], "default_value", text="色标‌‌")
                                row = layout.row()
                                row.prop(node.inputs[63], "default_value", text="位置‌‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[64], "default_value", text="扭曲旋转")
                                
                            row = layout.row()
                            row.label(text="----------------------")
                        row = layout.row()
                        try:
                            row.prop(node.node_tree.nodes["DropDown2"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown2"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="遮罩扭曲强度")
                            if node.node_tree.nodes["DropDown2"].use_custom_color:
                                
                                row = layout.row()
                                row.prop(node.inputs[12], "default_value", text="遮罩扭曲/绘画风格化‌‌‌")
                                row = layout.row()
                                row.prop(node.inputs[34], "default_value", text="绘画扭曲缩放（均匀）‌‌")
                                row = layout.row()
                                row.prop(node.inputs[41], "default_value", text="绘画扭曲缩放‌‌")
                                row = layout.row()
                                row.prop(node.inputs[37], "default_value", text="动画化绘画扭曲")
                        except:
                            row = layout.row()
                            row.label(text="扭曲遮罩设置‌‌‌")
                            row = layout.row()
                            row.prop(node.inputs[12], "default_value", text="遮罩扭曲/绘画风格化‌‌‌")
                            row = layout.row()
                            row.prop(node.inputs[34], "default_value", text="绘画扭曲缩放（均匀）‌‌")
                            row = layout.row()
                            row.prop(node.inputs[41], "default_value", text="绘画扭曲缩放‌‌")
                            row = layout.row()
                            row.prop(node.inputs[37], "default_value", text="动画化绘画扭曲")


                        if node.node_tree.name.startswith("TransparentNoise"):
                            try:
                                row.prop(node.node_tree.nodes["DropDown3"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown3"].use_custom_color else "TRIA_RIGHT", emboss=False)
                                row.label(text="边缘透明度‌‌")
                                if node.node_tree.nodes["DropDown3"].use_custom_color:
                                    row = layout.row()
                                    row.label(text="边缘透明度（不可烘焙）‌‌")
                                    row = layout.row()
                                    row.prop(node.inputs[70], "default_value", text="启用边缘透明度？‌")
                                    if node.inputs[70].default_value > 0.01:
                                        row = layout.row()
                                        row.operator("shaderaddon.maskspeculars", text="解除高光遮罩")
                                        row = layout.row()
                                        row.prop(node.inputs[71], "default_value", text="混合模式")
                                        row.prop(node.inputs[72], "default_value", text="颜色反转？‌")
                            except:
                                row = layout.row()
                                row.label(text="边缘透明度（不可烘焙）‌‌")
                                row = layout.row()
                                row.prop(node.inputs[70], "default_value", text="启用边缘透明度？‌")
                                if node.inputs[70].default_value > 0.01:
                                    row = layout.row()
                                    row.operator("shaderaddon.maskspeculars", text="解除高光遮罩")
                                    row = layout.row()
                                    row.prop(node.inputs[71], "default_value", text="混合模式")
                                    row.prop(node.inputs[72], "default_value", text="颜色反转？‌")

                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown4"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown4"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="手绘遮罩")
                            if node.node_tree.nodes["DropDown4"].use_custom_color:
                                row = layout.row()
                                row.label(text="如需手绘遮罩，请使用下方新建/打开按钮")
                                row = layout.row()
                                drawmask2 = node.node_tree.nodes["DrawMask"]
                                row.template_ID(drawmask2, "image", new="image.new", open="image.open")
                                row = layout.row()
                                row.prop(node.inputs[40], "default_value", text="启用手绘遮罩？")
                                if node.node_tree.name.startswith("TransparentNoise") and node.inputs[40].default_value > 0.01:
                                    row = layout.row()
                                    row.prop(node.inputs[74], "default_value", text="遮罩作用域")
                                    row = layout.row()
                                    row.prop(node.inputs[75], "default_value", text="遮罩缩放")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["Color Ramp"].color_ramp.elements[0], "position", text="钳制‌")
                                    row = layout.row()
                                    row.prop(node.node_tree.nodes["Color Ramp"].color_ramp.elements[1], "position", text="钳制#2")
                                row = layout.row()
                                row = layout.row()
                        except:
                            row = layout.row()
                            row.label(text="如需手绘遮罩，请使用下方新建/打开按钮")
                            row = layout.row()
                            drawmask2 = node.node_tree.nodes["DrawMask"]
                            row.template_ID(drawmask2, "image", new="image.new", open="image.open")
                            row = layout.row()
                            row.prop(node.inputs[40], "default_value", text="启用手绘遮罩？")
                            if node.node_tree.name.startswith("TransparentNoise") and node.inputs[40].default_value > 0.01:
                                row = layout.row()
                                row.prop(node.inputs[74], "default_value", text="遮罩作用域")
                                row = layout.row()
                                row.prop(node.inputs[75], "default_value", text="遮罩缩放")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["Color Ramp"].color_ramp.elements[0], "position", text="钳制‌")
                                row = layout.row()
                                row.prop(node.node_tree.nodes["Color Ramp"].color_ramp.elements[1], "position", text="钳制#2")
                            row = layout.row()
                            row = layout.row()
                        
                        try:
                            row = layout.row()
                            row.prop(node.node_tree.nodes["DropDown5"], "use_custom_color", text="", icon="TRIA_DOWN" if node.node_tree.nodes["DropDown5"].use_custom_color else "TRIA_RIGHT", emboss=False)
                            row.label(text="坐标设置‌")
                            if node.node_tree.nodes["DropDown5"].use_custom_color:
                                row = layout.row()
                                row.label(text="遮罩纹理坐标设置")
                                row = layout.row()
                                row.prop(node.inputs[17], "default_value", text="物体坐标（遮罩）")
                                row = layout.row()
                                row.prop(node.inputs[18], "default_value", text="UV坐标（遮罩）")
                        except:
                            row = layout.row()
                            row.label(text="遮罩纹理坐标设置")
                            row = layout.row()
                            row.prop(node.inputs[17], "default_value", text="物体坐标（遮罩）")
                            row = layout.row()
                            row.prop(node.inputs[18], "default_value", text="UV坐标（遮罩）")
                        
                        row = layout.row()
                        row.prop(node.node_tree.nodes["ZhaTexture Coordinate"], "object", text="遮罩物体‌")

            
            
            if node.outputs and node.outputs[0].is_linked and nodecount < 9:
                node = node.outputs[0].links[0].to_node
            else:
                break
            

        # if not obj.active_material.name.startswith("Outline for"):
        #     #delete effect
        row = layout.row()
        box = layout.box()
        #     row = box.row()
        #     row.prop(obj, "node_groups_enum", text="")
        #     row.operator("shaderaddon.deleteeffect", text="删除‌")


        modifier_count = 0

        for modifier in obj.modifiers:
            if modifier.name.startswith("SB Disp"):
                modifier_count += 1
                box = layout.box()
                row = box.row()
                row.label(text=f"Displace Effect #{modifier_count}")
                row = layout.row()
                row.prop(modifier, "strength")
                row.prop(modifier, "mid_level")
                row.prop(modifier, "direction")
                row = layout.row()
                row.operator("shaderaddon.addcloudstexture", text="添加云层置换纹理‌")
                row = layout.row()
                row.prop(modifier, "texture")
                row.prop(modifier, "texture_coords")
                row.prop(modifier, "texture_coords_object")

                

        
        row = layout.row()
        row = box.row()
        row.prop(obj, "node_groups_enum_swap1", text="")
        row.prop(obj, "node_groups_enum_swap2", text="与‌")
        row.operator("shaderaddon.swapnodes", text="交换效果")
        row = layout.row()
        row = box.row()
        
        # row.prop(obj, "duplicate_group_enum", text="")
        # row.operator("shaderaddon.duplicateeffect", text="复制‌")
        # row = layout.row()
        # row.label(text="部分特效（如光照效果）无法复制，请从特效菜单添加")

        #check for steam/fog objects

        try:
            if bpy.context.object.active_material.node_tree.nodes.get("SB Fog") is not None or bpy.context.object.active_material.name.startswith("SB Fog"):
                row = layout.row()
                box = layout.box()
                row = box.row()
                row.label(text="体积雾")
                row = layout.row()
                fognode = bpy.context.object.active_material.node_tree.nodes.get("SB Fog")
                row.prop(fognode.inputs[0], "default_value", text="均匀缩放‌‌")
                row = layout.row()
                row.prop(fognode.inputs[1], "default_value", text="色标‌‌")
                row = layout.row()
                row.prop(fognode.inputs[2], "default_value", text="雾效最小值")
                row = layout.row()
                row.prop(fognode.inputs[3], "default_value", text="雾效最大值")
                row = layout.row()
                row.prop(fognode.inputs[4], "default_value", text="颜色")
                row = layout.row()
                row.prop(fognode.inputs[5], "default_value", text="交叉线位置‌")
                row = layout.row()
                row.prop(fognode.inputs[6], "default_value", text="遮罩限制")
                row = layout.row()
                row.prop(fognode.inputs[7], "default_value", text="遮罩作用域")
            if bpy.context.object.active_material.node_tree.nodes.get("SB Steam") is not None or bpy.context.object.active_material.name.startswith("SB Steam"):
                row = layout.row()
                box = layout.box()
                row = box.row()
                row.label(text="蒸汽效果")
                row = layout.row()
                steamnode = bpy.context.object.active_material.node_tree.nodes.get("SB Steam")
                row.prop(steamnode.inputs[0], "default_value", text="颜色")
                row = layout.row()
                row.prop(steamnode.inputs[9], "default_value", text="安装路径")
                row = layout.row()
                row.prop(steamnode.inputs[4], "default_value", text="均匀缩放‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[3], "default_value", text="色标‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[1], "default_value", text="蒸汽渐变‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[5], "default_value", text="细节‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[6], "default_value", text="粗糙度‌‌")
                row = layout.row()
                row.prop(steamnode.inputs[7], "default_value", text="扩散范围")
                row = layout.row()
                row.prop(steamnode.inputs[8], "default_value", text="底部")
        except:
            joe = 'kasou'
            




                        

bpy.types.Scene.show_collapsible_section = bpy.props.BoolProperty(name="Show Collapsible Section", default=True)



class CloudsTexture(bpy.types.Operator):
    bl_idname = "shaderaddon.addcloudstexture"
    bl_label = "Add a Clouds Texture"

    def execute(self, context):
        obj = bpy.context.active_object

        if not obj:
            return
        #check if empty
        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        

        texture = bpy.data.textures.new("CloudsTexture", 'CLOUDS')
    
        # Set the texture type to Clouds
        texture.type = 'CLOUDS'
        
        # Set additional settings for the Clouds texture
        texture.noise_scale = 0.25
        texture.noise_depth = 2

        for modifier in obj.modifiers:
            if modifier.name.startswith("SB Disp"):
                modifier.texture = texture
                break

        

        return {'FINISHED'}

class ExecuteOperator(bpy.types.Operator):
    bl_idname = "shaderaddon.execute_operator"
    bl_label = "Add Effect"

    def execute(self, context):
        obj = bpy.context.active_object

        tempobj = None
        if obj.type == 'EMPTY' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj
        elif obj.type == 'MESH' and obj.name.startswith("SB"):
            tempobj = obj.parent
            obj = tempobj

        if not obj or not obj.active_material or not obj.active_material.use_nodes:
            print("No active object or no material with nodes found.")
            return

        material = obj.active_material
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        count = 0
        for node in nodes:
            if node.type == 'GROUP':
                count += 1
        
        if not context.scene.my_operator_enum == 'SOLIDIFYOUTLINE':
            def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
                def draw(self, context):
                    self.layout.label(text=message)
                
                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

            if count >= 9:
                ShowMessageBox("Max Layers Reached, Please Upgrade or Join the Masterclass on ukiyogirls.io!", "My Title", 'ERROR')
                return {'FINISHED'}
            
        curcount = 0
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
            def draw(self, context):
                self.layout.label(text=message)
                
            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
        for obj in bpy.data.objects:
            try:
                if obj.active_material.node_tree.nodes.get("SAS Point Lights Group #1") is not None:
                    curcount += 1
            except:
                continue
        if curcount >= 25:
            ShowMessageBox(message="Max Objects (25) for using the Stylized Point Light Reached. Please Remove From Some Objects, Or Upgrade", title="Message Box", icon='INFO')
            return {'FINISHED'}

        
        operator = context.scene.my_operator_enum
        if operator == 'LOCALGRADIENT':
            bpy.ops.shaderaddon.addlocalgradient()
        elif operator == 'DIFFUSELIGHTING':
            bpy.ops.shaderaddon.adddiffuselighting()
        elif operator == 'SPECULAR':
            bpy.ops.shaderaddon.addspecularreflection()
        elif operator == 'AO':
            bpy.ops.shaderaddon.addao()
        elif operator == 'CIRCULARLIGHTING':
            bpy.ops.shaderaddon.addcircularlight()
        elif operator == 'TRANSPARENTPAINT':
            bpy.ops.shaderaddon.addtransparentpaint()
        elif operator == 'DRAWPAINT':
            bpy.ops.shaderaddon.addtexturepaint()
        elif operator == 'NOISETEXTURE':
            bpy.ops.shaderaddon.addnoisetexture()
        elif operator == 'LOCALGRADIENTSPHERE':
            bpy.ops.shaderaddon.addlocalgradientsphere()
        elif operator == 'OVERALLTEXTURE':
            bpy.ops.shaderaddon.addoveralltexture()
        elif operator == 'MOODLIGHT':
            bpy.ops.shaderaddon.addcoloredcircularlight()
        elif operator == 'EDGEDETECT':
            bpy.ops.shaderaddon.addedgedetect()
        elif operator == 'COLOREDEDGES':
            bpy.ops.shaderaddon.addcolorededges()
        elif operator == 'SOLIDIFYOUTLINE':
            bpy.ops.shaderaddon.addsolidifyoutline()
        elif operator == 'VERTEXPAINT':
            bpy.ops.shaderaddon.addvertexpaint()
        elif operator == 'DISPLACE':
            bpy.ops.shaderaddon.adddisplace()
        elif operator == 'FAKELIGHT':
            bpy.ops.shaderaddon.addobjectlight()
        elif operator == 'FAKESUNLIGHT':
            bpy.ops.shaderaddon.addsunlight()
        elif operator == 'DRAWONECOLOR':
            bpy.ops.shaderaddon.addsinglecolor()
        elif operator == 'TRANSPARENTNOISE':
            bpy.ops.shaderaddon.addtransparentnoise()
        elif operator == 'STYLIZEDFOAM':
            bpy.ops.shaderaddon.addstylizedfoam()
        elif operator == 'FOG':
            bpy.ops.shaderaddon.addfog()
        elif operator == 'STEAM':
            bpy.ops.shaderaddon.addsteam()
        elif operator == 'HSL':
            bpy.ops.shaderaddon.addhsl()
        elif operator == 'BRUSHSTROKES':
            bpy.ops.shaderaddon.addbrushstrokes()
        elif operator == 'OBJECTRANDOMIZE':
            bpy.ops.shaderaddon.addobjectrandomize()
        elif operator == 'CROSSHATCHING':
            bpy.ops.shaderaddon.addcrosshatch()
        elif operator == 'GODRAYS':
            bpy.ops.shaderaddon.addgodrays()
        elif operator == 'CONTRAST':
            bpy.ops.shaderaddon.addrgbcurves()
        elif operator == 'WORLDSTROKES':
            bpy.ops.shaderaddon.addtransparentworldstrokes()
        elif operator == 'INSTANTWATERCOLOR':
            bpy.ops.shaderaddon.addinstantwatercolor()
        elif operator == 'HAIRCURVES':
            bpy.ops.shaderaddon.addhaircurves()
        elif operator == 'EASYDT':
            bpy.ops.shaderaddon.addeasydt()
        elif operator == 'CURVATURE':
            bpy.ops.shaderaddon.addcurvature()
        elif operator == 'SPLRed':
            bpy.ops.shaderaddon.addredlight()
        return {'FINISHED'}

@persistent
def stimulate(dummy):
    bpy.app.timers.register(timer_function)


bpy.app.handlers.load_post.append(stimulate)
    

def register():
    bpy.utils.register_class(ShaderSetup)
    bpy.utils.register_class(ExecuteOperator)
    bpy.utils.register_class(ShaderPanel)
    bpy.utils.register_class(DeleteMaterial)
    bpy.utils.register_class(AddLocalGradient)
    bpy.utils.register_class(AddDiffuseLighting)
    bpy.utils.register_class(AddAO)
    bpy.utils.register_class(AddCircularLight)
    bpy.utils.register_class(AddTransparentPaint)
    bpy.utils.register_class(AddTexturePaint)
    bpy.utils.register_class(AddNoiseTexture)
    bpy.utils.register_class(AddLocalGradientSphere)
    bpy.utils.register_class(DeleteEffect)
    bpy.utils.register_class(RefreshMaterial)
    bpy.utils.register_class(AddOverallTexture)
    # bpy.utils.register_class(AddMoodLight)
    bpy.utils.register_class(SwapNodes)
    bpy.utils.register_class(AddEdgeDetect)
    bpy.utils.register_class(AddColoredEdges)
    bpy.utils.register_class(AddSolidifyOutline)
    bpy.app.timers.register(timer_function)
    bpy.app.handlers.load_post.append(stimulate)
    bpy.utils.register_class(AppendBrushes)
    bpy.utils.register_class(AddVertexPaint)
    bpy.utils.register_class(AddDisplace)
    bpy.utils.register_class(CloudsTexture)
    bpy.utils.register_class(AddFakeLight)
    bpy.utils.register_class(AddFakeSun)
    bpy.utils.register_class(AddSingleColor)
    bpy.utils.register_class(AddTransparentNoise)

    bpy.utils.register_class(DuplicateMaterial)
    bpy.utils.register_class(AddStylizedFoam)
    
    bpy.utils.register_class(AddCurvature)
    bpy.utils.register_class(AddHSL)
    bpy.utils.register_class(WorldSetup)
    bpy.utils.register_class(WorldPanel)
    bpy.utils.register_class(SwapNodes2)
    bpy.utils.register_class(DuplicateEffect)

    

    bpy.utils.register_class(AddBrushStrokes)
    bpy.utils.register_class(AddObjectRandomize)

    bpy.utils.register_class(SaveImageTextures)

    bpy.utils.register_class(BakeAlphaAnimated)
    bpy.utils.register_class(AddCrossHatch)
    bpy.utils.register_class(AddRGBCurves)
    bpy.utils.register_class(BakeNormals)
    bpy.utils.register_class(MaskSpeculars)
    bpy.utils.register_class(AddTransparentWorldStrokes)
    # bpy.utils.register_class(BakeBounced)
    bpy.utils.register_class(AddInstantWatercolor)
    bpy.utils.register_class(AddHairCurves)
    bpy.utils.register_class(ExternalPaint)
    bpy.utils.register_class(AddEasyDT)
    bpy.utils.register_class(NormalsPaint)
    bpy.utils.register_class(OpenURLOperator)
    bpy.utils.register_class(BakeCurvature)
    bpy.utils.register_class(AddRedLight)
    
    


def unregister():
    bpy.utils.unregister_class(ShaderSetup)
    bpy.utils.unregister_class(ExecuteOperator)
    bpy.utils.unregister_class(ShaderPanel)
    bpy.utils.unregister_class(DeleteMaterial)
    bpy.utils.unregister_class(AddLocalGradient)
    bpy.utils.unregister_class(AddDiffuseLighting)
    bpy.utils.unregister_class(AddAO)
    bpy.utils.unregister_class(AddCircularLight)
    bpy.utils.unregister_class(AddTransparentPaint)
    bpy.utils.unregister_class(AddTexturePaint)
    bpy.utils.unregister_class(AddNoiseTexture)
    bpy.utils.unregister_class(AddLocalGradientSphere)
    bpy.utils.unregister_class(DeleteEffect)
    bpy.utils.unregister_class(RefreshMaterial)
    bpy.utils.unregister_class(AddOverallTexture)
    bpy.utils.unregister_class(AddCurvature)
    # bpy.utils.unregister_class(AddMoodLight)
    bpy.utils.unregister_class(SwapNodes)
    bpy.utils.unregister_class(AddEdgeDetect)
    bpy.utils.unregister_class(AddColoredEdges)
    bpy.utils.unregister_class(AddSolidifyOutline)
    bpy.app.timers.unregister(timer_function)
    bpy.app.handlers.load_post.remove(stimulate)
    bpy.utils.unregister_class(AppendBrushes)
    bpy.utils.unregister_class(AddVertexPaint)
    bpy.utils.unregister_class(AddDisplace)
    bpy.utils.unregister_class(CloudsTexture)
    bpy.utils.unregister_class(AddFakeLight)
    bpy.utils.unregister_class(AddFakeSun)
    bpy.utils.unregister_class(AddSingleColor)
    bpy.utils.unregister_class(AddTransparentNoise)

    bpy.utils.unregister_class(DuplicateMaterial)
    bpy.utils.unregister_class(AddStylizedFoam)
    
    bpy.utils.unregister_class(AddHSL)
    bpy.utils.unregister_class(WorldSetup)
    bpy.utils.unregister_class(WorldPanel)
    bpy.utils.unregister_class(SwapNodes2)
    bpy.utils.unregister_class(DuplicateEffect)

    bpy.utils.unregister_class(AddObjectRandomize)

    


    bpy.utils.unregister_class(SaveImageTextures)

    bpy.utils.unregister_class(BakeAlphaAnimated)
    bpy.utils.unregister_class(AddCrossHatch)
    bpy.utils.unregister_class(AddRGBCurves)
    bpy.utils.unregister_class(BakeNormals)
    bpy.utils.unregister_class(MaskSpeculars)
    bpy.utils.unregister_class(AddTransparentWorldStrokes)
    # bpy.utils.unregister_class(BakeBounced)
    bpy.utils.unregister_class(AddHairCurves)
    bpy.utils.unregister_class(ExternalPaint)
    bpy.utils.unregister_class(AddEasyDT)
    bpy.utils.unregister_class(NormalsPaint)
    bpy.utils.unregister_class(OpenURLOperator)
    bpy.utils.unregister_class(BakeCurvature)
    bpy.utils.unregister_class(AddRedLight)


if __name__ == '__main__' :
    register()
import unreal

asset_registry = unreal.AssetRegistryHelpers().get_asset_registry()
editor_util = unreal.EditorUtilityLibrary()
material_util = unreal.MaterialEditingLibrary()

task_label = "Setting up material for zone {}"

asset_path = "/Game/ryzom/zorai/zones"
material_path = asset_path + "/materials"
data_texture_path = asset_path + "/data_textures"
material_template_path = "/Game/test/zone-test/layered-material/MI_jungle_tile_template"


def main():
    asset_filter = unreal.ARFilter(package_paths=[asset_path], recursive_paths=True,
                                   class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "StaticMesh")])
    assets = asset_registry.get_assets(asset_filter)
    asset_count = len(assets)

    with unreal.ScopedSlowTask(asset_count, task_label.format("...")) as slow_task:
        slow_task.make_dialog(True)
        run_for_assets(slow_task, assets)


def run_for_assets(slow_task, assets):
    for asset_data in assets:
        slow_task.enter_progress_frame(1, task_label.format(asset_data.asset_name))
        if slow_task.should_cancel():
            break
        run_for_asset(asset_data.get_asset())
        # unreal.EditorAssetLibrary.save_directory(asset_path)


def run_for_asset(asset: unreal.StaticMesh):
    zone_name = asset.get_name()
    zone_material_path = create_zone_material_path(zone_name)
    zone_material = find_asset(zone_material_path)
    if zone_material is None:
        zone_material = create_zone_material(zone_name, zone_material_path)
    else:
        print("Material already exists {0}".format(zone_material_path))
    asset.set_material(0, zone_material)


def create_zone_material_path(zone_name: str):
    return "{0}/MI_{1}".format(material_path, zone_name)


def find_asset(search_path: str):
    asset_data = unreal.EditorAssetLibrary.find_asset_data(search_path)
    if asset_data.is_valid():
        return asset_data.get_asset()
    else:
        print("Asset not found {0}".format(asset_path))
        return None


def create_zone_material(zone_name: str, zone_material_path: str) -> unreal.MaterialInstanceConstant:
    zone_material = unreal.EditorAssetLibrary.duplicate_asset(material_template_path, zone_material_path)
    setup_zone_material(zone_name, zone_material)
    return zone_material


def setup_zone_material(zone_name: str, zone_material: unreal.MaterialInstanceConstant):
    values = []
    texture_parameters: unreal.Array[unreal.TextureParameterValue] = zone_material.get_editor_property("texture_parameter_values")
    for texture_parameter in texture_parameters:
        layer_name = zone_layer_name(zone_name, texture_parameter)
        layer_texture = find_data_texture(layer_name)
        print("Setting layer texture {0} in material layer {1}".format(layer_texture.get_name(), zone_material.get_name()))
        texture_parameter.set_editor_property("parameter_value", layer_texture)
        values.append(texture_parameter)
    zone_material.set_editor_property("texture_parameter_values", values)


def zone_layer_name(zone_name: str, texture_parameter: unreal.TextureParameterValue) -> str:
    index = texture_parameter.parameter_info.index
    if texture_parameter.parameter_info.association == unreal.MaterialParameterAssociation.BLEND_PARAMETER:
        index += 1
    return zone_layer_name_by_index(zone_name, index)


def zone_layer_name_by_index(zone_name: str, index: int) -> str:
    return "{0}_zonel_tile-id-{1}".format(zone_name, index)


def find_data_texture(name: str) -> unreal.Texture2D | None:
    asset_path = "{0}/{1}".format(data_texture_path, name)
    return find_asset(asset_path)


main()

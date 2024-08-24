import unreal

zones_path = "/Game/ryzom/fyros/zones"
tilebank_path = "/Game/ryzom/desert/Materials"

asset_registry = unreal.AssetRegistryHelpers().get_asset_registry()
asset_filter = unreal.ARFilter(package_paths=[zones_path], class_names=["StaticMesh"])
assets = asset_registry.get_assets(asset_filter)
asset_count = len(assets)
print("Assets {}".format(asset_count))

material_filter = unreal.ARFilter(package_paths=[tilebank_path], class_names=["Material"])
material_lookup = {}
for material_data in asset_registry.get_assets(material_filter):
    material_lookup[material_data.asset_name] = material_data
material_count = len(material_lookup)
print("Materials {}".format(material_count))


def change_zone_materials(slow_task: unreal.ScopedSlowTask, asset_data: unreal.AssetData):
    zone: unreal.StaticMesh = asset_data.get_asset()
    for j in range(len(zone.static_materials)):
        if slow_task.should_cancel():
            break
        change_zone_material(zone, j)


def change_zone_material(zone: unreal.StaticMesh, material_index: int):
    static_material = zone.static_materials[material_index]
    material_slot: unreal.Name = static_material.get_editor_property("material_slot_name")
    if material_slot in material_lookup:
        current_material = zone.get_material(material_index)
        current_material_name = ""
        if current_material:
            current_material_name = current_material.get_name()
        if current_material_name != material_slot:
            zone.set_material(material_index, material_lookup[material_slot].get_asset())
        else:
            print("Material already set {}".format(current_material_name))
    else:
        print("No Material found for {}".format(material_slot))


text_label = "Setting Materials on Zone {}"
with unreal.ScopedSlowTask(asset_count, text_label.format("..")) as slow_task:
    slow_task.make_dialog(True)
    for asset_data in assets:
        slow_task.enter_progress_frame(1, text_label.format(asset_data.asset_name))
        if slow_task.should_cancel():
            break
        change_zone_materials(slow_task, asset_data)

import unreal

zones_path = "/Game/ryzom/zorai/zones"

mesh_editor = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
asset_helper = unreal.AssetRegistryHelpers()
asset_filter = unreal.ARFilter(package_paths=[zones_path], class_names=["StaticMesh"])
assets = asset_helper.get_asset_registry().get_assets(asset_filter)
asset_count = len(assets)
text_label = "Adding Collision to Zone {}"
print("Assets {}".format(asset_count))

with unreal.ScopedSlowTask(asset_count, text_label.format("...")) as slow_task:
    slow_task.make_dialog(True)
    for i in range(asset_count):
        asset_data = assets[i]
        if slow_task.should_cancel():
            break
        slow_task.enter_progress_frame(1, text_label.format(asset_data.asset_name))
        zone = asset_data.get_asset()
        if(mesh_editor.get_collision_complexity(zone) == unreal.CollisionTraceFlag.CTF_USE_DEFAULT):
            mesh_editor.remove_collisions(zone)
            zone.set_editor_property("complex_collision_mesh", zone)
            body_setup = zone.get_editor_property("body_setup")
            body_setup.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
        else:
            print("Asset already has complex collision {}".format(zone.get_name()))

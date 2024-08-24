import unreal

asset_registry = unreal.AssetRegistryHelpers().get_asset_registry()
task_label = "Setting Texture to Data {}"

asset_path = "/Game/ryzom/zorai/zones/data_textures"


def main():
    asset_filter = unreal.ARFilter(package_paths=[asset_path], recursive_paths=True,
                                   class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "Texture2D")])
    assets = asset_registry.get_assets(asset_filter)
    asset_count = len(assets)

    with unreal.ScopedSlowTask(asset_count, task_label.format("...")) as slow_task:
        slow_task.make_dialog(True)
        change_data_textures(slow_task, assets)

def change_data_textures(slow_task, assets):
    for asset_data in assets:
        slow_task.enter_progress_frame(1, task_label.format(asset_data.asset_name))
        if slow_task.should_cancel():
            break
        change_data_texture(asset_data.get_asset())
        unreal.EditorAssetLibrary.save_directory(asset_path)

def change_data_texture(asset: unreal.Texture2D):
    asset.lod_group = unreal.TextureGroup.TEXTUREGROUP_16_BIT_DATA
    asset.compression_settings = unreal.TextureCompressionSettings.TC_HDR
    asset.address_x = unreal.TextureAddress.TA_CLAMP
    asset.address_y = unreal.TextureAddress.TA_CLAMP

main()

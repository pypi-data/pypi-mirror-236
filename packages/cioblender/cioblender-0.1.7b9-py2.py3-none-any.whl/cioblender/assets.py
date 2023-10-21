import bpy
import os
from ciopath.gpath_list import PathList, GLOBBABLE_REGEX
import logging

logger = logging.getLogger(__name__)

STARTUP_VAL = "startup.blend"

def resolve_payload(**kwargs):
    """
    Resolve the upload_paths field for the payload.

    This function gathers a list of file paths to be uploaded, including auxiliary paths,
    extra assets, and scanned assets, and returns them as a dictionary.

    :param kwargs: A dictionary of keyword arguments that may include "blender_filepath".
    :return: A dictionary containing the "upload_paths" key with a list of file paths.
    """
    path_list = PathList()

    path_list.add(*auxiliary_paths(**kwargs))
    path_list.add(*extra_paths())
    path_list.add(*scan_assets())

    return {"upload_paths": [p.fslash() for p in path_list]}

def auxiliary_paths(**kwargs):
    """
    Get auxiliary paths.

    This function retrieves auxiliary paths, specifically the "blender_filepath" if it exists.

    :param kwargs: A dictionary of keyword arguments that may include "blender_filepath".
    :return: A PathList object containing auxiliary paths.
    """
    path_list = PathList()
    try:
        blender_filepath = kwargs.get("blender_filepath")
        blender_filepath = blender_filepath.replace("\\", "/")
        if blender_filepath and STARTUP_VAL not in blender_filepath:
            # Check if blender_filepath exists
            if os.path.exists(blender_filepath):
                path_list.add(blender_filepath)
                path_list.real_files()
            else:
                logger.debug("Unable to find blender_filepath: {}".format(blender_filepath))
    except Exception as e:
        logger.debug("Unable to load blender_filepath, error: {}".format(e))
    return path_list

def extra_paths():
    """
    Add extra assets.

    This function retrieves extra assets from the current Blender scene and adds them to the PathList.

    :return: A PathList object containing extra asset paths.
    """
    path_list = PathList()
    try:
        scene = bpy.context.scene
        extra_assets_list = scene.extra_assets_list

        for asset in extra_assets_list:
            if asset.file_path and STARTUP_VAL not in asset.file_path:
                # Check if asset.file_path exists
                if os.path.exists(asset.file_path):
                    path_list.add(asset.file_path)
                    path_list.real_files()
                else:
                    logger.debug("Unable to find extra asset: {}".format(asset.file_path))
    except Exception as e:
        logger.debug("Unable to load extra assets, error: {}".format(e))

    return path_list

def scan_assets():
    """
    Scan assets in the current Blender project and return a PathList containing their paths.

    :return: A PathList object containing the paths of scanned assets.
    """
    path_list = PathList()

    path_list.add(*scan_materials())
    path_list.add(*scan_objects())
    path_list.add(*scan_linked_libraries())
    path_list.add(*scan_objects_with_overrides())

    return path_list

def scan_materials():
    """
    Scan materials in the current Blender project and add their image paths to the PathList.

    :return: A PathList object containing image paths from materials with nodes.
    """
    path_list = PathList()
    try:
        if not bpy.data.materials:
            return path_list
        # Iterate through all materials in the scene
        for material in bpy.data.materials:
            if not material.use_nodes:
                continue
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image:
                    image_filepath = bpy.path.abspath(node.image.filepath)
                    # check if the image_filepath exists
                    if os.path.exists(image_filepath):
                        path_list.add(image_filepath)
                        path_list.real_files()
                    else:
                        logger.debug("Unable to find image_filepath: {}".format(image_filepath))
    except Exception as e:
        logger.debug("Unable to scan materials, error: {}".format(e))

    return path_list

def scan_objects():
    """
    Scan objects in the current Blender project and add image paths from materials with nodes to the PathList.

    :return: A PathList object containing image paths from materials in mesh objects.
    """
    path_list = PathList()

    try:
        if not bpy.data.objects:
            return path_list
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if not slot.material:
                        continue
                    if slot.material and slot.material.use_nodes:
                        for node in slot.material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE' and node.image:
                                image_filepath = bpy.path.abspath(node.image.filepath)
                                # check if the image_filepath exists
                                if os.path.exists(image_filepath):
                                    path_list.add(image_filepath)
                                    path_list.real_files()
                                else:
                                    logger.debug("Unable to find image_filepath: {}".format(image_filepath))
    except Exception as e:
        logger.debug("Unable to scan objects, error: {}".format(e))
    return path_list

def scan_linked_libraries():
    """
    Scan linked libraries in the current Blender project and add their paths to the PathList.

    :return: A PathList object containing paths of linked libraries.
    """
    path_list = PathList()

    try:
        if not bpy.data.libraries:
            return path_list
        for library in bpy.data.libraries:
            # Check if the library is linked or used in the scene
            if library.users > 0:
                library_filepath = bpy.path.abspath(library.filepath)
                # check if the library_filepath exists
                if os.path.exists(library_filepath):
                    path_list.add(library_filepath)
                    path_list.real_files()
                else:
                    logger.debug("Unable to find linked library: {}".format(library_filepath))
    except Exception as e:
        logger.debug("Unable to scan linked libraries, error: {}".format(e))
    return path_list

def scan_objects_with_overrides():
    """
    Scan objects with library overrides and add material library paths to the PathList.

    :return: A PathList object containing material library paths of objects with overrides.
    """
    path_list = PathList()

    try:
        if not bpy.context.scene.objects:
            return path_list
        for obj in bpy.context.scene.objects:
            if obj.is_library_indirect:
                for slot in obj.material_slots:
                    if not slot.material:
                        continue
                    material_filepath = bpy.path.abspath(slot.material.library.filepath)
                    # check if the material_filepath exists
                    if os.path.exists(material_filepath):
                        path_list.add(material_filepath)
                        path_list.real_files()
                    else:
                        logger.debug("Unable to find object with override: {}".format(material_filepath))
    except Exception as e:
        logger.debug("Unable to scan objects with overrides, error: {}".format(e))
    return path_list


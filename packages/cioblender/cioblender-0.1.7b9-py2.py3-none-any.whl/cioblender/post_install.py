import os
import sys
import shutil

def fslash(path):
    """
    Replace backslashes with forward slashes in the given path.

    :param path: A string representing a file path.
    :return: A string with backslashes replaced by forward slashes.
    """
    return path.replace("\\", "/")

PLATFORM = sys.platform
PWD = os.path.dirname(os.path.abspath(__file__))
CIO_DIR = fslash(os.path.dirname(PWD))

ADDOON_FILE = os.path.join(PWD, "conductor_submitter_plugin.py")
INIT_CONTENT = """
import sys
CIO_DIR = '{}'
sys.path.insert(1, CIO_DIR)
                       
from cioblender import conductor_submitter_plugin

bl_info = {{
    'name': 'Conductor Render Submitter',
    'author': 'Conductor Technologies, CoreWeave',
    'version': (0, 1),
    'blender': (3, 6, 1),
    'location': 'Render > Properties',
    'description': 'Render submitter UI for Conductor',
    'category': 'Render',
}}

def register():
    conductor_submitter_plugin.register()

def unregister():
    conductor_submitter_plugin.unregister()

if __name__ == '__main__':
    register()
""".format(CIO_DIR)


def create_plugin_at_blender_folders(platform):
    """
    Copy the Conductor Blender plugin to Blender addon folders based on the platform.

    :param platform: The platform identifier (e.g., "win", "linux", "darwin").
    :return: A list of folders where the plugin was copied to.
    """
    user_home = os.path.expanduser("~")
    blender_versions_folder = None
    copied_folders = []
    addon_destination = ""
    try:
        if platform.startswith("win"):
            blender_versions_folder = os.path.join(user_home, "AppData/Roaming/Blender Foundation/Blender")
        elif platform.startswith("linux"):
            blender_versions_folder = os.path.join(user_home, ".config/blender")
        elif platform.startswith("darwin"):
            blender_versions_folder = os.path.join(user_home, "Library/Application Support/Blender")

        if blender_versions_folder:
            for version_folder in os.listdir(blender_versions_folder):
                addon_folder = os.path.join(blender_versions_folder, version_folder, "scripts/addons")
                if not os.path.exists(addon_folder):
                    try:
                        os.makedirs(addon_folder)
                    except:
                        #print("Unable to create folder: {}".format(addon_folder))
                        continue

                addon_destination = os.path.join(addon_folder, "conductor.py")

                with open(addon_destination, "w", encoding="utf-8") as f:
                    f.write(INIT_CONTENT + "\n")
                copied_folders.append(addon_folder)
                
    except Exception as e:
        print("Unable to copy plugin {} to folder {}, error: {}".format(ADDOON_FILE, addon_destination, e))

    return copied_folders


def main():
    """
    Main function for setting up the Conductor Blender addon.

    This function adds the CIO_DIR path to the beginning of the addon file and copies the addon to Blender's
    addon folders based on the platform.
    """
    if not PLATFORM.startswith(("win", "linux", "darwin")):
        sys.stderr.write("Unsupported platform: {}".format(PLATFORM))
        sys.exit(1)

    copied_folders = create_plugin_at_blender_folders(PLATFORM)

    if copied_folders:
        sys.stdout.write("Created Conductor Blender plugin at the following folders:\n")
        for folder in copied_folders:
            sys.stdout.write(folder + "\n")
        sys.stdout.write("Completed Blender addon setup!\n")
    else:
        sys.stderr.write("No Blender addon folders found.\n")

if __name__ == "__main__":
    main()

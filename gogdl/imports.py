import os
import glob
import json
import logging
from sys import exit

def get_info(args, unknown_args):
    logger = logging.getLogger("IMPORT")
    path = args.path
    if not os.path.exists(path):
        logger.error("Provided path is invalid!")
        exit(1)
    game_details = load_game_details(path)

    info_file = game_details[0]
    build_id_file = game_details[1]
    platform = game_details[2]
    f = open(info_file, 'r')
    info = json.loads(f.read())
    f.close()


    game_id = info['rootGameId']
    build_id = info.get("buildId")
    installed_language = ""
    if 'languages' in info:
        installed_language = info['languages'][0]
    elif 'language' in info:
        installed_language = info['language']
    else:
        installed_language = 'en-US'
    if build_id_file:
        f = open(build_id_file, 'r')
        build = json.loads(f.read())
        f.close()
        build_id = build.get("buildId")

    version_name = build_id
    if build_id and platform != 'linux':
        # Get version name
        builds = dl_utils.get_json(
            self.api_handler, f'{constants.GOG_CONTENT_SYSTEM}/products/{self.dl_target["id"]}/os/{self.platform}/builds?generation=2')

        target_build = builds['items'][0]
        for build in builds['items']:
            if build['build_id'] == build_id:
                target_build = build
                break
        version_name = target_build['version_name']

    print(json.dumps({
        "appName": game_id,
        "buildId": build_id,
        "title": info['name'],
        "tasks": info["playTasks"],
        "installedLanguage": installed_language,
        "platform":platform,
        "versionName":version_name
    }))

def load_game_details(path):
    found = glob.glob(os.path.join(path, 'goggame-*.info'))
    build_id = glob.glob(os.path.join(path, 'goggame-*.id'))
    platform = "windows"
    if not found:
        found = glob.glob(os.path.join(path, "Contents", "Resources", 'goggame-*.info'))
        build_id = glob.glob(os.path.join(path, "Contents", "Resources", 'goggame-*.id'))
        platform='osx'
    if not found:
        found = glob.glob(os.path.join(path,'game', 'goggame-*.info'))
        build_id = glob.glob(os.path.join(path, "game", 'goggame-*.id'))
        platform = 'linux'
    return (found[0], build_id[0] if build_id else None, platform)
import os
import sys
import datetime
import subprocess
import shutil
import json
from CPCReady import common as cm


##
# Create SCR image
#
# @param project: image filename
# @param mode: CPC mode (0, 1, 2)
# @param fileout: folder out
# @param dsk: if create dsk
# @param api: function in code o out
##

def getData(filename, mode,api=False):
    
    ########################################
    # VARIABLES
    ########################################

    IMAGE_TEMP_PATH = cm.TEMP_PATH + "/." + os.path.basename(filename)
    IMAGE_TMP_FILE = os.path.basename(os.path.splitext(filename)[0])

    if not os.path.exists(cm.TEMP_PATH):
        os.mkdir(cm.TEMP_PATH)

    ########################################
    # WE CHECK IF WE COMPLY WITH RULE 6:3
    ########################################

    IMAGE_TMP_JSON = IMAGE_TEMP_PATH + "/" + IMAGE_TMP_FILE + ".json"

    if len(IMAGE_TMP_FILE) > 6:
        IMAGE_TMP_FILE =  IMAGE_TMP_FILE[:6]
        
    ########################################
    # DELETE TEMPORAL FILES
    ########################################

    cm.rmFolder(IMAGE_TEMP_PATH)

    cmd = [cm.MARTINE, '-in', filename, '-mode', str(mode), '-out', IMAGE_TEMP_PATH, '-json']

    ########################################
    # EXECUTE MARTINE
    ########################################
    if api == False:
        cm.showHeadDataProject(cm.getFileExt(filename))

    try:
        subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        cm.msgError(f'Error ' + cm.getFileExt(filename) + f' executing command: {e.output.decode()}')
        ########################################
        # DELETE TEMPORAL FILES
        ########################################

        cm.rmFolder(IMAGE_TEMP_PATH)
        

    ########################################
    # READ JSON PALETTE
    ########################################

    with open(IMAGE_TMP_JSON) as f:
        data = json.load(f)

    sw_palette = str(data['palette'])
    hw_palette = str(data['hardwarepalette'])
    ugBasic_palette = []
    
    for color in data['palette']:
        palette_amstrad = cm.CONVERSION_PALETTE.get("COLOR_" + color)
        ugBasic_palette.append(palette_amstrad)
    
    ug_palette = str(ugBasic_palette)

    ########################################
    # IF PARAM DSK IS TRUE
    ########################################

    cm.msgInfo(f"Software : {sw_palette}")
    cm.msgInfo(f"Hardware : {hw_palette}")
    cm.msgInfo(f"UgBasic  : {ug_palette}")

    ########################################
    # DELETE TEMPORAL FILES
    ########################################

    cm.rmFolder(IMAGE_TEMP_PATH)

    ########################################
    # SHOW FOOTER
    ########################################

    cm.showFoodDataProject(f"{cm.getFileExt(filename)} GET SUCCESSFULLY PALETTE.", 0)
    
    return True



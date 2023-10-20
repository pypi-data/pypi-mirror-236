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
# @param height: height size
# @param width: width size
# @param api; if funcion or not
##

def create(filename, mode, fileout, height, width, api=False):
    
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

    if len(IMAGE_TMP_FILE) > 6:
        IMAGE_TMP_TXT = IMAGE_TEMP_PATH + "/" + IMAGE_TMP_FILE[:6].upper() + ".TXT"
        IMAGE_TMP_CTXT = IMAGE_TEMP_PATH + "/" + IMAGE_TMP_FILE[:6].upper() + "C.TXT"
    else:
        IMAGE_TMP_TXT = IMAGE_TEMP_PATH + "/" + IMAGE_TMP_FILE.upper() + ".TXT"
        IMAGE_TMP_CTXT = IMAGE_TEMP_PATH + "/" + IMAGE_TMP_FILE.upper() + "C.TXT"
        
    IMAGE_TMP_JSON = IMAGE_TEMP_PATH + "/" + IMAGE_TMP_FILE + ".json"

    cm.rmFolder(IMAGE_TEMP_PATH)

    cmd = [cm.MARTINE, '-in', filename, '-width', str(width), '-height', str(height), '-mode', str(mode), '-out',
           IMAGE_TEMP_PATH, '-json', '-noheader']

    ########################################
    # EXECUTE MARTINE
    ########################################
    if api == False:
        cm.showHeadDataProject(cm.getFileExt(filename))

    try:
        if fileout:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            if not os.path.exists(fileout):
                os.makedirs(fileout)
        else:
            subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        cm.msgError(f'Error ' + cm.getFileExt(filename) + f' executing command: {e.output.decode()}')
        cm.rmFolder(IMAGE_TEMP_PATH)
        if api == False:
            cm.showFoodDataProject(IMAGE_TMP_FILE.upper() + ".DSK NOT CREATED.", 1)
        else:
            cm.showFoodDataProject(f"{fileout}/{IMAGE_TMP_FILE.upper()}.SCR NOT CREATED.", 1)
            return False

    ########################################
    # READ JSON PALETTE
    ########################################

    with open(IMAGE_TMP_JSON) as f:
        data = json.load(f)

    sw_palette = str(data['palette'])
    hw_palette = str(data['hardwarepalette'])

    ########################################
    # GENERATE C FILE
    ########################################

    only = 0
    copy = False
    with open(IMAGE_TMP_CTXT, 'r') as input_file:
        with open(fileout + "/" + IMAGE_TMP_FILE.upper() + ".C", 'w') as output_file:
            if only == 0:
                output_file.write("array byte " + IMAGE_TMP_FILE + " = {\n")
                only = 1
            for line in input_file:
                if line.startswith('; width'):
                    copy = True
                    continue
                elif line.startswith('; Palette'):
                    copy = False
                    continue
                if copy:
                    output_file.write(line.replace("db ", "   "))
            output_file.write("};\n")

    cm.msgInfo(f"Create C   File ==> " + IMAGE_TMP_FILE.upper() + ".C")
    
    ########################################
    # GENERATE ASM FILE
    ########################################

    only = 0
    with open(IMAGE_TMP_TXT, 'r') as input_file:
        with open(fileout + "/" + IMAGE_TMP_FILE.upper() + ".ASM", 'w') as output_file:
            if only == 0:
                output_file.write(";------ BEGIN SPRITE --------\n")
                output_file.write(IMAGE_TMP_FILE)
                output_file.write("\ndb " + str(width) + " ; ancho")
                output_file.write("\ndb " + str(height) + " ; alto\n")
                only = 1
            for line in input_file:
                if line.startswith('; width'):
                    copy = True
                    continue
                elif line.startswith('; Palette'):
                    copy = False
                    continue
                if copy:
                    output_file.write(line)
            output_file.write("\n;------ END SPRITE --------\n")

    cm.msgInfo(f"Create ASM File ==> " + IMAGE_TMP_FILE.upper() + ".ASM")
    cm.msgInfo(f"       SW PALETTE : {sw_palette}")
    cm.msgInfo(f"       HW PALETTE : {hw_palette}")

    if api == False:
        cm.showFoodDataProject("SPRITE FILES SUCCESSFULLY CREATED.", 0)

    cm.rmFolder(IMAGE_TEMP_PATH)
    
    return True

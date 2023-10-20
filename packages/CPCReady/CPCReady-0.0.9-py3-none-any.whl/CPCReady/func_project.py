import os
import sys
import datetime
import shutil

from CPCReady import common as cm



##
# Create project
#
# @param project: Project name
# @param model: CPC model
##

def create(project, model):
    if sys.platform == "win64" or sys.platform == "win32":
        user = os.getenv('USERNAME')
    else:
        user = os.getenv('USER') or os.getenv('LOGNAME')

    folder_project = f"{project}"

    current_datetime = datetime.datetime.now()
   

    # cm.banner(str(model))
    cm.showHeadDataProject(project)

    if os.path.exists(folder_project) and os.path.isdir(folder_project):
        cm.msgError(f"The {folder_project} project name exists on this path.")
        cm.showFoodDataProject("The project could not be created.", 1)
        sys.exit(1)
        # cm.endCreteProject("ERROR")
    else:
        os.makedirs(f"{folder_project}")
        cm.msgInfo(f"Create Project: {folder_project}")

    cm.msgInfo("CPC Model: " + str(model))

    ########################################
    # CREATE PROJECT FOLDERS
    ########################################
    for folders in cm.subfolders:
        os.makedirs(f"{folder_project}/{folders}")
        cm.msgInfo(f"Create folder: {folder_project}/{folders}")

    ########################################
    # CREATE TEMPLATES PROJECT
    ########################################
    
    ## PROJECT
    DATA = {'name': project,'user': user,'rvm_path': "",'date':current_datetime, "model": model}
    cm.createTemplate("project.cfg",  DATA, f"{folder_project}/{cm.PATH_CFG}")
    cm.createTemplate("emulators.cfg", DATA, f"{folder_project}/{cm.PATH_CFG}")
    cm.createTemplate("images.cfg",   DATA, f"{folder_project}/{cm.PATH_CFG}")
    cm.createTemplate("sprites.cfg",  DATA, f"{folder_project}/{cm.PATH_CFG}")
    cm.createTemplate("MAIN.BAS",     DATA, f"{folder_project}/{cm.PATH_SRC}")
    cm.createTemplate("MAIN.UGB",     DATA, f"{folder_project}/{cm.PATH_SRC}")

    cm.msgInfo(f"Create Template Files project")

    if sys.platform != "win64" or sys.platform != "win32":
        cm.createTemplate("Makefile", DATA, folder_project)
        cm.msgInfo(f"Create Makefile: {folder_project}/Makefile")

    cm.showFoodDataProject(f"{project} PROJECT SUCCESSFULLY CREATED.", 0)

from ctypes.wintypes import RGB
import os
import sys
import datetime
import time
import logging
import shutil
import configparser
from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text
from rich.console import Console
from rich import inspect
from rich.table import Table
from rich import print
from rich.columns import Columns
from configparser import ConfigParser
import configparser as cfg
from jinja2 import Template
import ipaddress as ip
import platform
import subprocess
import requests
import os


console = Console()
log = logging.getLogger("rich")

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=False, show_path=False,omit_repeated_times=True)]
)

CPC464 = """[grey]█▀▀█ █▀▄▀█ █▀▀▀█ ▀▀█▀▀ █▀▀█ █▀▀█ █▀▀▄                                     ╔═╗╔═╗╔═╗ ┏┓┏┓┏┓ ┌─────────────┐  ON 🟢
[grey]█▄▄█ █ █ █ ▀▀▀▄▄   █   █▄▄▀ █▄▄█ █  █                                     ║  ╠═╝║   ┃┃┣┓┃┃ │[red] ███ [green]███ [blue]███ [white]│
[grey]█  █ █   █ █▄▄▄█   █   █  █ █  █ █▄▄▀     64K COLOUR PERSONAL COMPUTER[white]    ╚═╝╩  ╚═╝ ┗╋┗┛┗╋ └─────────────┘ COLOR"""

CPC6128 = """[grey]█▀▀█ █▀▄▀█ █▀▀▀█ ▀▀█▀▀ █▀▀█ █▀▀█ █▀▀▄                                                      ┌─────────────┐  ENC.
[grey]█▄▄█ █ █ █ ▀▀▀▄▄   █   █▄▄▀ █▄▄█ █  █                                                      │[red] ███ [green]███ [blue]███ [white]│  [green]▄▄▄[/green]
[grey]█  █ █   █ █▄▄▄█   █   █  █ █  █ █▄▄▀     128K ORDENADOR PERSONAL[white]                          └─────────────┘"""

CPC664 = """[grey]█▀▀█ █▀▄▀█ █▀▀▀█ ▀▀█▀▀ █▀▀█ █▀▀█ █▀▀▄                                     ╔═╗╔═╗╔═╗ ┏┓┏┓┏┓ ┌─────────────┐  ON 🟢
[grey]█▄▄█ █ █ █ ▀▀▀▄▄   █   █▄▄▀ █▄▄█ █  █                                     ║  ╠═╝║   ┣┓┣┓┃┃ │[red] ███ [green]███ [blue]███ [white]│
[grey]█  █ █   █ █▄▄▄█   █   █  █ █  █ █▄▄▀     64K COLOUR PERSONAL COMPUTER[white]    ╚═╝╩  ╚═╝ ┗┛┗┛┗╋ └─────────────┘ COLOR"""

## Common Variables
#
##

subfolders        = ["out", "out/disc", "src", "cfg","lib","img","spr","docs"]
PWD               = os.getcwd() + "/"
TEMPLATE_RVM_WEB  = "rvm-web.html"
PATH_CFG          = "cfg"
PATH_DISC         = "out/disc"
PATH_OBJ          = "obj"
PATH_SRC          = "src"
PATH_DSK          = "out"
PATH_LIB          = "lib"
PATH_SPR          = "spr"
PATH_ASSETS       = "img"
CFG_PROJECT       = f"{PATH_CFG}/project.cfg"
CFG_EMULATORS     = f"{PATH_CFG}/emulators.cfg"
CFG_IMAGES        = f"{PATH_CFG}/images.cfg"
CFG_SPRITES       = f"{PATH_CFG}/sprites.cfg"
APP_PATH          = os.path.dirname(os.path.abspath(__file__))
SECTIONS_PROJECT  = ["general", "configurations", "CDT", "DSK"]
SECTIONS_EMULATOR = ["rvm-web", "rvm-desktop","m4board"]
CPC_MODELS        = ["6128","464","664"]

if sys.platform == "win32":
    cm.msgError(f"WIN32 Platform not supported")
    sys.exit(1)   

if sys.platform == "win64":
    TEMP_PATH = os.getenv('USERPROFILE') + "/tmp"
    MARTINE   = os.path.dirname(os.path.abspath(__file__)) + "/tools/win/martine.exe"
    DSK       = os.path.dirname(os.path.abspath(__file__)) + "/bin/win64/iDSK.exe"
    UGBASIC   = os.path.dirname(os.path.abspath(__file__)) + "/tools/win64/ugbc.exe"
    AMSDOS    = os.path.dirname(os.path.abspath(__file__)) + "/tools/win64/amsdos.exe"
    CDT       = os.path.dirname(os.path.abspath(__file__)) + "/tools/win64/2cdt.exe"
    M4BOARD   = os.path.dirname(os.path.abspath(__file__)) + "/tools/win64/xfer.exe"
    CPC2CDT   = os.path.dirname(os.path.abspath(__file__)) + "/tools/win64/cpc2cdt.exe"
if sys.platform == 'darwin':
    TEMP_PATH = os.getenv('HOME') + "/tmp"
    MARTINE   = os.path.dirname(os.path.abspath(__file__)) + "/tools/" + sys.platform + "/martine"
    IDSK      = os.path.dirname(os.path.abspath(__file__)) + "/tools/darwin/iDSK"
    AMSDOS    = os.path.dirname(os.path.abspath(__file__)) + "/tools/darwin/amsdos"
    CDT       = os.path.dirname(os.path.abspath(__file__)) + "/tools/darwin/2cdt"
    CPC2CDT   = os.path.dirname(os.path.abspath(__file__)) + "/tools/darwin/cpc2cdt"
    M4BOARD   = os.path.dirname(os.path.abspath(__file__)) + "/tools/darwin/xfer"
if sys.platform.startswith('linux'):
    TEMP_PATH = os.getenv('HOME') + "/tmp"
    MARTINE   = os.path.dirname(os.path.abspath(__file__)) + "/tools/" + sys.platform + "/martine"
    IDSK      = os.path.dirname(os.path.abspath(__file__)) + "/tools/linux/iDSK"
    UGBASIC   = os.path.dirname(os.path.abspath(__file__)) + "/tools/linux/ugbc"
    UGBASIC2   = os.path.dirname(os.path.abspath(__file__)) + "/tools/linux"
    UGBASICSH = os.path.dirname(os.path.abspath(__file__)) + "/tools/linux/ugbcsh"
    AMSDOS    = os.path.dirname(os.path.abspath(__file__)) + "/tools/linux/amsdos"
    CDT       = os.path.dirname(os.path.abspath(__file__)) + "/tools/linux/2cdt"
    CPC2CDT   = os.path.dirname(os.path.abspath(__file__)) + "/tools/linux/cpc2cdt"
    M4BOARD   = os.path.dirname(os.path.abspath(__file__)) + "/tools/linux/xfer"


CONVERSION_PALETTE = {
    "COLOR_0":"RGB(0,0,0)",
    "COLOR_1":"RGB(0,0,128)",
    "COLOR_2":"RGB(0,0,255)",
    "COLOR_3":"RGB(128,0,0)",
    "COLOR_4":"RGB(128,0,128)",
    "COLOR_5":"RGB(128,0,255)",
    "COLOR_6":"RGB(255,0,0)",
    "COLOR_7":"RGB(255,0,128)",
    "COLOR_8":"RGB(255,0,255)",
    "COLOR_9":"RGB(0,128,0)",
    "COLOR_00":"RGB(0,0,0)",
    "COLOR_01":"RGB(0,0,128)",
    "COLOR_02":"RGB(0,0,255)",
    "COLOR_03":"RGB(128,0,0)",
    "COLOR_04":"RGB(128,0,128)",
    "COLOR_05":"RGB(128,0,255)",
    "COLOR_06":"RGB(255,0,0)",
    "COLOR_07":"RGB(255,0,128)",
    "COLOR_08":"RGB(255,0,255)",
    "COLOR_09":"RGB(0,128,0)",
    "COLOR_10":"RGB(0,128,128)",
    "COLOR_11":"RGB(0,128,255)",
    "COLOR_12":"RGB(128,128,0)",
    "COLOR_13":"RGB(128,128,128)",
    "COLOR_14":"RGB(128,128,255)",
    "COLOR_15":"RGB(255,128,0)",
    "COLOR_16":"RGB(255,128,128)",
    "COLOR_17":"RGB(255,128,255)",
    "COLOR_18":"RGB(0,255,0)",
    "COLOR_19":"RGB(0,255,128)",
    "COLOR_20":"RGB(0,255,255)",
    "COLOR_21":"RGB(128,255,0)",
    "COLOR_22":"RGB(128,255,128)",
    "COLOR_23":"RGB(128,255,255)",
    "COLOR_24":"RGB(255,255,0)",
    "COLOR_25":"RGB(255,255,128)",
    "COLOR_26":"RGB(255,255,255)"
}



##
# create template file
#
# @param tempaletename: template name
# @param templatedata: template data
# @param out: generate template directory
##
def createTemplate(templateName, templateData, out):
    
    APP_PATH = os.path.dirname(os.path.abspath(__file__))
    with open(APP_PATH + f"/templates/{templateName}.j2", 'r') as file:
        template_string = file.read()
    template = Template(template_string)
    rendered_template = template.render(templateData)
    with open(out + "/" + templateName, 'w') as file:
        file.write(rendered_template)


##
# Delete folder
#
# @param directory: directory to remove
##
def rmFolder(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        shutil.rmtree(directory)

##
# get data ini/cfg file
#
# @param cfgfile: path filename
##
def getData(cfgFile):
    config = configparser.ConfigParser()
    config.read(cfgFile)
    return config

##
# Show banner dependencie model cpc
#
# @param cpc: Model CPC
##
def banner(cpc):
    BANNER = Table(show_header=False)

    if cpc == "6128":
        BANNER.add_row(CPC6128)
    elif cpc == "464":
        BANNER.add_row(CPC464)
    elif cpc == "664":
        BANNER.add_row(CPC664)
    else:
        msgError("Model CPC not supported")
        sys.exit(1)

    console.print(BANNER)


##
# Print message warning
#
# @param file: File to which the message refers
# @param message: message to display
##
def msgWarning(message):
    log.warning(message)


##
# Print message eror
#
# @param file: File to which the message refers
# @param message: message to display
##
def msgError(message):
    log.error(message)


##
# Print message info
#
# @param file: File to which the message refers
# @param message: message to display
##
def msgInfo(message):
    log.info(message, extra={"highlighter": None})


##
# Print message debug
#
# @param file: File to which the message refers
# @param message: message to display
##
def msgInfo(message):
    log.info(message)


##
# Get Get file without extension
#
# @param source: source filename
##
def getFile(source):
    file_name = os.path.basename(source)
    file_name = os.path.splitext(file_name)[0]
    return file_name


##
# Get file and extension
#
# @param source: source filename
##
def getFileExt(source):
    file_name = os.path.basename(source)
    return file_name


##
# Get extension file
#
# @param source: source filename
##
def getFileExtension(source):
    file_extension = os.path.splitext(source)[1]
    return file_extension

##
# Show head data proyect
#
# @param project: project name
##

def showHeadDataProject(project):
    description = f"*** {project} ***"
    center_text = description.center(80)
    console.print(
        "[bold yellow]\n==================================================================================== [/bold yellow]")
    console.print("[bold yellow]" + center_text.upper() + "[/bold yellow]")
    console.print(
        "[bold yellow]====================================================================================\n [/bold yellow]")


##
# Show food data proyect
#
# @param description: description to show
# @param out: 1 is error, 0 is ok
##

def showFoodDataProject(description, out):
    description = f"*** {description} ***"
    center_text = description.center(80)
    console.print(
        "[bold yellow]\n==================================================================================== [/bold yellow]")
    if out == 0:
        console.print("[bold green]" + center_text.upper() + "[/bold green]")
        console.print("[bold yellow]====================================================================================\n [/bold yellow]")
    if out == 1:
        console.print("[bold red]" + center_text.upper() + "[/bold red]")
        console.print("[bold yellow]====================================================================================\n [/bold yellow]")
        sys.exit(1)


##
# verify file exist
#
# @param source: source file name
##
def fileExist(source):
    if not os.path.isfile(source):
        msgError(f"File {source} does not exist.")
        return False
    return True


##
# Remove directory
#
# @param directory: directory name
##
def removeContentDirectory (directory):

    if os.path.exists(directory) and os.path.isdir(directory):
        archivos = os.listdir(directory)
        for archivo in archivos:
            ruta_completa = os.path.join(directory, archivo)
            if os.path.isfile(ruta_completa):
                os.remove(ruta_completa)
    msgInfo(f"Clean temporal directory.")            
                
##
# compilation image
#
# @param project: image name
##
def imageCompilation(image):
    console.print(
        "\n[bold white]------------------------------------------------------------------------------------- [/bold white]")
    console.print("[bold blue] IMAGE: [/bold blue][bold white]" + image + "[/bold white]")
    console.print(
        "[bold white]------------------------------------------------------------------------------------- [/bold white]\n")

def readProjectIni(file):
    config = configparser.ConfigParser()
    config.read(file)
    diccionario = {}
    for seccion in config.sections():
        diccionario[seccion] = {}
        for clave, valor in config.items(seccion):
            diccionario[seccion][clave] = valor
    return diccionario

def crear_entrada_ini(ruta_archivo, seccion, clave, valor):

    config = configparser.ConfigParser()
    config.read(ruta_archivo)
    if seccion not in config.sections():
        config.add_section(seccion)

    config.set(seccion, clave, valor)
    with open(ruta_archivo, 'w') as archivo:
        config.write(archivo)


def validateSection(file, sectionfile):
    config = configparser.ConfigParser()
    config.read(file)
    for seccion in config.sections():
        if seccion == sectionfile:
            return True
    return False

def validate_cfg(cfg,datos):
    if not fileExist(cfg):
        sys.exit(1)    
    for section in datos:
        if not validateSection(cfg,section):
            msgError(f"{section} section does not exist in the {cfg} file") 
            sys.exit(1)

def validateCPCModel(model): 
    for modelos in CPC_MODELS:
        if str(modelos) == str(model):
            return True
    return False
    

def validateIP(ip_string):
   try:
       ip_object = ip.ip_address(ip_string)
       msgInfo(f"IP address ==> {ip_string}") 
       return True
   except ValueError:
       msgError("IP address ==> '{ip_string}' is not valid")
       return False       


# def ping(host):
#     param = '-n' if platform.system().lower()=='windows' else '-c'
#     command = ['ping', param, '1', host]
#     return subprocess.call(command) == 0


# r = pyping.ping('google.com')

# if r.ret_code == 0:
#     print("Success")
# else:
#     print("Failed with {}".format(r.ret_code))
#     # config = configparser.ConfigParser()
#     # config.read(cfg)
#     # for seccion in config.sections():
#     #     print(f"{seccion}")
#     #     for clave, valor in config.items(seccion):
#     #         print(f"{clave} = {valor}")
#     #     print()
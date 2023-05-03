from os import startfile, system
from os.path import isfile
from sys import exit
from time import sleep
from timeit import default_timer
from urllib.request import urlretrieve
from webbrowser import open as webopen
from platform import release
# This has to be here
start = default_timer()
try:
    # Custom / Community made libs
    from colorama import init, Fore, Back
    from lastversion import latest
    from ping3 import ping
    from psutil import cpu_count, cpu_percent, disk_usage, virtual_memory
    from XeLib import cls, printer, download, color, getmyping
    from XTLLib import fwrite, runaspowershell, SetVars
except:
    print("Fixing libraries, wait...")
    #todo: add a warning message that this command will be run, in case someone prefers using virtal environments
    system("pip install -U psutil XeLib colorama lastversion XTLLib ping3")
    print("Libraries installed successfully!")

from xtools import Tool, tools

# This function defines a function called `eula()`
# that prints a warning message and asks the user
# to agree to a license agreement.
def eula():
    cls()

    # Print a warning message and sleep for 3 seconds
    print("Do Not Dumb License v1\n"
            "I'm not responsible for your dumb.")
    sleep(3)
    
    # Ask the user if they agree to the license agreement
    agree = yn(f"Do you agree? ({Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}): ")
    
    # If the user agrees, write "True" to the file EULA.XTB and set z to False
    if agree:
        print("You agreed to the EULA.")
        fwrite(0, 'EULA.XTB', 'True')
        z = False
    
    # If the user does not agree, exit the program
    else:
        print("Ok, come back if you change your mind."); exit(sleep(3))

# This function defines a function called `prep()`
# that checks the hardware requirements of the system
# and exits if they are not met.
def prep():
    # Clear the screen and print a message
    cls()
    printer.lprint("Initializing Libraries...")
    
    # Initialize the autoreset option of the colorama module
    init(autoreset=True)
    
    # Check the hardware requirements and ask the user
    # if they want to continue if the requirements are not met.
    printer.lprint("Checking hardware requirements...")
    if cpu_count(logical=True)<3 and cpu_count(logical=False)<2:
        printer.lprint("Your Processor don't meet the minimum hardware requirements (2C / 3T).\n"
                       "Do You want to continue anyways?")
        
        choose = yn(f"({Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}): ")
        if not choose: exit()

    if virtual_memory().total/1073741824<4:
        printer.lprint("Your RAM don't meet the minimum hardware requirements (4GB RAM).\n"
                       "Do You want to continue anyways?")
        choose = yn(f"({Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}): ")
        if not choose: exit()

    if int(release())<10:
        printer.lprint("Your windows version is older than 10, this program won't run. Upgrade to Windows 10/11 if you want to use this program.") ; exit(sleep(15))

    if not virtual_memory().total/1073741824<4 and cpu_count(logical=True)<3 and cpu_count(logical=False)<2 and int(release())<10:
        printer.lprint("All Hardware requirements met!")

# This function defines a function called `update()`
# that checks if the program is up to date and
# allows the user to update it if necessary.
def update():
    # Ask the user if they want to update the program
    print('Update?')
    doupdate = yn(f"({Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}): ")
    
    # If the user does not want to update, print a message and do nothing
    if not doupdate:
        print("Okey.")
        sleep(2)
    
    # If the user wants to update, try to download the latest version of the program
    # and run it. If the download fails, print an error message and exit.
    else:
        printer.lprint("Updating...")
        try:
            # save the latest version to avoid rate limiting
            latestXT = str(latest("xemulat/XToolbox"))
            # Download the latest version of the program
            download("https://github.com/xemulat/XToolbox/releases/download/v" + latestXT+"/XTBox.exe", "XTBox." + latestXT+".exe", "XTBox " + latestXT)
            startfile("XTBox." + latestXT + ".exe")
            exit()
        
        # If the download fails, print an error message and exit
        except:
            printer.lprint("Can't complete updates, aborting...") ; sleep(4) ; exit()


#function that interprets user input
#page is what the interface is showing and *args is additional info that may be required for some pages
#!return type is based on the page number! (if not stated otherwise, returns void)
def interpreter(page, prompt="> "):
    global lastPage
    choose = str(input(prompt)).strip().lower() # lower for easier iffing

    #if user inputs 99, exit the program
    if choose == "99":
        exit()

    #if user inputs h, open help
    if choose == "h" and page != 0 :
        # return the correct values to prevent crashes
        if page == 98 or page == 97:
            if lastPage != None: # prevent getting this message in EULA and similar functions
                print("Exit selection to access help!")
            return False, False
        else:
            while not helpe(): pass

    #page 0 (help)
    #returns true/false which indicate if helpe should close
    if page==0:
        # go back
        if choose == "b" or choose == "": 
            return True
        # elevate powershell execution policy
        if choose == "p": 
            # todo: add warning message that this command is about to be run (not every1 wants it)
            # best way to do that would be inside XTLLib
            runaspowershell("Set-ExecutionPolicy Unrestricted -Scope CurrentUser", "SetExecutionPolicy")
            return True
        # not valid option
        else:
            print("No option named " + choose)
            return False

    #for pages 1-3 (tool pickers)
    elif page >= 1 and page <= 3:
        #next page
        if choose == "n":
            if page==1: lastPage = p2
            elif page==2: lastPage = p3
            elif page==3: lastPage = p1
        #previous page
        elif choose == "b":
            if page==1: lastPage = p3
            elif page==2: lastPage = p1
            elif page==3: lastPage = p2
        #program ID entered
        elif (choose+"-"+str(page) in tools) and (choose != ""): dwnTool(tools[choose+"-"+str(page)])
        #other special options
        elif choose == "qt": quicktweaks()
        elif choose == "c6": chooseeset()
        elif choose == "c7": choosekas()
        #bad input
        else:
            print("No option named " + choose)
            sleep(3)
    
    #for page 10 (quicktweaks)
    elif page == 10:
        if choose == "b": lastPage = p1
        elif (choose+"-QT" in tools) and (choose != ""): dwnTool(tools[choose+"-QT"])
        elif choose == "2":
            dwnTool(tools[choose+"-QT-1"])
            dwnTool(tools[choose+"-QT-2"])
        else:
            print("No option named " + choose)
            sleep(3)

    #page 11 (ESET)
    elif page == 11:
        if choose == "b": lastPage = p1
        elif (choose+"-ESET" in tools) and (choose != ""):
            dwnTool(tools[choose+"-ESET"])
        else:
            print("No option named " + choose)
            sleep(3)

    #page 12 (Kaspersky)
    elif page == 12:
        if choose == "b": lastPage = p1
        elif (choose+"-KAS" in tools) and (choose !=""):
            dwnTool(tools[choose+"-KAS"])
        else:
            print("No option named "+ choose)
            sleep(3)

    #page 97 (y/n)
    #returns 2 bool args: correct/incorrect input, and y/n answer
    elif page == 97:
        if choose == "y": return True, True
        elif choose == "n": return True, False
        else:
            print("No option named "+ choose)
            return False, False

    #page 98 (multiple choice download)
    #returns 2 args: correct/incorrect input (bool), and the chosen option (int)
    #if user wants to exit selection, the second return value becomes negative
    elif page==98:
        # cancel (index < 0)
        if choose == "b": return True, -1
        # user choice
        elif choose.isnumeric() and int(choose) > 0:
            return True, int(choose)-1
        else:
            print("No option named " + choose)
            return False, 0

#function to reduce code when using interpreter() page 97
def yn(prompt="> "):
    goodInput, YNvalue = False
    while not goodInput:
        goodInput, YNvalue = interpreter(97, prompt)
    return YNvalue

#function for multiple choice downloads interpreter() page 98
#returns the index of chosen option, it can return -1 if the user canceled selection
#tool is <Tool>, prompt is <str>
def multiChoose(tool, prompt):
    # ┌──────────< B - back >──────────┐
    # │                                │
    # │ [1] name_name_name_1           │
    # │ [2] name_name_name_name_2      │
    # │                                │
    # ├────────────────────────────────┤
    # │    _________Prompt_________    │
    # └────────────────────────────────┘

    #determining window size
    size = 34 # min size
    if len(prompt)+10 > size: size = len(prompt)+10 # the +10 is because of minimum space on both sides of the prompt (|          |)
    for ind in range(len(tool.dwn)):
        if len(tool.getDesc(ind))+7+len(str(ind+1)) > size: #the +7 is because of the minimum possible space in an option (│ []  │)
            size = len(tool.getDesc(ind))+7+len(str(ind+1)) #ind +1 cuz ind goes from 0 to max-1

    #ensuring symmetry
    if len(prompt)%2 == 0:
        backMessage = "< B - back >"
        if size%2==1: size+=1
    else:
        backMessage = "< back: B >"
        if size%2==0: size+=1
    

    #the top bar
    print("┌" + "─"*int((size-2-len(backMessage))/2) + backMessage + "─"*int((size-2-len(backMessage))/2) + "┐")

    #empty line cuz it looks nice :D
    print("│" + " "*(size-2) + "│")

    #options
    for ind in range(len(tool.dwn)):
        print(f"│ [{ind+1}] {tool.getDesc(ind)}" + " "*int(size-6-len(tool.getDesc(ind))-len(str(ind+1))) + "│")

    #another empty
    print("│" + " "*(size-2) + "│")

    #prompt
    print("├" + "─"*(size-2) + "┤")    
    print("│" + " "*int((size-2-len(prompt))/2) + prompt + " "*int((size-2-len(prompt))/2) + "│")
    print("└" + "─"*(size-2) + "┘")


    goodInput = False
    while not goodInput:
        goodInput, index = interpreter(98)
        if index > len(tool.dwn): goodInput = False

    return index


#function that downloads a tool
def dwnTool(tool):
    if (len(tool.dwn)==0):
        raise LookupError(f"Tool {tool.name} has no download links")
    index = 0
    if (len(tool.dwn)!=1):
        if tool.code[0] == "l": prompt = "Choose your Distro Type"
        else: prompt = "Choose Verson"
        index = multiChoose(tool, prompt)
        if index < 0: return
        
    if tool.command==1:   dl(tool.getDwn(index), tool.getExec(index), tool.getName(index))
    elif tool.command==2: runaspowershell(tool.getDwn(index), tool.getName(index))
    elif tool.command==3: webopen(tool.getDwn(index))
    elif tool.command==4: urlretrieve(tool.getDwn(index), tool.getExec(index))
    elif tool.command==5: fwrite(tool.getDwn(index))


#function that downloads file from url
def dl(url, urlr, name):
    # The code below is redundant for now since download() cant overwrite a file
    # Best approach here would be to implement the functionality inside the XTLLib
    # # Try and except so the program won't crash when the website isn't accesible
    # try:
    #     if isfile(urlr) == True:
    #         printer.lprint("ERROR 1 - File " + urlr + " already exists!")
    #         overwrite = yn(f"{Fore.RED}[S>] Overwrite? {Fore.RESET}({Fore.GREEN}Y{Fore.RESET}/{Fore.RED}n{Fore.RESET}):")
    #         if not overwrite: return
    # except:
    #     printer.lprint("ERROR 2: Can't check for file overwrite. Missing file premissions?"); sleep(6)
    
    # Download module is located here.
    try:
        download(url, urlr, name)
        if name != "WindowsOnReins":
            run = yn(f"{Fore.RESET}Run {urlr}? ({Fore.GREEN}Y{Fore.RESET}/{Fore.RED}n{Fore.RESET}):")
            if run: startfile(urlr)
    except:
        printer.lprint("ERROR 3: Can't download file from the server...") ; sleep(3)


#help function is page 0
#returns if it should close
def helpe():
    cls()
    print("┌─────────────────────────────────────────────────────────────┐\n"
          "│  Keybind  │ Command                                         │\n"
          "│     H     │ Help Page (this page)                           │\n"
          "│     N     │ Next Page                                       │\n"
          "│  ENTER/B  │ Back                                            │\n"
          "│     UN    │ Uninstalls The Program                          │\n"
          "│     99    │ Exit                                            │\n"
          "├─────────────────────────────────────────────────────────────┤\n"
          "│ Color     │ Meaning                                         │\n"
         f"│ {e}       │ Dangerous Option                                │\n"
         f"│ {ng}      │ Option that can f*ck up your PC                 │\n"
         f"│ {ree}     │ Recommended Option                              │\n"
          "├─────────────────────────────────────────────────────────────┤\n"
          "│ Error code │ Explanation                                    │\n"
          "│      1     │ File already exists                            │\n"
          "│      2     │ Can't check for file overwrite                 │\n"
          "│      3     │ Can't download file from the server            │\n"
          "├─────────────────────────────────────────────────────────────┤\n"
          "│ If scrips won't execute, press P                            │\n"
          "├─────────────────────────────────────────────────────────────┤\n"
          "│                  Press ENTER/B to go back.                  │\n"
          "└─────────────────────────────────────────────────────────────┘\n")
    return interpreter(0)

#QuickTweaks is page 10
def quicktweaks():
    global lastPage; lastPage = quicktweaks
    cls()
    print(f"┌──────────────────────────┬──────────────────────────┐\n"
          f"│ [1] {AntiTrackTi}        │ [7] NoXboxBloat         R│\n"
          f"│ [2] NoNetworkAuto-Tune   │ [8] {LimitQ}            R│\n"
          f"│ [3] {optimizess}        R│ [9] XanderTweak         R│\n"
          f"│ [4] NoActionCenter      R│ [10] AddCopyPath        R│\n"
          f"│ [5] NoNews              R│ [11] DarkMode           R│\n"
          f"│ [6] NoOneDrive           │ [12] AddTakeOwnership   R│\n"
          f"│                          │                          │\n"
          f"├────┬────────────────────┬┴──────────┬──────────┬────┤\n"
          f"│    │ Choose your Tweaks │ 99 - Exit │ B - Back │    │\n"
          f"└────┴────────────────────┴───────────┴──────────┴────┘\n")
    interpreter(10)

#ESET is page 11
def chooseeset():
    global lastPage; lastPage = chooseeset
    cls()
    print(f"┌─────────────────────────────────────────────────────────────────────┐\n"
          f"│ [1] ESET Smart Security Premium                                     │\n"
          f"│ [2] ESET Internet Security                                          │\n"
          f"│ [3] ESET NOD32 Antivirus                                            │\n"
          f"│ [4] ESET NOD32 Antivirus Gamer Edition                              │\n"
          f"│ [5] ESET Security for Small Office                                  │\n"
          f"│                                                                     │\n"
          f"├─────────┬──────────────────────────┬───────────┬──────────┬─────────┤\n"
          f"│         │ Choose your ESET version │ 99 - Exit │ B - Back │         │\n"
          f"└─────────┴──────────────────────────┴───────────┴──────────┴─────────┘\n")
    interpreter(11)

#Kaspersky is page 12
def choosekas():
    global lastPage; lastPage = choosekas
    cls()
    print(f"┌──────────────────────────────────────────────────────────────────────┐\n"
          f"│ [1] Kaspersky Internet Security                                      │\n"
          f"│ [2] Kaspersky Anti-Virus                                             │\n"
          f"│ [3] Kaspersky Total Security                                         │\n"
          f"│                                                                      │\n"
          f"├───────┬───────────────────────────────┬───────────┬──────────┬───────┤\n"
          f"│       │ Choose your Kaspersky version │ 99 - Exit │ B - Back │       │\n"
          f"└───────┴───────────────────────────────┴───────────┴──────────┴───────┘\n")
    interpreter(12)

# page 1, 2, 3
def p1(preprint=False):
    global lastPage; lastPage = p1
    cls()
    if preprint is not False:
        print(preprint)
    print(  f"┌───────────────────────────────────────────────────┬────────────────────────────────┬────────────────────────────────┐\n"
            f"│ {xtoolbox00000000000000}                          │ Made by {xemulated000}         │ Internet: {ping0}              │\n"
            f"│ Update Status: {update0} │ RAM: {ramavailz}       │ CPU: {cpu00000000000} | {c}    │ Disk: {diskusage0000}          │\n"
            f"├──────────────────────────┼────────────────────────┼────────────────────────────────┼────────────────────────────────┤\n"
            f"│ [D] Debloat              │ [T] Tweaks             │ [A] Apps                       │ [C] Cleaning / Antiviruses     │\n"
            f"├──────────────────────────┼────────────────────────┼────────────────────────────────┼────────────────────────────────┤\n"
            f"│ [1] EchoX                │ [1] {posttweaksjfjfjf} │ [1] Chocholatey                │ [1] ADW Cleaner                │\n"
            f"│ [2] {neCtrl}             │ [2] Insider Enroller   │ [2] {rav}                      │ [2] ATF Cleaner                │\n"
            f"│ [3] ShutUp10             │ [3] Windows11Fixer     │ [3] {firef}                    │ [3] Defraggler                 │\n"
            f"│ [4] Optimizer            │ [4] AntiRoundCorners   │ [4] Lively Wallpaper           │ [4] {malwarebyt}               │\n"
            f"│ [5] PyDebloatX           │ [5] FixDrag&Drop       │ [5] LibreWolf                  │ [5] ESET Online Scanner        │\n"
            f"│ [6] {windowsonreinddddd} │ [6] Winaero Tweaker    │ [6] qBittorrent                │ [6] ESET                       │")
    print(  f"│ [7] QuickBoost           │ [7] CTT WinUtil        │ [7] Rainmeter                  │ [7] Kaspersky                  │\n"
            f"│ [8] Win10Debloater       │ [8] REAL               │ [8] 7-Zip                      │ [8] CleanMGR+                  │\n"
            f"│ [9] SadCoy               │ [9] NVCleanstall       │ [9] Memory Cleaner             │ [9] Glary Utilities            │\n"
            f"│ [10] {sweetyli}          │ [10] Twinker           │ [10] Compact Memory Cleaner    │                                │\n"
            f"│ [11] {ohdwindowwwwwwwww} │ [11] SophiApp          │                                │                                │\n"
            f"│ [12] WindowsSpyBlocker   │                        │                                │                                │\n"
            f"│ [13] PrivateZilla        │                        │                                │                                │\n"
            f"│ [14] ZusierAIO           │                        │                                │                                │\n"
            f"│ [15] CoutX               │ [QT] {quicktwea}       │                                │                                │\n"
            f"│                          │                        │                                │                                │\n"
            f"├──────────────────────────┴────────────────────────┴────────────────────────────────┴────────────────────────────────┤\n"
            f"│                           Ex.: 'D2' ─ HoneCtrl │ N ─ Next Page │ 99 ─ Exit │ H - Help                           1/3 │\n"
            f"└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘")
    interpreter(1)

def p2():
    global lastPage; lastPage = p2
    cls()
    print(  f"┌───────────────────────────────────────────────────┬────────────────────────────────┬────────────────────────────────┐\n"
            f"│ {xtoolbox00000000000000}                          │ Made by {xemulated000}         │ Internet: {ping0}              │\n"
            f"│ Update Status: {update0} │ RAM: {ramavailz}       │ CPU: {cpu00000000000} | {c}    │ Disk: {diskusage0000}          │\n"
            f"├──────────────────────────┼────────────────────────┼────────────────────────────────┼────────────────────────────────┤\n"
            f"│ [L] Linux Distros        │ [W] Windows versions   │ [M] Modded Windows versions    │ [T] Tools                      │\n"
            f"├──────────────────────────┼────────────────────────┼────────────────────────────────┼────────────────────────────────┤\n"
            f"│ [1] {minttuxe}           │ [1] {window11}         │ [1] {rectify}                  │ [1] {ruf}                      │\n"
            f"│ [2] Pop!_OS              │ [2] Windows 10         │ [2] {atlaso}                   │ [2] Balena Etcher              │\n"
            f"│ [3] Ubuntu               │ [3] Windows 8.1        │ [3] Ghost Spectre              │ [3] {unetboot}                 │")
    print(  f"│ [4] Arch Linux           │ [4] Windows 8          │ [4] ReviOS                     │ [4] HeiDoc Iso Downloader      │\n"
            f"│ [5] Artix Linux          │ [5] Windows 7          │ [5] GGOS                       │                                │\n"
            f"│ [6] Solus                │                        │ [6] {windowssimpli}            │                                │\n"
            f"│ [7] Debian               ├────────────────────────┤ [7] {aero}                     ├────────────────────────────────┤\n"
            f"│ [8] Garuda               │ [O] Other              │ [8] Tiny10                     │ [A] Apps                       │\n"
            f"│ [9] {zorino}             ├────────────────────────┤ [9] KernelOS                   ├────────────────────────────────┤\n"
            f"│ [10] CachyOS             │ [1] .NET 4.8 SDK       │ [10] Windows 7 Super Nano      │ [1] KeePassXC                  │\n"
            f"│                          │ [2] DirectX AIO        │ [11] Windows 11 Debloated      │ [2] PowerToys                  │\n"
            f"│                          │ [3] VisualCppRedist    │                                │ [3] Alacritty                  │\n"
            f"│                          │ [4] XNA Framework      │                                │ [4] PowerShell                 │\n"
            f"│                          │ [5] Python             │                                │ [5] Motrix                     │\n"
            f"│                          │                        │                                │ [6] Files                      │\n"
            f"│                          │                        │                                │                                │\n"
            f"├──────────────────────────┴────────────────────────┴────────────────────────────────┴────────────────────────────────┤\n"
            f"│                           Ex.: 'D2' ─ HoneCtrl │ N ─ Next Page │ 99 ─ Exit │ H - Help                           2/3 │\n"
            f"└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘")
    interpreter(2)

def p3():
    global lastPage; lastPage = p3
    cls()
    print(  f"┌───────────────────────────────────────────────────┬────────────────────────────────┬────────────────────────────────┐\n"
            f"│ {xtoolbox00000000000000}                          │ Made by {xemulated000}         │ Internet: {ping0}              │\n"
            f"│ Update Status: {update0} │ RAM: {ramavailz}       │ CPU: {cpu00000000000} | {c}    │ Disk: {diskusage0000}          │\n"
            f"├──────────────────────────┼────────────────────────┼────────────────────────────────┼────────────────────────────────┤\n"
            f"│ [L] Minecraft Launchers  │ [G] Game Launchers     │ [C] Minecraft Clients          │ [I] Misc                       │\n"
            f"├──────────────────────────┼────────────────────────┼────────────────────────────────┼────────────────────────────────┤\n"
            f"│ [1] {offici}             │ [1] {ste}              │ [1] Tecknix                    │ [1] Achivment Watcher          │\n"
            f"│ [2] {prismlaunch}        │ [2] {upl}              │ [2] Salwyrr                    │ [2] {disco}                    │\n"
            f"│ [3] ATLaucnher           │ [3] Origin             │ [3] LabyMod                    │ [3] Spotify                    │\n"
            f"│ [4] {hm}                 │ [4] Epic Games         │ [4] {feath}                    │                                │\n"
            f"│ [5] XMCL                 │ [5] GOG Galaxy         │ [5] {lunarclien}               │                                │\n"
            f"│ [6] GDLauncher           │ [6] Paradox            │ [6] {cheatbreake}              │                                │\n"
            f"│                          │ [7] Roblox             │ [7] Badlion                    ├────────────────────────────────┤")
    print(  f"│                          │                        │ [8] Crystal Client             │ [T] Tools                      │\n"
            f"│                          │                        │                                ├────────────────────────────────┤\n"
            f"│                          │                        │                                │ [1] {openas}                   │\n"
            f"│                          │                        │                                │ [2] Spicefy                    │\n"
            f"│                          │                        │                                │ [3] VenCord                    │\n"
            f"│                          │                        │                                │ [4] BetterDiscord              │\n"
            f"│                          │                        │                                │                                │\n"
            f"│                          │                        │                                │                                │\n"
            f"│                          │                        │                                │ // Sorry for so little tools   │\n"
            f"├──────────────────────────┴────────────────────────┴────────────────────────────────┴────────────────────────────────┤\n"
            f"│                           Ex.: 'D2' ─ HoneCtrl │ N ─ Next Page │ 99 ─ Exit │ H - Help                           3/3 │\n"
            f"└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘")
    interpreter(3)


# Basically a main function
cls()
printer.lprint("Starting...")
# Runs EULA check before prep to prevent issues.
if isfile("EULA.XTB") == False:
    eula()
prep()

# Set vars pre startup
printer.lprint("Running Pre-Startup tasks...")

# Updater
pre = ""
version = "2.5"
if pre == "": pre = "           "
# Sets `pre` to this long space to prevent some sort of bugs
# Can't be a defined function
printer.lprint("Checking updates...")
# Check for internet connection BEFORE trying to update the program.
# This should fix some issues with the updater.

isdev = False

if ping("github.com") == None or False:
    # No internet access, the program will not crash.
    update0 = color("NoNet    ", 2)

# Checks for the `noupdates` file 
if isfile("noupdates.xtb") == True:
    printer.lprint("NoUpdates Detected, not checking for updates.")
    update0 = color("NoUpdates", 3)

# Checks for DEV version  
if isdev == True:
    printer.lprint("DevBuild Detected, not checking for updates.")
    update0 = color("DevBuild ", 3)

else:
    # After all the checks
    newver = latest("xemulat/xtoolbox")
    if version == str(newver):
        update0 = color("UpToDate ", 1)

    elif str(newver) > version:
        # Triggers the update after outdated version is detected
        update0 = color("Outdated ", 2)
        update()

    else:
        update0 = color("DevBuild ", 3)

# Set color vars
printer.lprint("Setting vars...")
xtoolbox00000000000000 = color("XToolBox v"+version+pre, 2)
# ISSUES FIXED, STOP ASKING
# Un-Fucked, don't touch
SetVars.rama()
try:    ramavailz = '00GB / 00GB'
except: ramavailz = "error"

try:    cpu00000000000 = SetVars.cpup()
except: cpu00000000000 = '000 / 100%'

try:    diskusage0000 = SetVars.dusage()
except: diskusage0000 = '00GB / 00GB    '

try:    ping0 = SetVars.ping0() + "   "
except: ping0 = "000ms  "

try:    c = SetVars.c()
except: c = '0000/0000'

xemulated000 = color("xemulated#2622", 2)

# Page 1 Vairables
windowsonreinddddd = color("WindowsOnReins  DNGR", 2)
ohdwindowwwwwwwww = color("OHD Windows    DNGR", 2)
posttweaksjfjfjf = color("PostTweaks    DNGR", 2)
malwarebyt = color("Malwarebytes", 1)
quicktwea = color("QuickTweaks", 1)
sweetyli = color("SweetyLite", 1)
neCtrl = color("HoneCtrl", 1)
firef = color("Firefox", 1)
rav = color("Brave", 1)

# Page 2 Vairables
windowssimpli = color("WindowsSimplify", 2)
unetboot = color("UNetBootin", 2)
aero = color("Aero10", 2)
window11 = color("Windows 11", 1)
minttuxe = color("Linux Mint", 1)
rectify = color("Rectify11", 1)
zorino = color("Zorin OS", 1)
atlaso = color("Atlas OS", 1)
ruf = color("Rufus", 1)

# Page 3 Variables
cheatbreake = color("Cheat Breaker", 2)
offici = color("Official", 2)
upl = color("Uplay", 2)
hm = color("HMCL", 2)
prismlaunch = color("PrismLauncher", 1)
lunarclien = color("Lunar Client", 1)
openas = color("OpenAsar", 1)
disco = color("Discord", 1)
feath = color("Feather", 1)
ste = color("Steam", 1)
# Help Page Vars
e = Back.RED+"Red"+Back.RESET
ng = Back.RED+"DNGR"+Back.RESET
ree = Back.GREEN+"Green"+Back.RESET

# QuickTweaks Page Vars
LimitQ = color("LimitQoS", 2)
optimizess = color("Optimize SSD", 2)
AntiTrackTi = color("AntiTrackTime", 1)

# Run normal UI (Page 1)
printer.lprint("Starting...")

# function call rememberer (purpose is to prevent recursive behaviour) 
try:
    p1(preprint=("Loaded in " + str(str(default_timer() - start).split(".")[0]) + "s"))
    while True:
        #global variable declared in page functions
        lastPage() 
except KeyboardInterrupt:
    print("bai bai")
    sleep(1)
    cls()
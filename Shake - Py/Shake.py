#pip install pywin32
import win32gui
import win32con
import win32api
import random
import time
import ctypes
from ctypes import wintypes


def get_all_windows():
    windows = []
    
    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetParent(hwnd) == 0:
            windows.append(hwnd)
        return True
    
    win32gui.EnumWindows(enum_windows_proc, None)
    return windows

def main():

    windows = get_all_windows()
    

    original_info = []
    for hwnd in windows:
        rect = win32gui.GetWindowRect(hwnd)
        original_info.append({
            'hwnd': hwnd,
            'x': rect[0],
            'y': rect[1],
            'width': rect[2] - rect[0],
            'height': rect[3] - rect[1]
        })
    

    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    try:
        while True:

            start_time = time.time()
            while (time.time() - start_time) < 10:
                for info in original_info:
                    x_offset = random.randint(-15, 15)
                    y_offset = random.randint(-15, 15)
                    
                    win32gui.SetWindowPos(
                        info['hwnd'],
                        win32con.HWND_TOP,
                        info['x'] + x_offset,
                        info['y'] + y_offset,
                        info['width'],
                        info['height'],
                        win32con.SWP_NOZORDER
                    )
                time.sleep(0.03)
            

            for info in original_info:
                win32gui.SetWindowPos(
                    info['hwnd'],
                    win32con.HWND_TOP,
                    info['x'],
                    info['y'],
                    info['width'],
                    info['height'],
                    win32con.SWP_NOZORDER
                )
            

            start_time = time.time()
            

            current_positions = [{'x': 0, 'y': 0} for _ in original_info]
            directions = [{'x': 3, 'y': 2} for _ in original_info]
            
            while (time.time() - start_time) < 10:
                for i, info in enumerate(original_info):
                    current_positions[i]['x'] += directions[i]['x']
                    current_positions[i]['y'] += directions[i]['y']
                    

                    if (current_positions[i]['x'] <= 0 or 
                        current_positions[i]['x'] + info['width'] >= screen_width):
                        directions[i]['x'] = -directions[i]['x']
                    
                    if (current_positions[i]['y'] <= 0 or 
                        current_positions[i]['y'] + info['height'] >= screen_height):
                        directions[i]['y'] = -directions[i]['y']
                    
                    win32gui.SetWindowPos(
                        info['hwnd'],
                        win32con.HWND_TOP,
                        current_positions[i]['x'],
                        current_positions[i]['y'],
                        info['width'],
                        info['height'],
                        win32con.SWP_NOZORDER
                    )
                time.sleep(0.01)
            

            for info in original_info:
                win32gui.SetWindowPos(
                    info['hwnd'],
                    win32con.HWND_TOP,
                    info['x'],
                    info['y'],
                    info['width'],
                    info['height'],
                    win32con.SWP_NOZORDER
                )
                
    except KeyboardInterrupt:

        for info in original_info:
            win32gui.SetWindowPos(
                info['hwnd'],
                win32con.HWND_TOP,
                info['x'],
                info['y'],
                info['width'],
                info['height'],
                win32con.SWP_NOZORDER
            )
        print("End")

if __name__ == "__main__":
    main()
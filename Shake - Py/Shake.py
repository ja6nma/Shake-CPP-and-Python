#pip install pywin32
import win32gui
import win32con
import win32api
import random
import time

def get_all_windows():
    windows = []
    
    def enum_windows_proc(hwnd, lParam):
        if (win32gui.IsWindowVisible(hwnd) and 
            win32gui.GetParent(hwnd) == 0 and
            win32gui.GetWindowText(hwnd) != ''):
            windows.append(hwnd)
        return True
    
    win32gui.EnumWindows(enum_windows_proc, None)
    return windows

def can_move_window(hwnd):
    """Проверяет, можно ли перемещать окно"""
    try:

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        

        if not (style & win32con.WS_CAPTION):
            return False
            

        placement = win32gui.GetWindowPlacement(hwnd)
        if placement[1] == win32con.SW_SHOWMINIMIZED:
            return False
            
        return True
    except:
        return False

def main():
    windows = get_all_windows()
    
    original_info = []
    for hwnd in windows:
        if can_move_window(hwnd):
            try:
                rect = win32gui.GetWindowRect(hwnd)

                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                
                if width > 0 and height > 0 and width < 5000 and height < 5000:
                    original_info.append({
                        'hwnd': hwnd,
                        'x': rect[0],
                        'y': rect[1],
                        'width': width,
                        'height': height
                    })
            except:
                continue
    

    
    try:
        while True:

            start_time = time.time()
            while (time.time() - start_time) < 10:
                for info in original_info:
                    try:
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
                    except Exception as e:

                        continue
                time.sleep(0.03)
            

            for info in original_info:
                try:
                    win32gui.SetWindowPos(
                        info['hwnd'],
                        win32con.HWND_TOP,
                        info['x'],
                        info['y'],
                        info['width'],
                        info['height'],
                        win32con.SWP_NOZORDER
                    )
                except:
                    continue
                
    except KeyboardInterrupt:

        for info in original_info:
            try:
                win32gui.SetWindowPos(
                    info['hwnd'],
                    win32con.HWND_TOP,
                    info['x'],
                    info['y'],
                    info['width'],
                    info['height'],
                    win32con.SWP_NOZORDER
                )
            except:
                continue
        print("End")

if __name__ == "__main__":
    main()
#include <Windows.h>
#include <iostream>
#include <vector>


BOOL CALLBACK EnumWindowsProc(HWND hwnd, LPARAM lParam) {
    std::vector<HWND>* windows = reinterpret_cast<std::vector<HWND>*>(lParam);


    if (IsWindowVisible(hwnd) && GetParent(hwnd) == NULL) {
        windows->push_back(hwnd);
    }

    return TRUE;
}

int main() {

    std::vector<HWND> windows;
    EnumWindows(EnumWindowsProc, reinterpret_cast<LPARAM>(&windows));


    std::vector<POINT> originalPositions;
    std::vector<SIZE> originalSizes;

    for (HWND hwnd : windows) {
        RECT rect;
        GetWindowRect(hwnd, &rect);
        originalPositions.push_back({ rect.left, rect.top });
        originalSizes.push_back({ rect.right - rect.left, rect.bottom - rect.top });
    }

    int screenW = GetSystemMetrics(SM_CXSCREEN);
    int screenH = GetSystemMetrics(SM_CYSCREEN);

    while (true) {

        ULONGLONG startTime = GetTickCount64();
        while (GetTickCount64() - startTime < 10000) {
            for (size_t i = 0; i < windows.size(); i++) {
                int x = (rand() % 31) - 15;
                int y = (rand() % 31) - 15;
                SetWindowPos(windows[i], 0,
                    originalPositions[i].x + x,
                    originalPositions[i].y + y,
                    originalSizes[i].cx,
                    originalSizes[i].cy,
                    SWP_NOZORDER);
            }
            Sleep(30);
        }


        for (size_t i = 0; i < windows.size(); i++) {
            SetWindowPos(windows[i], 0,
                originalPositions[i].x,
                originalPositions[i].y,
                originalSizes[i].cx,
                originalSizes[i].cy,
                SWP_NOZORDER);
        }


        startTime = GetTickCount64();
        std::vector<POINT> currentPositions(windows.size(), POINT{ 0, 0 });
        std::vector<POINT> directions(windows.size(), POINT{ 3, 2 });

        while (GetTickCount64() - startTime < 10000) {
            for (size_t i = 0; i < windows.size(); i++) {
                currentPositions[i].x += directions[i].x;
                currentPositions[i].y += directions[i].y;

                if (currentPositions[i].x <= 0 || currentPositions[i].x + originalSizes[i].cx >= screenW)
                    directions[i].x = -directions[i].x;
                if (currentPositions[i].y <= 0 || currentPositions[i].y + originalSizes[i].cy >= screenH)
                    directions[i].y = -directions[i].y;

                SetWindowPos(windows[i], 0,
                    currentPositions[i].x,
                    currentPositions[i].y,
                    originalSizes[i].cx,
                    originalSizes[i].cy,
                    SWP_NOZORDER);
            }
            Sleep(10);
        }


        for (size_t i = 0; i < windows.size(); i++) {
            SetWindowPos(windows[i], 0,
                originalPositions[i].x,
                originalPositions[i].y,
                originalSizes[i].cx,
                originalSizes[i].cy,
                SWP_NOZORDER);
        }
    }

    return 0;
}
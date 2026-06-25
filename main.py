from ui.ctk_ui import main
import sys
import ctypes

mutex = ctypes.windll.kernel32.CreateMutexW(
    None,
    False,
    "PomoPlanner_SingleInstance"
)

ERROR_ALREADY_EXISTS = 183

if ctypes.windll.kernel32.GetLastError() == ERROR_ALREADY_EXISTS: #이미 열려있으면 종료
    sys.exit()

if __name__ == "__main__": #직접 실행할때만 실행
    main()

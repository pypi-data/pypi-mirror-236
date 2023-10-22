# some adb scripts

## Tested against Windows / Python 3.11 / Anaconda

## pip install adbscripts

```python
from adbscripts import AdbCapture
path_adb = r"C:\Android\android-sdk\platform-tools\adb.exe"
device_serial = "127.0.0.1:5555"
adbscripts = AdbCapture(
    adb_path=path_adb,
    device_serial=device_serial,
    capture_buffer=100000,
    use_busybox=False,
)
adbscripts.connect_to_device()
df1, stderr = adbscripts.get_one_csv_uiautomator(
    defaultvalue="null",convert_to_pandas=True
)


df, stderr = adbscripts.get_one_csv_activities(
    defaultvalue="null",
    with_hashcode=1,convert_to_pandas=True
)



from time import sleep
import pandas as pd
import io
from adbscripts import AdbCapture

path_adb = r"C:\Android\android-sdk\platform-tools\adb.exe"
device_serial = "127.0.0.1:5555"

self = AdbCapture(
    adb_path=path_adb,
    device_serial=device_serial,
    capture_buffer_for_ui_activities=100000,
    use_busybox=False,
)
stdout, stderr = self.connect_to_device()
exa = False
lscommand = self.execute_shell_script(
    "ls | cat",
    su=False,
    add_exit=True,
    print_stderr=True,
    print_stdout=True,
    clear_temp_lines_for_csv=False,
)
lscommand.is_alive()
print(lscommand.captured_stdout)

lscommand2 = self.execute_shell_script(
    """
while true; do    
    ls | cat
done    
    """,
    su=False,
    add_exit=True,
    print_stderr=True,
    print_stdout=True,
    clear_temp_lines_for_csv=False,
)

sleep(4)
print(lscommand2.is_alive())
lscommand2.stop_capturing = True
sleep(0.5)
print(lscommand2.is_alive())

activitieselements = self.start_capture_activities(
    print_csv=1,
    defaultvalue="null",
    sleeptime=1,
    addtoscript="",
    print_stdout=False,
    print_stderr=True,
    add_exit=False,
    stripline=0,
    with_class=0,
    with_mid=0,
    with_hashcode=0,
    with_elementid=0,
    with_visibility=0,
    with_focusable=0,
    with_enabled=0,
    with_drawn=0,
    with_scrollbars_horizontal=0,
    with_scrollbars_vertical=0,
    with_clickable=0,
    with_long_clickable=0,
    with_context_clickable=0,
    with_pflag_is_root_namespace=0,
    with_pflag_focused=0,
    with_pflag_selected=0,
    with_pflag_prepressed=0,
    with_pflag_hovered=0,
    with_pflag_activated=0,
    with_pflag_invalidated=0,
    with_pflag_dirty_mask=0,
)
sleep(5)
print(activitieselements.stdout_for_ui_and_activities)
activitieselements.stop_capturing = True
df = pd.read_csv(io.StringIO(activitieselements.stdout_for_ui_and_activities[-1]))
print(df)
uia = self.start_capture_uiautomator(
    print_csv=1,
    defaultvalue="null",
    sleeptime=1,
    addtoscript="",
    print_stdout=True,
    print_stderr=True,
    add_exit=False,
)
sleep(5)
uia.stop_capturing = True
# df2=(pd.read_csv(io.StringIO(uia.stdout_for_ui_and_activities[-1])))
# print(df2)

capturedpixel = self.start_capture_get_color_at_pixel(
    x=500,
    y=509,
    print_stderr=True,
    print_stdout=True,
)
sleep(5)
capturedpixel.stop_capturing = True
print(capturedpixel.captured_stdout)

onlyonetime = self.get_color_at_pixel(
    x=100,
    y=200,
    print_stderr=True,
    print_stdout=True,
)
print(onlyonetime)

activneu = self.start_capture_activities()
sleep(20)
activneu.stop_capturing = True
print(activneu.stdout_for_ui_and_activities)
pd.read_csv(io.StringIO(activneu.stdout_for_ui_and_activities[1]))


webscraping = self.start_chrome_webscraping(
    id_positive_button="app:id/positive_button",
    id_save_offline_button="app:id/save_offline_button",
    id_refresh_button="",
    # id_refresh_button="app:id/refresh_button",
    sleep_after_positive_button=1,
    sleep_after_save_offline_button=1,
    sleep_after_refresh_button=1,
    print_stderr=True,
    print_stdout=False,
)

counter = 0
from lxml2pandas import subprocess_parsing
from threading import Lock

lock = Lock()
parsedata = []
tmpfiles = []
co = 0

bubu = False
while True:
    try:
        sleep(5)
        if webscraping.captured_stdout:
            try:
                lock.acquire()

                parsedata = [webscraping.captured_stdout[-1]]
                webscraping.captured_stdout.clear()
            finally:
                lock.release()
        if parsedata:
            df = subprocess_parsing(
                parsedata,
                chunks=1,
                processes=4,
                print_stdout=True,
                print_stderr=True,
                print_function_exceptions=True,
                children_and_parents=True,
                allowed_tags=(),
                forbidden_tags=("html", "body"),
                filter_function=lambda x: "t" in str(x.aa_attr_values).lower(),
            )
            print(df)
            parsedata.clear()

    except Exception as fe:
        print(fe)
        continue

webscraping.stop_capturing = True

```
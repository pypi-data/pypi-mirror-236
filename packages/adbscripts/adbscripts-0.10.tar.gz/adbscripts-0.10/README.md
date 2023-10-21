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




```
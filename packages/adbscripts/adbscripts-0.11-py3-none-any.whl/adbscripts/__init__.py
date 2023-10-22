import base64
import functools
import importlib
import os
import platform
import subprocess
import sys
from collections import deque

from adbscripts.chromewebscraping import bashscript_chrome_download
from adbscripts.coloratpixeloncerep import coloratpixelrep
from adbscripts.getcoloratpixel import getpixelcolor

from .getuiautomator import uiautomatorscript, uiautomatorscriptbasis

from .getactivityelements import activityelements, activityelementsbasic
#from kthread_sleep import sleep
from time import time,sleep
import kthread
import psutil

iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
    from ctypes import wintypes
    import ctypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    kernel32 = windll.kernel32

    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.LPWSTR,
        wintypes.DWORD,
    ]
    _GetShortPathNameW.restype = wintypes.DWORD

else:
    invisibledict = {}

try:
    pd = importlib.__import__("pandas")
except Exception:
    pass


@functools.cache
def get_short_path_name(long_name):
    if not iswindows:
        return long_name
    try:
        if not os.path.exists(long_name):
            return long_name

        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        pa = output_buf.value
        return pa if os.path.exists(pa) else long_name
    except Exception:
        return long_name


def _format_command(
    adbpath,
    serial_number,
    cmd,
    su=False,
    use_busybox=False,
    errors="strict",
    use_short_adb_path=True,
    add_exit=True,
):
    wholecommand = [get_short_path_name(adbpath) if use_short_adb_path else adbpath]
    nolimitcommand = []
    base64_command = base64.standard_b64encode(cmd.encode("utf-8", errors)).decode(
        "utf-8", errors
    )
    base64_command = "'" + base64_command + "'"
    if serial_number:
        wholecommand.extend(["-s", serial_number])
    wholecommand.extend(["shell"])
    if su:
        wholecommand.extend(["su", "--"])

    nolimitcommand.extend(["echo", base64_command, "|"])
    if use_busybox:
        nolimitcommand.extend(["busybox"])
    nolimitcommand.extend(["base64", "-d", "|", "sh"])

    exit_u = "\nexit\n"
    exit_b = b"\nexit\n"
    if not add_exit:
        exit_u = ""
        exit_b = b""

    nolimitcommand_no_bytes = " ".join(nolimitcommand) + exit_u
    nolimitcommand_bytes = " ".join(nolimitcommand).encode("utf-8", errors) + exit_b
    return nolimitcommand_no_bytes, nolimitcommand_bytes, wholecommand, cmd


def killproc(pid):
    return subprocess.Popen(f"taskkill /F /PID {pid} /T", **invisibledict)


def kill_subproc(p, t=()):
    try:
        p.stdin.close()
    except Exception:
        pass
    try:
        p.stdout.close()
    except Exception:
        pass
    try:
        p.stderr.close()
    except Exception:
        pass
    try:
        _ = killproc(p.pid)
    except Exception:
        pass
    if t:
        for tt in t:
            try:
                tt.kill()
            except Exception:
                pass


columncheck = [
    "INDEX,TEXT,RESOURCE_ID,CLASS,PACKAGE,CONTENT_DESC,CHECKABLE,CHECKED,CLICKABLE,ENABLED,FOCUSABLE,FOCUSED,SCROLLABLE,LONG_CLICKABLE,PASSWORD,SELECTED,BOUNDS,STARTX,ENDX,STARTY,ENDY,CENTER_X,CENTER_Y,AREA,WIDTH,HEIGHT",
    "IS_ACTIVE,ELEMENT_INDEX,START_X,START_Y,CENTER_X,CENTER_Y,AREA,END_X,END_Y,WIDTH,HEIGHT,START_X_RELATIVE,START_Y_RELATIVE,END_X_RELATIVE,END_Y_RELATIVE,PARENTSINDEX,ELEMENT_ID,MID,HASHCODE,VISIBILITY,FOCUSABLE,ENABLED,DRAWN,SCROLLBARS_HORIZONTAL,SCROLLBARS_VERTICAL,CLICKABLE,LONG_CLICKABLE,CONTEXT_CLICKABLE,CLASSNAME,PFLAG_IS_ROOT_NAMESPACE,PFLAG_FOCUSED,PFLAG_SELECTED,PFLAG_PREPRESSED,PFLAG_HOVERED,PFLAG_ACTIVATED,PFLAG_INVALIDATED,PFLAG_DIRTY_MASK,LINE_STRIPPED",
]


def get_script_activities(
    print_csv=1,
    defaultvalue="null",
    sleeptime=1.0,
    addtoscript="",
    stripline=1,
    with_class=1,
    with_mid=1,
    with_hashcode=1,
    with_elementid=1,
    with_visibility=1,
    with_focusable=1,
    with_enabled=1,
    with_drawn=1,
    with_scrollbars_horizontal=1,
    with_scrollbars_vertical=1,
    with_clickable=1,
    with_long_clickable=1,
    with_context_clickable=1,
    with_pflag_is_root_namespace=1,
    with_pflag_focused=1,
    with_pflag_selected=1,
    with_pflag_prepressed=1,
    with_pflag_hovered=1,
    with_pflag_activated=1,
    with_pflag_invalidated=1,
    with_pflag_dirty_mask=1,
):
    if addtoscript:
        addtoscript = "\n".join(
            [x.replace("\t", "    ") for x in addtoscript.splitlines()]
        )
    else:
        addtoscript = activityelementsbasic
    return (
        activityelements.replace("ADD_TO_SCRIPT_REPLACE", str(addtoscript))
        .replace("WITH_CLASS_REPLACE", str(with_class))
        .replace("WITH_MID_REPLACE", str(with_mid))
        .replace("WITH_HASHCODE_REPLACE", str(with_hashcode))
        .replace("WITH_ELEMENTID_REPLACE", str(with_elementid))
        .replace("WITH_VISIBILITY_REPLACE", str(with_visibility))
        .replace("WITH_FOCUSABLE_REPLACE", str(with_focusable))
        .replace("WITH_ENABLED_REPLACE", str(with_enabled))
        .replace("WITH_DRAWN_REPLACE", str(with_drawn))
        .replace("WITH_SCROLLBARS_HORIZONTAL_REPLACE", str(with_scrollbars_horizontal))
        .replace("WITH_SCROLLBARS_VERTICAL_REPLACE", str(with_scrollbars_vertical))
        .replace("WITH_CLICKABLE_REPLACE", str(with_clickable))
        .replace("WITH_LONG_CLICKABLE_REPLACE", str(with_long_clickable))
        .replace("WITH_CONTEXT_CLICKABLE_REPLACE", str(with_context_clickable))
        .replace(
            "WITH_PFLAG_IS_ROOT_NAMESPACE_REPLACE", str(with_pflag_is_root_namespace)
        )
        .replace("WITH_PFLAG_FOCUSED_REPLACE", str(with_pflag_focused))
        .replace("WITH_PFLAG_SELECTED_REPLACE", str(with_pflag_selected))
        .replace("WITH_PFLAG_PREPRESSED_REPLACE", str(with_pflag_prepressed))
        .replace("WITH_PFLAG_HOVERED_REPLACE", str(with_pflag_hovered))
        .replace("WITH_PFLAG_ACTIVATED_REPLACE", str(with_pflag_activated))
        .replace("WITH_PFLAG_INVALIDATED_REPLACE", str(with_pflag_invalidated))
        .replace("WITH_PFLAG_DIRTY_MASK_REPLACE", str(with_pflag_dirty_mask))
        .replace("STRIPLINE_REPLACE", str(stripline))
        .replace("PRINT_CSV_REPLACE", str(int(print_csv)))
        .replace("DEFAULTVALUE_REPLACE", str(defaultvalue))
        .replace("SLEEPTIME_REPLACE", str(sleeptime))
    )


def get_script_uiautomator(
    print_csv=1,
    defaultvalue="null",
    sleeptime=1,
    addtoscript="",
):
    if addtoscript:
        addtoscript = "\n".join(
            [x.replace("\t", "    ") for x in addtoscript.splitlines()]
        )
    else:
        addtoscript = uiautomatorscriptbasis
    return (
        uiautomatorscript.replace("ADD_TO_SCRIPT_REPLACE", str(addtoscript))
        .replace("PRINT_CSV_REPLACE", str(int(print_csv)))
        .replace("DEFAULTVALUE_REPLACE", str(defaultvalue))
        .replace("SLEEPTIME_REPLACE", str(sleeptime))
    )


class AdbCapture:
    def __init__(
        self,
        adb_path,
        device_serial,
        capture_buffer_for_ui_activities=100,
        use_busybox=False,
        decode_bytes=True,
    ):
        self.adb_path_short = get_short_path_name(adb_path)
        self.adb_path = adb_path
        self.device_serial = device_serial
        self.use_busybox = use_busybox
        self.capture_buffer = capture_buffer_for_ui_activities
        self.stdout_for_ui_and_activities = deque([], capture_buffer_for_ui_activities)
        self.captured_stderr = deque([], capture_buffer_for_ui_activities)
        self.captured_stdout = []

        self.stop_capturing = False
        self.subproc = None
        self.stdout_thread_capture_thread = None
        self.stderr_thread_capture_thread = None
        self._base64_command_utf_8 = None
        self._base64_command_bytes = None
        self._subprocess_commandline = None
        self._shell_command = None
        self._alive_check_thread = None
        self.decode_bytes = decode_bytes

    def __str__(self):
        return f"{self.adb_path_short} {self.device_serial}"

    def __repr__(self):
        return self.__str__()

    def get_color_at_pixel(
        self,
        x,
        y,
        print_stderr=False,
        print_stdout=False,
    ):
        q = self.start_capture_get_color_at_pixel(
            x,
            y,
            print_stderr=print_stderr,
            print_stdout=print_stdout,
        )
        while True:
            try:
                x, y, r, g, b = q.captured_stdout[-1].strip().split(",")
                x, y, r, g, b = tuple(map(int, (x, y, r, g, b)))
                q.stop_capturing = True
                self.stop_capturing = True
                break
            except Exception as fe:
                sleep(0.1)
                if print_stderr:
                    sys.stderr.write(f"{fe}\n\n")
                    sys.stderr.flush()
        return x, y, r, g, b

    def clear_stdout_stderr_buffer(self):
        self.captured_stdout.clear()
        self.captured_stderr.clear()
        self.stdout_for_ui_and_activities.clear()

    def start_capture_get_color_at_pixel(
        self,
        x,
        y,
        print_stderr=True,
        print_stdout=True,
    ):
        getv = coloratpixelrep % (
            x,
            y,
        )
        scriptpixelcolor = getpixelcolor + "\n" + getv
        return self.execute_shell_script(
            scriptpixelcolor,
            su=False,
            add_exit=False,
            print_stderr=print_stderr,
            print_stdout=print_stdout,
            clear_temp_lines_for_csv=False,
        )

    def start_capture_uiautomator(
        self,
        print_csv=1,
        defaultvalue="null",
        sleeptime=1,
        addtoscript="",
        print_stdout=True,
        print_stderr=True,
        add_exit=False,
    ):
        scri = get_script_uiautomator(
            print_csv=print_csv,
            defaultvalue=defaultvalue,
            sleeptime=sleeptime,
            addtoscript=addtoscript,
        )
        return self.execute_shell_script(
            script=scri,
            su=False,
            add_exit=add_exit,
            print_stderr=print_stderr,
            print_stdout=print_stdout,
            clear_temp_lines_for_csv=True,
        )

    def start_capture_activities(
        self,
        print_csv=1,
        defaultvalue="null",
        sleeptime=1,
        addtoscript="",
        print_stdout=True,
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
        **kwargs,
    ):
        scri = get_script_activities(
            print_csv=print_csv,
            defaultvalue=defaultvalue,
            sleeptime=sleeptime,
            addtoscript=addtoscript,
            stripline=int(stripline),
            with_class=int(with_class),
            with_mid=int(with_mid),
            with_hashcode=int(with_hashcode),
            with_elementid=int(with_elementid),
            with_visibility=int(with_visibility),
            with_focusable=int(with_focusable),
            with_enabled=int(with_enabled),
            with_drawn=int(with_drawn),
            with_scrollbars_horizontal=int(with_scrollbars_horizontal),
            with_scrollbars_vertical=int(with_scrollbars_vertical),
            with_clickable=int(with_clickable),
            with_long_clickable=int(with_long_clickable),
            with_context_clickable=int(with_context_clickable),
            with_pflag_is_root_namespace=int(with_pflag_is_root_namespace),
            with_pflag_focused=int(with_pflag_focused),
            with_pflag_selected=int(with_pflag_selected),
            with_pflag_prepressed=int(with_pflag_prepressed),
            with_pflag_hovered=int(with_pflag_hovered),
            with_pflag_activated=int(with_pflag_activated),
            with_pflag_invalidated=int(with_pflag_invalidated),
            with_pflag_dirty_mask=int(with_pflag_dirty_mask),
        )
        return self.execute_shell_script(
            script=scri,
            su=False,
            add_exit=add_exit,
            print_stderr=print_stderr,
            print_stdout=print_stdout,
            clear_temp_lines_for_csv=True,
        )

    def open_adb_shell(self):
        subprocess.run(
            f'start cmd /k "{self.adb_path_short}" -s {self.device_serial} shell',
            shell=True,
        )

    def execute_shell_script(
        self,
        script,
        su=False,
        add_exit=True,
        print_stderr=True,
        print_stdout=True,
        clear_temp_lines_for_csv=False,
        decode_bytes=True,
        function_to_apply_line=lambda x: x,
        function_to_apply_joined=lambda x: x.rstrip(),
    ):
        c = self.__class__(
            adb_path=self.adb_path_short,
            device_serial=self.device_serial,
            capture_buffer_for_ui_activities=self.capture_buffer,
            use_busybox=self.use_busybox,
            decode_bytes=decode_bytes,
        )
        c._execute_shell_script(
            script,
            su=su,
            add_exit=add_exit,
            print_stderr=print_stderr,
            print_stdout=print_stdout,
            clear_temp_lines_for_csv=clear_temp_lines_for_csv,
            function_to_apply_line=function_to_apply_line,
            function_to_apply_joined=function_to_apply_joined,
        )
        return c

    def kill_csv_capture(self):
        self.stop_capturing = True
        try:
            if iswindows:
                subprocess.Popen(
                    f"taskkill /F /PID {self.subproc.pid} /T", **invisibledict
                )
            # sleep(.1)
        except Exception:
            pass
        kill_subproc(
            self.subproc,
            (self.stdout_thread_capture_thread, self.stderr_thread_capture_thread),
        )
        return self

    def _alive_check(self):
        sleep(3)
        while True:
            try:
                alive = psutil.pid_exists(self.subproc.pid)
                if not alive:
                    self.stop_capturing = True
                    break
                else:
                    sleep(1)
            except Exception:
                sleep(1)
                pass

    def _execute_shell_script(
        self,
        script,
        su=False,
        add_exit=True,
        print_stderr=True,
        print_stdout=True,
        clear_temp_lines_for_csv=False,
        function_to_apply_line=lambda x: x.rstrip(),
        function_to_apply_joined=lambda x: x,
    ):
        self.stop_capturing = False

        def read_stderr_thread():
            while not self.stop_capturing:
                try:
                    for q in iter(self.subproc.stderr.readline, b""):
                        if self.stop_capturing:
                            break
                        deco = q.decode("utf-8", "backslashreplace").strip()
                        self.captured_stderr.append(deco)
                        if print_stderr:
                            sys.stderr.write(f"{deco}\n")
                except Exception:
                    if self.stop_capturing:
                        break
                    #sleep(0.1)
                    pass
            else:
                self.kill_csv_capture()

        def read_stdout_thread():
            while not self.stop_capturing:
                try:
                    for q in iter(self.subproc.stdout.readline, b""):
                        if self.stop_capturing:
                            break
                        deco = q.decode("utf-8", "backslashreplace").strip()
                        if not deco:
                            continue
                        if deco not in columncheck:
                            if not deco.startswith("ERROR"):
                                if self.decode_bytes:
                                    line2append = function_to_apply_line(deco)
                                else:
                                    line2append = function_to_apply_line(q)
                                self.captured_stdout.append(line2append)

                                if print_stdout:
                                    print(f"{deco}")

                        else:
                            if clear_temp_lines_for_csv:
                                if self.decode_bytes:
                                    joining = "\n".join(self.captured_stdout)
                                else:
                                    joining = b"\n".join(self.captured_stdout)
                                joining = function_to_apply_joined(joining.strip())
                                if joining:
                                    self.stdout_for_ui_and_activities.append(joining)
                                    self.captured_stdout.clear()
                                else:
                                    if self.decode_bytes:
                                        self.captured_stdout.append(deco)

                                    else:
                                        self.captured_stdout.append(q.rstrip())

                except Exception:
                    if self.stop_capturing:
                        break
                    #sleep(0.1)
            else:
                self.kill_csv_capture()

        if "#!/bin/bash" not in script:
            script = "#!/bin/bash\n" + script
        (
            self._base64_command_utf_8,
            self._base64_command_bytes,
            self._subprocess_commandline,
            self._shell_command,
        ) = _format_command(
            adbpath=self.adb_path_short,
            serial_number=self.device_serial,
            cmd=script,
            su=su,
            use_busybox=self.use_busybox,
            errors="strict",
            use_short_adb_path=True,
            add_exit=add_exit,
        )

        self.subproc = subprocess.Popen(
            self._subprocess_commandline,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **invisibledict,
        )

        self.subproc.stdin.write(self._base64_command_bytes)
        self.subproc.stdin.close()
        self.stdout_thread_capture_thread = kthread.KThread(
            target=read_stdout_thread, name=f"read_stdout_thread{time()}"
        )
        self.stderr_thread_capture_thread = kthread.KThread(
            target=read_stderr_thread, name=f"read_stderr_thread{time()}"
        )
        self.stdout_thread_capture_thread.start()
        self.stderr_thread_capture_thread.start()
        self._alive_check_thread = kthread.KThread(
            target=self._alive_check, name=f"_alive_check{time()}"
        )
        self._alive_check_thread.start()

    def is_alive(self):
        a = False
        b = False
        try:
            a = self.stdout_thread_capture_thread.is_alive()
        except Exception:
            pass
        try:
            b = self.stderr_thread_capture_thread.is_alive()
        except Exception:
            pass
        return any([a, b])

    def connect_to_device(
        self,
        **kwargs,
    ):
        p = subprocess.run(
            f"{self.adb_path_short} connect {self.device_serial}",
            capture_output=True,
            **kwargs,
            **invisibledict,
        )
        stdout = p.stdout.splitlines()
        stderr = p.stderr.splitlines()
        return stdout, stderr

    def start_chrome_webscraping(
        self,
        id_positive_button="app:id/positive_button",
        id_save_offline_button="app:id/save_offline_button",
        id_refresh_button="app:id/refresh_button",
        sleep_after_positive_button=1,
        sleep_after_save_offline_button=1,
        sleep_after_refresh_button=1,
        print_stderr=True,
        print_stdout=False,
    ):
        sleep_after_positive_button = str(sleep_after_positive_button)
        sleep_after_save_offline_button = str(sleep_after_save_offline_button)
        sleep_after_refresh_button = str(sleep_after_refresh_button)
        id_positive_button = '"' + id_positive_button.strip("'\" ") + '"'
        id_save_offline_button = '"' + id_save_offline_button.strip("'\" ") + '"'
        id_refresh_button = '"' + id_refresh_button.strip("'\" ") + '"'
        bashscript_chrome_download_execute = (
            bashscript_chrome_download.replace(
                "ID_OF_POSITIVE_BUTTON", id_positive_button
            )
            .replace("ID_OF_SAVE_OFFLINE_BUTTON", id_save_offline_button)
            .replace("ID_OF_REFRESH_BUTTON", id_refresh_button)
            .replace("SLEEP_AFTER_POSITIVE_BUTTON", sleep_after_positive_button)
            .replace("SLEEP_AFTER_SAVE_BUTTON", sleep_after_save_offline_button)
            .replace("SLEEP_AFTER_REFRESH_BUTTON", sleep_after_refresh_button)
        )

        return self.execute_shell_script(
            bashscript_chrome_download_execute,
            su=False,
            add_exit=False,
            print_stdout=print_stdout,
            print_stderr=print_stderr,
            clear_temp_lines_for_csv=True,
            decode_bytes=False,
            function_to_apply_line=lambda x: x.replace(b"QQQQQAAAAA", b"\n"),
            function_to_apply_joined=lambda x: x.rstrip().replace(b"QQQQQAAAAA", b"\n"),
        )

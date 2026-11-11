import platform


def get_system_info() -> dict[str, str]:
    system = platform.system()
    os_name = system

    if system == "Linux":
        try:
            info = platform.freedesktop_os_release()
            os_name = info.get("PRETTY_NAME", "Linux")
        except OSError:
            pass

    elif system == "Darwin":
        os_name = f"macOS {platform.mac_ver()[0]}"

    return {
        "os": os_name,
        "arch": platform.machine(),
    }

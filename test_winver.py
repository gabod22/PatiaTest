
def get_registry_value(key, subkey, value):
    import winreg
    key = getattr(winreg, key)
    handle = winreg.OpenKey(key, subkey)
    (value, type) = winreg.QueryValueEx(handle, value)
    return value


def os_version():
    def get(key):
        return get_registry_value(
            "HKEY_LOCAL_MACHINE",
            "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            key)
    os = get("ProductName")
    # sp = get("CSDVersion")
    build = get("DisplayVersion")
    return "%s (build %s)" % (os, build)


print(os_version())

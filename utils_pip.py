import bpy
import subprocess

PYPATH = bpy.app.binary_path_python

class Pip:
    @staticmethod
    def _ensure_user_site_package():
        import site, os, sys
        site_package = site.getusersitepackages()
        if not os.path.exists(site_package):
            site_package = bpy.utils.user_resource('SCRIPTS', "site_package", create=True)
        if site_package not in sys.path:
            sys.path.append(site_package)

    def install(self, module):
        self._ensure_user_site_package()
        cmd = [PYPATH, "-m", "pip", "install", "--user", module]
        return subprocess.run(cmd, capture_output=True, text=True)

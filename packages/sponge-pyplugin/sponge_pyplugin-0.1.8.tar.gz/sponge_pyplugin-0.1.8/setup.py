import sys
import os
import pathlib
import re
from setuptools import setup, Extension
try:
    from setuptools import SetuptoolsDeprecationWarning
except:
    SetuptoolsDeprecationWarning = DeprecationWarning
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from setuptools.command.egg_info import egg_info
from wheel.bdist_wheel import bdist_wheel

import warnings
warnings.filterwarnings("ignore",category=SetuptoolsDeprecationWarning)

class MyInstall(install):
    user_options = install.user_options + bdist_wheel.user_options
    def run(self):
        self.run_command('build_ext')

class MyBuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        build_temp = f"{pathlib.Path(self.build_temp)}/{ext.name}"
        os.makedirs(build_temp, exist_ok=True)
        for i, argv in enumerate(sys.argv):
            if argv == "--root":
                out_dir = pathlib.Path(sys.argv[i+1])
                break
        else:
            raise ValueError("root should be provided. Use '--root absolute_path' to set the root path")
        if not out_dir.is_absolute():
            raise ValueError("root should be an absolute path")

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(out_dir),
            "-DCMAKE_BUILD_TYPE=Release"
        ]
        build_args = ["--config", "Release"]

        os.chdir(build_temp)
        if os.name == "nt":
            s = os.popen("cmake --help")
            for line in s:
                if line.strip().startswith("*") and "Visual Studio" in line:
                    t = line.split()[1:5]
                    if int(line.split()[3]) <= 15:
                        t.append("Win64")
                        t = " ".join(t)
                        cmake_args.extend(["-G", t])
                    else:
                        t = " ".join(t)
                        cmake_args.extend(["-G", t])
                    break
        self.spawn(["cmake", f"{str(cwd)}/{ext.name}"] + cmake_args)
        if os.name == "nt":
            with open(f"{ext.name}.vcxproj", encoding="utf-8-sig") as f:
                contents = f.read()
            with open(f"{ext.name}.vcxproj", "w", encoding="utf-8-sig") as f:
                f.write(re.sub("(<CudaCompile>(?:.(?!<CudaCompile>))+<AdditionalOptions>)([^<]*)(</AdditionalOptions>(?:.(?!<CudaCompile>))+</CudaCompile>)", lambda x: x.group(1) + x.group(3), contents, flags=re.M | re.S))
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(str(cwd))

class MyEggInfo(egg_info):
    def run(self):
        super().run()
        self.filelist.include("sponge_pyplugin/*")
        self.filelist.include("sponge_pyplugin/MD_core/*")
        self.filelist.include("sponge_pyplugin/crd_molecular_map/*")
        self.filelist.include("sponge_pyplugin/collective_variable/*")

setup(name="sponge_pyplugin",
      version="0.1.8",
      description="This is the python plugin of SPONGE",
      ext_modules=[Extension("sponge_pyplugin", [])],
      install_requires = ["cmake>=3.18"],
      cmdclass={"install": MyInstall, "bdist_wheel": MyInstall, "build_ext":MyBuildExt, "egg_info": MyEggInfo},
      data_files=[("cpp", "*.cpp")],
      long_description=open('README.md', encoding="utf-8").read(),
      long_description_content_type ="text/markdown"
      )
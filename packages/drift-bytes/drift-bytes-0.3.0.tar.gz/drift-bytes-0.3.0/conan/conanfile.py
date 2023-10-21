import os

from conans import ConanFile
from conans.tools import Git

from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout

required_conan_version = ">=1.58"


class WaveletBufferConan(ConanFile):
    name = "drift_bytes"
    version = "0.3.0"
    license = "MPL-2.0"
    author = "PANDA GmbH"
    description = "A serializer for typed data in the Drift infrastructure"
    url = "https://github.com/panda-official/DriftBytes"
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    requires = ("cereal/1.3.2",)

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}

    generators = "CMakeDeps"

    def set_version(self):
        suffix = os.getenv("VERSION_SUFFIX")
        if suffix:
            self.version += f"-b.{suffix}"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        local_source = os.getenv("CONAN_SOURCE_DIR")
        if local_source is not None:
            print(f"Use local sources: {local_source}")
            self.run(
                "cp -r {}/. {}/".format(
                    os.getenv("CONAN_SOURCE_DIR"), self.source_folder
                )
            )
        else:
            branch = f"v{self.version}" if self.channel == "stable" else self.channel
            print(f"Use remote sources, branch: {branch}")
            git = Git()
            git.clone(
                "https://github.com/panda-official/DriftBytes.git",
                branch=branch,
                shallow=True,
            )

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CONAN_EXPORTED"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        self.copy("*.h", dst="include", src="drift_bytes")

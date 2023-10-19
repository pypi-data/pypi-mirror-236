#
# Copyright (C) Alibaba Cloud Ltd. 2021-2024.  ALL RIGHTS RESERVED.
#
import sys
import os
import shutil
import time
import platform

#import torch
#from torch.utils import cpp_extension
#from Cython.Build import cythonize
from setuptools import setup, Extension, find_packages
from wheel.bdist_wheel import bdist_wheel
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install 
#from distutils.core import setup
#from distutils.command.install import install


deep_nccl_version = "1.0.5"
package_name = "deepnccl"
total_packages = [
    "deepnccl"
]

def new_pip_version():
    import pip
    pip_version = pip.__version__
    pip_major_version = pip_version.split(".")[0]
    pip_minor_version = pip_version.split(".")[1]
    if int(pip_major_version) >= 23 and int(pip_minor_version) >= 1:
        return True
    else:
        return False

class post_install(install):
    def run(self):
        # print('install ...')
        install.run(self)
        path = os.__file__
        from distutils.sysconfig import get_python_lib
        #>>> get_python_lib()
        #'/root/miniconda3/lib/python3.9/site-packages'
        path = get_python_lib() + '/deepnccl/'
        if os.path.exists('/etc/ld.so.conf.d/aiacc_nccl.conf'):
            os.system(f'echo {path} >> "/etc/ld.so.conf.d/aiacc_nccl.conf"')
        else:
            os.system(f'echo {path} > "/etc/ld.so.conf.d/aiacc_nccl.conf"')
        # get index path
        if new_pip_version():
            try:
                import deep_index as package
            except:
                import pip as package
        else:
            import deep_index as package

        real_path = os.path.abspath(os.path.dirname(os.path.dirname(package.__file__)))
        os.system(f'echo {real_path}/deepnccl/ >> "/etc/ld.so.conf.d/aiacc_nccl.conf"')
        os.system(f'ldconfig')

        # for deepncclplugin
        os.system(f'ln -s {real_path}/deepncclplugin/libnccl-net.so.0.0.0 {real_path}/deepncclplugin/libnccl-net.so')
        os.system(f'ldconfig')
        # print('echo aiacc_nccl install done!')
        # os.system('echo aiacc_nccl > "/tmp/debug"')

setup(
    name=package_name,
    version=f"{deep_nccl_version}",
    description=("AIACC-NCCL is an AI-Accelerator communication framework for NVIDIA-NCCL. "\
                 "It implements optimized all-reduce, all-gather, reduce, broadcast, reduce-scatter, all-to-all," \
                 "as well as any send/receive based communication pattern." \
                 "It has been optimized to achieve high bandwidth on aliyun machines using PCIe, NVLink, NVswitch," \
                 "as well as networking using InfiniBand Verbs, eRDMA or TCP/IP sockets."),
    author="Alibaba Cloud",
    author_email="ziqi.yzq@alibaba-inc.com",
    license="Copyright (C) Alibaba Group Holding Limited",
    keywords="Distributed, Deep Learning, Communication, NCCL, AIACC",
    url="https://help.aliyun.com/document_detail/462422.html?spm=a2c4g.462031.0.0.c5f96b4drcx52F",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    packages=total_packages,
    package_dir={package_name: "deepnccl"},
    package_data={'deepnccl': ['libnccl.so.2']},
    include_package_data=True,
    #data_files=[("aiacc_nccl", ["aiacc/aiacc.so"])],
    # ext_modules=aiacc_ext_modules,
    install_requires=[
      'deep-index',
      'deepncclplugin',
    ],
    # scripts=['aiacc_bind'],
    # cmdclass=aiacc_cmdclass
    # install_requires=['aiacc_nccl_cu11']
    cmdclass={
      'install': post_install
    },
    python_requires=">=3.0",
)

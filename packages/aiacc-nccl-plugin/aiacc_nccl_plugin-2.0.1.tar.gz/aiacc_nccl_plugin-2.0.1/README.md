# AIACC-NCCL-PLUGIN

Optimized socket/rdma for inter-GPU communication on Aliyun machines.

## Introduction

AIACC-NCCL-PLUGIN is an AI-Accelerator communication framework plugin for NVIDIA-NCCL.
It has been optimized to achieve high bandwidth on aliyun machines using InfiniBand Verbs, eRDMA or TCP/IP sockets.

## Install

To install AIACC NCCL PLUGIN on the system, create a package then install it as root as follow two methods:

- method1: rpm/deb (Recommended)
```sh
# Centos:
wget http://mirrors.aliyun.com/aiacc/aiacc-nccl-plugin/aiacc-nccl-plugin-1.1.0.rpm
rpm -i aiacc-nccl-plugin-1.1.0.rpm
# Ubuntu:
wget http://mirrors.aliyun.com/aiacc/aiacc-nccl-plugin/aiacc-nccl-plugin-1.1.0.deb
dpkg -i aiacc-nccl-plugin-1.1.0.deb
```

- method2: python-pypi
```sh
pip install aiacc_nccl_plugin
```

## Usage

After install aiacc-nccl-plugin package, you need do nothing to change code!

## Copyright

All source code and accompanying documentation is copyright (c) 2015-2020, NVIDIA CORPORATION. All rights reserved.
All modifications are copyright (c) 2020-2024, ALIYUN CORPORATION. All rights reserved.

# 一种通用SfM-MVS三维重建框架环境搭建

基于SfM(运动恢复结构)的三维重建基本流程可用下图表示：

<div align=center>
<img src="https://lazywzx.info/wp-content/uploads/2022/06/mosaic.jpg" />
</div>

其核心原理是是通过多张高度重叠、视角变化的图片恢复相机位置姿态和空间点坐标，如下图

<div align=center>
<img src="https://lazywzx.info/wp-content/uploads/2022/06/sfm_colmap.jpg" />
</div>

下载框架代码到本地，地址：[SfM_MVS](https://github.com/lazywzx/study/tree/master/SfM_MVS)，可使用浏览器插件如GitZip下载。

然后根据下面的说明进行环境搭建，在`s0_dataset`目录下的`DSTree.py`中配置数据路径，在`DSParameter.py`中配置运行参数，在`s1_sfm`目录下的`config_yaml.py`中配置运行参数，最后在顶层目录下运行`main.py`即可（可通过`main.py`控制重建步骤）。

# 运行环境搭建

> ⚠实验版本，有待优化

## 0、建议在Docker中搭建环境（便于环境隔离和移植）

### [Dockerの简单使用🐳](https://lazywzx.info/?p=906)

### 安装[YaHei Consolas Hybrid 1.12](https://github.com/yakumioto/YaHei-Consolas-Hybrid-1.12#yahei-consolas-hybrid-112)字体

### ✅建议：对于需要编译安装的项目

> 每次编译后建议执行一次`ldconfig`
>  
> 如果编译有问题需要重新编译，在重新编译前清理一下：`make clean`
>  
> 如果系统配置发生变化，需要重新编译，将build/目录下内容全部删掉在重新cmake（使用configure工具的项目可忽略）

### ❗所有项目的安装顺序不可改变

## 1、安装python3依赖

```Shell
pip3 install -r requirements.txt
```

## 2、编译安装OpenCV2（同时支持Python3和C++）

* 😡带着opencv_contrib编译，第一次编译成功，后来装了VTK，编译其它软件时报了OpenCV的错，遂重装OpenCV，然在编译opencv_sfm模块时抛出链接错误，不带opencv_contrib编译成功。
* OpenCV看似平常，资料很多，实测是最难对付的

[opencv.org](https://docs.opencv.org/4.x/d2/de6/tutorial_py_setup_in_ubuntu.html)

[Building OpenCV from source🐮](https://lazywzx.info/?p=605)

[Installation in Linux](https://docs.opencv.org/4.x/d7/d9f/tutorial_linux_install.html)

### 安装编译依赖和图片格式支持包

```bash
sudo apt install -y cmake gcc g++ \
python3-dev python3-numpy \
libavcodec-dev libavformat-dev libswscale-dev \
libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev \
libgtk-3-dev
```

```bash
sudo apt install -y libpng-dev libjpeg-dev libopenexr-dev libtiff-dev libwebp-dev
```

### 编译libTIFF

```bash
cd
wget http://download.osgeo.org/libtiff/tiff-4.4.0.tar.gz
# 解压后进入目录
./configure
make -j 10 && sudo make install
```

### 编译GeoTIFF库

```bash
cd
wget http://download.osgeo.org/geotiff/libgeotiff/libgeotiff-1.7.1.tar.gz
# 解压后进入目录
./configure --with-jpeg --with-zlib
make -j 10 && sudo make install
```

* 上边这两个库原本是后边编译PROJ的依赖项，但我发现有很多其他包也依赖它们，所以把它们提前编译了

### [Building VTK](https://github.com/Kitware/VTK/blob/master/Documentation/dev/build.md#building-vtk)

根据官网指导编译即可

* [Removed VTK, odm_cleanmesh module #1275](https://github.com/OpenDroneMap/ODM/pull/1275)
* 这个主要是为后边编译odm_cleanmesh做依赖，但后者已经被证实效果不好，可以考虑修改重建工程代码，删掉`s6_meshing/meshing.py`中的`clean_mesh()`函数

### 下载源码

```bash
sudo apt install -y git wget
cd
git clone https://hub.fastgit.xyz/opencv/opencv.git
wget https://hub.fastgit.xyz/opencv/opencv_contrib/archive/refs/tags/4.5.5.tar.gz
# 解压
tar -zxvf opencv_contrib-4.5.5.tar.gz
```

### 准备编译

```bash
cd opencv/ && mkdir build/ && cd build/
cmake -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.5.5/modules/ -DOPENCV_GENERATE_PKGCONFIG=YES -DOPENCV_ENABLE_NONFREE=ON -DCMAKE_INSTALL_PREFIX=/usr/local/ ../
# 这里大概率time out，手动下载的话验证可能不通过，最好有全局代理或者在CMake文件里禁止hash验证
```

这里要检查一下opencv是要给python3安装还是python2，如果出现以下提示信息，则表示给python3安装，是正常的，如果**Python for build**后边是*usr/bin/python2*，则需要卸载python2。

```bash
--   Python 3:
--     Interpreter:                 /usr/bin/python3 (ver 3.8.10)
--     Libraries:                   /usr/lib/x86_64-linux-gnu/libpython3.8.so (ver 3.8.10)
--     numpy:                       /usr/local/lib/python3.8/dist-packages/numpy/core/include (ver 1.22.4)
--     install path:                lib/python3.8/site-packages/cv2/python-3.8
-- 
--   Python (for build):            /usr/bin/python3
```

### 开始编译

编译时间较长，建议选择空闲时间进行。

```bash
cd ~/opencv/build/
make -j 10
# 安装到系统: /usr/local/opencv4/
sudo make install
```

### 配置C++环境

[配置C++开发环境](https://www.cnblogs.com/zfb132/p/14619017.html)

注意路径改成自己的（**准备编译**中的路径）

### 验证安装

```bash
# python应能够输出版本号
python3 -c 'import cv2; print(cv2.__version__)'
```

```CPP
// C++
#include<iostream>
#include <opencv2/opencv.hpp>

using namespace cv;

int main() {
    printf(CV_VERSION);
}
```

```cmake
# 声明一个cmake工程
project(cvTest)

# 声明要求的cmake最低版本
cmake_minimum_required(VERSION 2.8)

# 添加库
# 静态库：add_library(libhello_static libHello.cpp)
# 共享库：add_library(libhello_shared SHARED libHello.cpp)
# add_library(libHello_shared SHARED libHello.cpp)

# 外部依赖包
find_package(OpenCV REQUIRED)

# set(OpenCV_DIR "/usr/local/opencv4/")
# 指定头文件路径
include_directories(${OpenCV_INCLUDE_DIRS})
# 外部lib
# link_directories(${OpenCV_LIBS_DIR})

# 添加一个可执行程序
# 语法：add_executable(程序名 源代码文件)
add_executable(cvTest cvtest.cpp)

# 链接库和可执行文件
target_link_libraries(cvTest)
```

## 3、安装OpenSfM

### [Ceres](http://ceres-solver.org/installation.html#linux)

根据官网指导安装即可（如果github访问超时，将*github.com*修改为*hub.fastgit.xyz*即可，以下同理）

### [OpenGV](https://laurentkneip.github.io/opengv/page_installation.html)

```bash
# 下载地址
git clone --recurse-submodules -j10 https://hub.fastgit.xyz/laurentkneip/opengv
```

```bash
cd opengv/ && mkdir build/
cd build/ && cmake -DBUILD_PYTHON=ON -DPYBIND11_PYTHON_VERSION=3.8 -DPYTHON_INSTALL_DIR=/usr/local/lib/python3.8/dist-packages/ ../
make -j 10 && make install
```

### [OpenSfM](https://opensfm.org/docs/building.html#building)

根据官网指导安装

（这里可能有个坑：pip安装依赖过程中，requirements.txt指定joblib==0.14.1，但之前装的scikit-learn 1.1.1需要依赖joblib>=1.0.0，我暂时装了joblib>=1.0.0，祈祷能兼容吧）

安装完成后，将`./bin/`和`./opensfm/`两个目录拷贝到重建工程目录下的`bin/osfm/`目录下

## 4、编译PoissonRecon

### [三维建模之泊松重建 Poisson Surface Reconstruction](https://blog.csdn.net/weixin_37835423/article/details/114874129)

这里有个巨坑，直接`make`会内存不足而卡死，对于16G内存，经测试使用2核编译可以成功：

```bash
make -j 2
# 建议打开htop监测内存占用情况，一旦接近占满，立刻kill掉编译进程
# 真要是卡死了也最好不要强制关机，Ctrl+Alt+F3开一个终端，等待不太卡的时机正常关机：
sudo shutdown now
# 或者干等着，等系统触发OOM自动杀死编译进程（大约需要等5分钟）
```

编译完成后在`./Bin/Linux/`目录下找到`PoissonRecon`，将其拷贝到重建工程目录下的`bin/`目录下

## 5、编译GDAL

### [PROJ](https://proj.org/install.html#compilation-and-installation-from-source-code)

```bash
# 安装依赖
sudo apt install curl libssl-dev libcurl4-openssl-dev
```

[ubuntu编译安装sqlite3](https://www.jianshu.com/p/10ef3e23a9f6)

```bash
cd
wget https://www.sqlite.org/2022/sqlite-autoconf-3380500.tar.gz
# 解压后进入（解压命令tar -zxvf XXX.tar）
# 如果配置了oh-my-zsh可以用'x'命令
mkdir build && cd build
./configure
make -j 10 && sudo make install
```

* [安装zsh并配置oh-my-zsh——让你的命令行起飞！🚀](https://lazywzx.info/?p=310)

正式编译PROJ

```bash
sudo apt install zip unzip
# 下载PROJ源码
cd
git clone https://hub.fastgit.xyz/OSGeo/PROJ.git
cd PROJ/ && mkdir build
cd build && cmake ../
# 正常情况到这里会卡在Checking if network is available...，等待一会进入下载状态，如果github访问不了，这里就Ctrl+C结束掉
```

* 如果上一步没有下载成功：

```bash
ls
# 可以看到要下载的目录
cd googletest-download/
# 查看下面这个文件里的url，将github.com改为hub.fastgit.xyz后手动下载
vim CMakeLists.txt
cd
wget https://hub.fastgit.xyz/google/googletest/archive/release-1.11.0.zip
# 拷贝到目的目录下
cp release-1.11.0.zip PROJ/build/googletest-download/googletest-prefix/src/release-1.11.0.zip
# 再次cmake
cd PROJ/build/
cmake ../
# 实测可以成功（意外的是HASH验证竟然能通过，一般这种手动下载的是不能通过的）
```

```bash
make -j 10 && sudo make install
```

### [Building GEOS From Source](https://github.com/libgeos/geos/blob/main/INSTALL.md#building-geos-from-source)

根据指导安装即可

### 正式编译GDAL

```bash
cd
git clone https://hub.fastgit.xyz/OSGeo/GDAL.git
cd GDAL && mkdir build && build
cmake -DCMAKE_BUILD_TYPE=Release ../
make -j 10 && sudo make install
```

编译完成后进入`apps/`目录下将`gdal_translate`, `gdalbuildvrt`, `gdalwarp`拷贝到重建工程目录下的`bin/gdal/`目录下

将`ogr2ogr`拷贝到重建工程目录下的`bin/`目录下

编译python库

```bash
cd ~/GDAL/build/swig/python/
python3 setup.py build
python3 setup.py install
```

编译完成后在`build/scripts-3.8`目录下将`gdal_proximity.py`和`gdal_fillnodata.py`拷贝到重建工程目录下的`bin/gdal/`目录下

## 6、编译PDAL

### [ubuntu 安装ninja](https://blog.csdn.net/u013171226/article/details/120971325)

根据网页指导安装即可

```bash
git clone https://hub.fastgit.xyz/PDAL/PDAL.git
cd PDAL/ && mkdir build/ && cd build/
cmake -G Ninja ../
ninja
ninja install
```

编译完成后将`bin/`目录下的`gdal`拷贝到重建工程目录下的`bin/`目录下

## 7、编译dem2mesh

### [dem2mesh](https://github.com/OpenDroneMap/dem2mesh#dem2mesh)

根据提示直接编译即可，注意不需要安装到系统中，即不用执行`sudo make install`，将`build/`目录下的`dem2mesh`拷贝到重建工程目录下的`bin/odm/`目录下

## 8、编译odm_cleanmesh

```bash
cd
wget https://hub.fastgit.xyz/OpenDroneMap/ODM/archive/refs/tags/2.4.7.tar.gz
# 解压后进入
cd modules/odm_cleanmesh/ && mkdir build/ && cd build/
cmake ../
make -j 10
# 不用安装到系统
```

编译完成后将`build/`目录下的`odm_cleanmesh`拷贝到重建工程目录下的`bin/odm/`目录下

## 😡9、编译odm_orthophoto（⛔失败）

* 暂时未能安装成功，可能属环境混乱，版本冲突问题，待重开Docker实验
* 如果不需要生成正射图，则不需要此步骤，同时将重建工程目录下的第8步取消掉

[odm_orthophoto](https://github.com/OpenDroneMap/odm_orthophoto#odm_orthophoto)

```bash
# 安装依赖
apt install libpcl-dev
```

## 10、编译MVS-Texturing

[MVS-Texturing Exercise](https://blog.csdn.net/esther_Mo/article/details/104444586)

[MVS-Texturing](https://github.com/nmoehrle/mvs-texturing#mvs-texturing)

```bash
# 下载源码后进入目录，先进入elibs/目录
# 修改CMakeLists.txt
vim CMakeLists.txt
# 将文件中的"github.com"修改为"hub.fastgit.xyz"
cd ../ && mkdir build && cd build
cmake ../ && make -j 10
```

> 批量替换文件内容：在Vim命令模式下输入%s/github.com/hub.fastgit.xyz/g
>  
> [一些VIM配置项🛠](https://lazywzx.info/?p=876)

编译完成后将`build/apps/texrecon/`目录下的`texrecon`拷贝到重建工程目录的`bin/`目录下。

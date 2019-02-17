**pySimmToolbox**
--------

**Installation:**

1. Setup for this guide is Python 3.6 (not Anaconda) and PyCharm
2. After cloning / downloading the Repository to PyCharm set `src` Folder and `test` Folder as `Rightclick` &rarr; `Mark Directory as` &rarr; `Sources Root`.  
This is necessary to enable imports in the `test` Folder.
3. pySimmToolbox uses [Treelib](https://treelib.readthedocs.io/en/latest/) which can be installed with
`pip install treelib`
4. pySimmToolbox uses the [java open source simm library by acadiasoft](https://github.com/AcadiaSoft/simm-lib "simm-lib"). pySimmToolbox includes a precompiled jar of simm version 2.1 found at `src` &rarr;`simmLib`
5. To call simmLib from Python [Pyjnius](https://pyjnius.readthedocs.io/en/stable/index.html) is used. Follow the installation instructions found [here](https://pyjnius.readthedocs.io/en/stable/installation.html#installation-for-windows "Pyjnius installation for Windows"). It is recommended to use [Java 8](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html). Using Java 11 will as of Feb 2019 crash the installation of Pyjnius. (Note: Make sure that a Folder called 'JRE' can be found in your JDK. If not download the JRE and copy the JRE installation in the JDK folder. Rename the folder to just `jre`.)
6. Run Unittests by rightclicking on Directories in `test` root folder and selecting `Run Unittests in ...` where `...` may be `Calculation`, `CRIF`, `ResultTrees` etc.

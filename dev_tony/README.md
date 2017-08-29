# LNLS - Desafio 5

## FILES

* **AFC_Omnysis_Test -** Repository with the code to test the AFC Board

* **AFC_Loopback -** Repository with the code to test the AFC Board with Loopback Board

* **Plano_de_Testes-Desafio 5.pdf -** Test plan walkthrough

* **AFC_Diagram.pdf -** Test plan setup diagrams

## Documentation

The system documentation for the tests and the test diagrams are in documentation branch:
## Software

Vivado v2016.2 (64-bit)
Download link: https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/archive.html

## Drivers

Xilinx USB Cable Drivers
1. Disconnect all Xilinx USB cables from the host computer. 
2. Open a shell or terminal console. 
3. Download install_drivers.tar.gz from: secure.xilinx.com/webreg/clickthrough.do?cid=103670 
4. Extract the driver script and its support files by typing: tar xzvf install_drivers.tar.gz.
The extraction creates a directory named install_drivers in the current directory. 
5. Navigate to the install_drivers directory by typing: cd install_drivers.
6. Run the script by typing: ./install_drivers.
7. When the installation is complete, connect the Xilinx USB cable to the desired USB port. If the STATUS indicator on the cable illuminates, then the driver installation completed successfully.

## Libraries

### Ipmitool

sudo apt-get update
sudo apt-get install ipmitool

Below there are the libraries that are not built-in in python 3.71.
 
### Installing the pip

First of all, pip has to be installed. To install pip, securely download get-pip.py.
Then run the following:

```
python get-pip.py
```

Or in case of pip already installed, upgrade it to the latest version:

```
python -m pip install --upgrade pip
```


### Pyipmi
```
sudo apt-get update
sudo apt-get install ipmitool
```


### PyQT4

#### qt4-designer (must be qt4)

Debian/Ubuntu:

```
sudo apt-get install python-qt4 qt4-designer
```

### sip (Must be 4.19.1 or above)

Debian/Ubuntu:

```
https://www.riverbankcomputing.com/software/sip/download
```

And then go to the sipfile/doc/installation.html

## Authors

* **Tony Ishak** - *Developer* - [Email](tony.ishak@thalesgroup.com)
* **Guilherme Santos** - *Developer* - [Email](guilherme.santos@thalesgroup.com)

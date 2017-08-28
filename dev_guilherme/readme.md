# LNLS - Desafio 5

## Documentation

The system documentation for the tests, and the test diagrams are the below files on the repository root:
* **Plano_de_Testes-Desafio 5.pdf**
* **RFFE-and-ADC_Diagram.pdf**

## Libraries

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

### SciPy Stack

Install the SciPy stack packages with pip. It is recommend a user install, using the --user flag to pip (note: don’t usesudo pip, that will give problems). This installs packages for your local user, 
and does not need extra permissions to write to the system directories:

```
pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
```

For user installs, make sure your user install executable directory is on your PATH. Here are example commands for setting the user PATH:

```
# Consider adding this at the end of your ~/.bashrc file
export PATH="$PATH:/home/your_user/.local/bin"
```

### Matplotlib

You might prefer to use your package manager. matplotlib is packaged for almost every major Linux distribution.

Debian / Ubuntu :

```
sudo apt-get install python-matplotlib
```

Fedora / Redhat :

```
sudo yum install python-matplotlib
```

### pyserial

There are also packaged versions for some Linux distributions:

Debian/Ubuntu:

```
sudo apt-get install python-serial
sudo apt-get install python3-serial
```

Fedora / RHEL / CentOS / EPEL:

```
sudo yum install pyserial
```

Some distributions may package an older version of pySerial. These packages are created and maintained by developers working on these distributions.

### paramiko

The recommended way to get Paramiko is to install the latest stable release via pip:


```
pip install paramiko
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

* **Fernando Petrecca** - *Developer* - [Email](fernando.petrecca@thalesgroup.com)

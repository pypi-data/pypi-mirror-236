# Table of Contents <a name="table-of-contents"></a>
- [Table of Contents ](#table-of-contents-)
- [electronconfig ](#electronconfig-)
- [Installation ](#installation-)
- [Usage ](#usage-)

# electronconfig <a name="electronconfig"></a>
This package is used to find the electron configuration of an element. It is also used to do different operations on the electron configuration of an element. 

# Installation <a name="installation"></a>
To install this package, run the following command in the terminal:
```bash
pip install electronconfig
```
For developer installation, run the following command in the terminal:
```bash
git clone https://github.com/jako4295/electronconfig
pip install -e electronconfig
```

# Usage <a name="usage"></a>
To use this package, run the following command in the terminal:
```python
import electronconfig as ec

ec_obj = ec.ElectronConfig()
```
This will create an object of the ElectronConfig class. This object can be used to find the electron configuration of an element. All electron configuations are saved as attributes to the ```ec_obj``` object. For example, ```ec_obj.ec1``` gives the electron configuration of hydrogen. 

The following code can be used to remove electrons from a given element:
```python
ec_obj.remove_electrons(82, 54)
```
This will remove 54 electrons from the element with atomic number 82 (lead). To find the principle quantum number of outermost projectile electron ($n_0$) of an element, one can either look at the string returned from the code above or run the following code:
```python
ec_obj.n_0(82, 54)
```
This will return the principle quantum number of the outermost projectile electron of lead.

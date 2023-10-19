# Geez Number Convertor

This library helps you to convert any arabic number to geez number. 

## Installation 
```
$ pip install geeznum
```

Example 
```
python

from geeznum import GeezNumber

geez = GeezNumber()

numbers = [15, 20, 109, 55, 1011, 1500, 167, 2345, 2500, 5100, 10,000]

for num in numbers:
    print(geez.convert(num))
```
Output
```
፲፭
፳
፻፱
፶፭
፲፻፲፩
፲፭፻
፲፷፯
፳፫፻፵፭
፳፭፻
፶፩፻
፼
```
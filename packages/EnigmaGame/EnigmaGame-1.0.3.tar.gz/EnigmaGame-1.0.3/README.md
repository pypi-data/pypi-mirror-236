# EnigmaGame

*A game as difficult as the Rubik’s cube*

* **category**    Game, Program
* **version**     1.0.3
* **author**      Michael Hodel <info@adiuvaris.ch>
* **copyright**   2023 Michael Hodel - Adiuvaris
* **license**     http://www.gnu.org/copyleft/lesser.html GNU-LGPL v3 (see LICENSE.TXT)
* **link**        https://adiuvaris.ch
* **source**      https://github.com/adiuvaris/EnigmaGame


## Description

This puzzle was invented by Douglas A. Engel and it consists of two intersecting disks in a plastic holder.
This program is a computer version of this puzzle that I wrote in Python.


![image](https://github.com/adiuvaris/EnigmaGame/raw/master/EnigmaGame.png)


## Install

Via PyPi

``` bash
$ pip install EnigmaGame
```

## Usage

``` python
python -m EnigmaGame
```

Start a game and turn the upper and lower disk. The goal is to reset the pattern to the example in the right corner.

The rotations can be initiated with an intuitive mouse movement (or on a touch screen with a finger gesture). 
This requires a mouse click on the appropriate disk and then a mouse move while holding the mouse button pressed. 
When you release the mouse button, the rotation is executed. With a touch screen you can do that with the finger.
It is also possible to turn the disks with the left and right cursor keys. 
If you additionally hold the shift key the upper disk will be rotated.

On the screen you see the actual playing area. It consists of two circular disks that are intersecting each other. 
On each disk, there are six stones alternating with six bones. The stones look like overweight triangles, 
the bones as malnourished rectangles. Since the disks are intersecting, they share two stones and a bone. If a disk, 
let’s say the upper one, is rotated by 60 degrees, then one stone and one bone that had previously also belonged 
to the lower disk are replaced by a new stone and new bone.



## License

GNU LESSER GENERAL PUBLIC LICENSE. Please see [License File](LICENSE) for more information.
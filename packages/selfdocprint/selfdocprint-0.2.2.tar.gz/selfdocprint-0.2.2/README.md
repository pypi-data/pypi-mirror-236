# Selfdocprint

Provides enhanced and configurable `print()` functionality that allows for easily printing values such that they are: 

* *self-documented*
* *formatted*
* *nicely laid out*

Fully compatible with python's built-in `print()`. Supports all its keyword arguments, including `file=` and `flush=`. 

The module comes with four layout classes. Below is an example of InlineLayout.


```python
from selfdocprint import PrintFunc, InlineLayout

# instantiate a function
print = PrintFunc()  # this will now shadow python's built-in print function

# some data
formula = "Ultimate Question of Life,\nthe Universe, and Everything"
theta = 6.006
x = 7

# let's print it with our print function
print(formula, theta, x, x*theta, layout=InlineLayout())
```

![image_1](https://raw.githubusercontent.com/marcelloDC/selfdocprint/main/images/output_image_1.png)

The default value for the `layout=` keyword argument (normally `None`) can be configured so that subsequent calls require even less typing. In this case it would be good practice to not call the function 'print' to avoid confusion with the expected behaviour of python's built-in `print()`.


```python
prinline = PrintFunc(default_layout=InlineLayout())

prinline(formula, theta, x, x*theta)
```

![image_2](https://raw.githubusercontent.com/marcelloDC/selfdocprint/main/images/output_image_2.png)

A layout can be customised by overriding one or more of its fields (The fields are described in detail in the section: 'Style, format and layout specification'). Note that in the example below we override `head=` to suppress the empty line that is normally printed in front of the output when using the InlineLayout.


```python
for i in range(0, 99, 21):
    print(i, i * theta, layout=InlineLayout(float_format="12.6f", pointer=" -> ", head=""))
```

![image_3](https://raw.githubusercontent.com/marcelloDC/selfdocprint/main/images/output_image_3.png)

Custom layouts can be created and referenced in subsequent calls. Note that in the example below we change the `style=` for the labels, which is specified as [ANSI Select Graphic Rendition](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters) parameters.


```python
my_layout = InlineLayout(style="92;3", int_format="4")

print(x, x * theta, layout=my_layout)
```

![image_4](https://raw.githubusercontent.com/marcelloDC/selfdocprint/main/images/output_image_4.png)

## Built-in layouts
Next to the *'inline'* layout three additional layouts are available. The example below demonstrates the *'dict'* layout. In addition it shows the use of the `beg=` keyword argument which can be used to provide a heading to the output.


```python
from selfdocprint import DictLayout

print(formula, theta, x, x*theta, layout=DictLayout(), beg="Using the 'dict' layout:\n")
```

![image_5](https://raw.githubusercontent.com/marcelloDC/selfdocprint/main/images/output_image_5.png)

For values that take up a lot of horizontal space the *'scroll'* layout is particularly useful.


```python
from selfdocprint import ScrollLayout
import numpy as np

X = np.random.rand(5,5)

print(X, X.T @ X, layout=ScrollLayout(), beg="Using the 'scroll' layout:\n")
```

![image_6](https://raw.githubusercontent.com/marcelloDC/selfdocprint/main/images/output_image_6.png)

Use the *'minimal'* layout if you only want to print labels in front of the values.


```python
from selfdocprint import MinimalLayout

print(formula, theta, x, theta*x, layout=MinimalLayout(), beg="Using the 'minimal' layout:\n\n")
```

![image_7](https://raw.githubusercontent.com/marcelloDC/selfdocprint/main/images/output_image_7.png)

## Style, format and layout specification
The `selfdocprint.print_layout_specs()` function prints the specification for every built-in layout and a rudimentary description of the layout algorithm.


```python
import selfdocprint as sdp

sdp.print_layout_specs()
```

![image_8](https://raw.githubusercontent.com/marcelloDC/selfdocprint/main/images/output_image_8.png)

All parameters are of type str. The format parameters are specified according to python's [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec). If an alignment character (<, >, or ^) is specified without a fixed width in the lbl_format, then the alignment will be made relative to all other <labels\>. For the str_format a missing width value will result in an alignment of all lines in the string representation of a value. The algorithm injects the width of the longest string of the <label\> strings and the width of the longest line in a <value\> string into lbl_format and str_format respectively.

The sty parameter is a string with zero or more [ANSI Select Graphic Rendition](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters) parameters seperated by semicolons (;).

The layout algorithm globally works as follows: 1) adjust lbl_format and str_format where necessary; 2) style and format the concatenations of each <label\> with `pointer`; 3) format the values; 4) layout each <label\>/<value\> pair in a 'pane'; 5) join these panes together with `seperator`; 6) print the panes: if `seperator` contains a newline ('\n') character then the panes are laid out from top to bottom, if not, they are laid out from left to right.

## Limitations
* Selfdocprint cannot be used in the Repl nor with `eval()`, `exec()` and `compile()`. Selfdocprint uses the `inspect` module to discover the labels and this does not work in these situations.
* Selfdocprint's print function cannot accept arguments that use the unpack operator, for example to unpack a tuple: `*my_tuple`. This does not make sense anyway because there is nothing to label the individual values of the tuple with, so it's just as informative to just use the tuple variable as is.

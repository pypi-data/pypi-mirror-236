# Pigmento: Colorize and Trace Printing

<style>
span.red {
    color: #FF6B6B;
}

span.green {
    color: #9EE09E;
}

span.yellow {
    color: #FFE156;
}

span.blue {
    color: #6B9BFF;
}

span.magenta {
    color: #E27DEA;
}

span.cyan {
    color: #6BE7E7;
}
</style>

![Pigmento](https://liu.qijiong.work/images/covers/pigmento.png)

## Introduction

Pigmento is a Python package that can colorize and trace printing. It can be used to quickly locate the source of the print statement.
Moreover, it supports customizing the style of printing, prefixes, and powerful plugins.

## Installation

```bash
pip install pigmento
```

## Quick Start

```python
from pigmento import pnt

class Test:
    @classmethod
    def class_method(cls):
        pnt('Hello World')

    def instance_method(self):
        pnt('Hello World')

    @staticmethod
    def static_method():
        pnt('Hello World')
        

def global_function():
    pnt('Hello World')

Test.class_method()
Test().instance_method()
Test.static_method()
global_function()
```

<pre>
<span class="magenta">|Test|</span> <span class="cyan">(class_method)</span> Hello World
<span class="magenta">|Test|</span> <span class="cyan">(instance_method)</span> Hello World
<span class="magenta">|Test|</span> <span class="cyan">(static_method)</span> Hello World
<span class="cyan">(global_function)</span> Hello World
</pre>

### Style Customization

```python
from pigmento import pnt, Color

pnt.set_display_style(
    method_color=Color.RED,
    method_bracket=('<', '>'),
    class_color=Color.BLUE,
    class_bracket=('[', ']'),
)

Test.class_method()
Test().instance_method()
Test.static_method()
```

<pre>
<span class="blue">[Test]</span> <span class="red">&lt;class_method&gt;</span> Hello World
<span class="blue">[Test]</span> <span class="red">&lt;instance_method&gt;</span> Hello World
<span class="blue">[Test]</span> <span class="red">&lt;static_method&gt;</span> Hello World
</pre>

### Display Mode Customization

```python
from pigmento import pnt

pnt.set_display_mode(
    display_method_name=False,
)

Test.class_method()
```

<pre>
<span class="magenta">|Test|</span> Hello World
</pre>

## Prefixes

Pigmento supports customized prefixes for each print.
It is important to note that all prefixes are in **first-in-first-print** order.

```python
from pigmento import pnt, Prefix, Color, Bracket

pnt.add_prefix(Prefix('DEBUG', bracket=Bracket.DEFAULT, color=Color.GREEN))

global_function()
```

<pre>
<span class="green">[DEBUG]</span> <span class="cyan">(global_function)</span> Hello World
</pre>

### Dynamic Prefix

Texts inside prefix can be dynamically generated.

```python
from pigmento import pnt, Prefix, Color, Bracket

class System:
    STATUS = 'TRAINING'
    
    @classmethod
    def get_status(cls):
        return cls.STATUS
    
    
pnt.add_prefix(Prefix(System.get_status, bracket=Bracket.DEFAULT, color=Color.GREEN))

global_function()
System.STATUS = 'TESTING'
global_function()
```

<pre>
<span class="green">[TRAINING]</span> <span class="cyan">(global_function)</span> Hello World
<span class="green">[TESTING]</span> <span class="cyan">(global_function)</span> Hello World
</pre>

### Build-in Time Prefix

TimePrefix is a build-in prefix that can be used to display time.

```python
import time
import pigmento
from pigmento import pnt

pigmento.add_time_prefix()

Test.class_method()
time.sleep(1)
Test.class_method()
```

<pre>
<span class="green">[00:00:00]</span> <span class="magenta">|Test|</span> <span class="cyan">(class_method)</span> Hello World
<span class="green">[00:00:01]</span> <span class="magenta">|Test|</span> <span class="cyan">(class_method)</span> Hello World
</pre>

## Plugins

Pigmento supports plugins to extend its functionalities.

### Build-in Logger

Everytime you print something, it will be logged to a file.

```python
import pigmento
from pigmento import pnt

pigmento.add_log_plugin('log.txt')

global_function()
```

<pre>
<span class="cyan">(global_function)</span> Hello World
</pre>

The log file will be created in the current working directory and the content will be removed the color codes.

```bash
cat log.txt
```

<pre>
[00:00:00] (global_function) Hello World
</pre>

### Build-in Dynamic Color

DynamicColor will map caller class names to colors.

```python
import pigmento
from pigmento import pnt


class A:
    @staticmethod
    def print():
        pnt(f'Hello from A')


class B:
    @staticmethod
    def print():
        pnt(f'Hello from B')


class D:
    @staticmethod
    def print():
        pnt(f'Hello from C')


A().print()
B().print()
D().print()

pigmento.add_dynamic_color_plugin()

A().print()
B().print()
D().print()
```

<pre>
<span class="magenta">|A|</span> <span class="cyan">(print)</span> Hello from A
<span class="magenta">|B|</span> <span class="cyan">(print)</span> Hello from B
<span class="magenta">|D|</span> <span class="cyan">(print)</span> Hello from C
<span class="magenta">|A|</span> <span class="cyan">(print)</span> Hello from A
<span class="red">|B|</span> <span class="cyan">(print)</span> Hello from B
<span class="yellow">|D|</span> <span class="cyan">(print)</span> Hello from C
</pre>

### Plugin Customization

```python
from pigmento import pnt, BasePlugin


class RenamePlugin(BasePlugin):
    def middleware_before_class_prefix(self, name, bracket, color):
        return name.lower(), bracket, color

    def middleware_before_method_prefix(self, name, bracket, color):
        return name.replace('_', '-'), bracket, color


pnt.add_plugin(RenamePlugin())

Test.class_method()
Test().instance_method()
Test.static_method()
```

<pre>
<span class="magenta">|test|</span> <span class="cyan">(class-method)</span> Hello World
<span class="magenta">|test|</span> <span class="cyan">(instance-method)</span> Hello World
<span class="magenta">|test|</span> <span class="cyan">(static-method)</span> Hello World
</pre>


## Multiple Printers

Pigmento supports multiple printers.

```python
from pigmento import Pigmento, Bracket, Color, Prefix

debug = Pigmento()
debug.add_prefix(Prefix('DEBUG', bracket=Bracket.DEFAULT, color=Color.GREEN))

info = Pigmento()
info.add_prefix(Prefix('INFO', bracket=Bracket.DEFAULT, color=Color.BLUE))

error = Pigmento()
error.add_prefix(Prefix('ERROR', bracket=Bracket.DEFAULT, color=Color.RED))


def divide(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        error('Inputs must be integers')
        return

    if b == 0:
        debug('Cannot divide by zero')
        return

    info(f'{a} / {b} = {a / b}')


divide(1, 2)
divide(1, 0)
divide('x', 'y')
```

<pre>
<span class="blue">[INFO]</span> <span class="cyan">(divide)</span> 1 / 2 = 0.5
<span class="green">[DEBUG]</span> <span class="cyan">(divide)</span> Cannot divide by zero
<span class="red">[ERROR]</span> <span class="cyan">(divide)</span> Inputs must be integers
</pre>

## License

MIT License

## Author

[Jyonn](https://liu.qijiong.work)

# Chroma Console

Chroma console is a python package for adding color and style to terminal text output using ANSI escape codes.

## Installation

```shell
pip install chromaconsole
```

## Functions
```python
Style.bold()
Style.italic()
Style.underline()
Style.strikethrough()
Style.negative()
Style.normal()
Style.reset()
Style.slowblink()
Style.rapidblink()
Style.hidden()
Style.minecraft(*args)
Style.enable()
Style.disable()
Color.text(*args)
Color.background(*args)
```

## Example usage

```python
from chromaconsole import Color, Style

print(f"{Color.text(r, g, b)}here is RGB colored text{Style.reset()}")
print(f"{Color.background(r, g, b)}here is RGB colored background{Style.reset()}")

print(f"{Color.text('#rrggbb')}here is HEX colored text{Style.reset()}")
print(f"{Color.background('#rrggbb')}here is HEX colored background{Style.reset()}")

print(f"{Style.bold()}Bold {Style.reset()}")
print(f"{Style.italic()}Italic {Style.reset()}")
print(f"{Style.underline()}Underline {Style.reset()}")
print(f"{Style.strikethrough()}Strikethrough {Style.reset()}")

print(f"{Style.bold()}{Style.italic()}bold+italic {Style.reset()}")
print(f"{Style.minecraft('§','§ahello §4world§r')}")
```

## .enable() and .disable():

After executing the `Style.disable()` command, the system will no longer apply coloring and styling to the content. To re-enable these features, simply use the `Style.enable()` command.

```python
#disable the coloring and styling
Style.disable()
print(f"{Color.text(r, g, b)}text without color{Style.reset()}")
Style.enable()
print(f"{Color.text(r, g, b)}text with color{Style.reset()}")
```
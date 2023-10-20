# FastPython v1.1.3

FastPython v1.1.3 is **FINALLY** here. my sanity is completely broken.
this is literally the 3nd attempt to fix the download bug-

*sigh*

anyways...

This package allows you to use things faster, such as:
- Colored text w/ [ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code)
- cls/clear command (Package chooses it automatically)
- Easy Error/Warn/Info messages

## Installation

```bash
pip install fasterpython
```

# Using the package

## Class fastpython.OS

### fastpython.OS.GetOSInfo()
Gets some OS info.

Usage:
```python
from fastpython import fastpython

fastpython.OS.GetOSInfo()
```
Output (Example):
```
OS Identifier : nt
OS : Windows
```

### fastpython.OS.ClearScreen()
Clears the screen using a command thats based on your OS.
(e.g. The package chooses the command automatically [cls/clear])

Usage:
```python
from fastpython import fastpython

fastpython.OS.ClearScreen()
```

## Class fastpython.ANSI

### fastpython.ANSI.ColoredOutput(color: int, text: str {optional})
Prints text with the specified color (Uses [ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code)). If you dont know any, please check fastpython.ANSI.ListColors().

Usage:
```python
from fastpython import fastpython

fastpython.ANSI.ColoredOutput(135, "Hello, World!")
```

Output:
Hello World in the color purple (\e[38;5;135mHello, World!)

### fastpython.ANSI.ListColors()
Gives a list of the ANSI colors

Usage:
```python
from fastpython import fastpython

fastpython.ANSI.ListColors()
```

Output:
All (0-255) ANSI colors.

## Class fastpython.Message

### fastpython.Message.Error(errtext: str)
Displays an error message.

Usage:
```python
from fastpython import fastpython

fastpython.Message.Error("Error")
```

Output:
```
[X] Error
```

### fastpython.Message.Warn(warntext: str)
Displays a warning.

Usage:
```python
from fastpython import fastpython

fastpython.Message.Warning("Warning")
```

Output:
```
[!] Warning
```

### fastpython.Message.Info(infotext: str)
Displays an information message.

Usage:
```python
from fastpython import fastpython

fastpython.Message.Info("Information")
```

Output:
```
[i] Information
```

## Class fastpython.Encoding

I dont want to make this readme too long, so....

### Classes in fastpython.Encoding: b16 (base16) b32 (base32) b64 (base64) hex (hexademical) binary (binary)

### Encode/Decode:

#### Encode           
- b16.encode16(txtinput)
- b32.encode32(txtinput)
- b64.encode64(txtinput)
- hex.encodeHex(txtinput)
- bin.encodeBin(txtinput)

#### Decode
- b16.decode16(b16input)
- b32.decode32(b32input)
- b64.decode64(b64input)
- hex.decodeHex(hexinput)
- bin.decodeBin(bininput)

#### Thats it! This was just the Encoding class update.
## Hope you enjoy FastPython! =)


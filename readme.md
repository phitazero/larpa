# LArPa

An argument parser I wrote because argparse is too complicated for most cases (it disgusts me).

## Installation

```bash
pip install git+https://github.com/phitazero/larpa.git
```

## Example

```python
# ran with: python test.py something -ac --input file1 -o file2 --verbose -- --not-a-flag

from larpa import ArgumentParser, SELECT_FROM_OPTIONS

parser = ArgumentParser(
	flags = ["-a", "-b", "-c", "-v", "--verbose"],
	options = ["-i", "--input", "-o", "--output", "-t"]
)

parser.getPositional(1) # "something"
parser.getPositional(2) # "--not-a-flag"
parser.getPositional(42) # None

parser.isSet("-a") # True
parser.isSet("-b") # False
parser.isSet("-c") # True

parser.getOption("-i", "--input") # "file1"
parser.getOption("-o", "--output") # "file2"

parser.getOption("-t") # None
parser.getOption("-t", default="yay") # "yay"

parser.isSet("-v", "--verbose") # True
parser.whichSet("-v", "--verbose") # "--verbose"
parser.whichSet("-v", "--verbose", selectFrom=SELECT_FROM_OPTIONS) # None

parser.assertNoIncompatible("-b", ("-o", "--output"))

parser.assertNoIncompatible("-a", ("-i", "--input"))
# fatal: incompatible flags: -a and --input
# (exit with code 1)
```

## Documentation

Flags like `-abc` will be treated as `-a -b -c`. 

`--` is a marker meaning that every argument after it is a positional argument and can't be a flag

The 0'th positional argument is the executable name.

#### ArgumentParser(argv=None, flags=None, options=None)  
argv - the list of arguments to parse. If `None` sys.argv is used.  
flags - the list of possible flags  
options - the list of possible options  

#### ArgumentParser().getPositional(index) -> str  
Returns the positional argument at the provided index. If none is found returns `None`.

#### ArgumentParser().isSet(\*flags) -> bool  
Returns `True` is at least one of provided flags is present, else `False`.

#### ArgumentParser().whichSet(\*flags, selectFrom=SELECT_FROM_ALL) -> str  
Returns the first encounted set flag from the provided list. If none is set returns `None`.  
selectFrom - what types of flags to check, can be `SELECT_FROM_ALL`, `SELECT_FROM_OPTIONS` or `SELECT_FROM_FLAGS`

#### ArgumentParser().getOption(\*flags, default=None) -> str  
Returns the option after the first encountered flag from the provided list. If none is encountered returns the default.

#### ArgumentParser().assertNoIncompatible(\*flagGroups)
Exits with an error if at least two flags from different groups are set.
A string can be a flag group, in that case it will be treated as a group containing just that string.

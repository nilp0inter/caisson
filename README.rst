`caisson`: The Recursive Decompressor
=====================================

Extract all compressed files recursively using external decompressors
found in the system.


Installation
------------

.. code-block:: shell

   $ pip3 install caisson


Usage
-----

.. code-block::

   $ caisson --help
   usage: caisson [-h] [-q | -v | -d] [--list] [-o {always,never,ask,rename}]
                  [source [source ...]] destination
   
   Recursively decompress files
   
   positional arguments:
     source                file or directory to be extracted
     destination           destination for extracted files
   
   optional arguments:
     -h, --help            show this help message and exit
     -q, --quiet           don't print any log
     -v, --verbose         print a moderate log
     -d, --debug           print a debugging log
     --list                print list of available decompressors
     -o {always,never,ask,rename}, --overwrite {always,never,ask,rename}


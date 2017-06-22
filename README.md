# USB Log Parser

Once `imagemounter` is correctly installed, the program can be run using the
following command (it is probably necessary to run it as root, but you can do it
in a VM):

```
# python3 usb_log_parser.py IMAGE
```

The IMAGE command line argument should be an EnCase file containing an image of
a Linux distribution. (BtrFS for `/` partition is not supported)

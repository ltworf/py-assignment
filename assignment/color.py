try:
    from xtermcolor import colorize
except:
    colorize=lambda string, rgb=None, ansi=None, bg=None, ansi_bg=None, fd=1:string
def message(m,l=0):
    d= (0x00ff00,
        0xffff00,
        0xff0000)
    print colorize(str(m),d[l])
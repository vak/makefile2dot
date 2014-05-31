# A quick-n-dirty visualizer for Makefiles #

DISCLAIMER: I've spent an hour to visualize a large Makefile I needed. 
            So, sorry if it won't work for you.

## DESCRIPTION ##
makefile2dot has been written to visualize Makefiles, e.g. GNU make Makefile. 
It is written in Python and implies that you have Python and GraphViz "dot" utility installed:

    sudo apt-get install graphviz python

## USAGE ##

    python makefile2dot <Makefile >out.dot
or

    python makefile2dot <Makefile |dot -Tpng > out.png
    
## Example ##

This [example Makefile](https://github.com/vak/makefile2dot/blob/master/Makefile) will result in this png-image:
    
![ScreenShot](https://raw.githubusercontent.com/vak/makefile2dot/master/output-examlple.png)

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/vak/makefile2dot/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

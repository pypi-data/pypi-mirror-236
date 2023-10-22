import logging
from datetime import datetime, date, time
import os

def save_to_text(message,folder,function_type):
    if function_type=="df":
        outdir = folder
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        f = open(folder+'\log.txt', 'w')
        f.write(message)
        f.close()

    if function_type=="sl":
        outdir = folder
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        f = open(folder+'\log.txt', 'a')
        f.write(message)
        f.close()

    return


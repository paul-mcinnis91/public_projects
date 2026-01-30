import os
import sys

import signal
from gnuradio import gr

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.auto_dj import PSYOP_Machine
from src import local_data_pull as ld_pull

def main():
    tb = gr.top_block()
    
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    try:
        broadcast_obj = PSYOP_Machine(tb, 2e6)
        broadcast_obj.broadcast()        
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()

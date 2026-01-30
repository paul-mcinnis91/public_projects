import os
import sys
import signal

from gnuradio import gr

dirname = os.path.dirname(__file__)
joined_paths = os.path.join(dirname, "..")
sys.path.append(joined_paths)

from src.record import Record_Attack


def main():
    """Main function of the program. Requires an SDR to be plugged into to work. Creates the top block and feeds it to an instance of
    Record_Attack
    
    Args: None
    
    Returns: None"""

    
    tb = gr.top_block()
    
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    try:
        recorder_object = Record_Attack(tb, 2e6)
        recorder_object.record_iq_data()        
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
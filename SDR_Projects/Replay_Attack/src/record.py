import os
import pathlib
import time

from gnuradio import blocks
from gnuradio import gr
import osmosdr

from src import local_data_pull as ld_pull


class Record_Attack():
    def __init__(self, tb: gr.top_block, samp_rate: int):
        self.tb = tb
        self.samp_rate = int(samp_rate)
        self.local_dirs = ld_pull.get_top_level_directories()

    def get_freqs(self) -> list:
        """Takes freq_list.txt from record_keeping and converts it into a list.
        
        Args: None
        
        Returns: list"""

     
        record_keeping_dir = self.local_dirs['record_keeping']
        freq_list_path = os.path.join(record_keeping_dir, 'freq_list.txt')
        with open(freq_list_path, 'r') as flp:
            freq_list = flp.readlines()
            return freq_list


    def get_iq_file(self) -> pathlib.Path:
        """Returns the path to where the file data will be dumped
        
        Args: None
        
        Returns: iq file path"""

        record_keeping_dir = self.local_dirs['record_keeping']
        iq_file_path = os.path.join(record_keeping_dir, 'myfile1.data')
        return iq_file_path

    def _write_iq_data(self) -> None:
        """Takes the data passed into it from self.record_iq_data and writes it to a file sink
        
        Args: tb (top block)
        
        Returns: None"""

        freq_list = self.get_freqs()
        iq_file_path = self.get_iq_file()
        # Steps: Osmocom Source -> File Sink
        self.tb.connect((self.tb.osmosdr_source,0), (self.tb.file_sink,0))
        
        for freq in freq_list:

            # Locking stops the flowgraph in place and allows you to modify things on the fly
            self.tb.lock()

            # Reconfigure Osmocom Source and File Sink 

            self.tb.disconnect(self.tb.osmosdr_source, self.tb.file_sink)
            self.tb.osmosdr_source.set_center_freq(freq * 1e6, 0)
            self.tb.file_sink = blocks.file_sink(gr.sizeof_gr_complex*1, iq_file_path, False)
            self.tb.file_sink.set_unbuffered(False)
        
            # Reconnect everything
            self.tb.connect((self.tb.osmosdr_source,0), (self.tb.file_sink,0))
            # Unlocking the flowgraph signals to the program that the flowgraph modifications are done and ready to execute
            self.tb.unlock()
            time.sleep(10)

        # input to stop program from automatically terminating
        input('Press Enter to quit')


    def record_iq_data(self):
        """Takes the top block object and the sample rate and records the data. Passes the record data to _write_iq_data which writes it
        to the correct file
        
        Args: tb (top block)
                samp_rate (sample rate in integer format)
                
        Returns: None"""
        
        iq_file_path = self.get_iq_file()
    
        self.tb.file_sink = blocks.file_sink(gr.sizeof_gr_complex*1, iq_file_path, False)
        self.tb.file_sink.set_unbuffered(False)

        self.tb.osmosdr_source = osmosdr.source(args="numchan=" + str(1) + " " + "")

        self.tb.osmosdr_source.set_time_unknown_pps(osmosdr.time_spec_t())
        self.tb.osmosdr_source.set_sample_rate(self.samp_rate)
        self.tb.osmosdr_source.set_center_freq(100e6, 0)
        self.tb.osmosdr_source.set_freq_corr(0, 0)
        self.tb.osmosdr_source.set_gain(0, 0)
        self.tb.osmosdr_source.set_if_gain(32, 0)
        self.tb.osmosdr_source.set_bb_gain(32, 0)
        self.tb.osmosdr_source.set_antenna('', 0)
        self.tb.osmosdr_source.set_bandwidth(0, 0)

        self._write_iq_data()
        
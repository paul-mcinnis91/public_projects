import os
import time

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import osmosdr
import contextlib
import wave

from src import local_data_pull as ld_pull

class PSYOP_Machine:
    def __init__(self, tb: gr.top_block, samp_rate: int):
        self.local_dirs = ld_pull.get_top_level_directories()
        self.tb = tb
        self.samp_rate = samp_rate


    def _song_data(self, song) -> tuple:
        """Extracts song length and sample rate from a song file
        
        Args: song (path)
        
        Returns song_samp_rate (int)
                duration (float)"""
        with contextlib.closing(wave.open(song, 'r')) as s:
            frames, song_samp_rate, = s.getnframes(), s.getframerate()
            duration = frames / float(song_samp_rate)
            return song_samp_rate, duration

    def _get_song_list(self) -> list:
        """Pulls songs from the song_list directory and returns their paths in a list format
        
        Args: None
        
        Returns: list of songs """

        song_list_dir = self.local_dirs['song_list']
        song_file_paths = os.listdir(song_list_dir)
        all_songs = [os.path.join(song_list_dir, song_path) for song_path in song_file_paths]
        return all_songs


    def broadcast(self) -> None:
        """Actual broadcast function. Relies upon the topblock and the sample_rate to be fed into it to run
        
        Args: tb (top block)
              samp_rate (sample rate in integer format)"""

        song_list = self._get_song_list()

        self.tb.WB_Freq_Mod = analog.wfm_tx(self.samp_rate, self.samp_rate)
        
        self.tb.osmo_sink = osmosdr.sink()
        self.tb.osmo_sink.set_sample_rate(self.samp_rate)
        self.tb.osmo_sink.set_center_freq(102e6)
        self.tb.osmo_sink.set_gain(0)
        self.tb.osmo_sink.set_if_gain(20)
        

        # Steps: Wavfile Source -> Rational Resampler -> Frequency Modulation -> Osmo Sink
        #  old  # self.tb.connect(self.tb.wavfile_source, self.tb.rational_resampler, self.tb.WB_Freq_Mod, self.tb.osmo_sink)
        self.tb.connect(self.tb.WB_Freq_Mod, self.tb.osmo_sink)
        
        for song in song_list:

            song_samp_rate = self._song_data(song)[0]

            # Locking stops the flowgraph in place and allows you to modify things on the fly
            self.tb.lock()

            # Disconnect Wavfile Source and Rational Resampler
            if hasattr(self.tb, "wavfile_source"):
                self.tb.disconnect(self.tb.wavfile_source)
                self.tb.disconnect(self.tb.rational_resampler)
            
            # Reconfigure Wavfile Source and Rational Resampler settings
            self.tb.wavfile_source = blocks.wavfile_source(song)
            self.tb.rational_resampler = filter.rational_resampler_fff(self.samp_rate,song_samp_rate)

            # Reconnect everything
            self.tb.connect(self.tb.wavfile_source, self.tb.rational_resampler, self.tb.WB_Freq_Mod)

            # Unlocking the flowgraph signals to the program that the flowgraph modifications are done and ready to execute
            self.tb.unlock()
            time.sleep(3)

        # input to stop program from automatically terminating
        input('Press Enter to quit')



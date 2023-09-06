import pretty_midi

#------------------------------------------------------------------------------------------------------------------------------------


class PhraseToMIDI:
    def __init__(self, phrase, tempo=120):
        """
        Initialize the PhraseToMIDI object.

        Args:
        phrase (list): A list of dictionaries, each containing 'pitch_list' and 'length_list' for a part.
        tempo (int): Optional. The tempo (BPM) for the MIDI file. Default is 120.
        """
        self.phrase = phrase
        self.tempo = tempo
        
    def write_phrase_to_MIDI(self, phrase_array):
        """
        A function that takes the phrase and writes it to a MIDI file.
        
        Args:
            - phrase (list): An array containing the pitches of the four parts.
            
        Returns:
            - A MIDI file storing the note data.
        """
        # Create a new MIDI data object
        midi_data = pretty_midi.PrettyMIDI(initial_tempo=self.tempo)
        
        # Name the parts
        instrument_names = ["Part 1", "Part 2", "Part 3", "Part 4"]
        
        for part in range(4):
            # Define the instrument to acoustic grand piano
            instrument = pretty_midi.Instrument(program=0, name=instrument_names[part])
            # Get the pitch and length lists
            part_pitch_list, part_pitch_length = pitch_and_length(phrase_array, part)
            for i in range(len(part_pitch_list)):
                note_start = sum(part_pitch_length[:i])
                note_end = sum(part_pitch_length[:i+1])
                # Create a Note object 
                note = pretty_midi.Note(
                    velocity=100,  
                    pitch=part_pitch_list[i],  
                    start=note_start,      
                    end=note_end         
                )
                # Add the Note object to the Instrument
                instrument.notes.append(note)
            # Add the Instrument to the MIDI data
            midi_data.instruments.append(instrument)
                
        return midi_data
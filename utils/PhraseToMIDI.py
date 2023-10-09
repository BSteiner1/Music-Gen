import pretty_midi

#------------------------------------------------------------------------------------------------------------------------------------


class PhraseToMIDI:
    def __init__(self, phrase, tempo):
        """
        Initialize the PhraseToMIDI object.

        Args:
        phrase (list): An array for the four parts.
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
    
#------------------------------------------------------------------------------------------------------------------------------------

def pitch_and_length(phrase, part):
    """
    A function that takes the array and splits a part into lists of note pitch and length.
    
    Args:
        - phrase (tuple): a tuple of lists of the form (pitches, note_start_step, note_end_step, instruments).
        - part (int): an integer between 0 and 3 (inclusive) to denote which of the four parts.
        
    Returns:
        - Two lists for the note pitch and length.
    """
    # Extract a single part of the phrase
    phrase_part = phrase[part].tolist()
    
    # Initialize empty lists for note lengths and unique pitches
    note_lengths = []
    pitches = []

    # Initialize variables to track the current note and its length
    current_note = None
    current_length = 0

    # Iterate through the original list
    for pitch in phrase_part:
        if pitch == current_note:
            # Increment the length of the current note
            current_length += 1
        else:
            if current_note is not None:
                # Append the length of the previous note
                note_lengths.append(current_length)
                # Append the unique pitch
                pitches.append(current_note)

            # Start counting a new note
            current_note = pitch
            current_length = 1

    # Append the last note's length and unique pitch
    note_lengths.append(current_length)
    pitches.append(current_note)
    
    # Divide the length by two to represent the number of beats
    note_lengths = [note_length/2 for note_length in note_lengths]
    
    return pitches, note_lengths

#------------------------------------------------------------------------------------------------------------------------------------
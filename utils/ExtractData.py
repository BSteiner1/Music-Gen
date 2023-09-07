import json
import numpy as np

#------------------------------------------------------------------------------------------------------------------------------------

def sort_key(note):
    """
    A function to help with sorting. It obtains the start step (key) of a note (dictionary), or 0 if not present.
    """
    return int(note.get('quantizedStartStep', 0))

#------------------------------------------------------------------------------------------------------------------------------------

def coconet_harmony(path, num_users):
    """
    Extract the four-part harmony output created by CoCoNet

    Args:
        path (str): The path to the JSON file containing the data.
        num_users (int): The number of users' data to process.

    Returns:
        - A list of pitch sequences  of the harmony.
        - A list of start steps for each note in the sequences.
        - A list of end steps for each note in the sequences.
        - A list of the instruments playing each note.
    """
    
    all_harmonies, all_start_steps, all_end_steps, all_instruments = [], [], [], []
    
    with open(path, 'r') as file:
        all_melodies = []
        all_start_steps = []
        all_end_steps = []

        for i in range(num_users):
            line = file.readline()

            # Parse the user's line as JSON data
            parsed_data = json.loads(line)

            # Number of sessions per user
            num_user_sessions = len(parsed_data['output_sequence'])

            # Extract each session for a user
            for session in range(num_user_sessions):
                harmony_notes = parsed_data['output_sequence'][session]['notes']          

                # Sort the input melody by start step (0 if not present)
                sorted_harmony = sorted(harmony_notes, key=sort_key)
                #print(sorted_harmony)

                # Input melody
                harmony_pitches = [note['pitch'] for note in sorted_harmony]
                instruments = [int(note['instrument']) if 'instrument' in note else 0 for note in sorted_harmony]

                # Get the start and end steps of all the notes
                start_steps = [int(note['quantizedStartStep']) if 'quantizedStartStep' in note else 0 for note in sorted_harmony]
                end_steps = [int(note['quantizedEndStep']) if 'quantizedEndStep' in note else 0 for note in sorted_harmony]

                # Add the data to a list
                harmony_tuple = (harmony_pitches, start_steps, end_steps, instruments)
                all_harmonies.append(harmony_tuple)
                
    return all_harmonies    
#------------------------------------------------------------------------------------------------------------------------------------

def sort_phrase(phrase):
    """
    A function that sorts an unordered phrase into a four-bar phrase.
    
    Args:
        - phrase (tuple): a tuple of lists of the form (pitches, note_start_step, note_end_step, instruments).
        
    Returns:
        - A NumPy array of the four-part harmony sorted by time. 
        
    """
    # Assign the lists in the tuple
    pitch_list, note_start_list, note_end_list, instrument_list = phrase

    # Initialise a 4x32 NumPy array filled with zeros
    phrase_array = np.zeros((4, 32), dtype=int)

    # Iterate through the data and fill the array
    for i in range(len(instrument_list)):
        instrument = instrument_list[i]   # Adjust to zero-based index
        pitch = pitch_list[i]
        start_step = note_start_list[i]
        end_step = note_end_list[i]

        # Fill the array with pitch values for the specified range of steps
        phrase_array[instrument, start_step:end_step + 1] = pitch

    return phrase_array

#------------------------------------------------------------------------------------------------------------------------------------

def clean_sorted_phrases(all_harmonies):
    """
    A function to clean sorted phrases.
    We remove any dupliccate phrases or phrases that are not the full length (4 bars/32 quarter notes).
    
    Args:
        - all_harmonies (list): a list of all phrases.
        
    Returns:
        - A list of arrays of sorted phrases.
    """
    unique_melodies = []
    cleaned_and_sorted_phrases = []

    for phrase in all_harmonies:
        if phrase[2][-1] == 32:
            four_part_harmony = sort_phrase(phrase)
            melody = tuple(four_part_harmony[0])
            if melody not in unique_melodies:
                unique_melodies.append(melody)
                cleaned_and_sorted_phrases.append(four_part_harmony)
    
    return cleaned_and_sorted_phrases

#------------------------------------------------------------------------------------------------------------------------------------

def get_cleaned_phrases(path, num_users):
    """
    A function that extracts, sorts, and cleans the phrases.
    
    Args:
        - path (str): The path to the JSON file.
        
    Returns:
        - A list of arrays of suitable phrases to use.
    """
    
    all_four_part_harmonies = coconet_harmony(path, num_users)
    all_cleaned_phrases = clean_sorted_phrases(all_four_part_harmonies)
    
    return all_cleaned_phrases

#------------------------------------------------------------------------------------------------------------------------------------

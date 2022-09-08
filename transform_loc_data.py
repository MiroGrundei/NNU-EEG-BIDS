from eeg_to_bids import EEG_BIDS


# ======================================================================================================================
# LOCALIZER DATA
# ======================================================================================================================

# initiate class
bids = EEG_BIDS(bids_out_dir='E:/crossBL/data_publication_osf/bids_data',
                        bids_proj_name='localiser')

# initiate specific subject
bids.init_sj_dir(1)

# copy bdf of localiser
eeg_file = 'E:/crossBL/data/sub-01/eeg/sub-01_localizer.bdf'
bids.copy_eeg_file(eeg_file=eeg_file)

# create channel localization file ('sub-01_task-localiser_electrodes.tsv')
sfp_file = 'E:\crossBL\data\sub-01\loc\sub-01_crossBL.sfp'
bids.electrode_localisation(sfp_file=sfp_file,
                            write_tsv_file=False)

# create coordinate system file ('sub-01_task-localiser_coordsystem.json')
bids.coordinate_system()

# create eeg system description ('sub-01_task-localiser_eeg.json')
task_name = 'No specific task'
task_description = 'Participants are sequentially presented with uni-modal stimuli a specific modality which can each take one of two possible intensity levels (low/high). ' \
                   'The task was to fixate at the center of the screen and concentrate.'
instructions = 'Please fixate at the center of the screen on the fixation cross and attend the stimulation.'
bids.eeg_description(task_name=task_name,
                     task_description=task_description,
                     instructions=instructions)

# create channel description file ('sub-01_task-localiser_channels.tsv')
trigger_labels = 'trigger with label 128 indicates a tri-modal stimulation. ' \
                 'Please refer to the log file for the exact stimulus identity.' \
                 '126 and 127 indicate starting and stopping of EEG system'
bids.channel_description(trigger_labels)
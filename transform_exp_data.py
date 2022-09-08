from eeg_to_bids import EEG_BIDS


# ======================================================================================================================
# EXPERIMENT DATA
# ======================================================================================================================

# initiate class
bids = EEG_BIDS(bids_out_dir='E:/crossBL/data_publication_osf/bids_data',
                    bids_proj_name='crossbl')

# dataset infos
dataset_name = 'Tri-modal stimulation with probabilistic roving stimulus sequences'
data_type = 'raw'
authors = ['Miro Grundei', 'Felix Blankenburg']
acknowledgement = 'Please cite this data set by referring to the publication'
dataset_doi = 'DOI'
bids.dataset_description(dataset_name=dataset_name,
                             data_type=data_type,
                             authors=authors,
                             acknowledgement=acknowledgement,
                             dataset_doi=dataset_doi)

n_subs = 34
rm_subs = [20, 21]
for sub in [s for s in range(7, n_subs+1) if s not in rm_subs]:

    sub_name = 'sub-{:02d}'.format(sub)
    print(sub_name)

    # initiate specific subject
    bids.init_sj_dir(sub)

    # copy bdf file of experiment ('sub-01_task-localizer_eeg.bdf')
    eeg_file = 'E:/crossBL/data/{}/eeg/{}.bdf'.format(sub_name, sub_name)
    bids.copy_eeg_file(eeg_file=eeg_file)

    # create channel localization file ('sub-01_task-crossbl_electrodes.tsv')
    sfp_file = 'E:\crossBL\data\{}\loc\{}_crossBL.sfp'.format(sub_name, sub_name)
    bids.electrode_localisation(sfp_file=sfp_file,
                                write_tsv_file=True)

    # create coordinate system file ('sub-01_task-crossbl_coordsystem.json')
    bids.coordinate_system()

    # create eeg system description ('sub-01_task-crossbl_eeg.json')
    task_name = 'Retrospective perceptual decision'
    task_description = 'Participants are sequentially presented with simultaneous stimuli in three modalities (Tactile=T, Auditory=A, Visual=V) which can each take one of two possible intensity levels (low/high). ' \
                       'The task is to fixate at the center of the screen with occasional promts to indicate the identity of one of the three modalities (T?/A?/V?) (randomly) of the most recent stimulus. ' \
                       'Participants can reply via a left or a right footpedal for left=low/right/high or left=high/right=low respectively (pressed with right foot only). '
    instructions = 'Please fixate at the center of the screen on the fixation cross and attend the stimulation.' \
                   'Please respond with the foot pedals if the most recent stimulus in the prompted modality (T/A/V) was low or high.'
    bids.eeg_description(task_name=task_name,
                         task_description=task_description,
                         instructions=instructions)

    # create channel description file ('sub-01_task-crossbl_channels.tsv')
    trigger_labels = 'trigger with label 128 indicates a tri-modal stimulation. ' \
                     'Please refer to the log file for the exact stimulus identity.' \
                     '126 and 127 indicate starting and stopping of EEG system'
    bids.channel_description(trigger_labels)

import os
import shutil


class EEG_BIDS:

    def __init__(self, bids_out_dir, bids_proj_name):

        self.out_dir = bids_out_dir
        self.proj_name = bids_proj_name

        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        self.startjson, self.endjson = ['{\n'], ['\n}']

    def dataset_description(self, dataset_name, data_type, authors, acknowledgement, dataset_doi):

        dataset_name = ['\t"Name": "{}",\n'.format(dataset_name)]
        author_list = ['\t"Authors": [\n']
        for author in authors:
            if not author == authors[-1]:
                author_list.append('\t\t\t\t\t\t"{}",\n'.format(author))
            else:
                author_list.append('\t\t\t\t\t\t"{}"'.format(author))
        author_list.append('\n\t\t\t\t\t\t],\n')
        data_type = ['\t"DatasetType": "{}",\n'.format(data_type)]
        bids_version = ['\t"BIDSVersion": "1.4.0",\n']
        acknowledgement = ['\t"HowToAcknowledge": "{}",\n'.format(acknowledgement)]
        doi = ['\t"DatasetDOI": "{}"'.format(dataset_doi)]

        write_lines = self.startjson + dataset_name + bids_version + data_type + author_list + acknowledgement + doi + self.endjson
        with open('{}/dataset_description.json'.format(self.out_dir), 'w') as f:
            for line in write_lines:
                f.write(''.join(line))

    def init_sj_dir(self, subject_number):
        self.subject = 'sub-{:02d}'.format(subject_number)
        self.sj_dir = '{}/{}/eeg'.format(self.out_dir, self.subject)
        if not os.path.exists(self.sj_dir):
            os.makedirs(self.sj_dir)

    def copy_eeg_file(self, eeg_file):
        out_file = os.path.join(self.sj_dir, '{}_task-{}_eeg.bdf'.format(self.subject, self.proj_name))
        shutil.copyfile(eeg_file, out_file)

    def electrode_localisation(self, sfp_file, write_tsv_file=True):
        if not os.path.exists(sfp_file):
            raise ValueError('Cannot find SFP localizer file!')

        fiducials, channels = [], []
        write_lines = ['name\t\t\tx\t\ty\t\tz']
        with open(sfp_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('fid'):
                    fiducials.append(line)
                if not line.startswith('fid'):
                    write_lines.append(line)
                    i = line.find('\t')
                    channels.append(line[0:i])
            write_lines = [line.rstrip() for line in write_lines]
            write_lines = [line for line in write_lines if not line == '']

        self.channels = channels

        fiducials = [fid.rstrip() for fid in fiducials]
        fiducials = [fiducials[0].replace('fidt9\t\t\t', ''),
                     fiducials[1].replace('fidnz\t\t\t', ''),
                     fiducials[2].replace('fidt10\t\t\t', '')]
        self.fiducials = fiducials

        if write_tsv_file:
            with open(os.path.join(self.sj_dir, '{}_task-{}_electrodes.tsv'.format(self.subject, self.proj_name)), 'w') as f:
                f.write('\n'.join(write_lines))

    def eeg_description(self, task_name, task_description, instructions):
        specs = ['\t"TaskName": "{}",\n'.format(task_name), '\t"TaskDescription": "{}",\n'.format(task_description),
                      '\t"Instructions: ""{}",\n'.format(instructions)]
        defaults = ['\t"InstitutionName": "Center for Cognitive Neuroscience Berlin (CCNB)",\n',
                          '\t"SamplingFrequency": {:d},\n'.format(2048),
                          '\t"Manufacturer": "Brain Products",\n',
                          '\t"ManufacturersModelName": "BrainAmp DC",\n',
                          '\t"CapManufacturer": "EasyCap",\n'
                          '\t"CapManufacturersModelName": "M1-ext",\n',
                          '\t"EEGChannelCount": {:d},\n'.format(64),
                          '\t"EOGChannelCount": {:d},\n'.format(4),
                          '\t"ECGChannelCount": {:d},\n'.format(0),
                          '\t"EMGChannelCount": {:d},\n'.format(0),
                          '\t"MiscChannelCount": {:d},\n'.format(0),
                          '\t"TriggerChannelCount": {:d},\n'.format(1),
                          '\t"PowerLineFrequency": {:d},\n'.format(50),
                          '\t"EEGPlacementScheme": "10-20 system",\n',
                          '\t"EEGReference": "CMS and DRL",\n',
                          '\t"EEGGround": "CMS and DRL",\n',
                          '\t"RecordingType": "continuous"']
        write_lines = self.startjson + specs + defaults + self.endjson
        with open('{}/{}_task-{}_eeg.json'.format(self.sj_dir, self.subject, self.proj_name), 'w') as f:
            for line in write_lines:
                f.write(''.join(line))

    def coordinate_system(self):
        specs = ['\t"FiducialsCoordinates": {\n',
                 '\t\t\t\t\t\t\t\t\t\t\t\t\t\t"LPA": [{}],\n'.format(self.fiducials[0]),
                 '\t\t\t\t\t\t\t\t\t\t\t\t\t\t"NAS": [{}],\n'.format(self.fiducials[1]),
                 '\t\t\t\t\t\t\t\t\t\t\t\t\t\t"RPA": [{}],\n'.format(self.fiducials[2]),
                 '\t\t\t\t\t\t\t\t\t\t\t\t\t}']
        defaults = ['\t"EEGCoordinateSystemDescription": "LPA, NASION, RPA",\n',
                    '\t"FiducialsDescription": "Electrodes and fiducials were digitised with ZEBRIS (zebris medical gmbh) '
                    '\tvia electrodes sticked on the left/right pre-auricular points and the nasion",\n']
        write_lines = self.startjson + defaults + specs + self.endjson
        with open('{}/{}_task-{}_coordsystem.json'.format(self.sj_dir, self.subject, self.proj_name), 'w') as f:
            for line in write_lines:
                f.write(''.join(line))

    def channel_description(self, trigger_labels):
        specs = ['Status\tTRIG\t"Trigger labels: {}"'.format(trigger_labels)]

        defaults = ['name\ttype\tdescription\n']
        for channel in self.channels:
            defaults.append('{}\tEEG\n'.format(channel))
        defaults.append(['EXG1\tEOG\n'
                         'EXG2\tEOG\n'
                         'EXG3\tEOG\n'
                         'EXG4\tEOG\n'
                         'EXG5\tEOG\n'
                         'EXG6\tEOG\n'
                         'EXG7\tEOG\n'
                         'EXG8\tEOG\n'])

        write_lines = defaults + specs
        with open('{}/{}_task-{}_channels.tsv'.format(self.sj_dir, self.subject, self.proj_name), 'w') as f:
            for line in write_lines:
                f.write(''.join(line))
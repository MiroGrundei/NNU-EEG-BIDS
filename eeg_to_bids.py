import os
import shutil
import json

class EEG_BIDS:

    def __init__(self, bids_out_dir, bids_proj_name):

        self.out_dir = bids_out_dir
        self.proj_name = bids_proj_name

        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

    def dataset_description(self, dataset_name, data_type, authors, acknowledgement, dataset_doi):

        json_dict = {
            "Name": dataset_name,
            "BIDSVersion": "1.4.0",
            "DatasetType": data_type,
            "Authors": authors,
            "HowToAcknowledge": acknowledgement,
            "DatasetDOI": dataset_doi
        }

        json_object = json.dumps(json_dict, indent=4)
        with open('{}/dataset_description.json'.format(self.out_dir), 'w') as outfile:
            outfile.write(json_object)

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
        write_lines = ['name\tx\ty\tz']
        with open(sfp_file, 'r') as infile:
            lines = infile.readlines()
            for line in lines:
                if line.startswith('fid'):
                    fiducials.append(line.split()[1:])
                if not line.startswith('fid'):
                    line_elements = line.split()
                    channels.append(line_elements[0])
                    write_lines.append('{}\t{}\t{}\t{}'.format(line_elements[0], line_elements[1], line_elements[2], line_elements[3]))

        self.channels = channels
        self.fiducials = fiducials

        if write_tsv_file:
            with open(os.path.join(self.sj_dir, '{}_task-{}_electrodes.tsv'.format(self.subject, self.proj_name)), 'w') as outfile:
                outfile.write('\n'.join(write_lines))

    def eeg_description(self, task_name, task_description, instructions):

        json_dict = {
            "TaskName": task_name,
            "TaskDescription": task_description,
            "Instructions": instructions,
            "InstitutionName": "Center for Cognitive Neuroscience Berlin (CCNB)",
            "SamplingFrequency": 2048,
            "Manufacturer": "Brain Products",
            "ManufacturersModelName": "BrainAmp DC",
            "CapManufacturer": "EasyCap",
            "CapManufacturersModelName": "M1-ext",
            "EEGChannelCount": 64,
            "EOGChannelCount": 4,
            "ECGChannelCount": 0,
            "EMGChannelCount": 0,
            "MiscChannelCount": 0,
            "TriggerChannelCount": 1,
            "PowerLineFrequency": 50,
            "EEGPlacementScheme": "10-20 system",
            "EEGReference": "CMS and DRL",
            "EEGGround": "CMS and DRL",
            "RecordingType": "continuous"
        }

        json_object = json.dumps(json_dict, indent=4)
        with open('{}/{}_task-{}_eeg.json'.format(self.sj_dir, self.subject, self.proj_name), 'w') as outfile:
            outfile.write(json_object)

    def coordinate_system(self):

        json_dict = {
            "FiducialsCoordinates": {
                "LPA": [float(self.fiducials[0][0]), float(self.fiducials[0][1]), float(self.fiducials[0][2])],
                "NAS": [float(self.fiducials[1][0]), float(self.fiducials[1][1]), float(self.fiducials[1][2])],
                "RPA": [float(self.fiducials[2][0]), float(self.fiducials[2][1]), float(self.fiducials[2][2])],
            },
            "EEGCoordinateSystemDescription": "LPA, NASION, RPA",
            "FiducialsDescription": "Electrodes and fiducials were digitised with ZEBRIS (zebris medical gmbh) "
                                    "via electrodes sticked on the left/right pre-auricular points and the nasion"
        }

        json_object = json.dumps(json_dict, indent=4)
        with open('{}/{}_task-{}_coordsystem.json'.format(self.sj_dir, self.subject, self.proj_name), 'w') as outfile:
            outfile.write(json_object)

    def channel_description(self, trigger_labels):

        write_lines_input = ['Status\tTRIG\t"Trigger labels: {}"'.format(trigger_labels)]

        write_lines_defaults = ['name\ttype\tdescription\n']

        for channel in self.channels:
            write_lines_defaults.append('{}\tEEG\n'.format(channel))

        write_lines_defaults.append(['EXG1\tEOG\n'
                                     'EXG2\tEOG\n'
                                     'EXG3\tEOG\n'
                                     'EXG4\tEOG\n'
                                     'EXG5\tEOG\n'
                                     'EXG6\tEOG\n'
                                     'EXG7\tEOG\n'
                                     'EXG8\tEOG\n'])

        write_lines = write_lines_defaults + write_lines_input
        with open('{}/{}_task-{}_channels.tsv'.format(self.sj_dir, self.subject, self.proj_name), 'w') as f:
            for line in write_lines:
                f.write(''.join(line))
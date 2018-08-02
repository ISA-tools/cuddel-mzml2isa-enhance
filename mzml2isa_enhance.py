from isatools import isatab
import sys
import json
import os

input_filepath = sys.argv[1]  # input path to ISA-Tab
output_filepath = sys.argv[2]  # output path to write ISA-Tab
mapping_filepath = sys.argv[3]  # path to mapping json file

ISA = isatab.load(input_filepath)

# only get first assay from first study obj
study = ISA.studies[0]

mapping = {}
with open(mapping_filepath) as fp:
    mapping = json.load(fp)
    for v in mapping.values():
        with open(os.path.join('MTBLS265-no-binary', 'json_meta', v + '.json')) as fp2:
            meta = json.load(fp2)
            ms_protocol = [x for x in study.protocols
                           if 'mass spectrometry' in x.protocol_type.term][0]
            for k2 in meta.keys():
                if not ms_protocol.get_param(k2):
                    ms_protocol.add_param(k2)

for assay in study.assays:
    # get mass spectrometry processes only
    ms_processes = [x for x in assay.process_sequence
                    if x.executes_protocol.protocol_type.term == 'mass spectrometry']
    """
    Check study.protocols for mass spectrometry incase ProtocolParameters
    need to be added based on incoming new metadata from mzML
    """

    # insert the new parameter values
    for k, v in mapping.items():
        try:
            ms_process = [x for x in ms_processes if k in [y.filename for y in x.outputs]][0]
            pvs = ms_process.parameter_values
            print('current pvs:', [x.category.parameter_name.term for x in pvs])
            print('insert pvs here for ', ms_process.name)
            """
            Make sure to check if parameter to add exists, so that the pv is
            updated rather than added to the pvs
            """
            print('new pvs:', [x.category.parameter_name.term for x in pvs])
        except IndexError:
            pass


isatab.dump(ISA, output_filepath)

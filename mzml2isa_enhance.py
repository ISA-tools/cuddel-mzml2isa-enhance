from isatools import isatab
from isatools.model import *
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
        with open(os.path.join('MTBLS265-no-binary', 'json_meta', v + '.json')) as fp2:
            mzml_meta = json.load(fp2)
        try:
            ms_process = [x for x in ms_processes if k in [y.filename for y in x.outputs]][0]
            pvs = ms_process.parameter_values
            print('current pvs:', [x.category.parameter_name.term for x in pvs])
            print('insert pvs here for ', ms_process.name)
            for item in mzml_meta:
                if not ms_process.executes_protocol.get_param(item):
                    print('need to add ', item, ' to protocol')
                    ms_process.executes_protocol.add_param(item)
                param = ms_process.executes_protocol.get_param(item)
                meta_item = mzml_meta[item]
                if 'value' in meta_item.keys():
                    value = meta_item['value']  # check for unit as well
                elif 'name' in meta_item.keys():
                    value = meta_item['name']  # check for ontology annotation
                elif 'entry_list' in meta_item.keys():
                    values = meta_item['entry_list']
                    if 'value' in values[-1].keys():
                        value = values[-1]['value']  # check for unit as well
                    elif 'name' in values[-1].keys():
                        value = values[-1]['name']  # check for ontology annotation
                    else:
                        raise IOError(values[-1])
                else:
                    raise IOError(meta_item)
                pv = ParameterValue(category=param, value=value)
                ms_process.parameter_values.append(pv)
            """
            Make sure to check if parameter to add exists, so that the pv is
            updated rather than added to the pvs
            """
            print('new pvs:', [x.category.parameter_name.term for x in pvs])
        except IndexError:
            pass


isatab.dump(ISA, output_filepath)

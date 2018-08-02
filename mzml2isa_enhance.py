from isatools import isatab
import sys

input_filepath = sys.argv[1]  # input path to ISA-Tab
output_filepath = sys.argv[2]  # output path to write ISA-Tab 

ISA = isatab.load(input_filepath)

# only get first assay from first study obj
study = ISA.studies[0]
assay = study.assays[0]

# get mass spectrometry processes only
ms_processes = [x for x in assay.process_sequence
                if x.executes_protocol.protocol_type.term == 'mass spectrometry']

"""
Check study.protocols for mass spectrometry incase ProtocolParameters
need to be added based on incoming new metadata from mzML
"""

# insert the new parameter values
for ms_process in ms_processes:
    pvs = ms_process.parameter_values

    print('current pvs:', [x.category.parameter_name.term for x in pvs])

    print('insert pvs here')
    """
    Make sure to check if parameter to add exists, so that the pv is
    updated rather than added to the pvs
    """

    print('new pvs:', [x.category.parameter_name.term for x in pvs])

isatab.dump(ISA, output_filepath)

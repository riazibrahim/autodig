import pydig
from app import logger, parser, args
import pandas as pd
from app.utilities import export_to_excel
from datetime import datetime

filename_prepend = datetime.now().strftime("%Y%m%d-%H%M%S")
input_file = args.input_file
output_file = args.output_file
if output_file is None:  # Create file naming if output file name not given
    output_file = '{} - Export Current Query'.format(filename_prepend)

input_list = []
ns_results_df = pd.DataFrame(
    columns=[
        'domain',
        'A',
        'CNAME'])

if input_file is not None:
    logger.debug('Input file detected')
    with open(input_file, 'r') as file:
        logger.debug('Opened input file {}'.format(input_file))
        i = 1
        for item in file.readlines():
            domain = item.rstrip()
            input_list.append(domain)
            i += 1
        logger.info('Finished reading {}'.format(input_file))

logger.info('Removing duplicates out of {} records...'.format(len(input_list)))
unique_domains_list = list(set(input_list))
logger.info('Number of unique domains : {}'.format(len(unique_domains_list)))

i = 1
for domain in unique_domains_list:
    logger.info('\n************************************************************\n'
                'Processing domain number {} : {}\n'
                '************************************************************\n'.format(i, domain))
    ns_result = pydig.query('{}'.format(domain), 'A')
    logger.info('Address record:{}'.format(ns_result))
    cname_result = pydig.query('{}'.format(domain), 'CNAME')
    logger.info('CNAME record:{}'.format(cname_result))
    if len(ns_result) + len(cname_result) == 0:  # both ns_result and cname_result is empty
        logger.info('both A and CNAME are empty')
        ns_results_df = ns_results_df.append({
            'domain': domain,
            'A': 'none',
            'CNAME': 'none'},
            ignore_index=True)
        continue
    if len(ns_result) != 0:  # ns result not empty
        for a_record in ns_result:
            if len(cname_result) != 0:  # ns result not empty and cname result not empty
                for cname in cname_result:
                    ns_results_df = ns_results_df.append({
                        'domain': domain,
                        'A': a_record,
                        'CNAME': cname},
                        ignore_index=True)
            else:  # ns result not empty and cname result is empty
                ns_results_df = ns_results_df.append({
                    'domain': domain,
                    'A': a_record,
                    'CNAME': 'none'},
                    ignore_index=True)
    else:  # ns result is empty
        for cname in cname_result:
            ns_results_df = ns_results_df.append({
                'domain': domain,
                'A': 'none',
                'CNAME': cname},
                ignore_index=True)
    i += 1
logger.info('Exporting to excel...')
export_to_excel(dataframe=ns_results_df, outfile='{} - {}'.format(filename_prepend, output_file),
                sheet_name='NS results')

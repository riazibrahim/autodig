import pandas as pd
from pandas import ExcelWriter
from app import logger, args
import os
import sys
import random


def export_to_excel(dataframe, outfile, **kwargs):
    logger.debug('Entered :: export_to_excel')
    logger.debug('Check if sheet_name is given')
    sheet_name = kwargs.get('sheet_name', None)
    logger.debug('Check if sheet_name is given')

    logger.debug('Checking if dataframe is None')
    if len(dataframe) > 0:  # Check if dataframe has any data in it
        try:
            filename = 'outputs/{}.xlsx'.format(outfile)
            if os.path.exists(filename):
                logger.debug(
                    'Output file already exists. Appending results')  # TODO: Add to existing sheet, currently it is another sheet
                with ExcelWriter(filename, mode='a') as writer:
                    if sheet_name is not None:
                        dataframe.to_excel(writer, sheet_name=sheet_name)
                    else:
                        dataframe.to_excel(writer)
                    logger.info('Added results to {}.xlsx in outputs folder\n'.format(outfile))
            else:
                if sheet_name is not None:
                    dataframe.to_excel('outputs/{}.xlsx'.format(outfile), sheet_name=sheet_name)
                else:
                    dataframe.to_excel('outputs/{}.xlsx'.format(outfile))
                logger.info('Generated {}.xlsx in outputs folder\n'.format(outfile))
        except Exception as e:
            logger.info('Some issue while generating the output : \n{}'.format(e))
            sys.exit('Some issue. Exiting!')
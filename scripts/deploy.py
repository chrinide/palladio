#!/usr/bin/env python
"""Script for easy deployment."""

import os
import shutil
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Palladio script for '
                                                 'deploying.')
    # If no argument is given, assume installation in home folder
    parser.add_argument('deployment_folder', nargs='?',
                        default=os.path.expanduser("~"),
                        help="Specify the deployment folder")
    parser.add_argument("-s", "--sample-data",
                        action="store_true", dest="sample_data", default=False,
                        help="Also copy sample data to the deployment folder")
    args = parser.parse_args()

    deployment_folder = os.path.abspath(args.deployment_folder)
    # The folder where scripts are located
    scripts_folder = os.path.dirname(os.path.realpath(__file__))

    # COPY PALLADIO LIBRARY FOLDER
    shutil.copytree(os.path.join(scripts_folder, "..", 'palladio'),
                    os.path.join(deployment_folder, 'palladio'))

    # COPY SCRIPTS
    shutil.copy(os.path.join(scripts_folder, "pd_run.py"),
                os.path.join(deployment_folder, "pd_run.py"))
    shutil.copy(os.path.join(scripts_folder, "pd_analysis.py"),
                os.path.join(deployment_folder, "pd_analysis.py"))
    shutil.copy(os.path.join(scripts_folder, "pd_test.py"),
                os.path.join(deployment_folder, "pd_test.py"))
    shutil.copy(os.path.join(scripts_folder, "clean_palladio_libs.sh"),
                os.path.join(deployment_folder, "clean_palladio_libs.sh"))

    # IF REQUESTED, COPY SAMPLE DATA
    if args.sample_data:
        shutil.copytree(os.path.join(scripts_folder, "..", 'example'),
                        os.path.join(deployment_folder,
                                     'palladio_example'))

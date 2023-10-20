# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                               copy_images.py
#        Copies the images of a given field to the calibration directory
# ******************************************************************************

"""
Copies fiels images from a database to the calibration directory.

The S-PLUS field is given as the first command line argument. Configurations
are set in the config file, given as the second command line argument.

--------------------------------------------------------------------------------
   FUNCTIONS:
--------------------------------------------------------------------------------

check_for_fz_images()
check_for_fits_images()
get_images_from_directory()
get_images_from_ssh()
unpack_images()

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
Ideally this script should only be run through the pipeline.py script.

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 copy_images.py *field_name* *config_file*

----------------
"""

################################################################################
# Import external packages

import os
import sys

steps_path = os.path.split(__file__)[0]
pipeline_path = os.path.split(steps_path)[0]
spluscalib_path = os.path.split(pipeline_path)[0]

sys.path.append(spluscalib_path)

################################################################################
# Import spluscalib packages

from spluscalib import utils as ut

################################################################################
# Read parameters

field     = sys.argv[1]
conf_file = sys.argv[2]

conf = ut.pipeline_conf(conf_file)

if conf["images_sshpass"]:
    sshpass = sys.argv[3]

################################################################################
# Get directories

field_path = os.path.join(conf['run_path'], field)
images_path = os.path.join(field_path, 'Images')
log_path = os.path.join(images_path, 'logs')

################################################################################
# Create Images directory

ut.makedir(field_path)
ut.makedir(images_path)
ut.makedir(log_path)

################################################################################
# Initiate log file

log_file_name = os.path.join(log_path, 'copy_images.log')
log_file_name = ut.gen_logfile_name(log_file_name)
log_file = os.path.join(images_path, log_file_name)

with open(log_file, "w") as log:
    log.write("")

################################################################################
# Begin script

############################################################################
# Copy fz images

# ***************************************************
#    Check if images already exist in run_path
# ***************************************************

def check_for_fz_images():

    # Check for .fz files
    all_fz = True

    for filt in conf['filters']:
        if conf['images_sshpass']:
            image_name = f'{field}_{filt}_swp.fits.fz'
        else:
            image_name = f'{field}_{filt}_swp.fz'

        image_fz = os.path.join(images_path, image_name)
        if not os.path.exists(image_fz):
            all_fz = False

        # Check for weight image
        if conf["use_weight"]:
            if conf['images_sshpass']:
                weight_name = f'{field}_{filt}_swpweight.fits.fz'
                weight_fz = os.path.join(images_path, weight_name)
            else:
                weight_name = f'{field}_{filt}_swpweight.fz'
                weight_fz = os.path.join(images_path, weight_name)

            if not os.path.exists(weight_fz):
                all_fz = False

    return all_fz

has_all_fz = check_for_fz_images()


# ***************************************************
#    Check if images already exist in run_path
# ***************************************************

def check_for_fits_images():
    # Check for .fits files
    all_fits = True

    for filt in conf['filters']:
        image_name = f'{field}_{filt}_swp.fits'
        image_fits = os.path.join(images_path, image_name)

        if not os.path.exists(image_fits):
            all_fits = False

        # Check for weight image
        if conf["use_weight"]:
            weight_name = f'{field}_{filt}_swpweight.fits'
            weight_fits = os.path.join(images_path, weight_name)

            if not os.path.exists(weight_fits):
                all_fits = False

    return all_fits

has_all_fits = check_for_fits_images()


# ***************************************************
#    Get images from a directory or...
# ***************************************************

def get_images_from_directory():

    for filt in conf['filters']:

        image_name = f'{field}_{filt}_swp.fz'
        image_db_fz = os.path.join(conf['path_to_images'], field,
                                   image_name)
        image_fz = os.path.join(images_path, image_name)

        if not os.path.exists(image_fz):

            ut.printlog(f"Copying image {image_name}", log_file,
                        color="yellow")

            cmd = f"cp {image_db_fz} {images_path}"
            ut.printlog(cmd, log_file, color="green")
            os.system(cmd)

        else:
            ut.printlog(f"Image {image_fz} already exists",
                        log_file, color="white", attrs=["dark"])

        if conf['use_weight']:

            weight_name = f'{field}_{filt}_swpweight.fz'
            weight_db_fz = os.path.join(conf['path_to_images'], field,
                                   weight_name)
            weight_fz = os.path.join(images_path, weight_name)

            if not os.path.exists(weight_fz):
                cmd = f"cp {weight_db_fz} {images_path}"
                ut.printlog(cmd, log_file, color="green")
                os.system(cmd)

            else:
                ut.printlog(f"Image {weight_fz} already exists",
                            log_file, color="white", attrs=["dark"])


if not (has_all_fz or has_all_fits):
    if not conf["images_sshpass"]:
        get_images_from_directory()


# ***************************************************
#    Get images from ssh
# ***************************************************

def get_images_from_ssh():

    sshuser = conf["sshpass_user"]
    sship = conf["sshpass_ip"]
    sshpath = conf["sshpass_path"]

    for filt in conf['filters']:

        # Deal with JYPE images ending with .fz and MAR ending with .fits.fz
        if sship == '10.180.3.152':
            image_name = f'{field}_{filt}_swp.fits.fz'
        elif sship == '10.180.3.104':
            image_name = f'{field}_{filt}_swp.fz'
        else:
            image_name = f'{field}_{filt}_swp.fits.fz'

        image_db_fz = os.path.join(sshpath, field, image_name)
        image_fz = os.path.join(images_path, image_name)

        new_image_fz = image_fz.replace(".fits.fz", ".fz")

        if not os.path.exists(new_image_fz):

            ut.printlog(f"Copying by sshpass image {image_name}",
                        log_file, color="yellow")

            cmd = f"sshpass -p '{sshpass}' scp {sshuser}@{sship}:{image_db_fz} "
            cmd += f"{images_path}"

            cmd_hidepass = cmd.replace(sshpass, "*" * len(sshpass))
            ut.printlog(cmd_hidepass, log_file, color="green")
            os.system(cmd)

            cmd = f"mv {image_fz} {new_image_fz}"
            ut.printlog(cmd, log_file, color="green")
            os.system(cmd)

        else:
            ut.printlog(f"Image {image_fz} already exists",
                        log_file, color="white", attrs=["dark"])


        if conf['use_weight']:

            # Deal with JYPE images ending with .fz and MAR ending with .fits.fz
            if sship == '10.180.3.152':
                weight_name = f'{field}_{filt}_swpweight.fits.fz'
            elif sship == '10.180.3.104':
                weight_name = f'{field}_{filt}_swpweight.fz'
            else:
                weight_name = f'{field}_{filt}_swpweight.fits.fz'

            weight_db_fz = os.path.join(sshpath, field, weight_name)
            weight_fz = os.path.join(images_path, weight_name)

            new_weight_fz = weight_fz.replace(".fits.fz", ".fz")

            if not os.path.exists(new_weight_fz):

                cmd = f"sshpass -p '{sshpass}' scp "
                cmd += f"{sshuser}@{sship}:{weight_db_fz} "
                cmd += f"{images_path}"

                cmd_hidepass = cmd.replace(sshpass, "*" * len(sshpass))
                ut.printlog(cmd_hidepass, log_file, color="green")
                os.system(cmd)

                cmd = f"mv {weight_fz} {new_weight_fz}"
                ut.printlog(cmd, log_file, color="green")
                os.system(cmd)

            else:
                ut.printlog(f"Image {weight_fz} already exists",
                            log_file,
                            color="white", attrs=["dark"])

if not (has_all_fz or has_all_fits):
    if conf["images_sshpass"]:
        get_images_from_ssh()

# ***************************************************
#    Unpack images
# ***************************************************
def unpack_images():

    for filt in conf['filters']:

        image_name = f'{field}_{filt}_swp.fz'
        image_fz = os.path.join(images_path, image_name)
        image_fits = image_fz.replace(".fz", ".fits")

        if not os.path.exists(image_fits):

            ut.printlog(f"Unpacking image {image_fz}", log_file,
                        color="yellow")
            ut.fz2fits(image_fz)

        else:
            ut.printlog(f"Image {image_fits} already exists",
                        log_file, color="white", attrs=["dark"])

        if conf['use_weight']:
            weight_fz = image_fz.replace(".fz", "weight.fz")
            weight_fits = weight_fz.replace(".fz", ".fits")

            if not os.path.exists(weight_fits):
                ut.printlog(f"Unpacking weight {weight_fz}",
                            log_file, color="yellow")
                ut.fz2fits(weight_fz)

            else:
                ut.printlog(f"Image {weight_fits} already exists",
                            log_file, color="white", attrs=["dark"])

if conf["unpack_images"] and not has_all_fits:
    unpack_images()
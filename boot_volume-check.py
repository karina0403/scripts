#!/usr/bin/env python3

import oci
import argparse
import datetime

verboose = False

def printtimestamp(message, is_verboose: bool = False):
    is_print = (is_verboose is False) or (verboose is True)
    if is_print:
        ct = datetime.datetime.now()
        print(f"{ct}:{message}")


parser = argparse.ArgumentParser(
    description="Script to find orphan Boot Volumes and delete them"
)
parser.add_argument("--profile", help="OCI Profile")
parser.add_argument("--compartment_id", help="Compartment ID")
parser.add_argument("--verboose", help="Show Additional output logs", default=False)

args = parser.parse_args()

if args.profile is None:
    profile = "TOGET"
else:
    profile = args.profile

if args.compartment_id is None:
    compartment_id = "TOGET"
else:
    compartment_id = args.compartment_id

if args.verboose is None:
    verboose = False
else:
    verboose = args.verboose

try:
    config_oci = oci.config.from_file(profile_name=profile)
    printtimestamp("Using profile: " + profile)
except:
    config_oci = oci.config.from_file()
    printtimestamp("Using profile DEFAULT")

blockstorageClient = oci.core.BlockstorageClient(config_oci)
computeClient = oci.core.ComputeClient(config_oci)

boot_volumes_list = blockstorageClient.list_boot_volumes(
    compartment_id=compartment_id
    ).data

to_be_deleted_count = 0

for boot_volume in boot_volumes_list:
    boot_volume_id = boot_volume.id
    boot_volume_display_name = boot_volume.display_name

    boot_volume_to_be_deleted = True
    boot_volume_to_be_deleted_reason = "no attachments"

    availability_domain_name = boot_volume.availability_domain

    printtimestamp(f"Searching attachments for boot volume: {boot_volume_id} \"{boot_volume_display_name}\" in availability domain: \"{availability_domain_name}\"", is_verboose=True)

    boot_volume_attachments_list = computeClient.list_boot_volume_attachments(
        availability_domain=availability_domain_name,
        compartment_id=compartment_id,
        boot_volume_id=boot_volume_id).data

    printtimestamp(f"Found attachments: {boot_volume_attachments_list}", is_verboose=True)

    for attachment in boot_volume_attachments_list:
        attachment_lifecycle_state = attachment.lifecycle_state
        boot_volume_to_be_deleted_reason = f"attached to instance \"{attachment.instance_id}\" with lifecycle_state: \"{attachment_lifecycle_state}\""

        if attachment_lifecycle_state == "ATTACHED":
            boot_volume_to_be_deleted = False
            continue

    if boot_volume_to_be_deleted:
        printtimestamp(f"Found boot volume: {boot_volume_id} \"{boot_volume_display_name}\". Reason: {boot_volume_to_be_deleted_reason}")
        to_be_deleted_count += 1

printtimestamp(f"Total boot volumes to be deleted: {to_be_deleted_count}")

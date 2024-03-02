GrabberFirmwareUpdater
======================

The GrabberFirmwareUpdater tool allows you to check if a firmware update for a Basler Interface Card or frame grabber is available
and how to perform the update if necessary.

To get a summary of all available options and parameters, call the tool with the --help option:

GrabberFirmwareUpdater --help

Firmware Version
----------------

The firmware version is separated into three parts:

* The **dynamic** firmware version is given in the form of a major and minor version (for example: 1.0)
* The **static** version starts with S and is given in the form of a major and minor version (for example: S1.2)
* The **PCIe core** version starts with P and is given in the form of a major version (for example: P0)

The dynamic firmware is fully integrated in the applets and is not part of the flashed firmware. This is why the dynamic firmware
version is omitted from the firmware flash files. In the GrabberFirmwareUpdater, only the static and PCIe core versions are used.

Applets are only compatible with a specific static version. Usually, with each pylon installation, the firmware update file matching
the version required by the applets is provided.

The PCIe core depends on the static version like the applet. It starts with 0 for each new static version. For example, updating
from S1.1 P1 to S1.2 P0 does not mean downgrading the PCIe core version.

NOTE: Unlike with the previous generation of Basler frame grabbers (the microEnable 5 ironman and marathon series), applets aren't
flashed on the board. Applets can be loaded as long as they match the installed firmware version.

The firmware update is partitioned and provides two separate partitions to make updating the firmware safer. Should anything go wrong
during the firmware update process, e.g., due to a power failure, only one partition can be compromised. The other partition will
automatically be used instead.

Checking for Firmware Updates
-----------------------------

To check for available updates, just run the GrabberFirmwareUpdater tool without any options and parameters:

GrabberFirmwareUpdater

The GrabberFirmwareUpdater tool will print a short message if any boards require firmware updates.

Updating the Firmware
---------------------

To update the frame grabber firmware, use the --update option:

GrabberFirmwareUpdater --update

NOTE: Never close the window running GrabberFirmwareUpdater, don't press Ctrl-C or interrupt the update process in any other way,
and don't shut down or power off your computer before all updates are finished.

During the update process, activity and progress is shown with a simple progress bar. GrabberFirmwareUpdater will perform all
updates automatically.

When the update process is finished, a short summary is shown and a message is printed, requesting you to power off the computer.
Because the firmware is loaded during the power-up phase, activating the updated firmware requires a power-cycle of the computer.

Downgrading to an Older Firmware Version
----------------------------------------

If a specific older firmware version is required for a frame grabber, the parameters --board <id>, --file <path> and the option --force
are needed in combination:

GrabberFirmwareUpdater --board 0 --file ..\firmware\CXP12-IC-1C\firmware.hap --force

The output of GrabberFirmwareUpdater is the same as during the update process.

NOTE: Downgrading the frame grabber firmware is only possible using a pylon version that provides applets matching the static version
installed on the frame grabber.

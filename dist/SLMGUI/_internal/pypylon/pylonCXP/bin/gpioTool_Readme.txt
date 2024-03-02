gpioTool
========

With gpioTool, you can configure the physical properties of the trigger signals received or sent by a Basler Interface Card
or frame grabber:

- You can configure the input lines to receive single-ended or differential signals.
- You can configure the input lines to operate in pull-up or pull-down mode.
- You can specify whether output signals should be inverted.

Options
-------

The following options are available:

gpioTool -b [board_index]
         -g
         -v
         -s [bank]:[settings]
         -h

-b [board_index]
Specify which interface card or frame grabber in your system you want to address. This parameter is mandatory for all
options except -h.
The value range of [board_index] is the index numbers of all boards installed in your system. If you only have one board
in your system, set [board_index] to 0.

-b [board_index] -g
Show the current GPIO bank settings of the board specified.

-b [board_index] -v
Show the current GPIO bank settings with verbose output.

-b [board_index] -s [bank]:[settings]
Configure the GPIO bank on the board specified. [bank] specifies the index number of the GPIO bank. [settings] configures
the settings. See below.

-h
Show help.

Settings
--------

For the [settings] part in -b [board_index] -s [bank]:[settings], the following settings are available:

| Setting          | Value | Result                                                       |
| ---------------- | ----- | ------------------------------------------------------------ |
| [signal]         | se    | Configures the input lines to receive single-ended signals.  |
| [signal]         | ds    | Configures the input lines to receive differential signals.  |
| [pull-up-down]   | pu    | Configures the input lines to operate in pull-up mode.[^1]   |
| [pull-up-down]   | pd    | Configures the input lines to operate in pull-down mode.     |
| [inversion]      | ni    | Disables inversion for the output lines.                     |
| [inversion]      | in    | Enables inversion for the output lines.                      |

[^1]: In most applications, you will need to configure this mode.

You must enter the settings in the following format: [signal],[pull-up-down],[inversion]. Example: ds,pu,ni

Alternatively, you can set settings to default. This resets the configuration of a GPIO bank (see below).

Example
-------

gpioTool -b 0 -s 0:ds,pu,ni

This command configures a board as follows:

- -b 0: Configure the GPIOs on board 0.
- -s: Start the actual configuration.
- 0:: Configure GPIO bank 0 (front GPIO).
- ds,pu,ni: Configure the front GPIO to receive differential signals (ds), to work in pull-up mode (pu),
and to send the outgoing signals not inverted (ni).

Resetting the Configuration
---------------------------

To reset a board and GPIO bank to the default settings, start gpioTool with [settings] set to default:

gpioTool -b [board_index] -s [bank]:default

Example: gpioTool -b 0 -s 0:default

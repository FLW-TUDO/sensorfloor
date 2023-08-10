# rfDualModeTx
---

### SysConfig Notice

All examples will soon be supported by SysConfig, a tool that will help you 
graphically configure your software components. A preview is available today in 
the examples/syscfg_preview directory. Starting in 3Q 2019, with SDK version 
3.30, only SysConfig-enabled versions of examples will be provided. For more 
information, click [here](http://www.ti.com/sysconfignotice).

-------------------------

Project Setup using the System Configuration Tool (SysConfig)
-------------------------
The purpose of SysConfig is to provide an easy to use interface for configuring 
drivers, RF stacks, and more. The .syscfg file provided with each example 
project has been configured and tested for that project. Changes to the .syscfg 
file may alter the behavior of the example away from default. Some parameters 
configured in SysConfig may require the use of specific APIs or additional 
modifications in the application source code. More information can be found in 
SysConfig by hovering over a configurable and clicking the question mark (?) 
next to it's name.

Example Summary
---------------
In this example you will learn how to setup multi-mode radio driver to send 
data to a receiver. The Dual Mode TX example configures a BLE and proprietary
radio mode to transmit the same random packet. The packet is first 
transmitted using the proprietary radio driver, then the same packet is then
transmitted  500 ms later using the BLE radio driver. This example is meant 
to be used with the Dual Mode RX example or Smart RF Studio. For every proprietary 
packet sent Board_PIN_LED2 is turned on and Board_PIN_LED1 is turned off. 
When the same BLE packet is sent, Board_PIN_LED2 is turned off and Board_PIN_LED1
is turned on. The frequency and other RF settings can be modified using SmartRF Studio.

Peripherals Exercised
---------------------
* `Board_PIN_LED2` - Blinking indicates a successful transmission of the 
proprietary packet (500 ms)
* `Board_PIN_LED1` - Blinking indicates a successful transmission of the 
BLE packet (500 ms)

Resources & Jumper Settings
---------------------------
> If you're using an IDE (such as CCS or IAR), please refer to Board.html in your project
directory for resources used and board-specific jumper settings. Otherwise, you can find
Board.html in the directory &lt;SDK_INSTALL_DIR&gt;/source/ti/boards/&lt;BOARD&gt;.

Example Usage
-------------
The use of this example will require two launchpads,  one running rfDualModeTx (`Board_1`)
and another running rfDualModeRx (`Board_2`). Run Board_2 first, followed by Board_1. 
Board_1 is set to alternate between transmitting a proprietary packet and BLE packet 
every 500 ms. Board_PIN_LED2 on Board_1 will turn on when a proprietary packet is 
transmitted. Board_PIN_LED2 on Board_2 will turn on to indicate the packet was successfully
received. On Board_1, Board_PIN_LED2 will turn off and Board_PIN_LED1 will turn on to 
indicate the BLE packet was successfully sent. The behavior on Board_2 will mimic the 
LEDs on Board_1 with Board_PIN_LED2 turning off and Board_PIN_LED1 turning on. This indicates
the BLE packet was successfully received and matches the proprietary packet. The cycle 
will then restart with the new packet. 

If a packet is missed from the receiver, the current status of the lights will remain. The extended
duration that the LED is on ( > 500 ms) indicates that the receiver is stuck in its previous state 
(see [figure 1]). The next proprietary will cause the receiver and transmitter to resync. 

![missed_prop_packet_ref][figure 1]

If the BLE packet is received, but the packet is not the same as the proprietary packet both 
Board_PIN_LED1 and Board_PIN_LED2 will turn on (see [figure 2]). This means both a proprietary packet and BLE packet
were received but interference or a missed packet has caused the transmitter and receiver to become 
out of sync. If this happens the receiver and transmitter will automatically resync with the 
next proprietary packet. 

![missed_ble_packet_ref][figure 2]

Note for IAR users: When using the CC1310DK, the TI XDS110v3 USB Emulator must
be selected. For the CC1310_LAUNCHXL, select TI XDS110 Emulator. In both cases,
select the cJTAG interface.


[figure 1]:rfDualMode_MissedPropPacket.png "Missed Prop Packet"
[figure 2]:rfDualMode_MissedBlePacket.png "Missed BLE Packet"
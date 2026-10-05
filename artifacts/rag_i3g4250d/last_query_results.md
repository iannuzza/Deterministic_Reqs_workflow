# RAG Query Results\n\n- Timestamp: 2026-07-23 12:42:49\n- Query: shall OR must OR requirement\n- Top K: 8\n- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/MEMS_3axis_gyro/artifacts/rag_i3g4250d/rag_index.sqlite\n\n## Result 1\n- chunk_id: 70\n- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/MEMS_3axis_gyro/specs/i3g4250d.pdf\n- page: 41\n- chunk_index: 1\n- score: -3.561696\n\n```text\nIMPORTANT NOTICE â€“ READ CAREFULLY
STMicroelectronics NV and its subsidiaries (â€œSTâ€) reserve the right to make changes, corrections, enhancements, modifications, and improvements to ST 
products and/or to this document at any time without notice. Purchasers should obtain the latest relevant information on ST products before placing orders. ST 
products are sold pursuant to STâ€™s terms and conditions of sale in place at the time of order acknowledgment.
Purchasers are solely responsible for the choice, selection, and use of ST products and ST assumes no liability for application assistance or the design of 
purchasersâ€™ products.
No license, express or implied, to any intellectual property right is granted by ST herein.
Resale of ST products with provisions different from the information set forth herein shall void any warranty granted by ST for such product.
ST and the ST logo are trademarks of ST. For additional information about ST trademarks, refer to www.st.com/trademarks. All other product or service names 
are the property of their respective owners.
Information in this document supersedes and replaces information previously supplied in any prior versions of this document.
Â© 202\n```\n\n## Result 2\n- chunk_id: 26\n- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/MEMS_3axis_gyro/specs/i3g4250d.pdf\n- page: 17\n- chunk_index: 1\n- score: -3.032312\n\n```text\nData transfer with acknowledge is mandatory. The transmitter must release the SDA line during the acknowledge 
pulse. The receiver must then pull the data line low so that it remains stable low during the high period of the 
acknowledge clock pulse. A receiver that has been addressed is obliged to generate an acknowledge after each 
byte of data received.
The IÂ²C embedded in the I3G4250D behaves like a slave device, and the following protocol must be adhered to. 
After the start (ST) condition, a slave address is sent. Once a slave acknowledge (SAK) has been returned, an 8-
bit subaddress is transmitted. The 7 LSb represent the actual register address while the MSb enables address 
auto-increment. If the MSb of the SUB field is 1, the SUB (register address) is automatically incremented to allow 
multiple data read/write.
The slave address is completed with a read/write bit. If the bit is 1 (read), a repeated start (SR) condition must be 
issued after the two subaddress bytes; if the bit is 0 (write) the master transmits to the slave with the direction 
unchanged. The following table describes how the SAD+read/write bit pattern is composed, listing all the possible 
configurations.\n```\n\n## Result 3\n- chunk_id: 11\n- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/MEMS_3axis_gyro/specs/i3g4250d.pdf\n- page: 8\n- chunk_index: 1\n- score: -2.967409\n\n```text\n2.4.2 IÂ²C - inter IC control interface
Subject to general operating conditions for Vdd and Top.
Table 7. IÂ²C slave timing values
Symbol Parameter
IÂ²C standard mode(1) IÂ²C fast mode(1)
Unit
Min. Max. Min. Max.
f(SCL) SCL clock frequency 0 100 0 400 kHz
tw(SCLL) SCL clock low time 4.7 1.3
Âµs
tw(SCLH) SCL clock high time 4.0 0.6
tsu(SDA) SDA setup time 250 100 ns
th(SDA) SDA data hold time 0 3.45 0 0.9 Âµs
th(ST) START condition hold time 4 0.6
Âµs
tsu(SR) Repeated START condition setup time 4.7 0.6
tsu(SP) STOP condition setup time 4 0.6
tw(SP:SR) Bus free time between STOP and START condition 4.7 1.3
 
1. Data based on standard IÂ²C protocol requirement, not tested in production.
 
Figure 5. IÂ²C slave timing diagram
S D A  
SC L 
t f( S D A )
t s u (S P )
t w( S C L L )
t s u (S D A )t r (S D A )
t s u (S R )
t h( S T ) t w( S C L H )
t h (S D A )
t r (S C L ) t f(S C L )
t w (S P :S R )
S T A R T  
R EP E A T E D
S T A R T  
S T O P
S T A R T
Note: Measurement points are done at 0.2Â·Vdd_IO and 0.8Â·Vdd_IO for both ports.
I3G4250D
Mechanical and electrical characteristics
DS10938 - Rev 3 page 8/41\n```\n\n## Result 4\n- chunk_id: 28\n- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/MEMS_3axis_gyro/specs/i3g4250d.pdf\n- page: 17\n- chunk_index: 3\n- score: -2.754293\n\n```text\ns transferred 
per transfer is unlimited. Data is transferred with the most significant bit (MSb) first. If a receiver cannot receive 
another complete byte of data until it has performed some other function, it can hold the clock line SCL low to 
force the transmitter into a wait state. Data transfer only continues when the receiver is ready for another byte and 
releases the data line. If a slave receiver does not acknowledge the slave address (that is, it is not able to receive 
because it is performing some real-time function) the data line must be left high by the slave. The master can then 
abort the transfer. A low to high transition on the SDA line while the SCL line is high is defined as a stop condition. 
Each data transfer must be terminated by the generation of a stop (SP) condition.
In order to read multiple bytes, it is necessary to assert the most significant bit of the subaddress field. In other 
words, SUB(7) must be equal to 1, while SUB(6-0) represents the address of the first register to be read.
In the presented communication format, MAK is â€œmaster acknowledgeâ€ and NMAK is â€œno master acknowledgeâ€.
I3G4250D
Digital interfaces
DS10938 - Rev 3 page 17/41\n```\n\n## Result 5\n- chunk_id: 19\n- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/MEMS_3axis_gyro/specs/i3g4250d.pdf\n- page: 14\n- chunk_index: 1\n- score: -2.713396\n\n```text\n3.2.4 Retrieving data from FIFO
FIFO data is read from the OUT_X, OUT_Y, and OUT_Z registers. When the FIFO is in stream, bypass or FIFO 
mode, a read operation to the OUT_X, OUT_Y or OUT_Z registers provides the data stored in the FIFO. Each 
time data is read from the FIFO, the oldest pitch, roll, and yaw data are placed in the OUT_X, OUT_Y and OUT_Z 
registers, and both single read and read-burst (X, Y & Z with auto-incremental address) operations can be used. 
In read-burst mode, when data included in OUT_Z_H is read, the system again starts to read information from 
OUT_X_L.
The read from FIFO may be executed either in synchronous or asynchronous mode. For correct data acquisition, 
the following steps must be respected:
1. If reading is synchronous, all data should be acquired within one ODR cycle
2. If reading is asynchronous, an appropriate FIFO access sequence must be applied:
a. Single read from register 28h
b. Multiread: sequentially reading 2Ah, 2Bh, 2Ch, 2Dh, 28h, 29h
c. This procedure must be repeated for each dataset (X/Y/Z) in the FIFO:
-FSS times, if FSS â‰¤ 31
-(FSS + 1) times, if (FSS = 31) & (OVR = 1)
The following figure illustrates the correct sequence with a fl\n```\n\n## Result 6\n- chunk_id: 35\n- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/MEMS_3axis_gyro/specs/i3g4250d.pdf\n- page: 22\n- chunk_index: 2\n- score: -2.209561\n\n```text\n0101 00000000
INT1_THS_ZH R/W 36 011 0110 00000000
INT1_THS_ZL R/W 37 011 0111 00000000
INT1_DURATION R/W 38 011 1000 00000000
Reserved registers must not be changed. Writing to those registers may change calibration data and therefore 
lead to device malfunction.
The content of the registers that are loaded at boot should not be changed. They contain the factory calibration 
values. Their content is automatically restored when the device is powered up.
I3G4250D
Output register mapping
DS10938 - Rev 3 page 22/41\n```\n\n## Result 7\n- chunk_id: 23\n- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/MEMS_3axis_gyro/specs/i3g4250d.pdf\n- page: 16\n- chunk_index: 1\n- score: -1.655304\n\n```text\n5 Digital interfaces
The registers embedded in the I3G4250D may be accessed through both the IÂ²C and SPI serial interfaces. The 
latter may be software-configured to operate either in 3-wire or 4-wire interface mode.
The serial interfaces are mapped to the same pins. To select/exploit the IÂ²C interface, the CS line must be tied 
high (that is, connected to Vdd_IO).
Table 10. Serial interface pin description
Pin name Pin description
CS
Enable SPI
IÂ²C/SPI mode selection (1: SPI idle mode / IÂ²C communication enabled;
0: SPI communication mode / IÂ²C disabled)
SCL/SPC
IÂ²C serial clock (SCL)
SPI serial port clock (SPC)
SDA/SDI/SDO
IÂ²C serial data (SDA)
SPI serial data input (SDI)
3-wire interface serial data output (SDO)
SDO
SPI serial data output (SDO)
IÂ²C least significant bit of the device address
5.1 IÂ²C serial interface
The I3G4250D IÂ²C is a bus slave. The IÂ²C is employed to write data to registers whose content can also be read 
back.
The relevant IÂ²C terminology is given in the table below.
Table 11. IÂ²C terminology
Term Description
Transmitter The device that sends data to the bus
Receiver The device that receives data from the bus
Master The device that initiates a transfer, gen\n```\n\n## Result 8\n- chunk_id: 38\n- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/MEMS_3axis_gyro/specs/i3g4250d.pdf\n- page: 25\n- chunk_index: 1\n- score: -1.644988\n\n```text\n7.3 CTRL_REG2 (21h)
Table 23. CTRL_REG2 register
0(1) 0(1) HPM1 HPM0 HPCF3 HPCF2 HPCF1 HPCF0
 
1. Value loaded at boot. This value must not be changed.
 
Table 24. CTRL_REG2 description
HPM1-HPM0
High-pass filter mode selection. Default value: 00
Refer to Table 25
HPCF3-HPCF0
High-pass filter cutoff frequency selection
Refer to Table 26
Table 25. High-pass filter mode configuration
HPM1 HPM0 High-pass filter mode
0 0 Normal mode (reset by reading the REFERENCE/DATACAPTURE (25h) register)
0 1 Reference signal for filtering
1 0 Normal mode (reset by reading the REFERENCE/DATACAPTURE (25h) register)
1 1 Autoreset on interrupt event
Table 26. High-pass filter cutoff frequency configuration [Hz]
HPCF[3:0] ODR = 100 Hz ODR = 200 Hz ODR = 400 Hz ODR = 800 Hz
0000 8 15 30 56
0001 4 8 15 30
0010 2 4 8 15
0011 1 2 4 8
0100 0.5 1 2 4
0101 0.2 0.5 1 2
0110 0.1 0.2 0.5 1
0111 0.05 0.1 0.2 0.5
1000 0.02 0.05 0.1 0.2
1001 0.01 0.02 0.05 0.1
I3G4250D
Register description
DS10938 - Rev 3 page 25/41\n```\n\n

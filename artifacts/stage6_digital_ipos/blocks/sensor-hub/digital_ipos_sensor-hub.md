# **Digital IPOS - Sensor-Hub** {#digital-ipos---sensor-hub}

- Snapshot: `snap-b2e8101b00dc6909feaed885`

Author: Alessandro Lucio IANNUZZI

## **0. Document Navigation** {#0-document-navigation}

### **0.1 Table of contents** {#01-table-of-contents}
- [1. Block overview](#1-block-overview)
- [2. Source I/O](#2-source-io)
- [3. Block requirements](#3-block-requirements)

### **0.2 Document control** {#02-document-control}
#### **Table 1. Version history** {#table-1-version-history}
| Version | Date | Description | Author |
|---|---|---|---|
| 0.1 | 2026-10-01 | Snapshot snap-b2e8101b00dc6909feaed885 digital IPOS block baseline | Alessandro Lucio IANNUZZI |

### **0.3 Requirement navigation** {#03-requirement-navigation}
| Requirement | Internal link |
|---|---|
| IPOS-SENSOR-HUB-001 | [Go to requirement](#ipos-sensor-hub-001) |
| IPOS-SENSOR-HUB-002 | [Go to requirement](#ipos-sensor-hub-002) |
| IPOS-SENSOR-HUB-003 | [Go to requirement](#ipos-sensor-hub-003) |
| IPOS-SENSOR-HUB-004 | [Go to requirement](#ipos-sensor-hub-004) |
| IPOS-SENSOR-HUB-005 | [Go to requirement](#ipos-sensor-hub-005) |
| IPOS-SENSOR-HUB-006 | [Go to requirement](#ipos-sensor-hub-006) |
| IPOS-SENSOR-HUB-007 | [Go to requirement](#ipos-sensor-hub-007) |
| IPOS-SENSOR-HUB-008 | [Go to requirement](#ipos-sensor-hub-008) |
| IPOS-SENSOR-HUB-009 | [Go to requirement](#ipos-sensor-hub-009) |
| IPOS-SENSOR-HUB-010 | [Go to requirement](#ipos-sensor-hub-010) |
| IPOS-SENSOR-HUB-011 | [Go to requirement](#ipos-sensor-hub-011) |
| IPOS-SENSOR-HUB-012 | [Go to requirement](#ipos-sensor-hub-012) |
| IPOS-SENSOR-HUB-013 | [Go to requirement](#ipos-sensor-hub-013) |
| IPOS-SENSOR-HUB-014 | [Go to requirement](#ipos-sensor-hub-014) |
| IPOS-SENSOR-HUB-015 | [Go to requirement](#ipos-sensor-hub-015) |
| IPOS-SENSOR-HUB-016 | [Go to requirement](#ipos-sensor-hub-016) |
| IPOS-SENSOR-HUB-017 | [Go to requirement](#ipos-sensor-hub-017) |
| IPOS-SENSOR-HUB-018 | [Go to requirement](#ipos-sensor-hub-018) |

## **1. Block overview** {#1-block-overview}

### **1.1 Functionality** {#11-functionality}

The Sensor-Hub block is designed to operate the Sensor Hub I2C master for external targets, including trigger/control, pad enable, data collection, and FIFO multi-mode coordination.

### **1.2 Supported functions and scope** {#12-supported-functions-and-scope}

- The Sensor-Hub accepts primary sensing input and produces analog input signal.
- **Register reset on operation start.** Resets SENSOR_HUB_x registers whenever a new I2C operation starts.

## **2. Source I/O** {#2-source-io}

The following approved source I/O entries are owned by this block.

| Port name | Direction | Type / details | Table | Source page |
|---|---|---|---|---|
| scan_mode | input |  | Sensor Hub I/O List | 104 |
| scan_enable | input |  | Sensor Hub I/O List | 104 |
| scan_rstn | input |  | Sensor Hub I/O List | 104 |
| HCLKM | input |  | Sensor Hub I/O List | 104 |
| HCLKS | input |  | Sensor Hub I/O List | 104 |
| sys_clk | input |  | Sensor Hub I/O List | 104 |
| HRESETn | input |  | Sensor Hub I/O List | 104 |
| DEBUG_MODE_i | input |  | Sensor Hub I/O List | 104 |
| scl_master_in | input |  | Sensor Hub I/O List | 104 |
| sda_master_in | input |  | Sensor Hub I/O List | 104 |
| scl_master_out | output |  | Sensor Hub I/O List | 104 |
| sda_master_out | output |  | Sensor Hub I/O List | 104 |
| dvalid_masterblaze_ext | input |  | Sensor Hub I/O List | 104 |
| dvalid_masterblaze_ext_enable | input |  | Sensor Hub I/O List | 104 |
| sleep_master | output |  | Sensor Hub I/O List | 104 |
| master_end_op_pulse | output |  | Sensor Hub I/O List | 104 |
| SH_SMARTFIFO_OCCUPATION | input |  | Sensor Hub I/O List | 104 |
| fifo_mode | input |  | Sensor Hub I/O List | 104 |
| fifo_offset | input | [11:0] | Sensor Hub I/O List | 104 |
| HSELS | input |  | Sensor Hub I/O List | 104 |
| HADDRS | input | [ADDRWIDTH- 1:0] 104 | Sensor Hub I/O List | 104 |
| HTRANSS | input | [1:0] | Sensor Hub I/O List | 105 |
| HSIZES | input | [2:0] | Sensor Hub I/O List | 105 |
| HWRITES | input |  | Sensor Hub I/O List | 105 |
| HREADYS | input |  | Sensor Hub I/O List | 105 |
| HWDATAS | input | [31:0] | Sensor Hub I/O List | 105 |
| HREADYOUTS | output |  | Sensor Hub I/O List | 105 |
| HRESPS | output |  | Sensor Hub I/O List | 105 |
| HRDATAS | output | [31:0] | Sensor Hub I/O List | 105 |
| ahb_master_on | output |  | Sensor Hub I/O List | 105 |
| HRDATAM | input | [31:0] | Sensor Hub I/O List | 105 |
| HREADYM | input |  | Sensor Hub I/O List | 105 |
| HRESPM | input | [1:0] | Sensor Hub I/O List | 105 |
| HGRANTM | input |  | Sensor Hub I/O List | 105 |
| HSELM | output |  | Sensor Hub I/O List | 105 |
| HADDRM | output | [31:0] | Sensor Hub I/O List | 105 |
| HTRANSM | output | [1:0] | Sensor Hub I/O List | 105 |
| HWRITEM | output |  | Sensor Hub I/O List | 105 |
| HSIZEM | output | [2:0] | Sensor Hub I/O List | 105 |
| HBURSTM | output | [2:0] | Sensor Hub I/O List | 105 |
| HPROTM | output | [3:0] | Sensor Hub I/O List | 105 |
| HWDATAM | output | [31:0] | Sensor Hub I/O List | 105 |
| HBUSREQM | output |  | Sensor Hub I/O List | 105 |
| HLOCKM | output |  | Sensor Hub I/O List | 105 |

## **3. Block requirements** {#3-block-requirements}


#### **IPOS-SENSOR-HUB-001** {#ipos-sensor-hub-001}
The output port sleep_master shall be set to 1 when an I2C operation is not on-going. [Vpriority High] [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9017

[End]


#### **IPOS-SENSOR-HUB-002** {#ipos-sensor-hub-002}
[DDS_STBIO1_9018] Requirement The trigger of sensor hub shall be possible in both ways, HW via dvalid_masterblaze_ext signal or SW using DVALID_REGISTER.

Covers: DDS_STBIO1_9018

[End]


#### **IPOS-SENSOR-HUB-003** {#ipos-sensor-hub-003}
[DDS_STBIO1_9024] Requirement Only I2C target addressed through SLAVE0_DEV_ADD register shall be the destination of an I2C Write Operation.

Covers: DDS_STBIO1_9024

[End]


#### **IPOS-SENSOR-HUB-004** {#ipos-sensor-hub-004}
[DDS_STBIO1_9027] Requirement The bit 0 of SLAVE1_DEV_ADD, SLAVE2_DEV_ADD, SLAVE3_DEV_ADD registers shall be ignored: ONLY read operations towards I2C target 1, 2 and 3 shall be performed.

Covers: DDS_STBIO1_9027

[End]


#### **IPOS-SENSOR-HUB-005** {#ipos-sensor-hub-005}
AUX_SENS_ON possible values shall be 0,1,2,3. All the values shall be tested since MasterBlaze supports up-to 4 I2C targets connected to I2C network. [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9029

[End]


#### **IPOS-SENSOR-HUB-006** {#ipos-sensor-hub-006}
[DDS_STBIO1_9030] Requirement SLAVEx_NUMOP bit-fields of SLAVEx_CONFIG registers shall define how many bytes per slave are read as per effect of an I2C operation (x from 1 to 12).

Covers: DDS_STBIO1_9030

[End]


#### **IPOS-SENSOR-HUB-007** {#ipos-sensor-hub-007}
All the values from 1 to 12 shall be valid for SLAVEx_NUMOP bit-fields of SLAVEx_CONFIG registers. [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9031

[End]


#### **IPOS-SENSOR-HUB-008** {#ipos-sensor-hub-008}
[DDS_STBIO1_9032] Requirement SLAVE0_NUMOP bitfield shall be ignored if an I2C Write operation is issued to the I2C Slave 0.

Covers: DDS_STBIO1_9032

[End]


#### **IPOS-SENSOR-HUB-009** {#ipos-sensor-hub-009}
All the SENSOR_HUB_x registers shall be reset every time a new I2C operation starts. [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9033

[End]


#### **IPOS-SENSOR-HUB-010** {#ipos-sensor-hub-010}
The NACK_REGISTER register is reset every time a new I2C operation starts. [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9034

[End]


#### **IPOS-SENSOR-HUB-011** {#ipos-sensor-hub-011}
When Quokka MasterBlaze µP runs (sleep_master signal = 0), any dvalid triggered (HW or SW) shall be ignored. [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9035

[End]


#### **IPOS-SENSOR-HUB-012** {#ipos-sensor-hub-012}
Each data stored in FIFO shall be composed by 4 words (16bytes). [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9260

[End]


#### **IPOS-SENSOR-HUB-013** {#ipos-sensor-hub-013}
3 words (12bytes) of the data stored in FIFO shall contain the data from each I2C slave. [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9261

[End]


#### **IPOS-SENSOR-HUB-014** {#ipos-sensor-hub-014}
24-bits of the data stored in FIFO shall be reserved at '0'. [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9262

[End]


#### **IPOS-SENSOR-HUB-015** {#ipos-sensor-hub-015}
The last 8-bits of the data stored in FIFO shall contain the TAG field. [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9263

[End]


#### **IPOS-SENSOR-HUB-016** {#ipos-sensor-hub-016}
[DDS_STBIO1_9300] Requirement The AHB Write to registers has no effect if the IP masterblaze processor is busy (I2C operation on-going); the registers value shall not be updated.

Covers: DDS_STBIO1_9300

[End]


#### **IPOS-SENSOR-HUB-017** {#ipos-sensor-hub-017}
If the sensor hub IP is not enabled, the SCL and SDA pad shall not toggle. [Vpriority High] [TO: IPOS_Senshub_MB_i2c]

Covers: DDS_STBIO1_9317

[End]


#### **IPOS-SENSOR-HUB-018** {#ipos-sensor-hub-018}
[DDS_STBIO1_9500] Requirement In case also other sources that writes into FIFO are active, then sensor hub shall work always in multi-fifo mode fifo_mode input of sensor hub set to '1' .

Covers: DDS_STBIO1_9500

[End]


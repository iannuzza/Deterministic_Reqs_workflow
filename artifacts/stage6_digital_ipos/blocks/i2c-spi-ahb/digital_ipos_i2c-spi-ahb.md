# **Digital IPOS - I2C_SPI_AHB** {#digital-ipos---i2cspiahb}

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
| IPOS-I2C-SPI-AHB-001 | [Go to requirement](#ipos-i2c-spi-ahb-001) |
| IPOS-I2C-SPI-AHB-002 | [Go to requirement](#ipos-i2c-spi-ahb-002) |
| IPOS-I2C-SPI-AHB-003 | [Go to requirement](#ipos-i2c-spi-ahb-003) |
| IPOS-I2C-SPI-AHB-004 | [Go to requirement](#ipos-i2c-spi-ahb-004) |
| IPOS-I2C-SPI-AHB-005 | [Go to requirement](#ipos-i2c-spi-ahb-005) |
| IPOS-I2C-SPI-AHB-006 | [Go to requirement](#ipos-i2c-spi-ahb-006) |
| IPOS-I2C-SPI-AHB-007 | [Go to requirement](#ipos-i2c-spi-ahb-007) |
| IPOS-I2C-SPI-AHB-008 | [Go to requirement](#ipos-i2c-spi-ahb-008) |
| IPOS-I2C-SPI-AHB-009 | [Go to requirement](#ipos-i2c-spi-ahb-009) |
| IPOS-I2C-SPI-AHB-010 | [Go to requirement](#ipos-i2c-spi-ahb-010) |
| IPOS-I2C-SPI-AHB-011 | [Go to requirement](#ipos-i2c-spi-ahb-011) |
| IPOS-I2C-SPI-AHB-012 | [Go to requirement](#ipos-i2c-spi-ahb-012) |
| IPOS-I2C-SPI-AHB-013 | [Go to requirement](#ipos-i2c-spi-ahb-013) |
| IPOS-I2C-SPI-AHB-014 | [Go to requirement](#ipos-i2c-spi-ahb-014) |
| IPOS-I2C-SPI-AHB-015 | [Go to requirement](#ipos-i2c-spi-ahb-015) |

## **1. Block overview** {#1-block-overview}

### **1.1 Functionality** {#11-functionality}

The I2C_SPI_AHB block is designed to accept I2C/SPI accesses and translate them as needed into AHB transactions for device configuration and readback, including ISPU access.

### **1.2 Supported functions and scope** {#12-supported-functions-and-scope}

- The I2C_SPI_AHB accepts host bus transactions and produces protocol-compliant responses.
- **Read data preloading.** Preloads data from AHB after a double-byte write to 0x68-0x6f, keeping the internal FIFO ready for the master read request.

## **2. Source I/O** {#2-source-io}

The following approved source I/O entries are owned by this block.

| Port name | Direction | Type / details | Table | Source page |
|---|---|---|---|---|
| rst_n | input | POR | I2C/SPI AHB I/O List | 99 |
| i_if_cs | input | CS for SPI interface | I2C/SPI AHB I/O List | 99 |
| o_if_cs_tud | output | Control for CS PAD. 1 in scan mode 0 otherwise | I2C/SPI AHB I/O List | 99 |
| o_if_cs_en_n | output | Set to 0 for CS pad id bidir pad is used. Could be inverted depending on the PAD | I2C/SPI AHB I/O List | 99 |
| o_if_cs_out_n | output | Set to 0 for CS pad id bidir pad is used. Could be inverted depending on the PAD | I2C/SPI AHB I/O List | 99 |
| i_if_ck | input | Interface clock 99 | I2C/SPI AHB I/O List | 99 |
| i_if_sda_sdi_in | input | SDA/SDI from pad | I2C/SPI AHB I/O List | 100 |
| o_if_sda_sdi_en_n | output | SDA/SDI pad enable | I2C/SPI AHB I/O List | 100 |
| o_if_sda_sdi_out | output | SDA/SDI to pad | I2C/SPI AHB I/O List | 100 |
| o_ctrl_reg_7 | output | [7:0] 8 configuration bit set by local register (addr. 0x5e) | I2C/SPI AHB I/O List | 100 |
| i_ext_reg_dt | input | [7:0] Data from external register block (if present) | I2C/SPI AHB I/O List | 100 |
| o_ext_reg_wr_add | output | [7:0] Write address to external register block (if present) | I2C/SPI AHB I/O List | 100 |
| o_ext_reg_rd_add | output | [7:0] Read address to external register block (if present) | I2C/SPI AHB I/O List | 100 |
| o_ext_reg_dt | output | [7:0] Data to external register block (if present) | I2C/SPI AHB I/O List | 100 |
| o_ext_reg_ck_wr | output | Write enable for external register block (if present) | I2C/SPI AHB I/O List | 100 |
| o_ext_reg_we | output | Write direct enable for external register block (if present) rst_16m_n Sw reset for AHB domain | I2C/SPI AHB I/O List | 100 |
| sys_16m_clk | input | AHB clock | I2C/SPI AHB I/O List | 100 |
| o_hselm | output | AHB_M | I2C/SPI AHB I/O List | 100 |
| o_haddrm | output | [31:0] AHB_M | I2C/SPI AHB I/O List | 100 |
| o_htransm | output | [1:0] AHB_M | I2C/SPI AHB I/O List | 100 |
| o_hmasterm | output | [3:0] AHB_M | I2C/SPI AHB I/O List | 100 |
| o_hwritem | output | AHB_M | I2C/SPI AHB I/O List | 100 |
| o_hsizem | output | [2:0] AHB_M | I2C/SPI AHB I/O List | 100 |
| o_hmastlockm | output | AHB_M | I2C/SPI AHB I/O List | 100 |
| o_hwdatam | output | [31:0] AHB_M | I2C/SPI AHB I/O List | 100 |
| o_hburstm | output | [2:0] AHB_M | I2C/SPI AHB I/O List | 100 |
| o_hprotm | output | [3:0] AHB_M | I2C/SPI AHB I/O List | 100 |
| i_hrdatam | input | [31:0] AHB_M | I2C/SPI AHB I/O List | 100 |
| i_hreadym | input | AHB_M | I2C/SPI AHB I/O List | 100 |
| i_hrespm | input | AHB_M | I2C/SPI AHB I/O List | 100 |
| o_gt_ck_on | output | Pulse on interface clock to inform system that AHB clock must be switched on 100 | I2C/SPI AHB I/O List | 100 |
| o_gt_ck_off | output | Pulse on AHB clock to inform system that AHB clock can be switched off | I2C/SPI AHB I/O List | 101 |
| o_ahb_error | output | Error on AHB side. Active if bit 1 or of register at address 0x4f are active. | I2C/SPI AHB I/O List | 101 |
| o_rd_byte_nr_err | output | Active when | I2C/SPI AHB I/O List | 101 |
| o_req_error | output | Active when number of byte is missing for read or timeout between double yte write and read is expired | I2C/SPI AHB I/O List | 101 |
| scan_mode | input | Scan mode | I2C/SPI AHB I/O List | 101 |
| scan_enable | input | Scan enable | I2C/SPI AHB I/O List | 101 |
| scan_clk | input | Scan clk | I2C/SPI AHB I/O List | 101 |
| scan_rst | input | Scan reset | I2C/SPI AHB I/O List | 101 |

## **3. Block requirements** {#3-block-requirements}


#### **IPOS-I2C-SPI-AHB-001** {#ipos-i2c-spi-ahb-001}
[DDS_STBIO1_8000] Requirement: I2C interface shall support all the specified modalities (Standard, FM, FM+) and, if configured, HS is also supported.

Covers: DDS_STBIO1_8000

[End]


#### **IPOS-I2C-SPI-AHB-002** {#ipos-i2c-spi-ahb-002}
Clock frequency ratio between system (AHB) and I2C/SPI interfaces domains shall be at least 2 times. [TO: IPOS_I2C_SPI_AHB_0006] [Vpriority High]

Covers: DDS_STBIO1_8001

[End]


#### **IPOS-I2C-SPI-AHB-003** {#ipos-i2c-spi-ahb-003}
The IP has a serial interface (I2C or SPI) and a parallel bus interface AHB. [TO: IPOS_I2C_SPI_AHB_0007]

Covers: DDS_STBIO1_8002

[End]


#### **IPOS-I2C-SPI-AHB-004** {#ipos-i2c-spi-ahb-004}
An I2C/SPI write access to the address 0x60-0x67 shall be translated in an AHB write access to the configured AHB address (contained in registers SAM_ADDR_BYTE0/1/2/3, address 0x50/0x51/0x52/0x53). [TO: IPOS_I2C_SPI_AHB_0009] [Vpriority High]

Covers: DDS_STBIO1_8003

[End]


#### **IPOS-I2C-SPI-AHB-005** {#ipos-i2c-spi-ahb-005}
A double byte write access to the address 0x68-0x6f (with data that is the number of bytes that the master wants to read) shall start the data preload from AHB in order to have the internal fifo not empty when the read request will be done by the master. [TO: IPOS_I2C_SPI_AHB_0010] [Vpriority High]

Covers: DDS_STBIO1_8004

[End]


#### **IPOS-I2C-SPI-AHB-006** {#ipos-i2c-spi-ahb-006}
An I2C/SPI read access to the address 0x70-0x7f shall be translated in an AHB read access to the configured AHB address (contained in registers SAM_ADDR_BYTE0/1/2/3, address 0x50/0x51/0x52/0x53). [TO: IPOS_I2C_SPI_AHB_0011] [Vpriority High]

Covers: DDS_STBIO1_8005

[End]


#### **IPOS-I2C-SPI-AHB-007** {#ipos-i2c-spi-ahb-007}
On AHB interface, data size shall be limited to BYTE and WORD. [TO: IPOS_I2C_SPI_AHB_0361]

Covers: DDS_STBIO1_8006

[End]


#### **IPOS-I2C-SPI-AHB-008** {#ipos-i2c-spi-ahb-008}
On AHB interface, BURST shall not be supported as well as LOCKED transfers. [TO: IPOS_I2C_SPI_AHB_0362]

Covers: DDS_STBIO1_8007

[End]


#### **IPOS-I2C-SPI-AHB-009** {#ipos-i2c-spi-ahb-009}
CONNECTION fifo_dpt 8 FIFO depth. Suggested val 8

Covers: DDS_STBIO1_8100

[End]


#### **IPOS-I2C-SPI-AHB-010** {#ipos-i2c-spi-ahb-010}
rd_to_max_val 6000 Time available between double byte write to communicate the number of bytes to be read and the following read. If timer expires the operation is aborted and proper flag is activated. Suggested val. 1200

Covers: DDS_STBIO1_8101

[End]


#### **IPOS-I2C-SPI-AHB-011** {#ipos-i2c-spi-ahb-011}
i2c_hs_mode 1'b0 To activate HS I2C

Covers: DDS_STBIO1_8102

[End]


#### **IPOS-I2C-SPI-AHB-012** {#ipos-i2c-spi-ahb-012}
i2c_master_code 8'h00 Master code for HS I2C

Covers: DDS_STBIO1_8103

[End]


#### **IPOS-I2C-SPI-AHB-013** {#ipos-i2c-spi-ahb-013}
ser_mode "i2c_spi" To choose if the interface is SPI only, I2C only or both. Suggested : i2c_spi

Covers: DDS_STBIO1_8104

[End]


#### **IPOS-I2C-SPI-AHB-014** {#ipos-i2c-spi-ahb-014}
ip_version 8'haa IP version

Covers: DDS_STBIO1_8105

[End]


#### **IPOS-I2C-SPI-AHB-015** {#ipos-i2c-spi-ahb-015}
i2c_dev_id 7'h5f I2C device address

Covers: DDS_STBIO1_8106

[End]


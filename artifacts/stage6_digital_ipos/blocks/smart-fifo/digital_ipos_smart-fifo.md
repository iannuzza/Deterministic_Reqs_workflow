# **Digital IPOS - Smart FIFO** {#digital-ipos---smart-fifo}

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
| IPOS-SMART-FIFO-001 | [Go to requirement](#ipos-smart-fifo-001) |
| IPOS-SMART-FIFO-002 | [Go to requirement](#ipos-smart-fifo-002) |
| IPOS-SMART-FIFO-003 | [Go to requirement](#ipos-smart-fifo-003) |
| IPOS-SMART-FIFO-004 | [Go to requirement](#ipos-smart-fifo-004) |
| IPOS-SMART-FIFO-005 | [Go to requirement](#ipos-smart-fifo-005) |
| IPOS-SMART-FIFO-006 | [Go to requirement](#ipos-smart-fifo-006) |
| IPOS-SMART-FIFO-007 | [Go to requirement](#ipos-smart-fifo-007) |
| IPOS-SMART-FIFO-008 | [Go to requirement](#ipos-smart-fifo-008) |
| IPOS-SMART-FIFO-009 | [Go to requirement](#ipos-smart-fifo-009) |
| IPOS-SMART-FIFO-010 | [Go to requirement](#ipos-smart-fifo-010) |
| IPOS-SMART-FIFO-011 | [Go to requirement](#ipos-smart-fifo-011) |
| IPOS-SMART-FIFO-012 | [Go to requirement](#ipos-smart-fifo-012) |
| IPOS-SMART-FIFO-013 | [Go to requirement](#ipos-smart-fifo-013) |

## **1. Block overview** {#1-block-overview}

### **1.1 Functionality** {#11-functionality}

The Smart FIFO block is designed to provide FIFO storage and AHB/memory access in mutually exclusive Unique or Multiple modes, including sub-FIFO depth/addressing and tagged Sensor Hub data formatting.

### **1.2 Supported functions and scope** {#12-supported-functions-and-scope}

- The Smart FIFO accepts digital samples, FIFO mode configuration and produces buffered samples and FIFO status flags.
- **Memory mode entry.** Enters Memory mode when HMASTER is 0 or 1.

## **2. Source I/O** {#2-source-io}

The following approved source I/O entries are owned by this block.

| Port name | Direction | Type / details | Table | Source page |
|---|---|---|---|---|
| TEST_MODE | input | ScanMode u_pad_mux. scan_mode | FIFO Controller I/O List | 112 |
| HCLK | input | AHB Master Handler Clock 16MHz clock u_pmu.clk_fifo | FIFO Controller I/O List | 112 |
| HRESETn | input | u_pmu.resetn_fifo | FIFO Controller I/O List | 112 |
| HSEL | input | AHB Slave Port u_afa_xbar.hsel_M2 | FIFO Controller I/O List | 112 |
| HADDR | input | [AW-1:0] AHB Slave Port u_afa_xbar.haddr_M2 | FIFO Controller I/O List | 112 |
| HMASTER | input | [3:0] AHB Slave Port u_afa_xbar.hmaster_M2 | FIFO Controller I/O List | 112 |
| HTRANS | input | [1:0] AHB Slave Port u_afa_xbar.htrans_M2 | FIFO Controller I/O List | 112 |
| HSIZE | input | [2:0] AHB Slave Port u_afa_xbar.hsize_M2 | FIFO Controller I/O List | 112 |
| HWRITE | input | AHB Slave Port u_afa_xbar. | FIFO Controller I/O List | 112 |
| HWDATA | input | [31:0] AHB Slave Port u_afa_xbar. | FIFO Controller I/O List | 112 |
| HREADY | input | AHB Slave Port u_afa_xbar. | FIFO Controller I/O List | 112 |
| HREADYOUT | output | AHB Slave Port u_afa_xbar. | FIFO Controller I/O List | 112 |
| HRDATA | output | [31:0] AHB Slave Port u_afa_xbar. | FIFO Controller I/O List | 112 |
| HRESP | output | AHB Slave Port u_afa_xbar. | FIFO Controller I/O List | 112 |
| O_FIFO_RAM_A | output | [ADDR_WIDTH- 1:0] u_ca_fifo_bist_c.ags_1 | FIFO Controller I/O List | 112 |
| O_FIFO_RAM_D | output | [23:0] u_ca_fifo_bist_c.csns_1 | FIFO Controller I/O List | 112 |
| O_FIFO_RAM_CSN | output | u_ca_fifo_bist_c.dgs_1 | FIFO Controller I/O List | 112 |
| O_FIFO_RAM_M | output | [23:0] u_ca_fifo_bist_c.wens_1 | FIFO Controller I/O List | 112 |
| O_FIFO_RAM_WEN | output | u_ca_fifo_bist_c.mgs_1 | FIFO Controller I/O List | 112 |
| I_FIFO_RAM_Q | input | [23:0] u_ca_fifo_bist_c.dgrs_1 | FIFO Controller I/O List | 112 |

## **3. Block requirements** {#3-block-requirements}


#### **IPOS-SMART-FIFO-001** {#ipos-smart-fifo-001}
If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode. [TO: IPOS_FIFO_CTRL_00000008]

Covers: DDS_STBIO1_00000008

[End]


#### **IPOS-SMART-FIFO-002** {#ipos-smart-fifo-002}
The parameter MEM_LOC shall define the first Memory Location of the FIFO RAM: 0xC4000. [TO: IPOS_FIFO_CTRL_00000102]

Covers: DDS_STBIO1_00000102

[End]


#### **IPOS-SMART-FIFO-003** {#ipos-smart-fifo-003}
If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode. [TO: IPOS_FIFO_CTRL_00000008]

Covers: DDS_STBIO1_00000199

[End]


#### **IPOS-SMART-FIFO-004** {#ipos-smart-fifo-004}
The FIFO register map first memory location shall be defined as MEM_LOC + 0x1000: 0xC5000. [TO: IPOS_FIFO_CTRL_00000202]

Covers: DDS_STBIO1_00000202

[End]


#### **IPOS-SMART-FIFO-005** {#ipos-smart-fifo-005}
When in Multiple Fifo, the 6 sub-FIFO offset shall coincide with the following table : FIFO OFFSET DATA TYPE ECG FIFO OFFSET ECG0_AC, ECG0_DC BIA FIFO OFFSET BIA_AC_P, BIA_DC_P, BIA_AC_Q, BIA_DC_Q, ECG1_AC, ECG2_DC GSR FIFO OFFSET GSR, ECG1_DC, ECG2_AC PPG FIFO OFFSET PPG Table 31 : FIFO Offset Data Table

Covers: DDS_STBIO1_00001199

[End]


#### **IPOS-SMART-FIFO-006** {#ipos-smart-fifo-006}
As default, the FIFO shall work in Unique FIFO Mode. [TO: IPOS_FIFO_CTRL_89455232]

Covers: DDS_STBIO1_89455232

[End]


#### **IPOS-SMART-FIFO-007** {#ipos-smart-fifo-007}
The FIFO Controller shall have an AHB Slave Interface connected to the AHB BUS and a Memory Master Interface connected to the Physical Memory. [TO: IPOS_FIFO_CTRL_89455261]

Covers: DDS_STBIO1_89455261

[End]


#### **IPOS-SMART-FIFO-008** {#ipos-smart-fifo-008}
The FIFO Controller shall have two working modes: Multiple FIFO and Unique FIFO. These two modes are mutually exclusive. [TO: IPOS_FIFO_CTRL_89455449]

Covers: DDS_STBIO1_89455449

[End]


#### **IPOS-SMART-FIFO-009** {#ipos-smart-fifo-009}
The FIFO Controller shall be able to address 1.5 kbyte divided into 32-bit address. [TO: IPOS_FIFO_CTRL_89456557]

Covers: DDS_STBIO1_89456557

[End]


#### **IPOS-SMART-FIFO-010** {#ipos-smart-fifo-010}
The user shall select the Multiple FIFO mode setting to 1 the first bit into the FIFO_CFG_MODE and 0 for the Unique FIFO mode. [TO: IPOS_FIFO_CTRL_89456975]

Covers: DDS_STBIO1_89456975

[End]


#### **IPOS-SMART-FIFO-011** {#ipos-smart-fifo-011}
The FIFO Controller shall have a 6 i_depth input of 8 bit to be used in Multiple FIFO Mode to define the depth of each subFIFOs. [TO: IPOS_FIFO_CTRL_89457435]

Covers: DDS_STBIO1_89457435

[End]


#### **IPOS-SMART-FIFO-012** {#ipos-smart-fifo-012}
The FIFO 6 memory locations to access each sub-FIFO in Multiple mode are obtained adding multiples of 256 to the memory base address. Example: FIFO Memory Base Address = 0xC4000, then: FIFO 0 memory location 0xC4000 FIFO 1 memory location 0xC4100 FIFO 2 memory location 0xC4200 FIFO 3 memory location 0xC4300 FIFO 4 memory location 0xC4400 FIFO 5 memory location 0xC4500 Table 29: SUB FIFO Memory Address [TO: IPOS_FIFO_CTRL_89457790]

Covers: DDS_STBIO1_89457790

[End]


#### **IPOS-SMART-FIFO-013** {#ipos-smart-fifo-013}
The FIFO Controller shall work at 16 MHz clock frequency. [TO: IPOS_FIFO_CTRL_89459082]

Covers: DDS_STBIO1_89459082

[End]


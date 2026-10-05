# **Digital IPOS - Regmap** {#digital-ipos---regmap}

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
| IPOS-REGMAP-001 | [Go to requirement](#ipos-regmap-001) |
| IPOS-REGMAP-002 | [Go to requirement](#ipos-regmap-002) |
| IPOS-REGMAP-003 | [Go to requirement](#ipos-regmap-003) |
| IPOS-REGMAP-004 | [Go to requirement](#ipos-regmap-004) |
| IPOS-REGMAP-005 | [Go to requirement](#ipos-regmap-005) |
| IPOS-REGMAP-006 | [Go to requirement](#ipos-regmap-006) |
| IPOS-REGMAP-007 | [Go to requirement](#ipos-regmap-007) |
| IPOS-REGMAP-008 | [Go to requirement](#ipos-regmap-008) |

## **1. Block overview** {#1-block-overview}

### **1.1 Functionality** {#11-functionality}

The Regmap block is designed to implement the mapped AFE, system, and OTP registers, exposing configuration/status while enforcing reset and OTP write-protection rules.

### **1.2 Supported functions and scope** {#12-supported-functions-and-scope}

- The Regmap accepts host read/write transactions and produces register data and status fields.

## **2. Source I/O** {#2-source-io}

No approved source I/O entries are assigned to this block in the current architecture snapshot.

## **3. Block requirements** {#3-block-requirements}


#### **IPOS-REGMAP-001** {#ipos-regmap-001}
132 **Update-IR** Run-Test/Idle Select-DR-Scan 13.4. STBIO1 Register Map 13.4.1. STBIO1 Register Map Here is described the list of registers in the register map. The AFE_BLOCK registers are accessible by I2C/SPI direct access and AHB interface, while the others are only by AHB. The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers. BASE START ADDRESS ADDRESS BLOCK REGISTER WIDTH BASE END ADDRE VREF_TRIM SS RESET REQ_ID 0xC8000 AFE_BLOCK 8 0xC80EB tst_main_reset_n, regmap_sw_resetn

Covers: DDS_STBIO1_3000

[End]


#### **IPOS-REGMAP-002** {#ipos-regmap-002}
0xC80EC RESERVED 0xC8FFF tst_main_reset_n, regmap_sw_resetn

Covers: DDS_STBIO1_3001

[End]


#### **IPOS-REGMAP-003** {#ipos-regmap-003}
0xC9000 OTP REGISTER 8 0xC902C tst_main_reset_n

Covers: DDS_STBIO1_3002

[End]


#### **IPOS-REGMAP-004** {#ipos-regmap-004}
0xC9030 RESERVED 0xC9FFF tst_main_reset_n, regmap_sw_resetn

Covers: DDS_STBIO1_3003

[End]


#### **IPOS-REGMAP-005** {#ipos-regmap-005}
0xCA000 SYSTEM_REGISTER 32 0xCA140 tst_main_reset_n, regmap_sw_resetn

Covers: DDS_STBIO1_3004

[End]


#### **IPOS-REGMAP-006** {#ipos-regmap-006}
0xCA144 RESERVED 0xCCFFF tst_main_reset_n, regmap_sw_resetn

Covers: DDS_STBIO1_3005

[End]


#### **IPOS-REGMAP-007** {#ipos-regmap-007}
0xCD000 OTP (TRIMM REGS) 32 0xCD02F tst_main_reset_n, regmap_sw_resetn

Covers: DDS_STBIO1_3006

[End]


#### **IPOS-REGMAP-008** {#ipos-regmap-008}
[DDS_STBIO1_4000] Requirement: Write enable for each OTP REGISTER shall be 0, in functional mode, if bit 31 of OTP_PRG10 is set 1.

Covers: DDS_STBIO1_4000

[End]


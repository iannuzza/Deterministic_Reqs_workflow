# **Digital IPOS - ADSP** {#digital-ipos---adsp}

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
| IPOS-ADSP-001 | [Go to requirement](#ipos-adsp-001) |
| IPOS-ADSP-002 | [Go to requirement](#ipos-adsp-002) |
| IPOS-ADSP-003 | [Go to requirement](#ipos-adsp-003) |
| IPOS-ADSP-004 | [Go to requirement](#ipos-adsp-004) |
| IPOS-ADSP-005 | [Go to requirement](#ipos-adsp-005) |
| IPOS-ADSP-006 | [Go to requirement](#ipos-adsp-006) |
| IPOS-ADSP-007 | [Go to requirement](#ipos-adsp-007) |
| IPOS-ADSP-008 | [Go to requirement](#ipos-adsp-008) |
| IPOS-ADSP-009 | [Go to requirement](#ipos-adsp-009) |
| IPOS-ADSP-010 | [Go to requirement](#ipos-adsp-010) |
| IPOS-ADSP-011 | [Go to requirement](#ipos-adsp-011) |
| IPOS-ADSP-012 | [Go to requirement](#ipos-adsp-012) |
| IPOS-ADSP-013 | [Go to requirement](#ipos-adsp-013) |
| IPOS-ADSP-014 | [Go to requirement](#ipos-adsp-014) |
| IPOS-ADSP-015 | [Go to requirement](#ipos-adsp-015) |
| IPOS-ADSP-016 | [Go to requirement](#ipos-adsp-016) |
| IPOS-ADSP-017 | [Go to requirement](#ipos-adsp-017) |
| IPOS-ADSP-018 | [Go to requirement](#ipos-adsp-018) |
| IPOS-ADSP-019 | [Go to requirement](#ipos-adsp-019) |

## **1. Block overview** {#1-block-overview}

### **1.1 Functionality** {#11-functionality}

The ADSP block is designed to execute ADSP firmware for OTP boot/write/test and signal elaboration, using mapped program/data/register memory and soft-reset handling.

### **1.2 Supported functions and scope** {#12-supported-functions-and-scope}

- The ADSP accepts acquired samples and configuration data and produces elaborated signal data and metadata.
- **Operation start conditions.** Starts a new operation only when quokka_run is low and one of OTP_TEST, OTP_WRITE, or OTP_BOOT is set to 1; OTP_BOOT initiates the BOOT routine while quokka_run is low.
- **OTP memory transfer.** Copies data from OTP memory to OTP registers and OTP regmap to OTP memory.

## **2. Source I/O** {#2-source-io}

The following approved source I/O entries are owned by this block.

| Port name | Direction | Type / details | Table | Source page |
|---|---|---|---|---|
| stmc_clk | input | wire u_pmu.tst_clk_16m | ADSP I/O List | 86 |
| HCLK | input | wire u_pmu.clk_stmc | ADSP I/O List | 86 |
| HRESETn | input | wire u_pmu.resetn_stmc | ADSP I/O List | 86 |
| HSELS | input | wire u_xbar_afe. | ADSP I/O List | 86 |
| HADDRS | input | wire [ADDRWIDTH-1:0] u_xbar_afe.haddr_M1 | ADSP I/O List | 86 |
| HTRANSS | input | wire [ 1:0] u_xbar_afe.htrans_M1 | ADSP I/O List | 86 |
| HSIZES | input | wire [ 2:0] u_xbar_afe. | ADSP I/O List | 86 |
| HWRITES | input | wire u_xbar_afe. | ADSP I/O List | 86 |
| HREADYS | input | wire u_xbar_afe. | ADSP I/O List | 86 |
| HWDATAS | input | wire [ 31:0] u_xbar_afe. | ADSP I/O List | 86 |
| HREADYOUTS | output | wire u_xbar_afe. | ADSP I/O List | 86 |
| HRESPS | output | wire u_xbar_afe. | ADSP I/O List | 86 |
| HRDATAS | output | wire [ 31:0] u_xbar_afe. | ADSP I/O List | 86 |
| HRDATAM | input | wire [ 31:0] | ADSP I/O List | 86 |
| HREADYM | input | wire | ADSP I/O List | 86 |
| HRESPM | input | wire [ 1:0] | ADSP I/O List | 86 |
| HGRANTM | input | wire | ADSP I/O List | 86 |
| HSELM | output | wire | ADSP I/O List | 86 |
| HADDRM | output | wire [ 31:0] | ADSP I/O List | 86 |
| HTRANSM | output | wire [ 1:0] | ADSP I/O List | 86 |
| HWRITEM | output | wire | ADSP I/O List | 86 |
| HSIZEM | output | wire [ 2:0] 86 | ADSP I/O List | 86 |
| HBURSTM | output | wire [ 2:0] | ADSP I/O List | 87 |
| HPROTM | output | wire [ 3:0] | ADSP I/O List | 87 |
| HWDATAM | output | wire [ 31:0] | ADSP I/O List | 87 |
| HBUSREQM | output | wire | ADSP I/O List | 87 |
| HLOCKM | output | wire | ADSP I/O List | 87 |
| stmc_data_CSN | output | wire | ADSP I/O List | 87 |
| stmc_data_WEN | output | wire | ADSP I/O List | 87 |
| stmc_data_A | output | wire [ 8:0] | ADSP I/O List | 87 |
| stmc_data_D | output | wire [ 63:0] | ADSP I/O List | 87 |
| stmc_data_M | output | wire [ 63:0] | ADSP I/O List | 87 |
| stmc_data_Q | input | wire [ 63:0] | ADSP I/O List | 87 |
| stmc_rom_CLK | output | wire | ADSP I/O List | 87 |
| stmc_rom_CSN | output | wire | ADSP I/O List | 87 |
| stmc_rom_A | output | wire [ 10:0] | ADSP I/O List | 87 |
| stmc_rom_Q | input | wire [ 22:0] | ADSP I/O List | 87 |
| quokka_run | output | wire u_pmu.adsp_run main_controller_top.i_quokka_r un | ADSP I/O List | 87 |
| quokka_boot_end | output | wire main_controller_top.i_quokka_b oot_end | ADSP I/O List | 87 |
| ahb_master_clk_en | output | wire U_pmu.clk_en_s1 | ADSP I/O List | 87 |
| scan_mode | input | wire | ADSP I/O List | 87 |
| scan_en | input | wire | ADSP I/O List | 87 |
| scan_clk | input | wire | ADSP I/O List | 87 |
| scan_rst_n | input | wire | ADSP I/O List | 87 |

## **3. Block requirements** {#3-block-requirements}


#### **IPOS-ADSP-001** {#ipos-adsp-001}
To move OTP signal, ADSP shall write a new value in a regbank by AHB protocol.

Covers: DDS_STBIO1_0013

[End]


#### **IPOS-ADSP-002** {#ipos-adsp-002}
The BOOT routine shall starts when the OTP_BOOT bit rises and shall completes when quokka_boot_end rises. [Vpriority High]

Covers: DDS_STBIO1_0014

[End]


#### **IPOS-ADSP-003** {#ipos-adsp-003}
During OTP boot operation, the ADSP shall copy the content of the OTP memory into the OTP registers, following the procedure to access OTP memory [Vpriority High]

Covers: DDS_STBIO1_0015

[End]


#### **IPOS-ADSP-004** {#ipos-adsp-004}
During BOOT routine, ADSP shall first read the last location of the OTP memory, at address 0x7F. If the content is 0xFF, called “lifecycle” byte, then the READ operation proceeds from address 0 to address 0x2F; otherwise, ADSP shall not perform any further reads.

Covers: DDS_STBIO1_0016

[End]


#### **IPOS-ADSP-005** {#ipos-adsp-005}
To perform a BOOT routine, OTP_BOOT bit shall be written when quokka_run is low. [Vpriority High]

Covers: DDS_STBIO1_0017

[End]


#### **IPOS-ADSP-006** {#ipos-adsp-006}
The WRITE routine shall start when OTP Write Bit rises and completes when quokka_run falls. [Vpriority High]

Covers: DDS_STBIO1_0018

[End]


#### **IPOS-ADSP-007** {#ipos-adsp-007}
During WRITE routine ADSP shall copy the content of the OTP regmap into the OTP memory, following the procedure to burn the fuses as expressed in the OTP datasheet [Vpriority High]

Covers: DDS_STBIO1_0019

[End]


#### **IPOS-ADSP-008** {#ipos-adsp-008}
During WRITE routine, ADSP shall allow copying all OTP Registers into the OTP Memory only if the location 0x24 of OTP Memory (OTP[24] in the following diagram) is not set to 0xFF.

Covers: DDS_STBIO1_0020

[End]


#### **IPOS-ADSP-009** {#ipos-adsp-009}
During the WRITE routine and after copying all OTP Registers into the OTP Memory, ADSP shall compare each value inside the OTP memory with the corresponding value in OTP Registers to check if the WRITE routine has been succesfull. In that case ADSP shall write 0xFF into the last location of the OTP memory.

Covers: DDS_STBIO1_0021

[End]


#### **IPOS-ADSP-010** {#ipos-adsp-010}
OTP_WRITE, OTP_BOOT and OTP_TEST bits shall be cleared by ADSP at the end of their respective operation [Vpriority High]

Covers: DDS_STBIO1_0022

[End]


#### **IPOS-ADSP-011** {#ipos-adsp-011}
A new operation shall start only when quokka_run is low, and one between OTP_TEST bit, OTP_WRITE bit or OTP_BOOT bit is written to 1 [Vpriority High]

Covers: DDS_STBIO1_0023

[End]


#### **IPOS-ADSP-012** {#ipos-adsp-012}
OTP_IREF_WAKEUP shall be set to one by an external I2C/SPI to AHB write before initiating a new OTP_TEST or OTP_WRITE operation [Vpriority High]

Covers: DDS_STBIO1_0024

[End]


#### **IPOS-ADSP-013** {#ipos-adsp-013}
OTP_IREF_WAKEUP shall be setted to zero by an external I2C/SPI to AHB write at the end of OTP_TEST or OTP_WRITE operation [Vpriority High]

Covers: DDS_STBIO1_0025

[End]


#### **IPOS-ADSP-014** {#ipos-adsp-014}
After startup phase, once started with an operation, the IP shall ignore any further start incoming transactions. [Vpriority High]

Covers: DDS_STBIO1_0026

[End]


#### **IPOS-ADSP-015** {#ipos-adsp-015}
The TEST routine shall start when OTP Test Bit rises and completes when quokka_run falls. [Vpriority High]

Covers: DDS_STBIO1_0027

[End]


#### **IPOS-ADSP-016** {#ipos-adsp-016}
[DDS_STBIO1_0028] Requirement: The TEST routines shall allow reading an 8-bit word on OTP of a specific address written in OTP_A register, and write this value in OTP_D_TEST register.

Covers: DDS_STBIO1_0028

[End]


#### **IPOS-ADSP-017** {#ipos-adsp-017}
The Soft Reset routine shall start when SOFT_RESET Bit (in CONTROL_A register) rises and completes when quokka_run falls. [Vpriority High]

Covers: DDS_STBIO1_0033

[End]


#### **IPOS-ADSP-018** {#ipos-adsp-018}
During the Soft Reset routine, ADSP shall write the ADSP RAM with the value 0. Only the first 3.5Kbyte of ADSP RAM shall be cleared, from address 0x000 to address 0xDFF [Vpriority High]

Covers: DDS_STBIO1_0034

[End]


#### **IPOS-ADSP-019** {#ipos-adsp-019}
If during the start of a new operation, more than one bit is written into CONTROL_A reg in the same write operation, ADSP shall execute only the routine at higher priority and discard the others. Priority is listed below, with first routine at higher priority: 1. SOFT RESET routine 2. OTP WRITE routine 3. OTP TEST routine 4. OTP BOOT routine [Vpriority High]

Covers: DDS_STBIO1_0035

[End]


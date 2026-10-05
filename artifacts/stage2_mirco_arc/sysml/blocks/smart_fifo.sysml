// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 5424834735474f3f97ba3357e63e8703bd7f341f5995c19ba9e75bcba49d8157

package STBIO_Block_SmartFIFO {

    private import STBIO_Shared::*;

    part def SmartFIFO {
        attribute displayName : String = "Smart FIFO";
        attribute description : String = "Provide FIFO storage and AHB/memory access in mutually exclusive Unique or Multiple modes, including sub-FIFO depth/addressing and tagged Sensor Hub data formatting.";
        attribute function : String = "Provide FIFO storage and AHB/memory access in mutually exclusive Unique or Multiple modes, including sub-FIFO depth/addressing and tagged Sensor Hub data formatting.";
        attribute inputs : String = "Digital samples, FIFO mode configuration";
        attribute outputs : String = "Buffered samples and FIFO status flags";
        attribute approvedPortCount : Integer = 20;
        attribute linkedRequirementCount : Integer = 13;
        doc /* block=Smart FIFO | description=Provide FIFO storage and AHB/memory access in mutually exclusive Unique or Multiple modes, including sub-FIFO depth/addressing and tagged Sensor Hub data formatting. */;
        in port TEST_MODE : ArchitecturePort {
            attribute sourceName = "TEST_MODE";
            attribute sourceDetails = "ScanMode u_pad_mux. scan_mode";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HCLK : ArchitecturePort {
            attribute sourceName = "HCLK";
            attribute sourceDetails = "AHB Master Handler Clock 16MHz clock u_pmu.clk_fifo";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HRESETn : ArchitecturePort {
            attribute sourceName = "HRESETn";
            attribute sourceDetails = "u_pmu.resetn_fifo";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HSEL : ArchitecturePort {
            attribute sourceName = "HSEL";
            attribute sourceDetails = "AHB Slave Port u_afa_xbar.hsel_M2";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HADDR : ArchitecturePort {
            attribute sourceName = "HADDR";
            attribute sourceDetails = "[AW-1:0] AHB Slave Port u_afa_xbar.haddr_M2";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HMASTER : ArchitecturePort {
            attribute sourceName = "HMASTER";
            attribute sourceDetails = "[3:0] AHB Slave Port u_afa_xbar.hmaster_M2";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HTRANS : ArchitecturePort {
            attribute sourceName = "HTRANS";
            attribute sourceDetails = "[1:0] AHB Slave Port u_afa_xbar.htrans_M2";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HSIZE : ArchitecturePort {
            attribute sourceName = "HSIZE";
            attribute sourceDetails = "[2:0] AHB Slave Port u_afa_xbar.hsize_M2";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HWRITE : ArchitecturePort {
            attribute sourceName = "HWRITE";
            attribute sourceDetails = "AHB Slave Port u_afa_xbar.";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HWDATA : ArchitecturePort {
            attribute sourceName = "HWDATA";
            attribute sourceDetails = "[31:0] AHB Slave Port u_afa_xbar.";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port HREADY : ArchitecturePort {
            attribute sourceName = "HREADY";
            attribute sourceDetails = "AHB Slave Port u_afa_xbar.";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        out port HREADYOUT : ArchitecturePort {
            attribute sourceName = "HREADYOUT";
            attribute sourceDetails = "AHB Slave Port u_afa_xbar.";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        out port HRDATA : ArchitecturePort {
            attribute sourceName = "HRDATA";
            attribute sourceDetails = "[31:0] AHB Slave Port u_afa_xbar.";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        out port HRESP : ArchitecturePort {
            attribute sourceName = "HRESP";
            attribute sourceDetails = "AHB Slave Port u_afa_xbar.";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        out port O_FIFO_RAM_A : ArchitecturePort {
            attribute sourceName = "O_FIFO_RAM_A";
            attribute sourceDetails = "[ADDR_WIDTH- 1:0] u_ca_fifo_bist_c.ags_1";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        out port O_FIFO_RAM_D : ArchitecturePort {
            attribute sourceName = "O_FIFO_RAM_D";
            attribute sourceDetails = "[23:0] u_ca_fifo_bist_c.csns_1";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        out port O_FIFO_RAM_CSN : ArchitecturePort {
            attribute sourceName = "O_FIFO_RAM_CSN";
            attribute sourceDetails = "u_ca_fifo_bist_c.dgs_1";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        out port O_FIFO_RAM_M : ArchitecturePort {
            attribute sourceName = "O_FIFO_RAM_M";
            attribute sourceDetails = "[23:0] u_ca_fifo_bist_c.wens_1";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        out port O_FIFO_RAM_WEN : ArchitecturePort {
            attribute sourceName = "O_FIFO_RAM_WEN";
            attribute sourceDetails = "u_ca_fifo_bist_c.mgs_1";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }
        in port I_FIFO_RAM_Q : ArchitecturePort {
            attribute sourceName = "I_FIFO_RAM_Q";
            attribute sourceDetails = "[23:0] u_ca_fifo_bist_c.dgrs_1";
            attribute sourceTable = "FIFO Controller I/O List";
            attribute sourcePage = "112";
        }

        requirement def IPOS_SMART_FIFO_001 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_00000008";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-001";
            doc /* If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode. [TO: IPOS_FIFO_CTRL_00000008] */;
        }
        requirement req_IPOS_SMART_FIFO_001 : IPOS_SMART_FIFO_001;
        doc /* iposReqId=IPOS-SMART-FIFO-001 | sourceReqId=DDS_STBIO1_00000008 | If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode. [TO: IPOS_FIFO_CTRL_00000008] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-001 -> approved source requirement DDS_STBIO1_00000008 */;
        satisfy req_IPOS_SMART_FIFO_001 by self;
        requirement def IPOS_SMART_FIFO_002 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_00000102";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-002";
            doc /* The parameter MEM_LOC shall define the first Memory Location of the FIFO RAM: 0xC4000. [TO: IPOS_FIFO_CTRL_00000102] */;
        }
        requirement req_IPOS_SMART_FIFO_002 : IPOS_SMART_FIFO_002;
        doc /* iposReqId=IPOS-SMART-FIFO-002 | sourceReqId=DDS_STBIO1_00000102 | The parameter MEM_LOC shall define the first Memory Location of the FIFO RAM: 0xC4000. [TO: IPOS_FIFO_CTRL_00000102] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-002 -> approved source requirement DDS_STBIO1_00000102 */;
        satisfy req_IPOS_SMART_FIFO_002 by self;
        requirement def IPOS_SMART_FIFO_003 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_00000199";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-003";
            doc /* If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode. [TO: IPOS_FIFO_CTRL_00000008] */;
        }
        requirement req_IPOS_SMART_FIFO_003 : IPOS_SMART_FIFO_003;
        doc /* iposReqId=IPOS-SMART-FIFO-003 | sourceReqId=DDS_STBIO1_00000199 | If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode. [TO: IPOS_FIFO_CTRL_00000008] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-003 -> approved source requirement DDS_STBIO1_00000199 */;
        satisfy req_IPOS_SMART_FIFO_003 by self;
        requirement def IPOS_SMART_FIFO_004 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_00000202";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-004";
            doc /* The FIFO register map first memory location shall be defined as MEM_LOC + 0x1000: 0xC5000. [TO: IPOS_FIFO_CTRL_00000202] */;
        }
        requirement req_IPOS_SMART_FIFO_004 : IPOS_SMART_FIFO_004;
        doc /* iposReqId=IPOS-SMART-FIFO-004 | sourceReqId=DDS_STBIO1_00000202 | The FIFO register map first memory location shall be defined as MEM_LOC + 0x1000: 0xC5000. [TO: IPOS_FIFO_CTRL_00000202] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-004 -> approved source requirement DDS_STBIO1_00000202 */;
        satisfy req_IPOS_SMART_FIFO_004 by self;
        requirement def IPOS_SMART_FIFO_005 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_00001199";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-005";
            doc /* When in Multiple Fifo, the 6 sub-FIFO offset shall coincide with the following table : FIFO OFFSET DATA TYPE ECG FIFO OFFSET ECG0_AC, ECG0_DC BIA FIFO OFFSET BIA_AC_P, BIA_DC_P, BIA_AC_Q, BIA_DC_Q, ECG1_AC, ECG2_DC GSR FIFO OFFSET GSR, ECG1_DC, ECG2_AC PPG FIFO OFFSET PPG Table 31 : FIFO Offset Data Table */;
        }
        requirement req_IPOS_SMART_FIFO_005 : IPOS_SMART_FIFO_005;
        doc /* iposReqId=IPOS-SMART-FIFO-005 | sourceReqId=DDS_STBIO1_00001199 | When in Multiple Fifo, the 6 sub-FIFO offset shall coincide with the following table : FIFO OFFSET DATA TYPE ECG FIFO OFFSET ECG0_AC, ECG0_DC BIA FIFO OFFSET BIA_AC_P, BIA_DC_P, BIA_AC_Q, BIA_DC_Q, ECG1_AC, ECG2_DC GSR FIFO OFFSET GSR, ECG1_DC, ECG2_AC PPG FIFO OFFSET PPG Table 31 : FIFO Offset Data Table */;
        doc /* coverageDependency: IPOS-SMART-FIFO-005 -> approved source requirement DDS_STBIO1_00001199 */;
        satisfy req_IPOS_SMART_FIFO_005 by self;
        requirement def IPOS_SMART_FIFO_006 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_89455232";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-006";
            doc /* As default, the FIFO shall work in Unique FIFO Mode. [TO: IPOS_FIFO_CTRL_89455232] */;
        }
        requirement req_IPOS_SMART_FIFO_006 : IPOS_SMART_FIFO_006;
        doc /* iposReqId=IPOS-SMART-FIFO-006 | sourceReqId=DDS_STBIO1_89455232 | As default, the FIFO shall work in Unique FIFO Mode. [TO: IPOS_FIFO_CTRL_89455232] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-006 -> approved source requirement DDS_STBIO1_89455232 */;
        satisfy req_IPOS_SMART_FIFO_006 by self;
        requirement def IPOS_SMART_FIFO_007 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_89455261";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-007";
            doc /* The FIFO Controller shall have an AHB Slave Interface connected to the AHB BUS and a Memory Master Interface connected to the Physical Memory. [TO: IPOS_FIFO_CTRL_89455261] */;
        }
        requirement req_IPOS_SMART_FIFO_007 : IPOS_SMART_FIFO_007;
        doc /* iposReqId=IPOS-SMART-FIFO-007 | sourceReqId=DDS_STBIO1_89455261 | The FIFO Controller shall have an AHB Slave Interface connected to the AHB BUS and a Memory Master Interface connected to the Physical Memory. [TO: IPOS_FIFO_CTRL_89455261] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-007 -> approved source requirement DDS_STBIO1_89455261 */;
        satisfy req_IPOS_SMART_FIFO_007 by self;
        requirement def IPOS_SMART_FIFO_008 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_89455449";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-008";
            doc /* The FIFO Controller shall have two working modes: Multiple FIFO and Unique FIFO. These two modes are mutually exclusive. [TO: IPOS_FIFO_CTRL_89455449] */;
        }
        requirement req_IPOS_SMART_FIFO_008 : IPOS_SMART_FIFO_008;
        doc /* iposReqId=IPOS-SMART-FIFO-008 | sourceReqId=DDS_STBIO1_89455449 | The FIFO Controller shall have two working modes: Multiple FIFO and Unique FIFO. These two modes are mutually exclusive. [TO: IPOS_FIFO_CTRL_89455449] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-008 -> approved source requirement DDS_STBIO1_89455449 */;
        satisfy req_IPOS_SMART_FIFO_008 by self;
        requirement def IPOS_SMART_FIFO_009 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_89456557";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-009";
            doc /* The FIFO Controller shall be able to address 1.5 kbyte divided into 32-bit address. [TO: IPOS_FIFO_CTRL_89456557] */;
        }
        requirement req_IPOS_SMART_FIFO_009 : IPOS_SMART_FIFO_009;
        doc /* iposReqId=IPOS-SMART-FIFO-009 | sourceReqId=DDS_STBIO1_89456557 | The FIFO Controller shall be able to address 1.5 kbyte divided into 32-bit address. [TO: IPOS_FIFO_CTRL_89456557] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-009 -> approved source requirement DDS_STBIO1_89456557 */;
        satisfy req_IPOS_SMART_FIFO_009 by self;
        requirement def IPOS_SMART_FIFO_010 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_89456975";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-010";
            doc /* The user shall select the Multiple FIFO mode setting to 1 the first bit into the FIFO_CFG_MODE and 0 for the Unique FIFO mode. [TO: IPOS_FIFO_CTRL_89456975] */;
        }
        requirement req_IPOS_SMART_FIFO_010 : IPOS_SMART_FIFO_010;
        doc /* iposReqId=IPOS-SMART-FIFO-010 | sourceReqId=DDS_STBIO1_89456975 | The user shall select the Multiple FIFO mode setting to 1 the first bit into the FIFO_CFG_MODE and 0 for the Unique FIFO mode. [TO: IPOS_FIFO_CTRL_89456975] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-010 -> approved source requirement DDS_STBIO1_89456975 */;
        satisfy req_IPOS_SMART_FIFO_010 by self;
        requirement def IPOS_SMART_FIFO_011 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_89457435";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-011";
            doc /* The FIFO Controller shall have a 6 i_depth input of 8 bit to be used in Multiple FIFO Mode to define the depth of each subFIFOs. [TO: IPOS_FIFO_CTRL_89457435] */;
        }
        requirement req_IPOS_SMART_FIFO_011 : IPOS_SMART_FIFO_011;
        doc /* iposReqId=IPOS-SMART-FIFO-011 | sourceReqId=DDS_STBIO1_89457435 | The FIFO Controller shall have a 6 i_depth input of 8 bit to be used in Multiple FIFO Mode to define the depth of each subFIFOs. [TO: IPOS_FIFO_CTRL_89457435] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-011 -> approved source requirement DDS_STBIO1_89457435 */;
        satisfy req_IPOS_SMART_FIFO_011 by self;
        requirement def IPOS_SMART_FIFO_012 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_89457790";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-012";
            doc /* The FIFO 6 memory locations to access each sub-FIFO in Multiple mode are obtained adding multiples of 256 to the memory base address. Example: FIFO Memory Base Address = 0xC4000, then: FIFO 0 memory location 0xC4000 FIFO 1 memory location 0xC4100 FIFO 2 memory location 0xC4200 FIFO 3 memory location 0xC4300 FIFO 4 memory location 0xC4400 FIFO 5 memory location 0xC4500 Table 29: SUB FIFO Memory Address [TO: IPOS_FIFO_CTRL_89457790] */;
        }
        requirement req_IPOS_SMART_FIFO_012 : IPOS_SMART_FIFO_012;
        doc /* iposReqId=IPOS-SMART-FIFO-012 | sourceReqId=DDS_STBIO1_89457790 | The FIFO 6 memory locations to access each sub-FIFO in Multiple mode are obtained adding multiples of 256 to the memory base address. Example: FIFO Memory Base Address = 0xC4000, then: FIFO 0 memory location 0xC4000 FIFO 1 memory location 0xC4100 FIFO 2 memory location 0xC4200 FIFO 3 memory location 0xC4300 FIFO 4 memory location 0xC4400 FIFO 5 memory location 0xC4500 Table 29: SUB FIFO Memory Address [TO: IPOS_FIFO_CTRL_89457790] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-012 -> approved source requirement DDS_STBIO1_89457790 */;
        satisfy req_IPOS_SMART_FIFO_012 by self;
        requirement def IPOS_SMART_FIFO_013 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_89459082";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SMART-FIFO-013";
            doc /* The FIFO Controller shall work at 16 MHz clock frequency. [TO: IPOS_FIFO_CTRL_89459082] */;
        }
        requirement req_IPOS_SMART_FIFO_013 : IPOS_SMART_FIFO_013;
        doc /* iposReqId=IPOS-SMART-FIFO-013 | sourceReqId=DDS_STBIO1_89459082 | The FIFO Controller shall work at 16 MHz clock frequency. [TO: IPOS_FIFO_CTRL_89459082] */;
        doc /* coverageDependency: IPOS-SMART-FIFO-013 -> approved source requirement DDS_STBIO1_89459082 */;
        satisfy req_IPOS_SMART_FIFO_013 by self;
    }

}

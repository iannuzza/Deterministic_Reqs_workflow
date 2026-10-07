// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 8d22eb86b9a584c32e1fedacf6d98a199b8f93896143054eb1c8b2075b0ea372

package STBIO_Block_I2CSPIAHB {

    private import STBIO_Shared::*;

    part def I2CSPIAHB {
        attribute displayName : String = "I2C_SPI_AHB";
        attribute description : String = "Accept I2C/SPI accesses and translate them as needed into AHB transactions for device configuration and readback, including ISPU access.";
        attribute function : String = "Accept I2C/SPI accesses and translate them as needed into AHB transactions for device configuration and readback, including ISPU access.";
        attribute inputs : String = "Host bus transactions";
        attribute outputs : String = "Protocol-compliant responses";
        attribute approvedPortCount : Integer = 39;
        attribute linkedRequirementCount : Integer = 15;
        doc /* block=I2C_SPI_AHB | description=Accept I2C/SPI accesses and translate them as needed into AHB transactions for device configuration and readback, including ISPU access. */;
        in port rst_n : ArchitecturePort {
            attribute sourceName = "rst_n";
            attribute sourceDetails = "POR";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "99";
        }
        in port i_if_cs : ArchitecturePort {
            attribute sourceName = "i_if_cs";
            attribute sourceDetails = "CS for SPI interface";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "99";
        }
        out port o_if_cs_tud : ArchitecturePort {
            attribute sourceName = "o_if_cs_tud";
            attribute sourceDetails = "Control for CS PAD. 1 in scan mode 0 otherwise";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "99";
        }
        out port o_if_cs_en_n : ArchitecturePort {
            attribute sourceName = "o_if_cs_en_n";
            attribute sourceDetails = "Set to 0 for CS pad id bidir pad is used. Could be inverted depending on the PAD";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "99";
        }
        out port o_if_cs_out_n : ArchitecturePort {
            attribute sourceName = "o_if_cs_out_n";
            attribute sourceDetails = "Set to 0 for CS pad id bidir pad is used. Could be inverted depending on the PAD";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "99";
        }
        in port i_if_ck : ArchitecturePort {
            attribute sourceName = "i_if_ck";
            attribute sourceDetails = "Interface clock 99";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "99";
        }
        in port i_if_sda_sdi_in : ArchitecturePort {
            attribute sourceName = "i_if_sda_sdi_in";
            attribute sourceDetails = "SDA/SDI from pad";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_if_sda_sdi_en_n : ArchitecturePort {
            attribute sourceName = "o_if_sda_sdi_en_n";
            attribute sourceDetails = "SDA/SDI pad enable";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_if_sda_sdi_out : ArchitecturePort {
            attribute sourceName = "o_if_sda_sdi_out";
            attribute sourceDetails = "SDA/SDI to pad";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_ctrl_reg_7 : ArchitecturePort {
            attribute sourceName = "o_ctrl_reg_7";
            attribute sourceDetails = "[7:0] 8 configuration bit set by local register (addr. 0x5e)";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        in port i_ext_reg_dt : ArchitecturePort {
            attribute sourceName = "i_ext_reg_dt";
            attribute sourceDetails = "[7:0] Data from external register block (if present)";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_ext_reg_wr_add : ArchitecturePort {
            attribute sourceName = "o_ext_reg_wr_add";
            attribute sourceDetails = "[7:0] Write address to external register block (if present)";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_ext_reg_rd_add : ArchitecturePort {
            attribute sourceName = "o_ext_reg_rd_add";
            attribute sourceDetails = "[7:0] Read address to external register block (if present)";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_ext_reg_dt : ArchitecturePort {
            attribute sourceName = "o_ext_reg_dt";
            attribute sourceDetails = "[7:0] Data to external register block (if present)";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_ext_reg_ck_wr : ArchitecturePort {
            attribute sourceName = "o_ext_reg_ck_wr";
            attribute sourceDetails = "Write enable for external register block (if present)";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_ext_reg_we : ArchitecturePort {
            attribute sourceName = "o_ext_reg_we";
            attribute sourceDetails = "Write direct enable for external register block (if present) rst_16m_n Sw reset for AHB domain";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        in port sys_16m_clk : ArchitecturePort {
            attribute sourceName = "sys_16m_clk";
            attribute sourceDetails = "AHB clock";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_hselm : ArchitecturePort {
            attribute sourceName = "o_hselm";
            attribute sourceDetails = "AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_haddrm : ArchitecturePort {
            attribute sourceName = "o_haddrm";
            attribute sourceDetails = "[31:0] AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_htransm : ArchitecturePort {
            attribute sourceName = "o_htransm";
            attribute sourceDetails = "[1:0] AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_hmasterm : ArchitecturePort {
            attribute sourceName = "o_hmasterm";
            attribute sourceDetails = "[3:0] AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_hwritem : ArchitecturePort {
            attribute sourceName = "o_hwritem";
            attribute sourceDetails = "AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_hsizem : ArchitecturePort {
            attribute sourceName = "o_hsizem";
            attribute sourceDetails = "[2:0] AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_hmastlockm : ArchitecturePort {
            attribute sourceName = "o_hmastlockm";
            attribute sourceDetails = "AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_hwdatam : ArchitecturePort {
            attribute sourceName = "o_hwdatam";
            attribute sourceDetails = "[31:0] AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_hburstm : ArchitecturePort {
            attribute sourceName = "o_hburstm";
            attribute sourceDetails = "[2:0] AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_hprotm : ArchitecturePort {
            attribute sourceName = "o_hprotm";
            attribute sourceDetails = "[3:0] AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        in port i_hrdatam : ArchitecturePort {
            attribute sourceName = "i_hrdatam";
            attribute sourceDetails = "[31:0] AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        in port i_hreadym : ArchitecturePort {
            attribute sourceName = "i_hreadym";
            attribute sourceDetails = "AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        in port i_hrespm : ArchitecturePort {
            attribute sourceName = "i_hrespm";
            attribute sourceDetails = "AHB_M";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_gt_ck_on : ArchitecturePort {
            attribute sourceName = "o_gt_ck_on";
            attribute sourceDetails = "Pulse on interface clock to inform system that AHB clock must be switched on 100";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "100";
        }
        out port o_gt_ck_off : ArchitecturePort {
            attribute sourceName = "o_gt_ck_off";
            attribute sourceDetails = "Pulse on AHB clock to inform system that AHB clock can be switched off";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "101";
        }
        out port o_ahb_error : ArchitecturePort {
            attribute sourceName = "o_ahb_error";
            attribute sourceDetails = "Error on AHB side. Active if bit 1 or of register at address 0x4f are active.";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "101";
        }
        out port o_rd_byte_nr_err : ArchitecturePort {
            attribute sourceName = "o_rd_byte_nr_err";
            attribute sourceDetails = "Active when";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "101";
        }
        out port o_req_error : ArchitecturePort {
            attribute sourceName = "o_req_error";
            attribute sourceDetails = "Active when number of byte is missing for read or timeout between double yte write and read is expired";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "101";
        }
        in port scan_mode : ArchitecturePort {
            attribute sourceName = "scan_mode";
            attribute sourceDetails = "Scan mode";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "101";
        }
        in port scan_enable : ArchitecturePort {
            attribute sourceName = "scan_enable";
            attribute sourceDetails = "Scan enable";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "101";
        }
        in port scan_clk : ArchitecturePort {
            attribute sourceName = "scan_clk";
            attribute sourceDetails = "Scan clk";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "101";
        }
        in port scan_rst : ArchitecturePort {
            attribute sourceName = "scan_rst";
            attribute sourceDetails = "Scan reset";
            attribute sourceTable = "I2C/SPI AHB I/O List";
            attribute sourcePage = "101";
        }

        requirement def IPOS_I2C_SPI_AHB_001 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8000";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-001";
            doc /* [DDS_STBIO1_8000] Requirement: I2C interface shall support all the specified modalities (Standard, FM, FM+) and, if configured, HS is also supported. */;
        }
        requirement req_IPOS_I2C_SPI_AHB_001 : IPOS_I2C_SPI_AHB_001;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-001 | sourceReqId=DDS_STBIO1_8000 | [DDS_STBIO1_8000] Requirement: I2C interface shall support all the specified modalities (Standard, FM, FM+) and, if configured, HS is also supported. */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-001 -> approved source requirement DDS_STBIO1_8000 */;
        satisfy req_IPOS_I2C_SPI_AHB_001 by self;
        requirement def IPOS_I2C_SPI_AHB_002 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8001";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-002";
            doc /* Clock frequency ratio between system (AHB) and I2C/SPI interfaces domains shall be at least 2 times. [TO: IPOS_I2C_SPI_AHB_0006] [Vpriority High] */;
        }
        requirement req_IPOS_I2C_SPI_AHB_002 : IPOS_I2C_SPI_AHB_002;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-002 | sourceReqId=DDS_STBIO1_8001 | Clock frequency ratio between system (AHB) and I2C/SPI interfaces domains shall be at least 2 times. [TO: IPOS_I2C_SPI_AHB_0006] [Vpriority High] */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-002 -> approved source requirement DDS_STBIO1_8001 */;
        satisfy req_IPOS_I2C_SPI_AHB_002 by self;
        requirement def IPOS_I2C_SPI_AHB_003 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8002";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-003";
            doc /* The IP has a serial interface (I2C or SPI) and a parallel bus interface AHB. [TO: IPOS_I2C_SPI_AHB_0007] */;
        }
        requirement req_IPOS_I2C_SPI_AHB_003 : IPOS_I2C_SPI_AHB_003;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-003 | sourceReqId=DDS_STBIO1_8002 | The IP has a serial interface (I2C or SPI) and a parallel bus interface AHB. [TO: IPOS_I2C_SPI_AHB_0007] */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-003 -> approved source requirement DDS_STBIO1_8002 */;
        satisfy req_IPOS_I2C_SPI_AHB_003 by self;
        requirement def IPOS_I2C_SPI_AHB_004 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8003";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-004";
            doc /* An I2C/SPI write access to the address 0x60-0x67 shall be translated in an AHB write access to the configured AHB address (contained in registers SAM_ADDR_BYTE0/1/2/3, address 0x50/0x51/0x52/0x53). [TO: IPOS_I2C_SPI_AHB_0009] [Vpriority High] */;
        }
        requirement req_IPOS_I2C_SPI_AHB_004 : IPOS_I2C_SPI_AHB_004;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-004 | sourceReqId=DDS_STBIO1_8003 | An I2C/SPI write access to the address 0x60-0x67 shall be translated in an AHB write access to the configured AHB address (contained in registers SAM_ADDR_BYTE0/1/2/3, address 0x50/0x51/0x52/0x53). [TO: IPOS_I2C_SPI_AHB_0009] [Vpriority High] */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-004 -> approved source requirement DDS_STBIO1_8003 */;
        satisfy req_IPOS_I2C_SPI_AHB_004 by self;
        requirement def IPOS_I2C_SPI_AHB_005 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8004";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-005";
            doc /* A double byte write access to the address 0x68-0x6f (with data that is the number of bytes that the master wants to read) shall start the data preload from AHB in order to have the internal fifo not empty when the read request will be done by the master. [TO: IPOS_I2C_SPI_AHB_0010] [Vpriority High] */;
        }
        requirement req_IPOS_I2C_SPI_AHB_005 : IPOS_I2C_SPI_AHB_005;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-005 | sourceReqId=DDS_STBIO1_8004 | A double byte write access to the address 0x68-0x6f (with data that is the number of bytes that the master wants to read) shall start the data preload from AHB in order to have the internal fifo not empty when the read request will be done by the master. [TO: IPOS_I2C_SPI_AHB_0010] [Vpriority High] */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-005 -> approved source requirement DDS_STBIO1_8004 */;
        satisfy req_IPOS_I2C_SPI_AHB_005 by self;
        requirement def IPOS_I2C_SPI_AHB_006 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8005";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-006";
            doc /* An I2C/SPI read access to the address 0x70-0x7f shall be translated in an AHB read access to the configured AHB address (contained in registers SAM_ADDR_BYTE0/1/2/3, address 0x50/0x51/0x52/0x53). [TO: IPOS_I2C_SPI_AHB_0011] [Vpriority High] */;
        }
        requirement req_IPOS_I2C_SPI_AHB_006 : IPOS_I2C_SPI_AHB_006;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-006 | sourceReqId=DDS_STBIO1_8005 | An I2C/SPI read access to the address 0x70-0x7f shall be translated in an AHB read access to the configured AHB address (contained in registers SAM_ADDR_BYTE0/1/2/3, address 0x50/0x51/0x52/0x53). [TO: IPOS_I2C_SPI_AHB_0011] [Vpriority High] */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-006 -> approved source requirement DDS_STBIO1_8005 */;
        satisfy req_IPOS_I2C_SPI_AHB_006 by self;
        requirement def IPOS_I2C_SPI_AHB_007 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8006";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-007";
            doc /* On AHB interface, data size shall be limited to BYTE and WORD. [TO: IPOS_I2C_SPI_AHB_0361] */;
        }
        requirement req_IPOS_I2C_SPI_AHB_007 : IPOS_I2C_SPI_AHB_007;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-007 | sourceReqId=DDS_STBIO1_8006 | On AHB interface, data size shall be limited to BYTE and WORD. [TO: IPOS_I2C_SPI_AHB_0361] */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-007 -> approved source requirement DDS_STBIO1_8006 */;
        satisfy req_IPOS_I2C_SPI_AHB_007 by self;
        requirement def IPOS_I2C_SPI_AHB_008 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8007";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-008";
            doc /* On AHB interface, BURST shall not be supported as well as LOCKED transfers. [TO: IPOS_I2C_SPI_AHB_0362] */;
        }
        requirement req_IPOS_I2C_SPI_AHB_008 : IPOS_I2C_SPI_AHB_008;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-008 | sourceReqId=DDS_STBIO1_8007 | On AHB interface, BURST shall not be supported as well as LOCKED transfers. [TO: IPOS_I2C_SPI_AHB_0362] */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-008 -> approved source requirement DDS_STBIO1_8007 */;
        satisfy req_IPOS_I2C_SPI_AHB_008 by self;
        requirement def IPOS_I2C_SPI_AHB_009 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8100";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-009";
            doc /* CONNECTION fifo_dpt 8 FIFO depth. Suggested val 8 */;
        }
        requirement req_IPOS_I2C_SPI_AHB_009 : IPOS_I2C_SPI_AHB_009;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-009 | sourceReqId=DDS_STBIO1_8100 | CONNECTION fifo_dpt 8 FIFO depth. Suggested val 8 */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-009 -> approved source requirement DDS_STBIO1_8100 */;
        satisfy req_IPOS_I2C_SPI_AHB_009 by self;
        requirement def IPOS_I2C_SPI_AHB_010 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8101";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-010";
            doc /* rd_to_max_val 6000 Time available between double byte write to communicate the number of bytes to be read and the following read. If timer expires the operation is aborted and proper flag is activated. Suggested val. 1200 */;
        }
        requirement req_IPOS_I2C_SPI_AHB_010 : IPOS_I2C_SPI_AHB_010;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-010 | sourceReqId=DDS_STBIO1_8101 | rd_to_max_val 6000 Time available between double byte write to communicate the number of bytes to be read and the following read. If timer expires the operation is aborted and proper flag is activated. Suggested val. 1200 */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-010 -> approved source requirement DDS_STBIO1_8101 */;
        satisfy req_IPOS_I2C_SPI_AHB_010 by self;
        requirement def IPOS_I2C_SPI_AHB_011 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8102";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-011";
            doc /* i2c_hs_mode 1'b0 To activate HS I2C */;
        }
        requirement req_IPOS_I2C_SPI_AHB_011 : IPOS_I2C_SPI_AHB_011;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-011 | sourceReqId=DDS_STBIO1_8102 | i2c_hs_mode 1'b0 To activate HS I2C */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-011 -> approved source requirement DDS_STBIO1_8102 */;
        satisfy req_IPOS_I2C_SPI_AHB_011 by self;
        requirement def IPOS_I2C_SPI_AHB_012 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8103";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-012";
            doc /* i2c_master_code 8'h00 Master code for HS I2C */;
        }
        requirement req_IPOS_I2C_SPI_AHB_012 : IPOS_I2C_SPI_AHB_012;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-012 | sourceReqId=DDS_STBIO1_8103 | i2c_master_code 8'h00 Master code for HS I2C */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-012 -> approved source requirement DDS_STBIO1_8103 */;
        satisfy req_IPOS_I2C_SPI_AHB_012 by self;
        requirement def IPOS_I2C_SPI_AHB_013 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8104";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-013";
            doc /* ser_mode "i2c_spi" To choose if the interface is SPI only, I2C only or both. Suggested : i2c_spi */;
        }
        requirement req_IPOS_I2C_SPI_AHB_013 : IPOS_I2C_SPI_AHB_013;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-013 | sourceReqId=DDS_STBIO1_8104 | ser_mode "i2c_spi" To choose if the interface is SPI only, I2C only or both. Suggested : i2c_spi */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-013 -> approved source requirement DDS_STBIO1_8104 */;
        satisfy req_IPOS_I2C_SPI_AHB_013 by self;
        requirement def IPOS_I2C_SPI_AHB_014 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8105";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-014";
            doc /* ip_version 8'haa IP version */;
        }
        requirement req_IPOS_I2C_SPI_AHB_014 : IPOS_I2C_SPI_AHB_014;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-014 | sourceReqId=DDS_STBIO1_8105 | ip_version 8'haa IP version */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-014 -> approved source requirement DDS_STBIO1_8105 */;
        satisfy req_IPOS_I2C_SPI_AHB_014 by self;
        requirement def IPOS_I2C_SPI_AHB_015 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_8106";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-I2C-SPI-AHB-015";
            doc /* i2c_dev_id 7'h5f I2C device address */;
        }
        requirement req_IPOS_I2C_SPI_AHB_015 : IPOS_I2C_SPI_AHB_015;
        doc /* iposReqId=IPOS-I2C-SPI-AHB-015 | sourceReqId=DDS_STBIO1_8106 | i2c_dev_id 7'h5f I2C device address */;
        doc /* coverageDependency: IPOS-I2C-SPI-AHB-015 -> approved source requirement DDS_STBIO1_8106 */;
        satisfy req_IPOS_I2C_SPI_AHB_015 by self;
    }

}

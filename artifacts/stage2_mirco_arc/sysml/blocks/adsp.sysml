// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 8d22eb86b9a584c32e1fedacf6d98a199b8f93896143054eb1c8b2075b0ea372

package STBIO_Block_ADSP {

    private import STBIO_Shared::*;

    part def ADSP {
        attribute displayName : String = "ADSP";
        attribute description : String = "Execute ADSP firmware for OTP boot/write/test and signal elaboration, using mapped program/data/register memory and soft-reset handling.";
        attribute function : String = "Execute ADSP firmware for OTP boot/write/test and signal elaboration, using mapped program/data/register memory and soft-reset handling.";
        attribute inputs : String = "Acquired samples and configuration data";
        attribute outputs : String = "Elaborated signal data and metadata";
        attribute approvedPortCount : Integer = 44;
        attribute linkedRequirementCount : Integer = 19;
        doc /* block=ADSP | description=Execute ADSP firmware for OTP boot/write/test and signal elaboration, using mapped program/data/register memory and soft-reset handling. */;
        in port stmc_clk : ArchitecturePort {
            attribute sourceName = "stmc_clk";
            attribute sourceDetails = "wire u_pmu.tst_clk_16m";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HCLK : ArchitecturePort {
            attribute sourceName = "HCLK";
            attribute sourceDetails = "wire u_pmu.clk_stmc";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HRESETn : ArchitecturePort {
            attribute sourceName = "HRESETn";
            attribute sourceDetails = "wire u_pmu.resetn_stmc";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HSELS : ArchitecturePort {
            attribute sourceName = "HSELS";
            attribute sourceDetails = "wire u_xbar_afe.";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HADDRS : ArchitecturePort {
            attribute sourceName = "HADDRS";
            attribute sourceDetails = "wire [ADDRWIDTH-1:0] u_xbar_afe.haddr_M1";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HTRANSS : ArchitecturePort {
            attribute sourceName = "HTRANSS";
            attribute sourceDetails = "wire [ 1:0] u_xbar_afe.htrans_M1";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HSIZES : ArchitecturePort {
            attribute sourceName = "HSIZES";
            attribute sourceDetails = "wire [ 2:0] u_xbar_afe.";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HWRITES : ArchitecturePort {
            attribute sourceName = "HWRITES";
            attribute sourceDetails = "wire u_xbar_afe.";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HREADYS : ArchitecturePort {
            attribute sourceName = "HREADYS";
            attribute sourceDetails = "wire u_xbar_afe.";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HWDATAS : ArchitecturePort {
            attribute sourceName = "HWDATAS";
            attribute sourceDetails = "wire [ 31:0] u_xbar_afe.";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        out port HREADYOUTS : ArchitecturePort {
            attribute sourceName = "HREADYOUTS";
            attribute sourceDetails = "wire u_xbar_afe.";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        out port HRESPS : ArchitecturePort {
            attribute sourceName = "HRESPS";
            attribute sourceDetails = "wire u_xbar_afe.";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        out port HRDATAS : ArchitecturePort {
            attribute sourceName = "HRDATAS";
            attribute sourceDetails = "wire [ 31:0] u_xbar_afe.";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HRDATAM : ArchitecturePort {
            attribute sourceName = "HRDATAM";
            attribute sourceDetails = "wire [ 31:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HREADYM : ArchitecturePort {
            attribute sourceName = "HREADYM";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HRESPM : ArchitecturePort {
            attribute sourceName = "HRESPM";
            attribute sourceDetails = "wire [ 1:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        in port HGRANTM : ArchitecturePort {
            attribute sourceName = "HGRANTM";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        out port HSELM : ArchitecturePort {
            attribute sourceName = "HSELM";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        out port HADDRM : ArchitecturePort {
            attribute sourceName = "HADDRM";
            attribute sourceDetails = "wire [ 31:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        out port HTRANSM : ArchitecturePort {
            attribute sourceName = "HTRANSM";
            attribute sourceDetails = "wire [ 1:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        out port HWRITEM : ArchitecturePort {
            attribute sourceName = "HWRITEM";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        out port HSIZEM : ArchitecturePort {
            attribute sourceName = "HSIZEM";
            attribute sourceDetails = "wire [ 2:0] 86";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "86";
        }
        out port HBURSTM : ArchitecturePort {
            attribute sourceName = "HBURSTM";
            attribute sourceDetails = "wire [ 2:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port HPROTM : ArchitecturePort {
            attribute sourceName = "HPROTM";
            attribute sourceDetails = "wire [ 3:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port HWDATAM : ArchitecturePort {
            attribute sourceName = "HWDATAM";
            attribute sourceDetails = "wire [ 31:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port HBUSREQM : ArchitecturePort {
            attribute sourceName = "HBUSREQM";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port HLOCKM : ArchitecturePort {
            attribute sourceName = "HLOCKM";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port stmc_data_CSN : ArchitecturePort {
            attribute sourceName = "stmc_data_CSN";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port stmc_data_WEN : ArchitecturePort {
            attribute sourceName = "stmc_data_WEN";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port stmc_data_A : ArchitecturePort {
            attribute sourceName = "stmc_data_A";
            attribute sourceDetails = "wire [ 8:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port stmc_data_D : ArchitecturePort {
            attribute sourceName = "stmc_data_D";
            attribute sourceDetails = "wire [ 63:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port stmc_data_M : ArchitecturePort {
            attribute sourceName = "stmc_data_M";
            attribute sourceDetails = "wire [ 63:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        in port stmc_data_Q : ArchitecturePort {
            attribute sourceName = "stmc_data_Q";
            attribute sourceDetails = "wire [ 63:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port stmc_rom_CLK : ArchitecturePort {
            attribute sourceName = "stmc_rom_CLK";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port stmc_rom_CSN : ArchitecturePort {
            attribute sourceName = "stmc_rom_CSN";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port stmc_rom_A : ArchitecturePort {
            attribute sourceName = "stmc_rom_A";
            attribute sourceDetails = "wire [ 10:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        in port stmc_rom_Q : ArchitecturePort {
            attribute sourceName = "stmc_rom_Q";
            attribute sourceDetails = "wire [ 22:0]";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port quokka_run : ArchitecturePort {
            attribute sourceName = "quokka_run";
            attribute sourceDetails = "wire u_pmu.adsp_run main_controller_top.i_quokka_r un";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port quokka_boot_end : ArchitecturePort {
            attribute sourceName = "quokka_boot_end";
            attribute sourceDetails = "wire main_controller_top.i_quokka_b oot_end";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        out port ahb_master_clk_en : ArchitecturePort {
            attribute sourceName = "ahb_master_clk_en";
            attribute sourceDetails = "wire U_pmu.clk_en_s1";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        in port scan_mode : ArchitecturePort {
            attribute sourceName = "scan_mode";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        in port scan_en : ArchitecturePort {
            attribute sourceName = "scan_en";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        in port scan_clk : ArchitecturePort {
            attribute sourceName = "scan_clk";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }
        in port scan_rst_n : ArchitecturePort {
            attribute sourceName = "scan_rst_n";
            attribute sourceDetails = "wire";
            attribute sourceTable = "ADSP I/O List";
            attribute sourcePage = "87";
        }

        requirement def IPOS_ADSP_001 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0013";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-001";
            doc /* To move OTP signal, ADSP shall write a new value in a regbank by AHB protocol. */;
        }
        requirement req_IPOS_ADSP_001 : IPOS_ADSP_001;
        doc /* iposReqId=IPOS-ADSP-001 | sourceReqId=DDS_STBIO1_0013 | To move OTP signal, ADSP shall write a new value in a regbank by AHB protocol. */;
        doc /* coverageDependency: IPOS-ADSP-001 -> approved source requirement DDS_STBIO1_0013 */;
        satisfy req_IPOS_ADSP_001 by self;
        requirement def IPOS_ADSP_002 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0014";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-002";
            doc /* The BOOT routine shall starts when the OTP_BOOT bit rises and shall completes when quokka_boot_end rises. [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_002 : IPOS_ADSP_002;
        doc /* iposReqId=IPOS-ADSP-002 | sourceReqId=DDS_STBIO1_0014 | The BOOT routine shall starts when the OTP_BOOT bit rises and shall completes when quokka_boot_end rises. [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-002 -> approved source requirement DDS_STBIO1_0014 */;
        satisfy req_IPOS_ADSP_002 by self;
        requirement def IPOS_ADSP_003 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0015";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-003";
            doc /* During OTP boot operation, the ADSP shall copy the content of the OTP memory into the OTP registers, following the procedure to access OTP memory [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_003 : IPOS_ADSP_003;
        doc /* iposReqId=IPOS-ADSP-003 | sourceReqId=DDS_STBIO1_0015 | During OTP boot operation, the ADSP shall copy the content of the OTP memory into the OTP registers, following the procedure to access OTP memory [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-003 -> approved source requirement DDS_STBIO1_0015 */;
        satisfy req_IPOS_ADSP_003 by self;
        requirement def IPOS_ADSP_004 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0016";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-004";
            doc /* During BOOT routine, ADSP shall first read the last location of the OTP memory, at address 0x7F. If the content is 0xFF, called “lifecycle” byte, then the READ operation proceeds from address 0 to address 0x2F; otherwise, ADSP shall not perform any further reads. */;
        }
        requirement req_IPOS_ADSP_004 : IPOS_ADSP_004;
        doc /* iposReqId=IPOS-ADSP-004 | sourceReqId=DDS_STBIO1_0016 | During BOOT routine, ADSP shall first read the last location of the OTP memory, at address 0x7F. If the content is 0xFF, called “lifecycle” byte, then the READ operation proceeds from address 0 to address 0x2F; otherwise, ADSP shall not perform any further reads. */;
        doc /* coverageDependency: IPOS-ADSP-004 -> approved source requirement DDS_STBIO1_0016 */;
        satisfy req_IPOS_ADSP_004 by self;
        requirement def IPOS_ADSP_005 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0017";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-005";
            doc /* To perform a BOOT routine, OTP_BOOT bit shall be written when quokka_run is low. [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_005 : IPOS_ADSP_005;
        doc /* iposReqId=IPOS-ADSP-005 | sourceReqId=DDS_STBIO1_0017 | To perform a BOOT routine, OTP_BOOT bit shall be written when quokka_run is low. [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-005 -> approved source requirement DDS_STBIO1_0017 */;
        satisfy req_IPOS_ADSP_005 by self;
        requirement def IPOS_ADSP_006 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0018";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-006";
            doc /* The WRITE routine shall start when OTP Write Bit rises and completes when quokka_run falls. [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_006 : IPOS_ADSP_006;
        doc /* iposReqId=IPOS-ADSP-006 | sourceReqId=DDS_STBIO1_0018 | The WRITE routine shall start when OTP Write Bit rises and completes when quokka_run falls. [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-006 -> approved source requirement DDS_STBIO1_0018 */;
        satisfy req_IPOS_ADSP_006 by self;
        requirement def IPOS_ADSP_007 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0019";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-007";
            doc /* During WRITE routine ADSP shall copy the content of the OTP regmap into the OTP memory, following the procedure to burn the fuses as expressed in the OTP datasheet [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_007 : IPOS_ADSP_007;
        doc /* iposReqId=IPOS-ADSP-007 | sourceReqId=DDS_STBIO1_0019 | During WRITE routine ADSP shall copy the content of the OTP regmap into the OTP memory, following the procedure to burn the fuses as expressed in the OTP datasheet [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-007 -> approved source requirement DDS_STBIO1_0019 */;
        satisfy req_IPOS_ADSP_007 by self;
        requirement def IPOS_ADSP_008 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0020";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-008";
            doc /* During WRITE routine, ADSP shall allow copying all OTP Registers into the OTP Memory only if the location 0x24 of OTP Memory (OTP[24] in the following diagram) is not set to 0xFF. */;
        }
        requirement req_IPOS_ADSP_008 : IPOS_ADSP_008;
        doc /* iposReqId=IPOS-ADSP-008 | sourceReqId=DDS_STBIO1_0020 | During WRITE routine, ADSP shall allow copying all OTP Registers into the OTP Memory only if the location 0x24 of OTP Memory (OTP[24] in the following diagram) is not set to 0xFF. */;
        doc /* coverageDependency: IPOS-ADSP-008 -> approved source requirement DDS_STBIO1_0020 */;
        satisfy req_IPOS_ADSP_008 by self;
        requirement def IPOS_ADSP_009 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0021";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-009";
            doc /* During the WRITE routine and after copying all OTP Registers into the OTP Memory, ADSP shall compare each value inside the OTP memory with the corresponding value in OTP Registers to check if the WRITE routine has been succesfull. In that case ADSP shall write 0xFF into the last location of the OTP memory. */;
        }
        requirement req_IPOS_ADSP_009 : IPOS_ADSP_009;
        doc /* iposReqId=IPOS-ADSP-009 | sourceReqId=DDS_STBIO1_0021 | During the WRITE routine and after copying all OTP Registers into the OTP Memory, ADSP shall compare each value inside the OTP memory with the corresponding value in OTP Registers to check if the WRITE routine has been succesfull. In that case ADSP shall write 0xFF into the last location of the OTP memory. */;
        doc /* coverageDependency: IPOS-ADSP-009 -> approved source requirement DDS_STBIO1_0021 */;
        satisfy req_IPOS_ADSP_009 by self;
        requirement def IPOS_ADSP_010 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0022";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-010";
            doc /* OTP_WRITE, OTP_BOOT and OTP_TEST bits shall be cleared by ADSP at the end of their respective operation [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_010 : IPOS_ADSP_010;
        doc /* iposReqId=IPOS-ADSP-010 | sourceReqId=DDS_STBIO1_0022 | OTP_WRITE, OTP_BOOT and OTP_TEST bits shall be cleared by ADSP at the end of their respective operation [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-010 -> approved source requirement DDS_STBIO1_0022 */;
        satisfy req_IPOS_ADSP_010 by self;
        requirement def IPOS_ADSP_011 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0023";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-011";
            doc /* A new operation shall start only when quokka_run is low, and one between OTP_TEST bit, OTP_WRITE bit or OTP_BOOT bit is written to 1 [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_011 : IPOS_ADSP_011;
        doc /* iposReqId=IPOS-ADSP-011 | sourceReqId=DDS_STBIO1_0023 | A new operation shall start only when quokka_run is low, and one between OTP_TEST bit, OTP_WRITE bit or OTP_BOOT bit is written to 1 [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-011 -> approved source requirement DDS_STBIO1_0023 */;
        satisfy req_IPOS_ADSP_011 by self;
        requirement def IPOS_ADSP_012 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0024";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-012";
            doc /* OTP_IREF_WAKEUP shall be set to one by an external I2C/SPI to AHB write before initiating a new OTP_TEST or OTP_WRITE operation [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_012 : IPOS_ADSP_012;
        doc /* iposReqId=IPOS-ADSP-012 | sourceReqId=DDS_STBIO1_0024 | OTP_IREF_WAKEUP shall be set to one by an external I2C/SPI to AHB write before initiating a new OTP_TEST or OTP_WRITE operation [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-012 -> approved source requirement DDS_STBIO1_0024 */;
        satisfy req_IPOS_ADSP_012 by self;
        requirement def IPOS_ADSP_013 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0025";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-013";
            doc /* OTP_IREF_WAKEUP shall be setted to zero by an external I2C/SPI to AHB write at the end of OTP_TEST or OTP_WRITE operation [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_013 : IPOS_ADSP_013;
        doc /* iposReqId=IPOS-ADSP-013 | sourceReqId=DDS_STBIO1_0025 | OTP_IREF_WAKEUP shall be setted to zero by an external I2C/SPI to AHB write at the end of OTP_TEST or OTP_WRITE operation [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-013 -> approved source requirement DDS_STBIO1_0025 */;
        satisfy req_IPOS_ADSP_013 by self;
        requirement def IPOS_ADSP_014 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0026";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-014";
            doc /* After startup phase, once started with an operation, the IP shall ignore any further start incoming transactions. [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_014 : IPOS_ADSP_014;
        doc /* iposReqId=IPOS-ADSP-014 | sourceReqId=DDS_STBIO1_0026 | After startup phase, once started with an operation, the IP shall ignore any further start incoming transactions. [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-014 -> approved source requirement DDS_STBIO1_0026 */;
        satisfy req_IPOS_ADSP_014 by self;
        requirement def IPOS_ADSP_015 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0027";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-015";
            doc /* The TEST routine shall start when OTP Test Bit rises and completes when quokka_run falls. [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_015 : IPOS_ADSP_015;
        doc /* iposReqId=IPOS-ADSP-015 | sourceReqId=DDS_STBIO1_0027 | The TEST routine shall start when OTP Test Bit rises and completes when quokka_run falls. [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-015 -> approved source requirement DDS_STBIO1_0027 */;
        satisfy req_IPOS_ADSP_015 by self;
        requirement def IPOS_ADSP_016 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0028";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-016";
            doc /* [DDS_STBIO1_0028] Requirement: The TEST routines shall allow reading an 8-bit word on OTP of a specific address written in OTP_A register, and write this value in OTP_D_TEST register. */;
        }
        requirement req_IPOS_ADSP_016 : IPOS_ADSP_016;
        doc /* iposReqId=IPOS-ADSP-016 | sourceReqId=DDS_STBIO1_0028 | [DDS_STBIO1_0028] Requirement: The TEST routines shall allow reading an 8-bit word on OTP of a specific address written in OTP_A register, and write this value in OTP_D_TEST register. */;
        doc /* coverageDependency: IPOS-ADSP-016 -> approved source requirement DDS_STBIO1_0028 */;
        satisfy req_IPOS_ADSP_016 by self;
        requirement def IPOS_ADSP_017 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0033";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-017";
            doc /* The Soft Reset routine shall start when SOFT_RESET Bit (in CONTROL_A register) rises and completes when quokka_run falls. [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_017 : IPOS_ADSP_017;
        doc /* iposReqId=IPOS-ADSP-017 | sourceReqId=DDS_STBIO1_0033 | The Soft Reset routine shall start when SOFT_RESET Bit (in CONTROL_A register) rises and completes when quokka_run falls. [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-017 -> approved source requirement DDS_STBIO1_0033 */;
        satisfy req_IPOS_ADSP_017 by self;
        requirement def IPOS_ADSP_018 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0034";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-018";
            doc /* During the Soft Reset routine, ADSP shall write the ADSP RAM with the value 0. Only the first 3.5Kbyte of ADSP RAM shall be cleared, from address 0x000 to address 0xDFF [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_018 : IPOS_ADSP_018;
        doc /* iposReqId=IPOS-ADSP-018 | sourceReqId=DDS_STBIO1_0034 | During the Soft Reset routine, ADSP shall write the ADSP RAM with the value 0. Only the first 3.5Kbyte of ADSP RAM shall be cleared, from address 0x000 to address 0xDFF [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-018 -> approved source requirement DDS_STBIO1_0034 */;
        satisfy req_IPOS_ADSP_018 by self;
        requirement def IPOS_ADSP_019 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0035";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-ADSP-019";
            doc /* If during the start of a new operation, more than one bit is written into CONTROL_A reg in the same write operation, ADSP shall execute only the routine at higher priority and discard the others. Priority is listed below, with first routine at higher priority: 1. SOFT RESET routine 2. OTP WRITE routine 3. OTP TEST routine 4. OTP BOOT routine [Vpriority High] */;
        }
        requirement req_IPOS_ADSP_019 : IPOS_ADSP_019;
        doc /* iposReqId=IPOS-ADSP-019 | sourceReqId=DDS_STBIO1_0035 | If during the start of a new operation, more than one bit is written into CONTROL_A reg in the same write operation, ADSP shall execute only the routine at higher priority and discard the others. Priority is listed below, with first routine at higher priority: 1. SOFT RESET routine 2. OTP WRITE routine 3. OTP TEST routine 4. OTP BOOT routine [Vpriority High] */;
        doc /* coverageDependency: IPOS-ADSP-019 -> approved source requirement DDS_STBIO1_0035 */;
        satisfy req_IPOS_ADSP_019 by self;
    }

}

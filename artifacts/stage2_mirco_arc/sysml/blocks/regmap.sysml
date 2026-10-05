// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 5424834735474f3f97ba3357e63e8703bd7f341f5995c19ba9e75bcba49d8157

package STBIO_Block_Regmap {

    private import STBIO_Shared::*;

    part def Regmap {
        attribute displayName : String = "Regmap";
        attribute description : String = "Implement the mapped AFE, system, and OTP registers, exposing configuration/status while enforcing reset and OTP write-protection rules.";
        attribute function : String = "Implement the mapped AFE, system, and OTP registers, exposing configuration/status while enforcing reset and OTP write-protection rules.";
        attribute inputs : String = "Host read/write transactions";
        attribute outputs : String = "Register data and status fields";
        attribute approvedPortCount : Integer = 0;
        attribute linkedRequirementCount : Integer = 8;
        doc /* block=Regmap | description=Implement the mapped AFE, system, and OTP registers, exposing configuration/status while enforcing reset and OTP write-protection rules. */;
        doc /* No approved source ports are currently assigned to this block. */;
        requirement def IPOS_REGMAP_001 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_3000";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-REGMAP-001";
            doc /* 132 **Update-IR** Run-Test/Idle Select-DR-Scan 13.4. STBIO1 Register Map 13.4.1. STBIO1 Register Map Here is described the list of registers in the register map. The AFE_BLOCK registers are accessible by I2C/SPI direct access and AHB interface, while the others are only by AHB. The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers. BASE START ADDRESS ADDRESS BLOCK REGISTER WIDTH BASE END ADDRE VREF_TRIM SS RESET REQ_ID 0xC8000 AFE_BLOCK 8 0xC80EB tst_main_reset_n, regmap_sw_resetn */;
        }
        requirement req_IPOS_REGMAP_001 : IPOS_REGMAP_001;
        doc /* iposReqId=IPOS-REGMAP-001 | sourceReqId=DDS_STBIO1_3000 | 132 **Update-IR** Run-Test/Idle Select-DR-Scan 13.4. STBIO1 Register Map 13.4.1. STBIO1 Register Map Here is described the list of registers in the register map. The AFE_BLOCK registers are accessible by I2C/SPI direct access and AHB interface, while the others are only by AHB. The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers. BASE START ADDRESS ADDRESS BLOCK REGISTER WIDTH BASE END ADDRE VREF_TRIM SS RESET REQ_ID 0xC8000 AFE_BLOCK 8 0xC80EB tst_main_reset_n, regmap_sw_resetn */;
        doc /* coverageDependency: IPOS-REGMAP-001 -> approved source requirement DDS_STBIO1_3000 */;
        satisfy req_IPOS_REGMAP_001 by self;
        requirement def IPOS_REGMAP_002 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_3001";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-REGMAP-002";
            doc /* 0xC80EC RESERVED 0xC8FFF tst_main_reset_n, regmap_sw_resetn */;
        }
        requirement req_IPOS_REGMAP_002 : IPOS_REGMAP_002;
        doc /* iposReqId=IPOS-REGMAP-002 | sourceReqId=DDS_STBIO1_3001 | 0xC80EC RESERVED 0xC8FFF tst_main_reset_n, regmap_sw_resetn */;
        doc /* coverageDependency: IPOS-REGMAP-002 -> approved source requirement DDS_STBIO1_3001 */;
        satisfy req_IPOS_REGMAP_002 by self;
        requirement def IPOS_REGMAP_003 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_3002";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-REGMAP-003";
            doc /* 0xC9000 OTP REGISTER 8 0xC902C tst_main_reset_n */;
        }
        requirement req_IPOS_REGMAP_003 : IPOS_REGMAP_003;
        doc /* iposReqId=IPOS-REGMAP-003 | sourceReqId=DDS_STBIO1_3002 | 0xC9000 OTP REGISTER 8 0xC902C tst_main_reset_n */;
        doc /* coverageDependency: IPOS-REGMAP-003 -> approved source requirement DDS_STBIO1_3002 */;
        satisfy req_IPOS_REGMAP_003 by self;
        requirement def IPOS_REGMAP_004 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_3003";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-REGMAP-004";
            doc /* 0xC9030 RESERVED 0xC9FFF tst_main_reset_n, regmap_sw_resetn */;
        }
        requirement req_IPOS_REGMAP_004 : IPOS_REGMAP_004;
        doc /* iposReqId=IPOS-REGMAP-004 | sourceReqId=DDS_STBIO1_3003 | 0xC9030 RESERVED 0xC9FFF tst_main_reset_n, regmap_sw_resetn */;
        doc /* coverageDependency: IPOS-REGMAP-004 -> approved source requirement DDS_STBIO1_3003 */;
        satisfy req_IPOS_REGMAP_004 by self;
        requirement def IPOS_REGMAP_005 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_3004";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-REGMAP-005";
            doc /* 0xCA000 SYSTEM_REGISTER 32 0xCA140 tst_main_reset_n, regmap_sw_resetn */;
        }
        requirement req_IPOS_REGMAP_005 : IPOS_REGMAP_005;
        doc /* iposReqId=IPOS-REGMAP-005 | sourceReqId=DDS_STBIO1_3004 | 0xCA000 SYSTEM_REGISTER 32 0xCA140 tst_main_reset_n, regmap_sw_resetn */;
        doc /* coverageDependency: IPOS-REGMAP-005 -> approved source requirement DDS_STBIO1_3004 */;
        satisfy req_IPOS_REGMAP_005 by self;
        requirement def IPOS_REGMAP_006 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_3005";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-REGMAP-006";
            doc /* 0xCA144 RESERVED 0xCCFFF tst_main_reset_n, regmap_sw_resetn */;
        }
        requirement req_IPOS_REGMAP_006 : IPOS_REGMAP_006;
        doc /* iposReqId=IPOS-REGMAP-006 | sourceReqId=DDS_STBIO1_3005 | 0xCA144 RESERVED 0xCCFFF tst_main_reset_n, regmap_sw_resetn */;
        doc /* coverageDependency: IPOS-REGMAP-006 -> approved source requirement DDS_STBIO1_3005 */;
        satisfy req_IPOS_REGMAP_006 by self;
        requirement def IPOS_REGMAP_007 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_3006";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-REGMAP-007";
            doc /* 0xCD000 OTP (TRIMM REGS) 32 0xCD02F tst_main_reset_n, regmap_sw_resetn */;
        }
        requirement req_IPOS_REGMAP_007 : IPOS_REGMAP_007;
        doc /* iposReqId=IPOS-REGMAP-007 | sourceReqId=DDS_STBIO1_3006 | 0xCD000 OTP (TRIMM REGS) 32 0xCD02F tst_main_reset_n, regmap_sw_resetn */;
        doc /* coverageDependency: IPOS-REGMAP-007 -> approved source requirement DDS_STBIO1_3006 */;
        satisfy req_IPOS_REGMAP_007 by self;
        requirement def IPOS_REGMAP_008 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_4000";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-REGMAP-008";
            doc /* [DDS_STBIO1_4000] Requirement: Write enable for each OTP REGISTER shall be 0, in functional mode, if bit 31 of OTP_PRG10 is set 1. */;
        }
        requirement req_IPOS_REGMAP_008 : IPOS_REGMAP_008;
        doc /* iposReqId=IPOS-REGMAP-008 | sourceReqId=DDS_STBIO1_4000 | [DDS_STBIO1_4000] Requirement: Write enable for each OTP REGISTER shall be 0, in functional mode, if bit 31 of OTP_PRG10 is set 1. */;
        doc /* coverageDependency: IPOS-REGMAP-008 -> approved source requirement DDS_STBIO1_4000 */;
        satisfy req_IPOS_REGMAP_008 by self;
    }

}

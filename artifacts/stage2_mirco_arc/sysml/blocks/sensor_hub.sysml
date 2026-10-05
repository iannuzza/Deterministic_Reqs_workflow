// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 5424834735474f3f97ba3357e63e8703bd7f341f5995c19ba9e75bcba49d8157

package STBIO_Block_SensorHub {

    private import STBIO_Shared::*;

    part def SensorHub {
        attribute displayName : String = "Sensor-Hub";
        attribute description : String = "Operate the Sensor Hub I2C master for external targets, including trigger/control, pad enable, data collection, and FIFO multi-mode coordination.";
        attribute function : String = "Operate the Sensor Hub I2C master for external targets, including trigger/control, pad enable, data collection, and FIFO multi-mode coordination.";
        attribute inputs : String = "Primary sensing input";
        attribute outputs : String = "Analog input signal";
        attribute approvedPortCount : Integer = 44;
        attribute linkedRequirementCount : Integer = 18;
        doc /* block=Sensor-Hub | description=Operate the Sensor Hub I2C master for external targets, including trigger/control, pad enable, data collection, and FIFO multi-mode coordination. */;
        in port scan_mode : ArchitecturePort {
            attribute sourceName = "scan_mode";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port scan_enable : ArchitecturePort {
            attribute sourceName = "scan_enable";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port scan_rstn : ArchitecturePort {
            attribute sourceName = "scan_rstn";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port HCLKM : ArchitecturePort {
            attribute sourceName = "HCLKM";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port HCLKS : ArchitecturePort {
            attribute sourceName = "HCLKS";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port sys_clk : ArchitecturePort {
            attribute sourceName = "sys_clk";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port HRESETn : ArchitecturePort {
            attribute sourceName = "HRESETn";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port DEBUG_MODE_i : ArchitecturePort {
            attribute sourceName = "DEBUG_MODE_i";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port scl_master_in : ArchitecturePort {
            attribute sourceName = "scl_master_in";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port sda_master_in : ArchitecturePort {
            attribute sourceName = "sda_master_in";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        out port scl_master_out : ArchitecturePort {
            attribute sourceName = "scl_master_out";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        out port sda_master_out : ArchitecturePort {
            attribute sourceName = "sda_master_out";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port dvalid_masterblaze_ext : ArchitecturePort {
            attribute sourceName = "dvalid_masterblaze_ext";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port dvalid_masterblaze_ext_enable : ArchitecturePort {
            attribute sourceName = "dvalid_masterblaze_ext_enable";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        out port sleep_master : ArchitecturePort {
            attribute sourceName = "sleep_master";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        out port master_end_op_pulse : ArchitecturePort {
            attribute sourceName = "master_end_op_pulse";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port SH_SMARTFIFO_OCCUPATION : ArchitecturePort {
            attribute sourceName = "SH_SMARTFIFO_OCCUPATION";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port fifo_mode : ArchitecturePort {
            attribute sourceName = "fifo_mode";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port fifo_offset : ArchitecturePort {
            attribute sourceName = "fifo_offset";
            attribute sourceDetails = "[11:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port HSELS : ArchitecturePort {
            attribute sourceName = "HSELS";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port HADDRS : ArchitecturePort {
            attribute sourceName = "HADDRS";
            attribute sourceDetails = "[ADDRWIDTH- 1:0] 104";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "104";
        }
        in port HTRANSS : ArchitecturePort {
            attribute sourceName = "HTRANSS";
            attribute sourceDetails = "[1:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        in port HSIZES : ArchitecturePort {
            attribute sourceName = "HSIZES";
            attribute sourceDetails = "[2:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        in port HWRITES : ArchitecturePort {
            attribute sourceName = "HWRITES";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        in port HREADYS : ArchitecturePort {
            attribute sourceName = "HREADYS";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        in port HWDATAS : ArchitecturePort {
            attribute sourceName = "HWDATAS";
            attribute sourceDetails = "[31:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HREADYOUTS : ArchitecturePort {
            attribute sourceName = "HREADYOUTS";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HRESPS : ArchitecturePort {
            attribute sourceName = "HRESPS";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HRDATAS : ArchitecturePort {
            attribute sourceName = "HRDATAS";
            attribute sourceDetails = "[31:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port ahb_master_on : ArchitecturePort {
            attribute sourceName = "ahb_master_on";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        in port HRDATAM : ArchitecturePort {
            attribute sourceName = "HRDATAM";
            attribute sourceDetails = "[31:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        in port HREADYM : ArchitecturePort {
            attribute sourceName = "HREADYM";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        in port HRESPM : ArchitecturePort {
            attribute sourceName = "HRESPM";
            attribute sourceDetails = "[1:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        in port HGRANTM : ArchitecturePort {
            attribute sourceName = "HGRANTM";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HSELM : ArchitecturePort {
            attribute sourceName = "HSELM";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HADDRM : ArchitecturePort {
            attribute sourceName = "HADDRM";
            attribute sourceDetails = "[31:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HTRANSM : ArchitecturePort {
            attribute sourceName = "HTRANSM";
            attribute sourceDetails = "[1:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HWRITEM : ArchitecturePort {
            attribute sourceName = "HWRITEM";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HSIZEM : ArchitecturePort {
            attribute sourceName = "HSIZEM";
            attribute sourceDetails = "[2:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HBURSTM : ArchitecturePort {
            attribute sourceName = "HBURSTM";
            attribute sourceDetails = "[2:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HPROTM : ArchitecturePort {
            attribute sourceName = "HPROTM";
            attribute sourceDetails = "[3:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HWDATAM : ArchitecturePort {
            attribute sourceName = "HWDATAM";
            attribute sourceDetails = "[31:0]";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HBUSREQM : ArchitecturePort {
            attribute sourceName = "HBUSREQM";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }
        out port HLOCKM : ArchitecturePort {
            attribute sourceName = "HLOCKM";
            attribute sourceDetails = "";
            attribute sourceTable = "Sensor Hub I/O List";
            attribute sourcePage = "105";
        }

        requirement def IPOS_SENSOR_HUB_001 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9017";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-001";
            doc /* The output port sleep_master shall be set to 1 when an I2C operation is not on-going. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_001 : IPOS_SENSOR_HUB_001;
        doc /* iposReqId=IPOS-SENSOR-HUB-001 | sourceReqId=DDS_STBIO1_9017 | The output port sleep_master shall be set to 1 when an I2C operation is not on-going. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-001 -> approved source requirement DDS_STBIO1_9017 */;
        satisfy req_IPOS_SENSOR_HUB_001 by self;
        requirement def IPOS_SENSOR_HUB_002 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9018";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-002";
            doc /* [DDS_STBIO1_9018] Requirement The trigger of sensor hub shall be possible in both ways, HW via dvalid_masterblaze_ext signal or SW using DVALID_REGISTER. */;
        }
        requirement req_IPOS_SENSOR_HUB_002 : IPOS_SENSOR_HUB_002;
        doc /* iposReqId=IPOS-SENSOR-HUB-002 | sourceReqId=DDS_STBIO1_9018 | [DDS_STBIO1_9018] Requirement The trigger of sensor hub shall be possible in both ways, HW via dvalid_masterblaze_ext signal or SW using DVALID_REGISTER. */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-002 -> approved source requirement DDS_STBIO1_9018 */;
        satisfy req_IPOS_SENSOR_HUB_002 by self;
        requirement def IPOS_SENSOR_HUB_003 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9024";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-003";
            doc /* [DDS_STBIO1_9024] Requirement Only I2C target addressed through SLAVE0_DEV_ADD register shall be the destination of an I2C Write Operation. */;
        }
        requirement req_IPOS_SENSOR_HUB_003 : IPOS_SENSOR_HUB_003;
        doc /* iposReqId=IPOS-SENSOR-HUB-003 | sourceReqId=DDS_STBIO1_9024 | [DDS_STBIO1_9024] Requirement Only I2C target addressed through SLAVE0_DEV_ADD register shall be the destination of an I2C Write Operation. */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-003 -> approved source requirement DDS_STBIO1_9024 */;
        satisfy req_IPOS_SENSOR_HUB_003 by self;
        requirement def IPOS_SENSOR_HUB_004 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9027";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-004";
            doc /* [DDS_STBIO1_9027] Requirement The bit 0 of SLAVE1_DEV_ADD, SLAVE2_DEV_ADD, SLAVE3_DEV_ADD registers shall be ignored: ONLY read operations towards I2C target 1, 2 and 3 shall be performed. */;
        }
        requirement req_IPOS_SENSOR_HUB_004 : IPOS_SENSOR_HUB_004;
        doc /* iposReqId=IPOS-SENSOR-HUB-004 | sourceReqId=DDS_STBIO1_9027 | [DDS_STBIO1_9027] Requirement The bit 0 of SLAVE1_DEV_ADD, SLAVE2_DEV_ADD, SLAVE3_DEV_ADD registers shall be ignored: ONLY read operations towards I2C target 1, 2 and 3 shall be performed. */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-004 -> approved source requirement DDS_STBIO1_9027 */;
        satisfy req_IPOS_SENSOR_HUB_004 by self;
        requirement def IPOS_SENSOR_HUB_005 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9029";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-005";
            doc /* AUX_SENS_ON possible values shall be 0,1,2,3. All the values shall be tested since MasterBlaze supports up-to 4 I2C targets connected to I2C network. [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_005 : IPOS_SENSOR_HUB_005;
        doc /* iposReqId=IPOS-SENSOR-HUB-005 | sourceReqId=DDS_STBIO1_9029 | AUX_SENS_ON possible values shall be 0,1,2,3. All the values shall be tested since MasterBlaze supports up-to 4 I2C targets connected to I2C network. [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-005 -> approved source requirement DDS_STBIO1_9029 */;
        satisfy req_IPOS_SENSOR_HUB_005 by self;
        requirement def IPOS_SENSOR_HUB_006 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9030";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-006";
            doc /* [DDS_STBIO1_9030] Requirement SLAVEx_NUMOP bit-fields of SLAVEx_CONFIG registers shall define how many bytes per slave are read as per effect of an I2C operation (x from 1 to 12). */;
        }
        requirement req_IPOS_SENSOR_HUB_006 : IPOS_SENSOR_HUB_006;
        doc /* iposReqId=IPOS-SENSOR-HUB-006 | sourceReqId=DDS_STBIO1_9030 | [DDS_STBIO1_9030] Requirement SLAVEx_NUMOP bit-fields of SLAVEx_CONFIG registers shall define how many bytes per slave are read as per effect of an I2C operation (x from 1 to 12). */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-006 -> approved source requirement DDS_STBIO1_9030 */;
        satisfy req_IPOS_SENSOR_HUB_006 by self;
        requirement def IPOS_SENSOR_HUB_007 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9031";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-007";
            doc /* All the values from 1 to 12 shall be valid for SLAVEx_NUMOP bit-fields of SLAVEx_CONFIG registers. [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_007 : IPOS_SENSOR_HUB_007;
        doc /* iposReqId=IPOS-SENSOR-HUB-007 | sourceReqId=DDS_STBIO1_9031 | All the values from 1 to 12 shall be valid for SLAVEx_NUMOP bit-fields of SLAVEx_CONFIG registers. [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-007 -> approved source requirement DDS_STBIO1_9031 */;
        satisfy req_IPOS_SENSOR_HUB_007 by self;
        requirement def IPOS_SENSOR_HUB_008 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9032";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-008";
            doc /* [DDS_STBIO1_9032] Requirement SLAVE0_NUMOP bitfield shall be ignored if an I2C Write operation is issued to the I2C Slave 0. */;
        }
        requirement req_IPOS_SENSOR_HUB_008 : IPOS_SENSOR_HUB_008;
        doc /* iposReqId=IPOS-SENSOR-HUB-008 | sourceReqId=DDS_STBIO1_9032 | [DDS_STBIO1_9032] Requirement SLAVE0_NUMOP bitfield shall be ignored if an I2C Write operation is issued to the I2C Slave 0. */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-008 -> approved source requirement DDS_STBIO1_9032 */;
        satisfy req_IPOS_SENSOR_HUB_008 by self;
        requirement def IPOS_SENSOR_HUB_009 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9033";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-009";
            doc /* All the SENSOR_HUB_x registers shall be reset every time a new I2C operation starts. [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_009 : IPOS_SENSOR_HUB_009;
        doc /* iposReqId=IPOS-SENSOR-HUB-009 | sourceReqId=DDS_STBIO1_9033 | All the SENSOR_HUB_x registers shall be reset every time a new I2C operation starts. [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-009 -> approved source requirement DDS_STBIO1_9033 */;
        satisfy req_IPOS_SENSOR_HUB_009 by self;
        requirement def IPOS_SENSOR_HUB_010 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9034";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-010";
            doc /* The NACK_REGISTER register is reset every time a new I2C operation starts. [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_010 : IPOS_SENSOR_HUB_010;
        doc /* iposReqId=IPOS-SENSOR-HUB-010 | sourceReqId=DDS_STBIO1_9034 | The NACK_REGISTER register is reset every time a new I2C operation starts. [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-010 -> approved source requirement DDS_STBIO1_9034 */;
        satisfy req_IPOS_SENSOR_HUB_010 by self;
        requirement def IPOS_SENSOR_HUB_011 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9035";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-011";
            doc /* When Quokka MasterBlaze µP runs (sleep_master signal = 0), any dvalid triggered (HW or SW) shall be ignored. [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_011 : IPOS_SENSOR_HUB_011;
        doc /* iposReqId=IPOS-SENSOR-HUB-011 | sourceReqId=DDS_STBIO1_9035 | When Quokka MasterBlaze µP runs (sleep_master signal = 0), any dvalid triggered (HW or SW) shall be ignored. [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-011 -> approved source requirement DDS_STBIO1_9035 */;
        satisfy req_IPOS_SENSOR_HUB_011 by self;
        requirement def IPOS_SENSOR_HUB_012 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9260";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-012";
            doc /* Each data stored in FIFO shall be composed by 4 words (16bytes). [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_012 : IPOS_SENSOR_HUB_012;
        doc /* iposReqId=IPOS-SENSOR-HUB-012 | sourceReqId=DDS_STBIO1_9260 | Each data stored in FIFO shall be composed by 4 words (16bytes). [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-012 -> approved source requirement DDS_STBIO1_9260 */;
        satisfy req_IPOS_SENSOR_HUB_012 by self;
        requirement def IPOS_SENSOR_HUB_013 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9261";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-013";
            doc /* 3 words (12bytes) of the data stored in FIFO shall contain the data from each I2C slave. [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_013 : IPOS_SENSOR_HUB_013;
        doc /* iposReqId=IPOS-SENSOR-HUB-013 | sourceReqId=DDS_STBIO1_9261 | 3 words (12bytes) of the data stored in FIFO shall contain the data from each I2C slave. [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-013 -> approved source requirement DDS_STBIO1_9261 */;
        satisfy req_IPOS_SENSOR_HUB_013 by self;
        requirement def IPOS_SENSOR_HUB_014 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9262";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-014";
            doc /* 24-bits of the data stored in FIFO shall be reserved at '0'. [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_014 : IPOS_SENSOR_HUB_014;
        doc /* iposReqId=IPOS-SENSOR-HUB-014 | sourceReqId=DDS_STBIO1_9262 | 24-bits of the data stored in FIFO shall be reserved at '0'. [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-014 -> approved source requirement DDS_STBIO1_9262 */;
        satisfy req_IPOS_SENSOR_HUB_014 by self;
        requirement def IPOS_SENSOR_HUB_015 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9263";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-015";
            doc /* The last 8-bits of the data stored in FIFO shall contain the TAG field. [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_015 : IPOS_SENSOR_HUB_015;
        doc /* iposReqId=IPOS-SENSOR-HUB-015 | sourceReqId=DDS_STBIO1_9263 | The last 8-bits of the data stored in FIFO shall contain the TAG field. [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-015 -> approved source requirement DDS_STBIO1_9263 */;
        satisfy req_IPOS_SENSOR_HUB_015 by self;
        requirement def IPOS_SENSOR_HUB_016 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9300";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-016";
            doc /* [DDS_STBIO1_9300] Requirement The AHB Write to registers has no effect if the IP masterblaze processor is busy (I2C operation on-going); the registers value shall not be updated. */;
        }
        requirement req_IPOS_SENSOR_HUB_016 : IPOS_SENSOR_HUB_016;
        doc /* iposReqId=IPOS-SENSOR-HUB-016 | sourceReqId=DDS_STBIO1_9300 | [DDS_STBIO1_9300] Requirement The AHB Write to registers has no effect if the IP masterblaze processor is busy (I2C operation on-going); the registers value shall not be updated. */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-016 -> approved source requirement DDS_STBIO1_9300 */;
        satisfy req_IPOS_SENSOR_HUB_016 by self;
        requirement def IPOS_SENSOR_HUB_017 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9317";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-017";
            doc /* If the sensor hub IP is not enabled, the SCL and SDA pad shall not toggle. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_IPOS_SENSOR_HUB_017 : IPOS_SENSOR_HUB_017;
        doc /* iposReqId=IPOS-SENSOR-HUB-017 | sourceReqId=DDS_STBIO1_9317 | If the sensor hub IP is not enabled, the SCL and SDA pad shall not toggle. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-017 -> approved source requirement DDS_STBIO1_9317 */;
        satisfy req_IPOS_SENSOR_HUB_017 by self;
        requirement def IPOS_SENSOR_HUB_018 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9500";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-SENSOR-HUB-018";
            doc /* [DDS_STBIO1_9500] Requirement In case also other sources that writes into FIFO are active, then sensor hub shall work always in multi-fifo mode fifo_mode input of sensor hub set to '1' . */;
        }
        requirement req_IPOS_SENSOR_HUB_018 : IPOS_SENSOR_HUB_018;
        doc /* iposReqId=IPOS-SENSOR-HUB-018 | sourceReqId=DDS_STBIO1_9500 | [DDS_STBIO1_9500] Requirement In case also other sources that writes into FIFO are active, then sensor hub shall work always in multi-fifo mode fifo_mode input of sensor hub set to '1' . */;
        doc /* coverageDependency: IPOS-SENSOR-HUB-018 -> approved source requirement DDS_STBIO1_9500 */;
        satisfy req_IPOS_SENSOR_HUB_018 by self;
    }

}

// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 5424834735474f3f97ba3357e63e8703bd7f341f5995c19ba9e75bcba49d8157

package STBIO_DigitalSubsystem {

    private import STBIO_Shared::*;

    private import STBIO_Block_ADSP::*;
    private import STBIO_Block_BISTController::*;
    private import STBIO_Block_I2CSPIAHB::*;
    private import STBIO_Block_IRQLogic::*;
    private import STBIO_Block_ISPU::*;
    private import STBIO_Block_MainController::*;
    private import STBIO_Block_OTP::*;
    private import STBIO_Block_PMU::*;
    private import STBIO_Block_PadMux::*;
    private import STBIO_Block_Regmap::*;
    private import STBIO_Block_SensorHub::*;
    private import STBIO_Block_SmartFIFO::*;

    part def DigitalSubsystem {
        attribute displayName : String = "Digital Subsystem";
        requirement def DRS_REQ_001 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0206";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-001";
            doc /* The digital subsystem shall satisfy the following behavior: ADSP. */;
        }
        requirement req_DRS_REQ_001 : DRS_REQ_001;
        doc /* drsReqId=DRS-REQ-001 | sourceReqId=DDS_STBIO1_0206 | The digital subsystem shall satisfy the following behavior: ADSP. */;
        doc /* coverageDependency: DRS-REQ-001 -> approved source requirement DDS_STBIO1_0206 */;
        satisfy req_DRS_REQ_001 by self;
        requirement def DRS_REQ_002 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0508";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-002";
            doc /* To turn off the ISPU shall be: • Disable the power island by writing to regmap POWER CONFIGURATION REGISTER via AHB interface (ADDRESS=0xCA000, DATA=0x00) */;
        }
        requirement req_DRS_REQ_002 : DRS_REQ_002;
        doc /* drsReqId=DRS-REQ-002 | sourceReqId=DDS_STBIO1_0508 | To turn off the ISPU shall be: • Disable the power island by writing to regmap POWER CONFIGURATION REGISTER via AHB interface (ADDRESS=0xCA000, DATA=0x00) */;
        doc /* coverageDependency: DRS-REQ-002 -> approved source requirement DDS_STBIO1_0508 */;
        satisfy req_DRS_REQ_002 by self;
        requirement def DRS_REQ_003 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0507";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-003";
            doc /* After the initial boot phase, to turn on the ISPU shall be: • Select page 3 of the regmap (ADDRESS=0x04, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable user mode by writing to regmap (ADDRESS=0x5E, DATA=0x01) • Enable the power island by writing to regmap POWER CONFIGURATION REGISTER via AHB interface (ADDRESS=0xCA000, DATA=0x01) */;
        }
        requirement req_DRS_REQ_003 : DRS_REQ_003;
        doc /* drsReqId=DRS-REQ-003 | sourceReqId=DDS_STBIO1_0507 | After the initial boot phase, to turn on the ISPU shall be: • Select page 3 of the regmap (ADDRESS=0x04, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable user mode by writing to regmap (ADDRESS=0x5E, DATA=0x01) • Enable the power island by writing to regmap POWER CONFIGURATION REGISTER via AHB interface (ADDRESS=0xCA000, DATA=0x01) */;
        doc /* coverageDependency: DRS-REQ-003 -> approved source requirement DDS_STBIO1_0507 */;
        satisfy req_DRS_REQ_003 by self;
        requirement def DRS_REQ_004 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0208";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-004";
            doc /* The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        }
        requirement req_DRS_REQ_004 : DRS_REQ_004;
        doc /* drsReqId=DRS-REQ-004 | sourceReqId=DDS_STBIO1_0208 | The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        doc /* coverageDependency: DRS-REQ-004 -> approved source requirement DDS_STBIO1_0208 */;
        satisfy req_DRS_REQ_004 by self;
        requirement def DRS_REQ_005 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0505";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-005";
            doc /* The irq_timer interrupt shall be connected to Internal timer to bit 1. */;
        }
        requirement req_DRS_REQ_005 : DRS_REQ_005;
        doc /* drsReqId=DRS-REQ-005 | sourceReqId=DDS_STBIO1_0505 | The irq_timer interrupt shall be connected to Internal timer to bit 1. */;
        doc /* coverageDependency: DRS-REQ-005 -> approved source requirement DDS_STBIO1_0505 */;
        satisfy req_DRS_REQ_005 by self;
        requirement def DRS_REQ_006 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0142";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-006";
            doc /* • To check data in unique FIFO (default config) the user shall check the first MSB which will have to be equal to the one described in the DATA TAG Table. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_DRS_REQ_006 : DRS_REQ_006;
        doc /* drsReqId=DRS-REQ-006 | sourceReqId=DDS_STBIO1_0142 | • To check data in unique FIFO (default config) the user shall check the first MSB which will have to be equal to the one described in the DATA TAG Table. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: DRS-REQ-006 -> approved source requirement DDS_STBIO1_0142 */;
        satisfy req_DRS_REQ_006 by self;
        requirement def DRS_REQ_007 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9012";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-007";
            doc /* Input sda_master_in of sensor hub shall be connected to input buffer from sensor hub's SDA PAD. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_DRS_REQ_007 : DRS_REQ_007;
        doc /* drsReqId=DRS-REQ-007 | sourceReqId=DDS_STBIO1_9012 | Input sda_master_in of sensor hub shall be connected to input buffer from sensor hub's SDA PAD. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: DRS-REQ-007 -> approved source requirement DDS_STBIO1_9012 */;
        satisfy req_DRS_REQ_007 by self;
        requirement def DRS_REQ_008 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0222";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-008";
            doc /* The digital subsystem shall satisfy the following behavior: ISPU. */;
        }
        requirement req_DRS_REQ_008 : DRS_REQ_008;
        doc /* drsReqId=DRS-REQ-008 | sourceReqId=DDS_STBIO1_0222 | The digital subsystem shall satisfy the following behavior: ISPU. */;
        doc /* coverageDependency: DRS-REQ-008 -> approved source requirement DDS_STBIO1_0222 */;
        satisfy req_DRS_REQ_008 by self;
        requirement def DRS_REQ_009 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0143";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-009";
            doc /* [DDS_STBIO1_0143] Requirement: • The User shall configure time slot duration in DEVICE_CONFIG_OPERATION register [4:2]. */;
        }
        requirement req_DRS_REQ_009 : DRS_REQ_009;
        doc /* drsReqId=DRS-REQ-009 | sourceReqId=DDS_STBIO1_0143 | [DDS_STBIO1_0143] Requirement: • The User shall configure time slot duration in DEVICE_CONFIG_OPERATION register [4:2]. */;
        doc /* coverageDependency: DRS-REQ-009 -> approved source requirement DDS_STBIO1_0143 */;
        satisfy req_DRS_REQ_009 by self;
        requirement def DRS_REQ_010 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0207";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-010";
            doc /* The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        }
        requirement req_DRS_REQ_010 : DRS_REQ_010;
        doc /* drsReqId=DRS-REQ-010 | sourceReqId=DDS_STBIO1_0207 | The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        doc /* coverageDependency: DRS-REQ-010 -> approved source requirement DDS_STBIO1_0207 */;
        satisfy req_DRS_REQ_010 by self;
        requirement def DRS_REQ_011 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0701";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-011";
            doc /* To turn on the ADC TEST LOW NOISE mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0xF, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable ADC in debug mode (ADDRESS=0x09, DATA=0x06) • Select page 2 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable ADC TEST LOW NOISE and input of ADC from GPIO (ADDRESS=0x0A, DATA=0x14) • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) */;
        }
        requirement req_DRS_REQ_011 : DRS_REQ_011;
        doc /* drsReqId=DRS-REQ-011 | sourceReqId=DDS_STBIO1_0701 | To turn on the ADC TEST LOW NOISE mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0xF, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable ADC in debug mode (ADDRESS=0x09, DATA=0x06) • Select page 2 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable ADC TEST LOW NOISE and input of ADC from GPIO (ADDRESS=0x0A, DATA=0x14) • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) */;
        doc /* coverageDependency: DRS-REQ-011 -> approved source requirement DDS_STBIO1_0701 */;
        satisfy req_DRS_REQ_011 by self;
        requirement def DRS_REQ_012 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0700";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-012";
            doc /* After the initial boot phase, to turn on the Debug mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) */;
        }
        requirement req_DRS_REQ_012 : DRS_REQ_012;
        doc /* drsReqId=DRS-REQ-012 | sourceReqId=DDS_STBIO1_0700 | After the initial boot phase, to turn on the Debug mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) */;
        doc /* coverageDependency: DRS-REQ-012 -> approved source requirement DDS_STBIO1_0700 */;
        satisfy req_DRS_REQ_012 by self;
        requirement def DRS_REQ_013 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0201";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-013";
            doc /* The digital subsystem shall satisfy the following behavior: 11.1. XBAR Connection Matrix Destination Source Regmap SENSOR HUB ISPU FIFO ADSP Main Controller. */;
        }
        requirement req_DRS_REQ_013 : DRS_REQ_013;
        doc /* drsReqId=DRS-REQ-013 | sourceReqId=DDS_STBIO1_0201 | The digital subsystem shall satisfy the following behavior: 11.1. XBAR Connection Matrix Destination Source Regmap SENSOR HUB ISPU FIFO ADSP Main Controller. */;
        doc /* coverageDependency: DRS-REQ-013 -> approved source requirement DDS_STBIO1_0201 */;
        satisfy req_DRS_REQ_013 by self;
        requirement def DRS_REQ_014 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0217";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-014";
            doc /* The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        }
        requirement req_DRS_REQ_014 : DRS_REQ_014;
        doc /* drsReqId=DRS-REQ-014 | sourceReqId=DDS_STBIO1_0217 | The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        doc /* coverageDependency: DRS-REQ-014 -> approved source requirement DDS_STBIO1_0217 */;
        satisfy req_DRS_REQ_014 by self;
        requirement def DRS_REQ_015 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0147";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-015";
            doc /* The user shall configure each frame following these steps: 5.1 ALC PARAMETERS: • T1 in PPG_ALC_CONFIG_PARAM_1 register. • T2, GAIN_START_SET, GAIN_MAX_SET in PPG_ALC_CONFIG_PARAM_2 register. 5.2 DIGITAL RAMP PARAMETERS: • N_MAX, T_DELTA in DIGITAL_RAMP_CONFIG_PARAM_1 register. • DELTA, T_DELTA1 in DIGITAL_RAMP_CONFIG_PARAM_2 register. • DELTA1 in DIGITAL_RAMP_CONFIG_PARAM_3 register. 5.3 GENERAL PPG PARAMETERS: • N_PPG_FRAME, WAVE_VELOCITY_MODE, SEL_PPG_ELAB in GENERAL_PPG_PARAMETERS_1 register. • T_TX_STARTUP in GENERAL_PPG_PARAMETERS_2 register. • T_RX_SET, PPG_START_UP_TIME_l in GENERAL_PPG_PARAMETERS_3 register. • PPG_START_UP_TIME_h in GENERAL_PPG_PARAMETERS_4 register. 5.4 PARAMETERS FOR EACH FRAME CONFIGURED BY USER: • RX_CH_FRAME_{n}, FRAME_{n}_SAMPLES, FRAME_{n}_REPETITION in FRAME_n_PARAMETERS_1 register. • BTIA_GAIN_FRAME_{n}, TX_LEDSET_FRAME_l_{n} in FRAME_n_PARAMETERS_2 register. • TX_LEDSET_FRAME_h_{n}, TX_LEDOFF_FRAME_l_{n} in FRAME_n_PARAMETERS_3 register. • TX_LEDOFF_FRAME_h_{n} in FRAME_n_PARAMETERS_4 register. • IDAC_DC_PPG_FRAME_{n} in FRAME_n_PARAMETERS_5 register. • EN_TX_i in FRAME_n_PARAMETERS_6 register. • CURR_SEL_TX_FRAME{n} in FRAME_n_PARAMETERS_7 register. • TX1_OUTAB_SEL_FRAME_{n}, TX2_OUTAB_SEL_FRAME_{n}, TX3_OUTAB_SEL_FRAME_{n}, TX4_OUTAB_SEL_FRAME_{n} in FRAME_n_PARAMETERS_10 register. */;
        }
        requirement req_DRS_REQ_015 : DRS_REQ_015;
        doc /* drsReqId=DRS-REQ-015 | sourceReqId=DDS_STBIO1_0147 | The user shall configure each frame following these steps: 5.1 ALC PARAMETERS: • T1 in PPG_ALC_CONFIG_PARAM_1 register. • T2, GAIN_START_SET, GAIN_MAX_SET in PPG_ALC_CONFIG_PARAM_2 register. 5.2 DIGITAL RAMP PARAMETERS: • N_MAX, T_DELTA in DIGITAL_RAMP_CONFIG_PARAM_1 register. • DELTA, T_DELTA1 in DIGITAL_RAMP_CONFIG_PARAM_2 register. • DELTA1 in DIGITAL_RAMP_CONFIG_PARAM_3 register. 5.3 GENERAL PPG PARAMETERS: • N_PPG_FRAME, WAVE_VELOCITY_MODE, SEL_PPG_ELAB in GENERAL_PPG_PARAMETERS_1 register. • T_TX_STARTUP in GENERAL_PPG_PARAMETERS_2 register. • T_RX_SET, PPG_START_UP_TIME_l in GENERAL_PPG_PARAMETERS_3 register. • PPG_START_UP_TIME_h in GENERAL_PPG_PARAMETERS_4 register. 5.4 PARAMETERS FOR EACH FRAME CONFIGURED BY USER: • RX_CH_FRAME_{n}, FRAME_{n}_SAMPLES, FRAME_{n}_REPETITION in FRAME_n_PARAMETERS_1 register. • BTIA_GAIN_FRAME_{n}, TX_LEDSET_FRAME_l_{n} in FRAME_n_PARAMETERS_2 register. • TX_LEDSET_FRAME_h_{n}, TX_LEDOFF_FRAME_l_{n} in FRAME_n_PARAMETERS_3 register. • TX_LEDOFF_FRAME_h_{n} in FRAME_n_PARAMETERS_4 register. • IDAC_DC_PPG_FRAME_{n} in FRAME_n_PARAMETERS_5 register. • EN_TX_i in FRAME_n_PARAMETERS_6 register. • CURR_SEL_TX_FRAME{n} in FRAME_n_PARAMETERS_7 register. • TX1_OUTAB_SEL_FRAME_{n}, TX2_OUTAB_SEL_FRAME_{n}, TX3_OUTAB_SEL_FRAME_{n}, TX4_OUTAB_SEL_FRAME_{n} in FRAME_n_PARAMETERS_10 register. */;
        doc /* coverageDependency: DRS-REQ-015 -> approved source requirement DDS_STBIO1_0147 */;
        satisfy req_DRS_REQ_015 by self;
        requirement def DRS_REQ_016 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1507";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-016";
            doc /* To turn on the ADC TEST LOW NOISE mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0xF, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable ADC in debug mode (ADDRESS=0x09, DATA=0x06) • Select page 2 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable ADC TEST LOW NOISE and input of ADC from GPIO (ADDRESS=0x0A, DATA=0x0C) • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) */;
        }
        requirement req_DRS_REQ_016 : DRS_REQ_016;
        doc /* drsReqId=DRS-REQ-016 | sourceReqId=DDS_STBIO1_1507 | To turn on the ADC TEST LOW NOISE mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0xF, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable ADC in debug mode (ADDRESS=0x09, DATA=0x06) • Select page 2 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable ADC TEST LOW NOISE and input of ADC from GPIO (ADDRESS=0x0A, DATA=0x0C) • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) */;
        doc /* coverageDependency: DRS-REQ-016 -> approved source requirement DDS_STBIO1_1507 */;
        satisfy req_DRS_REQ_016 by self;
        requirement def DRS_REQ_017 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0141";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-017";
            doc /* • The user shall start measurement writing register DEVICE_CONFIG_OPERATION [0] at 1. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_DRS_REQ_017 : DRS_REQ_017;
        doc /* drsReqId=DRS-REQ-017 | sourceReqId=DDS_STBIO1_0141 | • The user shall start measurement writing register DEVICE_CONFIG_OPERATION [0] at 1. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: DRS-REQ-017 -> approved source requirement DDS_STBIO1_0141 */;
        satisfy req_DRS_REQ_017 by self;
        requirement def DRS_REQ_018 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0209";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-018";
            doc /* The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        }
        requirement req_DRS_REQ_018 : DRS_REQ_018;
        doc /* drsReqId=DRS-REQ-018 | sourceReqId=DDS_STBIO1_0209 | The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        doc /* coverageDependency: DRS-REQ-018 -> approved source requirement DDS_STBIO1_0209 */;
        satisfy req_DRS_REQ_018 by self;
        requirement def DRS_REQ_019 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0149";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-019";
            doc /* • To check data in unique FIFO (default config) the user shall check the first MSB. PPG DATA has 20 bits of data and 4 of TAG. The 4 bits, from 0 to 11, are used to identify the frame (as described in the table in DATA TAG table). */;
        }
        requirement req_DRS_REQ_019 : DRS_REQ_019;
        doc /* drsReqId=DRS-REQ-019 | sourceReqId=DDS_STBIO1_0149 | • To check data in unique FIFO (default config) the user shall check the first MSB. PPG DATA has 20 bits of data and 4 of TAG. The 4 bits, from 0 to 11, are used to identify the frame (as described in the table in DATA TAG table). */;
        doc /* coverageDependency: DRS-REQ-019 -> approved source requirement DDS_STBIO1_0149 */;
        satisfy req_DRS_REQ_019 by self;
        requirement def DRS_REQ_020 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0032";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-020";
            doc /* After each Boot routine performed by the ADSP, a value of 0x04 shall be written once to address 0x0CA00C to ensure correct operation of the AHB transactions. [Vpriority High] */;
        }
        requirement req_DRS_REQ_020 : DRS_REQ_020;
        doc /* drsReqId=DRS-REQ-020 | sourceReqId=DDS_STBIO1_0032 | After each Boot routine performed by the ADSP, a value of 0x04 shall be written once to address 0x0CA00C to ensure correct operation of the AHB transactions. [Vpriority High] */;
        doc /* coverageDependency: DRS-REQ-020 -> approved source requirement DDS_STBIO1_0032 */;
        satisfy req_DRS_REQ_020 by self;
        requirement def DRS_REQ_021 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0215";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-021";
            doc /* The digital subsystem shall satisfy the following behavior: ISPU. */;
        }
        requirement req_DRS_REQ_021 : DRS_REQ_021;
        doc /* drsReqId=DRS-REQ-021 | sourceReqId=DDS_STBIO1_0215 | The digital subsystem shall satisfy the following behavior: ISPU. */;
        doc /* coverageDependency: DRS-REQ-021 -> approved source requirement DDS_STBIO1_0215 */;
        satisfy req_DRS_REQ_021 by self;
        requirement def DRS_REQ_022 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0210";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-022";
            doc /* The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        }
        requirement req_DRS_REQ_022 : DRS_REQ_022;
        doc /* drsReqId=DRS-REQ-022 | sourceReqId=DDS_STBIO1_0210 | The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        doc /* coverageDependency: DRS-REQ-022 -> approved source requirement DDS_STBIO1_0210 */;
        satisfy req_DRS_REQ_022 by self;
        requirement def DRS_REQ_023 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9004";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-023";
            doc /* Input sys_clk of sensor hub shall be connected to 8MHz clock to generate I2C communications compliant with FM+ I2C standard. [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_DRS_REQ_023 : DRS_REQ_023;
        doc /* drsReqId=DRS-REQ-023 | sourceReqId=DDS_STBIO1_9004 | Input sys_clk of sensor hub shall be connected to 8MHz clock to generate I2C communications compliant with FM+ I2C standard. [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: DRS-REQ-023 -> approved source requirement DDS_STBIO1_9004 */;
        satisfy req_DRS_REQ_023 by self;
        requirement def DRS_REQ_024 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0220";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-024";
            doc /* The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        }
        requirement req_DRS_REQ_024 : DRS_REQ_024;
        doc /* drsReqId=DRS-REQ-024 | sourceReqId=DDS_STBIO1_0220 | The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        doc /* coverageDependency: DRS-REQ-024 -> approved source requirement DDS_STBIO1_0220 */;
        satisfy req_DRS_REQ_024 by self;
        requirement def DRS_REQ_025 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0221";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-025";
            doc /* The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        }
        requirement req_DRS_REQ_025 : DRS_REQ_025;
        doc /* drsReqId=DRS-REQ-025 | sourceReqId=DDS_STBIO1_0221 | The digital subsystem shall satisfy the following behavior: I2C_SPI_AHB. */;
        doc /* coverageDependency: DRS-REQ-025 -> approved source requirement DDS_STBIO1_0221 */;
        satisfy req_DRS_REQ_025 by self;
        requirement def DRS_REQ_026 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0501";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-026";
            doc /* The irq_FIFO_U_M_IRQ_STsATUS interrupt shall be connected to FIFO status to bit 29. */;
        }
        requirement req_DRS_REQ_026 : DRS_REQ_026;
        doc /* drsReqId=DRS-REQ-026 | sourceReqId=DDS_STBIO1_0501 | The irq_FIFO_U_M_IRQ_STsATUS interrupt shall be connected to FIFO status to bit 29. */;
        doc /* coverageDependency: DRS-REQ-026 -> approved source requirement DDS_STBIO1_0501 */;
        satisfy req_DRS_REQ_026 by self;
        requirement def DRS_REQ_027 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0212";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-027";
            doc /* The digital subsystem shall satisfy the following behavior: ISPU. */;
        }
        requirement req_DRS_REQ_027 : DRS_REQ_027;
        doc /* drsReqId=DRS-REQ-027 | sourceReqId=DDS_STBIO1_0212 | The digital subsystem shall satisfy the following behavior: ISPU. */;
        doc /* coverageDependency: DRS-REQ-027 -> approved source requirement DDS_STBIO1_0212 */;
        satisfy req_DRS_REQ_027 by self;
        requirement def DRS_REQ_028 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0145";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-028";
            doc /* [DDS_STBIO1_0145] Requirement: • The user shall configure a division index PPG, writing M_PPG_l and M_PPG_h in SET_PPG_FREQ_l register and SET_PPG_FREQ_h register. */;
        }
        requirement req_DRS_REQ_028 : DRS_REQ_028;
        doc /* drsReqId=DRS-REQ-028 | sourceReqId=DDS_STBIO1_0145 | [DDS_STBIO1_0145] Requirement: • The user shall configure a division index PPG, writing M_PPG_l and M_PPG_h in SET_PPG_FREQ_l register and SET_PPG_FREQ_h register. */;
        doc /* coverageDependency: DRS-REQ-028 -> approved source requirement DDS_STBIO1_0145 */;
        satisfy req_DRS_REQ_028 by self;
        requirement def DRS_REQ_029 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1114";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-029";
            doc /* To perform a SOFT Reset procedure, the user shall perform the following steps: 1. If Mode Operation has been set to 1, shall be reset to 0 2. Set the Soft Reset Main Controller Bit (SW_RESETN_REG[0]) to 0 for at least 1 ms 3. Set the Soft Reset Main Controller Bit (SW_RESETN_REG[0]) to 1 4. Wait for the DEVICE_STATUS_REGISTER to reach the IDLE Value */;
        }
        requirement req_DRS_REQ_029 : DRS_REQ_029;
        doc /* drsReqId=DRS-REQ-029 | sourceReqId=DDS_STBIO1_1114 | To perform a SOFT Reset procedure, the user shall perform the following steps: 1. If Mode Operation has been set to 1, shall be reset to 0 2. Set the Soft Reset Main Controller Bit (SW_RESETN_REG[0]) to 0 for at least 1 ms 3. Set the Soft Reset Main Controller Bit (SW_RESETN_REG[0]) to 1 4. Wait for the DEVICE_STATUS_REGISTER to reach the IDLE Value */;
        doc /* coverageDependency: DRS-REQ-029 -> approved source requirement DDS_STBIO1_1114 */;
        satisfy req_DRS_REQ_029 by self;
        requirement def DRS_REQ_030 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0216";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-030";
            doc /* The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        }
        requirement req_DRS_REQ_030 : DRS_REQ_030;
        doc /* drsReqId=DRS-REQ-030 | sourceReqId=DDS_STBIO1_0216 | The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        doc /* coverageDependency: DRS-REQ-030 -> approved source requirement DDS_STBIO1_0216 */;
        satisfy req_DRS_REQ_030 by self;
        requirement def DRS_REQ_031 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0504";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-031";
            doc /* The sw_interrupt interrupt shall be connected to sw interrupt used by ADSP or external user to bit 26:11 16. */;
        }
        requirement req_DRS_REQ_031 : DRS_REQ_031;
        doc /* drsReqId=DRS-REQ-031 | sourceReqId=DDS_STBIO1_0504 | The sw_interrupt interrupt shall be connected to sw interrupt used by ADSP or external user to bit 26:11 16. */;
        doc /* coverageDependency: DRS-REQ-031 -> approved source requirement DDS_STBIO1_0504 */;
        satisfy req_DRS_REQ_031 by self;
        requirement def DRS_REQ_032 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0509";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-032";
            doc /* The digital subsystem shall satisfy the following behavior: [DDS_STBIO1_0509] Requirement: To put the ISPU into sleep mode, it is necessary to perform a read at address 0x80054. */;
        }
        requirement req_DRS_REQ_032 : DRS_REQ_032;
        doc /* drsReqId=DRS-REQ-032 | sourceReqId=DDS_STBIO1_0509 | The digital subsystem shall satisfy the following behavior: [DDS_STBIO1_0509] Requirement: To put the ISPU into sleep mode, it is necessary to perform a read at address 0x80054. */;
        doc /* coverageDependency: DRS-REQ-032 -> approved source requirement DDS_STBIO1_0509 */;
        satisfy req_DRS_REQ_032 by self;
        requirement def DRS_REQ_033 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0219";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-033";
            doc /* The digital subsystem shall satisfy the following behavior: 11.1. XBAR Connection Matrix Destination Source Regmap SENSOR HUB ISPU FIFO ADSP Main Controller. */;
        }
        requirement req_DRS_REQ_033 : DRS_REQ_033;
        doc /* drsReqId=DRS-REQ-033 | sourceReqId=DDS_STBIO1_0219 | The digital subsystem shall satisfy the following behavior: 11.1. XBAR Connection Matrix Destination Source Regmap SENSOR HUB ISPU FIFO ADSP Main Controller. */;
        doc /* coverageDependency: DRS-REQ-033 -> approved source requirement DDS_STBIO1_0219 */;
        satisfy req_DRS_REQ_033 by self;
        requirement def DRS_REQ_034 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0699";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-034";
            doc /* After the initial boot phase, only with SPI interface, to turn on the Scan mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x01) Figure 26 scan mode activation timing */;
        }
        requirement req_DRS_REQ_034 : DRS_REQ_034;
        doc /* drsReqId=DRS-REQ-034 | sourceReqId=DDS_STBIO1_0699 | After the initial boot phase, only with SPI interface, to turn on the Scan mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x01) Figure 26 scan mode activation timing */;
        doc /* coverageDependency: DRS-REQ-034 -> approved source requirement DDS_STBIO1_0699 */;
        satisfy req_DRS_REQ_034 by self;
        requirement def DRS_REQ_035 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0116";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-035";
            doc /* To check the end of the BOOT phase, the user shall read the main_controller_status_register (DEVICE_STATUS_REG register [2:0]) and follow these steps: • Read the DEVICE_STATUS_REG [2:0] • Check if the Value is 1 (BOOT phase still in process) • If the value is 2, then the BOOT phase is ended and the device is in IDLE. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_DRS_REQ_035 : DRS_REQ_035;
        doc /* drsReqId=DRS-REQ-035 | sourceReqId=DDS_STBIO1_0116 | To check the end of the BOOT phase, the user shall read the main_controller_status_register (DEVICE_STATUS_REG register [2:0]) and follow these steps: • Read the DEVICE_STATUS_REG [2:0] • Check if the Value is 1 (BOOT phase still in process) • If the value is 2, then the BOOT phase is ended and the device is in IDLE. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: DRS-REQ-035 -> approved source requirement DDS_STBIO1_0116 */;
        satisfy req_DRS_REQ_035 by self;
        requirement def DRS_REQ_036 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_2507";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-036";
            doc /* After the initial boot phase, to turn on the Debug mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable the power island [DDS_STBIO1_0507] • Enable bist mode by writing to regmap (ADDRESS=0x3E, DATA=0x04) */;
        }
        requirement req_DRS_REQ_036 : DRS_REQ_036;
        doc /* drsReqId=DRS-REQ-036 | sourceReqId=DDS_STBIO1_2507 | After the initial boot phase, to turn on the Debug mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable the power island [DDS_STBIO1_0507] • Enable bist mode by writing to regmap (ADDRESS=0x3E, DATA=0x04) */;
        doc /* coverageDependency: DRS-REQ-036 -> approved source requirement DDS_STBIO1_2507 */;
        satisfy req_DRS_REQ_036 by self;
        requirement def DRS_REQ_037 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0204";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-037";
            doc /* The digital subsystem shall satisfy the following behavior: ADSP. */;
        }
        requirement req_DRS_REQ_037 : DRS_REQ_037;
        doc /* drsReqId=DRS-REQ-037 | sourceReqId=DDS_STBIO1_0204 | The digital subsystem shall satisfy the following behavior: ADSP. */;
        doc /* coverageDependency: DRS-REQ-037 -> approved source requirement DDS_STBIO1_0204 */;
        satisfy req_DRS_REQ_037 by self;
        requirement def DRS_REQ_038 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0146";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-038";
            doc /* [DDS_STBIO1_0146] Requirement: • The user shall configure the number of clocks for sampling PPG data from ADC in ADC_CONFIG_PPG register. */;
        }
        requirement req_DRS_REQ_038 : DRS_REQ_038;
        doc /* drsReqId=DRS-REQ-038 | sourceReqId=DDS_STBIO1_0146 | [DDS_STBIO1_0146] Requirement: • The user shall configure the number of clocks for sampling PPG data from ADC in ADC_CONFIG_PPG register. */;
        doc /* coverageDependency: DRS-REQ-038 -> approved source requirement DDS_STBIO1_0146 */;
        satisfy req_DRS_REQ_038 by self;
        requirement def DRS_REQ_039 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0202";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-039";
            doc /* The digital subsystem shall satisfy the following behavior: 11.1. XBAR Connection Matrix Destination Source Regmap SENSOR HUB ISPU FIFO ADSP Main Controller. */;
        }
        requirement req_DRS_REQ_039 : DRS_REQ_039;
        doc /* drsReqId=DRS-REQ-039 | sourceReqId=DDS_STBIO1_0202 | The digital subsystem shall satisfy the following behavior: 11.1. XBAR Connection Matrix Destination Source Regmap SENSOR HUB ISPU FIFO ADSP Main Controller. */;
        doc /* coverageDependency: DRS-REQ-039 -> approved source requirement DDS_STBIO1_0202 */;
        satisfy req_DRS_REQ_039 by self;
        requirement def DRS_REQ_040 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9014";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-040";
            doc /* Output sda_master_out of sensor hub shall be connected to enable of output buffer of sensor hub's SDA PAD. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_DRS_REQ_040 : DRS_REQ_040;
        doc /* drsReqId=DRS-REQ-040 | sourceReqId=DDS_STBIO1_9014 | Output sda_master_out of sensor hub shall be connected to enable of output buffer of sensor hub's SDA PAD. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: DRS-REQ-040 -> approved source requirement DDS_STBIO1_9014 */;
        satisfy req_DRS_REQ_040 by self;
        requirement def DRS_REQ_041 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0211";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-041";
            doc /* The digital subsystem shall satisfy the following behavior: SENSOR HUB. */;
        }
        requirement req_DRS_REQ_041 : DRS_REQ_041;
        doc /* drsReqId=DRS-REQ-041 | sourceReqId=DDS_STBIO1_0211 | The digital subsystem shall satisfy the following behavior: SENSOR HUB. */;
        doc /* coverageDependency: DRS-REQ-041 -> approved source requirement DDS_STBIO1_0211 */;
        satisfy req_DRS_REQ_041 by self;
        requirement def DRS_REQ_042 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0203";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-042";
            doc /* The digital subsystem shall satisfy the following behavior: ADSP. */;
        }
        requirement req_DRS_REQ_042 : DRS_REQ_042;
        doc /* drsReqId=DRS-REQ-042 | sourceReqId=DDS_STBIO1_0203 | The digital subsystem shall satisfy the following behavior: ADSP. */;
        doc /* coverageDependency: DRS-REQ-042 -> approved source requirement DDS_STBIO1_0203 */;
        satisfy req_DRS_REQ_042 by self;
        requirement def DRS_REQ_043 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0148";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-043";
            doc /* [DDS_STBIO1_0148] Requirement: • The user shall write DEVICE_CONFIG_OPERATION register [0] at 1. */;
        }
        requirement req_DRS_REQ_043 : DRS_REQ_043;
        doc /* drsReqId=DRS-REQ-043 | sourceReqId=DDS_STBIO1_0148 | [DDS_STBIO1_0148] Requirement: • The user shall write DEVICE_CONFIG_OPERATION register [0] at 1. */;
        doc /* coverageDependency: DRS-REQ-043 -> approved source requirement DDS_STBIO1_0148 */;
        satisfy req_DRS_REQ_043 by self;
        requirement def DRS_REQ_044 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9011";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-044";
            doc /* Input scl_master_in of sensor hub shall be connected to input buffer from sensor hub's SCL PAD. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_DRS_REQ_044 : DRS_REQ_044;
        doc /* drsReqId=DRS-REQ-044 | sourceReqId=DDS_STBIO1_9011 | Input scl_master_in of sensor hub shall be connected to input buffer from sensor hub's SCL PAD. [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: DRS-REQ-044 -> approved source requirement DDS_STBIO1_9011 */;
        satisfy req_DRS_REQ_044 by self;
        requirement def DRS_REQ_045 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0502";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-045";
            doc /* The irq_SENSHUB_STS interrupt shall be connected to SENSOR HUB status to bit 28. */;
        }
        requirement req_DRS_REQ_045 : DRS_REQ_045;
        doc /* drsReqId=DRS-REQ-045 | sourceReqId=DDS_STBIO1_0502 | The irq_SENSHUB_STS interrupt shall be connected to SENSOR HUB status to bit 28. */;
        doc /* coverageDependency: DRS-REQ-045 -> approved source requirement DDS_STBIO1_0502 */;
        satisfy req_DRS_REQ_045 by self;
        requirement def DRS_REQ_046 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_05010";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-046";
            doc /* The digital subsystem shall satisfy the following behavior: [DDS_STBIO1_05010] Requirement: To wake up the ISPU, it is necessary to trigger an interrupt. */;
        }
        requirement req_DRS_REQ_046 : DRS_REQ_046;
        doc /* drsReqId=DRS-REQ-046 | sourceReqId=DDS_STBIO1_05010 | The digital subsystem shall satisfy the following behavior: [DDS_STBIO1_05010] Requirement: To wake up the ISPU, it is necessary to trigger an interrupt. */;
        doc /* coverageDependency: DRS-REQ-046 -> approved source requirement DDS_STBIO1_05010 */;
        satisfy req_DRS_REQ_046 by self;
        requirement def DRS_REQ_047 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_9013";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-047";
            doc /* Output scl_master_out of sensor hub shall be connected to enable of output buffer of sensor hub's SCL PAD in case it is a bi-directional PAD). [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        }
        requirement req_DRS_REQ_047 : DRS_REQ_047;
        doc /* drsReqId=DRS-REQ-047 | sourceReqId=DDS_STBIO1_9013 | Output scl_master_out of sensor hub shall be connected to enable of output buffer of sensor hub's SCL PAD in case it is a bi-directional PAD). [Vpriority High] [TO: IPOS_Senshub_MB_i2c] */;
        doc /* coverageDependency: DRS-REQ-047 -> approved source requirement DDS_STBIO1_9013 */;
        satisfy req_DRS_REQ_047 by self;
        requirement def DRS_REQ_048 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_05011";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-048";
            doc /* The digital subsystem shall satisfy the following behavior: [DDS_STBIO1_05011] Requirement: When the ISPU is in sleep mode, it is possible to perform reads and writes from the data and code memory by triggering an AHB transition. */;
        }
        requirement req_DRS_REQ_048 : DRS_REQ_048;
        doc /* drsReqId=DRS-REQ-048 | sourceReqId=DDS_STBIO1_05011 | The digital subsystem shall satisfy the following behavior: [DDS_STBIO1_05011] Requirement: When the ISPU is in sleep mode, it is possible to perform reads and writes from the data and code memory by triggering an AHB transition. */;
        doc /* coverageDependency: DRS-REQ-048 -> approved source requirement DDS_STBIO1_05011 */;
        satisfy req_DRS_REQ_048 by self;
        requirement def DRS_REQ_049 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0036";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-049";
            doc /* [DDS_STBIO1_0036] Requirement: If bit OTP_PRG10[31] in OTP Registers, called write_protection_en, is set to 1, and STBIO1 is not in debug_mode, register map shall refuse any incoming write request if the transaction address is within the OTP Registers space (from 0xCD000 to 0xCD02F). */;
        }
        requirement req_DRS_REQ_049 : DRS_REQ_049;
        doc /* drsReqId=DRS-REQ-049 | sourceReqId=DDS_STBIO1_0036 | [DDS_STBIO1_0036] Requirement: If bit OTP_PRG10[31] in OTP Registers, called write_protection_en, is set to 1, and STBIO1 is not in debug_mode, register map shall refuse any incoming write request if the transaction address is within the OTP Registers space (from 0xCD000 to 0xCD02F). */;
        doc /* coverageDependency: DRS-REQ-049 -> approved source requirement DDS_STBIO1_0036 */;
        satisfy req_DRS_REQ_049 by self;
        requirement def DRS_REQ_050 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0218";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-050";
            doc /* The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        }
        requirement req_DRS_REQ_050 : DRS_REQ_050;
        doc /* drsReqId=DRS-REQ-050 | sourceReqId=DDS_STBIO1_0218 | The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        doc /* coverageDependency: DRS-REQ-050 -> approved source requirement DDS_STBIO1_0218 */;
        satisfy req_DRS_REQ_050 by self;
        requirement def DRS_REQ_051 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0144";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-051";
            doc /* • The user shall select active channel, in this case only PPG_SEL and DS_SEL (data Storage) in DEVICE_CONFIG_CHANNEL register shall be set to 0x30. */;
        }
        requirement req_DRS_REQ_051 : DRS_REQ_051;
        doc /* drsReqId=DRS-REQ-051 | sourceReqId=DDS_STBIO1_0144 | • The user shall select active channel, in this case only PPG_SEL and DS_SEL (data Storage) in DEVICE_CONFIG_CHANNEL register shall be set to 0x30. */;
        doc /* coverageDependency: DRS-REQ-051 -> approved source requirement DDS_STBIO1_0144 */;
        satisfy req_DRS_REQ_051 by self;
        requirement def DRS_REQ_052 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0503";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-052";
            doc /* The irq_ISPU_MC_INTR_STS interrupt shall be connected to ECG, BIA or PPG samples ready for elaboration to bit 27. */;
        }
        requirement req_DRS_REQ_052 : DRS_REQ_052;
        doc /* drsReqId=DRS-REQ-052 | sourceReqId=DDS_STBIO1_0503 | The irq_ISPU_MC_INTR_STS interrupt shall be connected to ECG, BIA or PPG samples ready for elaboration to bit 27. */;
        doc /* coverageDependency: DRS-REQ-052 -> approved source requirement DDS_STBIO1_0503 */;
        satisfy req_DRS_REQ_052 by self;
        requirement def DRS_REQ_053 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0702";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-053";
            doc /* To turn on the ADC TEST LOW NOISE mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0xF, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable ADC in debug mode (ADDRESS=0x09, DATA=0x06) • Select page 2 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable ADC TEST LOW NOISE and input of ADC from GPIO (ADDRESS=0x0A, DATA=0x14) • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) */;
        }
        requirement req_DRS_REQ_053 : DRS_REQ_053;
        doc /* drsReqId=DRS-REQ-053 | sourceReqId=DDS_STBIO1_0702 | To turn on the ADC TEST LOW NOISE mode shall be: • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) • Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0xF, DATA=0x02) • Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register (ADDRESS=0x0F, DATA=0x12) • Enable ADC in debug mode (ADDRESS=0x09, DATA=0x06) • Select page 2 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable ADC TEST LOW NOISE and input of ADC from GPIO (ADDRESS=0x0A, DATA=0x14) • Select page 3 of the regmap (ADDRESS=0x40, DATA=0x02) • Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) */;
        doc /* coverageDependency: DRS-REQ-053 -> approved source requirement DDS_STBIO1_0702 */;
        satisfy req_DRS_REQ_053 by self;
        requirement def DRS_REQ_054 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0213";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-054";
            doc /* The digital subsystem shall satisfy the following behavior: ISPU. */;
        }
        requirement req_DRS_REQ_054 : DRS_REQ_054;
        doc /* drsReqId=DRS-REQ-054 | sourceReqId=DDS_STBIO1_0213 | The digital subsystem shall satisfy the following behavior: ISPU. */;
        doc /* coverageDependency: DRS-REQ-054 -> approved source requirement DDS_STBIO1_0213 */;
        satisfy req_DRS_REQ_054 by self;
        requirement def DRS_REQ_055 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0223";
            attribute sourceArtifact = "artifacts/stage5_drs/drs_traceability_matrix.csv";
            attribute sourceContext = "DRS-REQ-055";
            doc /* The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        }
        requirement req_DRS_REQ_055 : DRS_REQ_055;
        doc /* drsReqId=DRS-REQ-055 | sourceReqId=DDS_STBIO1_0223 | The digital subsystem shall satisfy the following behavior: ISPU debug. */;
        doc /* coverageDependency: DRS-REQ-055 -> approved source requirement DDS_STBIO1_0223 */;
        satisfy req_DRS_REQ_055 by self;
        in port i_comp_rx_out : ArchitecturePort {
            attribute sourceName = "i_comp_rx_out";
            attribute sourceDetails = "0 wire to u_main_controller_top, Description: \"Inserire LS";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "19";
        }
        out port o_BIDAC : ArchitecturePort {
            attribute sourceName = "o_BIDAC";
            attribute sourceDetails = "0 wire [11:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "19";
        }
        out port o_BDC_PPG : ArchitecturePort {
            attribute sourceName = "o_BDC_PPG";
            attribute sourceDetails = "0 wire [7:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "19";
        }
        out port o_BTIA_gain : ArchitecturePort {
            attribute sourceName = "o_BTIA_gain";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "19";
        }
        out port o_PD_PGA : ArchitecturePort {
            attribute sourceName = "o_PD_PGA";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "19";
        }
        out port o_PD_IDAC : ArchitecturePort {
            attribute sourceName = "o_PD_IDAC";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "19";
        }
        out port o_PD_TIA : ArchitecturePort {
            attribute sourceName = "o_PD_TIA";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "19";
        }
        out port o_comp_rx_ck : ArchitecturePort {
            attribute sourceName = "o_comp_rx_ck";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "19";
        }
        out port BT_IDAC_N : ArchitecturePort {
            attribute sourceName = "BT_IDAC_N";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux 19";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "19";
        }
        out port BT_IDAC_P : ArchitecturePort {
            attribute sourceName = "BT_IDAC_P";
            attribute sourceDetails = "0 wire [9:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port o_b_cap_idac : ArchitecturePort {
            attribute sourceName = "o_b_cap_idac";
            attribute sourceDetails = "0 wire [1:0] from u_scan_out_mux, Description: IDAC Filter Cap";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port o_rx_ch_frame : ArchitecturePort {
            attribute sourceName = "o_rx_ch_frame";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux, Description: BMUX_Selection";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port DIS_LOOP_TIA : ArchitecturePort {
            attribute sourceName = "DIS_LOOP_TIA";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: Disable TIA loop";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port T_RX_GPIO1 : ArchitecturePort {
            attribute sourceName = "T_RX_GPIO1";
            attribute sourceDetails = "0 wire [1:0] from u_scan_out_mux, Description: TEST RX signal on";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port T_RX_GPIO2 : ArchitecturePort {
            attribute sourceName = "T_RX_GPIO2";
            attribute sourceDetails = "0 wire [1:0] from u_scan_out_mux, Description: TEST RX signal on";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port TM_SEL_1V8 : ArchitecturePort {
            attribute sourceName = "TM_SEL_1V8";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: Force PGA input";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port o_en_tx_1V2 : ArchitecturePort {
            attribute sourceName = "o_en_tx_1V2";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux o_tx1_outlab_sel_frame_x_ 1V2 output 0 wire from u_scan_out_mux o_tx2_outlab_sel_frame_x_ 1V2 output 0 wire from u_scan_out_mux o_tx3_outlab_sel_frame_x_ 1V2 output 0 wire from u_scan_out_mux o_tx4_outlab_sel_frame_x_ 1V2 output 0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port o_tx_preset_1V2 : ArchitecturePort {
            attribute sourceName = "o_tx_preset_1V2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port BtrimIREF_TX_1V2 : ArchitecturePort {
            attribute sourceName = "BtrimIREF_TX_1V2";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux, Description: TX Ramp Current";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port DFT_SEL_1V2 : ArchitecturePort {
            attribute sourceName = "DFT_SEL_1V2";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: VFEED_1V2 Monitor";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port o_curr_sel_tx_frame_x_1V2 : ArchitecturePort {
            attribute sourceName = "o_curr_sel_tx_frame_x_1V2";
            attribute sourceDetails = "0 wire [7:0] from u_scan_out_mux, Description: Selezione corrente 20";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "20";
        }
        out port o_Txi_RAMP_1V2 : ArchitecturePort {
            attribute sourceName = "o_Txi_RAMP_1V2";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux, Description: B_RAMP_1V2<3:0>";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_ck_chop_imp : ArchitecturePort {
            attribute sourceName = "o_ck_chop_imp";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_ck_hc2_10k : ArchitecturePort {
            attribute sourceName = "o_ck_hc2_10k";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_ck_m : ArchitecturePort {
            attribute sourceName = "o_ck_m";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: inserito new bit";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_ck_p : ArchitecturePort {
            attribute sourceName = "o_ck_p";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: inserito new bit";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_ck_q : ArchitecturePort {
            attribute sourceName = "o_ck_q";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: inserito new bit";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_short_on : ArchitecturePort {
            attribute sourceName = "o_short_on";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: (codex 1417523";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_resh_on : ArchitecturePort {
            attribute sourceName = "o_resh_on";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: (codex 1417523";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_resl_on : ArchitecturePort {
            attribute sourceName = "o_resl_on";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: (codex 1417523";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_pd_hc2 : ArchitecturePort {
            attribute sourceName = "o_pd_hc2";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_pd_imp : ArchitecturePort {
            attribute sourceName = "o_pd_imp";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_rst_hc2 : ArchitecturePort {
            attribute sourceName = "o_rst_hc2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_rst_imp : ArchitecturePort {
            attribute sourceName = "o_rst_imp";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_rsti_hc2 : ArchitecturePort {
            attribute sourceName = "o_rsti_hc2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_rsti_imp : ArchitecturePort {
            attribute sourceName = "o_rsti_imp";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_su_hc2 : ArchitecturePort {
            attribute sourceName = "o_su_hc2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_sug_imp : ArchitecturePort {
            attribute sourceName = "o_sug_imp";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        in port i_ADC_EOC : ArchitecturePort {
            attribute sourceName = "i_ADC_EOC";
            attribute sourceDetails = "0 wire to u_main_controller_top/u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        in port i_data_ADC_out : ArchitecturePort {
            attribute sourceName = "i_data_ADC_out";
            attribute sourceDetails = "0 wire [15:0] to u_main_controller_top/u_pad_mux 21";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "21";
        }
        out port o_adc_mux_bio_channel : ArchitecturePort {
            attribute sourceName = "o_adc_mux_bio_channel";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_mux_sel : ArchitecturePort {
            attribute sourceName = "o_adc_mux_sel";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_gsr_curr_on : ArchitecturePort {
            attribute sourceName = "o_gsr_curr_on";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_gsr_on : ArchitecturePort {
            attribute sourceName = "o_gsr_on";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_ADC_en : ArchitecturePort {
            attribute sourceName = "o_ADC_en";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_ADC_start : ArchitecturePort {
            attribute sourceName = "o_ADC_start";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_error_cap8_1V2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap8_1V2";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_error_cap7_1V2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap7_1V2";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_error_cap6_1V2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap6_1V2";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_error_cap5_1V2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap5_1V2";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_error_cap4_1V2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap4_1V2";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_error_cap3_1V2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap3_1V2";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_error_cap2_1V2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap2_1V2";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_error_cap1_1V2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap1_1V2";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_adc_error_cap0_1V2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap0_1V2";
            attribute sourceDetails = "0 wire [6:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_pd_cm_buf : ArchitecturePort {
            attribute sourceName = "o_pd_cm_buf";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_pd_rld : ArchitecturePort {
            attribute sourceName = "o_pd_rld";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_pd_avg1 : ArchitecturePort {
            attribute sourceName = "o_pd_avg1";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        out port o_pd_avg2 : ArchitecturePort {
            attribute sourceName = "o_pd_avg2";
            attribute sourceDetails = "1 wire from u_scan_out_mux 22";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "22";
        }
        in port POR1V2_1V2 : ArchitecturePort {
            attribute sourceName = "POR1V2_1V2";
            attribute sourceDetails = "0 wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        in port clk_16m : ArchitecturePort {
            attribute sourceName = "clk_16m";
            attribute sourceDetails = "0 wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        in port clk_64k : ArchitecturePort {
            attribute sourceName = "clk_64k";
            attribute sourceDetails = "0 wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        in port START_CLK_16M : ArchitecturePort {
            attribute sourceName = "START_CLK_16M";
            attribute sourceDetails = "0 wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port o_DIS_RC_VIREF : ArchitecturePort {
            attribute sourceName = "o_DIS_RC_VIREF";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port o_EN_LDO1V8 : ArchitecturePort {
            attribute sourceName = "o_EN_LDO1V8";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port o_PD_CLKF : ArchitecturePort {
            attribute sourceName = "o_PD_CLKF";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port ADC_CAL_CORR_DIS : ArchitecturePort {
            attribute sourceName = "ADC_CAL_CORR_DIS";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port ADC_ERROR_CAP9_DEBUG : ArchitecturePort {
            attribute sourceName = "ADC_ERROR_CAP9_DEBUG";
            attribute sourceDetails = "0 wire [7:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port ADC_SR_ENHANCE_DIS : ArchitecturePort {
            attribute sourceName = "ADC_SR_ENHANCE_DIS";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port CCK_THRESHN_SEL : ArchitecturePort {
            attribute sourceName = "CCK_THRESHN_SEL";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port CCK_THRESHP_SEL : ArchitecturePort {
            attribute sourceName = "CCK_THRESHP_SEL";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port CURR_BG_TRIM : ArchitecturePort {
            attribute sourceName = "CURR_BG_TRIM";
            attribute sourceDetails = "8 wire [3:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port CURR_PTAT_TRIM : ArchitecturePort {
            attribute sourceName = "CURR_PTAT_TRIM";
            attribute sourceDetails = "8 wire [3:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port DCCK_CURRINJ : ArchitecturePort {
            attribute sourceName = "DCCK_CURRINJ";
            attribute sourceDetails = "0 wire [1:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port DCCK_ISINK_IN : ArchitecturePort {
            attribute sourceName = "DCCK_ISINK_IN";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port DCCK_ISOURCE_IN : ArchitecturePort {
            attribute sourceName = "DCCK_ISOURCE_IN";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port ECG_PSDRES_DOWN : ArchitecturePort {
            attribute sourceName = "ECG_PSDRES_DOWN";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port ECG_PSDRES_UP : ArchitecturePort {
            attribute sourceName = "ECG_PSDRES_UP";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux 23 EN_DEBUG_ADC_ERROR_C AP9 output 0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "23";
        }
        out port EN_ECG_50m : ArchitecturePort {
            attribute sourceName = "EN_ECG_50m";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port EN_GRS_50m : ArchitecturePort {
            attribute sourceName = "EN_GRS_50m";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port EN_IMP_50m : ArchitecturePort {
            attribute sourceName = "EN_IMP_50m";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port EN_RLD_CM : ArchitecturePort {
            attribute sourceName = "EN_RLD_CM";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port EN_SW_IMP : ArchitecturePort {
            attribute sourceName = "EN_SW_IMP";
            attribute sourceDetails = "1 wire from u_scan_out_mux, Description: per selezionare";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port GAIN1_BUF : ArchitecturePort {
            attribute sourceName = "GAIN1_BUF";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port GSR_IN_TRIM : ArchitecturePort {
            attribute sourceName = "GSR_IN_TRIM";
            attribute sourceDetails = "0 wire [7:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port GSR_IP_TRIM : ArchitecturePort {
            attribute sourceName = "GSR_IP_TRIM";
            attribute sourceDetails = "0 wire [7:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port IMPP_PSDRES_DOWN : ArchitecturePort {
            attribute sourceName = "IMPP_PSDRES_DOWN";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port IMPP_PSDRES_UP : ArchitecturePort {
            attribute sourceName = "IMPP_PSDRES_UP";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port IMPQ_PSDRES_DOWN : ArchitecturePort {
            attribute sourceName = "IMPQ_PSDRES_DOWN";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port IMPQ_PSDRES_UP : ArchitecturePort {
            attribute sourceName = "IMPQ_PSDRES_UP";
            attribute sourceDetails = "0 wire [2:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port IMP_CURINJN_TRIM : ArchitecturePort {
            attribute sourceName = "IMP_CURINJN_TRIM";
            attribute sourceDetails = "0 wire [5:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port IMP_CURINJP_TRIM : ArchitecturePort {
            attribute sourceName = "IMP_CURINJP_TRIM";
            attribute sourceDetails = "0 wire [5:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port RLD_CAP_COMP : ArchitecturePort {
            attribute sourceName = "RLD_CAP_COMP";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux, Description: [1/2/3/…/15/16]*16pF";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port RLD_VREF : ArchitecturePort {
            attribute sourceName = "RLD_VREF";
            attribute sourceDetails = "0 wire [1:0] from u_scan_out_mux, Description: select 0.9V/ 0.6V 24";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "24";
        }
        out port TRIM_LDOD_I : ArchitecturePort {
            attribute sourceName = "TRIM_LDOD_I";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port TRIM_LDOD_V : ArchitecturePort {
            attribute sourceName = "TRIM_LDOD_V";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port TRIM_OSC_FAST : ArchitecturePort {
            attribute sourceName = "TRIM_OSC_FAST";
            attribute sourceDetails = "18 wire [4:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port TRIM_OSC_SLOW : ArchitecturePort {
            attribute sourceName = "TRIM_OSC_SLOW";
            attribute sourceDetails = "0 wire [3:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port TRIM_V1V8 : ArchitecturePort {
            attribute sourceName = "TRIM_V1V8";
            attribute sourceDetails = "7 wire [2:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port VREF_TRIM : ArchitecturePort {
            attribute sourceName = "VREF_TRIM";
            attribute sourceDetails = "10 wire [4:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port CAPF_IMP_EN : ArchitecturePort {
            attribute sourceName = "CAPF_IMP_EN";
            attribute sourceDetails = "1 wire from u_scan_out_mux, Description: Enable filtro per";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port ECG0_GAIN_HC_0 : ArchitecturePort {
            attribute sourceName = "ECG0_GAIN_HC_0";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port ECG0_GAIN_HC_1 : ArchitecturePort {
            attribute sourceName = "ECG0_GAIN_HC_1";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port EN_EXT_CAP : ArchitecturePort {
            attribute sourceName = "EN_EXT_CAP";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: Mantenuta opzione";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port EN_ECG0_0P05HP : ArchitecturePort {
            attribute sourceName = "EN_ECG0_0P05HP";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: aggiunto bit per";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port EN_ECG12_0P05HP : ArchitecturePort {
            attribute sourceName = "EN_ECG12_0P05HP";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: aggiunto bit per";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port GAIN_IMP : ArchitecturePort {
            attribute sourceName = "GAIN_IMP";
            attribute sourceDetails = "1 wire [1:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port GIMP_DC : ArchitecturePort {
            attribute sourceName = "GIMP_DC";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port o_gsr_switchon : ArchitecturePort {
            attribute sourceName = "o_gsr_switchon";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: spostato il bit";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port GSR_GAIN_SEL : ArchitecturePort {
            attribute sourceName = "GSR_GAIN_SEL";
            attribute sourceDetails = "0 wire [1:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port GSR_GAIN_X1 : ArchitecturePort {
            attribute sourceName = "GSR_GAIN_X1";
            attribute sourceDetails = "0 wire from u_scan_out_mux 25";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "25";
        }
        out port IGSR_X10 : ArchitecturePort {
            attribute sourceName = "IGSR_X10";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port IMP_CURRINJ_CUR : ArchitecturePort {
            attribute sourceName = "IMP_CURRINJ_CUR";
            attribute sourceDetails = "2 wire [1:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port IMP_CURRINJ_x10 : ArchitecturePort {
            attribute sourceName = "IMP_CURRINJ_x10";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port SEL_GSR_CURR : ArchitecturePort {
            attribute sourceName = "SEL_GSR_CURR";
            attribute sourceDetails = "3 wire [1:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port o_ck_bg : ArchitecturePort {
            attribute sourceName = "o_ck_bg";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port o_imp_curinj_pd : ArchitecturePort {
            attribute sourceName = "o_imp_curinj_pd";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port o_pd_p : ArchitecturePort {
            attribute sourceName = "o_pd_p";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port o_pd_n : ArchitecturePort {
            attribute sourceName = "o_pd_n";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port o_adc_error_cap9 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap9";
            attribute sourceDetails = "0 wire [7:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port o_en_bufxbio : ArchitecturePort {
            attribute sourceName = "o_en_bufxbio";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port o_ldo_ext : ArchitecturePort {
            attribute sourceName = "o_ldo_ext";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port o_clk_ext_div : ArchitecturePort {
            attribute sourceName = "o_clk_ext_div";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port o_adc_test_cap : ArchitecturePort {
            attribute sourceName = "o_adc_test_cap";
            attribute sourceDetails = "0 wire [9:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port if_cs_en : ArchitecturePort {
            attribute sourceName = "if_cs_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_cs_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        in port if_cs_in : ArchitecturePort {
            attribute sourceName = "if_cs_in";
            attribute sourceDetails = "wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port if_cs_out : ArchitecturePort {
            attribute sourceName = "if_cs_out";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_cs_out_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port if_cs_tud : ArchitecturePort {
            attribute sourceName = "if_cs_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_cs_tud_ls_out, Description:";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port if_gpio0_en : ArchitecturePort {
            attribute sourceName = "if_gpio0_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_gpio0_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        in port if_gpio0_in : ArchitecturePort {
            attribute sourceName = "if_gpio0_in";
            attribute sourceDetails = "wire to u_pad_mux/u_pmu.if_sh_ck_in";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port if_gpio0_out : ArchitecturePort {
            attribute sourceName = "if_gpio0_out";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_gpio0_out_ls_out 26";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "26";
        }
        out port if_gpio0_tud : ArchitecturePort {
            attribute sourceName = "if_gpio0_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_gpio0_tud_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio1_en : ArchitecturePort {
            attribute sourceName = "if_gpio1_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_gpio1_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        in port if_gpio1_in : ArchitecturePort {
            attribute sourceName = "if_gpio1_in";
            attribute sourceDetails = "wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio1_out : ArchitecturePort {
            attribute sourceName = "if_gpio1_out";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_gpio1_out_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio1_tud : ArchitecturePort {
            attribute sourceName = "if_gpio1_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_gpio1_tud_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        in port if_gpio2_in : ArchitecturePort {
            attribute sourceName = "if_gpio2_in";
            attribute sourceDetails = "wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio2_en : ArchitecturePort {
            attribute sourceName = "if_gpio2_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_gpio2_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio2_out : ArchitecturePort {
            attribute sourceName = "if_gpio2_out";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_gpio2_out_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio2_tud : ArchitecturePort {
            attribute sourceName = "if_gpio2_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_gpio2_tud_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio3_en : ArchitecturePort {
            attribute sourceName = "if_gpio3_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_gpio3_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        in port if_gpio3_in : ArchitecturePort {
            attribute sourceName = "if_gpio3_in";
            attribute sourceDetails = "wire to u_pad_mux, Description: decidere se mantenere l'IN";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio3_out : ArchitecturePort {
            attribute sourceName = "if_gpio3_out";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_gpio3_out_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio3_tud : ArchitecturePort {
            attribute sourceName = "if_gpio3_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_gpio3_tud_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio4_en : ArchitecturePort {
            attribute sourceName = "if_gpio4_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_gpio4_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        in port if_gpio4_in : ArchitecturePort {
            attribute sourceName = "if_gpio4_in";
            attribute sourceDetails = "wire to u_pad_mux, Description: decidere se mantenere l'IN";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio4_out : ArchitecturePort {
            attribute sourceName = "if_gpio4_out";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_gpio4_out_ls_out 27";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "27";
        }
        out port if_gpio4_tud : ArchitecturePort {
            attribute sourceName = "if_gpio4_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_gpio4_tud_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sclk_en : ArchitecturePort {
            attribute sourceName = "if_sclk_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_sclk_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        in port if_sclk_in : ArchitecturePort {
            attribute sourceName = "if_sclk_in";
            attribute sourceDetails = "wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sclk_out : ArchitecturePort {
            attribute sourceName = "if_sclk_out";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_sclk_out_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sclk_tud : ArchitecturePort {
            attribute sourceName = "if_sclk_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_sclk_tud_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sda_sdi_en : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_sda_sdi_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        in port if_sda_sdi_in : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_in";
            attribute sourceDetails = "wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sda_sdi_out : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_out";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_sda_sdi_out_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sda_sdi_tud : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_sda_sdi_tud_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sh_ck_en : ArchitecturePort {
            attribute sourceName = "if_sh_ck_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_sh_ck_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        in port if_sh_ck_in : ArchitecturePort {
            attribute sourceName = "if_sh_ck_in";
            attribute sourceDetails = "wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sh_ck_out : ArchitecturePort {
            attribute sourceName = "if_sh_ck_out";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_sh_ck_out_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sh_ck_tud : ArchitecturePort {
            attribute sourceName = "if_sh_ck_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_sh_ck_tud_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sh_sda_en : ArchitecturePort {
            attribute sourceName = "if_sh_sda_en";
            attribute sourceDetails = "wire from u_level_shifter_sel.if_sh_sda_en_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        in port if_sh_sda_in : ArchitecturePort {
            attribute sourceName = "if_sh_sda_in";
            attribute sourceDetails = "wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sh_sda_out : ArchitecturePort {
            attribute sourceName = "if_sh_sda_out";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_sh_sda_out_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port if_sh_sda_tud : ArchitecturePort {
            attribute sourceName = "if_sh_sda_tud";
            attribute sourceDetails = "1 wire from u_level_shifter_sel.if_sh_sda_tud_ls_out 28";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "28";
        }
        out port o_trim_ldo_d : ArchitecturePort {
            attribute sourceName = "o_trim_ldo_d";
            attribute sourceDetails = "0 wire [1:0] from u_level_shifter_sel.o_trim_ldo_d_ls_out";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port ADC_BUFF_REFRESH_DIS : ArchitecturePort {
            attribute sourceName = "ADC_BUFF_REFRESH_DIS";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port ADC_EXTRAPERIOD_DIS : ArchitecturePort {
            attribute sourceName = "ADC_EXTRAPERIOD_DIS";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port ADC_INPUT_FROM_GPIO : ArchitecturePort {
            attribute sourceName = "ADC_INPUT_FROM_GPIO";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port ADC_REF_FROM_GPIO : ArchitecturePort {
            attribute sourceName = "ADC_REF_FROM_GPIO";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port AFE_SPARE_0_1V2 : ArchitecturePort {
            attribute sourceName = "AFE_SPARE_0_1V2";
            attribute sourceDetails = "0 wire [7:0] from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port AFE_SPARE_1 : ArchitecturePort {
            attribute sourceName = "AFE_SPARE_1";
            attribute sourceDetails = "0 wire [7:0] from u_scan_out_mux, Description: modificato l'utilizzo";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port DIS_LDOD_HP : ArchitecturePort {
            attribute sourceName = "DIS_LDOD_HP";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port DIS_LDOD_IP : ArchitecturePort {
            attribute sourceName = "DIS_LDOD_IP";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port EN_LDOD_FIFO : ArchitecturePort {
            attribute sourceName = "EN_LDOD_FIFO";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port EN_LDOD_STREDL : ArchitecturePort {
            attribute sourceName = "EN_LDOD_STREDL";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port OTP_SPARE : ArchitecturePort {
            attribute sourceName = "OTP_SPARE";
            attribute sourceDetails = "00007F0 0 wire [31:0] from u_scan_out_mux, Description: i PMB_EXT sono collegati";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        in port OVERCURR_N_IN_i : ArchitecturePort {
            attribute sourceName = "OVERCURR_N_IN_i";
            attribute sourceDetails = "0 wire to u_regmap_otp";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        in port OVERCURR_P_IN_i : ArchitecturePort {
            attribute sourceName = "OVERCURR_P_IN_i";
            attribute sourceDetails = "0 wire to u_regmap_otp";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        in port O_DCCK_N_i : ArchitecturePort {
            attribute sourceName = "O_DCCK_N_i";
            attribute sourceDetails = "0 wire to u_pad_mux/u_regmap_otp/u_regmap_o tp.DCCK_N_IRQ_i/u_N_not_logic.A,";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        in port O_DCCK_P_i : ArchitecturePort {
            attribute sourceName = "O_DCCK_P_i";
            attribute sourceDetails = "0 wire to u_pad_mux/u_regmap_otp/u_regmap_o tp.DCCK_P_IRQ_i/u_P_not_logic.A,";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port t_en_gpio1 : ArchitecturePort {
            attribute sourceName = "t_en_gpio1";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: spostato il bit";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port t_en_gpio2 : ArchitecturePort {
            attribute sourceName = "t_en_gpio2";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: spostato il bit";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port t_en_gpio3 : ArchitecturePort {
            attribute sourceName = "t_en_gpio3";
            attribute sourceDetails = "0 wire from u_scan_out_mux 29";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "29";
        }
        out port t_en_gpio4 : ArchitecturePort {
            attribute sourceName = "t_en_gpio4";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port t_ecg0_out_pre_buf : ArchitecturePort {
            attribute sourceName = "t_ecg0_out_pre_buf";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port t_offset_gpio12 : ArchitecturePort {
            attribute sourceName = "t_offset_gpio12";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port t_in_bio_buf34 : ArchitecturePort {
            attribute sourceName = "t_in_bio_buf34";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port t_ecg1_out_pre_bufp_3 : ArchitecturePort {
            attribute sourceName = "t_ecg1_out_pre_bufp_3";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port t_ecg1_out_pre_bufn_4 : ArchitecturePort {
            attribute sourceName = "t_ecg1_out_pre_bufn_4";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port t_ecg2_out_pre_bufn_3 : ArchitecturePort {
            attribute sourceName = "t_ecg2_out_pre_bufn_3";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port t_ecg2_out_pre_bufp_4 : ArchitecturePort {
            attribute sourceName = "t_ecg2_out_pre_bufp_4";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_CM_HLT_2 : ArchitecturePort {
            attribute sourceName = "T_CM_HLT_2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_CM_RLD_1 : ArchitecturePort {
            attribute sourceName = "T_CM_RLD_1";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_ECG0_AC_1 : ArchitecturePort {
            attribute sourceName = "T_ECG0_AC_1";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_ECG0_DC_2 : ArchitecturePort {
            attribute sourceName = "T_ECG0_DC_2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_EXT_HPF_ECG0 : ArchitecturePort {
            attribute sourceName = "T_EXT_HPF_ECG0";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_FORCE_1V2 : ArchitecturePort {
            attribute sourceName = "T_FORCE_1V2";
            attribute sourceDetails = "0 wire from u_pad_mux.o_t_force_1v2";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_IBG_1u_2 : ArchitecturePort {
            attribute sourceName = "T_IBG_1u_2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_IMPP_AC_1 : ArchitecturePort {
            attribute sourceName = "T_IMPP_AC_1";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_IMPP_DC_2 : ArchitecturePort {
            attribute sourceName = "T_IMPP_DC_2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_IMPQ_AC_2 : ArchitecturePort {
            attribute sourceName = "T_IMPQ_AC_2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_IMPQ_DC_1 : ArchitecturePort {
            attribute sourceName = "T_IMPQ_DC_1";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_IN_BIO_BUF : ArchitecturePort {
            attribute sourceName = "T_IN_BIO_BUF";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_IPTAT_1u_1 : ArchitecturePort {
            attribute sourceName = "T_IPTAT_1u_1";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_OP55_1 : ArchitecturePort {
            attribute sourceName = "T_OP55_1";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_OP90_2 : ArchitecturePort {
            attribute sourceName = "T_OP90_2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_OUT_BIO_BUF : ArchitecturePort {
            attribute sourceName = "T_OUT_BIO_BUF";
            attribute sourceDetails = "0 wire from u_scan_out_mux 30";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "30";
        }
        out port T_OUT_GSR : ArchitecturePort {
            attribute sourceName = "T_OUT_GSR";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port T_OUT_PPG_BUF : ArchitecturePort {
            attribute sourceName = "T_OUT_PPG_BUF";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port T_SENSE_1V2 : ArchitecturePort {
            attribute sourceName = "T_SENSE_1V2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port T_SENSEIBG_1V2 : ArchitecturePort {
            attribute sourceName = "T_SENSEIBG_1V2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port T_CM_HLT_1 : ArchitecturePort {
            attribute sourceName = "T_CM_HLT_1";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port T_SENSEVBG_1V2 : ArchitecturePort {
            attribute sourceName = "T_SENSEVBG_1V2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port o_end_calibration_1V2 : ArchitecturePort {
            attribute sourceName = "o_end_calibration_1V2";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port pd_osc_clk32k : ArchitecturePort {
            attribute sourceName = "pd_osc_clk32k";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: se si seleziona";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port o_pd_buf_gpio1 : ArchitecturePort {
            attribute sourceName = "o_pd_buf_gpio1";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port o_pd_buf_gpio2 : ArchitecturePort {
            attribute sourceName = "o_pd_buf_gpio2";
            attribute sourceDetails = "1 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port EN_CLK_EXT : ArchitecturePort {
            attribute sourceName = "EN_CLK_EXT";
            attribute sourceDetails = "0 wire from u_scan_out_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        in port WHO_AM_I : ArchitecturePort {
            attribute sourceName = "WHO_AM_I";
            attribute sourceDetails = "D7 wire [7:0] to u_regmap_otp.DEV_ID_i, Description: ? OK ?";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        in port if_sclk_i3c_in : ArchitecturePort {
            attribute sourceName = "if_sclk_i3c_in";
            attribute sourceDetails = "wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        in port if_sda_sdi_i3c_in : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_i3c_in";
            attribute sourceDetails = "wire to u_pad_mux";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        in port VREF : ArchitecturePort {
            attribute sourceName = "VREF";
            attribute sourceDetails = "wire to u_otp";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        in port IREF : ArchitecturePort {
            attribute sourceName = "IREF";
            attribute sourceDetails = "wire to u_otp";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        out port OTP_IREF_WAKEUP : ArchitecturePort {
            attribute sourceName = "OTP_IREF_WAKEUP";
            attribute sourceDetails = "0 wire from u_scan_out_mux, Description: Enable Mirror OTP";
            attribute sourceTable = "Digital I/O List";
            attribute sourcePage = "31";
        }
        part aDSP : ADSP;
        part bISTController : BISTController;
        part i2CSPIAHB : I2CSPIAHB;
        part iRQLogic : IRQLogic;
        part iSPU : ISPU;
        part mainController : MainController;
        part oTP : OTP;
        part pMU : PMU;
        part padMux : PadMux;
        part regmap : Regmap;
        part sensorHub : SensorHub;
        part smartFIFO : SmartFIFO;
    }

}

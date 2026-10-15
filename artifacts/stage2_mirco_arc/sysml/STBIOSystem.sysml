// NOT READY for RTL or high-level model generation
// Snapshot ID: snap-73c872b1307b6adb5eaf843e
// Downstream contract fingerprint: fe7fcb076580a4245cd18758f20d821b4ea5f2e9333b83cbcabaac32735886cf

package SystemArchitecture {

    // Generated hierarchical top model; block definitions are in sysml/blocks/.
    private import ArchitectureShared::*;

    private import Block_ADSP::*;
    private import Block_I2CSPIAHB::*;
    private import Block_MainController::*;
    private import Block_PadMux::*;
    private import Block_PMU::*;
    private import Block_Regmap::*;
    private import Block_SensorHub::*;
    private import Block_SmartFIFO::*;
    private import DigitalArchitecture::*;

    part def AnalogSubsystem {
        attribute displayName : String = "Analog Subsystem";
    }

    part def TopAnalogArchitecture {
        attribute displayName : String = "Top Analog Architecture";
        part analogSubsystem : AnalogSubsystem;
    }

    part def STBIOSystem {
        doc /* Level 1 system architecture. Concrete requirements are contained by their owning Level 2 block. */;
        part topAnalog : TopAnalogArchitecture;
        part topDigital : DigitalSubsystem;
        port AV1V8 : ArchitecturePort {
            attribute sourceName = "AV1V8";
            attribute sourceDetails = "1.8 V Analog Power Supply D5 Power";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port AV3V3 : ArchitecturePort {
            attribute sourceName = "AV3V3";
            attribute sourceDetails = "3.3 V Analog Power Supply D4 Power";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port AGND : ArchitecturePort {
            attribute sourceName = "AGND";
            attribute sourceDetails = "Analog Ground D6 Power";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port DVDD : ArchitecturePort {
            attribute sourceName = "DVDD";
            attribute sourceDetails = "1.8 V Digital Power Supply A3 Power";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port GNDD : ArchitecturePort {
            attribute sourceName = "GNDD";
            attribute sourceDetails = "Digital Ground B3 Power";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port VDDIO : ArchitecturePort {
            attribute sourceName = "VDDIO";
            attribute sourceDetails = "I/O Power Supply. A2 Power";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port GNDIO : ArchitecturePort {
            attribute sourceName = "GNDIO";
            attribute sourceDetails = "I/O Ground B2 Power";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port LGND : ArchitecturePort {
            attribute sourceName = "LGND";
            attribute sourceDetails = "LED Ground F2 Power";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port VREF : ArchitecturePort {
            attribute sourceName = "VREF";
            attribute sourceDetails = "Voltage Reference D7 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port PDIN5N : ArchitecturePort {
            attribute sourceName = "PDIN5N";
            attribute sourceDetails = "Photodiode 5 N A7 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port PDIN1P : ArchitecturePort {
            attribute sourceName = "PDIN1P";
            attribute sourceDetails = "Photodiode 5 P A6 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port PDIN6N : ArchitecturePort {
            attribute sourceName = "PDIN6N";
            attribute sourceDetails = "Photodiode 6 N A5 Analog 16";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "16";
        }
        port PDIN6P : ArchitecturePort {
            attribute sourceName = "PDIN6P";
            attribute sourceDetails = "Photodiode 6 P A4 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port PDIN3N : ArchitecturePort {
            attribute sourceName = "PDIN3N";
            attribute sourceDetails = "Photodiode 3 N B7 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port PDIN3P : ArchitecturePort {
            attribute sourceName = "PDIN3P";
            attribute sourceDetails = "Photodiode 3 P B6 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port PDIN4N : ArchitecturePort {
            attribute sourceName = "PDIN4N";
            attribute sourceDetails = "Photodiode 4 N B5 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port PDIN4P : ArchitecturePort {
            attribute sourceName = "PDIN4P";
            attribute sourceDetails = "Photodiode 4 P B4 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port PDIN2P : ArchitecturePort {
            attribute sourceName = "PDIN2P";
            attribute sourceDetails = "Photodiode 2 P C4 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port PDIN2N : ArchitecturePort {
            attribute sourceName = "PDIN2N";
            attribute sourceDetails = "Photodiode 2 N C5 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port PDIN1P_2 : ArchitecturePort {
            attribute sourceName = "PDIN1P";
            attribute sourceDetails = "Photodiode 1 P C6 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port PDIN1N : ArchitecturePort {
            attribute sourceName = "PDIN1N";
            attribute sourceDetails = "Photodiode 1 N C7 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port LED1 : ArchitecturePort {
            attribute sourceName = "LED1";
            attribute sourceDetails = "LED driver 1 G3 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port LED2 : ArchitecturePort {
            attribute sourceName = "LED2";
            attribute sourceDetails = "LED driver 2 G2 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port LED3 : ArchitecturePort {
            attribute sourceName = "LED3";
            attribute sourceDetails = "LED driver 3 G1 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port LED4 : ArchitecturePort {
            attribute sourceName = "LED4";
            attribute sourceDetails = "LED driver 4 F1 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port LED5 : ArchitecturePort {
            attribute sourceName = "LED5";
            attribute sourceDetails = "LED driver 5 F3 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port LED6 : ArchitecturePort {
            attribute sourceName = "LED6";
            attribute sourceDetails = "LED driver 6 E1 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port LED7 : ArchitecturePort {
            attribute sourceName = "LED7";
            attribute sourceDetails = "LED driver 7 E2 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port LED8 : ArchitecturePort {
            attribute sourceName = "LED8";
            attribute sourceDetails = "LED driver 8 E3 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port ECGIP : ArchitecturePort {
            attribute sourceName = "ECGIP";
            attribute sourceDetails = "ECG Positive Input E7 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port ECGIN : ArchitecturePort {
            attribute sourceName = "ECGIN";
            attribute sourceDetails = "ECG Negative Input E6 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port RLD : ArchitecturePort {
            attribute sourceName = "RLD";
            attribute sourceDetails = "Right LEG Driver E5 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port IMPIP : ArchitecturePort {
            attribute sourceName = "IMPIP";
            attribute sourceDetails = "BIA Positive Input F7 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port IMPIN : ArchitecturePort {
            attribute sourceName = "IMPIN";
            attribute sourceDetails = "BIA Negative Input F6 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port GSRP : ArchitecturePort {
            attribute sourceName = "GSRP";
            attribute sourceDetails = "GSR Positive Input G7 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port GSRN : ArchitecturePort {
            attribute sourceName = "GSRN";
            attribute sourceDetails = "GSR Negative Input G6 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port CIP : ArchitecturePort {
            attribute sourceName = "CIP";
            attribute sourceDetails = "BIA Injection Positive Output. G5 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port CIN : ArchitecturePort {
            attribute sourceName = "CIN";
            attribute sourceDetails = "BIA Injection Negative Output. F Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port GPIO3 : ArchitecturePort {
            attribute sourceName = "GPIO3";
            attribute sourceDetails = "General-Purpose Input/Output 3 G4 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port GPIO4 : ArchitecturePort {
            attribute sourceName = "GPIO4";
            attribute sourceDetails = "General-Purpose Input/Output 4 F4 Analog";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port SCLK : ArchitecturePort {
            attribute sourceName = "SCLK";
            attribute sourceDetails = "SPI Clock INPUT A1 Digital";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port CLKext : ArchitecturePort {
            attribute sourceName = "CLKext";
            attribute sourceDetails = "External Clock C2 Digital";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port SDA_SDI : ArchitecturePort {
            attribute sourceName = "SDA_SDI";
            attribute sourceDetails = "I2C / SPI serial data line B1 Digital";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port SH_SDA : ArchitecturePort {
            attribute sourceName = "SH_SDA";
            attribute sourceDetails = "Sensor Hub Data D1 Digital";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port CS : ArchitecturePort {
            attribute sourceName = "CS";
            attribute sourceDetails = "Chip Select C1 Digital";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port SH_CK : ArchitecturePort {
            attribute sourceName = "SH_CK";
            attribute sourceDetails = "Sensor Hub Clock C3";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port GPIO0 : ArchitecturePort {
            attribute sourceName = "GPIO0";
            attribute sourceDetails = "General-Purpose Input/Output 0 D2 Digital";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port GPIO1 : ArchitecturePort {
            attribute sourceName = "GPIO1";
            attribute sourceDetails = "General-Purpose Input/Output 1 D3 Digital";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }
        port GPIO2 : ArchitecturePort {
            attribute sourceName = "GPIO2";
            attribute sourceDetails = "General-Purpose Input/Output 2 E4 Digital 17";
            attribute sourceTable = "I/O List";
            attribute sourcePage = "17";
        }


        connection relation_6dd27dbb0a6f24f53df0 : BlockRelation connect topDigital.mainController to topDigital.regmap;
        doc relation_6dd27dbb0a6f24f53df0 /* governedRelation={"evidence": ["DDS_STBIO1_0201", "snapshot_profile:interaction_rows:13"], "identity": "relation_6dd27dbb0a6f24f53df0", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}, "status": "resolved", "target": {"block": "Regmap", "direction": "", "node": "topDigital.regmap", "port": "", "status": "resolved", "token": "Regmap"}} */;
        connection relation_480ef9d5abdb3165629c : BlockRelation connect topDigital.mainController to topDigital.smartFIFO;
        doc relation_480ef9d5abdb3165629c /* governedRelation={"evidence": ["DDS_STBIO1_0202", "snapshot_profile:interaction_rows:14"], "identity": "relation_480ef9d5abdb3165629c", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_11c83b65abd888b8d733 : BlockRelation connect topDigital.mainController to topDigital.aDSP;
        doc relation_11c83b65abd888b8d733 /* governedRelation={"evidence": ["DDS_STBIO1_0219", "snapshot_profile:interaction_rows:15"], "identity": "relation_11c83b65abd888b8d733", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}, "status": "resolved", "target": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}} */;
        connection relation_4ccc723c59c9efee6aec : BlockRelation connect topDigital.aDSP to topDigital.regmap;
        doc relation_4ccc723c59c9efee6aec /* governedRelation={"evidence": ["DDS_STBIO1_0203", "snapshot_profile:interaction_rows:16"], "identity": "relation_4ccc723c59c9efee6aec", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}, "status": "resolved", "target": {"block": "Regmap", "direction": "", "node": "topDigital.regmap", "port": "", "status": "resolved", "token": "Regmap"}} */;
        connection relation_c4ef40dd7f0a14ec8c15 : BlockRelation connect topDigital.aDSP to topDigital.sensorHub;
        doc relation_c4ef40dd7f0a14ec8c15 /* governedRelation={"evidence": ["DDS_STBIO1_0204", "snapshot_profile:interaction_rows:17"], "identity": "relation_c4ef40dd7f0a14ec8c15", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}, "status": "resolved", "target": {"block": "Sensor-Hub", "direction": "", "node": "topDigital.sensorHub", "port": "", "status": "resolved", "token": "Sensor-Hub"}} */;
        connection relation_67ac15a21030c6b3e655 : BlockRelation connect topDigital.aDSP to topDigital.smartFIFO;
        doc relation_67ac15a21030c6b3e655 /* governedRelation={"evidence": ["DDS_STBIO1_0206", "snapshot_profile:interaction_rows:18"], "identity": "relation_67ac15a21030c6b3e655", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_18a469462f40787d2bc8 : BlockRelation connect topDigital.i2CSPIAHB to topDigital.regmap;
        doc relation_18a469462f40787d2bc8 /* governedRelation={"evidence": ["DDS_STBIO1_0207", "snapshot_profile:interaction_rows:19"], "identity": "relation_18a469462f40787d2bc8", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "I2C_SPI_AHB", "direction": "", "node": "topDigital.i2CSPIAHB", "port": "", "status": "resolved", "token": "I2C_SPI_AHB"}, "status": "resolved", "target": {"block": "Regmap", "direction": "", "node": "topDigital.regmap", "port": "", "status": "resolved", "token": "Regmap"}} */;
        connection relation_c93f96704f131d25b959 : BlockRelation connect topDigital.i2CSPIAHB to topDigital.sensorHub;
        doc relation_c93f96704f131d25b959 /* governedRelation={"evidence": ["DDS_STBIO1_0208", "snapshot_profile:interaction_rows:20"], "identity": "relation_c93f96704f131d25b959", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "I2C_SPI_AHB", "direction": "", "node": "topDigital.i2CSPIAHB", "port": "", "status": "resolved", "token": "I2C_SPI_AHB"}, "status": "resolved", "target": {"block": "Sensor-Hub", "direction": "", "node": "topDigital.sensorHub", "port": "", "status": "resolved", "token": "Sensor-Hub"}} */;
        connection relation_c3ec7465ad64dc78f54f : BlockRelation connect topDigital.i2CSPIAHB to topDigital.smartFIFO;
        doc relation_c3ec7465ad64dc78f54f /* governedRelation={"evidence": ["DDS_STBIO1_0210", "snapshot_profile:interaction_rows:22"], "identity": "relation_c3ec7465ad64dc78f54f", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "I2C_SPI_AHB", "direction": "", "node": "topDigital.i2CSPIAHB", "port": "", "status": "resolved", "token": "I2C_SPI_AHB"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_cb779322ceaed4369d75 : BlockRelation connect topDigital.i2CSPIAHB to topDigital.aDSP;
        doc relation_cb779322ceaed4369d75 /* governedRelation={"evidence": ["DDS_STBIO1_0221", "snapshot_profile:interaction_rows:23"], "identity": "relation_cb779322ceaed4369d75", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "I2C_SPI_AHB", "direction": "", "node": "topDigital.i2CSPIAHB", "port": "", "status": "resolved", "token": "I2C_SPI_AHB"}, "status": "resolved", "target": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}} */;
        connection relation_8b69c4174f0f7bd1fe10 : BlockRelation connect topDigital.sensorHub to topDigital.smartFIFO;
        doc relation_8b69c4174f0f7bd1fe10 /* governedRelation={"evidence": ["DDS_STBIO1_0211", "snapshot_profile:interaction_rows:24"], "identity": "relation_8b69c4174f0f7bd1fe10", "kind": "bus", "qualifiers": [["exchange", "XBAR connection"], ["trigger", "XBAR matrix cell"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Sensor-Hub", "direction": "", "node": "topDigital.sensorHub", "port": "", "status": "resolved", "token": "Sensor-Hub"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_2cc53881a947e9b60f5e : BlockRelation connect topDigital.pMU to topDigital.regmap;
        doc relation_2cc53881a947e9b60f5e /* governedRelation={"evidence": ["DDS_STBIO1_2026"], "identity": "relation_2cc53881a947e9b60f5e", "kind": "clock", "qualifiers": [["frequency", "16 MHz"], ["gating", "with"], ["control", "stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3 | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3_reg | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_s3 | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Regmap", "direction": "", "node": "topDigital.regmap", "port": "", "status": "resolved", "token": "Regmap"}} */;
        connection relation_802d8cf5cf56ded8f7ca : BlockRelation connect topDigital.pMU to topDigital.aDSP;
        doc relation_802d8cf5cf56ded8f7ca /* governedRelation={"evidence": ["DDS_STBIO1_1022"], "identity": "relation_802d8cf5cf56ded8f7ca", "kind": "clock", "qualifiers": [["frequency", "16 MHz"], ["gating", "with"], ["control", "stbio1_top.dig_wrapper_LV.u_pm u.adsp_run | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}} */;
        connection relation_2c715c698a10d224a1a1 : BlockRelation connect topDigital.pMU to topDigital.mainController;
        doc relation_2c715c698a10d224a1a1 /* governedRelation={"evidence": ["DDS_STBIO1_1026"], "identity": "relation_2c715c698a10d224a1a1", "kind": "clock", "qualifiers": [["frequency", "16 MHz"], ["gating", "with"], ["control", "stbio1_top.dig_wrapper_LV.u_pm u.i_en_clk_16MHz_sleep | stbio1_top.dig_wrapper_LV.u_pm u.scan_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}} */;
        connection relation_4a5b6583033e2468121a : SignalConnection connect topDigital.pMU.tst_clk_16m to topDigital.mainController.i_clk_16MHz;
        doc relation_4a5b6583033e2468121a /* governedRelation={"evidence": ["DDS_STBIO1_1026"], "identity": "relation_4a5b6583033e2468121a", "kind": "clock", "qualifiers": [["frequency", "16 MHz"], ["gating", "with"], ["control", "stbio1_top.dig_wrapper_LV.u_pm u.i_en_clk_16MHz_sleep | stbio1_top.dig_wrapper_LV.u_pm u.scan_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable"]], "reason": "", "relation_class": "signal_connection", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "out", "node": "topDigital.pMU", "port": "tst_clk_16m", "status": "resolved", "token": "stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_16m"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "in", "node": "topDigital.mainController", "port": "i_clk_16MHz", "status": "resolved", "token": "stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_16MHz"}} */;
        connection relation_4e86dcc275c2e9b2ab22 : BlockRelation connect topDigital.pMU to topDigital.mainController;
        doc relation_4e86dcc275c2e9b2ab22 /* governedRelation={"evidence": ["DDS_STBIO1_1027"], "identity": "relation_4e86dcc275c2e9b2ab22", "kind": "clock", "qualifiers": [["frequency", "32 kHz"], ["gating", "without"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}} */;
        connection relation_f4098f85cfee3cad43ae : SignalConnection connect topDigital.pMU.tst_clk_32k to topDigital.mainController.i_clk_32kHz;
        doc relation_f4098f85cfee3cad43ae /* governedRelation={"evidence": ["DDS_STBIO1_1027"], "identity": "relation_f4098f85cfee3cad43ae", "kind": "clock", "qualifiers": [["frequency", "32 kHz"], ["gating", "without"]], "reason": "", "relation_class": "signal_connection", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "out", "node": "topDigital.pMU", "port": "tst_clk_32k", "status": "resolved", "token": "stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_32k"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "in", "node": "topDigital.mainController", "port": "i_clk_32kHz", "status": "resolved", "token": "stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_32kHz"}} */;
        connection relation_584a18411bc5f7055a93 : BlockRelation connect topDigital.pMU to topDigital.mainController;
        doc relation_584a18411bc5f7055a93 /* governedRelation={"evidence": ["source_port_catalog:PMU:tst_clk_32k:40"], "identity": "relation_584a18411bc5f7055a93", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.tst_clk_32k"], ["reference_level", "block"], ["peer_label", "main_controller"], ["directionality", "directed"], ["source_details", "wire clock slow 32k to main_controller"], ["source_table", ""], ["source_page", "40"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}} */;
        connection relation_a8ed8a50f8354739c7f9 : BlockRelation connect topDigital.pMU to topDigital.mainController;
        doc relation_a8ed8a50f8354739c7f9 /* governedRelation={"evidence": ["source_port_catalog:PMU:clk_main_ctrl:40"], "identity": "relation_a8ed8a50f8354739c7f9", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.clk_main_ctrl"], ["reference_level", "block"], ["peer_label", "main controller"], ["directionality", "directed"], ["source_details", "wire clock for main controller"], ["source_table", ""], ["source_page", "40"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}} */;
        connection relation_d57d263aaacab7ac5b55 : BlockRelation connect topDigital.pMU to topDigital.aDSP;
        doc relation_d57d263aaacab7ac5b55 /* governedRelation={"evidence": ["source_port_catalog:PMU:clk_stmc:40"], "identity": "relation_d57d263aaacab7ac5b55", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.clk_stmc"], ["reference_level", "block"], ["peer_label", "adsp"], ["directionality", "directed"], ["source_details", "wire adsp clock"], ["source_table", ""], ["source_page", "40"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}} */;
        connection relation_2b2c26961a69a81aa1fa : BlockRelation connect topDigital.pMU to topDigital.aDSP;
        doc relation_2b2c26961a69a81aa1fa /* governedRelation={"evidence": ["source_port_catalog:PMU:clk_stmc_ahb:40"], "identity": "relation_2b2c26961a69a81aa1fa", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.clk_stmc_ahb"], ["reference_level", "block"], ["peer_label", "adsp"], ["directionality", "directed"], ["source_details", "wire adsp clk elaboration"], ["source_table", ""], ["source_page", "40"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}} */;
        connection relation_c4d3bc41194022cba802 : BlockRelation connect topDigital.pMU to topDigital.smartFIFO;
        doc relation_c4d3bc41194022cba802 /* governedRelation={"evidence": ["source_port_catalog:PMU:clk_fifo:40"], "identity": "relation_c4d3bc41194022cba802", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.clk_fifo"], ["reference_level", "block"], ["peer_label", "fifo"], ["directionality", "directed"], ["source_details", "wire fifo clock"], ["source_table", ""], ["source_page", "40"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_3739db761acfd9cb096b : BlockRelation connect topDigital.pMU to topDigital.sensorHub;
        doc relation_3739db761acfd9cb096b /* governedRelation={"evidence": ["source_port_catalog:PMU:clk_masterblaze_m:40"], "identity": "relation_3739db761acfd9cb096b", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.clk_masterblaze_m"], ["reference_level", "block"], ["peer_label", "sensor hub"], ["directionality", "directed"], ["source_details", "wire sensor hub master clock"], ["source_table", ""], ["source_page", "40"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Sensor-Hub", "direction": "", "node": "topDigital.sensorHub", "port": "", "status": "resolved", "token": "Sensor-Hub"}} */;
        connection relation_e6ff2f46d09aa3ac649f : BlockRelation connect topDigital.pMU to topDigital.sensorHub;
        doc relation_e6ff2f46d09aa3ac649f /* governedRelation={"evidence": ["source_port_catalog:PMU:clk_masterblaze_s:40"], "identity": "relation_e6ff2f46d09aa3ac649f", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.clk_masterblaze_s"], ["reference_level", "block"], ["peer_label", "sensor hub"], ["directionality", "directed"], ["source_details", "wire sensor hub slave clock"], ["source_table", ""], ["source_page", "40"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Sensor-Hub", "direction": "", "node": "topDigital.sensorHub", "port": "", "status": "resolved", "token": "Sensor-Hub"}} */;
        connection relation_f8be799e8734cf190bf6 : BlockRelation connect topDigital.pMU to topDigital.regmap;
        doc relation_f8be799e8734cf190bf6 /* governedRelation={"evidence": ["source_port_catalog:PMU:clk_regmap:40"], "identity": "relation_f8be799e8734cf190bf6", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.clk_regmap"], ["reference_level", "block"], ["peer_label", "regmap"], ["directionality", "directed"], ["source_details", "wire regmap clock"], ["source_table", ""], ["source_page", "40"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Regmap", "direction": "", "node": "topDigital.regmap", "port": "", "status": "resolved", "token": "Regmap"}} */;
        connection relation_85760236681dcb0ce677 : BlockRelation connect topDigital.pMU to topDigital.mainController;
        doc relation_85760236681dcb0ce677 /* governedRelation={"evidence": ["source_port_catalog:PMU:resetn_main_ctrl:41"], "identity": "relation_85760236681dcb0ce677", "kind": "reset", "qualifiers": [["local_port", "topDigital.pMU.resetn_main_ctrl"], ["reference_level", "block"], ["peer_label", "main controller"], ["directionality", "directed"], ["source_details", "wire reset main controller"], ["source_table", ""], ["source_page", "41"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}} */;
        connection relation_8d5d79b8f3635ce05325 : BlockRelation connect topDigital.pMU to topDigital.mainController;
        doc relation_8d5d79b8f3635ce05325 /* governedRelation={"evidence": ["source_port_catalog:PMU:resetn_32k_main_ctrl:41"], "identity": "relation_8d5d79b8f3635ce05325", "kind": "reset", "qualifiers": [["local_port", "topDigital.pMU.resetn_32k_main_ctrl"], ["reference_level", "block"], ["peer_label", "main controller"], ["directionality", "directed"], ["source_details", "wire reset 32kHz domain main controller"], ["source_table", ""], ["source_page", "41"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}} */;
        connection relation_82870bba01e77279fc51 : BlockRelation connect topDigital.pMU to topDigital.aDSP;
        doc relation_82870bba01e77279fc51 /* governedRelation={"evidence": ["source_port_catalog:PMU:resetn_stmc:41"], "identity": "relation_82870bba01e77279fc51", "kind": "reset", "qualifiers": [["local_port", "topDigital.pMU.resetn_stmc"], ["reference_level", "block"], ["peer_label", "adsp"], ["directionality", "directed"], ["source_details", "wire reset adsp"], ["source_table", ""], ["source_page", "41"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}} */;
        connection relation_1d2720efe209c6c2eba0 : BlockRelation connect topDigital.pMU to topDigital.smartFIFO;
        doc relation_1d2720efe209c6c2eba0 /* governedRelation={"evidence": ["source_port_catalog:PMU:resetn_fifo:41"], "identity": "relation_1d2720efe209c6c2eba0", "kind": "reset", "qualifiers": [["local_port", "topDigital.pMU.resetn_fifo"], ["reference_level", "block"], ["peer_label", "FIFO"], ["directionality", "directed"], ["source_details", "wire reset FIFO"], ["source_table", ""], ["source_page", "41"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_b8bddfe700fc32b93f0f : BlockRelation connect topDigital.pMU to topDigital.sensorHub;
        doc relation_b8bddfe700fc32b93f0f /* governedRelation={"evidence": ["source_port_catalog:PMU:resetn_masterblaze:41"], "identity": "relation_b8bddfe700fc32b93f0f", "kind": "reset", "qualifiers": [["local_port", "topDigital.pMU.resetn_masterblaze"], ["reference_level", "block"], ["peer_label", "sensor hub"], ["directionality", "directed"], ["source_details", "wire reset sensor hub"], ["source_table", ""], ["source_page", "41"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Sensor-Hub", "direction": "", "node": "topDigital.sensorHub", "port": "", "status": "resolved", "token": "Sensor-Hub"}} */;
        connection relation_55069899923ee35a6bc1 : BlockRelation connect topDigital.pMU to topDigital.regmap;
        doc relation_55069899923ee35a6bc1 /* governedRelation={"evidence": ["source_port_catalog:PMU:resetn_regmap:41"], "identity": "relation_55069899923ee35a6bc1", "kind": "reset", "qualifiers": [["local_port", "topDigital.pMU.resetn_regmap"], ["reference_level", "block"], ["peer_label", "regmap"], ["directionality", "directed"], ["source_details", "wire reset regmap"], ["source_table", ""], ["source_page", "41"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Regmap", "direction": "", "node": "topDigital.regmap", "port": "", "status": "resolved", "token": "Regmap"}} */;
        connection relation_ca03d737c128953dc231 : BlockRelation connect topDigital.pMU to topDigital.sensorHub;
        doc relation_ca03d737c128953dc231 /* governedRelation={"evidence": ["source_port_catalog:PMU:o_sh_clk:41"], "identity": "relation_ca03d737c128953dc231", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.o_sh_clk"], ["reference_level", "block"], ["peer_label", "sensor hub"], ["directionality", "directed"], ["source_details", "wire sensor hub clock"], ["source_table", ""], ["source_page", "41"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Sensor-Hub", "direction": "", "node": "topDigital.sensorHub", "port": "", "status": "resolved", "token": "Sensor-Hub"}} */;
        connection relation_d37a12c67532b3823db7 : BlockRelation connect topDigital.pMU to topDigital.mainController;
        doc relation_d37a12c67532b3823db7 /* governedRelation={"evidence": ["source_port_catalog:PMU:o_clk_16M_mc:41"], "identity": "relation_d37a12c67532b3823db7", "kind": "clock", "qualifiers": [["local_port", "topDigital.pMU.o_clk_16M_mc"], ["reference_level", "block"], ["peer_label", "Main Controller"], ["directionality", "directed"], ["source_details", "wire 16MHz clock for Main Controller"], ["source_table", ""], ["source_page", "41"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}} */;
        connection relation_71046a4fcfa578f86ada : BlockRelation connect topDigital.pMU to topDigital.mainController;
        doc relation_71046a4fcfa578f86ada /* governedRelation={"evidence": ["source_port_catalog:Main Controller:i_clk_32kHz:76"], "identity": "relation_71046a4fcfa578f86ada", "kind": "clock", "qualifiers": [["local_port", "topDigital.mainController.i_clk_32kHz"], ["reference_level", "block"], ["peer_label", "pmu"], ["directionality", "directed"], ["source_details", "clk 32kHz from pmu"], ["source_table", ""], ["source_page", "76"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}} */;
        connection relation_2cb7fbc2d22118700d9e : BlockRelation connect topDigital.pMU to topDigital.mainController;
        doc relation_2cb7fbc2d22118700d9e /* governedRelation={"evidence": ["source_port_catalog:Main Controller:i_clk_16MHz:76"], "identity": "relation_2cb7fbc2d22118700d9e", "kind": "clock", "qualifiers": [["local_port", "topDigital.mainController.i_clk_16MHz"], ["reference_level", "block"], ["peer_label", "pmu"], ["directionality", "directed"], ["source_details", "clk 16MHz from pmu"], ["source_table", ""], ["source_page", "76"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Main Controller", "direction": "", "node": "topDigital.mainController", "port": "", "status": "resolved", "token": "Main Controller"}} */;
        connection relation_76441c370e234450205c : BlockRelation connect topDigital.pMU to topDigital.aDSP;
        doc relation_76441c370e234450205c /* governedRelation={"evidence": ["source_port_catalog:ADSP:stmc_clk:86"], "identity": "relation_76441c370e234450205c", "kind": "clock", "qualifiers": [["local_port", "topDigital.aDSP.stmc_clk"], ["peer_endpoint", "u_pmu.tst_clk_16m"], ["source_details", "wire u_pmu.tst_clk_16m"], ["source_table", ""], ["source_page", "86"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}} */;
        connection relation_be287aada79c3782bcd2 : SignalConnection connect topDigital.pMU.tst_clk_16m to topDigital.aDSP.stmc_clk;
        doc relation_be287aada79c3782bcd2 /* governedRelation={"evidence": ["source_port_catalog:ADSP:stmc_clk:86"], "identity": "relation_be287aada79c3782bcd2", "kind": "clock", "qualifiers": [["local_port", "topDigital.aDSP.stmc_clk"], ["peer_endpoint", "u_pmu.tst_clk_16m"], ["source_details", "wire u_pmu.tst_clk_16m"], ["source_table", ""], ["source_page", "86"]], "reason": "", "relation_class": "signal_connection", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "out", "node": "topDigital.pMU", "port": "tst_clk_16m", "status": "resolved", "token": "u_pmu.tst_clk_16m"}, "status": "resolved", "target": {"block": "ADSP", "direction": "in", "node": "topDigital.aDSP", "port": "stmc_clk", "status": "resolved", "token": "stmc_clk"}} */;
        connection relation_61a9cb1f650c6a88cb72 : BlockRelation connect topDigital.pMU to topDigital.aDSP;
        doc relation_61a9cb1f650c6a88cb72 /* governedRelation={"evidence": ["source_port_catalog:ADSP:HCLK:86"], "identity": "relation_61a9cb1f650c6a88cb72", "kind": "clock", "qualifiers": [["local_port", "topDigital.aDSP.HCLK"], ["peer_endpoint", "u_pmu.clk_stmc"], ["source_details", "wire u_pmu.clk_stmc"], ["source_table", ""], ["source_page", "86"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}} */;
        connection relation_38f66362ecc3cf4a928d : SignalConnection connect topDigital.pMU.clk_stmc to topDigital.aDSP.HCLK;
        doc relation_38f66362ecc3cf4a928d /* governedRelation={"evidence": ["source_port_catalog:ADSP:HCLK:86"], "identity": "relation_38f66362ecc3cf4a928d", "kind": "clock", "qualifiers": [["local_port", "topDigital.aDSP.HCLK"], ["peer_endpoint", "u_pmu.clk_stmc"], ["source_details", "wire u_pmu.clk_stmc"], ["source_table", ""], ["source_page", "86"]], "reason": "", "relation_class": "signal_connection", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "out", "node": "topDigital.pMU", "port": "clk_stmc", "status": "resolved", "token": "u_pmu.clk_stmc"}, "status": "resolved", "target": {"block": "ADSP", "direction": "in", "node": "topDigital.aDSP", "port": "HCLK", "status": "resolved", "token": "HCLK"}} */;
        connection relation_c0388e80b211f6f6e1c8 : BlockRelation connect topDigital.pMU to topDigital.aDSP;
        doc relation_c0388e80b211f6f6e1c8 /* governedRelation={"evidence": ["source_port_catalog:ADSP:HRESETn:86"], "identity": "relation_c0388e80b211f6f6e1c8", "kind": "reset", "qualifiers": [["local_port", "topDigital.aDSP.HRESETn"], ["peer_endpoint", "u_pmu.resetn_stmc"], ["source_details", "wire u_pmu.resetn_stmc"], ["source_table", ""], ["source_page", "86"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}} */;
        connection relation_20e5b8d1401f3e521d20 : SignalConnection connect topDigital.pMU.resetn_stmc to topDigital.aDSP.HRESETn;
        doc relation_20e5b8d1401f3e521d20 /* governedRelation={"evidence": ["source_port_catalog:ADSP:HRESETn:86"], "identity": "relation_20e5b8d1401f3e521d20", "kind": "reset", "qualifiers": [["local_port", "topDigital.aDSP.HRESETn"], ["peer_endpoint", "u_pmu.resetn_stmc"], ["source_details", "wire u_pmu.resetn_stmc"], ["source_table", ""], ["source_page", "86"]], "reason": "", "relation_class": "signal_connection", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "out", "node": "topDigital.pMU", "port": "resetn_stmc", "status": "resolved", "token": "u_pmu.resetn_stmc"}, "status": "resolved", "target": {"block": "ADSP", "direction": "in", "node": "topDigital.aDSP", "port": "HRESETn", "status": "resolved", "token": "HRESETn"}} */;
        connection relation_236fe780c722335e5cb9 : BlockRelation connect topDigital.aDSP to topDigital.pMU;
        doc relation_236fe780c722335e5cb9 /* governedRelation={"evidence": ["source_port_catalog:ADSP:ahb_master_clk_en:87"], "identity": "relation_236fe780c722335e5cb9", "kind": "clock", "qualifiers": [["local_port", "topDigital.aDSP.ahb_master_clk_en"], ["peer_endpoint", "U_pmu.clk_en_s1"], ["source_details", "wire U_pmu.clk_en_s1"], ["source_table", ""], ["source_page", "87"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "ADSP", "direction": "", "node": "topDigital.aDSP", "port": "", "status": "resolved", "token": "ADSP"}, "status": "resolved", "target": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}} */;
        connection relation_b4e20be236b399169b63 : SignalConnection connect topDigital.aDSP.ahb_master_clk_en to topDigital.pMU.clk_en_s1;
        doc relation_b4e20be236b399169b63 /* governedRelation={"evidence": ["source_port_catalog:ADSP:ahb_master_clk_en:87"], "identity": "relation_b4e20be236b399169b63", "kind": "clock", "qualifiers": [["local_port", "topDigital.aDSP.ahb_master_clk_en"], ["peer_endpoint", "U_pmu.clk_en_s1"], ["source_details", "wire U_pmu.clk_en_s1"], ["source_table", ""], ["source_page", "87"]], "reason": "", "relation_class": "signal_connection", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "ADSP", "direction": "out", "node": "topDigital.aDSP", "port": "ahb_master_clk_en", "status": "resolved", "token": "ahb_master_clk_en"}, "status": "resolved", "target": {"block": "PMU", "direction": "in", "node": "topDigital.pMU", "port": "clk_en_s1", "status": "resolved", "token": "U_pmu.clk_en_s1"}} */;
        connection relation_2ea76850fac455563164 : BlockRelation connect topDigital.pMU to topDigital.smartFIFO;
        doc relation_2ea76850fac455563164 /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:HCLK:112"], "identity": "relation_2ea76850fac455563164", "kind": "clock", "qualifiers": [["local_port", "topDigital.smartFIFO.HCLK"], ["peer_endpoint", "u_pmu.clk_fifo"], ["source_details", "AHB Master Handler Clock 16MHz clock u_pmu.clk_fifo"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_f4d1012e243a132e3f8e : SignalConnection connect topDigital.pMU.clk_fifo to topDigital.smartFIFO.HCLK;
        doc relation_f4d1012e243a132e3f8e /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:HCLK:112"], "identity": "relation_f4d1012e243a132e3f8e", "kind": "clock", "qualifiers": [["local_port", "topDigital.smartFIFO.HCLK"], ["peer_endpoint", "u_pmu.clk_fifo"], ["source_details", "AHB Master Handler Clock 16MHz clock u_pmu.clk_fifo"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "signal_connection", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "out", "node": "topDigital.pMU", "port": "clk_fifo", "status": "resolved", "token": "u_pmu.clk_fifo"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "in", "node": "topDigital.smartFIFO", "port": "HCLK", "status": "resolved", "token": "HCLK"}} */;
        connection relation_7a9b5236ea733424c6b5 : BlockRelation connect topDigital.pMU to topDigital.smartFIFO;
        doc relation_7a9b5236ea733424c6b5 /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:HRESETn:112"], "identity": "relation_7a9b5236ea733424c6b5", "kind": "reset", "qualifiers": [["local_port", "topDigital.smartFIFO.HRESETn"], ["peer_endpoint", "u_pmu.resetn_fifo"], ["source_details", "u_pmu.resetn_fifo"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "", "node": "topDigital.pMU", "port": "", "status": "resolved", "token": "PMU"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_fcf103179eeb7c598547 : SignalConnection connect topDigital.pMU.resetn_fifo to topDigital.smartFIFO.HRESETn;
        doc relation_fcf103179eeb7c598547 /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:HRESETn:112"], "identity": "relation_fcf103179eeb7c598547", "kind": "reset", "qualifiers": [["local_port", "topDigital.smartFIFO.HRESETn"], ["peer_endpoint", "u_pmu.resetn_fifo"], ["source_details", "u_pmu.resetn_fifo"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "signal_connection", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "PMU", "direction": "out", "node": "topDigital.pMU", "port": "resetn_fifo", "status": "resolved", "token": "u_pmu.resetn_fifo"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "in", "node": "topDigital.smartFIFO", "port": "HRESETn", "status": "resolved", "token": "HRESETn"}} */;
        connection relation_99f2d0f068c678591a7c : BlockRelation connect topDigital.smartFIFO to topDigital.smartFIFO;
        doc relation_99f2d0f068c678591a7c /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:O_FIFO_RAM_A:112"], "identity": "relation_99f2d0f068c678591a7c", "kind": "signal", "qualifiers": [["local_port", "topDigital.smartFIFO.O_FIFO_RAM_A"], ["peer_endpoint", "u_ca_fifo_bist_c.ags_1"], ["source_details", "[ADDR_WIDTH- 1:0] u_ca_fifo_bist_c.ags_1"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_795a648f46e51fef3036 : BlockRelation connect topDigital.smartFIFO to topDigital.smartFIFO;
        doc relation_795a648f46e51fef3036 /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:O_FIFO_RAM_D:112"], "identity": "relation_795a648f46e51fef3036", "kind": "signal", "qualifiers": [["local_port", "topDigital.smartFIFO.O_FIFO_RAM_D"], ["peer_endpoint", "u_ca_fifo_bist_c.csns_1"], ["source_details", "[23:0] u_ca_fifo_bist_c.csns_1"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_cc77ffb4e665d6ec85dc : BlockRelation connect topDigital.smartFIFO to topDigital.smartFIFO;
        doc relation_cc77ffb4e665d6ec85dc /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:O_FIFO_RAM_CSN:112"], "identity": "relation_cc77ffb4e665d6ec85dc", "kind": "signal", "qualifiers": [["local_port", "topDigital.smartFIFO.O_FIFO_RAM_CSN"], ["peer_endpoint", "u_ca_fifo_bist_c.dgs_1"], ["source_details", "u_ca_fifo_bist_c.dgs_1"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_49db736dcb67fd84a151 : BlockRelation connect topDigital.smartFIFO to topDigital.smartFIFO;
        doc relation_49db736dcb67fd84a151 /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:O_FIFO_RAM_M:112"], "identity": "relation_49db736dcb67fd84a151", "kind": "signal", "qualifiers": [["local_port", "topDigital.smartFIFO.O_FIFO_RAM_M"], ["peer_endpoint", "u_ca_fifo_bist_c.wens_1"], ["source_details", "[23:0] u_ca_fifo_bist_c.wens_1"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_c961cf5ca7829482d45b : BlockRelation connect topDigital.smartFIFO to topDigital.smartFIFO;
        doc relation_c961cf5ca7829482d45b /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:O_FIFO_RAM_WEN:112"], "identity": "relation_c961cf5ca7829482d45b", "kind": "signal", "qualifiers": [["local_port", "topDigital.smartFIFO.O_FIFO_RAM_WEN"], ["peer_endpoint", "u_ca_fifo_bist_c.mgs_1"], ["source_details", "u_ca_fifo_bist_c.mgs_1"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
        connection relation_3530ca822baa8fd53cdc : BlockRelation connect topDigital.smartFIFO to topDigital.smartFIFO;
        doc relation_3530ca822baa8fd53cdc /* governedRelation={"evidence": ["source_port_catalog:Smart FIFO:I_FIFO_RAM_Q:112"], "identity": "relation_3530ca822baa8fd53cdc", "kind": "signal", "qualifiers": [["local_port", "topDigital.smartFIFO.I_FIFO_RAM_Q"], ["peer_endpoint", "u_ca_fifo_bist_c.dgrs_1"], ["source_details", "[23:0] u_ca_fifo_bist_c.dgrs_1"], ["source_table", ""], ["source_page", "112"]], "reason": "", "relation_class": "block_relation", "snapshot_id": "snap-73c872b1307b6adb5eaf843e", "source": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}, "status": "resolved", "target": {"block": "Smart FIFO", "direction": "", "node": "topDigital.smartFIFO", "port": "", "status": "resolved", "token": "Smart FIFO"}} */;
    }

}

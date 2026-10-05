// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 5424834735474f3f97ba3357e63e8703bd7f341f5995c19ba9e75bcba49d8157

package STBIO_Architecture {

    // Generated hierarchical top model; block definitions are in sysml/blocks/.
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
    private import STBIO_DigitalSubsystem::*;

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

        // Level 1 subsystem relationships are derived from the interaction matrix.
        connection analog_to_digital : ArchitectureConnection connect topAnalog to topDigital;


        connection connection_002 : ArchitectureConnection connect topDigital.mainController to topDigital.smartFIFO;
        doc connection_002 /* signal=sample stream and FIFO mode control | trigger=FIFO enabled | notes=stream/bypass/fifo mode routing | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_003 : ArchitectureConnection connect topDigital.smartFIFO to topDigital.iRQLogic;
        doc connection_003 /* signal=watermark/overrun/empty flags | trigger=FIFO status change | notes=interrupt condition generation | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_004 : ArchitectureConnection connect topDigital.regmap to topDigital.mainController;
        doc connection_004 /* signal=configuration writes | trigger=register update | notes=sample-rate/filter/mode setup | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_009 : ArchitectureConnection connect topDigital.pMU to topDigital.mainController;
        doc connection_009 /* signal=power/clock status | trigger=power mode transition | notes=power-aware digital control | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_010 : ArchitectureConnection connect topDigital.bISTController to topDigital.regmap;
        doc connection_010 /* signal=self-test/calibration status | trigger=self-test command | notes=status publication through registers | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_013 : ArchitectureConnection connect topDigital.mainController to topDigital.regmap;
        doc connection_013 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_014 : ArchitectureConnection connect topDigital.mainController to topDigital.smartFIFO;
        doc connection_014 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_015 : ArchitectureConnection connect topDigital.mainController to topDigital.aDSP;
        doc connection_015 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_016 : ArchitectureConnection connect topDigital.aDSP to topDigital.regmap;
        doc connection_016 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_017 : ArchitectureConnection connect topDigital.aDSP to topDigital.sensorHub;
        doc connection_017 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_018 : ArchitectureConnection connect topDigital.aDSP to topDigital.smartFIFO;
        doc connection_018 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_019 : ArchitectureConnection connect topDigital.i2CSPIAHB to topDigital.regmap;
        doc connection_019 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_020 : ArchitectureConnection connect topDigital.i2CSPIAHB to topDigital.sensorHub;
        doc connection_020 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_021 : ArchitectureConnection connect topDigital.i2CSPIAHB to topDigital.iSPU;
        doc connection_021 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_022 : ArchitectureConnection connect topDigital.i2CSPIAHB to topDigital.smartFIFO;
        doc connection_022 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_023 : ArchitectureConnection connect topDigital.i2CSPIAHB to topDigital.aDSP;
        doc connection_023 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_024 : ArchitectureConnection connect topDigital.sensorHub to topDigital.smartFIFO;
        doc connection_024 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_025 : ArchitectureConnection connect topDigital.iSPU to topDigital.regmap;
        doc connection_025 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_026 : ArchitectureConnection connect topDigital.iSPU to topDigital.sensorHub;
        doc connection_026 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_027 : ArchitectureConnection connect topDigital.iSPU to topDigital.smartFIFO;
        doc connection_027 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
        connection connection_028 : ArchitectureConnection connect topDigital.iSPU to topDigital.aDSP;
        doc connection_028 /* signal=XBAR connection | trigger=XBAR matrix cell | notes=XBAR Connection Matrix; source-derived cell | sourceReqIds= | sourceArtifact=artifacts/stage2_mirco_arc/interaction_matrix.csv */;
    }

}

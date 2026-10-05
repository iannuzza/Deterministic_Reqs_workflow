// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 5424834735474f3f97ba3357e63e8703bd7f341f5995c19ba9e75bcba49d8157

package STBIO_Block_PMU {

    private import STBIO_Shared::*;

    part def PMU {
        attribute displayName : String = "PMU";
        attribute description : String = "Sequence POR-driven LDO1V8 enable, 64/32 kHz and 16 MHz clocks, clock-ready signaling, and digital-reset release for boot and power modes.";
        attribute function : String = "Sequence POR-driven LDO1V8 enable, 64/32 kHz and 16 MHz clocks, clock-ready signaling, and digital-reset release for boot and power modes.";
        attribute inputs : String = "VDD/VDD_IO, power-on reset, clock references, clock-start requests, power-mode configuration";
        attribute outputs : String = "LDO and power-domain controls, clock enable/gating and ready status, reset-release signals, power-state status";
        attribute approvedPortCount : Integer = 102;
        attribute linkedRequirementCount : Integer = 31;
        doc /* block=PMU | description=Sequence POR-driven LDO1V8 enable, 64/32 kHz and 16 MHz clocks, clock-ready signaling, and digital-reset release for boot and power modes. */;
        in port clk_16m : ArchitecturePort {
            attribute sourceName = "clk_16m";
            attribute sourceDetails = "wire Clock 16 MHz from analog ring oscillators";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "37";
        }
        in port clk_64k : ArchitecturePort {
            attribute sourceName = "clk_64k";
            attribute sourceDetails = "wire Clock 64kHz from analog ring oscillators";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "37";
        }
        in port POR1V2_1V2 : ArchitecturePort {
            attribute sourceName = "POR1V2_1V2";
            attribute sourceDetails = "wire POR Signal";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "37";
        }
        in port START_CLK_16M : ArchitecturePort {
            attribute sourceName = "START_CLK_16M";
            attribute sourceDetails = "wire Clock ready for 16MHz";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "37";
        }
        in port PDClockF : ArchitecturePort {
            attribute sourceName = "PDClockF";
            attribute sourceDetails = "wire Power Down for 16MHz Ring Oscillator from main controller";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "37";
        }
        in port i_bio_divider : ArchitecturePort {
            attribute sourceName = "i_bio_divider";
            attribute sourceDetails = "wire Enable 32kHz geneartion from 16MHz when a Bio-Channel is activated";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "37";
        }
        in port EN_LDO : ArchitecturePort {
            attribute sourceName = "EN_LDO";
            attribute sourceDetails = "wire enable LDO from main controller";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "37";
        }
        in port PD_CLK_REG : ArchitecturePort {
            attribute sourceName = "PD_CLK_REG";
            attribute sourceDetails = "wire power down 16MHz from Regmap 37";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "37";
        }
        in port EN_LDO1V8_REG : ArchitecturePort {
            attribute sourceName = "EN_LDO1V8_REG";
            attribute sourceDetails = "wire Enable LDO from regmap";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port bist_mode : ArchitecturePort {
            attribute sourceName = "bist_mode";
            attribute sourceDetails = "wire enable bist mode";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port debug_mode : ArchitecturePort {
            attribute sourceName = "debug_mode";
            attribute sourceDetails = "wire enable debug";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port scan_mode : ArchitecturePort {
            attribute sourceName = "scan_mode";
            attribute sourceDetails = "wire enable scan mode";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port scan_enable : ArchitecturePort {
            attribute sourceName = "scan_enable";
            attribute sourceDetails = "wire start scan mode";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port scan_clk : ArchitecturePort {
            attribute sourceName = "scan_clk";
            attribute sourceDetails = "wire scan clk";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port scan_rstn : ArchitecturePort {
            attribute sourceName = "scan_rstn";
            attribute sourceDetails = "wire scan rst";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_bistctlr : ArchitecturePort {
            attribute sourceName = "clk_bistctlr";
            attribute sourceDetails = "wire bist controller and collar clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port rst_bistctlr_n : ArchitecturePort {
            attribute sourceName = "rst_bistctlr_n";
            attribute sourceDetails = "wire bist controller and collar resetn";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_ext_en : ArchitecturePort {
            attribute sourceName = "clk_ext_en";
            attribute sourceDetails = "wire enable external clock from pad";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_ext_slow : ArchitecturePort {
            attribute sourceName = "clk_ext_slow";
            attribute sourceDetails = "wire external clock 32kHz";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port i_en_sh_clk : ArchitecturePort {
            attribute sourceName = "i_en_sh_clk";
            attribute sourceDetails = "wire enable sensor hub clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port i_senshub_clk_sel : ArchitecturePort {
            attribute sourceName = "i_senshub_clk_sel";
            attribute sourceDetails = "wire [2:0] selector for sensor hub clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port i_test_clk_fast : ArchitecturePort {
            attribute sourceName = "i_test_clk_fast";
            attribute sourceDetails = "wire enable test and trimming for 16MHz clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port i_half_charge_ldo : ArchitecturePort {
            attribute sourceName = "i_half_charge_ldo";
            attribute sourceDetails = "wire enable the low power mode for ldo when only ppg is selected";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port mask_en_ldo_pdclkf : ArchitecturePort {
            attribute sourceName = "mask_en_ldo_pdclkf";
            attribute sourceDetails = "wire mask the control of pdf and ldo control during boot";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_en_s0 : ArchitecturePort {
            attribute sourceName = "clk_en_s0";
            attribute sourceDetails = "wire clock gating logic inside stredl_afe_top";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_en_s1 : ArchitecturePort {
            attribute sourceName = "clk_en_s1";
            attribute sourceDetails = "wire if present should be HSEL STMC AHB Master";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_en_s2_i2c : ArchitecturePort {
            attribute sourceName = "clk_en_s2_i2c";
            attribute sourceDetails = "wire if present should be HSEL STMC AHB Master";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_en_s2_on : ArchitecturePort {
            attribute sourceName = "clk_en_s2_on";
            attribute sourceDetails = "wire clk gating ON from AHB I2C/SPI Interface";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_en_s2_off : ArchitecturePort {
            attribute sourceName = "clk_en_s2_off";
            attribute sourceDetails = "wire clk gating OFF from AHB I2C/SPI Interface";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_en_s3 : ArchitecturePort {
            attribute sourceName = "clk_en_s3";
            attribute sourceDetails = "wire clk gating from AHB Master Main Controller 38";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "38";
        }
        in port clk_en_s4 : ArchitecturePort {
            attribute sourceName = "clk_en_s4";
            attribute sourceDetails = "wire clock gating logic inside stredl_afe_top";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port clk_en_s5 : ArchitecturePort {
            attribute sourceName = "clk_en_s5";
            attribute sourceDetails = "wire clock gating logic inside masterblaze_ahb";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port clk_en_m0 : ArchitecturePort {
            attribute sourceName = "clk_en_m0";
            attribute sourceDetails = "wire clock gating logic inside stredl_afe_top";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port clk_en_m1 : ArchitecturePort {
            attribute sourceName = "clk_en_m1";
            attribute sourceDetails = "wire HSEL M1 from xbar to STMC AHB Slave";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port clk_en_m2 : ArchitecturePort {
            attribute sourceName = "clk_en_m2";
            attribute sourceDetails = "wire HSEL M2 from xbar to FIFO";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port clk_en_m22 : ArchitecturePort {
            attribute sourceName = "clk_en_m22";
            attribute sourceDetails = "wire HSEL M2 from xbar to MASTERBLAZE";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port clk_en_m3 : ArchitecturePort {
            attribute sourceName = "clk_en_m3";
            attribute sourceDetails = "wire HSEL M3 from xbar to Regmap";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port iso_i : ArchitecturePort {
            attribute sourceName = "iso_i";
            attribute sourceDetails = "wire from register";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port vdden_i : ArchitecturePort {
            attribute sourceName = "vdden_i";
            attribute sourceDetails = "wire enable ISPU Power Island";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port i_start_operative_16MHz : ArchitecturePort {
            attribute sourceName = "i_start_operative_16MHz";
            attribute sourceDetails = "wire enable the lead of check";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port main_ctrl_sw_resetn : ArchitecturePort {
            attribute sourceName = "main_ctrl_sw_resetn";
            attribute sourceDetails = "wire soft reset for main controller";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port stmc_sw_resetn : ArchitecturePort {
            attribute sourceName = "stmc_sw_resetn";
            attribute sourceDetails = "wire adsp soft reset";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port fifo_sw_resetn : ArchitecturePort {
            attribute sourceName = "fifo_sw_resetn";
            attribute sourceDetails = "wire fifo soft reset";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port masterblaze_sw_resetn : ArchitecturePort {
            attribute sourceName = "masterblaze_sw_resetn";
            attribute sourceDetails = "wire sensor hub soft reset";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port regmap_sw_resetn : ArchitecturePort {
            attribute sourceName = "regmap_sw_resetn";
            attribute sourceDetails = "wire regmap soft reset";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port adsp_run : ArchitecturePort {
            attribute sourceName = "adsp_run";
            attribute sourceDetails = "wire adsp is running";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port adsp_xbar_sw_en : ArchitecturePort {
            attribute sourceName = "adsp_xbar_sw_en";
            attribute sourceDetails = "wire adsp clk ahb";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port i_en_clk_gsr_16M : ArchitecturePort {
            attribute sourceName = "i_en_clk_gsr_16M";
            attribute sourceDetails = "wire enable the clock for gsr digital circuit";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port i_en_ck_m_p_q : ArchitecturePort {
            attribute sourceName = "i_en_ck_m_p_q";
            attribute sourceDetails = "wire enable quadrature and phase clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port i_en_clk_mod_debug : ArchitecturePort {
            attribute sourceName = "i_en_clk_mod_debug";
            attribute sourceDetails = "wire enable the clock modulation debug";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port i_en_chop_ref : ArchitecturePort {
            attribute sourceName = "i_en_chop_ref";
            attribute sourceDetails = "wire enable chopper clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port i_en_ck_chop_imp : ArchitecturePort {
            attribute sourceName = "i_en_ck_chop_imp";
            attribute sourceDetails = "wire enable chopper clock for bia";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port i_en_ck_hc2_10k : ArchitecturePort {
            attribute sourceName = "i_en_ck_hc2_10k";
            attribute sourceDetails = "wire enable health channel clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port i_freq_bia_m_p_q : ArchitecturePort {
            attribute sourceName = "i_freq_bia_m_p_q";
            attribute sourceDetails = "wire [2:0] frequency selector for phase and quadrature 39";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "39";
        }
        in port i_en_clk_16MHz_sleep : ArchitecturePort {
            attribute sourceName = "i_en_clk_16MHz_sleep";
            attribute sourceDetails = "wire enable clock in SLEEP mode when a bio- channel is selected";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        in port EN_ADC_TEST_LOW_NOISE : ArchitecturePort {
            attribute sourceName = "EN_ADC_TEST_LOW_NOISE";
            attribute sourceDetails = "wire enable adc test low noise";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        in port EN_ADC_TEST_FAST : ArchitecturePort {
            attribute sourceName = "EN_ADC_TEST_FAST";
            attribute sourceDetails = "wire enable adc test fast";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        in port if_sh_ck_in : ArchitecturePort {
            attribute sourceName = "if_sh_ck_in";
            attribute sourceDetails = "wire sensor hub clock interface";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port o_EN_LDO1V8 : ArchitecturePort {
            attribute sourceName = "o_EN_LDO1V8";
            attribute sourceDetails = "wire enable ldo to analog domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port o_PD_CLKF : ArchitecturePort {
            attribute sourceName = "o_PD_CLKF";
            attribute sourceDetails = "wire power down 16MHz clock to analog domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port o_CLK_16M_READY : ArchitecturePort {
            attribute sourceName = "o_CLK_16M_READY";
            attribute sourceDetails = "wire clock ready to the digital domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port o_DIS_RC_VIREF : ArchitecturePort {
            attribute sourceName = "o_DIS_RC_VIREF";
            attribute sourceDetails = "wire dis rc viref to the analog domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port pd_osc_clk32k : ArchitecturePort {
            attribute sourceName = "pd_osc_clk32k";
            attribute sourceDetails = "wire power down for clk 64kHz";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port tst_clk_32k : ArchitecturePort {
            attribute sourceName = "tst_clk_32k";
            attribute sourceDetails = "wire clock slow 32k to main_controller";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port tst_clk_16m : ArchitecturePort {
            attribute sourceName = "tst_clk_16m";
            attribute sourceDetails = "wire clock fast 16M";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port tst_clk_bistctlr : ArchitecturePort {
            attribute sourceName = "tst_clk_bistctlr";
            attribute sourceDetails = "wire test clock for bist ctrl";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port tst_rst_bistctlr_n : ArchitecturePort {
            attribute sourceName = "tst_rst_bistctlr_n";
            attribute sourceDetails = "wire test reset for bist ctrl";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_stredl : ArchitecturePort {
            attribute sourceName = "clk_stredl";
            attribute sourceDetails = "wire clock gating logic inside stredl_afe_top";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_xbar : ArchitecturePort {
            attribute sourceName = "clk_xbar";
            attribute sourceDetails = "wire xbar clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_intf : ArchitecturePort {
            attribute sourceName = "clk_intf";
            attribute sourceDetails = "wire interface clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_main_ctrl : ArchitecturePort {
            attribute sourceName = "clk_main_ctrl";
            attribute sourceDetails = "wire clock for main controller";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_stmc : ArchitecturePort {
            attribute sourceName = "clk_stmc";
            attribute sourceDetails = "wire adsp clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_stmc_ahb : ArchitecturePort {
            attribute sourceName = "clk_stmc_ahb";
            attribute sourceDetails = "wire adsp clk elaboration";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_fifo : ArchitecturePort {
            attribute sourceName = "clk_fifo";
            attribute sourceDetails = "wire fifo clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_masterblaze_m : ArchitecturePort {
            attribute sourceName = "clk_masterblaze_m";
            attribute sourceDetails = "wire sensor hub master clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_masterblaze_s : ArchitecturePort {
            attribute sourceName = "clk_masterblaze_s";
            attribute sourceDetails = "wire sensor hub slave clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port clk_regmap : ArchitecturePort {
            attribute sourceName = "clk_regmap";
            attribute sourceDetails = "wire regmap clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port o_clk_ext_en : ArchitecturePort {
            attribute sourceName = "o_clk_ext_en";
            attribute sourceDetails = "wire enable external clock 40";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "40";
        }
        out port resetn_stredl : ArchitecturePort {
            attribute sourceName = "resetn_stredl";
            attribute sourceDetails = "wire reset mngmt inside stredl_afe_top";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port resetn_xbar : ArchitecturePort {
            attribute sourceName = "resetn_xbar";
            attribute sourceDetails = "wire xbar reset";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port resetn_intf : ArchitecturePort {
            attribute sourceName = "resetn_intf";
            attribute sourceDetails = "wire reset interface";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port resetn_main_ctrl : ArchitecturePort {
            attribute sourceName = "resetn_main_ctrl";
            attribute sourceDetails = "wire reset main controller";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port resetn_32k_main_ctrl : ArchitecturePort {
            attribute sourceName = "resetn_32k_main_ctrl";
            attribute sourceDetails = "wire reset 32kHz domain main controller";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port resetn_stmc : ArchitecturePort {
            attribute sourceName = "resetn_stmc";
            attribute sourceDetails = "wire reset adsp";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port resetn_fifo : ArchitecturePort {
            attribute sourceName = "resetn_fifo";
            attribute sourceDetails = "wire reset FIFO";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port resetn_masterblaze : ArchitecturePort {
            attribute sourceName = "resetn_masterblaze";
            attribute sourceDetails = "wire reset sensor hub";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port resetn_regmap : ArchitecturePort {
            attribute sourceName = "resetn_regmap";
            attribute sourceDetails = "wire reset regmap";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_trimming_clk_fast : ArchitecturePort {
            attribute sourceName = "o_trimming_clk_fast";
            attribute sourceDetails = "wire trimming output clock fast";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port iso_o : ArchitecturePort {
            attribute sourceName = "iso_o";
            attribute sourceDetails = "wire left open . to be connected in synthesis";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port vdden_o : ArchitecturePort {
            attribute sourceName = "vdden_o";
            attribute sourceDetails = "wire to be connected to psw_ctrl.VDDIEN";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_ck_bg : ArchitecturePort {
            attribute sourceName = "o_ck_bg";
            attribute sourceDetails = "wire bg clock to analog domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_sh_clk : ArchitecturePort {
            attribute sourceName = "o_sh_clk";
            attribute sourceDetails = "wire sensor hub clock";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_ck_chop_imp : ArchitecturePort {
            attribute sourceName = "o_ck_chop_imp";
            attribute sourceDetails = "wire chopper bia clock to analog domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_ck_m : ArchitecturePort {
            attribute sourceName = "o_ck_m";
            attribute sourceDetails = "wire modulation clock to analog domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_ck_hc2_10k : ArchitecturePort {
            attribute sourceName = "o_ck_hc2_10k";
            attribute sourceDetails = "wire healt channel 10kHz clock to analog domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_ck_p : ArchitecturePort {
            attribute sourceName = "o_ck_p";
            attribute sourceDetails = "wire phase clock to analog domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_ck_q : ArchitecturePort {
            attribute sourceName = "o_ck_q";
            attribute sourceDetails = "wire quadrature clock to analog domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_clk_16M_mc : ArchitecturePort {
            attribute sourceName = "o_clk_16M_mc";
            attribute sourceDetails = "wire 16MHz clock for Main Controller";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_clk_dft_adc : ArchitecturePort {
            attribute sourceName = "o_clk_dft_adc";
            attribute sourceDetails = "wire 16MHz clock for ADC DFT";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_clk_gsr_16M : ArchitecturePort {
            attribute sourceName = "o_clk_gsr_16M";
            attribute sourceDetails = "wire gsr clock to digital domain";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_ADC_clk_serial_dft : ArchitecturePort {
            attribute sourceName = "o_ADC_clk_serial_dft";
            attribute sourceDetails = "wire adc serial clock in dft";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }
        out port o_sh_clk_gate : ArchitecturePort {
            attribute sourceName = "o_sh_clk_gate";
            attribute sourceDetails = "wire status clk reg clk sh 16Mhz 41";
            attribute sourceTable = "PMU I/O List";
            attribute sourcePage = "41";
        }

        requirement def IPOS_PMU_001 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0104";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-001";
            doc /* When the device is turned on, i_POR1V2_1V2 shall be high. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_001 : IPOS_PMU_001;
        doc /* iposReqId=IPOS-PMU-001 | sourceReqId=DDS_STBIO1_0104 | When the device is turned on, i_POR1V2_1V2 shall be high. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-001 -> approved source requirement DDS_STBIO1_0104 */;
        satisfy req_IPOS_PMU_001 by self;
        requirement def IPOS_PMU_002 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0105";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-002";
            doc /* When i_POR1V2_1V2 is low, o_ EN_LDO1V8 shall be low. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_002 : IPOS_PMU_002;
        doc /* iposReqId=IPOS-PMU-002 | sourceReqId=DDS_STBIO1_0105 | When i_POR1V2_1V2 is low, o_ EN_LDO1V8 shall be low. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-002 -> approved source requirement DDS_STBIO1_0105 */;
        satisfy req_IPOS_PMU_002 by self;
        requirement def IPOS_PMU_003 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0106";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-003";
            doc /* When i_POR1V2_1V2 is low, o_PD_CLKF shall be high. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_003 : IPOS_PMU_003;
        doc /* iposReqId=IPOS-PMU-003 | sourceReqId=DDS_STBIO1_0106 | When i_POR1V2_1V2 is low, o_PD_CLKF shall be high. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-003 -> approved source requirement DDS_STBIO1_0106 */;
        satisfy req_IPOS_PMU_003 by self;
        requirement def IPOS_PMU_004 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0107";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-004";
            doc /* When i_POR1V2_1V2 is low, o_CLK_16M_READY shall be low. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_004 : IPOS_PMU_004;
        doc /* iposReqId=IPOS-PMU-004 | sourceReqId=DDS_STBIO1_0107 | When i_POR1V2_1V2 is low, o_CLK_16M_READY shall be low. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-004 -> approved source requirement DDS_STBIO1_0107 */;
        satisfy req_IPOS_PMU_004 by self;
        requirement def IPOS_PMU_005 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0108";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-005";
            doc /* When i_POR1V2_1V2 is low, o_DIS_RC_VIREF shall be high. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_005 : IPOS_PMU_005;
        doc /* iposReqId=IPOS-PMU-005 | sourceReqId=DDS_STBIO1_0108 | When i_POR1V2_1V2 is low, o_DIS_RC_VIREF shall be high. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-005 -> approved source requirement DDS_STBIO1_0108 */;
        satisfy req_IPOS_PMU_005 by self;
        requirement def IPOS_PMU_006 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0109";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-006";
            doc /* When i_POR1V2_1V2 rises, after at least 10 cycles of i_clk_64k (64kHz), o_ EN_LDO1V8 shall be high and the clk_64k_divided is considered stable. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_006 : IPOS_PMU_006;
        doc /* iposReqId=IPOS-PMU-006 | sourceReqId=DDS_STBIO1_0109 | When i_POR1V2_1V2 rises, after at least 10 cycles of i_clk_64k (64kHz), o_ EN_LDO1V8 shall be high and the clk_64k_divided is considered stable. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-006 -> approved source requirement DDS_STBIO1_0109 */;
        satisfy req_IPOS_PMU_006 by self;
        requirement def IPOS_PMU_007 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0110";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-007";
            doc /* When clk_64k_divided is stable, after at least 352 cycles of clk_64k_divided (32kHz), o_DIS_RC_VIREF shall be low. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_007 : IPOS_PMU_007;
        doc /* iposReqId=IPOS-PMU-007 | sourceReqId=DDS_STBIO1_0110 | When clk_64k_divided is stable, after at least 352 cycles of clk_64k_divided (32kHz), o_DIS_RC_VIREF shall be low. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-007 -> approved source requirement DDS_STBIO1_0110 */;
        satisfy req_IPOS_PMU_007 by self;
        requirement def IPOS_PMU_008 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0111";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-008";
            doc /* When i_mask_en_ldo_pdclkf_reg and o_EN_LDO1V8 are set to 1, o_PD_CLKF shall be low after at least 40 cycles of the clk_64k_divided. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_008 : IPOS_PMU_008;
        doc /* iposReqId=IPOS-PMU-008 | sourceReqId=DDS_STBIO1_0111 | When i_mask_en_ldo_pdclkf_reg and o_EN_LDO1V8 are set to 1, o_PD_CLKF shall be low after at least 40 cycles of the clk_64k_divided. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-008 -> approved source requirement DDS_STBIO1_0111 */;
        satisfy req_IPOS_PMU_008 by self;
        requirement def IPOS_PMU_009 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0112";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-009";
            doc /* When i_START_CLK_16M is high, after at least 20 cycles of i_clk_16M (16MHz), o_CLK_16M_READY shall be high. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_009 : IPOS_PMU_009;
        doc /* iposReqId=IPOS-PMU-009 | sourceReqId=DDS_STBIO1_0112 | When i_START_CLK_16M is high, after at least 20 cycles of i_clk_16M (16MHz), o_CLK_16M_READY shall be high. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-009 -> approved source requirement DDS_STBIO1_0112 */;
        satisfy req_IPOS_PMU_009 by self;
        requirement def IPOS_PMU_010 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0113";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-010";
            doc /* When i_START_CLK_16M is high for the first time, after at least 20 cycles of i_clk_16M (16MHz), o_main_resetn shall be high. [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_010 : IPOS_PMU_010;
        doc /* iposReqId=IPOS-PMU-010 | sourceReqId=DDS_STBIO1_0113 | When i_START_CLK_16M is high for the first time, after at least 20 cycles of i_clk_16M (16MHz), o_main_resetn shall be high. [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-010 -> approved source requirement DDS_STBIO1_0113 */;
        satisfy req_IPOS_PMU_010 by self;
        requirement def IPOS_PMU_011 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0114";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-011";
            doc /* At the release of the POR signal from the analog domain, the PMU shall manage the turn-on of the LDO1V8 and starts clocks Start-Up Sequence (reported in PMU IPOS) [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_011 : IPOS_PMU_011;
        doc /* iposReqId=IPOS-PMU-011 | sourceReqId=DDS_STBIO1_0114 | At the release of the POR signal from the analog domain, the PMU shall manage the turn-on of the LDO1V8 and starts clocks Start-Up Sequence (reported in PMU IPOS) [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-011 -> approved source requirement DDS_STBIO1_0114 */;
        satisfy req_IPOS_PMU_011 by self;
        requirement def IPOS_PMU_012 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0115";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-012";
            doc /* After At least 2 ms from the Release of the POR, the reset of the digital domain shall be de- asserted (an overlook on this part is described in the PMU IPOS) and the device shall start the Boot Phase [TO: IPOS_PMU] */;
        }
        requirement req_IPOS_PMU_012 : IPOS_PMU_012;
        doc /* iposReqId=IPOS-PMU-012 | sourceReqId=DDS_STBIO1_0115 | After At least 2 ms from the Release of the POR, the reset of the digital domain shall be de- asserted (an overlook on this part is described in the PMU IPOS) and the device shall start the Boot Phase [TO: IPOS_PMU] */;
        doc /* coverageDependency: IPOS-PMU-012 -> approved source requirement DDS_STBIO1_0115 */;
        satisfy req_IPOS_PMU_012 by self;
        requirement def IPOS_PMU_013 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1020";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-013";
            doc /* The stbio1_top.clk_16m signal shall be connected to the stbio1_top.dig_wrapper_LV.u_pmu.clk_16m signal, with frequency 16 MHz and without clock gating. */;
        }
        requirement req_IPOS_PMU_013 : IPOS_PMU_013;
        doc /* iposReqId=IPOS-PMU-013 | sourceReqId=DDS_STBIO1_1020 | The stbio1_top.clk_16m signal shall be connected to the stbio1_top.dig_wrapper_LV.u_pmu.clk_16m signal, with frequency 16 MHz and without clock gating. */;
        doc /* coverageDependency: IPOS-PMU-013 -> approved source requirement DDS_STBIO1_1020 */;
        satisfy req_IPOS_PMU_013 by self;
        requirement def IPOS_PMU_014 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1021";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-014";
            doc /* The stbio1_top.clk_64k signal shall be connected to the stbio1_top.dig_wrapper_LV.u_pmu.clk_64k signal, with frequency 64 kHz and without clock gating. */;
        }
        requirement req_IPOS_PMU_014 : IPOS_PMU_014;
        doc /* iposReqId=IPOS-PMU-014 | sourceReqId=DDS_STBIO1_1021 | The stbio1_top.clk_64k signal shall be connected to the stbio1_top.dig_wrapper_LV.u_pmu.clk_64k signal, with frequency 64 kHz and without clock gating. */;
        doc /* coverageDependency: IPOS-PMU-014 -> approved source requirement DDS_STBIO1_1021 */;
        satisfy req_IPOS_PMU_014 by self;
        requirement def IPOS_PMU_015 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1022";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-015";
            doc /* The stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft signal shall be connected to the stbio1_top.dig_wrapper_LV.u_ADSP.stmc_clk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.adsp_run | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        }
        requirement req_IPOS_PMU_015 : IPOS_PMU_015;
        doc /* iposReqId=IPOS-PMU-015 | sourceReqId=DDS_STBIO1_1022 | The stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft signal shall be connected to the stbio1_top.dig_wrapper_LV.u_ADSP.stmc_clk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.adsp_run | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        doc /* coverageDependency: IPOS-PMU-015 -> approved source requirement DDS_STBIO1_1022 */;
        satisfy req_IPOS_PMU_015 by self;
        requirement def IPOS_PMU_016 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1023";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-016";
            doc /* The stbio1_top.dig_wrapper_LV.u_pmu.w_sh_clk signal shall be connected to the stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.sys_clk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.i_en_sh_clk | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        }
        requirement req_IPOS_PMU_016 : IPOS_PMU_016;
        doc /* iposReqId=IPOS-PMU-016 | sourceReqId=DDS_STBIO1_1023 | The stbio1_top.dig_wrapper_LV.u_pmu.w_sh_clk signal shall be connected to the stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.sys_clk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.i_en_sh_clk | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        doc /* coverageDependency: IPOS-PMU-016 -> approved source requirement DDS_STBIO1_1023 */;
        satisfy req_IPOS_PMU_016 by self;
        requirement def IPOS_PMU_017 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1024";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-017";
            doc /* The stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft signal shall be connected to the stbio1_top.dig_wrapper_LV.u_xbar_afe.hclk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.clk_xbar_en | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        }
        requirement req_IPOS_PMU_017 : IPOS_PMU_017;
        doc /* iposReqId=IPOS-PMU-017 | sourceReqId=DDS_STBIO1_1024 | The stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft signal shall be connected to the stbio1_top.dig_wrapper_LV.u_xbar_afe.hclk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.clk_xbar_en | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        doc /* coverageDependency: IPOS-PMU-017 -> approved source requirement DDS_STBIO1_1024 */;
        satisfy req_IPOS_PMU_017 by self;
        requirement def IPOS_PMU_018 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1025";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-018";
            doc /* The u_stbio1_top.u_pmu.u_device_startup.tst_clk_32k signal shall be connected to the stbio1_top.dig_wrapper_LV.tst_clk_32k signal, with frequency 32 kHz and without clock gating. */;
        }
        requirement req_IPOS_PMU_018 : IPOS_PMU_018;
        doc /* iposReqId=IPOS-PMU-018 | sourceReqId=DDS_STBIO1_1025 | The u_stbio1_top.u_pmu.u_device_startup.tst_clk_32k signal shall be connected to the stbio1_top.dig_wrapper_LV.tst_clk_32k signal, with frequency 32 kHz and without clock gating. */;
        doc /* coverageDependency: IPOS-PMU-018 -> approved source requirement DDS_STBIO1_1025 */;
        satisfy req_IPOS_PMU_018 by self;
        requirement def IPOS_PMU_019 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1026";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-019";
            doc /* The stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_16m signal shall be connected to the stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_16MHz signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.i_en_clk_16MHz_sleep | stbio1_top.dig_wrapper_LV.u_pm u.scan_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        }
        requirement req_IPOS_PMU_019 : IPOS_PMU_019;
        doc /* iposReqId=IPOS-PMU-019 | sourceReqId=DDS_STBIO1_1026 | The stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_16m signal shall be connected to the stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_16MHz signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.i_en_clk_16MHz_sleep | stbio1_top.dig_wrapper_LV.u_pm u.scan_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        doc /* coverageDependency: IPOS-PMU-019 -> approved source requirement DDS_STBIO1_1026 */;
        satisfy req_IPOS_PMU_019 by self;
        requirement def IPOS_PMU_020 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1027";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-020";
            doc /* The stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_32k signal shall be connected to the stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_32kHz signal, with frequency 32 kHz and without clock gating. */;
        }
        requirement req_IPOS_PMU_020 : IPOS_PMU_020;
        doc /* iposReqId=IPOS-PMU-020 | sourceReqId=DDS_STBIO1_1027 | The stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_32k signal shall be connected to the stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_32kHz signal, with frequency 32 kHz and without clock gating. */;
        doc /* coverageDependency: IPOS-PMU-020 -> approved source requirement DDS_STBIO1_1027 */;
        satisfy req_IPOS_PMU_020 by self;
        requirement def IPOS_PMU_021 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1050";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-021";
            doc /* The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_stmcu_stbio1_top.dig_wrapper_LV.u_ADSP.HRESETn signal. */;
        }
        requirement req_IPOS_PMU_021 : IPOS_PMU_021;
        doc /* iposReqId=IPOS-PMU-021 | sourceReqId=DDS_STBIO1_1050 | The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_stmcu_stbio1_top.dig_wrapper_LV.u_ADSP.HRESETn signal. */;
        doc /* coverageDependency: IPOS-PMU-021 -> approved source requirement DDS_STBIO1_1050 */;
        satisfy req_IPOS_PMU_021 by self;
        requirement def IPOS_PMU_022 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1051";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-022";
            doc /* The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_masterblazeu_stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.HRESETn signal. */;
        }
        requirement req_IPOS_PMU_022 : IPOS_PMU_022;
        doc /* iposReqId=IPOS-PMU-022 | sourceReqId=DDS_STBIO1_1051 | The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_masterblazeu_stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.HRESETn signal. */;
        doc /* coverageDependency: IPOS-PMU-022 -> approved source requirement DDS_STBIO1_1051 */;
        satisfy req_IPOS_PMU_022 by self;
        requirement def IPOS_PMU_023 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1052";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-023";
            doc /* The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_regmapu_stbio1_top.dig_wrapper_LV.u_regmap_otp.hresetn signal. */;
        }
        requirement req_IPOS_PMU_023 : IPOS_PMU_023;
        doc /* iposReqId=IPOS-PMU-023 | sourceReqId=DDS_STBIO1_1052 | The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_regmapu_stbio1_top.dig_wrapper_LV.u_regmap_otp.hresetn signal. */;
        doc /* coverageDependency: IPOS-PMU-023 -> approved source requirement DDS_STBIO1_1052 */;
        satisfy req_IPOS_PMU_023 by self;
        requirement def IPOS_PMU_024 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1053";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-024";
            doc /* The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_fifou_stbio1_top.dig_wrapper_LV.u_multi_channel_fifo_top.HRESETn signal. */;
        }
        requirement req_IPOS_PMU_024 : IPOS_PMU_024;
        doc /* iposReqId=IPOS-PMU-024 | sourceReqId=DDS_STBIO1_1053 | The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_fifou_stbio1_top.dig_wrapper_LV.u_multi_channel_fifo_top.HRESETn signal. */;
        doc /* coverageDependency: IPOS-PMU-024 -> approved source requirement DDS_STBIO1_1053 */;
        satisfy req_IPOS_PMU_024 by self;
        requirement def IPOS_PMU_025 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_1054";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-025";
            doc /* The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_main_ctrlu_stbio1_top.dig_wrapper_LV.u_main_controller_top.i_rstn signal. */;
        }
        requirement req_IPOS_PMU_025 : IPOS_PMU_025;
        doc /* iposReqId=IPOS-PMU-025 | sourceReqId=DDS_STBIO1_1054 | The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_main_ctrlu_stbio1_top.dig_wrapper_LV.u_main_controller_top.i_rstn signal. */;
        doc /* coverageDependency: IPOS-PMU-025 -> approved source requirement DDS_STBIO1_1054 */;
        satisfy req_IPOS_PMU_025 by self;
        requirement def IPOS_PMU_026 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_2024";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-026";
            doc /* The stbio1_top.dig_wrapper_LV.u_pmuclk_xbar signal shall be connected to the stbio1_top.dig_wrapper_LV.u.fifo.HCLK signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m2 | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m2_reg | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        }
        requirement req_IPOS_PMU_026 : IPOS_PMU_026;
        doc /* iposReqId=IPOS-PMU-026 | sourceReqId=DDS_STBIO1_2024 | The stbio1_top.dig_wrapper_LV.u_pmuclk_xbar signal shall be connected to the stbio1_top.dig_wrapper_LV.u.fifo.HCLK signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m2 | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m2_reg | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        doc /* coverageDependency: IPOS-PMU-026 -> approved source requirement DDS_STBIO1_2024 */;
        satisfy req_IPOS_PMU_026 by self;
        requirement def IPOS_PMU_027 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_2025";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-027";
            doc /* The stbio1_top.dig_wrapper_LV.u_pmu.clk_stredl signal shall be connected to the stbio1_top.dig_wrapper_LV.u_ispu.clk signal, with frequency 16 MHz and without clock gating. */;
        }
        requirement req_IPOS_PMU_027 : IPOS_PMU_027;
        doc /* iposReqId=IPOS-PMU-027 | sourceReqId=DDS_STBIO1_2025 | The stbio1_top.dig_wrapper_LV.u_pmu.clk_stredl signal shall be connected to the stbio1_top.dig_wrapper_LV.u_ispu.clk signal, with frequency 16 MHz and without clock gating. */;
        doc /* coverageDependency: IPOS-PMU-027 -> approved source requirement DDS_STBIO1_2025 */;
        satisfy req_IPOS_PMU_027 by self;
        requirement def IPOS_PMU_028 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_2026";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-028";
            doc /* The stbio1_top.dig_wrapper_LV.u_pmu.clk_xbar signal shall be connected to the stbio1_top.dig_wrapper_LV.u_regmap_otp.hclk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3 | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3_reg | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_s3 | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        }
        requirement req_IPOS_PMU_028 : IPOS_PMU_028;
        doc /* iposReqId=IPOS-PMU-028 | sourceReqId=DDS_STBIO1_2026 | The stbio1_top.dig_wrapper_LV.u_pmu.clk_xbar signal shall be connected to the stbio1_top.dig_wrapper_LV.u_regmap_otp.hclk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3 | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3_reg | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_s3 | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable. */;
        doc /* coverageDependency: IPOS-PMU-028 -> approved source requirement DDS_STBIO1_2026 */;
        satisfy req_IPOS_PMU_028 by self;
        requirement def IPOS_PMU_029 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_2052";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-029";
            doc /* The stbio1_top.dig_wrapper_LV.u_pmu. signal shall be connected to the u_device_startup.u_por_main_resetn.RST_N_FF[0]u_stbio1_top.dig_wrapper_LV.u_xbar_afe.hresetn signal. */;
        }
        requirement req_IPOS_PMU_029 : IPOS_PMU_029;
        doc /* iposReqId=IPOS-PMU-029 | sourceReqId=DDS_STBIO1_2052 | The stbio1_top.dig_wrapper_LV.u_pmu. signal shall be connected to the u_device_startup.u_por_main_resetn.RST_N_FF[0]u_stbio1_top.dig_wrapper_LV.u_xbar_afe.hresetn signal. */;
        doc /* coverageDependency: IPOS-PMU-029 -> approved source requirement DDS_STBIO1_2052 */;
        satisfy req_IPOS_PMU_029 by self;
        requirement def IPOS_PMU_030 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_2053";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-030";
            doc /* The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_regmapu_stbio1_top.dig_wrapper_LV.u_ispu.main_rst_n signal. */;
        }
        requirement req_IPOS_PMU_030 : IPOS_PMU_030;
        doc /* iposReqId=IPOS-PMU-030 | sourceReqId=DDS_STBIO1_2053 | The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_regmapu_stbio1_top.dig_wrapper_LV.u_ispu.main_rst_n signal. */;
        doc /* coverageDependency: IPOS-PMU-030 -> approved source requirement DDS_STBIO1_2053 */;
        satisfy req_IPOS_PMU_030 by self;
        requirement def IPOS_PMU_031 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_2054";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PMU-031";
            doc /* The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_32k_main_ctrlu_stbio1_top.dig_wrapper_LV.u_main_controller_top.i_rstn_sync_32 signal. */;
        }
        requirement req_IPOS_PMU_031 : IPOS_PMU_031;
        doc /* iposReqId=IPOS-PMU-031 | sourceReqId=DDS_STBIO1_2054 | The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_32k_main_ctrlu_stbio1_top.dig_wrapper_LV.u_main_controller_top.i_rstn_sync_32 signal. */;
        doc /* coverageDependency: IPOS-PMU-031 -> approved source requirement DDS_STBIO1_2054 */;
        satisfy req_IPOS_PMU_031 by self;
    }

}

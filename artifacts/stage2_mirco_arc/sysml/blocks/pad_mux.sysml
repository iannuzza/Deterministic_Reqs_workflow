// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 8d22eb86b9a584c32e1fedacf6d98a199b8f93896143054eb1c8b2075b0ea372

package STBIO_Block_PadMux {

    private import STBIO_Shared::*;

    part def PadMux {
        attribute displayName : String = "Pad Mux";
        attribute description : String = "Route source-specified functional, scan, BIST, debug, and ISPU-debug signals to and from device pads.";
        attribute function : String = "Route source-specified functional, scan, BIST, debug, and ISPU-debug signals to and from device pads.";
        attribute inputs : String = "Mode selection, register-map controls, test controls, and internal block outputs";
        attribute outputs : String = "Pad controls, test observations, and routed internal signals";
        attribute approvedPortCount : Integer = 178;
        attribute linkedRequirementCount : Integer = 17;
        doc /* block=Pad Mux | description=Route source-specified functional, scan, BIST, debug, and ISPU-debug signals to and from device pads. */;
        in port i_write_protection_en : ArchitecturePort {
            attribute sourceName = "i_write_protection_en";
            attribute sourceDetails = "write_protection_en OTP regmap enable from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        out port o_write_protection_en : ArchitecturePort {
            attribute sourceName = "o_write_protection_en";
            attribute sourceDetails = "write_protection_en OTP regmap enable to regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port i_tap_bist_mode : ArchitecturePort {
            attribute sourceName = "i_tap_bist_mode";
            attribute sourceDetails = "bist_mode signal used retun in functional mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port i_EN_0P05HP_ECG0 : ArchitecturePort {
            attribute sourceName = "i_EN_0P05HP_ECG0";
            attribute sourceDetails = "bit enable select PDRES 05 ECG0 channel";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port i_EN_0P05HP_ECG12 : ArchitecturePort {
            attribute sourceName = "i_EN_0P05HP_ECG12";
            attribute sourceDetails = "bit enable select PDRES 05 ECG12 channel";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port IMPQ_PSDRES_UP_02 : ArchitecturePort {
            attribute sourceName = "IMPQ_PSDRES_UP_02";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port IMPQ_PSDRES_DOWN_02 : ArchitecturePort {
            attribute sourceName = "IMPQ_PSDRES_DOWN_02";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port IMPP_PSDRES_UP_02 : ArchitecturePort {
            attribute sourceName = "IMPP_PSDRES_UP_02";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port IMPP_PSDRES_DOWN_02 : ArchitecturePort {
            attribute sourceName = "IMPP_PSDRES_DOWN_02";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port ECG_PSDRES_DOWN_02 : ArchitecturePort {
            attribute sourceName = "ECG_PSDRES_DOWN_02";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port ECG_PSDRES_UP_02 : ArchitecturePort {
            attribute sourceName = "ECG_PSDRES_UP_02";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port IMPQ_PSDRES_UP_05 : ArchitecturePort {
            attribute sourceName = "IMPQ_PSDRES_UP_05";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port IMPQ_PSDRES_DOWN_05 : ArchitecturePort {
            attribute sourceName = "IMPQ_PSDRES_DOWN_05";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port IMPP_PSDRES_UP_05 : ArchitecturePort {
            attribute sourceName = "IMPP_PSDRES_UP_05";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port IMPP_PSDRES_DOWN_05 : ArchitecturePort {
            attribute sourceName = "IMPP_PSDRES_DOWN_05";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port ECG_PSDRES_DOWN_05 : ArchitecturePort {
            attribute sourceName = "ECG_PSDRES_DOWN_05";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        in port ECG_PSDRES_UP_05 : ArchitecturePort {
            attribute sourceName = "ECG_PSDRES_UP_05";
            attribute sourceDetails = "[2:0] OTP value for Analog block 49";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "49";
        }
        out port IMPQ_PSDRES_UP : ArchitecturePort {
            attribute sourceName = "IMPQ_PSDRES_UP";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        out port IMPQ_PSDRES_DOWN : ArchitecturePort {
            attribute sourceName = "IMPQ_PSDRES_DOWN";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        out port IMPP_PSDRES_UP : ArchitecturePort {
            attribute sourceName = "IMPP_PSDRES_UP";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        out port IMPP_PSDRES_DOWN : ArchitecturePort {
            attribute sourceName = "IMPP_PSDRES_DOWN";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        out port ECG_PSDRES_DOWN : ArchitecturePort {
            attribute sourceName = "ECG_PSDRES_DOWN";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        out port ECG_PSDRES_UP : ArchitecturePort {
            attribute sourceName = "ECG_PSDRES_UP";
            attribute sourceDetails = "[2:0] OTP value for Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port i_TS_IRQ_ST : ArchitecturePort {
            attribute sourceName = "i_TS_IRQ_ST";
            attribute sourceDetails = "time slot irq";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port i_DCCK_IRQ_ST : ArchitecturePort {
            attribute sourceName = "i_DCCK_IRQ_ST";
            attribute sourceDetails = "DCCK irq change status";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port o_en_tx_1V2 : ArchitecturePort {
            attribute sourceName = "o_en_tx_1V2";
            attribute sourceDetails = "input to LED pilot";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port o_tx_preset_1V2 : ArchitecturePort {
            attribute sourceName = "o_tx_preset_1V2";
            attribute sourceDetails = "input to LED pilot";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port o_tx1_outlab_sel_frame_x_1V2 : ArchitecturePort {
            attribute sourceName = "o_tx1_outlab_sel_frame_x_1V2";
            attribute sourceDetails = "input to LED pilot";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port sel_irq_gpio1 : ArchitecturePort {
            attribute sourceName = "sel_irq_gpio1";
            attribute sourceDetails = "[3:0] sel irq gpi1 {000:NC, 001:i_fifo_irq, 010:i_LED_Pilot, 011:i_DCCK_irq, 100:i_error_time_slot, 101:i_time_slot_irq}";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port sel_irq_gpio2 : ArchitecturePort {
            attribute sourceName = "sel_irq_gpio2";
            attribute sourceDetails = "[3:0] sel irq gpi2 {000:NC, 001:i_fifo_irq, 010:i_LED_Pilot, 011:i_DCCK_irq, 100:i_error_time_slot, 101:i_time_slot_irq}";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port sel_irq_gpio3 : ArchitecturePort {
            attribute sourceName = "sel_irq_gpio3";
            attribute sourceDetails = "[3:0] sel irq gpi3 {000:NC, 001:i_fifo_irq, 010:i_LED_Pilot, 011:i_DCCK_irq, 100:i_error_time_slot, 101:i_time_slot_irq}";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port sel_irq_gpio4 : ArchitecturePort {
            attribute sourceName = "sel_irq_gpio4";
            attribute sourceDetails = "[3:0] sel irq gpi4 {000:NC, 001:i_fifo_irq, 010:i_LED_Pilot, 011:i_DCCK_irq, 100:i_error_time_slot, 101:i_time_slot_irq}";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port DCCK_P_en : ArchitecturePort {
            attribute sourceName = "DCCK_P_en";
            attribute sourceDetails = "Manages lead off mode DCCK_P, Source: Regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port DCCK_N_en : ArchitecturePort {
            attribute sourceName = "DCCK_N_en";
            attribute sourceDetails = "Manages lead off mode DCCK_P, Source: Regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        in port MODE_OPERATION : ArchitecturePort {
            attribute sourceName = "MODE_OPERATION";
            attribute sourceDetails = "Start Divice operations status 50";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "50";
        }
        out port o_pd_p : ArchitecturePort {
            attribute sourceName = "o_pd_p";
            attribute sourceDetails = "enable lead off mode DCCK_P, Destination:Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        out port o_pd_n : ArchitecturePort {
            attribute sourceName = "o_pd_n";
            attribute sourceDetails = "enable lead off mode DCCK_N, Destination:Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port O_DCCK_P_i : ArchitecturePort {
            attribute sourceName = "O_DCCK_P_i";
            attribute sourceDetails = "status lead off mode DCCK_P {0:low impedance,1:floating electrode}, Source: Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port O_DCCK_N_i : ArchitecturePort {
            attribute sourceName = "O_DCCK_N_i";
            attribute sourceDetails = "status lead off mode DCCK_N {0:low impedance,1:floating electrode}, Source: Analog block";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        out port if_gpio1_in_reg : ArchitecturePort {
            attribute sourceName = "if_gpio1_in_reg";
            attribute sourceDetails = "ZI value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port if_gpio1_en_reg : ArchitecturePort {
            attribute sourceName = "if_gpio1_en_reg";
            attribute sourceDetails = "EN value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port if_gpio1_out_reg : ArchitecturePort {
            attribute sourceName = "if_gpio1_out_reg";
            attribute sourceDetails = "OUT value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        out port if_gpio2_in_reg : ArchitecturePort {
            attribute sourceName = "if_gpio2_in_reg";
            attribute sourceDetails = "ZI value from regmap// ZI";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port if_gpio2_en_reg : ArchitecturePort {
            attribute sourceName = "if_gpio2_en_reg";
            attribute sourceDetails = "EN value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port if_gpio2_out_reg : ArchitecturePort {
            attribute sourceName = "if_gpio2_out_reg";
            attribute sourceDetails = "OUT value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        out port if_gpio3_in_reg : ArchitecturePort {
            attribute sourceName = "if_gpio3_in_reg";
            attribute sourceDetails = "ZI value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port if_gpio3_en_reg : ArchitecturePort {
            attribute sourceName = "if_gpio3_en_reg";
            attribute sourceDetails = "EN value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port if_gpio3_out_reg : ArchitecturePort {
            attribute sourceName = "if_gpio3_out_reg";
            attribute sourceDetails = "OUT value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        out port if_gpio4_in_reg : ArchitecturePort {
            attribute sourceName = "if_gpio4_in_reg";
            attribute sourceDetails = "ZI value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port if_gpio4_en_reg : ArchitecturePort {
            attribute sourceName = "if_gpio4_en_reg";
            attribute sourceDetails = "EN value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port if_gpio4_out_reg : ArchitecturePort {
            attribute sourceName = "if_gpio4_out_reg";
            attribute sourceDetails = "OUT value from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port o_ext_reg_dt_afe : ArchitecturePort {
            attribute sourceName = "o_ext_reg_dt_afe";
            attribute sourceDetails = "[7:0] i2c/spi read data u_regmap_otp";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        out port o_ext_reg_dt : ArchitecturePort {
            attribute sourceName = "o_ext_reg_dt";
            attribute sourceDetails = "[7:0] i2c/spi read data output";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port i_ext_reg_add : ArchitecturePort {
            attribute sourceName = "i_ext_reg_add";
            attribute sourceDetails = "[7:0] i2c/spi address";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port i_ext_reg_dt : ArchitecturePort {
            attribute sourceName = "i_ext_reg_dt";
            attribute sourceDetails = "[7:0] i2c/spi write data";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port i_ext_reg_ck_wr : ArchitecturePort {
            attribute sourceName = "i_ext_reg_ck_wr";
            attribute sourceDetails = "i2c/spi clk 51";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "51";
        }
        in port i_ext_reg_we : ArchitecturePort {
            attribute sourceName = "i_ext_reg_we";
            attribute sourceDetails = "i2c/spi regmap direct write enable";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        in port if_sclk_in : ArchitecturePort {
            attribute sourceName = "if_sclk_in";
            attribute sourceDetails = "ZI_I2C";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        in port if_sclk_i3c_in : ArchitecturePort {
            attribute sourceName = "if_sclk_i3c_in";
            attribute sourceDetails = "ZI_I3C";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_sclk_out : ArchitecturePort {
            attribute sourceName = "if_sclk_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_sclk_en : ArchitecturePort {
            attribute sourceName = "if_sclk_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_sclk_tud : ArchitecturePort {
            attribute sourceName = "if_sclk_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        in port if_sda_sdi_in : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_in";
            attribute sourceDetails = "ZI_I2C";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        in port if_sda_sdi_i3c_in : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_i3c_in";
            attribute sourceDetails = "ZI_I3C";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_sda_sdi_out : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_sda_sdi_en : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_sda_sdi_tud : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        in port if_cs_in : ArchitecturePort {
            attribute sourceName = "if_cs_in";
            attribute sourceDetails = "ZI CS";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_cs_out : ArchitecturePort {
            attribute sourceName = "if_cs_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_cs_en : ArchitecturePort {
            attribute sourceName = "if_cs_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_cs_tud : ArchitecturePort {
            attribute sourceName = "if_cs_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        in port if_gpio0_in : ArchitecturePort {
            attribute sourceName = "if_gpio0_in";
            attribute sourceDetails = "ZI GPIO0";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_gpio0_out : ArchitecturePort {
            attribute sourceName = "if_gpio0_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_gpio0_en : ArchitecturePort {
            attribute sourceName = "if_gpio0_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_gpio0_tud : ArchitecturePort {
            attribute sourceName = "if_gpio0_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        in port if_gpio1_in : ArchitecturePort {
            attribute sourceName = "if_gpio1_in";
            attribute sourceDetails = "ZI GPIO1";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_gpio1_out : ArchitecturePort {
            attribute sourceName = "if_gpio1_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_gpio1_en : ArchitecturePort {
            attribute sourceName = "if_gpio1_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_gpio1_tud : ArchitecturePort {
            attribute sourceName = "if_gpio1_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        in port if_gpio2_in : ArchitecturePort {
            attribute sourceName = "if_gpio2_in";
            attribute sourceDetails = "ZI GPIO2 52";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "52";
        }
        out port if_gpio2_out : ArchitecturePort {
            attribute sourceName = "if_gpio2_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_gpio2_en : ArchitecturePort {
            attribute sourceName = "if_gpio2_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_gpio2_tud : ArchitecturePort {
            attribute sourceName = "if_gpio2_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        in port if_gpio3_in : ArchitecturePort {
            attribute sourceName = "if_gpio3_in";
            attribute sourceDetails = "ZI GPIO3";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_gpio3_out : ArchitecturePort {
            attribute sourceName = "if_gpio3_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_gpio3_en : ArchitecturePort {
            attribute sourceName = "if_gpio3_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_gpio3_tud : ArchitecturePort {
            attribute sourceName = "if_gpio3_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        in port if_gpio4_in : ArchitecturePort {
            attribute sourceName = "if_gpio4_in";
            attribute sourceDetails = "ZI GPIO4";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_gpio4_out : ArchitecturePort {
            attribute sourceName = "if_gpio4_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_gpio4_en : ArchitecturePort {
            attribute sourceName = "if_gpio4_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_gpio4_tud : ArchitecturePort {
            attribute sourceName = "if_gpio4_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        in port if_sh_ck_in : ArchitecturePort {
            attribute sourceName = "if_sh_ck_in";
            attribute sourceDetails = "ZI sensor hub ck";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_sh_ck_out : ArchitecturePort {
            attribute sourceName = "if_sh_ck_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_sh_ck_en : ArchitecturePort {
            attribute sourceName = "if_sh_ck_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_sh_ck_tud : ArchitecturePort {
            attribute sourceName = "if_sh_ck_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        in port if_sh_sda_in : ArchitecturePort {
            attribute sourceName = "if_sh_sda_in";
            attribute sourceDetails = "ZI sensor hub SDA";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_sh_sda_out : ArchitecturePort {
            attribute sourceName = "if_sh_sda_out";
            attribute sourceDetails = "A";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_sh_sda_en : ArchitecturePort {
            attribute sourceName = "if_sh_sda_en";
            attribute sourceDetails = "EN";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port if_sh_sda_tud : ArchitecturePort {
            attribute sourceName = "if_sh_sda_tud";
            attribute sourceDetails = "TUD";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        in port POR1V2_1V2 : ArchitecturePort {
            attribute sourceName = "POR1V2_1V2";
            attribute sourceDetails = "POR";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port ispu_tck : ArchitecturePort {
            attribute sourceName = "ispu_tck";
            attribute sourceDetails = "jtag clk port ispu in ispu debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port ispu_tdi : ArchitecturePort {
            attribute sourceName = "ispu_tdi";
            attribute sourceDetails = "jtag data in port ispu in ispu debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        in port ispu_tdo : ArchitecturePort {
            attribute sourceName = "ispu_tdo";
            attribute sourceDetails = "jtag data out port ispu in ispu debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        in port ispu_tdo_en : ArchitecturePort {
            attribute sourceName = "ispu_tdo_en";
            attribute sourceDetails = "jtag en port ispu in ispu debug mode 53";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "53";
        }
        out port ispu_tms : ArchitecturePort {
            attribute sourceName = "ispu_tms";
            attribute sourceDetails = "jtag state in port ispu in ispu debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port ispu_trst_n : ArchitecturePort {
            attribute sourceName = "ispu_trst_n";
            attribute sourceDetails = "jtag reset in port ispu in ispu debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port i_if_ck : ArchitecturePort {
            attribute sourceName = "i_if_ck";
            attribute sourceDetails = "i2c/spi clk";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port i_if_cs : ArchitecturePort {
            attribute sourceName = "i_if_cs";
            attribute sourceDetails = "i2c/spi cs";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port i_if_sda_sdi_in : ArchitecturePort {
            attribute sourceName = "i_if_sda_sdi_in";
            attribute sourceDetails = "i2c/spi data";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port o_if_cs_en_n : ArchitecturePort {
            attribute sourceName = "o_if_cs_en_n";
            attribute sourceDetails = "i2c/spi cs en from i2c/spi ip";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port o_if_cs_out_n : ArchitecturePort {
            attribute sourceName = "o_if_cs_out_n";
            attribute sourceDetails = "i2c/spi cs out from i2c/spi ip";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port o_if_cs_tud : ArchitecturePort {
            attribute sourceName = "o_if_cs_tud";
            attribute sourceDetails = "i2c/spi cs tud from i2c/spi ip";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port o_if_sda_sdi_en_n : ArchitecturePort {
            attribute sourceName = "o_if_sda_sdi_en_n";
            attribute sourceDetails = "i2c/spi data en from i2c/spi ip";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port o_if_sda_sdi_out : ArchitecturePort {
            attribute sourceName = "o_if_sda_sdi_out";
            attribute sourceDetails = "i2c/spi data out from i2c/spi ip";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port scl_master_in : ArchitecturePort {
            attribute sourceName = "scl_master_in";
            attribute sourceDetails = "from sensorhub";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port scl_master_out : ArchitecturePort {
            attribute sourceName = "scl_master_out";
            attribute sourceDetails = "from sensorhub";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port sda_master_in : ArchitecturePort {
            attribute sourceName = "sda_master_in";
            attribute sourceDetails = "to sensorhub";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port sda_master_out : ArchitecturePort {
            attribute sourceName = "sda_master_out";
            attribute sourceDetails = "from sensorhub";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port afe_bist_ctrl_tdi : ArchitecturePort {
            attribute sourceName = "afe_bist_ctrl_tdi";
            attribute sourceDetails = "bist jtag port";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port afe_bist_ctrl_trstn : ArchitecturePort {
            attribute sourceName = "afe_bist_ctrl_trstn";
            attribute sourceDetails = "bist jtag port";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port afe_bist_ctrl_tms : ArchitecturePort {
            attribute sourceName = "afe_bist_ctrl_tms";
            attribute sourceDetails = "bist jtag port";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port afe_bist_ctrl_tdo : ArchitecturePort {
            attribute sourceName = "afe_bist_ctrl_tdo";
            attribute sourceDetails = "bist jtag port";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port afe_bist_ctrl_tdo_en_n : ArchitecturePort {
            attribute sourceName = "afe_bist_ctrl_tdo_en_n";
            attribute sourceDetails = "bist jtag port";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port afe_bist_ctrl_tck : ArchitecturePort {
            attribute sourceName = "afe_bist_ctrl_tck";
            attribute sourceDetails = "bist jtag port";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port ck_16m : ArchitecturePort {
            attribute sourceName = "ck_16m";
            attribute sourceDetails = "clk16MHz trimming in debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port ck_2m : ArchitecturePort {
            attribute sourceName = "ck_2m";
            attribute sourceDetails = "clk2MHz trimming in debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        in port ck_64k : ArchitecturePort {
            attribute sourceName = "ck_64k";
            attribute sourceDetails = "clk64MHz trimming in debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port scan_rstn : ArchitecturePort {
            attribute sourceName = "scan_rstn";
            attribute sourceDetails = "scan reset 54";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "54";
        }
        out port scan_enable : ArchitecturePort {
            attribute sourceName = "scan_enable";
            attribute sourceDetails = "scan enable";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        out port scan_clk : ArchitecturePort {
            attribute sourceName = "scan_clk";
            attribute sourceDetails = "scan clock";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port ext_cap_en : ArchitecturePort {
            attribute sourceName = "ext_cap_en";
            attribute sourceDetails = "extenal cap in debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port irq_fifo : ArchitecturePort {
            attribute sourceName = "irq_fifo";
            attribute sourceDetails = "fifo irq from main controller - regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port error_time_slot : ArchitecturePort {
            attribute sourceName = "error_time_slot";
            attribute sourceDetails = "error timeslot from error time slot";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        out port gpio_in : ArchitecturePort {
            attribute sourceName = "gpio_in";
            attribute sourceDetails = "gpio0 in in functional mode from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port gpio_out : ArchitecturePort {
            attribute sourceName = "gpio_out";
            attribute sourceDetails = "gpio0 out in functional mode from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port gpio_en : ArchitecturePort {
            attribute sourceName = "gpio_en";
            attribute sourceDetails = "gpio0 en in functional mode from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port irq_SENSHUB_STS : ArchitecturePort {
            attribute sourceName = "irq_SENSHUB_STS";
            attribute sourceDetails = "sensorhub status";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port irq_ISPU_MC_INTR_STS : ArchitecturePort {
            attribute sourceName = "irq_ISPU_MC_INTR_STS";
            attribute sourceDetails = "irq main controller data-valid";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        out port scan_mode : ArchitecturePort {
            attribute sourceName = "scan_mode";
            attribute sourceDetails = "stbio1 scan mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        out port bist_mode : ArchitecturePort {
            attribute sourceName = "bist_mode";
            attribute sourceDetails = "stbio1 bist mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        out port debug_mode : ArchitecturePort {
            attribute sourceName = "debug_mode";
            attribute sourceDetails = "stbio1 debug mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        out port memsafe : ArchitecturePort {
            attribute sourceName = "memsafe";
            attribute sourceDetails = "memsafe for bist";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port test_clk_fast : ArchitecturePort {
            attribute sourceName = "test_clk_fast";
            attribute sourceDetails = "enable test clk 16MHz trimming";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port test_clk_slow : ArchitecturePort {
            attribute sourceName = "test_clk_slow";
            attribute sourceDetails = "enable test clk 64kHz trimming";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port if_sclk_tud_reg : ArchitecturePort {
            attribute sourceName = "if_sclk_tud_reg";
            attribute sourceDetails = "if sclk_tud from reg";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port if_sda_sdi_tud_reg : ArchitecturePort {
            attribute sourceName = "if_sda_sdi_tud_reg";
            attribute sourceDetails = "if sda_sdi_tud from re";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port if_sh_sda_tud_reg : ArchitecturePort {
            attribute sourceName = "if_sh_sda_tud_reg";
            attribute sourceDetails = "if sh_sda_tud from reg";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port if_gpio0_tud_reg : ArchitecturePort {
            attribute sourceName = "if_gpio0_tud_reg";
            attribute sourceDetails = "if gpio0_tud from reg";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port if_gpio1_tud_reg : ArchitecturePort {
            attribute sourceName = "if_gpio1_tud_reg";
            attribute sourceDetails = "if gpio1_tud from reg";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port if_gpio2_tud_reg : ArchitecturePort {
            attribute sourceName = "if_gpio2_tud_reg";
            attribute sourceDetails = "if gpio2_tud from reg";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port if_gpio3_tud_reg : ArchitecturePort {
            attribute sourceName = "if_gpio3_tud_reg";
            attribute sourceDetails = "if gpio3_tud from reg 55";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "55";
        }
        in port if_gpio4_tud_reg : ArchitecturePort {
            attribute sourceName = "if_gpio4_tud_reg";
            attribute sourceDetails = "if gpio4_tud from reg";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port if_sh_ck_tud_reg : ArchitecturePort {
            attribute sourceName = "if_sh_ck_tud_reg";
            attribute sourceDetails = "if sh_ck_tud from reg";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port clk_dft_adc : ArchitecturePort {
            attribute sourceName = "clk_dft_adc";
            attribute sourceDetails = "16MHz adc dft clk";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_ADC_clk_serial_dft : ArchitecturePort {
            attribute sourceName = "i_ADC_clk_serial_dft";
            attribute sourceDetails = "serial clk for adc dft 16Mhz:Fast mode, if_sh_ck_in:Low noise mode";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port EN_ADC_TEST_FAST : ArchitecturePort {
            attribute sourceName = "EN_ADC_TEST_FAST";
            attribute sourceDetails = "enable adc test fast";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port EN_ADC_TEST_LOW_NOISE : ArchitecturePort {
            attribute sourceName = "EN_ADC_TEST_LOW_NOISE";
            attribute sourceDetails = "enable adc test low noise";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_ADC_EOC : ArchitecturePort {
            attribute sourceName = "i_ADC_EOC";
            attribute sourceDetails = "adc eoc input";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_ADC_start : ArchitecturePort {
            attribute sourceName = "i_ADC_start";
            attribute sourceDetails = "adc star from main controller";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_data_ADC_out : ArchitecturePort {
            attribute sourceName = "i_data_ADC_out";
            attribute sourceDetails = "[15:0] adc data input";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        out port o_ADC_start : ArchitecturePort {
            attribute sourceName = "o_ADC_start";
            attribute sourceDetails = "adc star output";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_N_clk : ArchitecturePort {
            attribute sourceName = "i_N_clk";
            attribute sourceDetails = "[6- 1:0] n clk start time high";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_saturation_irq : ArchitecturePort {
            attribute sourceName = "i_saturation_irq";
            attribute sourceDetails = "interrupt saturation from main controller";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_end_boot : ArchitecturePort {
            attribute sourceName = "i_end_boot";
            attribute sourceDetails = "end boot signal from adsp";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port quokka_run : ArchitecturePort {
            attribute sourceName = "quokka_run";
            attribute sourceDetails = "status quokka elaboration 1:run 0:not elaboration";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port sensor_hub_status : ArchitecturePort {
            attribute sourceName = "sensor_hub_status";
            attribute sourceDetails = "status sensor_hob from regmap";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port SH_CKL_EN : ArchitecturePort {
            attribute sourceName = "SH_CKL_EN";
            attribute sourceDetails = "sensorhub clk enable from regmap (master_end_op_clr or sleep_master_clr or ahb_master_on_clr)";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_t_force_1v2 : ArchitecturePort {
            attribute sourceName = "i_t_force_1v2";
            attribute sourceDetails = "input force signal to IDDQ test";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        out port o_t_force_1v2 : ArchitecturePort {
            attribute sourceName = "o_t_force_1v2";
            attribute sourceDetails = "force signal to IDDQ test";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_bfail_fifo : ArchitecturePort {
            attribute sourceName = "i_bfail_fifo";
            attribute sourceDetails = "bist fail fifo ram";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_bfail_qk : ArchitecturePort {
            attribute sourceName = "i_bfail_qk";
            attribute sourceDetails = "bist fail adsp ram";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_bfail_ispu1 : ArchitecturePort {
            attribute sourceName = "i_bfail_ispu1";
            attribute sourceDetails = "bist fail ispu ram instruction mem";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_bfail_ispu2 : ArchitecturePort {
            attribute sourceName = "i_bfail_ispu2";
            attribute sourceDetails = "bist fail ispu ram data mem 1 56";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "56";
        }
        in port i_bfail_ispu3 : ArchitecturePort {
            attribute sourceName = "i_bfail_ispu3";
            attribute sourceDetails = "bist fail ispu ram data mem 2";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "57";
        }
        in port i_bfail_ispu4 : ArchitecturePort {
            attribute sourceName = "i_bfail_ispu4";
            attribute sourceDetails = "bist fail ispu ram data mem 3";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "57";
        }
        in port i_bend : ArchitecturePort {
            attribute sourceName = "i_bend";
            attribute sourceDetails = "bist end signal";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "57";
        }
        in port i_bbad : ArchitecturePort {
            attribute sourceName = "i_bbad";
            attribute sourceDetails = "signal fail bist test";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "57";
        }
        out port o_bypass : ArchitecturePort {
            attribute sourceName = "o_bypass";
            attribute sourceDetails = "bypass memory signal";
            attribute sourceTable = "PAD MUX I/O List";
            attribute sourcePage = "57";
        }

        requirement def IPOS_PAD_MUX_001 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_302";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-001";
            doc /* [DDS_STBIO1_302] Requirement If MODE_CONFIG register is 0x00 the operative mode shall be functional. */;
        }
        requirement req_IPOS_PAD_MUX_001 : IPOS_PAD_MUX_001;
        doc /* iposReqId=IPOS-PAD-MUX-001 | sourceReqId=DDS_STBIO1_302 | [DDS_STBIO1_302] Requirement If MODE_CONFIG register is 0x00 the operative mode shall be functional. */;
        doc /* coverageDependency: IPOS-PAD-MUX-001 -> approved source requirement DDS_STBIO1_302 */;
        satisfy req_IPOS_PAD_MUX_001 by self;
        requirement def IPOS_PAD_MUX_002 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_303";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-002";
            doc /* [DDS_STBIO1_303] Requirement If MODE_CONFIG register is 0x01 the operative mode shall be SCAN. */;
        }
        requirement req_IPOS_PAD_MUX_002 : IPOS_PAD_MUX_002;
        doc /* iposReqId=IPOS-PAD-MUX-002 | sourceReqId=DDS_STBIO1_303 | [DDS_STBIO1_303] Requirement If MODE_CONFIG register is 0x01 the operative mode shall be SCAN. */;
        doc /* coverageDependency: IPOS-PAD-MUX-002 -> approved source requirement DDS_STBIO1_303 */;
        satisfy req_IPOS_PAD_MUX_002 by self;
        requirement def IPOS_PAD_MUX_003 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_304";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-003";
            doc /* [DDS_STBIO1_304] Requirement If MODE_CONFIG register is 0x04 the operative mode shall be BIST. */;
        }
        requirement req_IPOS_PAD_MUX_003 : IPOS_PAD_MUX_003;
        doc /* iposReqId=IPOS-PAD-MUX-003 | sourceReqId=DDS_STBIO1_304 | [DDS_STBIO1_304] Requirement If MODE_CONFIG register is 0x04 the operative mode shall be BIST. */;
        doc /* coverageDependency: IPOS-PAD-MUX-003 -> approved source requirement DDS_STBIO1_304 */;
        satisfy req_IPOS_PAD_MUX_003 by self;
        requirement def IPOS_PAD_MUX_004 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_305";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-004";
            doc /* [DDS_STBIO1_305] Requirement If MODE_CONFIG register is 0x08 the operative mode shall be DEBUG. */;
        }
        requirement req_IPOS_PAD_MUX_004 : IPOS_PAD_MUX_004;
        doc /* iposReqId=IPOS-PAD-MUX-004 | sourceReqId=DDS_STBIO1_305 | [DDS_STBIO1_305] Requirement If MODE_CONFIG register is 0x08 the operative mode shall be DEBUG. */;
        doc /* coverageDependency: IPOS-PAD-MUX-004 -> approved source requirement DDS_STBIO1_305 */;
        satisfy req_IPOS_PAD_MUX_004 by self;
        requirement def IPOS_PAD_MUX_005 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_306";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-005";
            doc /* [DDS_STBIO1_306] Requirement If MODE_CONFIG register is 0x10 the operative mode shall be ISPU_DEBUG. */;
        }
        requirement req_IPOS_PAD_MUX_005 : IPOS_PAD_MUX_005;
        doc /* iposReqId=IPOS-PAD-MUX-005 | sourceReqId=DDS_STBIO1_306 | [DDS_STBIO1_306] Requirement If MODE_CONFIG register is 0x10 the operative mode shall be ISPU_DEBUG. */;
        doc /* coverageDependency: IPOS-PAD-MUX-005 -> approved source requirement DDS_STBIO1_306 */;
        satisfy req_IPOS_PAD_MUX_005 by self;
        requirement def IPOS_PAD_MUX_006 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_307";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-006";
            doc /* [DDS_STBIO1_307] Requirement If MODE_CONFIG register is 0x20 the operative mode shall be Bist MEMSAFE mode. */;
        }
        requirement req_IPOS_PAD_MUX_006 : IPOS_PAD_MUX_006;
        doc /* iposReqId=IPOS-PAD-MUX-006 | sourceReqId=DDS_STBIO1_307 | [DDS_STBIO1_307] Requirement If MODE_CONFIG register is 0x20 the operative mode shall be Bist MEMSAFE mode. */;
        doc /* coverageDependency: IPOS-PAD-MUX-006 -> approved source requirement DDS_STBIO1_307 */;
        satisfy req_IPOS_PAD_MUX_006 by self;
        requirement def IPOS_PAD_MUX_007 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_308";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-007";
            doc /* [DDS_STBIO1_308] Requirement If MODE_CONFIG register is 0x40 the operative mode shall be Bist Bypass mode. */;
        }
        requirement req_IPOS_PAD_MUX_007 : IPOS_PAD_MUX_007;
        doc /* iposReqId=IPOS-PAD-MUX-007 | sourceReqId=DDS_STBIO1_308 | [DDS_STBIO1_308] Requirement If MODE_CONFIG register is 0x40 the operative mode shall be Bist Bypass mode. */;
        doc /* coverageDependency: IPOS-PAD-MUX-007 -> approved source requirement DDS_STBIO1_308 */;
        satisfy req_IPOS_PAD_MUX_007 by self;
        requirement def IPOS_PAD_MUX_008 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_309";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-008";
            doc /* In function mode, the GPIO1,2,3,4_out shall be irq_fifo if sel irq gpio1,2,3,4 is 0x01 and ext_cap_en is “0” [Vpriority High] */;
        }
        requirement req_IPOS_PAD_MUX_008 : IPOS_PAD_MUX_008;
        doc /* iposReqId=IPOS-PAD-MUX-008 | sourceReqId=DDS_STBIO1_309 | In function mode, the GPIO1,2,3,4_out shall be irq_fifo if sel irq gpio1,2,3,4 is 0x01 and ext_cap_en is “0” [Vpriority High] */;
        doc /* coverageDependency: IPOS-PAD-MUX-008 -> approved source requirement DDS_STBIO1_309 */;
        satisfy req_IPOS_PAD_MUX_008 by self;
        requirement def IPOS_PAD_MUX_009 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_310";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-009";
            doc /* In function mode, the GPIO1,2,3,4_out shall be i_LED_Pilot if sel irq gpi1,2,3,4 is 0x02 and ext_cap_en is “0” [Vpriority High] */;
        }
        requirement req_IPOS_PAD_MUX_009 : IPOS_PAD_MUX_009;
        doc /* iposReqId=IPOS-PAD-MUX-009 | sourceReqId=DDS_STBIO1_310 | In function mode, the GPIO1,2,3,4_out shall be i_LED_Pilot if sel irq gpi1,2,3,4 is 0x02 and ext_cap_en is “0” [Vpriority High] */;
        doc /* coverageDependency: IPOS-PAD-MUX-009 -> approved source requirement DDS_STBIO1_310 */;
        satisfy req_IPOS_PAD_MUX_009 by self;
        requirement def IPOS_PAD_MUX_010 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_311";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-010";
            doc /* In function mode, the GPIO1,2,3,4_out shall be i_DCCK_irq if sel irq gpi1,2,3,4 is 0x03 and ext_cap_en is “0” [Vpriority High] */;
        }
        requirement req_IPOS_PAD_MUX_010 : IPOS_PAD_MUX_010;
        doc /* iposReqId=IPOS-PAD-MUX-010 | sourceReqId=DDS_STBIO1_311 | In function mode, the GPIO1,2,3,4_out shall be i_DCCK_irq if sel irq gpi1,2,3,4 is 0x03 and ext_cap_en is “0” [Vpriority High] */;
        doc /* coverageDependency: IPOS-PAD-MUX-010 -> approved source requirement DDS_STBIO1_311 */;
        satisfy req_IPOS_PAD_MUX_010 by self;
        requirement def IPOS_PAD_MUX_011 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_312";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-011";
            doc /* In function mode, the GPIO1,2,3,4 output shall be i_error_time_slot if sel irq gpi1,2,3,4 is 0x04 and ext_cap_en is “0” [Vpriority High] */;
        }
        requirement req_IPOS_PAD_MUX_011 : IPOS_PAD_MUX_011;
        doc /* iposReqId=IPOS-PAD-MUX-011 | sourceReqId=DDS_STBIO1_312 | In function mode, the GPIO1,2,3,4 output shall be i_error_time_slot if sel irq gpi1,2,3,4 is 0x04 and ext_cap_en is “0” [Vpriority High] */;
        doc /* coverageDependency: IPOS-PAD-MUX-011 -> approved source requirement DDS_STBIO1_312 */;
        satisfy req_IPOS_PAD_MUX_011 by self;
        requirement def IPOS_PAD_MUX_012 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_313";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-012";
            doc /* In function mode, the GPIO1,2,3,4 output shall be i_time_slot_irq if sel irq gpi1,2,3,4 is 0x05 and ext_cap_en is “0” [Vpriority High] */;
        }
        requirement req_IPOS_PAD_MUX_012 : IPOS_PAD_MUX_012;
        doc /* iposReqId=IPOS-PAD-MUX-012 | sourceReqId=DDS_STBIO1_313 | In function mode, the GPIO1,2,3,4 output shall be i_time_slot_irq if sel irq gpi1,2,3,4 is 0x05 and ext_cap_en is “0” [Vpriority High] */;
        doc /* coverageDependency: IPOS-PAD-MUX-012 -> approved source requirement DDS_STBIO1_313 */;
        satisfy req_IPOS_PAD_MUX_012 by self;
        requirement def IPOS_PAD_MUX_013 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_314";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-013";
            doc /* In function mode, the GPIO1,2,3,4_out shall be General-Purpose if sel irq gpi1,2,3,4 is 0x00 and ext_cap_en is “0” [Vpriority High] */;
        }
        requirement req_IPOS_PAD_MUX_013 : IPOS_PAD_MUX_013;
        doc /* iposReqId=IPOS-PAD-MUX-013 | sourceReqId=DDS_STBIO1_314 | In function mode, the GPIO1,2,3,4_out shall be General-Purpose if sel irq gpi1,2,3,4 is 0x00 and ext_cap_en is “0” [Vpriority High] */;
        doc /* coverageDependency: IPOS-PAD-MUX-013 -> approved source requirement DDS_STBIO1_314 */;
        satisfy req_IPOS_PAD_MUX_013 by self;
        requirement def IPOS_PAD_MUX_014 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_392";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-014";
            doc /* If O_DCCK_P_i changes its value from '0' to '1' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp, shall be set to '1' */;
        }
        requirement req_IPOS_PAD_MUX_014 : IPOS_PAD_MUX_014;
        doc /* iposReqId=IPOS-PAD-MUX-014 | sourceReqId=DDS_STBIO1_392 | If O_DCCK_P_i changes its value from '0' to '1' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp, shall be set to '1' */;
        doc /* coverageDependency: IPOS-PAD-MUX-014 -> approved source requirement DDS_STBIO1_392 */;
        satisfy req_IPOS_PAD_MUX_014 by self;
        requirement def IPOS_PAD_MUX_015 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_393";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-015";
            doc /* If O_DCCK_N_i changes its value from '0' to '1' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp, shall be set to '1' */;
        }
        requirement req_IPOS_PAD_MUX_015 : IPOS_PAD_MUX_015;
        doc /* iposReqId=IPOS-PAD-MUX-015 | sourceReqId=DDS_STBIO1_393 | If O_DCCK_N_i changes its value from '0' to '1' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp, shall be set to '1' */;
        doc /* coverageDependency: IPOS-PAD-MUX-015 -> approved source requirement DDS_STBIO1_393 */;
        satisfy req_IPOS_PAD_MUX_015 by self;
        requirement def IPOS_PAD_MUX_016 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_394";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-016";
            doc /* If O_DCCK_P_i changes its value from '1' to '0' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp, shall be set to '1' */;
        }
        requirement req_IPOS_PAD_MUX_016 : IPOS_PAD_MUX_016;
        doc /* iposReqId=IPOS-PAD-MUX-016 | sourceReqId=DDS_STBIO1_394 | If O_DCCK_P_i changes its value from '1' to '0' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp, shall be set to '1' */;
        doc /* coverageDependency: IPOS-PAD-MUX-016 -> approved source requirement DDS_STBIO1_394 */;
        satisfy req_IPOS_PAD_MUX_016 by self;
        requirement def IPOS_PAD_MUX_017 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_395";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-PAD-MUX-017";
            doc /* The DCC feature consists of two stages that detect whether one of six electrode inputs is in the range 0 to 1.5V; thresholds have a 100mV step, and continuous current from 25nA to 200nA flows from the stages into the electrodes. */;
        }
        requirement req_IPOS_PAD_MUX_017 : IPOS_PAD_MUX_017;
        doc /* iposReqId=IPOS-PAD-MUX-017 | sourceReqId=DDS_STBIO1_395 | The DCC feature consists of two stages that detect whether one of six electrode inputs is in the range 0 to 1.5V; thresholds have a 100mV step, and continuous current from 25nA to 200nA flows from the stages into the electrodes. */;
        doc /* coverageDependency: IPOS-PAD-MUX-017 -> approved source requirement DDS_STBIO1_395 */;
        satisfy req_IPOS_PAD_MUX_017 by self;
    }

}

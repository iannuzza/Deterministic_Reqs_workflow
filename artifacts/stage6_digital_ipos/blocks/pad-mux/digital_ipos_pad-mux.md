# **Digital IPOS - PAD MUX** {#digital-ipos---pad-mux}

- Snapshot: `snap-b2e8101b00dc6909feaed885`

Author: Alessandro Lucio IANNUZZI

## **0. Document Navigation** {#0-document-navigation}

### **0.1 Table of contents** {#01-table-of-contents}
- [1. Block overview](#1-block-overview)
- [2. Source I/O](#2-source-io)
- [3. Block requirements](#3-block-requirements)

### **0.2 Document control** {#02-document-control}
#### **Table 1. Version history** {#table-1-version-history}
| Version | Date | Description | Author |
|---|---|---|---|
| 0.1 | 2026-10-01 | Snapshot snap-b2e8101b00dc6909feaed885 digital IPOS block baseline | Alessandro Lucio IANNUZZI |

### **0.3 Requirement navigation** {#03-requirement-navigation}
| Requirement | Internal link |
|---|---|
| IPOS-PAD-MUX-001 | [Go to requirement](#ipos-pad-mux-001) |
| IPOS-PAD-MUX-002 | [Go to requirement](#ipos-pad-mux-002) |
| IPOS-PAD-MUX-003 | [Go to requirement](#ipos-pad-mux-003) |
| IPOS-PAD-MUX-004 | [Go to requirement](#ipos-pad-mux-004) |
| IPOS-PAD-MUX-005 | [Go to requirement](#ipos-pad-mux-005) |
| IPOS-PAD-MUX-006 | [Go to requirement](#ipos-pad-mux-006) |
| IPOS-PAD-MUX-007 | [Go to requirement](#ipos-pad-mux-007) |
| IPOS-PAD-MUX-008 | [Go to requirement](#ipos-pad-mux-008) |
| IPOS-PAD-MUX-009 | [Go to requirement](#ipos-pad-mux-009) |
| IPOS-PAD-MUX-010 | [Go to requirement](#ipos-pad-mux-010) |
| IPOS-PAD-MUX-011 | [Go to requirement](#ipos-pad-mux-011) |
| IPOS-PAD-MUX-012 | [Go to requirement](#ipos-pad-mux-012) |
| IPOS-PAD-MUX-013 | [Go to requirement](#ipos-pad-mux-013) |
| IPOS-PAD-MUX-014 | [Go to requirement](#ipos-pad-mux-014) |
| IPOS-PAD-MUX-015 | [Go to requirement](#ipos-pad-mux-015) |
| IPOS-PAD-MUX-016 | [Go to requirement](#ipos-pad-mux-016) |
| IPOS-PAD-MUX-017 | [Go to requirement](#ipos-pad-mux-017) |

## **1. Block overview** {#1-block-overview}

### **1.1 Functionality** {#11-functionality}

The PAD MUX block is designed to route source-specified functional, scan, BIST, debug, and ISPU-debug signals to and from device pads.

### **1.2 Supported functions and scope** {#12-supported-functions-and-scope}

- The PAD MUX accepts mode selection, register-map controls, test controls, and internal block outputs and produces pad controls, test observations, and routed internal signals.

## **2. Source I/O** {#2-source-io}

The following approved source I/O entries are owned by this block.

| Port name | Direction | Type / details | Table | Source page |
|---|---|---|---|---|
| i_write_protection_en | input | write_protection_en OTP regmap enable from regmap | PAD MUX I/O List | 49 |
| o_write_protection_en | output | write_protection_en OTP regmap enable to regmap | PAD MUX I/O List | 49 |
| i_tap_bist_mode | input | bist_mode signal used retun in functional mode | PAD MUX I/O List | 49 |
| i_EN_0P05HP_ECG0 | input | bit enable select PDRES 05 ECG0 channel | PAD MUX I/O List | 49 |
| i_EN_0P05HP_ECG12 | input | bit enable select PDRES 05 ECG12 channel | PAD MUX I/O List | 49 |
| IMPQ_PSDRES_UP_02 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| IMPQ_PSDRES_DOWN_02 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| IMPP_PSDRES_UP_02 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| IMPP_PSDRES_DOWN_02 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| ECG_PSDRES_DOWN_02 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| ECG_PSDRES_UP_02 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| IMPQ_PSDRES_UP_05 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| IMPQ_PSDRES_DOWN_05 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| IMPP_PSDRES_UP_05 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| IMPP_PSDRES_DOWN_05 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| ECG_PSDRES_DOWN_05 | input | [2:0] OTP value for Analog block | PAD MUX I/O List | 49 |
| ECG_PSDRES_UP_05 | input | [2:0] OTP value for Analog block 49 | PAD MUX I/O List | 49 |
| IMPQ_PSDRES_UP | output | [2:0] OTP value for Analog block | PAD MUX I/O List | 50 |
| IMPQ_PSDRES_DOWN | output | [2:0] OTP value for Analog block | PAD MUX I/O List | 50 |
| IMPP_PSDRES_UP | output | [2:0] OTP value for Analog block | PAD MUX I/O List | 50 |
| IMPP_PSDRES_DOWN | output | [2:0] OTP value for Analog block | PAD MUX I/O List | 50 |
| ECG_PSDRES_DOWN | output | [2:0] OTP value for Analog block | PAD MUX I/O List | 50 |
| ECG_PSDRES_UP | output | [2:0] OTP value for Analog block | PAD MUX I/O List | 50 |
| i_TS_IRQ_ST | input | time slot irq | PAD MUX I/O List | 50 |
| i_DCCK_IRQ_ST | input | DCCK irq change status | PAD MUX I/O List | 50 |
| o_en_tx_1V2 | input | input to LED pilot | PAD MUX I/O List | 50 |
| o_tx_preset_1V2 | input | input to LED pilot | PAD MUX I/O List | 50 |
| o_tx1_outlab_sel_frame_x_1V2 | input | input to LED pilot | PAD MUX I/O List | 50 |
| sel_irq_gpio1 | input | [3:0] sel irq gpi1 {000:NC, 001:i_fifo_irq, 010:i_LED_Pilot, 011:i_DCCK_irq, 100:i_error_time_slot, 101:i_time_slot_irq} | PAD MUX I/O List | 50 |
| sel_irq_gpio2 | input | [3:0] sel irq gpi2 {000:NC, 001:i_fifo_irq, 010:i_LED_Pilot, 011:i_DCCK_irq, 100:i_error_time_slot, 101:i_time_slot_irq} | PAD MUX I/O List | 50 |
| sel_irq_gpio3 | input | [3:0] sel irq gpi3 {000:NC, 001:i_fifo_irq, 010:i_LED_Pilot, 011:i_DCCK_irq, 100:i_error_time_slot, 101:i_time_slot_irq} | PAD MUX I/O List | 50 |
| sel_irq_gpio4 | input | [3:0] sel irq gpi4 {000:NC, 001:i_fifo_irq, 010:i_LED_Pilot, 011:i_DCCK_irq, 100:i_error_time_slot, 101:i_time_slot_irq} | PAD MUX I/O List | 50 |
| DCCK_P_en | input | Manages lead off mode DCCK_P, Source: Regmap | PAD MUX I/O List | 50 |
| DCCK_N_en | input | Manages lead off mode DCCK_P, Source: Regmap | PAD MUX I/O List | 50 |
| MODE_OPERATION | input | Start Divice operations status 50 | PAD MUX I/O List | 50 |
| o_pd_p | output | enable lead off mode DCCK_P, Destination:Analog block | PAD MUX I/O List | 51 |
| o_pd_n | output | enable lead off mode DCCK_N, Destination:Analog block | PAD MUX I/O List | 51 |
| O_DCCK_P_i | input | status lead off mode DCCK_P {0:low impedance,1:floating electrode}, Source: Analog block | PAD MUX I/O List | 51 |
| O_DCCK_N_i | input | status lead off mode DCCK_N {0:low impedance,1:floating electrode}, Source: Analog block | PAD MUX I/O List | 51 |
| if_gpio1_in_reg | output | ZI value from regmap | PAD MUX I/O List | 51 |
| if_gpio1_en_reg | input | EN value from regmap | PAD MUX I/O List | 51 |
| if_gpio1_out_reg | input | OUT value from regmap | PAD MUX I/O List | 51 |
| if_gpio2_in_reg | output | ZI value from regmap// ZI | PAD MUX I/O List | 51 |
| if_gpio2_en_reg | input | EN value from regmap | PAD MUX I/O List | 51 |
| if_gpio2_out_reg | input | OUT value from regmap | PAD MUX I/O List | 51 |
| if_gpio3_in_reg | output | ZI value from regmap | PAD MUX I/O List | 51 |
| if_gpio3_en_reg | input | EN value from regmap | PAD MUX I/O List | 51 |
| if_gpio3_out_reg | input | OUT value from regmap | PAD MUX I/O List | 51 |
| if_gpio4_in_reg | output | ZI value from regmap | PAD MUX I/O List | 51 |
| if_gpio4_en_reg | input | EN value from regmap | PAD MUX I/O List | 51 |
| if_gpio4_out_reg | input | OUT value from regmap | PAD MUX I/O List | 51 |
| o_ext_reg_dt_afe | input | [7:0] i2c/spi read data u_regmap_otp | PAD MUX I/O List | 51 |
| o_ext_reg_dt | output | [7:0] i2c/spi read data output | PAD MUX I/O List | 51 |
| i_ext_reg_add | input | [7:0] i2c/spi address | PAD MUX I/O List | 51 |
| i_ext_reg_dt | input | [7:0] i2c/spi write data | PAD MUX I/O List | 51 |
| i_ext_reg_ck_wr | input | i2c/spi clk 51 | PAD MUX I/O List | 51 |
| i_ext_reg_we | input | i2c/spi regmap direct write enable | PAD MUX I/O List | 52 |
| if_sclk_in | input | ZI_I2C | PAD MUX I/O List | 52 |
| if_sclk_i3c_in | input | ZI_I3C | PAD MUX I/O List | 52 |
| if_sclk_out | output | A | PAD MUX I/O List | 52 |
| if_sclk_en | output | EN | PAD MUX I/O List | 52 |
| if_sclk_tud | output | TUD | PAD MUX I/O List | 52 |
| if_sda_sdi_in | input | ZI_I2C | PAD MUX I/O List | 52 |
| if_sda_sdi_i3c_in | input | ZI_I3C | PAD MUX I/O List | 52 |
| if_sda_sdi_out | output | A | PAD MUX I/O List | 52 |
| if_sda_sdi_en | output | EN | PAD MUX I/O List | 52 |
| if_sda_sdi_tud | output | TUD | PAD MUX I/O List | 52 |
| if_cs_in | input | ZI CS | PAD MUX I/O List | 52 |
| if_cs_out | output | A | PAD MUX I/O List | 52 |
| if_cs_en | output | EN | PAD MUX I/O List | 52 |
| if_cs_tud | output | TUD | PAD MUX I/O List | 52 |
| if_gpio0_in | input | ZI GPIO0 | PAD MUX I/O List | 52 |
| if_gpio0_out | output | A | PAD MUX I/O List | 52 |
| if_gpio0_en | output | EN | PAD MUX I/O List | 52 |
| if_gpio0_tud | output | TUD | PAD MUX I/O List | 52 |
| if_gpio1_in | input | ZI GPIO1 | PAD MUX I/O List | 52 |
| if_gpio1_out | output | A | PAD MUX I/O List | 52 |
| if_gpio1_en | output | EN | PAD MUX I/O List | 52 |
| if_gpio1_tud | output | TUD | PAD MUX I/O List | 52 |
| if_gpio2_in | input | ZI GPIO2 52 | PAD MUX I/O List | 52 |
| if_gpio2_out | output | A | PAD MUX I/O List | 53 |
| if_gpio2_en | output | EN | PAD MUX I/O List | 53 |
| if_gpio2_tud | output | TUD | PAD MUX I/O List | 53 |
| if_gpio3_in | input | ZI GPIO3 | PAD MUX I/O List | 53 |
| if_gpio3_out | output | A | PAD MUX I/O List | 53 |
| if_gpio3_en | output | EN | PAD MUX I/O List | 53 |
| if_gpio3_tud | output | TUD | PAD MUX I/O List | 53 |
| if_gpio4_in | input | ZI GPIO4 | PAD MUX I/O List | 53 |
| if_gpio4_out | output | A | PAD MUX I/O List | 53 |
| if_gpio4_en | output | EN | PAD MUX I/O List | 53 |
| if_gpio4_tud | output | TUD | PAD MUX I/O List | 53 |
| if_sh_ck_in | input | ZI sensor hub ck | PAD MUX I/O List | 53 |
| if_sh_ck_out | output | A | PAD MUX I/O List | 53 |
| if_sh_ck_en | output | EN | PAD MUX I/O List | 53 |
| if_sh_ck_tud | output | TUD | PAD MUX I/O List | 53 |
| if_sh_sda_in | input | ZI sensor hub SDA | PAD MUX I/O List | 53 |
| if_sh_sda_out | output | A | PAD MUX I/O List | 53 |
| if_sh_sda_en | output | EN | PAD MUX I/O List | 53 |
| if_sh_sda_tud | output | TUD | PAD MUX I/O List | 53 |
| POR1V2_1V2 | input | POR | PAD MUX I/O List | 53 |
| ispu_tck | output | jtag clk port ispu in ispu debug mode | PAD MUX I/O List | 53 |
| ispu_tdi | output | jtag data in port ispu in ispu debug mode | PAD MUX I/O List | 53 |
| ispu_tdo | input | jtag data out port ispu in ispu debug mode | PAD MUX I/O List | 53 |
| ispu_tdo_en | input | jtag en port ispu in ispu debug mode 53 | PAD MUX I/O List | 53 |
| ispu_tms | output | jtag state in port ispu in ispu debug mode | PAD MUX I/O List | 54 |
| ispu_trst_n | output | jtag reset in port ispu in ispu debug mode | PAD MUX I/O List | 54 |
| i_if_ck | output | i2c/spi clk | PAD MUX I/O List | 54 |
| i_if_cs | output | i2c/spi cs | PAD MUX I/O List | 54 |
| i_if_sda_sdi_in | output | i2c/spi data | PAD MUX I/O List | 54 |
| o_if_cs_en_n | input | i2c/spi cs en from i2c/spi ip | PAD MUX I/O List | 54 |
| o_if_cs_out_n | input | i2c/spi cs out from i2c/spi ip | PAD MUX I/O List | 54 |
| o_if_cs_tud | input | i2c/spi cs tud from i2c/spi ip | PAD MUX I/O List | 54 |
| o_if_sda_sdi_en_n | input | i2c/spi data en from i2c/spi ip | PAD MUX I/O List | 54 |
| o_if_sda_sdi_out | input | i2c/spi data out from i2c/spi ip | PAD MUX I/O List | 54 |
| scl_master_in | output | from sensorhub | PAD MUX I/O List | 54 |
| scl_master_out | input | from sensorhub | PAD MUX I/O List | 54 |
| sda_master_in | output | to sensorhub | PAD MUX I/O List | 54 |
| sda_master_out | input | from sensorhub | PAD MUX I/O List | 54 |
| afe_bist_ctrl_tdi | output | bist jtag port | PAD MUX I/O List | 54 |
| afe_bist_ctrl_trstn | output | bist jtag port | PAD MUX I/O List | 54 |
| afe_bist_ctrl_tms | output | bist jtag port | PAD MUX I/O List | 54 |
| afe_bist_ctrl_tdo | input | bist jtag port | PAD MUX I/O List | 54 |
| afe_bist_ctrl_tdo_en_n | input | bist jtag port | PAD MUX I/O List | 54 |
| afe_bist_ctrl_tck | output | bist jtag port | PAD MUX I/O List | 54 |
| ck_16m | input | clk16MHz trimming in debug mode | PAD MUX I/O List | 54 |
| ck_2m | input | clk2MHz trimming in debug mode | PAD MUX I/O List | 54 |
| ck_64k | input | clk64MHz trimming in debug mode | PAD MUX I/O List | 54 |
| scan_rstn | output | scan reset 54 | PAD MUX I/O List | 54 |
| scan_enable | output | scan enable | PAD MUX I/O List | 55 |
| scan_clk | output | scan clock | PAD MUX I/O List | 55 |
| ext_cap_en | input | extenal cap in debug mode | PAD MUX I/O List | 55 |
| irq_fifo | input | fifo irq from main controller - regmap | PAD MUX I/O List | 55 |
| error_time_slot | input | error timeslot from error time slot | PAD MUX I/O List | 55 |
| gpio_in | output | gpio0 in in functional mode from regmap | PAD MUX I/O List | 55 |
| gpio_out | input | gpio0 out in functional mode from regmap | PAD MUX I/O List | 55 |
| gpio_en | input | gpio0 en in functional mode from regmap | PAD MUX I/O List | 55 |
| irq_SENSHUB_STS | input | sensorhub status | PAD MUX I/O List | 55 |
| irq_ISPU_MC_INTR_STS | input | irq main controller data-valid | PAD MUX I/O List | 55 |
| scan_mode | output | stbio1 scan mode | PAD MUX I/O List | 55 |
| bist_mode | output | stbio1 bist mode | PAD MUX I/O List | 55 |
| debug_mode | output | stbio1 debug mode | PAD MUX I/O List | 55 |
| memsafe | output | memsafe for bist | PAD MUX I/O List | 55 |
| test_clk_fast | input | enable test clk 16MHz trimming | PAD MUX I/O List | 55 |
| test_clk_slow | input | enable test clk 64kHz trimming | PAD MUX I/O List | 55 |
| if_sclk_tud_reg | input | if sclk_tud from reg | PAD MUX I/O List | 55 |
| if_sda_sdi_tud_reg | input | if sda_sdi_tud from re | PAD MUX I/O List | 55 |
| if_sh_sda_tud_reg | input | if sh_sda_tud from reg | PAD MUX I/O List | 55 |
| if_gpio0_tud_reg | input | if gpio0_tud from reg | PAD MUX I/O List | 55 |
| if_gpio1_tud_reg | input | if gpio1_tud from reg | PAD MUX I/O List | 55 |
| if_gpio2_tud_reg | input | if gpio2_tud from reg | PAD MUX I/O List | 55 |
| if_gpio3_tud_reg | input | if gpio3_tud from reg 55 | PAD MUX I/O List | 55 |
| if_gpio4_tud_reg | input | if gpio4_tud from reg | PAD MUX I/O List | 56 |
| if_sh_ck_tud_reg | input | if sh_ck_tud from reg | PAD MUX I/O List | 56 |
| clk_dft_adc | input | 16MHz adc dft clk | PAD MUX I/O List | 56 |
| i_ADC_clk_serial_dft | input | serial clk for adc dft 16Mhz:Fast mode, if_sh_ck_in:Low noise mode | PAD MUX I/O List | 56 |
| EN_ADC_TEST_FAST | input | enable adc test fast | PAD MUX I/O List | 56 |
| EN_ADC_TEST_LOW_NOISE | input | enable adc test low noise | PAD MUX I/O List | 56 |
| i_ADC_EOC | input | adc eoc input | PAD MUX I/O List | 56 |
| i_ADC_start | input | adc star from main controller | PAD MUX I/O List | 56 |
| i_data_ADC_out | input | [15:0] adc data input | PAD MUX I/O List | 56 |
| o_ADC_start | output | adc star output | PAD MUX I/O List | 56 |
| i_N_clk | input | [6- 1:0] n clk start time high | PAD MUX I/O List | 56 |
| i_saturation_irq | input | interrupt saturation from main controller | PAD MUX I/O List | 56 |
| i_end_boot | input | end boot signal from adsp | PAD MUX I/O List | 56 |
| quokka_run | input | status quokka elaboration 1:run 0:not elaboration | PAD MUX I/O List | 56 |
| sensor_hub_status | input | status sensor_hob from regmap | PAD MUX I/O List | 56 |
| SH_CKL_EN | input | sensorhub clk enable from regmap (master_end_op_clr or sleep_master_clr or ahb_master_on_clr) | PAD MUX I/O List | 56 |
| i_t_force_1v2 | input | input force signal to IDDQ test | PAD MUX I/O List | 56 |
| o_t_force_1v2 | output | force signal to IDDQ test | PAD MUX I/O List | 56 |
| i_bfail_fifo | input | bist fail fifo ram | PAD MUX I/O List | 56 |
| i_bfail_qk | input | bist fail adsp ram | PAD MUX I/O List | 56 |
| i_bfail_ispu1 | input | bist fail ispu ram instruction mem | PAD MUX I/O List | 56 |
| i_bfail_ispu2 | input | bist fail ispu ram data mem 1 56 | PAD MUX I/O List | 56 |
| i_bfail_ispu3 | input | bist fail ispu ram data mem 2 | PAD MUX I/O List | 57 |
| i_bfail_ispu4 | input | bist fail ispu ram data mem 3 | PAD MUX I/O List | 57 |
| i_bend | input | bist end signal | PAD MUX I/O List | 57 |
| i_bbad | input | signal fail bist test | PAD MUX I/O List | 57 |
| o_bypass | output | bypass memory signal | PAD MUX I/O List | 57 |

## **3. Block requirements** {#3-block-requirements}


#### **IPOS-PAD-MUX-001** {#ipos-pad-mux-001}
[DDS_STBIO1_302] Requirement If MODE_CONFIG register is 0x00 the operative mode shall be functional.

Covers: DDS_STBIO1_302

[End]


#### **IPOS-PAD-MUX-002** {#ipos-pad-mux-002}
[DDS_STBIO1_303] Requirement If MODE_CONFIG register is 0x01 the operative mode shall be SCAN.

Covers: DDS_STBIO1_303

[End]


#### **IPOS-PAD-MUX-003** {#ipos-pad-mux-003}
[DDS_STBIO1_304] Requirement If MODE_CONFIG register is 0x04 the operative mode shall be BIST.

Covers: DDS_STBIO1_304

[End]


#### **IPOS-PAD-MUX-004** {#ipos-pad-mux-004}
[DDS_STBIO1_305] Requirement If MODE_CONFIG register is 0x08 the operative mode shall be DEBUG.

Covers: DDS_STBIO1_305

[End]


#### **IPOS-PAD-MUX-005** {#ipos-pad-mux-005}
[DDS_STBIO1_306] Requirement If MODE_CONFIG register is 0x10 the operative mode shall be ISPU_DEBUG.

Covers: DDS_STBIO1_306

[End]


#### **IPOS-PAD-MUX-006** {#ipos-pad-mux-006}
[DDS_STBIO1_307] Requirement If MODE_CONFIG register is 0x20 the operative mode shall be Bist MEMSAFE mode.

Covers: DDS_STBIO1_307

[End]


#### **IPOS-PAD-MUX-007** {#ipos-pad-mux-007}
[DDS_STBIO1_308] Requirement If MODE_CONFIG register is 0x40 the operative mode shall be Bist Bypass mode.

Covers: DDS_STBIO1_308

[End]


#### **IPOS-PAD-MUX-008** {#ipos-pad-mux-008}
In function mode, the GPIO1,2,3,4_out shall be irq_fifo if sel irq gpio1,2,3,4 is 0x01 and ext_cap_en is “0” [Vpriority High]

Covers: DDS_STBIO1_309

[End]


#### **IPOS-PAD-MUX-009** {#ipos-pad-mux-009}
In function mode, the GPIO1,2,3,4_out shall be i_LED_Pilot if sel irq gpi1,2,3,4 is 0x02 and ext_cap_en is “0” [Vpriority High]

Covers: DDS_STBIO1_310

[End]


#### **IPOS-PAD-MUX-010** {#ipos-pad-mux-010}
In function mode, the GPIO1,2,3,4_out shall be i_DCCK_irq if sel irq gpi1,2,3,4 is 0x03 and ext_cap_en is “0” [Vpriority High]

Covers: DDS_STBIO1_311

[End]


#### **IPOS-PAD-MUX-011** {#ipos-pad-mux-011}
In function mode, the GPIO1,2,3,4 output shall be i_error_time_slot if sel irq gpi1,2,3,4 is 0x04 and ext_cap_en is “0” [Vpriority High]

Covers: DDS_STBIO1_312

[End]


#### **IPOS-PAD-MUX-012** {#ipos-pad-mux-012}
In function mode, the GPIO1,2,3,4 output shall be i_time_slot_irq if sel irq gpi1,2,3,4 is 0x05 and ext_cap_en is “0” [Vpriority High]

Covers: DDS_STBIO1_313

[End]


#### **IPOS-PAD-MUX-013** {#ipos-pad-mux-013}
In function mode, the GPIO1,2,3,4_out shall be General-Purpose if sel irq gpi1,2,3,4 is 0x00 and ext_cap_en is “0” [Vpriority High]

Covers: DDS_STBIO1_314

[End]


#### **IPOS-PAD-MUX-014** {#ipos-pad-mux-014}
If O_DCCK_P_i changes its value from '0' to '1' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp, shall be set to '1'

Covers: DDS_STBIO1_392

[End]


#### **IPOS-PAD-MUX-015** {#ipos-pad-mux-015}
If O_DCCK_N_i changes its value from '0' to '1' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp, shall be set to '1'

Covers: DDS_STBIO1_393

[End]


#### **IPOS-PAD-MUX-016** {#ipos-pad-mux-016}
If O_DCCK_P_i changes its value from '1' to '0' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp, shall be set to '1'

Covers: DDS_STBIO1_394

[End]


#### **IPOS-PAD-MUX-017** {#ipos-pad-mux-017}
The DCC feature consists of two stages that detect whether one of six electrode inputs is in the range 0 to 1.5V; thresholds have a 100mV step, and continuous current from 25nA to 200nA flows from the stages into the electrodes.

Covers: DDS_STBIO1_395

[End]


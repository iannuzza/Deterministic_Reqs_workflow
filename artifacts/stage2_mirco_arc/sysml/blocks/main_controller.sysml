// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 8d22eb86b9a584c32e1fedacf6d98a199b8f93896143054eb1c8b2075b0ea372

package STBIO_Block_MainController {

    private import STBIO_Shared::*;

    part def MainController {
        attribute displayName : String = "Main Controller";
        attribute description : String = "Generate and receive Analog Domain control signals, perform DSP elaboration on ADC outputs, and write elaborated results to the defined addresses.";
        attribute function : String = "Generate and receive Analog Domain control signals, perform DSP elaboration on ADC outputs, and write elaborated results to the defined addresses.";
        attribute inputs : String = "Configuration register settings, sampled data";
        attribute outputs : String = "Control state and data routing";
        attribute approvedPortCount : Integer = 224;
        attribute linkedRequirementCount : Integer = 138;
        doc /* block=Main Controller | description=Generate and receive Analog Domain control signals, perform DSP elaboration on ADC outputs, and write elaborated results to the defined addresses. */;
        in port i_clk_32kHz : ArchitecturePort {
            attribute sourceName = "i_clk_32kHz";
            attribute sourceDetails = "clk 32kHz from pmu";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_clk_16MHz : ArchitecturePort {
            attribute sourceName = "i_clk_16MHz";
            attribute sourceDetails = "clk 16MHz from pmu";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_clk_gsr_16M : ArchitecturePort {
            attribute sourceName = "i_clk_gsr_16M";
            attribute sourceDetails = "clk for gsr signal";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_clk_ahb_master : ArchitecturePort {
            attribute sourceName = "i_clk_ahb_master";
            attribute sourceDetails = "clock for ahb master";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_rstn : ArchitecturePort {
            attribute sourceName = "i_rstn";
            attribute sourceDetails = "reset in 16MHz domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_rstn_sync_32 : ArchitecturePort {
            attribute sourceName = "i_rstn_sync_32";
            attribute sourceDetails = "reset in 32kz domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_wave_velocity_mode : ArchitecturePort {
            attribute sourceName = "i_wave_velocity_mode";
            attribute sourceDetails = "enable of the wave velocity mode";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_ispu_end_elab : ArchitecturePort {
            attribute sourceName = "i_ispu_end_elab";
            attribute sourceDetails = "";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_n_ppg_frame : ArchitecturePort {
            attribute sourceName = "i_n_ppg_frame";
            attribute sourceDetails = "[ppg_frame_bit_top-1:0] number of frame selected";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_const_value_ioff : ArchitecturePort {
            attribute sourceName = "i_const_value_ioff";
            attribute sourceDetails = "[data_in_size_bit_top-1:0] constant value from regmap used for ppg ioff calibraton";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_rx_ch_frame : ArchitecturePort {
            attribute sourceName = "i_rx_ch_frame";
            attribute sourceDetails = "[n_max_frame-1:0] ppg rx channel frame from regamp";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_T_tx_led_set : ArchitecturePort {
            attribute sourceName = "i_T_tx_led_set";
            attribute sourceDetails = "[n_max_frame-1:0] tx led set time from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_T_tx_led_off : ArchitecturePort {
            attribute sourceName = "i_T_tx_led_off";
            attribute sourceDetails = "[n_max_frame-1:0] tx led off time from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_curr_sel_tx_frame_x : ArchitecturePort {
            attribute sourceName = "i_curr_sel_tx_frame_x";
            attribute sourceDetails = "[n_max_frame-1:0] current injection";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_tx1_outlab_sel_frame_x : ArchitecturePort {
            attribute sourceName = "i_tx1_outlab_sel_frame_x";
            attribute sourceDetails = "[n_max_frame-1:0] led output selected from regmap for each frame";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_tx2_outlab_sel_frame_x : ArchitecturePort {
            attribute sourceName = "i_tx2_outlab_sel_frame_x";
            attribute sourceDetails = "[n_max_frame-1:0] led output selected from regmap for each frame";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_tx3_outlab_sel_frame_x : ArchitecturePort {
            attribute sourceName = "i_tx3_outlab_sel_frame_x";
            attribute sourceDetails = "[n_max_frame-1:0] led output selected from regmap for each frame";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_tx4_outlab_sel_frame_x : ArchitecturePort {
            attribute sourceName = "i_tx4_outlab_sel_frame_x";
            attribute sourceDetails = "[n_max_frame-1:0] led output selected from regmap for each frame";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_idac_dc_ppg_frame : ArchitecturePort {
            attribute sourceName = "i_idac_dc_ppg_frame";
            attribute sourceDetails = "[n_max_frame-1:0] idac value for each frame selected from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_average_ppg : ArchitecturePort {
            attribute sourceName = "i_average_ppg";
            attribute sourceDetails = "[n_max_frame-1:0] average ppg for each frame selected from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_gain_alc_start : ArchitecturePort {
            attribute sourceName = "i_gain_alc_start";
            attribute sourceDetails = "[gain_max_bit_top-1:0] btia gain for alc from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_gain_start : ArchitecturePort {
            attribute sourceName = "i_gain_start";
            attribute sourceDetails = "[n_max_frame-1:0] btia gain start for compensation from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_Tx_idac_Vref_debug : ArchitecturePort {
            attribute sourceName = "i_Tx_idac_Vref_debug";
            attribute sourceDetails = "[Nmax_bit_top-1:0] Idac value for debug from regmap 76";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "76";
        }
        in port i_ppg_start_up_time : ArchitecturePort {
            attribute sourceName = "i_ppg_start_up_time";
            attribute sourceDetails = "[ppg_start_up_decod_bit_top-1:0] start up time for ppg from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_en_txi : ArchitecturePort {
            attribute sourceName = "i_en_txi";
            attribute sourceDetails = "[n_max_frame-1:0] tx enabling for each frame from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_frame_repetition : ArchitecturePort {
            attribute sourceName = "i_frame_repetition";
            attribute sourceDetails = "[n_max_frame-1:0] i frame repetition for each frame from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_T_preset : ArchitecturePort {
            attribute sourceName = "i_T_preset";
            attribute sourceDetails = "[1:0] Preset time for digital ramp from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_m_ecg : ArchitecturePort {
            attribute sourceName = "i_m_ecg";
            attribute sourceDetails = "[m_odr_max_bit_top-1:0] m parameter for ecg from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_m_bia : ArchitecturePort {
            attribute sourceName = "i_m_bia";
            attribute sourceDetails = "[m_odr_max_bit_top-1:0] m parameter for bia from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_m_gsr : ArchitecturePort {
            attribute sourceName = "i_m_gsr";
            attribute sourceDetails = "[m_odr_max_bit_top-1:0] m parameter for gsr from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_m_ppg : ArchitecturePort {
            attribute sourceName = "i_m_ppg";
            attribute sourceDetails = "[m_odr_max_bit_top-1:0] m parameter for ppg from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_debug_adc_error_cap8_0_bypass : ArchitecturePort {
            attribute sourceName = "i_debug_adc_error_cap8_0_bypass";
            attribute sourceDetails = "error cap bypass for adc from regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_base_address_ecg0 : ArchitecturePort {
            attribute sourceName = "i_base_address_ecg0";
            attribute sourceDetails = "[base_address_bit_top-1:0] base address for ecg0 in multiple fifo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_base_address_bia : ArchitecturePort {
            attribute sourceName = "i_base_address_bia";
            attribute sourceDetails = "[base_address_bit_top-1:0] base address for bia/ecg1-2 in multiple fifo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_base_address_gsr : ArchitecturePort {
            attribute sourceName = "i_base_address_gsr";
            attribute sourceDetails = "[base_address_bit_top-1:0] base address for gsr in multiple fifo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_base_address_ppg : ArchitecturePort {
            attribute sourceName = "i_base_address_ppg";
            attribute sourceDetails = "[base_address_bit_top-1:0] base address for ppg in multiple fifo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_frame_ppg_debug : ArchitecturePort {
            attribute sourceName = "i_frame_ppg_debug";
            attribute sourceDetails = "[ppg_frame_bit_top-1:0] frame selection for ppg data debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_en_buf_gpio1 : ArchitecturePort {
            attribute sourceName = "i_en_buf_gpio1";
            attribute sourceDetails = "enable buffer on gpio1";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_en_buf_gpio2 : ArchitecturePort {
            attribute sourceName = "i_en_buf_gpio2";
            attribute sourceDetails = "enable buffer on gpio2";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_en_biobuf : ArchitecturePort {
            attribute sourceName = "i_en_biobuf";
            attribute sourceDetails = "enable biobuffer";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_do_calibration : ArchitecturePort {
            attribute sourceName = "i_do_calibration";
            attribute sourceDetails = "enabling for adc calibration";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_mode_operation : ArchitecturePort {
            attribute sourceName = "i_mode_operation";
            attribute sourceDetails = "[mode_operation_n_bit_top-1:0] mode operation selection";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_T_rx_set : ArchitecturePort {
            attribute sourceName = "i_T_rx_set";
            attribute sourceDetails = "[T1_max_bit_from_decoder_top- 1:0] rx channel time set";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_en_clkf : ArchitecturePort {
            attribute sourceName = "i_en_clkf";
            attribute sourceDetails = "en 16 MHz clock";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_quokka_boot_end : ArchitecturePort {
            attribute sourceName = "i_quokka_boot_end";
            attribute sourceDetails = "from quokka";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_quokka_run : ArchitecturePort {
            attribute sourceName = "i_quokka_run";
            attribute sourceDetails = "from quokka 77";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "77";
        }
        in port i_clk_16MHz_ready : ArchitecturePort {
            attribute sourceName = "i_clk_16MHz_ready";
            attribute sourceDetails = "(from analog circuit)";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_imp_curinj_en : ArchitecturePort {
            attribute sourceName = "i_imp_curinj_en";
            attribute sourceDetails = "enabling current injection for bia";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_en_ldo_1v8 : ArchitecturePort {
            attribute sourceName = "i_en_ldo_1v8";
            attribute sourceDetails = "enabling ldo 1v8";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_debug_comp_rx_ck : ArchitecturePort {
            attribute sourceName = "i_debug_comp_rx_ck";
            attribute sourceDetails = "enabling debug for comp rx ck";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_debug_gsr_on : ArchitecturePort {
            attribute sourceName = "i_debug_gsr_on";
            attribute sourceDetails = "gsr on debug mode";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_debug_gsr_curr_on : ArchitecturePort {
            attribute sourceName = "i_debug_gsr_curr_on";
            attribute sourceDetails = "gsr curr on debug mode";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_alc_disabled : ArchitecturePort {
            attribute sourceName = "i_alc_disabled";
            attribute sourceDetails = "[n_max_frame-1:0] disabling alc bit for each frame";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_en_cm_buf : ArchitecturePort {
            attribute sourceName = "i_en_cm_buf";
            attribute sourceDetails = "enabling common buffer";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_en_rld : ArchitecturePort {
            attribute sourceName = "i_en_rld";
            attribute sourceDetails = "enabling rld";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_en_avg1 : ArchitecturePort {
            attribute sourceName = "i_en_avg1";
            attribute sourceDetails = "enabling avg1";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_en_avg2 : ArchitecturePort {
            attribute sourceName = "i_en_avg2";
            attribute sourceDetails = "enabling avg1";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_hc_en : ArchitecturePort {
            attribute sourceName = "i_hc_en";
            attribute sourceDetails = "enabling health channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_debug : ArchitecturePort {
            attribute sourceName = "i_debug";
            attribute sourceDetails = "enabling debug mode";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_imp_en : ArchitecturePort {
            attribute sourceName = "i_imp_en";
            attribute sourceDetails = "enabling bia channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_debug_en_tia : ArchitecturePort {
            attribute sourceName = "i_debug_en_tia";
            attribute sourceDetails = "enabling debug tia";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_debug_en_buffer : ArchitecturePort {
            attribute sourceName = "i_debug_en_buffer";
            attribute sourceDetails = "enabling debug for buffer";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_debug_en_idac : ArchitecturePort {
            attribute sourceName = "i_debug_en_idac";
            attribute sourceDetails = "enabling debug for IDAC";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_en_clk_chop10k : ArchitecturePort {
            attribute sourceName = "i_en_clk_chop10k";
            attribute sourceDetails = "enabling chopper clock";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_debug_tx_preset : ArchitecturePort {
            attribute sourceName = "i_debug_tx_preset";
            attribute sourceDetails = "enabling tx preset";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_en_ldo_1v8_ext : ArchitecturePort {
            attribute sourceName = "i_en_ldo_1v8_ext";
            attribute sourceDetails = "enabling external ldo 1v8";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_clk_imp_10k_en : ArchitecturePort {
            attribute sourceName = "i_clk_imp_10k_en";
            attribute sourceDetails = "enabling clock chopper for bia";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_b_cap_idac : ArchitecturePort {
            attribute sourceName = "i_b_cap_idac";
            attribute sourceDetails = "[1:0] enabling cap for idac";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_adc_mux_bio_channel_debug : ArchitecturePort {
            attribute sourceName = "i_adc_mux_bio_channel_debug";
            attribute sourceDetails = "[2:0] enabling debug adc mux bio channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_adc_mux_sel_debug : ArchitecturePort {
            attribute sourceName = "i_adc_mux_sel_debug";
            attribute sourceDetails = "enabling adc mux 78";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "78";
        }
        in port i_ispu_core_sw_rstn : ArchitecturePort {
            attribute sourceName = "i_ispu_core_sw_rstn";
            attribute sourceDetails = "ispu core enabling";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_T_TIAON : ArchitecturePort {
            attribute sourceName = "i_T_TIAON";
            attribute sourceDetails = "[T1_max_bit_from_decoder_top- 1:0] TIA Time";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_scan_mode : ArchitecturePort {
            attribute sourceName = "i_scan_mode";
            attribute sourceDetails = "scan mode enabling";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_reset_debug_adc_data : ArchitecturePort {
            attribute sourceName = "i_reset_debug_adc_data";
            attribute sourceDetails = "reset adc data debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_start_adc_debug : ArchitecturePort {
            attribute sourceName = "i_start_adc_debug";
            attribute sourceDetails = "pilot adc start om debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_en_ADC_debug : ArchitecturePort {
            attribute sourceName = "i_en_ADC_debug";
            attribute sourceDetails = "enabling adc debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_debug_adc_readout_bypass : ArchitecturePort {
            attribute sourceName = "i_debug_adc_readout_bypass";
            attribute sourceDetails = "enabling adc readout bypass";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_su_hlt_dly : ArchitecturePort {
            attribute sourceName = "i_su_hlt_dly";
            attribute sourceDetails = "enabling start up delay for ecg";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_multiple_fifo_sel : ArchitecturePort {
            attribute sourceName = "i_multiple_fifo_sel";
            attribute sourceDetails = "enabling multiple fifo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_debug_calibration : ArchitecturePort {
            attribute sourceName = "i_debug_calibration";
            attribute sourceDetails = "enabling debug calibraiton";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_en_gsr_dc_cds : ArchitecturePort {
            attribute sourceName = "i_en_gsr_dc_cds";
            attribute sourceDetails = "[1:0] enabling gsr cds mode";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_ADC_EOC : ArchitecturePort {
            attribute sourceName = "i_ADC_EOC";
            attribute sourceDetails = "end of conversion from adc";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_ecg0_sel : ArchitecturePort {
            attribute sourceName = "i_ecg0_sel";
            attribute sourceDetails = "select ecg0 channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_bia_sel : ArchitecturePort {
            attribute sourceName = "i_bia_sel";
            attribute sourceDetails = "select bia channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_gsr_sel : ArchitecturePort {
            attribute sourceName = "i_gsr_sel";
            attribute sourceDetails = "select gsr channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_ppg_sel : ArchitecturePort {
            attribute sourceName = "i_ppg_sel";
            attribute sourceDetails = "select ppg channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_ppg_ioff_calibration : ArchitecturePort {
            attribute sourceName = "i_ppg_ioff_calibration";
            attribute sourceDetails = "enabling ppg ioff calibration";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_ecg1_ecg2_sel : ArchitecturePort {
            attribute sourceName = "i_ecg1_ecg2_sel";
            attribute sourceDetails = "enabling ecg1 and ecg2 channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_rst_async_ecg : ArchitecturePort {
            attribute sourceName = "i_rst_async_ecg";
            attribute sourceDetails = "reset async for ecg";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_rst_async_bia : ArchitecturePort {
            attribute sourceName = "i_rst_async_bia";
            attribute sourceDetails = "reset async for bia";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_ppg_quokka_elab_sel : ArchitecturePort {
            attribute sourceName = "i_ppg_quokka_elab_sel";
            attribute sourceDetails = "enabling adsp elab for ppg";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_data_ADC_out : ArchitecturePort {
            attribute sourceName = "i_data_ADC_out";
            attribute sourceDetails = "[data_in_size_bit_top-1:0] (from analog circuit)";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_time_slot_selection : ArchitecturePort {
            attribute sourceName = "i_time_slot_selection";
            attribute sourceDetails = "[time_slot_sel_bit_top-1:0] odr selection from regmap 79";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "79";
        }
        in port i_Nmax_to_reg : ArchitecturePort {
            attribute sourceName = "i_Nmax_to_reg";
            attribute sourceDetails = "[Nmax_bit_top-1:0] Max value for digital ramp";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_nstart_case : ArchitecturePort {
            attribute sourceName = "i_nstart_case";
            attribute sourceDetails = "[Nmax_bit_top-1:0] n_start value for frist sterp";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_debug_rx_ch : ArchitecturePort {
            attribute sourceName = "i_debug_rx_ch";
            attribute sourceDetails = "[rx_ch_frame_n_bit_top-1:0] enabling debug for rx channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_T_delta1_to_reg : ArchitecturePort {
            attribute sourceName = "i_T_delta1_to_reg";
            attribute sourceDetails = "[delta_bit_top-1:0] delta 1 time for digital ramp";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_gain_max_set : ArchitecturePort {
            attribute sourceName = "i_gain_max_set";
            attribute sourceDetails = "[gain_max_bit_top-1:0] gain max for alc";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_BTIA_ALC_debug : ArchitecturePort {
            attribute sourceName = "i_BTIA_ALC_debug";
            attribute sourceDetails = "[BTIA_ALC_register_bit_top-1:0] BTIA ALC Debug enable";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_comp_rx_out : ArchitecturePort {
            attribute sourceName = "i_comp_rx_out";
            attribute sourceDetails = "input from analog comparator";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_adc_error_cap8_debug : ArchitecturePort {
            attribute sourceName = "i_adc_error_cap8_debug";
            attribute sourceDetails = "[6:0] adc cap error debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_adc_error_cap7_debug : ArchitecturePort {
            attribute sourceName = "i_adc_error_cap7_debug";
            attribute sourceDetails = "[6:0] adc cap error debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_adc_error_cap6_debug : ArchitecturePort {
            attribute sourceName = "i_adc_error_cap6_debug";
            attribute sourceDetails = "[6:0] adc cap error debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_adc_error_cap5_debug : ArchitecturePort {
            attribute sourceName = "i_adc_error_cap5_debug";
            attribute sourceDetails = "[6:0] adc cap error debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_adc_error_cap4_debug : ArchitecturePort {
            attribute sourceName = "i_adc_error_cap4_debug";
            attribute sourceDetails = "[6:0] adc cap error debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_adc_error_cap3_debug : ArchitecturePort {
            attribute sourceName = "i_adc_error_cap3_debug";
            attribute sourceDetails = "[6:0] adc cap error debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_adc_error_cap2_debug : ArchitecturePort {
            attribute sourceName = "i_adc_error_cap2_debug";
            attribute sourceDetails = "[6:0] adc cap error debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_adc_error_cap1_debug : ArchitecturePort {
            attribute sourceName = "i_adc_error_cap1_debug";
            attribute sourceDetails = "[6:0] adc cap error debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_adc_error_cap0_debug : ArchitecturePort {
            attribute sourceName = "i_adc_error_cap0_debug";
            attribute sourceDetails = "[6:0] adc cap error debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_BIDAC_debug_register : ArchitecturePort {
            attribute sourceName = "i_BIDAC_debug_register";
            attribute sourceDetails = "[IDAC_offset-1:0]";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_sleep_master : ArchitecturePort {
            attribute sourceName = "i_sleep_master";
            attribute sourceDetails = "";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_lpm : ArchitecturePort {
            attribute sourceName = "i_lpm";
            attribute sourceDetails = "[1:0] low power mode for ldo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_mpm : ArchitecturePort {
            attribute sourceName = "i_mpm";
            attribute sourceDetails = "[1:0] medium power mode for ldo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_hpm : ArchitecturePort {
            attribute sourceName = "i_hpm";
            attribute sourceDetails = "[1:0] high power mode for ldo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_dis_rc_viref : ArchitecturePort {
            attribute sourceName = "i_dis_rc_viref";
            attribute sourceDetails = "dis rc viref";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_T1 : ArchitecturePort {
            attribute sourceName = "i_T1";
            attribute sourceDetails = "[T1_max_bit_from_decoder_top- 1:0] 4 to 10 us=160nclk 80";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "80";
        }
        in port i_T2 : ArchitecturePort {
            attribute sourceName = "i_T2";
            attribute sourceDetails = "[T2_max_bit_from_decoder_top- 1:0] 0.5 to 2 us=~32";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port i_N_clk_ppg : ArchitecturePort {
            attribute sourceName = "i_N_clk_ppg";
            attribute sourceDetails = "[N_clk_max_bit_top-1:0] Sample time for ppg";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port i_N_clk_ecg : ArchitecturePort {
            attribute sourceName = "i_N_clk_ecg";
            attribute sourceDetails = "[N_clk_max_bit_top-1:0] Sample time for ecg";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port i_N_clk_cal : ArchitecturePort {
            attribute sourceName = "i_N_clk_cal";
            attribute sourceDetails = "[N_clk_max_bit_top-1:0] Sample time for adc calibration";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port scan_enable : ArchitecturePort {
            attribute sourceName = "scan_enable";
            attribute sourceDetails = "scan enable for scan mode";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port i_timer_buffer_config : ArchitecturePort {
            attribute sourceName = "i_timer_buffer_config";
            attribute sourceDetails = "[1:0] timer buffer configuration";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port i_ppg_alc_frame_save : ArchitecturePort {
            attribute sourceName = "i_ppg_alc_frame_save";
            attribute sourceDetails = "[ppg_frame_bit_top-1:0] alc data frame to save";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port i_reset_ppg_ioff_calib : ArchitecturePort {
            attribute sourceName = "i_reset_ppg_ioff_calib";
            attribute sourceDetails = "";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port HRDATA : ArchitecturePort {
            attribute sourceName = "HRDATA";
            attribute sourceDetails = "[31:0] AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port HREADY : ArchitecturePort {
            attribute sourceName = "HREADY";
            attribute sourceDetails = "AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port HRESP : ArchitecturePort {
            attribute sourceName = "HRESP";
            attribute sourceDetails = "[1:0] AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port HGRANT : ArchitecturePort {
            attribute sourceName = "HGRANT";
            attribute sourceDetails = "AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port SCANENABLE : ArchitecturePort {
            attribute sourceName = "SCANENABLE";
            attribute sourceDetails = "Scan Test Mode Enbl";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        in port SCANINHCLK : ArchitecturePort {
            attribute sourceName = "SCANINHCLK";
            attribute sourceDetails = "Scan Chain Input";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port SCANOUTHCLK : ArchitecturePort {
            attribute sourceName = "SCANOUTHCLK";
            attribute sourceDetails = "Scan Chain Output";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port HSEL : ArchitecturePort {
            attribute sourceName = "HSEL";
            attribute sourceDetails = "0 AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port HADDR : ArchitecturePort {
            attribute sourceName = "HADDR";
            attribute sourceDetails = "[31:0] 0 AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port HTRANS : ArchitecturePort {
            attribute sourceName = "HTRANS";
            attribute sourceDetails = "[1:0] 0 AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port HWRITE : ArchitecturePort {
            attribute sourceName = "HWRITE";
            attribute sourceDetails = "0 AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port HSIZE : ArchitecturePort {
            attribute sourceName = "HSIZE";
            attribute sourceDetails = "[2:0] 0 AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port HBURST : ArchitecturePort {
            attribute sourceName = "HBURST";
            attribute sourceDetails = "[2:0] 0 AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port HPROT : ArchitecturePort {
            attribute sourceName = "HPROT";
            attribute sourceDetails = "[3:0] 0 AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port HWDATA : ArchitecturePort {
            attribute sourceName = "HWDATA";
            attribute sourceDetails = "[31:0] 0 AHB Protocol signals 81";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "81";
        }
        out port HBUSREQ : ArchitecturePort {
            attribute sourceName = "HBUSREQ";
            attribute sourceDetails = "0 AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port HLOCK : ArchitecturePort {
            attribute sourceName = "HLOCK";
            attribute sourceDetails = "0 AHB Protocol signals";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_bio_clock_div : ArchitecturePort {
            attribute sourceName = "o_bio_clock_div";
            attribute sourceDetails = "0 output for clock chopper";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_BIDAC : ArchitecturePort {
            attribute sourceName = "o_BIDAC";
            attribute sourceDetails = "[IDAC_offset-1:0] 0 IDAC for top";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_rst_imp : ArchitecturePort {
            attribute sourceName = "o_rst_imp";
            attribute sourceDetails = "1 bia start up rst signal";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_rsti_imp : ArchitecturePort {
            attribute sourceName = "o_rsti_imp";
            attribute sourceDetails = "1 bia start up rsti signal";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_sug_imp : ArchitecturePort {
            attribute sourceName = "o_sug_imp";
            attribute sourceDetails = "1 bia start up sug channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_pd_imp : ArchitecturePort {
            attribute sourceName = "o_pd_imp";
            attribute sourceDetails = "1 bia start up pd channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_start_operative_16MHz : ArchitecturePort {
            attribute sourceName = "o_start_operative_16MHz";
            attribute sourceDetails = "0 start operative 16MHz";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_su_hc2 : ArchitecturePort {
            attribute sourceName = "o_su_hc2";
            attribute sourceDetails = "1 ecg start up hc2 signal";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_rst_hc2 : ArchitecturePort {
            attribute sourceName = "o_rst_hc2";
            attribute sourceDetails = "1 ecg start up rst signal";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_rsti_hc2 : ArchitecturePort {
            attribute sourceName = "o_rsti_hc2";
            attribute sourceDetails = "1 ecg start up rsti signal";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_pd_hc2 : ArchitecturePort {
            attribute sourceName = "o_pd_hc2";
            attribute sourceDetails = "1 ecg start up pd signal";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_reset_reg_rst : ArchitecturePort {
            attribute sourceName = "o_reset_reg_rst";
            attribute sourceDetails = "1 end of reset async phase";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_reset_reg_rst_imp_async : ArchitecturePort {
            attribute sourceName = "o_reset_reg_rst_imp_async";
            attribute sourceDetails = "1 end of reset async phase";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_imp_curinj_pd : ArchitecturePort {
            attribute sourceName = "o_imp_curinj_pd";
            attribute sourceDetails = "0 bia current injection output";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_Txi_IDAC_Vref : ArchitecturePort {
            attribute sourceName = "o_Txi_IDAC_Vref";
            attribute sourceDetails = "[Nmax_bit_top-1:0] 0 TX IDAC VREF TO analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_comp_rx_ck : ArchitecturePort {
            attribute sourceName = "o_comp_rx_ck";
            attribute sourceDetails = "0 output for comparator debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_BTIA_gain : ArchitecturePort {
            attribute sourceName = "o_BTIA_gain";
            attribute sourceDetails = "[gain_max_bit_top-1:0] 0 BTIA gain output to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_data_out_debug_adc : ArchitecturePort {
            attribute sourceName = "o_data_out_debug_adc";
            attribute sourceDetails = "[15:0] 0 o data output for adc debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_en_mask_ldo_pdclkf_reg : ArchitecturePort {
            attribute sourceName = "o_en_mask_ldo_pdclkf_reg";
            attribute sourceDetails = "1 mask for en_ldo and pdf";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_pd_clkf : ArchitecturePort {
            attribute sourceName = "o_pd_clkf";
            attribute sourceDetails = "1 pd_clkf";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_trim_ldo_d : ArchitecturePort {
            attribute sourceName = "o_trim_ldo_d";
            attribute sourceDetails = "[1:0] 3 trim ldo value";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_BDC_PPG : ArchitecturePort {
            attribute sourceName = "o_BDC_PPG";
            attribute sourceDetails = "[idac_dc_ppg_frame_bit_top-1:0] 0 idac dc ppg frame output 82";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "82";
        }
        out port o_adc_mux_bio_channel : ArchitecturePort {
            attribute sourceName = "o_adc_mux_bio_channel";
            attribute sourceDetails = "[2:0] 0 adc mux bio channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_adc_mux_sel : ArchitecturePort {
            attribute sourceName = "o_adc_mux_sel";
            attribute sourceDetails = "0 adc mux sel output";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_error_time_slot : ArchitecturePort {
            attribute sourceName = "o_error_time_slot";
            attribute sourceDetails = "0 error time slot irq";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_curr_sel_tx_frame_x : ArchitecturePort {
            attribute sourceName = "o_curr_sel_tx_frame_x";
            attribute sourceDetails = "[curr_sel_bit_top-1:0] 0 current selection for tx channel output";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_tx1_outlab_sel_frame_x : ArchitecturePort {
            attribute sourceName = "o_tx1_outlab_sel_frame_x";
            attribute sourceDetails = "[bit_outab_sel_top-1:0] 0 tx outlab sel frame x";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_tx2_outlab_sel_frame_x : ArchitecturePort {
            attribute sourceName = "o_tx2_outlab_sel_frame_x";
            attribute sourceDetails = "[bit_outab_sel_top-1:0] 0 tx outlab sel frame x";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_tx3_outlab_sel_frame_x : ArchitecturePort {
            attribute sourceName = "o_tx3_outlab_sel_frame_x";
            attribute sourceDetails = "[bit_outab_sel_top-1:0] 0 tx outlab sel frame x";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_tx4_outlab_sel_frame_x : ArchitecturePort {
            attribute sourceName = "o_tx4_outlab_sel_frame_x";
            attribute sourceDetails = "[bit_outab_sel_top-1:0] 0 tx outlab sel frame x";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_tx_preset : ArchitecturePort {
            attribute sourceName = "o_tx_preset";
            attribute sourceDetails = "0 tx prese to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_en_tx : ArchitecturePort {
            attribute sourceName = "o_en_tx";
            attribute sourceDetails = "[n_tx_channel-1:0] 0 tx enable to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_PD_TIA : ArchitecturePort {
            attribute sourceName = "o_PD_TIA";
            attribute sourceDetails = "1 enabling tia to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_PD_PGA : ArchitecturePort {
            attribute sourceName = "o_PD_PGA";
            attribute sourceDetails = "1 enabling buffer to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_PD_IDAC : ArchitecturePort {
            attribute sourceName = "o_PD_IDAC";
            attribute sourceDetails = "1 enabling idac to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_gsr_curr_on : ArchitecturePort {
            attribute sourceName = "o_gsr_curr_on";
            attribute sourceDetails = "0 gsr curr on pilot to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_gsr_on : ArchitecturePort {
            attribute sourceName = "o_gsr_on";
            attribute sourceDetails = "0 grs on on pilot to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_ADC_en : ArchitecturePort {
            attribute sourceName = "o_ADC_en";
            attribute sourceDetails = "0 ADC enabling";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_half_charge_ldo : ArchitecturePort {
            attribute sourceName = "o_half_charge_ldo";
            attribute sourceDetails = "0";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_ADC_start : ArchitecturePort {
            attribute sourceName = "o_ADC_start";
            attribute sourceDetails = "0 ADC Start sampling";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_N_step2_to_reg : ArchitecturePort {
            attribute sourceName = "o_N_step2_to_reg";
            attribute sourceDetails = "[rx_ch_gain_limit-1:0] 0 N_Step2 calibration value";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_adc_test_cap : ArchitecturePort {
            attribute sourceName = "o_adc_test_cap";
            attribute sourceDetails = "[9:0] 0 adc test cap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_adc_error_cap9 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap9";
            attribute sourceDetails = "[7:0] 0 adc calibration result";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_adc_error_cap8 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap8";
            attribute sourceDetails = "[6:0] 0 adc calibration result";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_adc_error_cap7 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap7";
            attribute sourceDetails = "[6:0] 0 adc calibration result";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_adc_error_cap6 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap6";
            attribute sourceDetails = "[6:0] 0 adc calibration result 83";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "83";
        }
        out port o_adc_error_cap5 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap5";
            attribute sourceDetails = "[6:0] 0 adc calibration result";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_adc_error_cap4 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap4";
            attribute sourceDetails = "[6:0] 0 adc calibration result";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_adc_error_cap3 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap3";
            attribute sourceDetails = "[6:0] 0 adc calibration result";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_adc_error_cap2 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap2";
            attribute sourceDetails = "[6:0] 0 adc calibration result";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_adc_error_cap1 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap1";
            attribute sourceDetails = "[6:0] 0 adc calibration result";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_adc_error_cap0 : ArchitecturePort {
            attribute sourceName = "o_adc_error_cap0";
            attribute sourceDetails = "[6:0] 0 adc calibration result";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_pd_cm_buf : ArchitecturePort {
            attribute sourceName = "o_pd_cm_buf";
            attribute sourceDetails = "1 power down common buffer";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_pd_rld : ArchitecturePort {
            attribute sourceName = "o_pd_rld";
            attribute sourceDetails = "1 power down rld";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_pd_avg1 : ArchitecturePort {
            attribute sourceName = "o_pd_avg1";
            attribute sourceDetails = "1 power down avg1";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_pd_avg2 : ArchitecturePort {
            attribute sourceName = "o_pd_avg2";
            attribute sourceDetails = "1 power down avg2";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_mc_ahb_clk_en : ArchitecturePort {
            attribute sourceName = "o_mc_ahb_clk_en";
            attribute sourceDetails = "0 enable for master ahb clock";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_main_controller_device_status_register : ArchitecturePort {
            attribute sourceName = "o_main_controller_device_status_register";
            attribute sourceDetails = "[2:0] 0 device status register";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_main_controller_elab_status_register : ArchitecturePort {
            attribute sourceName = "o_main_controller_elab_status_register";
            attribute sourceDetails = "[3:0] 0 device status register";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_en_ldo_1v8 : ArchitecturePort {
            attribute sourceName = "o_en_ldo_1v8";
            attribute sourceDetails = "0 enable ldo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_en_bufxbio : ArchitecturePort {
            attribute sourceName = "o_en_bufxbio";
            attribute sourceDetails = "0 enable biobuffer to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_rx_ch_frame : ArchitecturePort {
            attribute sourceName = "o_rx_ch_frame";
            attribute sourceDetails = "[ppg_rx_channel_bit_top-1:0] 0 selected rx ch frame to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_ldo_ext : ArchitecturePort {
            attribute sourceName = "o_ldo_ext";
            attribute sourceDetails = "0 enable external ldo";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_ppg_status_register : ArchitecturePort {
            attribute sourceName = "o_ppg_status_register";
            attribute sourceDetails = "[n_state_bit-1:0] 0 ppg state status register";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_b_cap_idac : ArchitecturePort {
            attribute sourceName = "o_b_cap_idac";
            attribute sourceDetails = "[1:0] 0 b cap idac to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_ispu_irq_ctrl : ArchitecturePort {
            attribute sourceName = "o_ispu_irq_ctrl";
            attribute sourceDetails = "[3:0] 0 ispu irq";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_irq_start_measurement : ArchitecturePort {
            attribute sourceName = "o_irq_start_measurement";
            attribute sourceDetails = "0 irq start measurement to GPIO";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_end_calibration : ArchitecturePort {
            attribute sourceName = "o_end_calibration";
            attribute sourceDetails = "1 end calibration to analog domain";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_alc_data : ArchitecturePort {
            attribute sourceName = "o_alc_data";
            attribute sourceDetails = "[data_out_size_bit_top+2:0] 0 alc data to regmap";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_ppg_data_raw : ArchitecturePort {
            attribute sourceName = "o_ppg_data_raw";
            attribute sourceDetails = "[data_out_size_bit_top+2:0] 0 ppg raw data to regmap 84";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "84";
        }
        out port o_pd_buf_gpio1 : ArchitecturePort {
            attribute sourceName = "o_pd_buf_gpio1";
            attribute sourceDetails = "1 power down for buffer gpio1";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_pd_buf_gpio2 : ArchitecturePort {
            attribute sourceName = "o_pd_buf_gpio2";
            attribute sourceDetails = "1 power down for buffer gpio2";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_adc_data_debug_alc_1 : ArchitecturePort {
            attribute sourceName = "o_adc_data_debug_alc_1";
            attribute sourceDetails = "[frame_ppg_debug_alc_top-1:0] 0 alc 1 registers data debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_adc_data_debug_alc_2 : ArchitecturePort {
            attribute sourceName = "o_adc_data_debug_alc_2";
            attribute sourceDetails = "[frame_ppg_debug_alc_top-1:0] 0 alc 2 registers data debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_adc_data_debug_ppg_raw : ArchitecturePort {
            attribute sourceName = "o_adc_data_debug_ppg_raw";
            attribute sourceDetails = "[frame_ppg_debug_ppg_raw_top- 1:0] 0 ppg raw registers data debug";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_en_lead_off : ArchitecturePort {
            attribute sourceName = "o_en_lead_off";
            attribute sourceDetails = "0 mask lead off";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_mc_busy : ArchitecturePort {
            attribute sourceName = "o_mc_busy";
            attribute sourceDetails = "0 main controller is working";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_en_ck_m_p_q : ArchitecturePort {
            attribute sourceName = "o_en_ck_m_p_q";
            attribute sourceDetails = "0 clock m and q bia";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_en_ck_chop_imp : ArchitecturePort {
            attribute sourceName = "o_en_ck_chop_imp";
            attribute sourceDetails = "0 clock chopper bia";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_saturation_flag : ArchitecturePort {
            attribute sourceName = "o_saturation_flag";
            attribute sourceDetails = "[n_max_frame-1:0] 0 ppg saturation flag";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_en_ck_hc2_10k : ArchitecturePort {
            attribute sourceName = "o_en_ck_hc2_10k";
            attribute sourceDetails = "0 clock chipper ecg";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_en_clk_16MHz_sleep : ArchitecturePort {
            attribute sourceName = "o_en_clk_16MHz_sleep";
            attribute sourceDetails = "1 sleep signal for pmu";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }
        out port o_gsr_clk_en_16M : ArchitecturePort {
            attribute sourceName = "o_gsr_clk_en_16M";
            attribute sourceDetails = "0 enable clock for gsr channel";
            attribute sourceTable = "Main Controller I/O List";
            attribute sourcePage = "85";
        }

        requirement def IPOS_MAIN_CONTROLLER_001 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0117";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-001";
            doc /* During the Configuration Phase (IDLE STATE of the Device_FSM), the user shall be able to: • Configure Bio-Channel or Optical Channel, the ADC Calibration and then Start a measurement cycle. • Put the device in Debug-Mode. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_001 : IPOS_MAIN_CONTROLLER_001;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-001 | sourceReqId=DDS_STBIO1_0117 | During the Configuration Phase (IDLE STATE of the Device_FSM), the user shall be able to: • Configure Bio-Channel or Optical Channel, the ADC Calibration and then Start a measurement cycle. • Put the device in Debug-Mode. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-001 -> approved source requirement DDS_STBIO1_0117 */;
        satisfy req_IPOS_MAIN_CONTROLLER_001 by self;
        requirement def IPOS_MAIN_CONTROLLER_002 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0118";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-002";
            doc /* • The user shall configure time slot duration in DEVICE_CONFIG_OPERATION register [4:2] [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_002 : IPOS_MAIN_CONTROLLER_002;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-002 | sourceReqId=DDS_STBIO1_0118 | • The user shall configure time slot duration in DEVICE_CONFIG_OPERATION register [4:2] [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-002 -> approved source requirement DDS_STBIO1_0118 */;
        satisfy req_IPOS_MAIN_CONTROLLER_002 by self;
        requirement def IPOS_MAIN_CONTROLLER_003 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0119";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-003";
            doc /* • The user shall select active channel, in this case only ECG0_SEL and DS_SEL (Data Storage Mode) in DEVICE_CONFIG_CHANNEL register writing 0x21. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_003 : IPOS_MAIN_CONTROLLER_003;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-003 | sourceReqId=DDS_STBIO1_0119 | • The user shall select active channel, in this case only ECG0_SEL and DS_SEL (Data Storage Mode) in DEVICE_CONFIG_CHANNEL register writing 0x21. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-003 -> approved source requirement DDS_STBIO1_0119 */;
        satisfy req_IPOS_MAIN_CONTROLLER_003 by self;
        requirement def IPOS_MAIN_CONTROLLER_004 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0120";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-004";
            doc /* • The user shall select a division index for ECG, configuring M_ECG_l and M_ECG_h in SET_ECG_FREQ_l register and SET_ECG_FREQ_h register. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_004 : IPOS_MAIN_CONTROLLER_004;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-004 | sourceReqId=DDS_STBIO1_0120 | • The user shall select a division index for ECG, configuring M_ECG_l and M_ECG_h in SET_ECG_FREQ_l register and SET_ECG_FREQ_h register. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-004 -> approved source requirement DDS_STBIO1_0120 */;
        satisfy req_IPOS_MAIN_CONTROLLER_004 by self;
        requirement def IPOS_MAIN_CONTROLLER_005 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0121";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-005";
            doc /* • The user shall set the number of clocks for sampling ECG data from ADC in ADC_CONFIG_ECG register. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_005 : IPOS_MAIN_CONTROLLER_005;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-005 | sourceReqId=DDS_STBIO1_0121 | • The user shall set the number of clocks for sampling ECG data from ADC in ADC_CONFIG_ECG register. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-005 -> approved source requirement DDS_STBIO1_0121 */;
        satisfy req_IPOS_MAIN_CONTROLLER_005 by self;
        requirement def IPOS_MAIN_CONTROLLER_006 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0122";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-006";
            doc /* • The User shall set at 1 HC_EN in ECG_CTRL register. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_006 : IPOS_MAIN_CONTROLLER_006;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-006 | sourceReqId=DDS_STBIO1_0122 | • The User shall set at 1 HC_EN in ECG_CTRL register. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-006 -> approved source requirement DDS_STBIO1_0122 */;
        satisfy req_IPOS_MAIN_CONTROLLER_006 by self;
        requirement def IPOS_MAIN_CONTROLLER_007 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0123";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-007";
            doc /* • The user shall start measurement writing register DEVICE_CONFIG_OPERATION [0] at 1. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_007 : IPOS_MAIN_CONTROLLER_007;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-007 | sourceReqId=DDS_STBIO1_0123 | • The user shall start measurement writing register DEVICE_CONFIG_OPERATION [0] at 1. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-007 -> approved source requirement DDS_STBIO1_0123 */;
        satisfy req_IPOS_MAIN_CONTROLLER_007 by self;
        requirement def IPOS_MAIN_CONTROLLER_008 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0124";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-008";
            doc /* • To check data in unique FIFO (default config) the user shall check the first MSB which will have to be equal to the table in DATA TAG Table. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_008 : IPOS_MAIN_CONTROLLER_008;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-008 | sourceReqId=DDS_STBIO1_0124 | • To check data in unique FIFO (default config) the user shall check the first MSB which will have to be equal to the table in DATA TAG Table. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-008 -> approved source requirement DDS_STBIO1_0124 */;
        satisfy req_IPOS_MAIN_CONTROLLER_008 by self;
        requirement def IPOS_MAIN_CONTROLLER_009 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0125";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-009";
            doc /* [DDS_STBIO1_0125] Requirement: • The user shall configure the time slot duration in DEVICE_CONFIG_OPERATION register [4:2]. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_009 : IPOS_MAIN_CONTROLLER_009;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-009 | sourceReqId=DDS_STBIO1_0125 | [DDS_STBIO1_0125] Requirement: • The user shall configure the time slot duration in DEVICE_CONFIG_OPERATION register [4:2]. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-009 -> approved source requirement DDS_STBIO1_0125 */;
        satisfy req_IPOS_MAIN_CONTROLLER_009 by self;
        requirement def IPOS_MAIN_CONTROLLER_010 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0126";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-010";
            doc /* • The user shall select active channel, in this case ECG0_SEL, BIA_SEL and DS_SEL (Data Storage Mode) in DEVICE_CONFIG_CHANNEL writing 0x23. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_010 : IPOS_MAIN_CONTROLLER_010;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-010 | sourceReqId=DDS_STBIO1_0126 | • The user shall select active channel, in this case ECG0_SEL, BIA_SEL and DS_SEL (Data Storage Mode) in DEVICE_CONFIG_CHANNEL writing 0x23. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-010 -> approved source requirement DDS_STBIO1_0126 */;
        satisfy req_IPOS_MAIN_CONTROLLER_010 by self;
        requirement def IPOS_MAIN_CONTROLLER_011 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0127";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-011";
            doc /* • The user shall select a division index for ECG, configuring M_ECG_l and M_ECG_h in SET_ECG_FREQ_l register and SET_ECG_FREQ_h register. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_011 : IPOS_MAIN_CONTROLLER_011;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-011 | sourceReqId=DDS_STBIO1_0127 | • The user shall select a division index for ECG, configuring M_ECG_l and M_ECG_h in SET_ECG_FREQ_l register and SET_ECG_FREQ_h register. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-011 -> approved source requirement DDS_STBIO1_0127 */;
        satisfy req_IPOS_MAIN_CONTROLLER_011 by self;
        requirement def IPOS_MAIN_CONTROLLER_012 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0128";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-012";
            doc /* • The user shall select a division index for ECG, configuring M_BIA_l and M_BIA_h in SET_BIA_FREQ_l register and SET_BIA_FREQ_h register. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_012 : IPOS_MAIN_CONTROLLER_012;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-012 | sourceReqId=DDS_STBIO1_0128 | • The user shall select a division index for ECG, configuring M_BIA_l and M_BIA_h in SET_BIA_FREQ_l register and SET_BIA_FREQ_h register. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-012 -> approved source requirement DDS_STBIO1_0128 */;
        satisfy req_IPOS_MAIN_CONTROLLER_012 by self;
        requirement def IPOS_MAIN_CONTROLLER_013 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0129";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-013";
            doc /* • The user shall set number of clocks for sampling ECG and BIA data from ADC in ADC_CONFIG_ECG register. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_013 : IPOS_MAIN_CONTROLLER_013;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-013 | sourceReqId=DDS_STBIO1_0129 | • The user shall set number of clocks for sampling ECG and BIA data from ADC in ADC_CONFIG_ECG register. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-013 -> approved source requirement DDS_STBIO1_0129 */;
        satisfy req_IPOS_MAIN_CONTROLLER_013 by self;
        requirement def IPOS_MAIN_CONTROLLER_014 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0130";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-014";
            doc /* • The user shall set at 1 HC_EN in ECG_CTRL register. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_014 : IPOS_MAIN_CONTROLLER_014;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-014 | sourceReqId=DDS_STBIO1_0130 | • The user shall set at 1 HC_EN in ECG_CTRL register. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-014 -> approved source requirement DDS_STBIO1_0130 */;
        satisfy req_IPOS_MAIN_CONTROLLER_014 by self;
        requirement def IPOS_MAIN_CONTROLLER_015 : SourceRequirement {
            attribute sourceReqId = "DDS_STBIO1_0140";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-015";
            doc /* • The user shall set at 1 IMP_EN in IMP_CTRL register. [TO: IPOS_MAIN_CTRL] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_015 : IPOS_MAIN_CONTROLLER_015;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-015 | sourceReqId=DDS_STBIO1_0140 | • The user shall set at 1 IMP_EN in IMP_CTRL register. [TO: IPOS_MAIN_CTRL] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-015 -> approved source requirement DDS_STBIO1_0140 */;
        satisfy req_IPOS_MAIN_CONTROLLER_015 by self;
        requirement def IPOS_MAIN_CONTROLLER_016 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_002";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-016";
            doc /* The only registers that the user shall change after setting the mode_operation to 1 are the ones described in requirement 7096. All the Other signals shall change only with mode_operation set */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_016 : IPOS_MAIN_CONTROLLER_016;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-016 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_002 | The only registers that the user shall change after setting the mode_operation to 1 are the ones described in requirement 7096. All the Other signals shall change only with mode_operation set */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-016 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_002 */;
        satisfy req_IPOS_MAIN_CONTROLLER_016 by self;
        requirement def IPOS_MAIN_CONTROLLER_017 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_004";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-017";
            doc /* [Covers: DDS_STBIO1_0116] When the Device_FSM FSM is in BOOT State, that is DEVICE_STATUS_REG register [2:0]) == 0x01 (main_controller_status_register), it shall wait that the ADSP ends the BOOT Phase, checking when the i_quokka_boot_end is set high. When the BOOT Phase is ended, the Device_FSM FSM shall go to IDLE State, check that DEVICE_STATUS_REG register [2:0]) == 0x02, (main_controller_status_register), check that the w_en_ldo1v8 signal is set low and that */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_017 : IPOS_MAIN_CONTROLLER_017;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-017 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_004 | [Covers: DDS_STBIO1_0116] When the Device_FSM FSM is in BOOT State, that is DEVICE_STATUS_REG register [2:0]) == 0x01 (main_controller_status_register), it shall wait that the ADSP ends the BOOT Phase, checking when the i_quokka_boot_end is set high. When the BOOT Phase is ended, the Device_FSM FSM shall go to IDLE State, check that DEVICE_STATUS_REG register [2:0]) == 0x02, (main_controller_status_register), check that the w_en_ldo1v8 signal is set low and that */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-017 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_004 */;
        satisfy req_IPOS_MAIN_CONTROLLER_017 by self;
        requirement def IPOS_MAIN_CONTROLLER_018 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_008";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-018";
            doc /* When in unique_fifo_mode (i_multiple_fifo set to 0), if during a time slot an operation is done, the Main_Controller_FSM shall write the time_slot_data inside the FIFO with a dedicated tag. The value of the time_slot_data shall be referred to the start of the entire measurement cycle (for */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_018 : IPOS_MAIN_CONTROLLER_018;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-018 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_008 | When in unique_fifo_mode (i_multiple_fifo set to 0), if during a time slot an operation is done, the Main_Controller_FSM shall write the time_slot_data inside the FIFO with a dedicated tag. The value of the time_slot_data shall be referred to the start of the entire measurement cycle (for */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-018 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_008 */;
        satisfy req_IPOS_MAIN_CONTROLLER_018 by self;
        requirement def IPOS_MAIN_CONTROLLER_019 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_009";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-019";
            doc /* [Covers: DDS_STBIO1_0123] [Covers: DDS_STBIO1_0141] When in IDLE State, if ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is high, or BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is set high, or ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL register [1]) is set high, or GSR_SEL (DEVICE_CONFIG_CHANNEL register [3]) is set high, or ADC_DO_CALIBRATION ( ADC_CAL_CONFIG register [0]) is set high, or WAVE_VELOCITY_MODE (GENERAL_PPG_PARAMETERS_1 register [4]) is set high together wit h PPG_SEL (DEVICE_CONFIG_CHANNEL register [4]), when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_CLKF shall go */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_019 : IPOS_MAIN_CONTROLLER_019;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-019 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_009 | [Covers: DDS_STBIO1_0123] [Covers: DDS_STBIO1_0141] When in IDLE State, if ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is high, or BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is set high, or ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL register [1]) is set high, or GSR_SEL (DEVICE_CONFIG_CHANNEL register [3]) is set high, or ADC_DO_CALIBRATION ( ADC_CAL_CONFIG register [0]) is set high, or WAVE_VELOCITY_MODE (GENERAL_PPG_PARAMETERS_1 register [4]) is set high together wit h PPG_SEL (DEVICE_CONFIG_CHANNEL register [4]), when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_CLKF shall go */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-019 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_009 */;
        satisfy req_IPOS_MAIN_CONTROLLER_019 by self;
        requirement def IPOS_MAIN_CONTROLLER_020 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_010";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-020";
            doc /* [Covers: DDS_STBIO1_0119] When the FSM is in IDLE State, if ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is high, HC_EN (ECG_CTRL register [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 0, ECG0 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall go low and the Device_FSM FSM shall go to the WAIT_SU State , so the main_controller_status_register (DEVICE_STATUS_REG register */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_020 : IPOS_MAIN_CONTROLLER_020;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-020 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_010 | [Covers: DDS_STBIO1_0119] When the FSM is in IDLE State, if ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is high, HC_EN (ECG_CTRL register [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 0, ECG0 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall go low and the Device_FSM FSM shall go to the WAIT_SU State , so the main_controller_status_register (DEVICE_STATUS_REG register */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-020 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_010 */;
        satisfy req_IPOS_MAIN_CONTROLLER_020 by self;
        requirement def IPOS_MAIN_CONTROLLER_021 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_011";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-021";
            doc /* When the HC_EN (ECG_CTRL register [0]) is set to 0 and IMP_EN (IMP_CTRL register [0]) is set to 1 and ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL register [1]) is set to 1, ECG1 and ECG2 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall remain high, O_PD_IMP shall go low and the Device_FSM shall go to the WAIT_SU State, so main_controller_status_register */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_021 : IPOS_MAIN_CONTROLLER_021;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-021 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_011 | When the HC_EN (ECG_CTRL register [0]) is set to 0 and IMP_EN (IMP_CTRL register [0]) is set to 1 and ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL register [1]) is set to 1, ECG1 and ECG2 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall remain high, O_PD_IMP shall go low and the Device_FSM shall go to the WAIT_SU State, so main_controller_status_register */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-021 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_011 */;
        satisfy req_IPOS_MAIN_CONTROLLER_021 by self;
        requirement def IPOS_MAIN_CONTROLLER_022 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_0152";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-022";
            doc /* If the calibration has been done, the ADC_error_caps values computed shall reset only if the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_022 : IPOS_MAIN_CONTROLLER_022;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-022 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_0152 | If the calibration has been done, the ADC_error_caps values computed shall reset only if the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-022 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_0152 */;
        satisfy req_IPOS_MAIN_CONTROLLER_022 by self;
        requirement def IPOS_MAIN_CONTROLLER_023 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_016";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-023";
            doc /* When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL [2]) is equal to 1, O_PD_IMP shall go low within 5 clock cycle at */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_023 : IPOS_MAIN_CONTROLLER_023;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-023 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_016 | When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL [2]) is equal to 1, O_PD_IMP shall go low within 5 clock cycle at */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-023 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_016 */;
        satisfy req_IPOS_MAIN_CONTROLLER_023 by self;
        requirement def IPOS_MAIN_CONTROLLER_024 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_017";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-024";
            doc /* When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1 and the IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 1, the O_IMP_CURINJ_PD shall go low. On the other hand, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 0, the O_IMP_CURINJ_PD shall remain */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_024 : IPOS_MAIN_CONTROLLER_024;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-024 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_017 | When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1 and the IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 1, the O_IMP_CURINJ_PD shall go low. On the other hand, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 0, the O_IMP_CURINJ_PD shall remain */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-024 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_017 */;
        satisfy req_IPOS_MAIN_CONTROLLER_024 by self;
        requirement def IPOS_MAIN_CONTROLLER_025 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_018";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-025";
            doc /* When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) signal is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1, 5ms after the falling of imp_curinj_pd and O_PD_IMP, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 1, O_CK_M, O_CK_P and O_CK_Q shall be generated from Clock generator block so they run at FREQ_BIA_CLK_m_p_q (EN_CHOP_FREQ_MOD_DEMOD register [4:3] ) and its values shall be chosen from 20kHz, 50kHz, 100kHz, 200kHz . On the other hand, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 0, ck_m, ck_p and */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_025 : IPOS_MAIN_CONTROLLER_025;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-025 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_018 | When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) signal is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1, 5ms after the falling of imp_curinj_pd and O_PD_IMP, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 1, O_CK_M, O_CK_P and O_CK_Q shall be generated from Clock generator block so they run at FREQ_BIA_CLK_m_p_q (EN_CHOP_FREQ_MOD_DEMOD register [4:3] ) and its values shall be chosen from 20kHz, 50kHz, 100kHz, 200kHz . On the other hand, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 0, ck_m, ck_p and */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-025 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_018 */;
        satisfy req_IPOS_MAIN_CONTROLLER_025 by self;
        requirement def IPOS_MAIN_CONTROLLER_026 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_019";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-026";
            doc /* When IMP_CURRINJ_EN (CURR_INJ register [3]) is high, O_CK_Q shall be run with a phase */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_026 : IPOS_MAIN_CONTROLLER_026;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-026 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_019 | When IMP_CURRINJ_EN (CURR_INJ register [3]) is high, O_CK_Q shall be run with a phase */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-026 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_019 */;
        satisfy req_IPOS_MAIN_CONTROLLER_026 by self;
        requirement def IPOS_MAIN_CONTROLLER_027 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_021";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-027";
            doc /* When DEVICE_FSM FSM is in WAIT_SU state, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1; 20ms after the falling of O_RST_IMP, if EN_CHOP_CLK_IMP (EN_CHOP_FREQ_MOD_DEMOD register [1]) is set to 1, O_CK_CHOP_IMP shall be generated from Clock generator block, so O_CK_CHOP_IMP shall be run at 10kHz frequency. On the other hand, if EN_CHOP_CLK_IMP (EN_CHOP_FREQ_MOD_DEMOD register [1]) is set */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_027 : IPOS_MAIN_CONTROLLER_027;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-027 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_021 | When DEVICE_FSM FSM is in WAIT_SU state, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1; 20ms after the falling of O_RST_IMP, if EN_CHOP_CLK_IMP (EN_CHOP_FREQ_MOD_DEMOD register [1]) is set to 1, O_CK_CHOP_IMP shall be generated from Clock generator block, so O_CK_CHOP_IMP shall be run at 10kHz frequency. On the other hand, if EN_CHOP_CLK_IMP (EN_CHOP_FREQ_MOD_DEMOD register [1]) is set */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-027 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_021 */;
        satisfy req_IPOS_MAIN_CONTROLLER_027 by self;
        requirement def IPOS_MAIN_CONTROLLER_028 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_023";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-028";
            doc /* When DEVICE_FSM FSM is in WAIT_SU state, if IMP_EN signal (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1; If i_su_hlt_dly is set to 0, 205ms after the falling of O_RSTI_IMP, O_SUG_IMP shall go low. Instead, if SU_DLY (EN_CHOP_FREQ_MOD_DEMOD register [2]) is set to 1, 755ms after the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_028 : IPOS_MAIN_CONTROLLER_028;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-028 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_023 | When DEVICE_FSM FSM is in WAIT_SU state, if IMP_EN signal (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1; If i_su_hlt_dly is set to 0, 205ms after the falling of O_RSTI_IMP, O_SUG_IMP shall go low. Instead, if SU_DLY (EN_CHOP_FREQ_MOD_DEMOD register [2]) is set to 1, 755ms after the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-028 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_023 */;
        satisfy req_IPOS_MAIN_CONTROLLER_028 by self;
        requirement def IPOS_MAIN_CONTROLLER_029 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_024";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-029";
            doc /* When DEVICE_FSM FSM is in WAIT_SU STATE ( main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x03) if HC_EN (ECG_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is set to 1 and MODE_OPERATION (bit [1:0] on DEVICE_CONFIG_OPERATION register) is different to 0, after WAIT_SU state the device shall go in OPERATIVE (DEVICE_STATUS_REG register [2:0] is equal */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_029 : IPOS_MAIN_CONTROLLER_029;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-029 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_024 | When DEVICE_FSM FSM is in WAIT_SU STATE ( main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x03) if HC_EN (ECG_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is set to 1 and MODE_OPERATION (bit [1:0] on DEVICE_CONFIG_OPERATION register) is different to 0, after WAIT_SU state the device shall go in OPERATIVE (DEVICE_STATUS_REG register [2:0] is equal */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-029 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_024 */;
        satisfy req_IPOS_MAIN_CONTROLLER_029 by self;
        requirement def IPOS_MAIN_CONTROLLER_030 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_026";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-030";
            doc /* When DEVICE_FSM FSM is in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) if HC_EN (ECG_CTRL register [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL [0]) is set to 1 and ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL [1]) is set to 1, after WAIT_SU the device_fsm shall go in */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_030 : IPOS_MAIN_CONTROLLER_030;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-030 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_026 | When DEVICE_FSM FSM is in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) if HC_EN (ECG_CTRL register [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL [0]) is set to 1 and ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL [1]) is set to 1, after WAIT_SU the device_fsm shall go in */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-030 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_026 */;
        satisfy req_IPOS_MAIN_CONTROLLER_030 by self;
        requirement def IPOS_MAIN_CONTROLLER_031 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_028";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-031";
            doc /* When DEVICE_FSM FSM is in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) if HC_EN (ECG_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL [2]) is set to 1, after WAIT_SU, the device FSM shall go in OPERATIVE (DEVICE_STATUS_REG register [2:0] is equal to 0x04). */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_031 : IPOS_MAIN_CONTROLLER_031;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-031 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_028 | When DEVICE_FSM FSM is in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) if HC_EN (ECG_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL [2]) is set to 1, after WAIT_SU, the device FSM shall go in OPERATIVE (DEVICE_STATUS_REG register [2:0] is equal to 0x04). */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-031 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_028 */;
        satisfy req_IPOS_MAIN_CONTROLLER_031 by self;
        requirement def IPOS_MAIN_CONTROLLER_032 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_029";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-032";
            doc /* When DEVICE_FSM FSM is in IDLE if PPG_SEL (DEVICE_CONFIG_CHANNEL [4]) is set to 1 and MODE_OPERATION (bit [1:0] on DEVICE_CONFIG_OPERATION register) is different to 0, the device shall go in PPG state (main_controller_status_register in ELAB_STATUS_REG register */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_032 : IPOS_MAIN_CONTROLLER_032;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-032 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_029 | When DEVICE_FSM FSM is in IDLE if PPG_SEL (DEVICE_CONFIG_CHANNEL [4]) is set to 1 and MODE_OPERATION (bit [1:0] on DEVICE_CONFIG_OPERATION register) is different to 0, the device shall go in PPG state (main_controller_status_register in ELAB_STATUS_REG register */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-032 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_029 */;
        satisfy req_IPOS_MAIN_CONTROLLER_032 by self;
        requirement def IPOS_MAIN_CONTROLLER_033 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_030";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-033";
            doc /* When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) the device shall be execute a number of frames equal to N_PPG_FRAME (GENERAL_PPG_PARAMETERS_1 register [3:0]) (Check the i_id_frame shall increase until it’s equal to N_PPG_FRAME-1). At the beginning of each frame o_ADC_EN shall go high and it shall go low when ALC_COMPENSATION is performed or */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_033 : IPOS_MAIN_CONTROLLER_033;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-033 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_030 | When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) the device shall be execute a number of frames equal to N_PPG_FRAME (GENERAL_PPG_PARAMETERS_1 register [3:0]) (Check the i_id_frame shall increase until it’s equal to N_PPG_FRAME-1). At the beginning of each frame o_ADC_EN shall go high and it shall go low when ALC_COMPENSATION is performed or */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-033 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_030 */;
        satisfy req_IPOS_MAIN_CONTROLLER_033 by self;
        requirement def IPOS_MAIN_CONTROLLER_034 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_031";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-034";
            doc /* When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x 05) o_ADC_start shall go high a number of times equal “2 ^ value indicated in regmap of FRAME_{n}_SAMPLES (FRAME_n_PARAMETERS_1 register [5:3]) for ALC and PPG both (2*(2^regmap_value). Except when FRAME_{n}_SAMPLES is equal to 3’b000, in this case o_ADC_start shall go high 3 times. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_034 : IPOS_MAIN_CONTROLLER_034;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-034 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_031 | When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x 05) o_ADC_start shall go high a number of times equal “2 ^ value indicated in regmap of FRAME_{n}_SAMPLES (FRAME_n_PARAMETERS_1 register [5:3]) for ALC and PPG both (2*(2^regmap_value). Except when FRAME_{n}_SAMPLES is equal to 3’b000, in this case o_ADC_start shall go high 3 times. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-034 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_031 */;
        satisfy req_IPOS_MAIN_CONTROLLER_034 by self;
        requirement def IPOS_MAIN_CONTROLLER_035 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_032";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-035";
            doc /* When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) during each frame o_Txi_idac_VREF shall go from 0 to N_MAX (DIGITAL_RAMP_CONFIG_PARAM_1 register [3:0]). At first, o_Txi_idac_VREF shall be increase its value of N_START for next step o_Txi_idac_VREF shall */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_035 : IPOS_MAIN_CONTROLLER_035;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-035 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_032 | When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) during each frame o_Txi_idac_VREF shall go from 0 to N_MAX (DIGITAL_RAMP_CONFIG_PARAM_1 register [3:0]). At first, o_Txi_idac_VREF shall be increase its value of N_START for next step o_Txi_idac_VREF shall */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-035 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_032 */;
        satisfy req_IPOS_MAIN_CONTROLLER_035 by self;
        requirement def IPOS_MAIN_CONTROLLER_036 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_033";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-036";
            doc /* When not in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) , Device_FSM shall go back in IDLE only if the user turns off the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_036 : IPOS_MAIN_CONTROLLER_036;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-036 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_033 | When not in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) , Device_FSM shall go back in IDLE only if the user turns off the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-036 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_033 */;
        satisfy req_IPOS_MAIN_CONTROLLER_036 by self;
        requirement def IPOS_MAIN_CONTROLLER_037 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_034";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-037";
            doc /* When in OPERATIVE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02), if the time slot counter reach its limit, the Device_FSM shall go into the error state (DEVICE_STATUS_REGISTER) and raise an interrupt (o_error_time_slot) to the Digital_Top. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_037 : IPOS_MAIN_CONTROLLER_037;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-037 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_034 | When in OPERATIVE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02), if the time slot counter reach its limit, the Device_FSM shall go into the error state (DEVICE_STATUS_REGISTER) and raise an interrupt (o_error_time_slot) to the Digital_Top. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-037 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_034 */;
        satisfy req_IPOS_MAIN_CONTROLLER_037 by self;
        requirement def IPOS_MAIN_CONTROLLER_038 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_035";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-038";
            doc /* When DEVICE_FSM FSM is in Operative State (DEVICE_STATUS_REG register [2:0]==0x04), the o_MC_busy shall go to 1 and shall go to 0 one clock cycle after entering the SLEEP state if */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_038 : IPOS_MAIN_CONTROLLER_038;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-038 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_035 | When DEVICE_FSM FSM is in Operative State (DEVICE_STATUS_REG register [2:0]==0x04), the o_MC_busy shall go to 1 and shall go to 0 one clock cycle after entering the SLEEP state if */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-038 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_035 */;
        satisfy req_IPOS_MAIN_CONTROLLER_038 by self;
        requirement def IPOS_MAIN_CONTROLLER_039 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_036";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-039";
            doc /* When in Sleep Mode, the device shall go back to the Operative State if no error (o_error_irq stuck at 0) occurs and all the operations are ended . Furthermore, if no Bio -Channel operations are selected and more than 150us are left before the start of a new time slot, the o_pd_clkf (Digital */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_039 : IPOS_MAIN_CONTROLLER_039;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-039 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_036 | When in Sleep Mode, the device shall go back to the Operative State if no error (o_error_irq stuck at 0) occurs and all the operations are ended . Furthermore, if no Bio -Channel operations are selected and more than 150us are left before the start of a new time slot, the o_pd_clkf (Digital */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-039 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_036 */;
        satisfy req_IPOS_MAIN_CONTROLLER_039 by self;
        requirement def IPOS_MAIN_CONTROLLER_040 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_037";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-040";
            doc /* In a Time Slot, when a BIO-Channel operation is selected, o_en_bufxbio signal (in Digital Top) shall go high at least a configurable time (Device Config Operation [6:5]) before selecting the first */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_040 : IPOS_MAIN_CONTROLLER_040;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-040 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_037 | In a Time Slot, when a BIO-Channel operation is selected, o_en_bufxbio signal (in Digital Top) shall go high at least a configurable time (Device Config Operation [6:5]) before selecting the first */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-040 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_037 */;
        satisfy req_IPOS_MAIN_CONTROLLER_040 by self;
        requirement def IPOS_MAIN_CONTROLLER_041 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_038";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-041";
            doc /* When the ELAB_FSM is in ECG State, the ADC_Mux (concatenation of {o_adc_mux_sel, o_adc_mux_bio_channel} on digital top) output shall be set equal to 001 and after 4 acquisitions (described in section 5.4 ADC PHASE) shall be set to 010. If ECG1 and ECG2 are selected, the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_041 : IPOS_MAIN_CONTROLLER_041;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-041 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_038 | When the ELAB_FSM is in ECG State, the ADC_Mux (concatenation of {o_adc_mux_sel, o_adc_mux_bio_channel} on digital top) output shall be set equal to 001 and after 4 acquisitions (described in section 5.4 ADC PHASE) shall be set to 010. If ECG1 and ECG2 are selected, the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-041 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_038 */;
        satisfy req_IPOS_MAIN_CONTROLLER_041 by self;
        requirement def IPOS_MAIN_CONTROLLER_042 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_039";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-042";
            doc /* When ELAB FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) or a WAIT_END_OPERATIVE State, o_en_biobuffer shall */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_042 : IPOS_MAIN_CONTROLLER_042;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-042 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_039 | When ELAB FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) or a WAIT_END_OPERATIVE State, o_en_biobuffer shall */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-042 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_039 */;
        satisfy req_IPOS_MAIN_CONTROLLER_042 by self;
        requirement def IPOS_MAIN_CONTROLLER_043 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_044";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-043";
            doc /* When i_rstn is asserted low, all the output shall be set to 0, except for count_cap that shall be set */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_043 : IPOS_MAIN_CONTROLLER_043;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-043 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_044 | When i_rstn is asserted low, all the output shall be set to 0, except for count_cap that shall be set */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-043 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_044 */;
        satisfy req_IPOS_MAIN_CONTROLLER_043 by self;
        requirement def IPOS_MAIN_CONTROLLER_044 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_045";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-044";
            doc /* The o_adc_ready shall be set to 1 when the ADC is getting ready (o_adc_en is set to 1 but not */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_044 : IPOS_MAIN_CONTROLLER_044;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-044 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_045 | The o_adc_ready shall be set to 1 when the ADC is getting ready (o_adc_en is set to 1 but not */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-044 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_045 */;
        satisfy req_IPOS_MAIN_CONTROLLER_044 by self;
        requirement def IPOS_MAIN_CONTROLLER_045 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_047";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-045";
            doc /* When the calibration phase is ended, the o_end_cal_phase shall be set to 1 and shall stay high */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_045 : IPOS_MAIN_CONTROLLER_045;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-045 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_047 | When the calibration phase is ended, the o_end_cal_phase shall be set to 1 and shall stay high */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-045 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_047 */;
        satisfy req_IPOS_MAIN_CONTROLLER_045 by self;
        requirement def IPOS_MAIN_CONTROLLER_046 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_049";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-046";
            doc /* When ECG, BIA or GSR Is sampled, i_ADC_en is equal to 1, the o_ADC_clk_en shall be set to 1. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_046 : IPOS_MAIN_CONTROLLER_046;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-046 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_049 | When ECG, BIA or GSR Is sampled, i_ADC_en is equal to 1, the o_ADC_clk_en shall be set to 1. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-046 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_049 */;
        satisfy req_IPOS_MAIN_CONTROLLER_046 by self;
        requirement def IPOS_MAIN_CONTROLLER_047 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_051";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-047";
            doc /* [Covers: DDS_STBIO1_0121] [Covers: DDS_STBIO1_0129] The Sampling Phase shall be configurable by the user with i_N_clk values from 0 up to 63. This */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_047 : IPOS_MAIN_CONTROLLER_047;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-047 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_051 | [Covers: DDS_STBIO1_0121] [Covers: DDS_STBIO1_0129] The Sampling Phase shall be configurable by the user with i_N_clk values from 0 up to 63. This */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-047 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_051 */;
        satisfy req_IPOS_MAIN_CONTROLLER_047 by self;
        requirement def IPOS_MAIN_CONTROLLER_048 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_052";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-048";
            doc /* When the i_ADC_en_mc and i_adc_en_mask is set to 0, all the output shall be set to 0, except for the o_end_cal_phases and o_ADC_clk_en. The o_end_cal_phases shall be set to 1 if i_do_calibration (bit 0 of ADC_CAL_CONFIG) is set to 0, otherwise shall be set to 0 until the end */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_048 : IPOS_MAIN_CONTROLLER_048;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-048 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_052 | When the i_ADC_en_mc and i_adc_en_mask is set to 0, all the output shall be set to 0, except for the o_end_cal_phases and o_ADC_clk_en. The o_end_cal_phases shall be set to 1 if i_do_calibration (bit 0 of ADC_CAL_CONFIG) is set to 0, otherwise shall be set to 0 until the end */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-048 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_052 */;
        satisfy req_IPOS_MAIN_CONTROLLER_048 by self;
        requirement def IPOS_MAIN_CONTROLLER_049 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_053";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-049";
            doc /* When the i_ADC_en_mc and i_adc_en_mask is set to 1, at least 160 clock cycles shall pass before */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_049 : IPOS_MAIN_CONTROLLER_049;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-049 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_053 | When the i_ADC_en_mc and i_adc_en_mask is set to 1, at least 160 clock cycles shall pass before */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-049 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_053 */;
        satisfy req_IPOS_MAIN_CONTROLLER_049 by self;
        requirement def IPOS_MAIN_CONTROLLER_050 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_054";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-050";
            doc /* When the ADC_phases fsm is ready and an acquisition is required, the o_ADC_start shall stay */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_050 : IPOS_MAIN_CONTROLLER_050;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-050 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_054 | When the ADC_phases fsm is ready and an acquisition is required, the o_ADC_start shall stay */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-050 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_054 */;
        satisfy req_IPOS_MAIN_CONTROLLER_050 by self;
        requirement def IPOS_MAIN_CONTROLLER_051 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_055";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-051";
            doc /* After an acquisition is started, the ADC_Phases shall wait for the i_ADC_EOC sampling the new */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_051 : IPOS_MAIN_CONTROLLER_051;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-051 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_055 | After an acquisition is started, the ADC_Phases shall wait for the i_ADC_EOC sampling the new */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-051 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_055 */;
        satisfy req_IPOS_MAIN_CONTROLLER_051 by self;
        requirement def IPOS_MAIN_CONTROLLER_052 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_058";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-052";
            doc /* The calibration phase shall set the adc_error_cap8…0 to the correct value, following the calibration */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_052 : IPOS_MAIN_CONTROLLER_052;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-052 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_058 | The calibration phase shall set the adc_error_cap8…0 to the correct value, following the calibration */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-052 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_058 */;
        satisfy req_IPOS_MAIN_CONTROLLER_052 by self;
        requirement def IPOS_MAIN_CONTROLLER_053 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_059";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-053";
            doc /* If the i_noise signal is set to 1 when the DEVICE_FSM is into PPG State, the i_n_avarage shall */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_053 : IPOS_MAIN_CONTROLLER_053;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-053 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_059 | If the i_noise signal is set to 1 when the DEVICE_FSM is into PPG State, the i_n_avarage shall */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-053 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_059 */;
        satisfy req_IPOS_MAIN_CONTROLLER_053 by self;
        requirement def IPOS_MAIN_CONTROLLER_054 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_060";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-054";
            doc /* When the last acquisition is performed, after the last i_ADC_EOC arrived, the ADC_phases shall */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_054 : IPOS_MAIN_CONTROLLER_054;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-054 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_060 | When the last acquisition is performed, after the last i_ADC_EOC arrived, the ADC_phases shall */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-054 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_060 */;
        satisfy req_IPOS_MAIN_CONTROLLER_054 by self;
        requirement def IPOS_MAIN_CONTROLLER_055 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_061";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-055";
            doc /* When the i_data_out_adc is sampled, the 15 bit (MSB in little endian), shall be negated in order to */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_055 : IPOS_MAIN_CONTROLLER_055;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-055 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_061 | When the i_data_out_adc is sampled, the 15 bit (MSB in little endian), shall be negated in order to */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-055 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_061 */;
        satisfy req_IPOS_MAIN_CONTROLLER_055 by self;
        requirement def IPOS_MAIN_CONTROLLER_056 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_062";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-056";
            doc /* When i_debug_calibration is set (second bitfield of ADC_CAL_CONFIG ), the number of samples used by the avarage block during the calibration shall be set to 2. (The purpose of this mode is to */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_056 : IPOS_MAIN_CONTROLLER_056;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-056 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_062 | When i_debug_calibration is set (second bitfield of ADC_CAL_CONFIG ), the number of samples used by the avarage block during the calibration shall be set to 2. (The purpose of this mode is to */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-056 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_062 */;
        satisfy req_IPOS_MAIN_CONTROLLER_056 by self;
        requirement def IPOS_MAIN_CONTROLLER_057 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_063";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-057";
            doc /* When i_debug_adc_error_cap8_0_bypass is set to 1 (set to 1 en_debug_adc_error_cap8_0_bypass of ADC_GENERAL_DEBUG_0 ), the calibration result shall be bypassed in favor of the value written inside the registers */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_057 : IPOS_MAIN_CONTROLLER_057;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-057 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_063 | When i_debug_adc_error_cap8_0_bypass is set to 1 (set to 1 en_debug_adc_error_cap8_0_bypass of ADC_GENERAL_DEBUG_0 ), the calibration result shall be bypassed in favor of the value written inside the registers */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-057 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_063 */;
        satisfy req_IPOS_MAIN_CONTROLLER_057 by self;
        requirement def IPOS_MAIN_CONTROLLER_058 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_064";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-058";
            doc /* When the adc_readout_bypass mode is enabled by the 2 bitfield ADC_GENERAL_DEBUG_0 , the sampling phase of the ADC Phgen shall be bypassed in favor of regmap. In particular, the Sampling phase shall be controlled by the register EN_ADC_DEBUG and EN_ADC_START in ADC_GENERAL_DEBUG_0 and the sampled data shall be written in ADC_DATA_OUT_DEBUG_LOW and ADC_DATA_OUT_DEBUG_HIGH. and In this mode, before start a new sampling operation, the RESET_DEBUG_ADC DATA in */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_058 : IPOS_MAIN_CONTROLLER_058;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-058 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_064 | When the adc_readout_bypass mode is enabled by the 2 bitfield ADC_GENERAL_DEBUG_0 , the sampling phase of the ADC Phgen shall be bypassed in favor of regmap. In particular, the Sampling phase shall be controlled by the register EN_ADC_DEBUG and EN_ADC_START in ADC_GENERAL_DEBUG_0 and the sampled data shall be written in ADC_DATA_OUT_DEBUG_LOW and ADC_DATA_OUT_DEBUG_HIGH. and In this mode, before start a new sampling operation, the RESET_DEBUG_ADC DATA in */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-058 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_064 */;
        satisfy req_IPOS_MAIN_CONTROLLER_058 by self;
        requirement def IPOS_MAIN_CONTROLLER_059 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_073";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-059";
            doc /* When the i_hc_en is set to 0 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 2, ECG1 and ECG2 shall be active so the o_pd_hc2 shall remain high, o_pd_imp_from_bia shall go low */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_059 : IPOS_MAIN_CONTROLLER_059;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-059 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_073 | When the i_hc_en is set to 0 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 2, ECG1 and ECG2 shall be active so the o_pd_hc2 shall remain high, o_pd_imp_from_bia shall go low */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-059 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_073 */;
        satisfy req_IPOS_MAIN_CONTROLLER_059 by self;
        requirement def IPOS_MAIN_CONTROLLER_060 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_074";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-060";
            doc /* When the i_hc_en is set to 1 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 3, ECG0- ECG1 and ECG2 shall be active so the o_pd_hc2 shall go low, o_pd_imp shall go low and */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_060 : IPOS_MAIN_CONTROLLER_060;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-060 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_074 | When the i_hc_en is set to 1 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 3, ECG0- ECG1 and ECG2 shall be active so the o_pd_hc2 shall go low, o_pd_imp shall go low and */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-060 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_074 */;
        satisfy req_IPOS_MAIN_CONTROLLER_060 by self;
        requirement def IPOS_MAIN_CONTROLLER_061 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_077";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-061";
            doc /* 20ms after that the o_rst_hc2 is gone low, if i_clk_hlt_en is equal to 1, chopper_clock shall be generated and after another 10ms, o_rsti_hc2 shall go low. Instead, if i_clk_hlt_en is equal to 0, */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_061 : IPOS_MAIN_CONTROLLER_061;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-061 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_077 | 20ms after that the o_rst_hc2 is gone low, if i_clk_hlt_en is equal to 1, chopper_clock shall be generated and after another 10ms, o_rsti_hc2 shall go low. Instead, if i_clk_hlt_en is equal to 0, */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-061 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_077 */;
        satisfy req_IPOS_MAIN_CONTROLLER_061 by self;
        requirement def IPOS_MAIN_CONTROLLER_062 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_078";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-062";
            doc /* If i_su_hlt_dly is set to 0. At least after 205ms that the o_rsti_hc2 is gone low, o_su_hc2 shall go */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_062 : IPOS_MAIN_CONTROLLER_062;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-062 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_078 | If i_su_hlt_dly is set to 0. At least after 205ms that the o_rsti_hc2 is gone low, o_su_hc2 shall go */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-062 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_078 */;
        satisfy req_IPOS_MAIN_CONTROLLER_062 by self;
        requirement def IPOS_MAIN_CONTROLLER_063 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_080";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-063";
            doc /* When the user selects an operative mode that includes the BIA channel, a start-up shall be done. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_063 : IPOS_MAIN_CONTROLLER_063;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-063 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_080 | When the user selects an operative mode that includes the BIA channel, a start-up shall be done. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-063 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_080 */;
        satisfy req_IPOS_MAIN_CONTROLLER_063 by self;
        requirement def IPOS_MAIN_CONTROLLER_064 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_082";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-064";
            doc /* When i_imp_curinj signal is equal to 1, the o_imp_curinj_pd shall go low. On the other hand, if */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_064 : IPOS_MAIN_CONTROLLER_064;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-064 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_082 | When i_imp_curinj signal is equal to 1, the o_imp_curinj_pd shall go low. On the other hand, if */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-064 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_082 */;
        satisfy req_IPOS_MAIN_CONTROLLER_064 by self;
        requirement def IPOS_MAIN_CONTROLLER_065 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_083";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-065";
            doc /* At least 5ms after the falling of o_imp_curinj_pd and o_pd_imp_from_bia, if i_imp_curinj is equal to 1, o_en_ck_m_p_q shall be high and ck_m, ck_p and ck_q shall be generated from Clock generator block. On the other hand, if i_imp_curinj is equal to 0, the ck_m_p_q shall stay low. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_065 : IPOS_MAIN_CONTROLLER_065;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-065 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_083 | At least 5ms after the falling of o_imp_curinj_pd and o_pd_imp_from_bia, if i_imp_curinj is equal to 1, o_en_ck_m_p_q shall be high and ck_m, ck_p and ck_q shall be generated from Clock generator block. On the other hand, if i_imp_curinj is equal to 0, the ck_m_p_q shall stay low. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-065 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_083 */;
        satisfy req_IPOS_MAIN_CONTROLLER_065 by self;
        requirement def IPOS_MAIN_CONTROLLER_066 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_085";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-066";
            doc /* 20ms after the falling of o_rst_imp, if i_clk_imp_en is set to 1, the o_en_ck_chop_imp shall be high and ck_chop_imp shall be generated from Clock generator block. On the hand, if i_clk_imp_en is */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_066 : IPOS_MAIN_CONTROLLER_066;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-066 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_085 | 20ms after the falling of o_rst_imp, if i_clk_imp_en is set to 1, the o_en_ck_chop_imp shall be high and ck_chop_imp shall be generated from Clock generator block. On the hand, if i_clk_imp_en is */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-066 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_085 */;
        satisfy req_IPOS_MAIN_CONTROLLER_066 by self;
        requirement def IPOS_MAIN_CONTROLLER_067 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_087";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-067";
            doc /* If i_su_hlt_dly is set to 0,at least 205 ms after the falling of o_rsti_imp, o_sug_imp shall go low. Instead, if i_su_hlt_dly is set to 1, 755ms after the falling of o_rsti_imp, o_sug_imp shall go low. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_067 : IPOS_MAIN_CONTROLLER_067;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-067 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_087 | If i_su_hlt_dly is set to 0,at least 205 ms after the falling of o_rsti_imp, o_sug_imp shall go low. Instead, if i_su_hlt_dly is set to 1, 755ms after the falling of o_rsti_imp, o_sug_imp shall go low. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-067 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_087 */;
        satisfy req_IPOS_MAIN_CONTROLLER_067 by self;
        requirement def IPOS_MAIN_CONTROLLER_068 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_088";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-068";
            doc /* The i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] shall define how many time slots pass between two GSR acquisitions following this formula: GSRdata = time_slot 2 ∗ m_gsr */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_068 : IPOS_MAIN_CONTROLLER_068;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-068 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_088 | The i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] shall define how many time slots pass between two GSR acquisitions following this formula: GSRdata = time_slot 2 ∗ m_gsr */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-068 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_088 */;
        satisfy req_IPOS_MAIN_CONTROLLER_068 by self;
        requirement def IPOS_MAIN_CONTROLLER_069 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_089";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-069";
            doc /* If the en_gsr_cds [bit 3 of GSR_CTRL] is set High, the i_m_gsr shall define also in which time slot after the GSR_Curr_on falls from 1 to 0, an acquisition without current injection (o_gsr_curr_on set */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_069 : IPOS_MAIN_CONTROLLER_069;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-069 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_089 | If the en_gsr_cds [bit 3 of GSR_CTRL] is set High, the i_m_gsr shall define also in which time slot after the GSR_Curr_on falls from 1 to 0, an acquisition without current injection (o_gsr_curr_on set */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-069 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_089 */;
        satisfy req_IPOS_MAIN_CONTROLLER_069 by self;
        requirement def IPOS_MAIN_CONTROLLER_070 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_092";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-070";
            doc /* If en_gsr_cds is set low [bit 3 of GSR_CTRL], the gsr_curr_on shall set high in every time slot */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_070 : IPOS_MAIN_CONTROLLER_070;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-070 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_092 | If en_gsr_cds is set low [bit 3 of GSR_CTRL], the gsr_curr_on shall set high in every time slot */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-070 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_092 */;
        satisfy req_IPOS_MAIN_CONTROLLER_070 by self;
        requirement def IPOS_MAIN_CONTROLLER_071 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_093";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-071";
            doc /* If en_gsr_cds is set high [bit 3 of GSR_CTRL] the GSR_SNS (acquisition with o_gsr_curr_on set to 1) and GSR_CDS (acquisition with o_gsr_curr_on set to 0) shall be sampled 16 times, then mediated to get one single value for each of them, and then the final result shall be the subtraction between GSR_SNS and GSR_CDS. On the other hand, If en_gsr_cds is set low, no acquisition of GSR_CDS shall be done and the result shall be the average of 16 acquisitions of */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_071 : IPOS_MAIN_CONTROLLER_071;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-071 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_093 | If en_gsr_cds is set high [bit 3 of GSR_CTRL] the GSR_SNS (acquisition with o_gsr_curr_on set to 1) and GSR_CDS (acquisition with o_gsr_curr_on set to 0) shall be sampled 16 times, then mediated to get one single value for each of them, and then the final result shall be the subtraction between GSR_SNS and GSR_CDS. On the other hand, If en_gsr_cds is set low, no acquisition of GSR_CDS shall be done and the result shall be the average of 16 acquisitions of */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-071 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_093 */;
        satisfy req_IPOS_MAIN_CONTROLLER_071 by self;
        requirement def IPOS_MAIN_CONTROLLER_072 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_094";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-072";
            doc /* When only GSR is selected (NO ECG0 and PPG are selected), if i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] is greater than 0, the Device FSM shall go in SLEEP after the IDLE State and shall go back in Operative State only when the measurement shall be run or, in case of */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_072 : IPOS_MAIN_CONTROLLER_072;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-072 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_094 | When only GSR is selected (NO ECG0 and PPG are selected), if i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] is greater than 0, the Device FSM shall go in SLEEP after the IDLE State and shall go back in Operative State only when the measurement shall be run or, in case of */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-072 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_094 */;
        satisfy req_IPOS_MAIN_CONTROLLER_072 by self;
        requirement def IPOS_MAIN_CONTROLLER_073 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_095";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-073";
            doc /* The o_En_TIA, o_EN_Buff, o_EN_ADC and o_EN_IDAC shall be high when the PPG_FSM is */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_073 : IPOS_MAIN_CONTROLLER_073;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-073 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_095 | The o_En_TIA, o_EN_Buff, o_EN_ADC and o_EN_IDAC shall be high when the PPG_FSM is */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-073 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_095 */;
        satisfy req_IPOS_MAIN_CONTROLLER_073 by self;
        requirement def IPOS_MAIN_CONTROLLER_074 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_096";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-074";
            doc /* When the i_m_ppg ( SET_PPG_FREQ_h and SET_PPG_FREQ_l) is different from 0 and PPG_SEL in DEVICE_CONFIG_CHANNEL register is set to 1, when the ELAB_FSM is in PPG STATE, PPG_IOFF_CALIB or PPG_ALC_STORAGE, the i_start_operation_for_ppg shall be set */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_074 : IPOS_MAIN_CONTROLLER_074;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-074 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_096 | When the i_m_ppg ( SET_PPG_FREQ_h and SET_PPG_FREQ_l) is different from 0 and PPG_SEL in DEVICE_CONFIG_CHANNEL register is set to 1, when the ELAB_FSM is in PPG STATE, PPG_IOFF_CALIB or PPG_ALC_STORAGE, the i_start_operation_for_ppg shall be set */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-074 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_096 */;
        satisfy req_IPOS_MAIN_CONTROLLER_074 by self;
        requirement def IPOS_MAIN_CONTROLLER_075 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_098";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-075";
            doc /* When in ALC Compensation, the PPG FSM shall raise the o_start_alc_comp signal to the ALC */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_075 : IPOS_MAIN_CONTROLLER_075;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-075 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_098 | When in ALC Compensation, the PPG FSM shall raise the o_start_alc_comp signal to the ALC */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-075 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_098 */;
        satisfy req_IPOS_MAIN_CONTROLLER_075 by self;
        requirement def IPOS_MAIN_CONTROLLER_076 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_099";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-076";
            doc /* When in ALC Compensation, the PPG shall wait that the rise of i_end_compensation signal from the ALC Compensation block to go into the RX_Start_UP state. This shall happen in OPERATIVE. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_076 : IPOS_MAIN_CONTROLLER_076;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-076 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_099 | When in ALC Compensation, the PPG shall wait that the rise of i_end_compensation signal from the ALC Compensation block to go into the RX_Start_UP state. This shall happen in OPERATIVE. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-076 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_099 */;
        satisfy req_IPOS_MAIN_CONTROLLER_076 by self;
        requirement def IPOS_MAIN_CONTROLLER_077 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_100";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-077";
            doc /* When in Rx_Start_Up state, the o_tx_Preset shall be set 0, the en_tx_i shall be set to 1, the o_BIDAC shall maintain the value reached during the ALC Compensation summed up, if i_ppg_ioff_calibration is enabled, with the IOFF_OFFSET computed during the IOFF Calibration */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_077 : IPOS_MAIN_CONTROLLER_077;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-077 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_100 | When in Rx_Start_Up state, the o_tx_Preset shall be set 0, the en_tx_i shall be set to 1, the o_BIDAC shall maintain the value reached during the ALC Compensation summed up, if i_ppg_ioff_calibration is enabled, with the IOFF_OFFSET computed during the IOFF Calibration */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-077 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_100 */;
        satisfy req_IPOS_MAIN_CONTROLLER_077 by self;
        requirement def IPOS_MAIN_CONTROLLER_078 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1004";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-078";
            doc /* [Covers: DDS_STBIO1_0118] [Covers: DDS_STBIO1_0125] The user shall configure time slot duration in DEVICE_CONFIG_OPERATION register [4:2] */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_078 : IPOS_MAIN_CONTROLLER_078;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-078 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1004 | [Covers: DDS_STBIO1_0118] [Covers: DDS_STBIO1_0125] The user shall configure time slot duration in DEVICE_CONFIG_OPERATION register [4:2] */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-078 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1004 */;
        satisfy req_IPOS_MAIN_CONTROLLER_078 by self;
        requirement def IPOS_MAIN_CONTROLLER_079 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1005";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-079";
            doc /* The user shall configure which channel is selected and if work in Data Storage mode for the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_079 : IPOS_MAIN_CONTROLLER_079;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-079 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1005 | The user shall configure which channel is selected and if work in Data Storage mode for the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-079 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1005 */;
        satisfy req_IPOS_MAIN_CONTROLLER_079 by self;
        requirement def IPOS_MAIN_CONTROLLER_080 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1007";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-080";
            doc /* [Covers: DDS_STBIO1_0120] [Covers: DDS_STBIO1_0122] [Covers: DDS_STBIO1_0127] [Covers: DDS_STBIO1_0130] In Order to enable an ECG0 Channel Operation, the user shall always select the ECG0 channel */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_080 : IPOS_MAIN_CONTROLLER_080;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-080 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1007 | [Covers: DDS_STBIO1_0120] [Covers: DDS_STBIO1_0122] [Covers: DDS_STBIO1_0127] [Covers: DDS_STBIO1_0130] In Order to enable an ECG0 Channel Operation, the user shall always select the ECG0 channel */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-080 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1007 */;
        satisfy req_IPOS_MAIN_CONTROLLER_080 by self;
        requirement def IPOS_MAIN_CONTROLLER_081 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1008";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-081";
            doc /* [Covers: DDS_STBIO1_0128] [Covers: DDS_STBIO1_0140] In Order to enable a BIA Channel Operation, the user shall always select the BIA channel */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_081 : IPOS_MAIN_CONTROLLER_081;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-081 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1008 | [Covers: DDS_STBIO1_0128] [Covers: DDS_STBIO1_0140] In Order to enable a BIA Channel Operation, the user shall always select the BIA channel */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-081 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1008 */;
        satisfy req_IPOS_MAIN_CONTROLLER_081 by self;
        requirement def IPOS_MAIN_CONTROLLER_082 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1009";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-082";
            doc /* In Order to enable a GSR Channel Operation, the user shall always select the GSR channel */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_082 : IPOS_MAIN_CONTROLLER_082;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-082 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1009 | In Order to enable a GSR Channel Operation, the user shall always select the GSR channel */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-082 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1009 */;
        satisfy req_IPOS_MAIN_CONTROLLER_082 by self;
        requirement def IPOS_MAIN_CONTROLLER_083 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_101";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-083";
            doc /* When in Rx_Start_Up state, the PPG_FSM shall stay in this state for the T_rx_set time (GENERAL_PPG_PARAMETERS_3 register [3:0])) and then go into the FIRST_ALC_SAMPLES */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_083 : IPOS_MAIN_CONTROLLER_083;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-083 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_101 | When in Rx_Start_Up state, the PPG_FSM shall stay in this state for the T_rx_set time (GENERAL_PPG_PARAMETERS_3 register [3:0])) and then go into the FIRST_ALC_SAMPLES */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-083 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_101 */;
        satisfy req_IPOS_MAIN_CONTROLLER_083 by self;
        requirement def IPOS_MAIN_CONTROLLER_084 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1010";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-084";
            doc /* In Order to enable a PPG Channel Operation, the user shall always select the PPG channel */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_084 : IPOS_MAIN_CONTROLLER_084;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-084 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1010 | In Order to enable a PPG Channel Operation, the user shall always select the PPG channel */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-084 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1010 */;
        satisfy req_IPOS_MAIN_CONTROLLER_084 by self;
        requirement def IPOS_MAIN_CONTROLLER_085 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1011";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-085";
            doc /* In Order to enable an ECG1_ECG2 Channel Operation, the user shall always select the ECG1_ECG2 channel (DEVICE_CONFIG_CHANNEL), set the i_M_ECG greater than zero and */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_085 : IPOS_MAIN_CONTROLLER_085;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-085 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1011 | In Order to enable an ECG1_ECG2 Channel Operation, the user shall always select the ECG1_ECG2 channel (DEVICE_CONFIG_CHANNEL), set the i_M_ECG greater than zero and */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-085 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1011 */;
        satisfy req_IPOS_MAIN_CONTROLLER_085 by self;
        requirement def IPOS_MAIN_CONTROLLER_086 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_102";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-086";
            doc /* When in FIRST_ALC_SAMPLES state, the o_start_ADC signal shall be set high until */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_086 : IPOS_MAIN_CONTROLLER_086;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-086 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_102 | When in FIRST_ALC_SAMPLES state, the o_start_ADC signal shall be set high until */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-086 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_102 */;
        satisfy req_IPOS_MAIN_CONTROLLER_086 by self;
        requirement def IPOS_MAIN_CONTROLLER_087 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_103";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-087";
            doc /* When in FIRST_ALC_SAMPLES state, the PPG_FSM Shall stay in this state until 1 clock cycle after the rise of the i_end_average and the TX_start_up time has passed. After that, the PPG FSM */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_087 : IPOS_MAIN_CONTROLLER_087;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-087 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_103 | When in FIRST_ALC_SAMPLES state, the PPG_FSM Shall stay in this state until 1 clock cycle after the rise of the i_end_average and the TX_start_up time has passed. After that, the PPG FSM */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-087 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_103 */;
        satisfy req_IPOS_MAIN_CONTROLLER_087 by self;
        requirement def IPOS_MAIN_CONTROLLER_088 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1034";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-088";
            doc /* Once in the ERROR state, the user shall wait 1ms before set to 0 the MODE_OPERATION to go */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_088 : IPOS_MAIN_CONTROLLER_088;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-088 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1034 | Once in the ERROR state, the user shall wait 1ms before set to 0 the MODE_OPERATION to go */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-088 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1034 */;
        satisfy req_IPOS_MAIN_CONTROLLER_088 by self;
        requirement def IPOS_MAIN_CONTROLLER_089 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_104";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-089";
            doc /* When in FIRST_ALC_SAMPLES state, when i_end_average is set to 1, the o_start_digital_ramp signal shall be set high to start the rising of the digital ramp and go into the RISING_RAMP state. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_089 : IPOS_MAIN_CONTROLLER_089;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-089 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_104 | When in FIRST_ALC_SAMPLES state, when i_end_average is set to 1, the o_start_digital_ramp signal shall be set high to start the rising of the digital ramp and go into the RISING_RAMP state. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-089 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_104 */;
        satisfy req_IPOS_MAIN_CONTROLLER_089 by self;
        requirement def IPOS_MAIN_CONTROLLER_090 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_105";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-090";
            doc /* When in Rising_Ramp state, at the half of Rising_time, the o_idac_dc_ppg_frame shall be set to the IDAC_DC_PPG_FRAME_{n} (FRAME_n_PARAMETERS_5 register [5:0]) value related to the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_090 : IPOS_MAIN_CONTROLLER_090;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-090 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_105 | When in Rising_Ramp state, at the half of Rising_time, the o_idac_dc_ppg_frame shall be set to the IDAC_DC_PPG_FRAME_{n} (FRAME_n_PARAMETERS_5 register [5:0]) value related to the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-090 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_105 */;
        satisfy req_IPOS_MAIN_CONTROLLER_090 by self;
        requirement def IPOS_MAIN_CONTROLLER_091 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_106";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-091";
            doc /* When in Rising_Ramp State, the PPG_FSM shall stay in this state until the end of the Rising Time */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_091 : IPOS_MAIN_CONTROLLER_091;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-091 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_106 | When in Rising_Ramp State, the PPG_FSM shall stay in this state until the end of the Rising Time */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-091 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_106 */;
        satisfy req_IPOS_MAIN_CONTROLLER_091 by self;
        requirement def IPOS_MAIN_CONTROLLER_092 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_108";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-092";
            doc /* When in Measurement state, the PPG_FSM shall stay in this state until the rising of the i_end_average signal from the ADC block. After that, the PPG_FSM shall bring itself into the Falling */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_092 : IPOS_MAIN_CONTROLLER_092;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-092 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_108 | When in Measurement state, the PPG_FSM shall stay in this state until the rising of the i_end_average signal from the ADC block. After that, the PPG_FSM shall bring itself into the Falling */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-092 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_108 */;
        satisfy req_IPOS_MAIN_CONTROLLER_092 by self;
        requirement def IPOS_MAIN_CONTROLLER_093 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_109";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-093";
            doc /* When in MEASUREMENT State, the o_falling_digital_ramp signal shall be set to 1 to go into the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_093 : IPOS_MAIN_CONTROLLER_093;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-093 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_109 | When in MEASUREMENT State, the o_falling_digital_ramp signal shall be set to 1 to go into the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-093 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_109 */;
        satisfy req_IPOS_MAIN_CONTROLLER_093 by self;
        requirement def IPOS_MAIN_CONTROLLER_094 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1095";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-094";
            doc /* The o_pd_tia, o_pd_idac and o_pd_pga shall be the negated version the o_en_tia, o_en_idac */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_094 : IPOS_MAIN_CONTROLLER_094;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-094 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1095 | The o_pd_tia, o_pd_idac and o_pd_pga shall be the negated version the o_en_tia, o_en_idac */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-094 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1095 */;
        satisfy req_IPOS_MAIN_CONTROLLER_094 by self;
        requirement def IPOS_MAIN_CONTROLLER_095 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_110";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-095";
            doc /* When in Falling_Ramp State, at the half of the Falling_Time the o_idac_dc_ppg_frame shall be */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_095 : IPOS_MAIN_CONTROLLER_095;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-095 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_110 | When in Falling_Ramp State, at the half of the Falling_Time the o_idac_dc_ppg_frame shall be */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-095 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_110 */;
        satisfy req_IPOS_MAIN_CONTROLLER_095 by self;
        requirement def IPOS_MAIN_CONTROLLER_096 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1102";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-096";
            doc /* Tx Preset shall be set to 1 a configurable TX_Preset_Step time before the start of the Digital */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_096 : IPOS_MAIN_CONTROLLER_096;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-096 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1102 | Tx Preset shall be set to 1 a configurable TX_Preset_Step time before the start of the Digital */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-096 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1102 */;
        satisfy req_IPOS_MAIN_CONTROLLER_096 by self;
        requirement def IPOS_MAIN_CONTROLLER_097 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1104";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-097";
            doc /* Tx Preset shall be set to 0 before the rising phase(i_start_digtal_ramp) and after the falling phase */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_097 : IPOS_MAIN_CONTROLLER_097;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-097 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1104 | Tx Preset shall be set to 0 before the rising phase(i_start_digtal_ramp) and after the falling phase */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-097 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1104 */;
        satisfy req_IPOS_MAIN_CONTROLLER_097 by self;
        requirement def IPOS_MAIN_CONTROLLER_098 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_111";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-098";
            doc /* When in Falling_Ramp state, the PPG_FSM shall stay in this state until the end of the Falling Time (depends on the user's configuration of Digital Ramp parameters) and bring itself into the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_098 : IPOS_MAIN_CONTROLLER_098;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-098 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_111 | When in Falling_Ramp state, the PPG_FSM shall stay in this state until the end of the Falling Time (depends on the user's configuration of Digital Ramp parameters) and bring itself into the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-098 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_111 */;
        satisfy req_IPOS_MAIN_CONTROLLER_098 by self;
        requirement def IPOS_MAIN_CONTROLLER_099 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1116";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-099";
            doc /* When the Ioff Calibration algorithm is enabled, it shall be performed every time a new */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_099 : IPOS_MAIN_CONTROLLER_099;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-099 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1116 | When the Ioff Calibration algorithm is enabled, it shall be performed every time a new */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-099 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1116 */;
        satisfy req_IPOS_MAIN_CONTROLLER_099 by self;
        requirement def IPOS_MAIN_CONTROLLER_100 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_112";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-100";
            doc /* When in SECOND_ALC_SAMPLES state, the o_en_Txi shall be set low after the end at least of the T_tx_ledoff time (TX_LEDOFF_FRAME_{n}) and the o_start_adc signal shall be set to 1. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_100 : IPOS_MAIN_CONTROLLER_100;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-100 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_112 | When in SECOND_ALC_SAMPLES state, the o_en_Txi shall be set low after the end at least of the T_tx_ledoff time (TX_LEDOFF_FRAME_{n}) and the o_start_adc signal shall be set to 1. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-100 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_112 */;
        satisfy req_IPOS_MAIN_CONTROLLER_100 by self;
        requirement def IPOS_MAIN_CONTROLLER_101 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_113";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-101";
            doc /* When in SECOND_ALC_SAMPLES state, the PPG_FSM shall stay in this state until the rise of the end_of_conversion signal from the ADC block. After that, if there are no more frames to run, the PPG_FSM shall go into the Reset State, otherwise, if there are other frames to run and channel rx is not changed, the PPG_FSM shall go into the Rx_start_up phase. On the other hand, if there are other frame to run and rx_channel is changed, the PPG_FSM shall go into the RESET_PPG */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_101 : IPOS_MAIN_CONTROLLER_101;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-101 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_113 | When in SECOND_ALC_SAMPLES state, the PPG_FSM shall stay in this state until the rise of the end_of_conversion signal from the ADC block. After that, if there are no more frames to run, the PPG_FSM shall go into the Reset State, otherwise, if there are other frames to run and channel rx is not changed, the PPG_FSM shall go into the Rx_start_up phase. On the other hand, if there are other frame to run and rx_channel is changed, the PPG_FSM shall go into the RESET_PPG */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-101 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_113 */;
        satisfy req_IPOS_MAIN_CONTROLLER_101 by self;
        requirement def IPOS_MAIN_CONTROLLER_102 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1139";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-102";
            doc /* The PPG Noise Data shall be accumulated in two phases, the first when the PPG FSM state is in FIRST_ALC_SAMPLES States and the second when the PPG FSM state is in the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_102 : IPOS_MAIN_CONTROLLER_102;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-102 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1139 | The PPG Noise Data shall be accumulated in two phases, the first when the PPG FSM state is in FIRST_ALC_SAMPLES States and the second when the PPG FSM state is in the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-102 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1139 */;
        satisfy req_IPOS_MAIN_CONTROLLER_102 by self;
        requirement def IPOS_MAIN_CONTROLLER_103 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_1143";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-103";
            doc /* For GSR Operation, if i_en_cds is set 0, the behavior shall as described in Requirement 143, otherwise the o_write_enabled shall be asserted when i_end_of_coversion is set to 1 and i_n_average_ecg_bia_gsr is equal to their limit values when the measurement is done with */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_103 : IPOS_MAIN_CONTROLLER_103;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-103 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_1143 | For GSR Operation, if i_en_cds is set 0, the behavior shall as described in Requirement 143, otherwise the o_write_enabled shall be asserted when i_end_of_coversion is set to 1 and i_n_average_ecg_bia_gsr is equal to their limit values when the measurement is done with */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-103 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_1143 */;
        satisfy req_IPOS_MAIN_CONTROLLER_103 by self;
        requirement def IPOS_MAIN_CONTROLLER_104 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_115";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-104";
            doc /* At the end of each Frame, the start_avarage signal shall be rise to the Average block computation. Once the Average is computed, if no averages_between_equal_frames option is selected, the data shall be written inside the FIFO Memory using the Main Control ler AHB Master interface. If there is avareges_between_equal_frames option selected from regmap, after the computations of this average, the obtained data shall be written inside the FIFO Memory using the Main Controller AHB */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_104 : IPOS_MAIN_CONTROLLER_104;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-104 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_115 | At the end of each Frame, the start_avarage signal shall be rise to the Average block computation. Once the Average is computed, if no averages_between_equal_frames option is selected, the data shall be written inside the FIFO Memory using the Main Control ler AHB Master interface. If there is avareges_between_equal_frames option selected from regmap, after the computations of this average, the obtained data shall be written inside the FIFO Memory using the Main Controller AHB */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-104 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_115 */;
        satisfy req_IPOS_MAIN_CONTROLLER_104 by self;
        requirement def IPOS_MAIN_CONTROLLER_105 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_118";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-105";
            doc /* When the input signal o_Tx_preset is set to 1, the o_Tx_Vref shall increment the first step at value i_N_start (DIGITAL_RAMP_CONFIG_PARAM_3 register [2:0]) at a time i_T_preset */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_105 : IPOS_MAIN_CONTROLLER_105;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-105 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_118 | When the input signal o_Tx_preset is set to 1, the o_Tx_Vref shall increment the first step at value i_N_start (DIGITAL_RAMP_CONFIG_PARAM_3 register [2:0]) at a time i_T_preset */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-105 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_118 */;
        satisfy req_IPOS_MAIN_CONTROLLER_105 by self;
        requirement def IPOS_MAIN_CONTROLLER_106 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_120";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-106";
            doc /* When the i_falling_digital_ramp is set to 1, the o_TX_Vref shall decrement from N_MAX value (DIGITAL_RAMP_CONFIG_PARAM_1 register [3:0]) to zero with a step equal to 1 every 2-clock */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_106 : IPOS_MAIN_CONTROLLER_106;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-106 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_120 | When the i_falling_digital_ramp is set to 1, the o_TX_Vref shall decrement from N_MAX value (DIGITAL_RAMP_CONFIG_PARAM_1 register [3:0]) to zero with a step equal to 1 every 2-clock */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-106 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_120 */;
        satisfy req_IPOS_MAIN_CONTROLLER_106 by self;
        requirement def IPOS_MAIN_CONTROLLER_107 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_126";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-107";
            doc /* When ALC_COMP starts, o_BTIA_gain (2:0) shall be set at i_gain_start (PPG_ALC_CONFIG_PARAM_2 register [4:2]) and o_w_BTIA_ALC (8:0) shall be set at */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_107 : IPOS_MAIN_CONTROLLER_107;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-107 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_126 | When ALC_COMP starts, o_BTIA_gain (2:0) shall be set at i_gain_start (PPG_ALC_CONFIG_PARAM_2 register [4:2]) and o_w_BTIA_ALC (8:0) shall be set at */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-107 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_126 */;
        satisfy req_IPOS_MAIN_CONTROLLER_107 by self;
        requirement def IPOS_MAIN_CONTROLLER_108 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_128";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-108";
            doc /* When ECG0 and BIA are selected 21 acquisitions shall be required (acquisitions described in section 5.4 ADC PHASE) and then device shall go in SLEEP (DEVICE_STATUS_REG register */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_108 : IPOS_MAIN_CONTROLLER_108;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-108 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_128 | When ECG0 and BIA are selected 21 acquisitions shall be required (acquisitions described in section 5.4 ADC PHASE) and then device shall go in SLEEP (DEVICE_STATUS_REG register */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-108 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_128 */;
        satisfy req_IPOS_MAIN_CONTROLLER_108 by self;
        requirement def IPOS_MAIN_CONTROLLER_109 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_134";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-109";
            doc /* According to time diagram, when in RESET_PPG and ELAB_FSM is in PPG state during the first frame (i_id_frame=0) , shall be wait a configurable time PPG_START_UP_TIME (PPG_START_UP_TIME starting from when i_start_operation_ppg is set to 1 and at least 1 clock */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_109 : IPOS_MAIN_CONTROLLER_109;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-109 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_134 | According to time diagram, when in RESET_PPG and ELAB_FSM is in PPG state during the first frame (i_id_frame=0) , shall be wait a configurable time PPG_START_UP_TIME (PPG_START_UP_TIME starting from when i_start_operation_ppg is set to 1 and at least 1 clock */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-109 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_134 */;
        satisfy req_IPOS_MAIN_CONTROLLER_109 by self;
        requirement def IPOS_MAIN_CONTROLLER_110 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_137";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-110";
            doc /* The average block shall perform an average on 4 Samples for each of ECG_x_AC, BIA AC P, BIA AC Q, BIA DC P and BIA DC Q , 1 Sample ECG_x_DC (Check if the i_end_of_coversion rise the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_110 : IPOS_MAIN_CONTROLLER_110;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-110 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_137 | The average block shall perform an average on 4 Samples for each of ECG_x_AC, BIA AC P, BIA AC Q, BIA DC P and BIA DC Q , 1 Sample ECG_x_DC (Check if the i_end_of_coversion rise the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-110 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_137 */;
        satisfy req_IPOS_MAIN_CONTROLLER_110 by self;
        requirement def IPOS_MAIN_CONTROLLER_111 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_138";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-111";
            doc /* The average block shall perform the average on 16 sample acquisition for GSR. When the CDS mode is enabled, the average block shall perform a n average on 16 sample acquisition on GSR ON and 16 sample acquisition on GSR OFF, then shall perform a subtraction operation between */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_111 : IPOS_MAIN_CONTROLLER_111;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-111 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_138 | The average block shall perform the average on 16 sample acquisition for GSR. When the CDS mode is enabled, the average block shall perform a n average on 16 sample acquisition on GSR ON and 16 sample acquisition on GSR OFF, then shall perform a subtraction operation between */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-111 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_138 */;
        satisfy req_IPOS_MAIN_CONTROLLER_111 by self;
        requirement def IPOS_MAIN_CONTROLLER_112 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_140";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-112";
            doc /* Once the PPG Raw Data and PPG Noise reach the i_n_average_ppg value , depending on the ALC Mask bit value, the two accumulated shall be subtracted and final results shall be computed as follow: I_N_Average_PPG Samples Result with ALC MASK=0 Result with ALC Mask=1 0 3= (N1+P+N2) (Acc_P-(Acc_N)/2) * 8 Acc_P*16 2 4= (N1+2P+N2) (Acc_P -(Acc_N)) * 4 Acc_P *8 4 8= (2N1+4P+2N2) (Acc_P -(Acc_N)) * 2 Acc_P *4 8 16= (4N1+8P+4N2) (Acc_P -(Acc_N)) Acc_P *2 16 32= (8N1+16P+8N2) (Acc_P -(Acc_N))/2 Acc_P 32 64= (16N1+32P+16N2) (Acc_P -(Acc_N))/4 Acc_P /2 64 128= (32N1+64P+32N2) (Acc_P -(Acc_N))/8 Acc_P /4 128 256= (64N1+128P+64N2) (Acc_P -(Acc_N))/16 Acc_P /8 Table 18: PPG Result Table Where PPG Raw Data is indicated as P and PPG Noise is indicated as N1 and N2, while Acc_P */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_112 : IPOS_MAIN_CONTROLLER_112;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-112 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_140 | Once the PPG Raw Data and PPG Noise reach the i_n_average_ppg value , depending on the ALC Mask bit value, the two accumulated shall be subtracted and final results shall be computed as follow: I_N_Average_PPG Samples Result with ALC MASK=0 Result with ALC Mask=1 0 3= (N1+P+N2) (Acc_P-(Acc_N)/2) * 8 Acc_P*16 2 4= (N1+2P+N2) (Acc_P -(Acc_N)) * 4 Acc_P *8 4 8= (2N1+4P+2N2) (Acc_P -(Acc_N)) * 2 Acc_P *4 8 16= (4N1+8P+4N2) (Acc_P -(Acc_N)) Acc_P *2 16 32= (8N1+16P+8N2) (Acc_P -(Acc_N))/2 Acc_P 32 64= (16N1+32P+16N2) (Acc_P -(Acc_N))/4 Acc_P /2 64 128= (32N1+64P+32N2) (Acc_P -(Acc_N))/8 Acc_P /4 128 256= (64N1+128P+64N2) (Acc_P -(Acc_N))/16 Acc_P /8 Table 18: PPG Result Table Where PPG Raw Data is indicated as P and PPG Noise is indicated as N1 and N2, while Acc_P */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-112 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_140 */;
        satisfy req_IPOS_MAIN_CONTROLLER_112 by self;
        requirement def IPOS_MAIN_CONTROLLER_113 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_2143";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-113";
            doc /* When i_frame_ppg_debug is set to a value greater than 0 and i_n_average_ppg is set to a value between 1 and 16, all the ADC output (i_data_in) for ALC (i_data_valid_noise_ppg_adc set to 1) and PPG data (i_data_valid_ppg_adc) shall be stored in o_adc_data_debug_alc_2, */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_113 : IPOS_MAIN_CONTROLLER_113;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-113 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_2143 | When i_frame_ppg_debug is set to a value greater than 0 and i_n_average_ppg is set to a value between 1 and 16, all the ADC output (i_data_in) for ALC (i_data_valid_noise_ppg_adc set to 1) and PPG data (i_data_valid_ppg_adc) shall be stored in o_adc_data_debug_alc_2, */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-113 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_2143 */;
        satisfy req_IPOS_MAIN_CONTROLLER_113 by self;
        requirement def IPOS_MAIN_CONTROLLER_114 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_2144";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-114";
            doc /* [Covers: DDS_STBIO1_0124] [Covers: DDS_STBIO1_0142] The data written in FIFO shall have the following tag: DATA TYPE BIT: 23 - 20 BIT: 19 - 16 BIT: 15 - 0 PPG FRAME 0 0000 DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT PPG FRAME 1 0001 PPG FRAME 2 0010 PPG FRAME 3 0011 PPG FRAME 4 0100 PPG FRAME 5 0101 PPG FRAME 6 0110 PPG FRAME 7 0111 PPG FRAME 8 1000 PPG FRAME 9 1001 PPG FRAME 10 1010 PPG FRAME 11 1011 TIME SLOT DATA 1111 0000 DATA 16 BIT ECG0_AC 1100 0000 DATA 16 BIT ECG0_DC 1101 0000 DATA 16 BIT ECG1_AC 1100 0001 DATA 16 BIT ECG1_DC 1101 0001 DATA 16 BIT ECG2_AC 1100 0010 DATA 16 BIT ECG2_DC 1101 0010 DATA 16 BIT */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_114 : IPOS_MAIN_CONTROLLER_114;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-114 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_2144 | [Covers: DDS_STBIO1_0124] [Covers: DDS_STBIO1_0142] The data written in FIFO shall have the following tag: DATA TYPE BIT: 23 - 20 BIT: 19 - 16 BIT: 15 - 0 PPG FRAME 0 0000 DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT PPG FRAME 1 0001 PPG FRAME 2 0010 PPG FRAME 3 0011 PPG FRAME 4 0100 PPG FRAME 5 0101 PPG FRAME 6 0110 PPG FRAME 7 0111 PPG FRAME 8 1000 PPG FRAME 9 1001 PPG FRAME 10 1010 PPG FRAME 11 1011 TIME SLOT DATA 1111 0000 DATA 16 BIT ECG0_AC 1100 0000 DATA 16 BIT ECG0_DC 1101 0000 DATA 16 BIT ECG1_AC 1100 0001 DATA 16 BIT ECG1_DC 1101 0001 DATA 16 BIT ECG2_AC 1100 0010 DATA 16 BIT ECG2_DC 1101 0010 DATA 16 BIT */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-114 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_2144 */;
        satisfy req_IPOS_MAIN_CONTROLLER_114 by self;
        requirement def IPOS_MAIN_CONTROLLER_115 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_2145";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-115";
            doc /* The Frame shall work as follows: 1. Select how many times a particular frame shall be repeated 2. The result of each repetition shall be obtained as explained in [IPOS_STBIO1_MAIN_CONTROLLER_1 40] REQUIREMENT 3. After the last repetition has been accumulated, the data output shall be obtained dividing by the number of repeated frames the accumulated data to obtain a 20 bit data. The final result shall be computed as follows: Number of times the Frame has been repeated Result 2 (Res_F_R1 + Res_F_R2)/2 4 (Res_F_R1 + Res_F_R2+Res_F_R3+Res_F_R4)/4 8 (Res_F_R1 + Res_F_R2+Res_F_R3+…..+Res_F_R8)/8 Table 20: Frame Repetitions Result Computation table Where Res_F_Rx stands for Result_frame_Repeated_times (Example: RES_F_R2 refers to the result of the second repetition of the frame. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_115 : IPOS_MAIN_CONTROLLER_115;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-115 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_2145 | The Frame shall work as follows: 1. Select how many times a particular frame shall be repeated 2. The result of each repetition shall be obtained as explained in [IPOS_STBIO1_MAIN_CONTROLLER_1 40] REQUIREMENT 3. After the last repetition has been accumulated, the data output shall be obtained dividing by the number of repeated frames the accumulated data to obtain a 20 bit data. The final result shall be computed as follows: Number of times the Frame has been repeated Result 2 (Res_F_R1 + Res_F_R2)/2 4 (Res_F_R1 + Res_F_R2+Res_F_R3+Res_F_R4)/4 8 (Res_F_R1 + Res_F_R2+Res_F_R3+…..+Res_F_R8)/8 Table 20: Frame Repetitions Result Computation table Where Res_F_Rx stands for Result_frame_Repeated_times (Example: RES_F_R2 refers to the result of the second repetition of the frame. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-115 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_2145 */;
        satisfy req_IPOS_MAIN_CONTROLLER_115 by self;
        requirement def IPOS_MAIN_CONTROLLER_116 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_2146";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-116";
            doc /* In case the ppg sample data are equal (once converted in two’s complement) at 0x8000 or 0x7FFF for at least half of the selected average (example, if 128 acquisitions are selected, the threshold shall be greater or equal to 64), o_saturation_flag shall be set to 1 and shall go to 0 at the start of the next frame or frame repetition. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_116 : IPOS_MAIN_CONTROLLER_116;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-116 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_2146 | In case the ppg sample data are equal (once converted in two’s complement) at 0x8000 or 0x7FFF for at least half of the selected average (example, if 128 acquisitions are selected, the threshold shall be greater or equal to 64), o_saturation_flag shall be set to 1 and shall go to 0 at the start of the next frame or frame repetition. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-116 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_2146 */;
        satisfy req_IPOS_MAIN_CONTROLLER_116 by self;
        requirement def IPOS_MAIN_CONTROLLER_117 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_3124";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-117";
            doc /* When the ELAB_FSM is in ECG State and only ECG0 is selected, the o_ADC_EN shall go high, */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_117 : IPOS_MAIN_CONTROLLER_117;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-117 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_3124 | When the ELAB_FSM is in ECG State and only ECG0 is selected, the o_ADC_EN shall go high, */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-117 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_3124 */;
        satisfy req_IPOS_MAIN_CONTROLLER_117 by self;
        requirement def IPOS_MAIN_CONTROLLER_118 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_3125";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-118";
            doc /* When ELAB_FSM is in ECG state and ECG1 and ECG2 are selected , o_ADC_EN shall go high and 10 acquisitions are required (acquisitions described in chapter in section 5.4 ADC PHASE). */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_118 : IPOS_MAIN_CONTROLLER_118;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-118 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_3125 | When ELAB_FSM is in ECG state and ECG1 and ECG2 are selected , o_ADC_EN shall go high and 10 acquisitions are required (acquisitions described in chapter in section 5.4 ADC PHASE). */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-118 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_3125 */;
        satisfy req_IPOS_MAIN_CONTROLLER_118 by self;
        requirement def IPOS_MAIN_CONTROLLER_119 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_3126";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-119";
            doc /* When ELAB_FSM is in ECG state and EC0, ECG1 and ECG2 are selected , o_ADC_EN shall go high and15 acquisitions are required (acquisitions described in 5.4 ADC PHASE) and then device */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_119 : IPOS_MAIN_CONTROLLER_119;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-119 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_3126 | When ELAB_FSM is in ECG state and EC0, ECG1 and ECG2 are selected , o_ADC_EN shall go high and15 acquisitions are required (acquisitions described in 5.4 ADC PHASE) and then device */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-119 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_3126 */;
        satisfy req_IPOS_MAIN_CONTROLLER_119 by self;
        requirement def IPOS_MAIN_CONTROLLER_120 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_3127";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-120";
            doc /* When ELAB_FSM is in BIA state , o_ADC_EN shall go high and 16 acquisitions are required (acquisitions described in section 5.4 ADC PHASE ) and then device shall go in */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_120 : IPOS_MAIN_CONTROLLER_120;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-120 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_3127 | When ELAB_FSM is in BIA state , o_ADC_EN shall go high and 16 acquisitions are required (acquisitions described in section 5.4 ADC PHASE ) and then device shall go in */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-120 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_3127 */;
        satisfy req_IPOS_MAIN_CONTROLLER_120 by self;
        requirement def IPOS_MAIN_CONTROLLER_121 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_3128";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-121";
            doc /* When the wave velocity mode is selected and the device FSM is in WAIT_SU, the Elaboration FSM shall go into the TIMER BUFFER State and then into the PPG ALC STORAGE */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_121 : IPOS_MAIN_CONTROLLER_121;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-121 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_3128 | When the wave velocity mode is selected and the device FSM is in WAIT_SU, the Elaboration FSM shall go into the TIMER BUFFER State and then into the PPG ALC STORAGE */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-121 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_3128 */;
        satisfy req_IPOS_MAIN_CONTROLLER_121 by self;
        requirement def IPOS_MAIN_CONTROLLER_122 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_3129";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-122";
            doc /* When the ppg ioff calibration and the adc calibration are selected, the adc calibration shall be */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_122 : IPOS_MAIN_CONTROLLER_122;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-122 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_3129 | When the ppg ioff calibration and the adc calibration are selected, the adc calibration shall be */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-122 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_3129 */;
        satisfy req_IPOS_MAIN_CONTROLLER_122 by self;
        requirement def IPOS_MAIN_CONTROLLER_123 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_4079";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-123";
            doc /* If i_rst_async_ecg is set to 1, the start-up phase shall restart but no clock shall stop if enabled. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_123 : IPOS_MAIN_CONTROLLER_123;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-123 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_4079 | If i_rst_async_ecg is set to 1, the start-up phase shall restart but no clock shall stop if enabled. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-123 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_4079 */;
        satisfy req_IPOS_MAIN_CONTROLLER_123 by self;
        requirement def IPOS_MAIN_CONTROLLER_124 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_4080";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-124";
            doc /* If i_rst_async_ecg is set to 1, it shall go to zero at least 5ms after that o_su_hc2 is set to 0. */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_124 : IPOS_MAIN_CONTROLLER_124;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-124 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_4080 | If i_rst_async_ecg is set to 1, it shall go to zero at least 5ms after that o_su_hc2 is set to 0. */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-124 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_4080 */;
        satisfy req_IPOS_MAIN_CONTROLLER_124 by self;
        requirement def IPOS_MAIN_CONTROLLER_125 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_4090";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-125";
            doc /* If i_rst_async_bia is set to 1, the start-up phase shall restart but no clock shall stop if */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_125 : IPOS_MAIN_CONTROLLER_125;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-125 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_4090 | If i_rst_async_bia is set to 1, the start-up phase shall restart but no clock shall stop if */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-125 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_4090 */;
        satisfy req_IPOS_MAIN_CONTROLLER_125 by self;
        requirement def IPOS_MAIN_CONTROLLER_126 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_4091";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-126";
            doc /* If i_rst_async_bia is set to 1, it shall go to zero at least 5ms after that the o_sug_imp is set to 0 */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_126 : IPOS_MAIN_CONTROLLER_126;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-126 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_4091 | If i_rst_async_bia is set to 1, it shall go to zero at least 5ms after that the o_sug_imp is set to 0 */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-126 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_4091 */;
        satisfy req_IPOS_MAIN_CONTROLLER_126 by self;
        requirement def IPOS_MAIN_CONTROLLER_127 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_436";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-127";
            doc /* When in Sleep Mode and no Bio-Channel are selected, if every elaboration is ended and there are at least 34 clock cycles at 32kHz before the start of a new time slot, the o_en_ldo_1v8 shall go */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_127 : IPOS_MAIN_CONTROLLER_127;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-127 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_436 | When in Sleep Mode and no Bio-Channel are selected, if every elaboration is ended and there are at least 34 clock cycles at 32kHz before the start of a new time slot, the o_en_ldo_1v8 shall go */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-127 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_436 */;
        satisfy req_IPOS_MAIN_CONTROLLER_127 by self;
        requirement def IPOS_MAIN_CONTROLLER_128 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_5004";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-128";
            doc /* The max value that the user shall use for every m_channel (m_ecg, m_bia, m_gsr and m_ppg) is */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_128 : IPOS_MAIN_CONTROLLER_128;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-128 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_5004 | The max value that the user shall use for every m_channel (m_ecg, m_bia, m_gsr and m_ppg) is */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-128 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_5004 */;
        satisfy req_IPOS_MAIN_CONTROLLER_128 by self;
        requirement def IPOS_MAIN_CONTROLLER_129 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_5005";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-129";
            doc /* If the user set a value greater than 1024 into ones of the m_channel (see req 5004), the value shall clamp at 1024 (check the input i_m_ecg, i_m_bia, i_m_gsr or i_m_ppg into the main */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_129 : IPOS_MAIN_CONTROLLER_129;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-129 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_5005 | If the user set a value greater than 1024 into ones of the m_channel (see req 5004), the value shall clamp at 1024 (check the input i_m_ecg, i_m_bia, i_m_gsr or i_m_ppg into the main */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-129 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_5005 */;
        satisfy req_IPOS_MAIN_CONTROLLER_129 by self;
        requirement def IPOS_MAIN_CONTROLLER_130 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_5015";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-130";
            doc /* [Covers: DDS_STBIO1_1114] The State WAIT_SU shall not be considered interruptible. If the user wants to interrupt the WAIT_SU state, it shall perform the Soft Reset procedure described in the DDS */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_130 : IPOS_MAIN_CONTROLLER_130;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-130 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_5015 | [Covers: DDS_STBIO1_1114] The State WAIT_SU shall not be considered interruptible. If the user wants to interrupt the WAIT_SU state, it shall perform the Soft Reset procedure described in the DDS */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-130 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_5015 */;
        satisfy req_IPOS_MAIN_CONTROLLER_130 by self;
        requirement def IPOS_MAIN_CONTROLLER_131 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_5016";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-131";
            doc /* When an ECG, BIA or GSR Operation is selected and DS_SEL is set to 0, The DATA Output for these two channels shall be written in the following regmap registers ECG0_AC ECG0_DC ECG1_BIA_P_AC ECG1_BIA_P_DC ECG2_BIA_Q_AC ECG2_BIA_Q_DC GSR_RESULT */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_131 : IPOS_MAIN_CONTROLLER_131;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-131 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_5016 | When an ECG, BIA or GSR Operation is selected and DS_SEL is set to 0, The DATA Output for these two channels shall be written in the following regmap registers ECG0_AC ECG0_DC ECG1_BIA_P_AC ECG1_BIA_P_DC ECG2_BIA_Q_AC ECG2_BIA_Q_DC GSR_RESULT */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-131 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_5016 */;
        satisfy req_IPOS_MAIN_CONTROLLER_131 by self;
        requirement def IPOS_MAIN_CONTROLLER_132 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_5092";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-132";
            doc /* i_rst_async_bia shall be used also to reset the START-UP phase for ECG channel 1 and */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_132 : IPOS_MAIN_CONTROLLER_132;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-132 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_5092 | i_rst_async_bia shall be used also to reset the START-UP phase for ECG channel 1 and */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-132 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_5092 */;
        satisfy req_IPOS_MAIN_CONTROLLER_132 by self;
        requirement def IPOS_MAIN_CONTROLLER_133 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_6070";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-133";
            doc /* When i_wave_velocity mode is enabled together with the DISABLE_ALC, the PPG_ALC_STORAGE shall be performed but once the Device goes into OPERATIVE State, the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_133 : IPOS_MAIN_CONTROLLER_133;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-133 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_6070 | When i_wave_velocity mode is enabled together with the DISABLE_ALC, the PPG_ALC_STORAGE shall be performed but once the Device goes into OPERATIVE State, the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-133 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_6070 */;
        satisfy req_IPOS_MAIN_CONTROLLER_133 by self;
        requirement def IPOS_MAIN_CONTROLLER_134 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_6098";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-134";
            doc /* When i_wave_velocity_mode is set to 1, the ALC Compensation shall be set only when the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_134 : IPOS_MAIN_CONTROLLER_134;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-134 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_6098 | When i_wave_velocity_mode is set to 1, the ALC Compensation shall be set only when the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-134 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_6098 */;
        satisfy req_IPOS_MAIN_CONTROLLER_134 by self;
        requirement def IPOS_MAIN_CONTROLLER_135 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_6129";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-135";
            doc /* When i_ALC_comp_start is set to 1, the first rise of the o_comp_rx_ck shall happen at least after */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_135 : IPOS_MAIN_CONTROLLER_135;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-135 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_6129 | When i_ALC_comp_start is set to 1, the first rise of the o_comp_rx_ck shall happen at least after */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-135 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_6129 */;
        satisfy req_IPOS_MAIN_CONTROLLER_135 by self;
        requirement def IPOS_MAIN_CONTROLLER_136 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_7095";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-136";
            doc /* All the PPG_FSM state shall be checked using the PPG_STATUS_REGISTER in Regmap (the */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_136 : IPOS_MAIN_CONTROLLER_136;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-136 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_7095 | All the PPG_FSM state shall be checked using the PPG_STATUS_REGISTER in Regmap (the */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-136 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_7095 */;
        satisfy req_IPOS_MAIN_CONTROLLER_136 by self;
        requirement def IPOS_MAIN_CONTROLLER_137 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_728";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-137";
            doc /* At the end of ALC compensation, if ALC is not masked, o_w_BTIA_ALC relative to the running frame, shall be set to output system (check when i_end_of_compensation rise in PPG FSM). If */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_137 : IPOS_MAIN_CONTROLLER_137;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-137 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_728 | At the end of ALC compensation, if ALC is not masked, o_w_BTIA_ALC relative to the running frame, shall be set to output system (check when i_end_of_compensation rise in PPG FSM). If */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-137 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_728 */;
        satisfy req_IPOS_MAIN_CONTROLLER_137 by self;
        requirement def IPOS_MAIN_CONTROLLER_138 : SourceRequirement {
            attribute sourceReqId = "IPOS_STBIO1_MAIN_CONTROLLER_8106";
            attribute sourceArtifact = "data/canonical/canonical_store.sqlite";
            attribute sourceContext = "IPOS-MAIN-CONTROLLER-138";
            doc /* If multiple frame is selected (i_frame_repetition in ppg_fsm greater than 0), when Tx Preset falls from 1 to 0, the en_tx shall pass from 1 to 0 only during the last repetition (check that when */;
        }
        requirement req_IPOS_MAIN_CONTROLLER_138 : IPOS_MAIN_CONTROLLER_138;
        doc /* iposReqId=IPOS-MAIN-CONTROLLER-138 | sourceReqId=IPOS_STBIO1_MAIN_CONTROLLER_8106 | If multiple frame is selected (i_frame_repetition in ppg_fsm greater than 0), when Tx Preset falls from 1 to 0, the en_tx shall pass from 1 to 0 only during the last repetition (check that when */;
        doc /* coverageDependency: IPOS-MAIN-CONTROLLER-138 -> approved source requirement IPOS_STBIO1_MAIN_CONTROLLER_8106 */;
        satisfy req_IPOS_MAIN_CONTROLLER_138 by self;
    }

}

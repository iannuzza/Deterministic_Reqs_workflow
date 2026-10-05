# RAG Query Results
- Timestamp: 2026-09-21 10:46:58
- Query: adc error cap debug calibration bypass
- Mode: hybrid
- Requested mode: hybrid
- Normalized Query: adc error cap debug calibration bypass analog digital converter test_debug test scan bist dft self analog_to_digital
- Normalized FTS Query: adc OR error OR cap OR debug OR calibration OR bypass OR analog OR digital OR converter OR test_debug OR test OR scan OR bist OR dft OR self OR analog_to_digital
- Top K: 5
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: not requested
- Automatic semantic fallback: not used
- Requirement-ID mapping check: not_applicable
## Result 1
- chunk_id: 225
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 83
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 1
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -32.095116
- semantic_score: (not returned)
- rrf_score: 0.016393
- normalized_terms: half_charge_ldo output 0 o_adc_start adc start sampling sample o_n_step2_to_reg rx_ch_gain_limit 1 n_step2 calibration value o_adc_test_cap 9 test cap o_adc_error_cap9 7 result o_adc_error_cap8 6 o_adc_error_cap7 o_adc_error_cap6 analog digital converter acquire acquir acquisition test_debug debug scan bist dft self analog_to_digital

```text
half_charge_ldo output  0  
o_ADC_start output  0 ADC Start sampling 
o_N_step2_to_reg output [rx_ch_gain_limit-1:0] 0 N_Step2 calibration value 
o_adc_test_cap output [9:0] 0 adc test cap 
o_adc_error_cap9 output [7:0] 0 adc calibration result 
o_adc_error_cap8 output [6:0] 0 adc calibration result 
o_adc_error_cap7 output [6:0] 0 adc calibration result 
o_adc_error_cap6 output [6:0] 0 adc calibration result
```

## Result 2
- chunk_id: 216
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 78
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 2
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -26.366950
- semantic_score: (not returned)
- rrf_score: 0.016129
- normalized_terms: ap_idac input 1 0 enabling enabl cap idac i_adc_mux_bio_channel_debug 2 debug adc mux bio channel i_adc_mux_sel_debug analog digital converter test_debug test scan bist dft self analog_to_digital digital_to_analog

```text
ap_idac input [1:0]  enabling cap for idac 
i_adc_mux_bio_channel_debug input [2:0]  enabling debug adc mux bio channel 
i_adc_mux_sel_debug input   enabling adc mux
```

## Result 3
- chunk_id: 341
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 146
- section: 15.2. Configuration Phase
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 3
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -24.352935
- semantic_score: (not returned)
- rrf_score: 0.015873
- normalized_terms: 15 2 configuration configure phase dds_stbio1 0117 requirement during dur idle state device_fsm user able bio channel optical adc calibration then start measurement cycle put device debug mode ipos_main_ctrl end analog digital converter config test_debug test scan bist dft self analog_to_digital

```text
15.2. Configuration Phase 
 
[DDS_STBIO1_ 0117] Requirement: 
During the Configuration Phase (IDLE STATE of the Device_FSM), the user shall be able to: 
• Configure Bio-Channel or Optical Channel, the ADC Calibration and then Start a 
measurement cycle. 
• Put the device in Debug-Mode. [TO: IPOS_MAIN_CTRL] [END]
```

## Result 4
- chunk_id: 372
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 160
- section: 18.3. ADC TEST LOW NOISE
- source_type: text
- chunk_index: 4
- rank_lexical: (not returned)
- rank_normalized: 4
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -23.252988
- semantic_score: (not returned)
- rrf_score: 0.015625
- normalized_terms: data 0x06 select page 2 regmap address 0x40 0x02 enable adc test low noise input gpio 0x0a 0x14 3 analog digital converter test_debug debug scan bist dft self analog_to_digital

```text
, DATA=0x06) 
• Select page 2 of the regmap (ADDRESS=0x40, DATA=0x02) 
• Enable ADC TEST LOW NOISE and input of ADC from GPIO (ADDRESS=0x0A, 
DATA=0x14) 
• Select page 3 of the regmap (ADDRESS=0x40, DATA=0x02)
```

## Result 5
- chunk_id: 219
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 80
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 5
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -23.033225
- semantic_score: (not returned)
- rrf_score: 0.015385
- normalized_terms: 79 port name direction type output reset value description i_nmax_to_reg input nmax_bit_top 1 0 max digital ramp i_nstart_case n_start frist sterp i_debug_rx_ch rx_ch_frame_n_bit_top enabling enabl debug rx channel i_t_delta1_to_reg delta_bit_top delta time i_gain_max_set gain_max_bit_top gain alc i_btia_alc_debug btia_alc_register_bit_top btia enable i_comp_rx_out analog comparator i_adc_error_cap8_debug 6 adc cap error i_adc_error_cap7_debug i_adc_error_cap6_debug i_adc_error_cap5_debug i_adc_error_cap4_debug i_adc_error_cap3_debug i_adc_error_cap2_debug i_adc_error_cap1_debug i_adc_error_cap0_debug i_bidac_debug_register idac_offset i_sleep_master i_lpm low power mode ldo i_mpm converter dropout regulator clock_reset clock clk rst rst_n resetn por test_debug test scan bist dft self power_on_reset analog_to_digital digital_to_analog

```text
79 
 
Port name Direction Type Output 
Reset Value Description 
i_Nmax_to_reg input [Nmax_bit_top-1:0]  Max value for digital ramp 
i_nstart_case input [Nmax_bit_top-1:0]  n_start value for frist sterp 
i_debug_rx_ch input [rx_ch_frame_n_bit_top-1:0]  enabling debug for rx channel 
i_T_delta1_to_reg input [delta_bit_top-1:0]  delta 1 time for digital ramp 
i_gain_max_set input [gain_max_bit_top-1:0]  gain max for alc 
i_BTIA_ALC_debug input [BTIA_ALC_register_bit_top-1:0]  BTIA ALC Debug enable 
i_comp_rx_out input   input from analog comparator 
i_adc_error_cap8_debug input [6:0]  adc cap error debug 
i_adc_error_cap7_debug input [6:0]  adc cap error debug 
i_adc_error_cap6_debug input [6:0]  adc cap error debug 
i_adc_error_cap5_debug input [6:0]  adc cap error debug 
i_adc_error_cap4_debug input [6:0]  adc cap error debug 
i_adc_error_cap3_debug input [6:0]  adc cap error debug 
i_adc_error_cap2_debug input [6:0]  adc cap error debug 
i_adc_error_cap1_debug input [6:0]  adc cap error debug 
i_adc_error_cap0_debug input [6:0]  adc cap error debug 
i_BIDAC_debug_register input [IDAC_offset-1:0]   
i_sleep_master input    
i_lpm input [1:0]  low power mode for ldo 
i_mpm input [1:0
```


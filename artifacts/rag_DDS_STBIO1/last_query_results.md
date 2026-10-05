# RAG Query Results
- Timestamp: 2026-09-14 11:21:52
- Query: ADC TEST FAST DDS_STBIO1_1507
- Mode: hybrid
- Requested mode: auto
- Normalized Query: adc test fast dds_stbio1_1507 analog digital converter test_debug debug scan bist dft self analog_to_digital
- Normalized FTS Query: adc OR test OR fast OR dds_stbio1_1507 OR analog OR digital OR converter OR test_debug OR debug OR scan OR bist OR dft OR self OR analog_to_digital
- Top K: 5
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: not requested
- Automatic semantic fallback: not used
- Requirement-ID mapping check: pass
## Result 1
- chunk_id: 373
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 161
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 1
- rank_normalized: 2
- rank_semantic: (not returned)
- lexical_score: -13.381970
- normalized_score: -25.216533
- semantic_score: (not returned)
- rrf_score: 0.032522
- normalized_terms: 160 enable debug mode writing writ regmap address 0x3e data 0x08 end 18 4 adc test fast dds_stbio1_1507 requirement turn low noise select page 3 0x40 0x03 ldo 1v8 viref_ldo1v8_clk16m register 0xf 0x02 clock 0x0f 0x12 0x09 0x06 2 input gpio 0x0a 0x0c 5 bist dds_stbio1_2507 after initial boot phase analog digital converter dropout regulator built self clock_reset clk reset rst rst_n resetn por power_startup power up startup start initialization wake test_debug scan dft power_up analog_to_digital

```text
160 
 
• Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) 
 
 
[End] 
 
 
18.4. ADC TEST FAST  
[DDS_STBIO1_1507] Requirement: 
To turn on the ADC TEST LOW NOISE mode shall be: 
• Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) 
• Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register 
(ADDRESS=0xF, DATA=0x02) 
• Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register 
(ADDRESS=0x0F, DATA=0x12) 
• Enable ADC in debug mode (ADDRESS=0x09, DATA=0x06) 
• Select page 2 of the regmap (ADDRESS=0x40, DATA=0x02) 
• Enable ADC TEST LOW NOISE and input of ADC from GPIO (ADDRESS=0x0A, 
DATA=0x0C) 
• Select page 3 of the regmap (ADDRESS=0x40, DATA=0x02) 
• Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) 
 
 
 
 
[End] 
 
18.5. BIST MODE  
[DDS_STBIO1_2507] Requirement: 
After the initial boot phase, to turn on the Debug mode shall be: 
• Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03)
```

## Result 2
- chunk_id: 10
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 3
- section: (unknown)
- source_type: text
- chunk_index: 4
- rank_lexical: (not returned)
- rank_normalized: 1
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -26.410219
- semantic_score: (not returned)
- rrf_score: 0.016393
- normalized_terms: 156 17 2 3 top level approach 157 18 digital dft 158 1 scan mode debug adc test low noise 159 4 fast 160 5 bist analog converter built self design test_debug analog_to_digital

```text
................................................................................... 156 
17.2.3. Top Level Approach ................................................................................. 157 
18. Digital DFT ................................ ................................ ................................ ................... 158 
18.1. Scan mode ................................ ................................ ................................ ............... 158 
18.2. Debug mode ................................ ................................ ................................ ............. 158 
18.3. ADC TEST LOW NOISE ................................ ................................ ........................... 159 
18.4. ADC TEST FAST ................................ ................................ ................................ ...... 160 
18.5. BIST MODE ................................ ................................ ................................ .............. 160
```

## Result 3
- chunk_id: 216
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 78
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 3
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -23.827572
- semantic_score: (not returned)
- rrf_score: 0.015873
- normalized_terms: ap_idac input 1 0 enabling enabl cap idac i_adc_mux_bio_channel_debug 2 debug adc mux bio channel i_adc_mux_sel_debug analog digital converter test_debug test scan bist dft self analog_to_digital digital_to_analog

```text
ap_idac input [1:0]  enabling cap for idac 
i_adc_mux_bio_channel_debug input [2:0]  enabling debug adc mux bio channel 
i_adc_mux_sel_debug input   enabling adc mux
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
- chunk_id: 145
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 41
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 5
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -21.801315
- semantic_score: (not returned)
- rrf_score: 0.015385
- normalized_terms: tput wire 16mhz clock adc dft o_clk_gsr_16m output gsr digital domain o_adc_clk_serial_dft serial o_sh_clk_gate status statu clk reg sh analog converter design test clock_reset reset rst rst_n resetn por interrupt irq event flag test_debug debug scan bist self analog_to_digital

```text
tput wire 16MHz clock for ADC DFT 
o_clk_gsr_16M output wire gsr clock to digital domain 
o_ADC_clk_serial_dft output wire adc serial clock in dft 
o_sh_clk_gate output wire status clk reg clk sh 16Mhz
```

## Requirement-ID Mapping Check

```json
{
  "query_ids": [
    "DDS_STBIO1_1507"
  ],
  "status": "pass",
  "checks": [
    {
      "source_req_id": "DDS_STBIO1_1507",
      "known_in_stage1": true,
      "expected_owner": "ADC",
      "evidence_chunk_ids": [
        373
      ],
      "evidence_match": true
    }
  ]
}
```


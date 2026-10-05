# RAG Query Results
- Timestamp: 2026-09-04 15:47:09
- Query: clock gating
- Mode: semantic
- Requested mode: semantic
- Normalized Query: clock gating gat clock_reset clk reset rst rst_n resetn por clock_gating
- Normalized FTS Query: clock OR gating OR gat OR clock_reset OR clk OR reset OR rst OR rst_n OR resetn OR por OR clock_gating
- Top K: 3
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: available
- Automatic semantic fallback: not used
- Requirement-ID mapping check: not_applicable
## Result 1
- chunk_id: 143
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 40
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: (not returned)
- semantic_score: 0.408248
- rrf_score: (not used)
- normalized_terms: re fifo clock clk_masterblaze_m output wire sensor hub master clk_masterblaze_s clk_masterblaze slave clk_regmap regmap o_clk_ext_en enable external first out clock_reset clk reset rst rst_n resetn por storage_buffer store stor storage buffer queue

```text
re fifo clock 
clk_masterblaze_m output wire sensor hub master clock 
clk_masterblaze_s output wire sensor hub slave clock 
clk_regmap output wire regmap clock 
o_clk_ext_en output wire enable external clock
```

## Result 2
- chunk_id: 305
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 129
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: (not returned)
- semantic_score: 0.341882
- rrf_score: (not used)
- normalized_terms: 128 clock memory ports port atpg mode 0 functional 1 test ca_stredl_bist_c_tst_mem selck_4 input bist select u_ca_fifo_bist_c_oen_1 ca_stredl_bist_c_par_mem sel parallel selection bus b0 built self clock_reset clk reset rst rst_n resetn por test_debug debug scan dft power_on_reset power

```text
128 
 
clock and 
memory 
ports in 
ATPG mode 
0: 
Functional 
Clock / 
Functional 
Ports 1: 
Test Clock/ 
Test Ports 
ca_stredl_bist_c_tst_mem_
selck_4 input 
BIST To 
select the 
clock and 
memory 
ports in 
ATPG mode 
0: 
Functional 
Clock / 
Functional 
Ports 1: 
Test Clock/ 
Test Ports 
u_ca_fifo_bist_c_oen_1 
 
ca_stredl_bist_c_par_mem
sel input 
BIST 
Parallel 
Memory 
Selection 
Bus 
{ 1'b0, u_ca_fifo_bist_c_oen_1, 
u_ca_fifo_bist_c_oen_1, 
u_ca_fifo_bist_c_oen_1 }
```

## Result 3
- chunk_id: 142
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 40
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: (not returned)
- semantic_score: 0.326327
- rrf_score: (not used)
- normalized_terms: 39 i_en_clk_16mhz_sleep input wire enable clock sleep mode when bio channel selected select en_adc_test_low_noise adc test low noise en_adc_test_fast fast if_sh_ck_in sensor hub interface o_en_ldo1v8 output ldo analog domain o_pd_clkf power down 16mhz o_clk_16m_ready ready digital o_dis_rc_viref dis rc viref pd_osc_clk32k clk 64khz tst_clk_32k slow 32k main_controller tst_clk_16m 16m tst_clk_bistctlr bist ctrl tst_rst_bistctlr_n reset clk_stredl gating gat logic inside stredl_afe_top clk_xbar xbar clk_intf clk_main_ctrl main controller clk_stmc adsp clk_stmc_ahb elaboration clk_fifo fifo clk_masterblaze_m master clk_masterblaze_s clk_masterblaze slave clk_regmap reg converter dropout regulator first out built self clock_reset rst rst_n resetn por storage_buffer store stor storage buffer queue test_debug debug scan dft clock_gating analog_to_digital

```text
39 
 
i_en_clk_16MHz_sleep input wire enable clock in SLEEP mode when a bio-
channel is selected 
EN_ADC_TEST_LOW_NOISE input wire enable adc test low noise 
EN_ADC_TEST_FAST input wire enable adc test fast 
if_sh_ck_in input wire sensor hub clock interface 
o_EN_LDO1V8 output wire enable ldo to analog domain 
o_PD_CLKF output wire power down 16MHz clock to analog domain 
o_CLK_16M_READY output wire clock ready to the digital domain 
o_DIS_RC_VIREF output wire dis rc viref to the analog domain 
pd_osc_clk32k output wire power down for clk 64kHz 
tst_clk_32k output wire clock slow 32k to main_controller 
tst_clk_16m output wire clock fast 16M 
tst_clk_bistctlr output wire test clock for bist ctrl 
tst_rst_bistctlr_n output wire test reset for bist ctrl 
clk_stredl output wire clock gating logic inside stredl_afe_top 
clk_xbar output wire xbar clock 
clk_intf output wire interface clock 
clk_main_ctrl output wire clock for main controller 
clk_stmc output wire adsp clock 
clk_stmc_ahb output wire adsp clk elaboration 
clk_fifo output wire fifo clock 
clk_masterblaze_m output wire sensor hub master clock 
clk_masterblaze_s output wire sensor hub slave clock 
clk_regmap output wire reg
```


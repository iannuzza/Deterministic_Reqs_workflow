# RAG Query Results
- Timestamp: 2026-09-04 15:41:03
- Query: clock gating
- Mode: hybrid-semantic
- Requested mode: hybrid-semantic
- Normalized Query: clock gating gat clock_reset clk reset rst rst_n resetn por clock_gating
- Normalized FTS Query: clock OR gating OR gat OR clock_reset OR clk OR reset OR rst OR rst_n OR resetn OR por OR clock_gating
- Top K: 3
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: unavailable
- Semantic diagnostic: local embedding model not found: C:\Users\iannuzza\LOCAL_PROJ\Github_copilot_proj\STBIO_AI\models\local_embedding_model
- Automatic semantic fallback: not used
- Requirement-ID mapping check: not_applicable
## Result 1
- chunk_id: 140
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 39
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 1
- rank_normalized: 4
- rank_semantic: (not returned)
- lexical_score: -8.237966
- normalized_score: -21.450899
- semantic_score: (not returned)
- rrf_score: 0.032018
- normalized_terms: 38 clk_en_s4 input wire clock gating gat logic inside stredl_afe_top clk_en_s5 masterblaze_ahb clk_en_m0 clk_en_m1 hsel m1 xbar stmc ahb slave clk_en_m2 m2 fifo clk_en_m22 masterblaze clk_en_m3 m3 regmap iso_i register vdden_i enable ispu power island i_start_operative_16mhz lead check main_ctrl_sw_resetn soft reset main controller stmc_sw_resetn adsp fifo_sw_resetn masterblaze_sw_resetn sensor hub regmap_sw_resetn adsp_run running run adsp_xbar_sw_en clk i_en_clk_gsr_16m gsr digital circuit i_en_ck_m_p_q quadrature phase i_en_clk_mod_debug modulation debug i_en_chop_ref chopper i_en_ck_chop_imp bia i_en_ck_hc2_10k wi first out clock_reset rst rst_n resetn por storage_buffer store stor storage buffer queue test_debug test scan bist dft self clock_gating

```text
38 
 
clk_en_s4 input wire clock gating logic inside stredl_afe_top 
clk_en_s5 input wire clock gating logic inside masterblaze_ahb 
clk_en_m0 input wire clock gating logic inside stredl_afe_top 
clk_en_m1 input wire HSEL M1 from xbar to STMC AHB Slave 
clk_en_m2 input wire HSEL M2 from xbar to FIFO 
clk_en_m22 input wire HSEL M2 from xbar to MASTERBLAZE 
clk_en_m3 input wire HSEL M3 from xbar to Regmap 
iso_i input wire from register 
vdden_i input wire enable ISPU Power Island 
i_start_operative_16MHz input wire enable the lead of check 
main_ctrl_sw_resetn input wire soft reset for main controller 
stmc_sw_resetn input wire adsp soft reset 
fifo_sw_resetn input wire fifo soft reset 
masterblaze_sw_resetn input wire sensor hub soft reset 
regmap_sw_resetn input wire regmap soft reset 
adsp_run input wire adsp is running 
adsp_xbar_sw_en input wire adsp clk ahb 
i_en_clk_gsr_16M input wire enable the clock for gsr digital circuit 
i_en_ck_m_p_q input wire enable quadrature and phase clock 
i_en_clk_mod_debug input wire enable the clock modulation debug 
i_en_chop_ref input wire enable chopper clock 
i_en_ck_chop_imp input wire enable chopper clock for bia 
i_en_ck_hc2_10k input wi
```

## Result 2
- chunk_id: 154
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 45
- section: 13.1.1.4. Clocks and Reset
- source_type: figure
- chunk_index: 2
- rank_lexical: 5
- rank_normalized: 1
- rank_semantic: (not returned)
- lexical_score: -6.093608
- normalized_score: -24.871961
- semantic_score: (not returned)
- rrf_score: 0.031778
- normalized_terms: clocks clock scheme shown below figure 9 above req_id source target path delay gating gat analog control description f max requirements requirement definition dds_stbio1 1020 stbio1_top clk_16m dig_wrapper_lv u_pmu clk 16m no pwr_down controlled pmu 16 mhz 1021 clk_64k 64k 64 khz power management unit clock_reset reset rst rst_n resetn por clock_gating

```text
Clocks scheme is shown in the below figure 
 
Figure 9: Clocks Scheme 
Clocks scheme is shown in the above figure 
Req_ID Source Target Path Delay Clock Gating 
Analog Control 
and Description F Max 
Requirements 
Definition 
DDS_STBIO1_
1020 stbio1_top.clk_16m stbio1_top.dig_wrapper_LV.u_pmu.clk
_16m 
 No 
Pwr_down 
controlled by pmu 16 MHz 
DDS_STBIO1_
1021 stbio1_top.clk_64k stbio1_top.dig_wrapper_LV.u_pmu.clk
_64k  No 
No 
64 kHz
```

## Result 3
- chunk_id: 303
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 127
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 3
- rank_normalized: 3
- rank_semantic: (not returned)
- lexical_score: -7.525901
- normalized_score: -21.539393
- semantic_score: (not returned)
- rrf_score: 0.031746
- normalized_terms: 126 test_se one per collar provided provid top level ca_stredl_bist_c_tst_gated ca_stredl_bist_c_tst_gat clock input bist gating gat signal entire used force cell transparenc y atpg mode u_pad_mux_scan_enable_sig ca_stredl_bist_c_tst_reset mux bypass reset synchronize r allows allow synchronizin g circuit u_pad_mux_scan_mode_sig ca_stredl_bist_c_oen_1 memory output enable 1 u_ca_fifo_bist_c_oen_1 ca_stredl_bist_c_oen_2 2 ca_stredl_bist_c_oen_3 3 ca_stredl_bist_c_oen_4 built self test clock_reset clk rst rst_n resetn por test_debug debug scan dft clock_gating

```text
126 
 
test_se (one 
test_se per 
collar) is 
provided at 
the top level 
ca_stredl_bist_c_tst_gated
clock input 
BIST Clock 
Gating 
Signal for 
the entire 
BIST. Used 
to force 
clock gating 
cell 
transparenc
y in ATPG 
mode . 
u_pad_mux_scan_enable_sig 
 
ca_stredl_bist_c_tst_reset_
mux input 
BIST 
Bypass for 
reset 
synchronize
r. allows to 
force reset 
synchronizin
g circuit 
transparenc
y in ATPG 
mode. 
u_pad_mux_scan_mode_sig 
 
ca_stredl_bist_c_oen_1 input 
BIST 
Memory 
Output 
Enable 1 
u_ca_fifo_bist_c_oen_1 
 
ca_stredl_bist_c_oen_2 input 
BIST 
Memory 
Output 
Enable 2 
u_ca_fifo_bist_c_oen_1 
 
ca_stredl_bist_c_oen_3 input 
BIST 
Memory 
Output 
Enable 3 
u_ca_fifo_bist_c_oen_1 
 
ca_stredl_bist_c_oen_4 input BIST 
Memory 
u_ca_fifo_bist_c_oen_1
```


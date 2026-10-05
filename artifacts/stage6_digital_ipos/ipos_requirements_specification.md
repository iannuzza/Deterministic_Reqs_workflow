# Digital IPOS

- Snapshot: `snap-d91e3852a6d9230582c4677f`

## Requirements

**[IPOS-DIG-REQ-001] Requirement:**
In case the ppg sample data are equal (once converted in two’s complement) at 0x8000 or 0x7FFF for at least half of the selected average (example, if 128 acquisitions are selected, the threshold shall be greater or equal to 64), o_saturation_flag shall be set to 1 and shall go to 0 at the start of the next frame or frame repetition.

Covers: DRS-REQ-001
Canonical requirement: can-011c746f4576d0e7a100c158
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_2146
Mapped block: Main Controller

**[IPOS-DIG-REQ-002] Requirement:**
When the input signal o_Tx_preset is set to 1, the o_Tx_Vref shall increment the first step at value i_N_start (DIGITAL_RAMP_CONFIG_PARAM_3 register [2:0]) at a time i_T_preset

Covers: DRS-REQ-002
Canonical requirement: can-011daeee867c323a0ae96acc
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_118
Mapped block: Main Controller

**[IPOS-DIG-REQ-003] Requirement:**
The Sampling Phase shall be configurable by the user with i_N_clk values from 0 up to 63. This

Covers: DRS-REQ-003
Canonical requirement: can-01f182f10b0d865efd7969a8
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_051
Mapped block: Main Controller

**[IPOS-DIG-REQ-004] Requirement:**
Tx Preset shall be set to 0 before the rising phase(i_start_digtal_ramp) and after the falling phase

Covers: DRS-REQ-004
Canonical requirement: can-041fb76373c84db860ea3aee
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1104
Mapped block: Main Controller

**[IPOS-DIG-REQ-005] Requirement:**
The o_pd_tia, o_pd_idac and o_pd_pga shall be the negated version the o_en_tia, o_en_idac

Covers: DRS-REQ-005
Canonical requirement: can-04f2ffd84185ea0ceb40d37d
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1095
Mapped block: Main Controller

**[IPOS-DIG-REQ-006] Requirement:**
When in Rx_Start_Up state, the o_tx_Preset shall be set 0, the en_tx_i shall be set to 1, the o_BIDAC shall maintain the value reached during the ALC Compensation summed up, if i_ppg_ioff_calibration is enabled, with the IOFF_OFFSET computed during the IOFF Calibration

Covers: DRS-REQ-006
Canonical requirement: can-07ad9cbabb43ef1c31890d6c
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_100
Mapped block: Main Controller

**[IPOS-DIG-REQ-007] Requirement:**
i_rst_async_bia shall be used also to reset the START-UP phase for ECG channel 1 and

Covers: DRS-REQ-007
Canonical requirement: can-07ce0e279b04048385ba0fbe
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_5092
Mapped block: Main Controller

**[IPOS-DIG-REQ-008] Requirement:**
If i_rst_async_bia is set to 1, it shall go to zero at least 5ms after that the o_sug_imp is set to 0

Covers: DRS-REQ-008
Canonical requirement: can-0850a5f6f2e098934124e9a0
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_4091
Mapped block: Main Controller

**[IPOS-DIG-REQ-009] Requirement:**
When in FIRST_ALC_SAMPLES state, the o_start_ADC signal shall be set high until

Covers: DRS-REQ-009
Canonical requirement: can-09db1e7f4b10eb486009f9c7
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_102
Mapped block: Main Controller

**[IPOS-DIG-REQ-010] Requirement:**
When only GSR is selected (NO ECG0 and PPG are selected), if i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] is greater than 0, the Device FSM shall go in SLEEP after the IDLE State and shall go back in Operative State only when the measurement shall be run or, in case of

Covers: DRS-REQ-010
Canonical requirement: can-0a08d641b0779c72957f6a40
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_094
Mapped block: Main Controller

**[IPOS-DIG-REQ-011] Requirement:**
When the wave velocity mode is selected and the device FSM is in WAIT_SU, the Elaboration FSM shall go into the TIMER BUFFER State and then into the PPG ALC STORAGE

Covers: DRS-REQ-011
Canonical requirement: can-0b84927188517dfc3737d303
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_3128
Mapped block: Main Controller

**[IPOS-DIG-REQ-012] Requirement:**
When i_wave_velocity_mode is set to 1, the ALC Compensation shall be set only when the

Covers: DRS-REQ-012
Canonical requirement: can-0cf996371a1a792210355bcc
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_6098
Mapped block: Main Controller

**[IPOS-DIG-REQ-013] Requirement:**
When the i_ADC_en_mc and i_adc_en_mask is set to 0, all the output shall be set to 0, except for the o_end_cal_phases and o_ADC_clk_en. The o_end_cal_phases shall be set to 1 if i_do_calibration (bit 0 of ADC_CAL_CONFIG) is set to 0, otherwise shall be set to 0 until the end

Covers: DRS-REQ-013
Canonical requirement: can-114142433bdf80440779a8d4
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_052
Mapped block: Main Controller

**[IPOS-DIG-REQ-014] Requirement:**
When the HC_EN (ECG_CTRL register [0]) is set to 0 and IMP_EN (IMP_CTRL register [0]) is set to 1 and ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL register [1]) is set to 1, ECG1 and ECG2 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall remain high, O_PD_IMP shall go low and the Device_FSM shall go to the WAIT_SU State, so main_controller_status_register

Covers: DRS-REQ-014
Canonical requirement: can-130eb724d155384ced5c8bf0
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_011
Mapped block: Main Controller

**[IPOS-DIG-REQ-015] Requirement:**
In Order to enable a GSR Channel Operation, the user shall always select the GSR channel

Covers: DRS-REQ-015
Canonical requirement: can-207ee9b69e0e0a98b964248f
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1009
Mapped block: Main Controller

**[IPOS-DIG-REQ-016] Requirement:**
If en_gsr_cds is set low [bit 3 of GSR_CTRL], the gsr_curr_on shall set high in every time slot

Covers: DRS-REQ-016
Canonical requirement: can-2611cc3225a4b8c9304706b3
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_092
Mapped block: Main Controller

**[IPOS-DIG-REQ-017] Requirement:**
When an ECG, BIA or GSR Operation is selected and DS_SEL is set to 0, The DATA Output for these two channels shall be written in the following regmap registers ECG0_AC ECG0_DC ECG1_BIA_P_AC ECG1_BIA_P_DC ECG2_BIA_Q_AC ECG2_BIA_Q_DC GSR_RESULT

Covers: DRS-REQ-017
Canonical requirement: can-275d328600dfb32d0048853b
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_5016
Mapped block: Main Controller

**[IPOS-DIG-REQ-018] Requirement:**
When ECG, BIA or GSR Is sampled, i_ADC_en is equal to 1, the o_ADC_clk_en shall be set to 1.

Covers: DRS-REQ-018
Canonical requirement: can-283404e191d8ae826034f620
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_049
Mapped block: Main Controller

**[IPOS-DIG-REQ-019] Requirement:**
When the user selects an operative mode that includes the BIA channel, a start-up shall be done.

Covers: DRS-REQ-019
Canonical requirement: can-2b729ab58ce59eb5c4f6c3c7
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_080
Mapped block: Main Controller

**[IPOS-DIG-REQ-020] Requirement:**
Tx Preset shall be set to 1 a configurable TX_Preset_Step time before the start of the Digital

Covers: DRS-REQ-020
Canonical requirement: can-2c2dde1a892e7df6198323bf
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1102
Mapped block: Main Controller

**[IPOS-DIG-REQ-021] Requirement:**
Once the PPG Raw Data and PPG Noise reach the i_n_average_ppg value , depending on the ALC Mask bit value, the two accumulated shall be subtracted and final results shall be computed as follow: I_N_Average_PPG Samples Result with ALC MASK=0 Result with ALC Mask=1 0 3= (N1+P+N2) (Acc_P-(Acc_N)/2) * 8 Acc_P*16 2 4= (N1+2P+N2) (Acc_P -(Acc_N)) * 4 Acc_P *8 4 8= (2N1+4P+2N2) (Acc_P -(Acc_N)) * 2 Acc_P *4 8 16= (4N1+8P+4N2) (Acc_P -(Acc_N)) Acc_P *2 16 32= (8N1+16P+8N2) (Acc_P -(Acc_N))/2 Acc_P 32 64= (16N1+32P+16N2) (Acc_P -(Acc_N))/4 Acc_P /2 64 128= (32N1+64P+32N2) (Acc_P -(Acc_N))/8 Acc_P /4 128 256= (64N1+128P+64N2) (Acc_P -(Acc_N))/16 Acc_P /8 Table 18: PPG Result Table Where PPG Raw Data is indicated as P and PPG Noise is indicated as N1 and N2, while Acc_P

Covers: DRS-REQ-021
Canonical requirement: can-2d69243af8e7f0e817ebf499
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_140
Mapped block: Main Controller

**[IPOS-DIG-REQ-022] Requirement:**
When DEVICE_FSM FSM is in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) if HC_EN (ECG_CTRL register [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL [0]) is set to 1 and ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL [1]) is set to 1, after WAIT_SU the device_fsm shall go in

Covers: DRS-REQ-022
Canonical requirement: can-308fba69d3530281d3375e94
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_026
Mapped block: Main Controller

**[IPOS-DIG-REQ-023] Requirement:**
Once in the ERROR state, the user shall wait 1ms before set to 0 the MODE_OPERATION to go

Covers: DRS-REQ-023
Canonical requirement: can-31b834abae8de8b9bd36048d
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1034
Mapped block: Main Controller

**[IPOS-DIG-REQ-024] Requirement:**
When the i_m_ppg ( SET_PPG_FREQ_h and SET_PPG_FREQ_l) is different from 0 and PPG_SEL in DEVICE_CONFIG_CHANNEL register is set to 1, when the ELAB_FSM is in PPG STATE, PPG_IOFF_CALIB or PPG_ALC_STORAGE, the i_start_operation_for_ppg shall be set

Covers: DRS-REQ-024
Canonical requirement: can-334ba286f9f2b5a142f240ba
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_096
Mapped block: Main Controller

**[IPOS-DIG-REQ-025] Requirement:**
The user shall configure which channel is selected and if work in Data Storage mode for the

Covers: DRS-REQ-025
Canonical requirement: can-37f2a4b9bb0158db472035ef
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1005
Mapped block: Main Controller

**[IPOS-DIG-REQ-026] Requirement:**
When in FIRST_ALC_SAMPLES state, the PPG_FSM Shall stay in this state until 1 clock cycle after the rise of the i_end_average and the TX_start_up time has passed. After that, the PPG FSM

Covers: DRS-REQ-026
Canonical requirement: can-3896966eb93789c822f82ba1
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_103
Mapped block: Main Controller

**[IPOS-DIG-REQ-027] Requirement:**
When in Measurement state, the PPG_FSM shall stay in this state until the rising of the i_end_average signal from the ADC block. After that, the PPG_FSM shall bring itself into the Falling

Covers: DRS-REQ-027
Canonical requirement: can-396c0dbeca8382aac7a23415
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_108
Mapped block: Main Controller

**[IPOS-DIG-REQ-028] Requirement:**
The only registers that the user shall change after setting the mode_operation to 1 are the ones described in requirement 7096. All the Other signals shall change only with mode_operation set

Covers: DRS-REQ-028
Canonical requirement: can-3ed1b41ba3a6f13b44ebbe9c
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_002
Mapped block: Main Controller

**[IPOS-DIG-REQ-029] Requirement:**
If the user set a value greater than 1024 into ones of the m_channel (see req 5004), the value shall clamp at 1024 (check the input i_m_ecg, i_m_bia, i_m_gsr or i_m_ppg into the main

Covers: DRS-REQ-029
Canonical requirement: can-3f1f2e1ff5273fc40abe347d
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_5005
Mapped block: Main Controller

**[IPOS-DIG-REQ-030] Requirement:**
When i_imp_curinj signal is equal to 1, the o_imp_curinj_pd shall go low. On the other hand, if

Covers: DRS-REQ-030
Canonical requirement: can-40d4495556b12071d890e009
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_082
Mapped block: Main Controller

**[IPOS-DIG-REQ-031] Requirement:**
If multiple frame is selected (i_frame_repetition in ppg_fsm greater than 0), when Tx Preset falls from 1 to 0, the en_tx shall pass from 1 to 0 only during the last repetition (check that when

Covers: DRS-REQ-031
Canonical requirement: can-4366787694a718d02b94c202
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_8106
Mapped block: Main Controller

**[IPOS-DIG-REQ-032] Requirement:**
When ELAB FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) or a WAIT_END_OPERATIVE State, o_en_biobuffer shall

Covers: DRS-REQ-032
Canonical requirement: can-439ba5093606530cc56a3f5d
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_039
Mapped block: Main Controller

**[IPOS-DIG-REQ-033] Requirement:**
When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) during each frame o_Txi_idac_VREF shall go from 0 to N_MAX (DIGITAL_RAMP_CONFIG_PARAM_1 register [3:0]). At first, o_Txi_idac_VREF shall be increase its value of N_START for next step o_Txi_idac_VREF shall

Covers: DRS-REQ-033
Canonical requirement: can-463cb72c0212e2ea6019f555
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_032
Mapped block: Main Controller

**[IPOS-DIG-REQ-034] Requirement:**
When ELAB_FSM is in BIA state , o_ADC_EN shall go high and 16 acquisitions are required (acquisitions described in section 5.4 ADC PHASE ) and then device shall go in

Covers: DRS-REQ-034
Canonical requirement: can-467003ab893cea0538f829d1
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_3127
Mapped block: Main Controller

**[IPOS-DIG-REQ-035] Requirement:**
All the PPG_FSM state shall be checked using the PPG_STATUS_REGISTER in Regmap (the

Covers: DRS-REQ-035
Canonical requirement: can-471efb75b1f997f060a181f4
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_7095
Mapped block: Main Controller

**[IPOS-DIG-REQ-036] Requirement:**
When DEVICE_FSM FSM is in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) if HC_EN (ECG_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL [2]) is set to 1, after WAIT_SU, the device FSM shall go in OPERATIVE (DEVICE_STATUS_REG register [2:0] is equal to 0x04).

Covers: DRS-REQ-036
Canonical requirement: can-479f28a1db44924ad07cb961
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_028
Mapped block: Main Controller

**[IPOS-DIG-REQ-037] Requirement:**
When in Rising_Ramp State, the PPG_FSM shall stay in this state until the end of the Rising Time

Covers: DRS-REQ-037
Canonical requirement: can-481be0cb5bcaf9a7e5ed6b46
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_106
Mapped block: Main Controller

**[IPOS-DIG-REQ-038] Requirement:**
When in Rising_Ramp state, at the half of Rising_time, the o_idac_dc_ppg_frame shall be set to the IDAC_DC_PPG_FRAME_{n} (FRAME_n_PARAMETERS_5 register [5:0]) value related to the

Covers: DRS-REQ-038
Canonical requirement: can-48bca61825ae0aa8ded2abf1
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_105
Mapped block: Main Controller

**[IPOS-DIG-REQ-039] Requirement:**
If i_rst_async_bia is set to 1, the start-up phase shall restart but no clock shall stop if

Covers: DRS-REQ-039
Canonical requirement: can-4c9ad189607dd27e008ad91f
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_4090
Mapped block: Main Controller

**[IPOS-DIG-REQ-040] Requirement:**
For GSR Operation, if i_en_cds is set 0, the behavior shall as described in Requirement 143, otherwise the o_write_enabled shall be asserted when i_end_of_coversion is set to 1 and i_n_average_ecg_bia_gsr is equal to their limit values when the measurement is done with

Covers: DRS-REQ-040
Canonical requirement: can-4f18ab6e0b2069b6338d321d
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1143
Mapped block: Main Controller

**[IPOS-DIG-REQ-041] Requirement:**
When in MEASUREMENT State, the o_falling_digital_ramp signal shall be set to 1 to go into the

Covers: DRS-REQ-041
Canonical requirement: can-53fda3d0ba5440a1c323a8d7
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_109
Mapped block: Main Controller

**[IPOS-DIG-REQ-042] Requirement:**
The PPG Noise Data shall be accumulated in two phases, the first when the PPG FSM state is in FIRST_ALC_SAMPLES States and the second when the PPG FSM state is in the

Covers: DRS-REQ-042
Canonical requirement: can-54429a3016980462db15cd4c
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1139
Mapped block: Main Controller

**[IPOS-DIG-REQ-043] Requirement:**
When the ppg ioff calibration and the adc calibration are selected, the adc calibration shall be

Covers: DRS-REQ-043
Canonical requirement: can-561314ddb7fac99b5fd5a89b
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_3129
Mapped block: Main Controller

**[IPOS-DIG-REQ-044] Requirement:**
The average block shall perform the average on 16 sample acquisition for GSR. When the CDS mode is enabled, the average block shall perform a n average on 16 sample acquisition on GSR ON and 16 sample acquisition on GSR OFF, then shall perform a subtraction operation between

Covers: DRS-REQ-044
Canonical requirement: can-569c0cd40266206a06767d37
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_138
Mapped block: Main Controller

**[IPOS-DIG-REQ-045] Requirement:**
When in Falling_Ramp state, the PPG_FSM shall stay in this state until the end of the Falling Time (depends on the user's configuration of Digital Ramp parameters) and bring itself into the

Covers: DRS-REQ-045
Canonical requirement: can-5c51771379a5c8b4c543ecbb
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_111
Mapped block: Main Controller

**[IPOS-DIG-REQ-046] Requirement:**
When the calibration phase is ended, the o_end_cal_phase shall be set to 1 and shall stay high

Covers: DRS-REQ-046
Canonical requirement: can-658718c229db6bd21e8d072d
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_047
Mapped block: Main Controller

**[IPOS-DIG-REQ-047] Requirement:**
The Frame shall work as follows: 1. Select how many times a particular frame shall be repeated 2. The result of each repetition shall be obtained as explained in [IPOS_STBIO1_MAIN_CONTROLLER_1 40] REQUIREMENT 3. After the last repetition has been accumulated, the data output shall be obtained dividing by the number of repeated frames the accumulated data to obtain a 20 bit data. The final result shall be computed as follows: Number of times the Frame has been repeated Result 2 (Res_F_R1 + Res_F_R2)/2 4 (Res_F_R1 + Res_F_R2+Res_F_R3+Res_F_R4)/4 8 (Res_F_R1 + Res_F_R2+Res_F_R3+…..+Res_F_R8)/8 Table 20: Frame Repetitions Result Computation table Where Res_F_Rx stands for Result_frame_Repeated_times (Example: RES_F_R2 refers to the result of the second repetition of the frame.

Covers: DRS-REQ-047
Canonical requirement: can-659241fdf5825bdf8b2e6cb2
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_2145
Mapped block: Main Controller

**[IPOS-DIG-REQ-048] Requirement:**
At the end of each Frame, the start_avarage signal shall be rise to the Average block computation. Once the Average is computed, if no averages_between_equal_frames option is selected, the data shall be written inside the FIFO Memory using the Main Control ler AHB Master interface. If there is avareges_between_equal_frames option selected from regmap, after the computations of this average, the obtained data shall be written inside the FIFO Memory using the Main Controller AHB

Covers: DRS-REQ-048
Canonical requirement: can-68e3265f492ccd498f37000e
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_115
Mapped block: Main Controller

**[IPOS-DIG-REQ-049] Requirement:**
When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1 and the IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 1, the O_IMP_CURINJ_PD shall go low. On the other hand, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 0, the O_IMP_CURINJ_PD shall remain

Covers: DRS-REQ-049
Canonical requirement: can-69963eacbd5027260d15434e
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_017
Mapped block: Main Controller

**[IPOS-DIG-REQ-050] Requirement:**
When in IDLE State, if ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is high, or BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is set high, or ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL register [1]) is set high, or GSR_SEL (DEVICE_CONFIG_CHANNEL register [3]) is set high, or ADC_DO_CALIBRATION ( ADC_CAL_CONFIG register [0]) is set high, or WAVE_VELOCITY_MODE (GENERAL_PPG_PARAMETERS_1 register [4]) is set high together wit h PPG_SEL (DEVICE_CONFIG_CHANNEL register [4]), when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_CLKF shall go

Covers: DRS-REQ-050
Canonical requirement: can-699a73692458d0f5021852cd
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_009
Mapped block: Main Controller

**[IPOS-DIG-REQ-051] Requirement:**
When i_rstn is asserted low, all the output shall be set to 0, except for count_cap that shall be set

Covers: DRS-REQ-051
Canonical requirement: can-69a216d9e4149d598d68a0b2
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_044
Mapped block: Main Controller

**[IPOS-DIG-REQ-052] Requirement:**
If the calibration has been done, the ADC_error_caps values computed shall reset only if the

Covers: DRS-REQ-052
Canonical requirement: can-6ac04b78692e70a118ba4f0e
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_0152
Mapped block: Main Controller

**[IPOS-DIG-REQ-053] Requirement:**
When ECG0 and BIA are selected 21 acquisitions shall be required (acquisitions described in section 5.4 ADC PHASE) and then device shall go in SLEEP (DEVICE_STATUS_REG register

Covers: DRS-REQ-053
Canonical requirement: can-6ea20d93ffa222b0e2c99ba8
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_128
Mapped block: Main Controller

**[IPOS-DIG-REQ-054] Requirement:**
The system shall satisfy the following behavior: If the i_noise signal is set to 1 when the DEVICE_FSM is into PPG State, the i_n_avarage shall.

Covers: DRS-REQ-054
Canonical requirement: can-727cd9d0edc118b893874e73
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_059
Mapped block: Main Controller

**[IPOS-DIG-REQ-055] Requirement:**
If i_su_hlt_dly is set to 0. At least after 205ms that the o_rsti_hc2 is gone low, o_su_hc2 shall go

Covers: DRS-REQ-055
Canonical requirement: can-743ecc8f2f0808543c89abcc
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_078
Mapped block: Main Controller

**[IPOS-DIG-REQ-056] Requirement:**
If the en_gsr_cds [bit 3 of GSR_CTRL] is set High, the i_m_gsr shall define also in which time slot after the GSR_Curr_on falls from 1 to 0, an acquisition without current injection (o_gsr_curr_on set

Covers: DRS-REQ-056
Canonical requirement: can-78c988ecaea54700f9744c38
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_089
Mapped block: Main Controller

**[IPOS-DIG-REQ-057] Requirement:**
When in FIRST_ALC_SAMPLES state, when i_end_average is set to 1, the o_start_digital_ramp signal shall be set high to start the rising of the digital ramp and go into the RISING_RAMP state.

Covers: DRS-REQ-057
Canonical requirement: can-796769d65d1c7ddb329865ad
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_104
Mapped block: Main Controller

**[IPOS-DIG-REQ-058] Requirement:**
In Order to enable a BIA Channel Operation, the user shall always select the BIA channel

Covers: DRS-REQ-058
Canonical requirement: can-7a49992c398118548220a215
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1008
Mapped block: Main Controller

**[IPOS-DIG-REQ-059] Requirement:**
After an acquisition is started, the ADC_Phases shall wait for the i_ADC_EOC sampling the new

Covers: DRS-REQ-059
Canonical requirement: can-7b754242aeafe4c31d9765bd
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_055
Mapped block: Main Controller

**[IPOS-DIG-REQ-060] Requirement:**
When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) signal is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1, 5ms after the falling of imp_curinj_pd and O_PD_IMP, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 1, O_CK_M, O_CK_P and O_CK_Q shall be generated from Clock generator block so they run at FREQ_BIA_CLK_m_p_q (EN_CHOP_FREQ_MOD_DEMOD register [4:3] ) and its values shall be chosen from 20kHz, 50kHz, 100kHz, 200kHz . On the other hand, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 0, ck_m, ck_p and

Covers: DRS-REQ-060
Canonical requirement: can-7ffa202bdb5fa891e0a445cd
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_018
Mapped block: Main Controller

**[IPOS-DIG-REQ-061] Requirement:**
When i_debug_adc_error_cap8_0_bypass is set to 1 (set to 1 en_debug_adc_error_cap8_0_bypass of ADC_GENERAL_DEBUG_0 ), the calibration result shall be bypassed in favor of the value written inside the registers

Covers: DRS-REQ-061
Canonical requirement: can-80c7c8b7e186da993b6faeed
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_063
Mapped block: Main Controller

**[IPOS-DIG-REQ-062] Requirement:**
When in Sleep Mode, the device shall go back to the Operative State if no error (o_error_irq stuck at 0) occurs and all the operations are ended . Furthermore, if no Bio -Channel operations are selected and more than 150us are left before the start of a new time slot, the o_pd_clkf (Digital

Covers: DRS-REQ-062
Canonical requirement: can-81ed41d4fcba17937855edc6
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_036
Mapped block: Main Controller

**[IPOS-DIG-REQ-063] Requirement:**
When in OPERATIVE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02), if the time slot counter reach its limit, the Device_FSM shall go into the error state (DEVICE_STATUS_REGISTER) and raise an interrupt (o_error_time_slot) to the Digital_Top.

Covers: DRS-REQ-063
Canonical requirement: can-8301fcfad3c6a0d3a176fb2c
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_034
Mapped block: Main Controller

**[IPOS-DIG-REQ-064] Requirement:**
According to time diagram, when in RESET_PPG and ELAB_FSM is in PPG state during the first frame (i_id_frame=0) , shall be wait a configurable time PPG_START_UP_TIME (PPG_START_UP_TIME starting from when i_start_operation_ppg is set to 1 and at least 1 clock

Covers: DRS-REQ-064
Canonical requirement: can-83f0b7157fe28f6715efa10c
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_134
Mapped block: Main Controller

**[IPOS-DIG-REQ-065] Requirement:**
When the ELAB_FSM is in ECG State and only ECG0 is selected, the o_ADC_EN shall go high,

Covers: DRS-REQ-065
Canonical requirement: can-85778b8454e4d065795fa9f9
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_3124
Mapped block: Main Controller

**[IPOS-DIG-REQ-066] Requirement:**
In a Time Slot, when a BIO-Channel operation is selected, o_en_bufxbio signal (in Digital Top) shall go high at least a configurable time (Device Config Operation [6:5]) before selecting the first

Covers: DRS-REQ-066
Canonical requirement: can-899723acbc0cea0002411da1
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_037
Mapped block: Main Controller

**[IPOS-DIG-REQ-067] Requirement:**
When DEVICE_FSM FSM is in WAIT_SU STATE ( main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x03) if HC_EN (ECG_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is set to 1 and MODE_OPERATION (bit [1:0] on DEVICE_CONFIG_OPERATION register) is different to 0, after WAIT_SU state the device shall go in OPERATIVE (DEVICE_STATUS_REG register [2:0] is equal

Covers: DRS-REQ-067
Canonical requirement: can-8a74237fdc17790fa1d1a5b1
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_024
Mapped block: Main Controller

**[IPOS-DIG-REQ-068] Requirement:**
When in Falling_Ramp State, at the half of the Falling_Time the o_idac_dc_ppg_frame shall be

Covers: DRS-REQ-068
Canonical requirement: can-8bae8649d7bba6484e088d24
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_110
Mapped block: Main Controller

**[IPOS-DIG-REQ-069] Requirement:**
When ALC_COMP starts, o_BTIA_gain (2:0) shall be set at i_gain_start (PPG_ALC_CONFIG_PARAM_2 register [4:2]) and o_w_BTIA_ALC (8:0) shall be set at

Covers: DRS-REQ-069
Canonical requirement: can-8bff4530f202eaff1cc54624
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_126
Mapped block: Main Controller

**[IPOS-DIG-REQ-070] Requirement:**
The o_adc_ready shall be set to 1 when the ADC is getting ready (o_adc_en is set to 1 but not

Covers: DRS-REQ-070
Canonical requirement: can-8dc593c1e3f4b9c6f18d64bc
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_045
Mapped block: Main Controller

**[IPOS-DIG-REQ-071] Requirement:**
When the Device_FSM FSM is in BOOT State, that is DEVICE_STATUS_REG register [2:0]) == 0x01 (main_controller_status_register), it shall wait that the ADSP ends the BOOT Phase, checking when the i_quokka_boot_end is set high. When the BOOT Phase is ended, the Device_FSM FSM shall go to IDLE State, check that DEVICE_STATUS_REG register [2:0]) == 0x02, (main_controller_status_register), check that the w_en_ldo1v8 signal is set low and that

Covers: DRS-REQ-071
Canonical requirement: can-90755ffc808bb0e664eb02bf
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_004
Mapped block: Main Controller

**[IPOS-DIG-REQ-072] Requirement:**
When the ADC_phases fsm is ready and an acquisition is required, the o_ADC_start shall stay

Covers: DRS-REQ-072
Canonical requirement: can-949d301a115bda067e98c319
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_054
Mapped block: Main Controller

**[IPOS-DIG-REQ-073] Requirement:**
When the i_ADC_en_mc and i_adc_en_mask is set to 1, at least 160 clock cycles shall pass before

Covers: DRS-REQ-073
Canonical requirement: can-9a71ae848cb394e1f41f1179
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_053
Mapped block: Main Controller

**[IPOS-DIG-REQ-074] Requirement:**
When i_frame_ppg_debug is set to a value greater than 0 and i_n_average_ppg is set to a value between 1 and 16, all the ADC output (i_data_in) for ALC (i_data_valid_noise_ppg_adc set to 1) and PPG data (i_data_valid_ppg_adc) shall be stored in o_adc_data_debug_alc_2,

Covers: DRS-REQ-074
Canonical requirement: can-9ea0a8246c3fe782073070a0
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_2143
Mapped block: Main Controller

**[IPOS-DIG-REQ-075] Requirement:**
When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL [2]) is equal to 1, O_PD_IMP shall go low within 5 clock cycle at

Covers: DRS-REQ-075
Canonical requirement: can-9f657f8654d615aeb7b1f47c
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_016
Mapped block: Main Controller

**[IPOS-DIG-REQ-076] Requirement:**
When DEVICE_FSM FSM is in IDLE if PPG_SEL (DEVICE_CONFIG_CHANNEL [4]) is set to 1 and MODE_OPERATION (bit [1:0] on DEVICE_CONFIG_OPERATION register) is different to 0, the device shall go in PPG state (main_controller_status_register in ELAB_STATUS_REG register

Covers: DRS-REQ-076
Canonical requirement: can-a12fa28d397a8fecc3750634
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_029
Mapped block: Main Controller

**[IPOS-DIG-REQ-077] Requirement:**
If i_rst_async_ecg is set to 1, the start-up phase shall restart but no clock shall stop if enabled.

Covers: DRS-REQ-077
Canonical requirement: can-a3837229b89477e7d6614369
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_4079
Mapped block: Main Controller

**[IPOS-DIG-REQ-078] Requirement:**
When DEVICE_FSM FSM is in WAIT_SU state, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1; 20ms after the falling of O_RST_IMP, if EN_CHOP_CLK_IMP (EN_CHOP_FREQ_MOD_DEMOD register [1]) is set to 1, O_CK_CHOP_IMP shall be generated from Clock generator block, so O_CK_CHOP_IMP shall be run at 10kHz frequency. On the other hand, if EN_CHOP_CLK_IMP (EN_CHOP_FREQ_MOD_DEMOD register [1]) is set

Covers: DRS-REQ-078
Canonical requirement: can-a4a2e6fa06b1efb795d11f0f
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_021
Mapped block: Main Controller

**[IPOS-DIG-REQ-079] Requirement:**
At least 5ms after the falling of o_imp_curinj_pd and o_pd_imp_from_bia, if i_imp_curinj is equal to 1, o_en_ck_m_p_q shall be high and ck_m, ck_p and ck_q shall be generated from Clock generator block. On the other hand, if i_imp_curinj is equal to 0, the ck_m_p_q shall stay low.

Covers: DRS-REQ-079
Canonical requirement: can-a5cd7e0d3dbf56a520a82ef3
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_083
Mapped block: Main Controller

**[IPOS-DIG-REQ-080] Requirement:**
When in Sleep Mode and no Bio-Channel are selected, if every elaboration is ended and there are at least 34 clock cycles at 32kHz before the start of a new time slot, the o_en_ldo_1v8 shall go

Covers: DRS-REQ-080
Canonical requirement: can-a678243864c02c83ce158886
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_436
Mapped block: Main Controller

**[IPOS-DIG-REQ-081] Requirement:**
When in ALC Compensation, the PPG shall wait that the rise of i_end_compensation signal from the ALC Compensation block to go into the RX_Start_UP state. This shall happen in OPERATIVE.

Covers: DRS-REQ-081
Canonical requirement: can-a7aae5f4ae37ab4736066d0e
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_099
Mapped block: Main Controller

**[IPOS-DIG-REQ-082] Requirement:**
When the i_hc_en is set to 1 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 3, ECG0- ECG1 and ECG2 shall be active so the o_pd_hc2 shall go low, o_pd_imp shall go low and

Covers: DRS-REQ-082
Canonical requirement: can-aaf96b21b29144c5d9714144
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_074
Mapped block: Main Controller

**[IPOS-DIG-REQ-083] Requirement:**
When in ALC Compensation, the PPG FSM shall raise the o_start_alc_comp signal to the ALC

Covers: DRS-REQ-083
Canonical requirement: can-ace4c3f346f228a3d687e547
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_098
Mapped block: Main Controller

**[IPOS-DIG-REQ-084] Requirement:**
When the ELAB_FSM is in ECG State, the ADC_Mux (concatenation of {o_adc_mux_sel, o_adc_mux_bio_channel} on digital top) output shall be set equal to 001 and after 4 acquisitions (described in section 5.4 ADC PHASE) shall be set to 010. If ECG1 and ECG2 are selected, the

Covers: DRS-REQ-084
Canonical requirement: can-aeba08998bd4ae2c814ee262
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_038
Mapped block: Main Controller

**[IPOS-DIG-REQ-085] Requirement:**
If i_su_hlt_dly is set to 0,at least 205 ms after the falling of o_rsti_imp, o_sug_imp shall go low. Instead, if i_su_hlt_dly is set to 1, 755ms after the falling of o_rsti_imp, o_sug_imp shall go low.

Covers: DRS-REQ-085
Canonical requirement: can-af4c9bade830ba23134d3ba8
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_087
Mapped block: Main Controller

**[IPOS-DIG-REQ-086] Requirement:**
The max value that the user shall use for every m_channel (m_ecg, m_bia, m_gsr and m_ppg) is

Covers: DRS-REQ-086
Canonical requirement: can-afb79056c99d33b4f93a67e5
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_5004
Mapped block: Main Controller

**[IPOS-DIG-REQ-087] Requirement:**
If en_gsr_cds is set high [bit 3 of GSR_CTRL] the GSR_SNS (acquisition with o_gsr_curr_on set to 1) and GSR_CDS (acquisition with o_gsr_curr_on set to 0) shall be sampled 16 times, then mediated to get one single value for each of them, and then the final result shall be the subtraction between GSR_SNS and GSR_CDS. On the other hand, If en_gsr_cds is set low, no acquisition of GSR_CDS shall be done and the result shall be the average of 16 acquisitions of

Covers: DRS-REQ-087
Canonical requirement: can-afc26f5acc15bf552d041a28
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_093
Mapped block: Main Controller

**[IPOS-DIG-REQ-088] Requirement:**
When IMP_CURRINJ_EN (CURR_INJ register [3]) is high, O_CK_Q shall be run with a phase

Covers: DRS-REQ-088
Canonical requirement: can-b03cd3a8fc623d78cb36d1ef
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_019
Mapped block: Main Controller

**[IPOS-DIG-REQ-089] Requirement:**
When in SECOND_ALC_SAMPLES state, the PPG_FSM shall stay in this state until the rise of the end_of_conversion signal from the ADC block. After that, if there are no more frames to run, the PPG_FSM shall go into the Reset State, otherwise, if there are other frames to run and channel rx is not changed, the PPG_FSM shall go into the Rx_start_up phase. On the other hand, if there are other frame to run and rx_channel is changed, the PPG_FSM shall go into the RESET_PPG

Covers: DRS-REQ-089
Canonical requirement: can-b177cd4267393d53252b9d9c
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_113
Mapped block: Main Controller

**[IPOS-DIG-REQ-090] Requirement:**
When ELAB_FSM is in ECG state and EC0, ECG1 and ECG2 are selected , o_ADC_EN shall go high and15 acquisitions are required (acquisitions described in 5.4 ADC PHASE) and then device

Covers: DRS-REQ-090
Canonical requirement: can-b3049de0ad94eb28389a2da7
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_3126
Mapped block: Main Controller

**[IPOS-DIG-REQ-091] Requirement:**
In Order to enable an ECG0 Channel Operation, the user shall always select the ECG0 channel

Covers: DRS-REQ-091
Canonical requirement: can-b3f1c1049c13cd4c05c31ea4
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1007
Mapped block: Main Controller

**[IPOS-DIG-REQ-092] Requirement:**
When DEVICE_FSM FSM is in WAIT_SU state, if IMP_EN signal (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1; If i_su_hlt_dly is set to 0, 205ms after the falling of O_RSTI_IMP, O_SUG_IMP shall go low. Instead, if SU_DLY (EN_CHOP_FREQ_MOD_DEMOD register [2]) is set to 1, 755ms after the

Covers: DRS-REQ-092
Canonical requirement: can-b41763a8769ac954f65ec0ab
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_023
Mapped block: Main Controller

**[IPOS-DIG-REQ-093] Requirement:**
When in unique_fifo_mode (i_multiple_fifo set to 0), if during a time slot an operation is done, the Main_Controller_FSM shall write the time_slot_data inside the FIFO with a dedicated tag. The value of the time_slot_data shall be referred to the start of the entire measurement cycle (for

Covers: DRS-REQ-093
Canonical requirement: can-b885b74631e3733e95dcf5a8
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_008
Mapped block: Main Controller

**[IPOS-DIG-REQ-094] Requirement:**
At the end of ALC compensation, if ALC is not masked, o_w_BTIA_ALC relative to the running frame, shall be set to output system (check when i_end_of_compensation rise in PPG FSM). If

Covers: DRS-REQ-094
Canonical requirement: can-bd8d9b58cd8f3c266d51223c
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_728
Mapped block: Main Controller

**[IPOS-DIG-REQ-095] Requirement:**
The i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] shall define how many time slots pass between two GSR acquisitions following this formula: GSRdata = time_slot 2 ∗ m_gsr

Covers: DRS-REQ-095
Canonical requirement: can-c41d89621313ed4d19e90498
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_088
Mapped block: Main Controller

**[IPOS-DIG-REQ-096] Requirement:**
When DEVICE_FSM FSM is in Operative State (DEVICE_STATUS_REG register [2:0]==0x04), the o_MC_busy shall go to 1 and shall go to 0 one clock cycle after entering the SLEEP state if

Covers: DRS-REQ-096
Canonical requirement: can-c5f334bc51a20823ac692ad8
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_035
Mapped block: Main Controller

**[IPOS-DIG-REQ-097] Requirement:**
When i_wave_velocity mode is enabled together with the DISABLE_ALC, the PPG_ALC_STORAGE shall be performed but once the Device goes into OPERATIVE State, the

Covers: DRS-REQ-097
Canonical requirement: can-c808774d476ced044ae50ca2
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_6070
Mapped block: Main Controller

**[IPOS-DIG-REQ-098] Requirement:**
In Order to enable a PPG Channel Operation, the user shall always select the PPG channel

Covers: DRS-REQ-098
Canonical requirement: can-cba9fb257d4ac7dda69b1491
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1010
Mapped block: Main Controller

**[IPOS-DIG-REQ-099] Requirement:**
The system shall satisfy the following behavior: When the last acquisition is performed, after the last i_ADC_EOC arrived, the ADC_phases shall.

Covers: DRS-REQ-099
Canonical requirement: can-ce741a350690f33a6b2d4ac9
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_060
Mapped block: Main Controller

**[IPOS-DIG-REQ-100] Requirement:**
When the adc_readout_bypass mode is enabled by the 2 bitfield ADC_GENERAL_DEBUG_0 , the sampling phase of the ADC Phgen shall be bypassed in favor of regmap. In particular, the Sampling phase shall be controlled by the register EN_ADC_DEBUG and EN_ADC_START in ADC_GENERAL_DEBUG_0 and the sampled data shall be written in ADC_DATA_OUT_DEBUG_LOW and ADC_DATA_OUT_DEBUG_HIGH. and In this mode, before start a new sampling operation, the RESET_DEBUG_ADC DATA in

Covers: DRS-REQ-100
Canonical requirement: can-d38d0f592b26a6d558c1a908
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_064
Mapped block: Main Controller

**[IPOS-DIG-REQ-101] Requirement:**
In Order to enable an ECG1_ECG2 Channel Operation, the user shall always select the ECG1_ECG2 channel (DEVICE_CONFIG_CHANNEL), set the i_M_ECG greater than zero and

Covers: DRS-REQ-101
Canonical requirement: can-d39754656859455b339ef80f
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1011
Mapped block: Main Controller

**[IPOS-DIG-REQ-102] Requirement:**
When the FSM is in IDLE State, if ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is high, HC_EN (ECG_CTRL register [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 0, ECG0 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall go low and the Device_FSM FSM shall go to the WAIT_SU State , so the main_controller_status_register (DEVICE_STATUS_REG register

Covers: DRS-REQ-102
Canonical requirement: can-d408e5fcca891217c62c5a09
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_010
Mapped block: Main Controller

**[IPOS-DIG-REQ-103] Requirement:**
When not in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) , Device_FSM shall go back in IDLE only if the user turns off the

Covers: DRS-REQ-103
Canonical requirement: can-dc42ae19b64db272b31252d3
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_033
Mapped block: Main Controller

**[IPOS-DIG-REQ-104] Requirement:**
When the i_hc_en is set to 0 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 2, ECG1 and ECG2 shall be active so the o_pd_hc2 shall remain high, o_pd_imp_from_bia shall go low

Covers: DRS-REQ-104
Canonical requirement: can-dd33adbeb29452fab04ff673
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_073
Mapped block: Main Controller

**[IPOS-DIG-REQ-105] Requirement:**
The data written in FIFO shall have the following tag: DATA TYPE BIT: 23 - 20 BIT: 19 - 16 BIT: 15 - 0 PPG FRAME 0 0000 DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT PPG FRAME 1 0001 PPG FRAME 2 0010 PPG FRAME 3 0011 PPG FRAME 4 0100 PPG FRAME 5 0101 PPG FRAME 6 0110 PPG FRAME 7 0111 PPG FRAME 8 1000 PPG FRAME 9 1001 PPG FRAME 10 1010 PPG FRAME 11 1011 TIME SLOT DATA 1111 0000 DATA 16 BIT ECG0_AC 1100 0000 DATA 16 BIT ECG0_DC 1101 0000 DATA 16 BIT ECG1_AC 1100 0001 DATA 16 BIT ECG1_DC 1101 0001 DATA 16 BIT ECG2_AC 1100 0010 DATA 16 BIT ECG2_DC 1101 0010 DATA 16 BIT

Covers: DRS-REQ-105
Canonical requirement: can-df332e45fc711566566b7836
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_2144
Mapped block: Main Controller

**[IPOS-DIG-REQ-106] Requirement:**
20ms after that the o_rst_hc2 is gone low, if i_clk_hlt_en is equal to 1, chopper_clock shall be generated and after another 10ms, o_rsti_hc2 shall go low. Instead, if i_clk_hlt_en is equal to 0,

Covers: DRS-REQ-106
Canonical requirement: can-e2dd56a9df6fce20d2047956
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_077
Mapped block: Main Controller

**[IPOS-DIG-REQ-107] Requirement:**
The State WAIT_SU shall not be considered interruptible. If the user wants to interrupt the WAIT_SU state, it shall perform the Soft Reset procedure described in the DDS

Covers: DRS-REQ-107
Canonical requirement: can-e35e106d7724a1ee18a05637
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_5015
Mapped block: Main Controller

**[IPOS-DIG-REQ-108] Requirement:**
When ELAB_FSM is in ECG state and ECG1 and ECG2 are selected , o_ADC_EN shall go high and 10 acquisitions are required (acquisitions described in chapter in section 5.4 ADC PHASE).

Covers: DRS-REQ-108
Canonical requirement: can-e38fa3af5ce6bd176ab38aad
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_3125
Mapped block: Main Controller

**[IPOS-DIG-REQ-109] Requirement:**
The calibration phase shall set the adc_error_cap8…0 to the correct value, following the calibration

Covers: DRS-REQ-109
Canonical requirement: can-e562f96cdf76151c6904e013
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_058
Mapped block: Main Controller

**[IPOS-DIG-REQ-110] Requirement:**
When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x 05) o_ADC_start shall go high a number of times equal “2 ^ value indicated in regmap of FRAME_{n}_SAMPLES (FRAME_n_PARAMETERS_1 register [5:3]) for ALC and PPG both (2*(2^regmap_value). Except when FRAME_{n}_SAMPLES is equal to 3’b000, in this case o_ADC_start shall go high 3 times.

Covers: DRS-REQ-110
Canonical requirement: can-e5dc831176be98f7b6700206
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_031
Mapped block: Main Controller

**[IPOS-DIG-REQ-111] Requirement:**
When i_ALC_comp_start is set to 1, the first rise of the o_comp_rx_ck shall happen at least after

Covers: DRS-REQ-111
Canonical requirement: can-e736533f96cd6aff23d61fd2
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_6129
Mapped block: Main Controller

**[IPOS-DIG-REQ-112] Requirement:**
When in SECOND_ALC_SAMPLES state, the o_en_Txi shall be set low after the end at least of the T_tx_ledoff time (TX_LEDOFF_FRAME_{n}) and the o_start_adc signal shall be set to 1.

Covers: DRS-REQ-112
Canonical requirement: can-e85ea8d07d72d99e8de9d408
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_112
Mapped block: Main Controller

**[IPOS-DIG-REQ-113] Requirement:**
When in Rx_Start_Up state, the PPG_FSM shall stay in this state for the T_rx_set time (GENERAL_PPG_PARAMETERS_3 register [3:0])) and then go into the FIRST_ALC_SAMPLES

Covers: DRS-REQ-113
Canonical requirement: can-e97cd5b9b33c3e5eff022ead
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_101
Mapped block: Main Controller

**[IPOS-DIG-REQ-114] Requirement:**
When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) the device shall be execute a number of frames equal to N_PPG_FRAME (GENERAL_PPG_PARAMETERS_1 register [3:0]) (Check the i_id_frame shall increase until it’s equal to N_PPG_FRAME-1). At the beginning of each frame o_ADC_EN shall go high and it shall go low when ALC_COMPENSATION is performed or

Covers: DRS-REQ-114
Canonical requirement: can-e9b6cd22d1163aa76e4a787b
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_030
Mapped block: Main Controller

**[IPOS-DIG-REQ-115] Requirement:**
The o_En_TIA, o_EN_Buff, o_EN_ADC and o_EN_IDAC shall be high when the PPG_FSM is

Covers: DRS-REQ-115
Canonical requirement: can-eb93fbd3a59c8b065778f32b
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_095
Mapped block: Main Controller

**[IPOS-DIG-REQ-116] Requirement:**
If i_rst_async_ecg is set to 1, it shall go to zero at least 5ms after that o_su_hc2 is set to 0.

Covers: DRS-REQ-116
Canonical requirement: can-ec99b1c86b6dd01e8534cf8b
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_4080
Mapped block: Main Controller

**[IPOS-DIG-REQ-117] Requirement:**
20ms after the falling of o_rst_imp, if i_clk_imp_en is set to 1, the o_en_ck_chop_imp shall be high and ck_chop_imp shall be generated from Clock generator block. On the hand, if i_clk_imp_en is

Covers: DRS-REQ-117
Canonical requirement: can-edf1910be79ae35d766eaedf
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_085
Mapped block: Main Controller

**[IPOS-DIG-REQ-118] Requirement:**
The average block shall perform an average on 4 Samples for each of ECG_x_AC, BIA AC P, BIA AC Q, BIA DC P and BIA DC Q , 1 Sample ECG_x_DC (Check if the i_end_of_coversion rise the

Covers: DRS-REQ-118
Canonical requirement: can-f061cce8d8f6532910931f33
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_137
Mapped block: Main Controller

**[IPOS-DIG-REQ-119] Requirement:**
When the i_data_out_adc is sampled, the 15 bit (MSB in little endian), shall be negated in order to

Covers: DRS-REQ-119
Canonical requirement: can-f40b5b06ef800ecde3ebc3f7
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_061
Mapped block: Main Controller

**[IPOS-DIG-REQ-120] Requirement:**
The user shall configure time slot duration in DEVICE_CONFIG_OPERATION register [4:2]

Covers: DRS-REQ-120
Canonical requirement: can-f77e5d634719873f60f5736b
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1004
Mapped block: Main Controller

**[IPOS-DIG-REQ-121] Requirement:**
When the Ioff Calibration algorithm is enabled, it shall be performed every time a new

Covers: DRS-REQ-121
Canonical requirement: can-f99c99cd3eec873a8a9cdb7e
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_1116
Mapped block: Main Controller

**[IPOS-DIG-REQ-122] Requirement:**
When the i_falling_digital_ramp is set to 1, the o_TX_Vref shall decrement from N_MAX value (DIGITAL_RAMP_CONFIG_PARAM_1 register [3:0]) to zero with a step equal to 1 every 2-clock

Covers: DRS-REQ-122
Canonical requirement: can-fd26d89162656c62b5e6e88d
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_120
Mapped block: Main Controller

**[IPOS-DIG-REQ-123] Requirement:**
When i_debug_calibration is set (second bitfield of ADC_CAL_CONFIG ), the number of samples used by the avarage block during the calibration shall be set to 2. (The purpose of this mode is to

Covers: DRS-REQ-123
Canonical requirement: can-fe6d59c2f908ff9b1bf353d2
Source requirement: IPOS_STBIO1_MAIN_CONTROLLER_062
Mapped block: Main Controller

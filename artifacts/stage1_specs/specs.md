# Requirements Baseline

Date: 2026-10-06

## Scope
- Stage 2 formalization baseline generated from Stage 1 requirements summary.

## Requirements
- DDS_STBIO1_4000: [DDS_STBIO1_4000] Requirement: Write enable for each OTP REGISTER shall be 0, in functional mode, if bit 31 of OTP_PRG10 is set 1.
- DDS_STBIO1_0201: 11.1. XBAR Connection Matrix Destination Source Regmap SENSOR HUB ISPU FIFO ADSP Main Controller
- DDS_STBIO1_0202: 11.1. XBAR Connection Matrix Destination Source Regmap SENSOR HUB ISPU FIFO ADSP Main Controller
- DDS_STBIO1_0219: 11.1. XBAR Connection Matrix Destination Source Regmap SENSOR HUB ISPU FIFO ADSP Main Controller
- DDS_STBIO1_0203: ADSP
- DDS_STBIO1_0204: ADSP
- DDS_STBIO1_0206: ADSP
- DDS_STBIO1_0207: I2C_SPI_AHB
- DDS_STBIO1_0208: I2C_SPI_AHB
- DDS_STBIO1_0209: I2C_SPI_AHB
- DDS_STBIO1_0210: I2C_SPI_AHB
- DDS_STBIO1_0221: I2C_SPI_AHB
- DDS_STBIO1_0211: SENSOR HUB
- DDS_STBIO1_0212: ISPU
- DDS_STBIO1_0213: ISPU
- DDS_STBIO1_0215: ISPU
- DDS_STBIO1_0222: ISPU
- DDS_STBIO1_0216: ISPU debug
- DDS_STBIO1_0217: ISPU debug
- DDS_STBIO1_0218: ISPU debug

## Acceptance Tests (Given-When-Then)
- AT-DDS_STBIO1_4000: Given nominal setup, when scenario for DDS_STBIO1_4000 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0201: Given nominal setup, when scenario for DDS_STBIO1_0201 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0202: Given nominal setup, when scenario for DDS_STBIO1_0202 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0219: Given nominal setup, when scenario for DDS_STBIO1_0219 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0203: Given nominal setup, when scenario for DDS_STBIO1_0203 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0204: Given nominal setup, when scenario for DDS_STBIO1_0204 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0206: Given nominal setup, when scenario for DDS_STBIO1_0206 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0207: Given nominal setup, when scenario for DDS_STBIO1_0207 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0208: Given nominal setup, when scenario for DDS_STBIO1_0208 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0209: Given nominal setup, when scenario for DDS_STBIO1_0209 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0210: Given nominal setup, when scenario for DDS_STBIO1_0210 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0221: Given nominal setup, when scenario for DDS_STBIO1_0221 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0211: Given nominal setup, when scenario for DDS_STBIO1_0211 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0212: Given nominal setup, when scenario for DDS_STBIO1_0212 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0213: Given nominal setup, when scenario for DDS_STBIO1_0213 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0215: Given nominal setup, when scenario for DDS_STBIO1_0215 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0222: Given nominal setup, when scenario for DDS_STBIO1_0222 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0216: Given nominal setup, when scenario for DDS_STBIO1_0216 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0217: Given nominal setup, when scenario for DDS_STBIO1_0217 is exercised, then expected behavior is observed.
- AT-DDS_STBIO1_0218: Given nominal setup, when scenario for DDS_STBIO1_0218 is exercised, then expected behavior is observed.

## Assertions
- ASSERT_DDS_STBIO1_4000_01: trigger(DDS_STBIO1_4000) -> expected(DDS_STBIO1_4000)
- ASSERT_DDS_STBIO1_0201_01: trigger(DDS_STBIO1_0201) -> expected(DDS_STBIO1_0201)
- ASSERT_DDS_STBIO1_0202_01: trigger(DDS_STBIO1_0202) -> expected(DDS_STBIO1_0202)
- ASSERT_DDS_STBIO1_0219_01: trigger(DDS_STBIO1_0219) -> expected(DDS_STBIO1_0219)
- ASSERT_DDS_STBIO1_0203_01: trigger(DDS_STBIO1_0203) -> expected(DDS_STBIO1_0203)
- ASSERT_DDS_STBIO1_0204_01: trigger(DDS_STBIO1_0204) -> expected(DDS_STBIO1_0204)
- ASSERT_DDS_STBIO1_0206_01: trigger(DDS_STBIO1_0206) -> expected(DDS_STBIO1_0206)
- ASSERT_DDS_STBIO1_0207_01: trigger(DDS_STBIO1_0207) -> expected(DDS_STBIO1_0207)
- ASSERT_DDS_STBIO1_0208_01: trigger(DDS_STBIO1_0208) -> expected(DDS_STBIO1_0208)
- ASSERT_DDS_STBIO1_0209_01: trigger(DDS_STBIO1_0209) -> expected(DDS_STBIO1_0209)
- ASSERT_DDS_STBIO1_0210_01: trigger(DDS_STBIO1_0210) -> expected(DDS_STBIO1_0210)
- ASSERT_DDS_STBIO1_0221_01: trigger(DDS_STBIO1_0221) -> expected(DDS_STBIO1_0221)
- ASSERT_DDS_STBIO1_0211_01: trigger(DDS_STBIO1_0211) -> expected(DDS_STBIO1_0211)
- ASSERT_DDS_STBIO1_0212_01: trigger(DDS_STBIO1_0212) -> expected(DDS_STBIO1_0212)
- ASSERT_DDS_STBIO1_0213_01: trigger(DDS_STBIO1_0213) -> expected(DDS_STBIO1_0213)
- ASSERT_DDS_STBIO1_0215_01: trigger(DDS_STBIO1_0215) -> expected(DDS_STBIO1_0215)
- ASSERT_DDS_STBIO1_0222_01: trigger(DDS_STBIO1_0222) -> expected(DDS_STBIO1_0222)
- ASSERT_DDS_STBIO1_0216_01: trigger(DDS_STBIO1_0216) -> expected(DDS_STBIO1_0216)
- ASSERT_DDS_STBIO1_0217_01: trigger(DDS_STBIO1_0217) -> expected(DDS_STBIO1_0217)
- ASSERT_DDS_STBIO1_0218_01: trigger(DDS_STBIO1_0218) -> expected(DDS_STBIO1_0218)

## Open Ambiguities
- Full Stage 2 review pending for requirements beyond this generated baseline.

# Report centralizzato delle issue descrittive

**Solo per revisione utente. Non costituisce contenuto approvato, autorita o accettazione delle specifiche.**

Questo report non modifica requisiti, approvazioni, ownership, allocation, traceability o gate. Gli estratti sono evidenza diagnostica, non testo approvato da inserire nelle specifiche. Eventuali proposte sono esclusivamente candidate per la revisione utente.

Le voci includono esclusioni intenzionali, omissioni, blocchi e problemi di pubblicazione: il totale non equivale al numero di difetti sorgente. Un'esclusione per scope non dimostra corruzione.

Snapshot: snap\-73c872b1307b6adb5eaf843e

Inizio del run osservato: 2026\-10\-09 21\:08\:43

Voci totali: 737

## Sintesi per documento

| Documento | Gate o generazione | Scope | Marker inline | Voci |
| --- | --- | --- | --- | --- |
| SRS | PASS |  | NO\_MARKERS\_DETECTED | 328 |
| ARS | PASS |  | NO\_MARKERS\_DETECTED | 73 |
| DRS | PASS |  | NO\_MARKERS\_DETECTED | 190 |
| Digital IPOS | PARTIAL\_BLOCKS\_VALIDATED | MATERIALIZED\_SCOPE |  | 145 |
| Analog IPOS | NOT\_RUN | VALID\_EMPTY |  | 1 |

PASS indica soltanto l'esito del gate registrato. Non certifica l'assenza di marker o la completezza richiesta. I risultati IPOS per blocco riportano il gate esistente sui file correnti; non certificano l'intero stage o gli altri file storici.

## Preflight dei blocchi IPOS

| Documento | Blocco | Requisiti | Preflight | Contesti irrisolti | Pubblicazione osservata |
| --- | --- | --- | --- | --- | --- |
| Digital IPOS | ADSP | 19 | PASS | 0 | PASS |
| Digital IPOS | I2C\_SPI\_AHB | 15 | BLOCKED | 13 | BLOCKED\_NOT\_PUBLISHED |
| Digital IPOS | Main Controller | 181 | BLOCKED | 72 | BLOCKED\_NOT\_PUBLISHED |
| Digital IPOS | PAD MUX | 17 | BLOCKED | 11 | BLOCKED\_NOT\_PUBLISHED |
| Digital IPOS | PMU | 31 | BLOCKED | 2 | BLOCKED\_NOT\_PUBLISHED |
| Digital IPOS | Regmap | 8 | BLOCKED | 12 | BLOCKED\_NOT\_PUBLISHED |
| Digital IPOS | Sensor\-Hub | 18 | BLOCKED | 3 | BLOCKED\_NOT\_PUBLISHED |
| Digital IPOS | Smart FIFO | 13 | BLOCKED | 5 | BLOCKED\_NOT\_PUBLISHED |

## Conclusioni ammesse

- Candidate clarification proposal for user review
- Functionality not clear from approved source
- Need clarification
- Source\-model relationship needs review
- Structured evidence not sufficiently recoverable

## SRS

### REVIEW-0001

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** excluded phrase\: starting point from

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:5

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:5
- Section 0\.1 N\.A Marco Leo Starting point from VSM01 project, paragraph 011 \(page 8\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Added Soft Reset Procedure STBIO1_v2 1.6.2 9/1/2025 Ugo Garozzo Adde new OTP routines description, Adde Soft Reset Procedures STBIO1_v3 2 9/3/2025 Ugo Garozzo Add new output on TOP o_BDC_PPG, added Power Domain, Chanced ADSP IP ADSP_v0.3.21.
```

### REVIEW-0002

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:6

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:6
- Section 5 STBIO1 toplevel overview, paragraph 007 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
STBIO1 is an Analog Front End Device with embedded process capabilities.
```

### REVIEW-0003

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:7

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:7
- Section 5 STBIO1 toplevel overview, paragraph 017 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The ECG signal chain has several complementary features supporting ECG measurement, such as driven reference for common-mode rejection and lead off detection to identify a fallen electrode.
```

### REVIEW-0004

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:8

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:8
- Section 5 STBIO1 toplevel overview, paragraph 042 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain.
```

### REVIEW-0005

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:9

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:9
- Section 5 STBIO1 toplevel overview, paragraph 047 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The advanced ISPU (32bit proprietary core) is an ultra-low-power, high-performance programmable core which can execute signal processing and AI algorithms in the edge. The
```

### REVIEW-0006

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:10

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:10
- Section 5 STBIO1 toplevel overview, paragraph 004 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0007

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:11

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:11
- Section 5 STBIO1 toplevel overview, paragraph 020 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The BIA signal chain is designed for body impedance and human breathing measurements with a configurable excitation path and measurement path. BIA channel delivers both the real and the imaginary parts of the body and the breathing impedance.
```

### REVIEW-0008

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** excluded phrase\: ultra\-low\-power hardware circuitry

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:12

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:12
- Section 5 STBIO1 toplevel overview, paragraph 026 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
STBIO1 is optimized ultra-low-power hardware circuitry for real-time execution of the algorithms is a state-of-the-art feature for any personal electronics, from wearable accessories to high-end applications.
```

### REVIEW-0009

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:13

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:13
- Section 5 STBIO1 toplevel overview, paragraph 038 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main
```

### REVIEW-0010

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** excluded phrase\: party tools/ide

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:14

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:14
- Section 5 STBIO1 toplevel overview, paragraph 004 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
party tools/IDE. ISPU has 32 Kbyte program RAM, 24 Kbyte Data RAM capability and Floating- point support.
```

### REVIEW-0011

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:15

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:15
- Section 5 STBIO1 toplevel overview, paragraph 006 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
FIFO digital IPs oversees data collecting from multiple sources: internal and external data read by sensor hub, meta-data generated from both ADSP and ISPU.
```

### REVIEW-0012

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:16

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:16
- Section 5 STBIO1 toplevel overview, paragraph 013 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
All the data are stored inside a Smart FIFO that can be configured as: • Unique FIFO: Classic FIFO, the First Data that is written inside the Memory is also the First that is read.
```

### REVIEW-0013

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:17

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:17
- Section 64 Hz\., paragraph 028 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
o Sleep: where measures are finished, eventually only ADSP and/or ISPU is terminating its algorithms and writing elaborated data in FIFO.
```

### REVIEW-0014

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** excluded phrase\: in the last case

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:18

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:18
- Section 64 Hz\., paragraph 012 \(page 14\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In the last case, the device will remain in SLEEP_OPERATIVE (as described in the next paragraphs).
```

### REVIEW-0015

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:19

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:19
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 008 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Set DS_SEL bit in Device_Config_Channel register to 1 and PPG_ELAB to 0 in General_Parameters_PPG o This will cut the communication between Main Controller and ADSP • Analog control Interface samples ECG and BIA signals from ADC, average and stores data sampled in appropriate in FIFO.
```

### REVIEW-0016

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:20

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:20
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 013 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Analog control Interface samples GSR signal from ADC and stores GSR data raw in FIFO.
```

### REVIEW-0017

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:21

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:21
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 015 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Analog control Interface samples PPG signal from ADC, average (according to the user's configuration) and stores data in FIFO.
```

### REVIEW-0018

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:22

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:22
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 020 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this case, the ISPU shall read the data from FIFO and can communicate with the ADSP.
```

### REVIEW-0019

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:23

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:23
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 024 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Set DS_SEL bit in Device_Config_Channel register to 0 o Set PPG_ELAB to 1 if also PPG data shall be elaborated by the ADSP • Analog control Interface samples of ECG, BIA or GSR from ADC, average and stores data sampled in appropriate registers (SYSTEM REGISTERS from 0x007C to 0x0094) accessible by ADSP and other AHB Master.
```

### REVIEW-0020

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:24

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:24
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 032 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
o If PPG_ELAB is set to 1, ADSP Shall read PPG Raw Data Directly from FIFO • Finished processing phase ADSP stores elaborated data in FIFO.
```

### REVIEW-0021

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:25

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:25
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 019 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this mode, the ADSP is turned off, but it's possible to turn on the ISPU before the start of a measurement Cycle. In this case, the ISPU shall read the data from FIFO and can
```

### REVIEW-0022

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:26

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:26
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 031 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ECG, BIA or GSR data raw in SYSTEM REGISTERS are processed by ADSP.
```

### REVIEW-0023

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:27

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:27
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 035 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this mode is possible to turn on the ISPU to work with raw data and/or ADSP elaborated Data.
```

### REVIEW-0024

**Documento:** SRS

**Posizione:** Power\-domain architecture

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:30

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:30
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 007 \(page 32\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Power Domain (PD): A set of logic blocks sharing the same power supply, which can be powered on/off independently.
```

### REVIEW-0025

**Documento:** SRS

**Posizione:** Power\-domain architecture

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:31

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:31
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 009 \(page 32\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Always-On Domain (AON): Domain that is always powered, even in low-power modes.
```

### REVIEW-0026

**Documento:** SRS

**Posizione:** Power\-domain architecture

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:32

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:32
- Section 10\.4\.1 PD\_TOP1V2 \(under Section 10\.4 Power Domain Descriptions\), paragraph 005 \(page 33\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Function: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only).
```

### REVIEW-0027

**Documento:** SRS

**Posizione:** Power\-domain architecture

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:33

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:33
- Section 10\.4\.3 PD\_TOP3V3 \(under Section 10\.4 Power Domain Descriptions\), paragraph 015 \(page 33\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It provides 4.7V of power supply to the OTP memory block during programming (write) operations • Control: Managed by hardware.
```

### REVIEW-0028

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:34

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:34
- Section 13\.1\.1\.4 Clocks and Reset \(under Section 13\.1\.1 PMU\), paragraph 009 \(page 45\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Clocks scheme is shown in the above figure Req_ID Source Target Path Delay Clock Gating Analog Control and Description F Max Requirements Definition DDS_STBIO1_1020 stbio1_top.
```

### REVIEW-0029

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:35

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:35
- Section 13\.1\.2 PAD Mux \(under Section 13 Modules\), paragraph 004 \(page 49\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In the following table are reported the Pad Configuration for each operative mode of the device.
```

### REVIEW-0030

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:36

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:36
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 079 \(page 58\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
gpio2_irq_sel=4) input force = V1V2 SUPPLY (en=1) force = V1V2 SUPPLY (en=1) ck_64k ADC in - tdo GPIO3/PMBF Analog General-Purpose irq_fifo (IRQ_SEL1.
```

### REVIEW-0031

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:37

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:37
- Section 13\.1\.3\.1 Main Controller TOP Description \(under Section 13\.1\.3 Main Controller TOP\), paragraph 004 \(page 74\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The Main Controller is in charge of generating and receiving all the control signals for the Analog Domain, furthermore, performs DSP elaboration on ADC Output and writes it in different Address.
```

### REVIEW-0032

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:38

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:38
- Section 13\.1\.3\.1 Main Controller TOP Description \(under Section 13\.1\.3 Main Controller TOP\), paragraph 008 \(page 74\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
next chapter. Together with the Analog Domain, this IP is interfaced with the FIFO Controller, the ADSP and the PMU, these last two will not be described in this document. The IP is divided into
```

### REVIEW-0033

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:39

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:39
- Section 13\.1\.3\.3 Main Controller Peculiar Requirements \(under Section 13\.1\.3 Main Controller TOP\), paragraph 022 \(page 85\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Main Controller manage all the Analog domain, so all its requirements shall be considered as High Priority.
```

### REVIEW-0034

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:40

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:40
- Section 13\.2\.1\.1 ADSP Peculiar Requirements \(under Section 13\.2\.1 ADSP integration\), paragraph 036 \(page 87\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The selected OTP memory has a data bit cut size of 640 bits with an 8-bit word size.
```

### REVIEW-0035

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:41

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:41
- Section 13\.2\.1\.1\.2 Requirements \(under Section 13\.2\.1\.1 ADSP Peculiar Requirements\), paragraph 034 \(page 89\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The same register also contain a SOFT_RESET bit used to trigger the corresponding soft reset routine.
```

### REVIEW-0036

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** signal\-level detail not eligible for top\-level descriptive text

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:42

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:42
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 044 \(page 99\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Port name Direction Type TOP CONNECTION rst_n input POR i_if_cs input CS for SPI interface o_if_cs_tud output Control for CS PAD.
```

### REVIEW-0037

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:43

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:43
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 026 \(page 99\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
i2c_hs_mode 1'b0 To activate HS I2C [DDS_STBIO1_8102] i2c_master_code 8'h00 Master code for HS I2C [DDS_STBIO1_8103] ser_mode "i2c_spi" To choose if the interface is SPI only, I2C only or both.
```

### REVIEW-0038

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** signal\-level detail not eligible for top\-level descriptive text

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:44

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:44
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 003 \(page 100\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
i_if_sda_sdi_in input SDA/SDI from pad o_if_sda_sdi_en_n output SDA/SDI pad enable o_if_sda_sdi_out output SDA/SDI to pad o_ctrl_reg_7 output [7:0] 8 configuration bit set by local register (addr.
```

### REVIEW-0039

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** signal\-level detail not eligible for top\-level descriptive text

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:45

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:45
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 004 \(page 101\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Pulse on AHB clock to inform system that AHB clock can be switched off o_ahb_error output Error on AHB side.
```

### REVIEW-0040

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:46

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:46
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 005 \(page 109\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_9000] Description Sensor hub IP is an IP used to read up-to 4 external I2C devices.
```

### REVIEW-0041

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:47

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:47
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 003 \(page 110\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Input sys_clk of sensor hub shall be connected to 8MHz clock to generate I2C communications compliant with FM+ I2C standard.
```

### REVIEW-0042

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:48

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:48
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 027 \(page 110\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
All the values shall be tested since MasterBlaze supports up-to 4 I2C targets connected to I2C network.
```

### REVIEW-0043

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:49

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:49
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 030 \(page 113\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89455449] [End] [DDS_STBIO1_89455232] Requirement: As default, the FIFO shall work in Unique FIFO Mode.
```

### REVIEW-0044

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:50

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:50
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 034 \(page 113\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89455232] [End] [DDS_STBIO1_89456975] Requirement: The user shall select the Multiple FIFO mode setting to 1 the first bit into the FIFO_CFG_MODE and 0 for the Unique FIFO mode.
```

### REVIEW-0045

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:51

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:51
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 039 \(page 113\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89456975] [End] [DDS_STBIO1_89457435] Requirement: The FIFO Controller shall have a 6 i_depth input of 8 bit to be used in Multiple FIFO Mode to define the depth of each subFIFOs.
```

### REVIEW-0046

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:52

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:52
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 015 \(page 114\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89457790] [End] [DDS_STBIO1_00000008] Requirement: If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode.
```

### REVIEW-0047

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** signal\-level detail not eligible for top\-level descriptive text

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:53

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:53
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 015 \(page 121\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ca_stredl_bist_c_sif_reg_e n input BIST Enable for various types of data transfer (Bitmap, memory selection, programma ble algorithms) through serial interface.
```

### REVIEW-0048

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** signal\-level detail not eligible for top\-level descriptive text

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:54

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:54
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 008 \(page 127\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ca_stredl_bist_c_tst_gated clock input BIST Clock Gating Signal for the entire BIST.
```

### REVIEW-0049

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:55

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:55
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 014 \(page 127\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Used to force clock gating cell transparenc y in ATPG mode .
```

### REVIEW-0050

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:56

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:56
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 029 \(page 127\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
allows to force reset synchronizin g circuit transparenc y in ATPG mode.
```

### REVIEW-0051

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:57

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:57
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 059 \(page 133\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The device is configurable/readable by the I2C/AHB bridge. This IP is in charge of take an I2C/SPI access and (eventually) transform it into an AHB transaction, to allow the configuration/reading of the device using the ISPU.
```

### REVIEW-0052

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:58

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:58
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 009 \(page 133\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The AFE_BLOCK registers are accessible by I2C/SPI direct access and AHB interface, while the others are only by AHB.
```

### REVIEW-0053

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:59

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:59
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 011 \(page 133\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers.
```

### REVIEW-0054

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:60

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:60
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 025 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
To enable AHB Access, it needs using I2C/SPI direct access mode, for: • First turn-on the LDO1V8 and the Fast-Ring Oscillator (set EN_LDO1V8 and EN_CLKF of VIREF_LDO1V8_CLK16M, see address in the Table 34).
```

### REVIEW-0055

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:61

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:61
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 031 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ow it's possible to configure the registers that are mapped on AHB_Interface as explained in the following example: • Run an I2C/SPI transaction, with the type of AHB access word/byte, at the address 0x59 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0056

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:62

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:62
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 035 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI transaction, with the register address that you want to configure, at the address 0x50 (one of I2C/SPI Internal Configuration Registers), starting from the LSB. In other word, if you need to access at register VIREF_LDO1V8_CLK16M at AHB address
```

### REVIEW-0057

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:63

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:63
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 036 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In other word, if you need to access at register VIREF_LDO1V8_CLK16M at AHB address 0x000C_00CF, you have to perform four I2C/SPI accesses to write: o At address 0x50 0xCF o At address 0x51 0x00 o At address 0x52 0x0C o At address 0x53 → 0x00 • Run an I2C/SPI write, of the new data, at address 0x60 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0058

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:64

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:64
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 046 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI read transition, with the number of byte that you read, at address 0x68 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0059

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:65

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:65
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 003 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The only registers that are accessible also by an I2C/SPI direct access, are the ones of the AFE BLOCK section.
```

### REVIEW-0060

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:66

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:66
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 006 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers (Table 24).
```

### REVIEW-0061

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:67

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:67
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 005 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
To reach a very Low-Power consumption, the AHB interface is disabled as default.
```

### REVIEW-0062

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:68

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:68
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 003 \(page 135\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI transaction with the data that you want to read, at address loaded into the previous step, at the address 0x70 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0063

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:69

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:69
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 006 \(page 135\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It's possible remap the whole AFE register map with AHB addresses column “AHB Start Address” of Table 34), included the AFE_BLOCK block: in this case each registers is accessible with own AHB address (AHB start address + offset) and the I2C/SPI access to these registers must follow the previous procedure.
```

### REVIEW-0064

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:70

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:70
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 012 \(page 135\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This procedure is useful when you are thinking of configuring the STBIO1 by ISPU (with a code previously charged in code memory), leaving to host interface (I2C/SPI) the rule to collect the data from FIFO after AFE sampling and processing phases.
```

### REVIEW-0065

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:71

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:71
- Section 15\.2 Configuration Phase \(under Section 15 Measurement Cycle Examples\), paragraph 005 \(page 147\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The start and the end of a Measurement Cycle is selected by the writing of the dedicated register as described in following examples.
```

### REVIEW-0066

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:72

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:72
- Section 15\.3\.1 ECG Only \(under Section 15\.3 Measurement Cycle\), paragraph 004 \(page 148\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively.
```

### REVIEW-0067

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:73

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:73
- Section 15\.3\.2 ECG and BIA \(under Section 15\.3 Measurement Cycle\), paragraph 007 \(page 150\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively and four averaged BIA data which are BIA_AC_P, BIA_DC_P, BIA_AC_Q and BIA_DC_Q.
```

### REVIEW-0068

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:74

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:74
- Section 15\.3\.3 PPG Only \(under Section 15\.3 Measurement Cycle\), paragraph 006 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, a number of PPG DATA according to user configuration.
```

### REVIEW-0069

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:75

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:75
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 047 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
All user BIST control is done through the controller.
```

### REVIEW-0070

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:76

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:76
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 048 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
through the controller. The controller controls various testing and reporting activities of the memory test. It allows various mode selections and programs the pre-stored synthesized
```

### REVIEW-0071

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:77

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:77
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 049 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It allows various mode selections and programs the pre-stored synthesized algorithms instructions into collars attached to it.
```

### REVIEW-0072

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:78

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:78
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 059 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It includes a TAP controller, a 7-bit instruction register, three test data registers, and the bypass register.
```

### REVIEW-0073

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:79

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:79
- Section 17\.2 Memory BIST Architecture \(under Section 17 BIST\), paragraph 037 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The BIST solution consists of memory-wrapper “collar” and common master “controller” and an IEEE 1149.1 compliant Test Access Port (TAP).
```

### REVIEW-0074

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:80

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:80
- Section 17\.2\.1 MBIST Collar \(under Section 17\.2 Memory BIST Architecture\), paragraph 043 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
After testing it reports the execution status to the controller and manages all the BIST status, diagnosis, repair information and debug data. The collar also provides support for testing multiple
```

### REVIEW-0075

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:82

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:82
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 005 \(page 158\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this configuration, there is only one controller for the entire chip. All associated collars are
```

### REVIEW-0076

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:83

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:83
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 010 \(page 158\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Bend: Indicates that all the activities of the test run of all Memories in the current BIST mode are complete • Bfail: Indicates bfail for a specific memory.
```

### REVIEW-0077

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:84

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:84
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 017 \(page 158\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Tdo:TAP serial output Updated on falling edge of tck INPUT FROM PAD • Tck: TAP clock • Tdi: TAP serial input Sampled on rising edge of tck • Tms: TAP test mode select Sampled on rising edge of tck • Trstn: TAP reset INPUT FROM REGISTER • Memsafe (ADDRESS=0x3E, BIT=0x05): to globally deactivate the memory by making CSN high internally • Mem_atpg_mode (ADDRESS=0x3E, BIT=0x06): Used to constraint few memory inputs and improve controllability and observability.
```

### REVIEW-0078

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:85

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:85
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 010 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_302] Requirement If MODE_CONFIG register is 0x00 the operative mode shall be functional.
```

### REVIEW-0079

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:86

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:86
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 014 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_303] Requirement If MODE_CONFIG register is 0x01 the operative mode shall be SCAN.
```

### REVIEW-0080

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:87

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:87
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 018 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_304] Requirement If MODE_CONFIG register is 0x04 the operative mode shall be BIST.
```

### REVIEW-0081

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:88

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:88
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 022 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_305] Requirement If MODE_CONFIG register is 0x08 the operative mode shall be DEBUG.
```

### REVIEW-0082

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:89

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:89
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 026 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_306] Requirement If MODE_CONFIG register is 0x10 the operative mode shall be ISPU_DEBUG.
```

### REVIEW-0083

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:90

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:90
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 030 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_307] Requirement If MODE_CONFIG register is 0x20 the operative mode shall be Bist MEMSAFE mode.
```

### REVIEW-0084

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** scope not allowed

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:91

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_low\_power\_audit\.csv\:data\-record\:91
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 034 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_308] Requirement If MODE_CONFIG register is 0x40 the operative mode shall be Bist Bypass mode.
```

### REVIEW-0085

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:1

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:1
- Stage 1 OCR page 12, lines 4\-5
- Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio\-impedance, EDA and PPG \(Photoplethysmography\) embedded in a single die\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0086

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:2

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:2
- Stage 1 OCR page 12, lines 35\-35
- ISPU 32\-bit processor\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
ISPU 32-bit processor.
```

### REVIEW-0087

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:4

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:4
- Stage 1 OCR page 12, lines 38\-40
- ADSP is an embedded IP able to elaborate ultra\-low\-power custom DSP functions\. The main purpose of ADSP is to reduce the computation workload on both ISPU and host processor, while saving power through the optimization of both hardware and algorithm\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main purpose of ADSP is to reduce the computation workload on both ISPU and host processor, while saving power through the optimization of both hardware and algorithm.
```

### REVIEW-0088

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:11

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:11
- Section 5 STBIO1 toplevel overview, paragraph 007 \(page 12\)
- STBIO1 is an Analog Front End Device with embedded process capabilities\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
STBIO1 is an Analog Front End Device with embedded process capabilities.
```

### REVIEW-0089

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:14

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:14
- Section 5 STBIO1 toplevel overview, paragraph 047 \(page 12\)
- The advanced ISPU \(32bit proprietary core\) is an ultra\-low\-power, high\-performance programmable core which can execute signal processing and AI algorithms in the edge\. The

**audit_decision:** rejected

**Estratto sorgente:**

```text
The advanced ISPU (32bit proprietary core) is an ultra-low-power, high-performance programmable core which can execute signal processing and AI algorithms in the edge. The
```

### REVIEW-0090

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:15

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:15
- Section 5 STBIO1 toplevel overview, paragraph 004 \(page 12\)
- Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio\-impedance, EDA and PPG \(Photoplethysmography\) embedded in a single die\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0091

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:16

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:16
- Section 5 STBIO1 toplevel overview, paragraph 020 \(page 12\)
- The BIA signal chain is designed for body impedance and human breathing measurements with a configurable excitation path and measurement path\. BIA channel delivers both the real and the imaginary parts of the body and the breathing impedance\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The BIA signal chain is designed for body impedance and human breathing measurements with a configurable excitation path and measurement path. BIA channel delivers both the real and the imaginary parts of the body and the breathing impedance.
```

### REVIEW-0092

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:17

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:17
- Section 5 STBIO1 toplevel overview, paragraph 038 \(page 12\)
- ADSP is an embedded IP able to elaborate ultra\-low\-power custom DSP functions\. The main

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main
```

### REVIEW-0093

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:30

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:30
- Section 10\.1 Introduction \(under Section 10 Power Domains\), paragraph 031 \(page 31\)
- This document paragraph describes the Power Domain architecture implemented in the STBIO1\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
This document paragraph describes the Power Domain architecture implemented in the STBIO1.
```

### REVIEW-0094

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:32

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:32
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 007 \(page 32\)
- Power Domain \(PD\)\: A set of logic blocks sharing the same power supply, which can be powered on/off independently\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Power Domain (PD): A set of logic blocks sharing the same power supply, which can be powered on/off independently.
```

### REVIEW-0095

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:33

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:33
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 009 \(page 32\)
- Always\-On Domain \(AON\)\: Domain that is always powered, even in low\-power modes\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Always-On Domain (AON): Domain that is always powered, even in low-power modes.
```

### REVIEW-0096

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:39

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:39
- Section 13\.1\.3\.1 Main Controller TOP Description \(under Section 13\.1\.3 Main Controller TOP\), paragraph 004 \(page 74\)
- The Main Controller is in charge of generating and receiving all the control signals for the Analog Domain, furthermore, performs DSP elaboration on ADC Output and writes it in different Address\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The Main Controller is in charge of generating and receiving all the control signals for the Analog Domain, furthermore, performs DSP elaboration on ADC Output and writes it in different Address.
```

### REVIEW-0097

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:41

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:41
- Section 13\.1\.3\.3 Main Controller Peculiar Requirements \(under Section 13\.1\.3 Main Controller TOP\), paragraph 022 \(page 85\)
- Main Controller manage all the Analog domain, so all its requirements shall be considered as High Priority\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Main Controller manage all the Analog domain, so all its requirements shall be considered as High Priority.
```

### REVIEW-0098

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:44

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:44
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 044 \(page 99\)
- Port name Direction Type TOP CONNECTION rst\_n input POR i\_if\_cs input CS for SPI interface o\_if\_cs\_tud output Control for CS PAD\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Port name Direction Type TOP CONNECTION rst_n input POR i_if_cs input CS for SPI interface o_if_cs_tud output Control for CS PAD.
```

### REVIEW-0099

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:48

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:48
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 005 \(page 109\)
- \[DDS\_STBIO1\_9000\] Description Sensor hub IP is an IP used to read up\-to 4 external I2C devices\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_9000] Description Sensor hub IP is an IP used to read up-to 4 external I2C devices.
```

### REVIEW-0100

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:50

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:50
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 027 \(page 110\)
- All the values shall be tested since MasterBlaze supports up\-to 4 I2C targets connected to I2C network\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
All the values shall be tested since MasterBlaze supports up-to 4 I2C targets connected to I2C network.
```

### REVIEW-0101

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:74

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:74
- Section 15\.3\.1 ECG Only \(under Section 15\.3 Measurement Cycle\), paragraph 004 \(page 148\)
- This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively.
```

### REVIEW-0102

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:75

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:75
- Section 15\.3\.2 ECG and BIA \(under Section 15\.3 Measurement Cycle\), paragraph 007 \(page 150\)
- This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively and four averaged BIA data which are BIA\_AC\_P, BIA\_DC\_P, BIA\_AC\_Q and BIA\_DC\_Q\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively and four averaged BIA data which are BIA_AC_P, BIA_DC_P, BIA_AC_Q and BIA_DC_Q.
```

### REVIEW-0103

**Documento:** SRS

**Posizione:** Operating Modes

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:76

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_operating\_modes\_audit\.csv\:data\-record\:76
- Section 15\.3\.3 PPG Only \(under Section 15\.3 Measurement Cycle\), paragraph 006 \(page 152\)
- This configuration generates each time slot, a number of PPG DATA according to user configuration\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, a number of PPG DATA according to user configuration.
```

### REVIEW-0104

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:1

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:1
- Stage 1 OCR page 12, lines 4\-5
- Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio\-impedance, EDA and PPG \(Photoplethysmography\) embedded in a single die\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0105

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:2

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:2
- Stage 1 OCR page 12, lines 35\-35
- ISPU 32\-bit processor\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
ISPU 32-bit processor.
```

### REVIEW-0106

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:3

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:3
- Stage 1 OCR page 12, lines 36\-36
- Smart FIFO data collector\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Smart FIFO data collector.
```

### REVIEW-0107

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:4

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:4
- Stage 1 OCR page 12, lines 38\-40
- ADSP is an embedded IP able to elaborate ultra\-low\-power custom DSP functions\. The main purpose of ADSP is to reduce the computation workload on both ISPU and host processor, while saving power through the optimization of both hardware and algorithm\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main purpose of ADSP is to reduce the computation workload on both ISPU and host processor, while saving power through the optimization of both hardware and algorithm.
```

### REVIEW-0108

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:5

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:5
- Stage 1 OCR page 12, lines 42\-45
- Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain\. The data collected by sensor hub is accessible from the Advanced DSP and ISPU, for sensor fusion algorithm elaboration\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain. The data collected by sensor hub is accessible from the Advanced DSP and ISPU, for sensor fusion algorithm elaboration.
```

### REVIEW-0109

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:6

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:6
- Stage 1 OCR page 13, lines 17\-18
- Sensor Hub and Elaboration results\)\. The depth of each Sub\-FIFO is configurable by regmap\. Each Sub\-FIFO behavior as a Classic FIFO\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor Hub and Elaboration results). The depth of each Sub-FIFO is configurable by regmap. Each Sub-FIFO behavior as a Classic FIFO.
```

### REVIEW-0110

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:11

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:11
- Section 5 STBIO1 toplevel overview, paragraph 007 \(page 12\)
- STBIO1 is an Analog Front End Device with embedded process capabilities\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
STBIO1 is an Analog Front End Device with embedded process capabilities.
```

### REVIEW-0111

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:12

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:12
- Section 5 STBIO1 toplevel overview, paragraph 017 \(page 12\)
- The ECG signal chain has several complementary features supporting ECG measurement, such as driven reference for common\-mode rejection and lead off detection to identify a fallen electrode\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The ECG signal chain has several complementary features supporting ECG measurement, such as driven reference for common-mode rejection and lead off detection to identify a fallen electrode.
```

### REVIEW-0112

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:13

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:13
- Section 5 STBIO1 toplevel overview, paragraph 042 \(page 12\)
- Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain.
```

### REVIEW-0113

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:14

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:14
- Section 5 STBIO1 toplevel overview, paragraph 047 \(page 12\)
- The advanced ISPU \(32bit proprietary core\) is an ultra\-low\-power, high\-performance programmable core which can execute signal processing and AI algorithms in the edge\. The

**audit_decision:** rejected

**Estratto sorgente:**

```text
The advanced ISPU (32bit proprietary core) is an ultra-low-power, high-performance programmable core which can execute signal processing and AI algorithms in the edge. The
```

### REVIEW-0114

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:15

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:15
- Section 5 STBIO1 toplevel overview, paragraph 004 \(page 12\)
- Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio\-impedance, EDA and PPG \(Photoplethysmography\) embedded in a single die\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0115

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:16

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:16
- Section 5 STBIO1 toplevel overview, paragraph 020 \(page 12\)
- The BIA signal chain is designed for body impedance and human breathing measurements with a configurable excitation path and measurement path\. BIA channel delivers both the real and the imaginary parts of the body and the breathing impedance\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The BIA signal chain is designed for body impedance and human breathing measurements with a configurable excitation path and measurement path. BIA channel delivers both the real and the imaginary parts of the body and the breathing impedance.
```

### REVIEW-0116

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:17

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:17
- Section 5 STBIO1 toplevel overview, paragraph 038 \(page 12\)
- ADSP is an embedded IP able to elaborate ultra\-low\-power custom DSP functions\. The main

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main
```

### REVIEW-0117

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:18

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:18
- Section 5 STBIO1 toplevel overview, paragraph 006 \(page 13\)
- FIFO digital IPs oversees data collecting from multiple sources\: internal and external data read by sensor hub, meta\-data generated from both ADSP and ISPU\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
FIFO digital IPs oversees data collecting from multiple sources: internal and external data read by sensor hub, meta-data generated from both ADSP and ISPU.
```

### REVIEW-0118

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:19

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:19
- Section 5 STBIO1 toplevel overview, paragraph 013 \(page 13\)
- All the data are stored inside a Smart FIFO that can be configured as\: • Unique FIFO\: Classic FIFO, the First Data that is written inside the Memory is also the First that is read\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
All the data are stored inside a Smart FIFO that can be configured as: • Unique FIFO: Classic FIFO, the First Data that is written inside the Memory is also the First that is read.
```

### REVIEW-0119

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:21

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:21
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 008 \(page 18\)
- Set DS\_SEL bit in Device\_Config\_Channel register to 1 and PPG\_ELAB to 0 in General\_Parameters\_PPG o This will cut the communication between Main Controller and ADSP • Analog control Interface samples ECG and BIA signals from ADC, average and stores data sampled in appropriate in FIFO\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Set DS_SEL bit in Device_Config_Channel register to 1 and PPG_ELAB to 0 in General_Parameters_PPG o This will cut the communication between Main Controller and ADSP • Analog control Interface samples ECG and BIA signals from ADC, average and stores data sampled in appropriate in FIFO.
```

### REVIEW-0120

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:22

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:22
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 013 \(page 18\)
- Analog control Interface samples GSR signal from ADC and stores GSR data raw in FIFO\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Analog control Interface samples GSR signal from ADC and stores GSR data raw in FIFO.
```

### REVIEW-0121

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:23

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:23
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 015 \(page 18\)
- Analog control Interface samples PPG signal from ADC, average \(according to the user's configuration\) and stores data in FIFO\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Analog control Interface samples PPG signal from ADC, average (according to the user's configuration) and stores data in FIFO.
```

### REVIEW-0122

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:24

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:24
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 020 \(page 18\)
- In this case, the ISPU shall read the data from FIFO and can communicate with the ADSP\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this case, the ISPU shall read the data from FIFO and can communicate with the ADSP.
```

### REVIEW-0123

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:25

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:25
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 024 \(page 18\)
- Set DS\_SEL bit in Device\_Config\_Channel register to 0 o Set PPG\_ELAB to 1 if also PPG data shall be elaborated by the ADSP • Analog control Interface samples of ECG, BIA or GSR from ADC, average and stores data sampled in appropriate registers \(SYSTEM REGISTERS from 0x007C to 0x0094\) accessible by ADSP and other AHB Master\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Set DS_SEL bit in Device_Config_Channel register to 0 o Set PPG_ELAB to 1 if also PPG data shall be elaborated by the ADSP • Analog control Interface samples of ECG, BIA or GSR from ADC, average and stores data sampled in appropriate registers (SYSTEM REGISTERS from 0x007C to 0x0094) accessible by ADSP and other AHB Master.
```

### REVIEW-0124

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:26

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:26
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 032 \(page 18\)
- o If PPG\_ELAB is set to 1, ADSP Shall read PPG Raw Data Directly from FIFO • Finished processing phase ADSP stores elaborated data in FIFO\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
o If PPG_ELAB is set to 1, ADSP Shall read PPG Raw Data Directly from FIFO • Finished processing phase ADSP stores elaborated data in FIFO.
```

### REVIEW-0125

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:27

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:27
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 019 \(page 18\)
- In this mode, the ADSP is turned off, but it's possible to turn on the ISPU before the start of a measurement Cycle\. In this case, the ISPU shall read the data from FIFO and can

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this mode, the ADSP is turned off, but it's possible to turn on the ISPU before the start of a measurement Cycle. In this case, the ISPU shall read the data from FIFO and can
```

### REVIEW-0126

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:28

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:28
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 031 \(page 18\)
- ECG, BIA or GSR data raw in SYSTEM REGISTERS are processed by ADSP\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
ECG, BIA or GSR data raw in SYSTEM REGISTERS are processed by ADSP.
```

### REVIEW-0127

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:29

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:29
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 035 \(page 18\)
- In this mode is possible to turn on the ISPU to work with raw data and/or ADSP elaborated Data\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this mode is possible to turn on the ISPU to work with raw data and/or ADSP elaborated Data.
```

### REVIEW-0128

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:36

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:36
- Section 13\.1\.1\.4 Clocks and Reset \(under Section 13\.1\.1 PMU\), paragraph 009 \(page 45\)
- Clocks scheme is shown in the above figure Req\_ID Source Target Path Delay Clock Gating Analog Control and Description F Max Requirements Definition DDS\_STBIO1\_1020 stbio1\_top\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Clocks scheme is shown in the above figure Req_ID Source Target Path Delay Clock Gating Analog Control and Description F Max Requirements Definition DDS_STBIO1_1020 stbio1_top.
```

### REVIEW-0129

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:39

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:39
- Section 13\.1\.3\.1 Main Controller TOP Description \(under Section 13\.1\.3 Main Controller TOP\), paragraph 004 \(page 74\)
- The Main Controller is in charge of generating and receiving all the control signals for the Analog Domain, furthermore, performs DSP elaboration on ADC Output and writes it in different Address\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The Main Controller is in charge of generating and receiving all the control signals for the Analog Domain, furthermore, performs DSP elaboration on ADC Output and writes it in different Address.
```

### REVIEW-0130

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:40

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:40
- Section 13\.1\.3\.1 Main Controller TOP Description \(under Section 13\.1\.3 Main Controller TOP\), paragraph 008 \(page 74\)
- next chapter\. Together with the Analog Domain, this IP is interfaced with the FIFO Controller, the ADSP and the PMU, these last two will not be described in this document\. The IP is divided into

**audit_decision:** rejected

**Estratto sorgente:**

```text
next chapter. Together with the Analog Domain, this IP is interfaced with the FIFO Controller, the ADSP and the PMU, these last two will not be described in this document. The IP is divided into
```

### REVIEW-0131

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:41

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:41
- Section 13\.1\.3\.3 Main Controller Peculiar Requirements \(under Section 13\.1\.3 Main Controller TOP\), paragraph 022 \(page 85\)
- Main Controller manage all the Analog domain, so all its requirements shall be considered as High Priority\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Main Controller manage all the Analog domain, so all its requirements shall be considered as High Priority.
```

### REVIEW-0132

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:42

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:42
- Section 13\.2\.1\.1 ADSP Peculiar Requirements \(under Section 13\.2\.1 ADSP integration\), paragraph 036 \(page 87\)
- The selected OTP memory has a data bit cut size of 640 bits with an 8\-bit word size\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The selected OTP memory has a data bit cut size of 640 bits with an 8-bit word size.
```

### REVIEW-0133

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:43

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:43
- Section 13\.2\.1\.1\.2 Requirements \(under Section 13\.2\.1\.1 ADSP Peculiar Requirements\), paragraph 034 \(page 89\)
- The same register also contain a SOFT\_RESET bit used to trigger the corresponding soft reset routine\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The same register also contain a SOFT_RESET bit used to trigger the corresponding soft reset routine.
```

### REVIEW-0134

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:44

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:44
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 044 \(page 99\)
- Port name Direction Type TOP CONNECTION rst\_n input POR i\_if\_cs input CS for SPI interface o\_if\_cs\_tud output Control for CS PAD\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Port name Direction Type TOP CONNECTION rst_n input POR i_if_cs input CS for SPI interface o_if_cs_tud output Control for CS PAD.
```

### REVIEW-0135

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:45

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:45
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 026 \(page 99\)
- i2c\_hs\_mode 1'b0 To activate HS I2C \[DDS\_STBIO1\_8102\] i2c\_master\_code 8'h00 Master code for HS I2C \[DDS\_STBIO1\_8103\] ser\_mode "i2c\_spi" To choose if the interface is SPI only, I2C only or both\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
i2c_hs_mode 1'b0 To activate HS I2C [DDS_STBIO1_8102] i2c_master_code 8'h00 Master code for HS I2C [DDS_STBIO1_8103] ser_mode "i2c_spi" To choose if the interface is SPI only, I2C only or both.
```

### REVIEW-0136

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:47

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:47
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 004 \(page 101\)
- Pulse on AHB clock to inform system that AHB clock can be switched off o\_ahb\_error output Error on AHB side\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Pulse on AHB clock to inform system that AHB clock can be switched off o_ahb_error output Error on AHB side.
```

### REVIEW-0137

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:48

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:48
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 005 \(page 109\)
- \[DDS\_STBIO1\_9000\] Description Sensor hub IP is an IP used to read up\-to 4 external I2C devices\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_9000] Description Sensor hub IP is an IP used to read up-to 4 external I2C devices.
```

### REVIEW-0138

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:49

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:49
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 003 \(page 110\)
- Input sys\_clk of sensor hub shall be connected to 8MHz clock to generate I2C communications compliant with FM\+ I2C standard\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Input sys_clk of sensor hub shall be connected to 8MHz clock to generate I2C communications compliant with FM+ I2C standard.
```

### REVIEW-0139

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:50

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:50
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 027 \(page 110\)
- All the values shall be tested since MasterBlaze supports up\-to 4 I2C targets connected to I2C network\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
All the values shall be tested since MasterBlaze supports up-to 4 I2C targets connected to I2C network.
```

### REVIEW-0140

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:51

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:51
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 030 \(page 113\)
- \[TO\: IPOS\_FIFO\_CTRL\_89455449\] \[End\] \[DDS\_STBIO1\_89455232\] Requirement\: As default, the FIFO shall work in Unique FIFO Mode\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89455449] [End] [DDS_STBIO1_89455232] Requirement: As default, the FIFO shall work in Unique FIFO Mode.
```

### REVIEW-0141

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:52

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:52
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 034 \(page 113\)
- \[TO\: IPOS\_FIFO\_CTRL\_89455232\] \[End\] \[DDS\_STBIO1\_89456975\] Requirement\: The user shall select the Multiple FIFO mode setting to 1 the first bit into the FIFO\_CFG\_MODE and 0 for the Unique FIFO mode\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89455232] [End] [DDS_STBIO1_89456975] Requirement: The user shall select the Multiple FIFO mode setting to 1 the first bit into the FIFO_CFG_MODE and 0 for the Unique FIFO mode.
```

### REVIEW-0142

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:53

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:53
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 039 \(page 113\)
- \[TO\: IPOS\_FIFO\_CTRL\_89456975\] \[End\] \[DDS\_STBIO1\_89457435\] Requirement\: The FIFO Controller shall have a 6 i\_depth input of 8 bit to be used in Multiple FIFO Mode to define the depth of each subFIFOs\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89456975] [End] [DDS_STBIO1_89457435] Requirement: The FIFO Controller shall have a 6 i_depth input of 8 bit to be used in Multiple FIFO Mode to define the depth of each subFIFOs.
```

### REVIEW-0143

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:54

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:54
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 015 \(page 114\)
- \[TO\: IPOS\_FIFO\_CTRL\_89457790\] \[End\] \[DDS\_STBIO1\_00000008\] Requirement\: If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89457790] [End] [DDS_STBIO1_00000008] Requirement: If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode.
```

### REVIEW-0144

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:56

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:56
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 008 \(page 127\)
- ca\_stredl\_bist\_c\_tst\_gated clock input BIST Clock Gating Signal for the entire BIST\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
ca_stredl_bist_c_tst_gated clock input BIST Clock Gating Signal for the entire BIST.
```

### REVIEW-0145

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:57

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:57
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 014 \(page 127\)
- Used to force clock gating cell transparenc y in ATPG mode \.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Used to force clock gating cell transparenc y in ATPG mode .
```

### REVIEW-0146

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:58

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:58
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 029 \(page 127\)
- allows to force reset synchronizin g circuit transparenc y in ATPG mode\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
allows to force reset synchronizin g circuit transparenc y in ATPG mode.
```

### REVIEW-0147

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:59

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:59
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 059 \(page 133\)
- The device is configurable/readable by the I2C/AHB bridge\. This IP is in charge of take an I2C/SPI access and \(eventually\) transform it into an AHB transaction, to allow the configuration/reading of the device using the ISPU\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The device is configurable/readable by the I2C/AHB bridge. This IP is in charge of take an I2C/SPI access and (eventually) transform it into an AHB transaction, to allow the configuration/reading of the device using the ISPU.
```

### REVIEW-0148

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:60

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:60
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 009 \(page 133\)
- The AFE\_BLOCK registers are accessible by I2C/SPI direct access and AHB interface, while the others are only by AHB\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The AFE_BLOCK registers are accessible by I2C/SPI direct access and AHB interface, while the others are only by AHB.
```

### REVIEW-0149

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:61

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:61
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 011 \(page 133\)
- The I2C/SPI direct access mode is done by the HOST INTF port \(I2C/SPI AHB\) and the address of the AFE\_BLOCK registers are arranged in 4 pages of 64 registers\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers.
```

### REVIEW-0150

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:63

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:63
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 031 \(page 134\)
- ow it's possible to configure the registers that are mapped on AHB\_Interface as explained in the following example\: • Run an I2C/SPI transaction, with the type of AHB access word/byte, at the address 0x59 \(one of I2C/SPI Internal Configuration Registers\)\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
ow it's possible to configure the registers that are mapped on AHB_Interface as explained in the following example: • Run an I2C/SPI transaction, with the type of AHB access word/byte, at the address 0x59 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0151

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:64

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:64
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 035 \(page 134\)
- Run an I2C/SPI transaction, with the register address that you want to configure, at the address 0x50 \(one of I2C/SPI Internal Configuration Registers\), starting from the LSB\. In other word, if you need to access at register VIREF\_LDO1V8\_CLK16M at AHB address

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI transaction, with the register address that you want to configure, at the address 0x50 (one of I2C/SPI Internal Configuration Registers), starting from the LSB. In other word, if you need to access at register VIREF_LDO1V8_CLK16M at AHB address
```

### REVIEW-0152

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:65

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:65
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 036 \(page 134\)
- In other word, if you need to access at register VIREF\_LDO1V8\_CLK16M at AHB address 0x000C\_00CF, you have to perform four I2C/SPI accesses to write\: o At address 0x50 0xCF o At address 0x51 0x00 o At address 0x52 0x0C o At address 0x53 → 0x00 • Run an I2C/SPI write, of the new data, at address 0x60 \(one of I2C/SPI Internal Configuration Registers\)\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
In other word, if you need to access at register VIREF_LDO1V8_CLK16M at AHB address 0x000C_00CF, you have to perform four I2C/SPI accesses to write: o At address 0x50 0xCF o At address 0x51 0x00 o At address 0x52 0x0C o At address 0x53 → 0x00 • Run an I2C/SPI write, of the new data, at address 0x60 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0153

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:66

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:66
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 046 \(page 134\)
- Run an I2C/SPI read transition, with the number of byte that you read, at address 0x68 \(one of I2C/SPI Internal Configuration Registers\)\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI read transition, with the number of byte that you read, at address 0x68 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0154

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:67

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:67
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 003 \(page 134\)
- The only registers that are accessible also by an I2C/SPI direct access, are the ones of the AFE BLOCK section\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The only registers that are accessible also by an I2C/SPI direct access, are the ones of the AFE BLOCK section.
```

### REVIEW-0155

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:68

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:68
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 006 \(page 134\)
- The I2C/SPI direct access mode is done by the HOST INTF port \(I2C/SPI AHB\) and the address of the AFE\_BLOCK registers are arranged in 4 pages of 64 registers \(Table 24\)\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers (Table 24).
```

### REVIEW-0156

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:69

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:69
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 005 \(page 134\)
- To reach a very Low\-Power consumption, the AHB interface is disabled as default\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
To reach a very Low-Power consumption, the AHB interface is disabled as default.
```

### REVIEW-0157

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:70

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:70
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 003 \(page 135\)
- Run an I2C/SPI transaction with the data that you want to read, at address loaded into the previous step, at the address 0x70 \(one of I2C/SPI Internal Configuration Registers\)\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI transaction with the data that you want to read, at address loaded into the previous step, at the address 0x70 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0158

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:71

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:71
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 006 \(page 135\)
- It's possible remap the whole AFE register map with AHB addresses column “AHB Start Address” of Table 34\), included the AFE\_BLOCK block\: in this case each registers is accessible with own AHB address \(AHB start address \+ offset\) and the I2C/SPI access to these registers must follow the previous procedure\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
It's possible remap the whole AFE register map with AHB addresses column “AHB Start Address” of Table 34), included the AFE_BLOCK block: in this case each registers is accessible with own AHB address (AHB start address + offset) and the I2C/SPI access to these registers must follow the previous procedure.
```

### REVIEW-0159

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:72

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:72
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 012 \(page 135\)
- This procedure is useful when you are thinking of configuring the STBIO1 by ISPU \(with a code previously charged in code memory\), leaving to host interface \(I2C/SPI\) the rule to collect the data from FIFO after AFE sampling and processing phases\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
This procedure is useful when you are thinking of configuring the STBIO1 by ISPU (with a code previously charged in code memory), leaving to host interface (I2C/SPI) the rule to collect the data from FIFO after AFE sampling and processing phases.
```

### REVIEW-0160

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:73

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:73
- Section 15\.2 Configuration Phase \(under Section 15 Measurement Cycle Examples\), paragraph 005 \(page 147\)
- The start and the end of a Measurement Cycle is selected by the writing of the dedicated register as described in following examples\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The start and the end of a Measurement Cycle is selected by the writing of the dedicated register as described in following examples.
```

### REVIEW-0161

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:74

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:74
- Section 15\.3\.1 ECG Only \(under Section 15\.3 Measurement Cycle\), paragraph 004 \(page 148\)
- This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively.
```

### REVIEW-0162

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:75

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:75
- Section 15\.3\.2 ECG and BIA \(under Section 15\.3 Measurement Cycle\), paragraph 007 \(page 150\)
- This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively and four averaged BIA data which are BIA\_AC\_P, BIA\_DC\_P, BIA\_AC\_Q and BIA\_DC\_Q\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively and four averaged BIA data which are BIA_AC_P, BIA_DC_P, BIA_AC_Q and BIA_DC_Q.
```

### REVIEW-0163

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:76

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:76
- Section 15\.3\.3 PPG Only \(under Section 15\.3 Measurement Cycle\), paragraph 006 \(page 152\)
- This configuration generates each time slot, a number of PPG DATA according to user configuration\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, a number of PPG DATA according to user configuration.
```

### REVIEW-0164

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:77

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:77
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 047 \(page 157\)
- All user BIST control is done through the controller\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
All user BIST control is done through the controller.
```

### REVIEW-0165

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:78

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:78
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 048 \(page 157\)
- through the controller\. The controller controls various testing and reporting activities of the memory test\. It allows various mode selections and programs the pre\-stored synthesized

**audit_decision:** rejected

**Estratto sorgente:**

```text
through the controller. The controller controls various testing and reporting activities of the memory test. It allows various mode selections and programs the pre-stored synthesized
```

### REVIEW-0166

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:79

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:79
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 049 \(page 157\)
- It allows various mode selections and programs the pre\-stored synthesized algorithms instructions into collars attached to it\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
It allows various mode selections and programs the pre-stored synthesized algorithms instructions into collars attached to it.
```

### REVIEW-0167

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:80

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:80
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 059 \(page 157\)
- It includes a TAP controller, a 7\-bit instruction register, three test data registers, and the bypass register\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
It includes a TAP controller, a 7-bit instruction register, three test data registers, and the bypass register.
```

### REVIEW-0168

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:81

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:81
- Section 17\.2 Memory BIST Architecture \(under Section 17 BIST\), paragraph 037 \(page 157\)
- The BIST solution consists of memory\-wrapper “collar” and common master “controller” and an IEEE 1149\.1 compliant Test Access Port \(TAP\)\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
The BIST solution consists of memory-wrapper “collar” and common master “controller” and an IEEE 1149.1 compliant Test Access Port (TAP).
```

### REVIEW-0169

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:82

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:82
- Section 17\.2\.1 MBIST Collar \(under Section 17\.2 Memory BIST Architecture\), paragraph 043 \(page 157\)
- After testing it reports the execution status to the controller and manages all the BIST status, diagnosis, repair information and debug data\. The collar also provides support for testing multiple

**audit_decision:** rejected

**Estratto sorgente:**

```text
After testing it reports the execution status to the controller and manages all the BIST status, diagnosis, repair information and debug data. The collar also provides support for testing multiple
```

### REVIEW-0170

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:84

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:84
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 005 \(page 158\)
- In this configuration, there is only one controller for the entire chip\. All associated collars are

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this configuration, there is only one controller for the entire chip. All associated collars are
```

### REVIEW-0171

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:85

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:85
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 010 \(page 158\)
- Bend\: Indicates that all the activities of the test run of all Memories in the current BIST mode are complete • Bfail\: Indicates bfail for a specific memory\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Bend: Indicates that all the activities of the test run of all Memories in the current BIST mode are complete • Bfail: Indicates bfail for a specific memory.
```

### REVIEW-0172

**Documento:** SRS

**Posizione:** Power States

**Classe del blocco:** audit\_rejected

**Spiegazione:** no eligible configured topic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:86

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_power\_states\_audit\.csv\:data\-record\:86
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 017 \(page 158\)
- Tdo\:TAP serial output Updated on falling edge of tck INPUT FROM PAD • Tck\: TAP clock • Tdi\: TAP serial input Sampled on rising edge of tck • Tms\: TAP test mode select Sampled on rising edge of tck • Trstn\: TAP reset INPUT FROM REGISTER • Memsafe \(ADDRESS=0x3E, BIT=0x05\)\: to globally deactivate the memory by making CSN high internally • Mem\_atpg\_mode \(ADDRESS=0x3E, BIT=0x06\)\: Used to constraint few memory inputs and improve controllability and observability\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Tdo:TAP serial output Updated on falling edge of tck INPUT FROM PAD • Tck: TAP clock • Tdi: TAP serial input Sampled on rising edge of tck • Tms: TAP test mode select Sampled on rising edge of tck • Trstn: TAP reset INPUT FROM REGISTER • Memsafe (ADDRESS=0x3E, BIT=0x05): to globally deactivate the memory by making CSN high internally • Mem_atpg_mode (ADDRESS=0x3E, BIT=0x06): Used to constraint few memory inputs and improve controllability and observability.
```

### REVIEW-0173

**Documento:** SRS

**Posizione:** System Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_summary\_audit\.csv\:data\-record\:15

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_summary\_audit\.csv\:data\-record\:15
- Section 5 STBIO1 toplevel overview, paragraph 004 \(page 12\)
- Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio\-impedance, EDA and PPG \(Photoplethysmography\) embedded in a single die\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0174

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:1

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:1
- Stage 1 OCR page 12, lines 4\-5

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0175

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:2

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:2
- Stage 1 OCR page 12, lines 35\-35

**audit_decision:** rejected

**Estratto sorgente:**

```text
ISPU 32-bit processor.
```

### REVIEW-0176

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:3

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:3
- Stage 1 OCR page 12, lines 36\-36

**audit_decision:** rejected

**Estratto sorgente:**

```text
Smart FIFO data collector.
```

### REVIEW-0177

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:4

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:4
- Stage 1 OCR page 12, lines 38\-40

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main purpose of ADSP is to reduce the computation workload on both ISPU and host processor, while saving power through the optimization of both hardware and algorithm.
```

### REVIEW-0178

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** named block text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:5

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:5
- Stage 1 OCR page 12, lines 38\-40

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main purpose of ADSP is to reduce the computation workload on both ISPU and host processor, while saving power through the optimization of both hardware and algorithm.
```

### REVIEW-0179

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** named block text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:6

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:6
- Stage 1 OCR page 12, lines 42\-45

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain. The data collected by sensor hub is accessible from the Advanced DSP and ISPU, for sensor fusion algorithm elaboration.
```

### REVIEW-0180

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:7

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:7
- Stage 1 OCR page 13, lines 17\-18

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor Hub and Elaboration results). The depth of each Sub-FIFO is configurable by regmap. Each Sub-FIFO behavior as a Classic FIFO.
```

### REVIEW-0181

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:8

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:8
- Stage 1 OCR page 13, lines 17\-18

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor Hub and Elaboration results). The depth of each Sub-FIFO is configurable by regmap. Each Sub-FIFO behavior as a Classic FIFO.
```

### REVIEW-0182

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:9

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:9
- Stage 1 OCR power\-domain table/description \(PD\_TOP1V2\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOP1V2: Included block(s): ADSP,, multi_channel_fifo, i2c_spi_slave, main_controller_top, senshub_mst_i2c, pad_mux, pmu, stbio1_regmap, scan_out_mux, xbar_afe. Domain type: Always-On. Control mode: HW. Notes: Always active. • Function: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only). • Characteristics: Never powered down. • Control: Managed by hardware.
```

### REVIEW-0183

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:10

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:10
- Stage 1 OCR power\-domain table/description \(PD\_STREDL\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_STREDL: Included block(s): STREDL. Domain type: Switchable. Control mode: SW. Notes: Can be powered down in idle. • Function: Powers the STREDL core and associated cache. • Characteristics: Can be powered down when STREDL is not in use. • Control: Managed via software (power management driver)(see 12.3.1)
```

### REVIEW-0184

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:11

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:11
- Stage 1 OCR power\-domain table/description \(PD\_TOP3V3\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOP3V3: Included block(s): H9A_MEM_OTP_ PUMP_85AL05_2. Domain type: Always-On. Voltage: 3A. Control mode: HW. Notes: Always active. • Function: power supply to the OTP memory block. • Characteristics: Never powered down. It provides 4.7V of power supply to the OTP memory block during programming (write) operations • Control: Managed by hardware.
```

### REVIEW-0185

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:12

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:12
- Stage 1 OCR power\-domain table/description \(PD\_TOPIO\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOPIO: Included block(s): level_shifter_sel. Domain type: Always-On. Control mode: HW. Notes: Always active 32 10.4.. • Function: Powers communication PAD • Characteristics: Never powered down. • Control: Managed by hardware.
```

### REVIEW-0186

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:13

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:13
- Section 5 STBIO1 toplevel overview, paragraph 007 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
STBIO1 is an Analog Front End Device with embedded process capabilities.
```

### REVIEW-0187

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:14

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:14
- Section 5 STBIO1 toplevel overview, paragraph 007 \(page 12\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
STBIO1 is an Analog Front End Device with embedded process capabilities.
```

### REVIEW-0188

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:15

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:15
- Section 5 STBIO1 toplevel overview, paragraph 017 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The ECG signal chain has several complementary features supporting ECG measurement, such as driven reference for common-mode rejection and lead off detection to identify a fallen electrode.
```

### REVIEW-0189

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:16

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:16
- Section 5 STBIO1 toplevel overview, paragraph 017 \(page 12\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
The ECG signal chain has several complementary features supporting ECG measurement, such as driven reference for common-mode rejection and lead off detection to identify a fallen electrode.
```

### REVIEW-0190

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** named block text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:17

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:17
- Section 5 STBIO1 toplevel overview, paragraph 042 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain.
```

### REVIEW-0191

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:18

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:18
- Section 5 STBIO1 toplevel overview, paragraph 047 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The advanced ISPU (32bit proprietary core) is an ultra-low-power, high-performance programmable core which can execute signal processing and AI algorithms in the edge. The
```

### REVIEW-0192

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:19

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:19
- Section 5 STBIO1 toplevel overview, paragraph 004 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0193

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: unsupported descriptive clause requires explicit projection

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:20

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:20
- Section 5 STBIO1 toplevel overview, paragraph 020 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The BIA signal chain is designed for body impedance and human breathing measurements with a configurable excitation path and measurement path. BIA channel delivers both the real and the imaginary parts of the body and the breathing impedance.
```

### REVIEW-0194

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:21

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:21
- Section 5 STBIO1 toplevel overview, paragraph 020 \(page 12\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
The BIA signal chain is designed for body impedance and human breathing measurements with a configurable excitation path and measurement path. BIA channel delivers both the real and the imaginary parts of the body and the breathing impedance.
```

### REVIEW-0195

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:22

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:22
- Section 5 STBIO1 toplevel overview, paragraph 038 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main
```

### REVIEW-0196

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:23

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:23
- Section 5 STBIO1 toplevel overview, paragraph 006 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
FIFO digital IPs oversees data collecting from multiple sources: internal and external data read by sensor hub, meta-data generated from both ADSP and ISPU.
```

### REVIEW-0197

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** named block text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:24

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:24
- Section 5 STBIO1 toplevel overview, paragraph 006 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
FIFO digital IPs oversees data collecting from multiple sources: internal and external data read by sensor hub, meta-data generated from both ADSP and ISPU.
```

### REVIEW-0198

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:25

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:25
- Section 5 STBIO1 toplevel overview, paragraph 013 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
All the data are stored inside a Smart FIFO that can be configured as: • Unique FIFO: Classic FIFO, the First Data that is written inside the Memory is also the First that is read.
```

### REVIEW-0199

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:26

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:26
- Section 5 STBIO1 toplevel overview, paragraph 013 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
All the data are stored inside a Smart FIFO that can be configured as: • Unique FIFO: Classic FIFO, the First Data that is written inside the Memory is also the First that is read.
```

### REVIEW-0200

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:27

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:27
- Section 64 Hz\., paragraph 028 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
o Sleep: where measures are finished, eventually only ADSP and/or ISPU is terminating its algorithms and writing elaborated data in FIFO.
```

### REVIEW-0201

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** named block text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:28

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:28
- Section 64 Hz\., paragraph 028 \(page 13\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
o Sleep: where measures are finished, eventually only ADSP and/or ISPU is terminating its algorithms and writing elaborated data in FIFO.
```

### REVIEW-0202

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: unsupported descriptive clause requires explicit projection

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:29

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:29
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 008 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Set DS_SEL bit in Device_Config_Channel register to 1 and PPG_ELAB to 0 in General_Parameters_PPG o This will cut the communication between Main Controller and ADSP • Analog control Interface samples ECG and BIA signals from ADC, average and stores data sampled in appropriate in FIFO.
```

### REVIEW-0203

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:30

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:30
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 008 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Set DS_SEL bit in Device_Config_Channel register to 1 and PPG_ELAB to 0 in General_Parameters_PPG o This will cut the communication between Main Controller and ADSP • Analog control Interface samples ECG and BIA signals from ADC, average and stores data sampled in appropriate in FIFO.
```

### REVIEW-0204

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:31

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:31
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 013 \(page 18\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
Analog control Interface samples GSR signal from ADC and stores GSR data raw in FIFO.
```

### REVIEW-0205

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:32

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:32
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 015 \(page 18\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
Analog control Interface samples PPG signal from ADC, average (according to the user's configuration) and stores data in FIFO.
```

### REVIEW-0206

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:33

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:33
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 020 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this case, the ISPU shall read the data from FIFO and can communicate with the ADSP.
```

### REVIEW-0207

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:34

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:34
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 020 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this case, the ISPU shall read the data from FIFO and can communicate with the ADSP.
```

### REVIEW-0208

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:35

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:35
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 024 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Set DS_SEL bit in Device_Config_Channel register to 0 o Set PPG_ELAB to 1 if also PPG data shall be elaborated by the ADSP • Analog control Interface samples of ECG, BIA or GSR from ADC, average and stores data sampled in appropriate registers (SYSTEM REGISTERS from 0x007C to 0x0094) accessible by ADSP and other AHB Master.
```

### REVIEW-0209

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:36

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:36
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 032 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
o If PPG_ELAB is set to 1, ADSP Shall read PPG Raw Data Directly from FIFO • Finished processing phase ADSP stores elaborated data in FIFO.
```

### REVIEW-0210

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:37

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:37
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 032 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
o If PPG_ELAB is set to 1, ADSP Shall read PPG Raw Data Directly from FIFO • Finished processing phase ADSP stores elaborated data in FIFO.
```

### REVIEW-0211

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:38

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:38
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 019 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this mode, the ADSP is turned off, but it's possible to turn on the ISPU before the start of a measurement Cycle. In this case, the ISPU shall read the data from FIFO and can
```

### REVIEW-0212

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:39

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:39
- Section 8\.1 Data Storage Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 019 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this mode, the ADSP is turned off, but it's possible to turn on the ISPU before the start of a measurement Cycle. In this case, the ISPU shall read the data from FIFO and can
```

### REVIEW-0213

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** named block text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:40

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:40
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 031 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ECG, BIA or GSR data raw in SYSTEM REGISTERS are processed by ADSP.
```

### REVIEW-0214

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:41

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:41
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 035 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this mode is possible to turn on the ISPU to work with raw data and/or ADSP elaborated Data.
```

### REVIEW-0215

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** named block text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:42

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:42
- Section 8\.2 Normal Mode \(under Section 8 STBIO1\: Functional Modes\), paragraph 035 \(page 18\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this mode is possible to turn on the ISPU to work with raw data and/or ADSP elaborated Data.
```

### REVIEW-0216

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:43

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:43
- Section 10\.1 Introduction \(under Section 10 Power Domains\), paragraph 031 \(page 31\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This document paragraph describes the Power Domain architecture implemented in the STBIO1.
```

### REVIEW-0217

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:44

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:44
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 011 \(page 32\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Retention Domain: Domain that retains register state even when the main logic is powered down.
```

### REVIEW-0218

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:45

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:45
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 011 \(page 32\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Retention Domain: Domain that retains register state even when the main logic is powered down.
```

### REVIEW-0219

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:46

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:46
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 007 \(page 32\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Power Domain (PD): A set of logic blocks sharing the same power supply, which can be powered on/off independently.
```

### REVIEW-0220

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:47

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:47
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 007 \(page 32\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
Power Domain (PD): A set of logic blocks sharing the same power supply, which can be powered on/off independently.
```

### REVIEW-0221

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:48

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:48
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 009 \(page 32\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Always-On Domain (AON): Domain that is always powered, even in low-power modes.
```

### REVIEW-0222

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:49

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:49
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 009 \(page 32\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
Always-On Domain (AON): Domain that is always powered, even in low-power modes.
```

### REVIEW-0223

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:50

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:50
- Section 10\.4\.1 PD\_TOP1V2 \(under Section 10\.4 Power Domain Descriptions\), paragraph 005 \(page 33\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Function: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only).
```

### REVIEW-0224

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** named block text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:51

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:51
- Section 10\.4\.1 PD\_TOP1V2 \(under Section 10\.4 Power Domain Descriptions\), paragraph 005 \(page 33\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Function: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only).
```

### REVIEW-0225

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:52

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:52
- Section 10\.4\.3 PD\_TOP3V3 \(under Section 10\.4 Power Domain Descriptions\), paragraph 015 \(page 33\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It provides 4.7V of power supply to the OTP memory block during programming (write) operations • Control: Managed by hardware.
```

### REVIEW-0226

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:53

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:53
- Section 10\.4\.3 PD\_TOP3V3 \(under Section 10\.4 Power Domain Descriptions\), paragraph 015 \(page 33\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It provides 4.7V of power supply to the OTP memory block during programming (write) operations • Control: Managed by hardware.
```

### REVIEW-0227

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:54

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:54
- Section 13\.1\.1\.4 Clocks and Reset \(under Section 13\.1\.1 PMU\), paragraph 009 \(page 45\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Clocks scheme is shown in the above figure Req_ID Source Target Path Delay Clock Gating Analog Control and Description F Max Requirements Definition DDS_STBIO1_1020 stbio1_top.
```

### REVIEW-0228

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:55

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:55
- Section 13\.1\.2 PAD Mux \(under Section 13 Modules\), paragraph 004 \(page 49\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In the following table are reported the Pad Configuration for each operative mode of the device.
```

### REVIEW-0229

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:56

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:56
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 079 \(page 58\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
gpio2_irq_sel=4) input force = V1V2 SUPPLY (en=1) force = V1V2 SUPPLY (en=1) ck_64k ADC in - tdo GPIO3/PMBF Analog General-Purpose irq_fifo (IRQ_SEL1.
```

### REVIEW-0230

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:57

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:57
- Section 13\.1\.3\.1 Main Controller TOP Description \(under Section 13\.1\.3 Main Controller TOP\), paragraph 004 \(page 74\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The Main Controller is in charge of generating and receiving all the control signals for the Analog Domain, furthermore, performs DSP elaboration on ADC Output and writes it in different Address.
```

### REVIEW-0231

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:58

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:58
- Section 13\.1\.3\.1 Main Controller TOP Description \(under Section 13\.1\.3 Main Controller TOP\), paragraph 008 \(page 74\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
next chapter. Together with the Analog Domain, this IP is interfaced with the FIFO Controller, the ADSP and the PMU, these last two will not be described in this document. The IP is divided into
```

### REVIEW-0232

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:59

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:59
- Section 13\.1\.3\.3 Main Controller Peculiar Requirements \(under Section 13\.1\.3 Main Controller TOP\), paragraph 022 \(page 85\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Main Controller manage all the Analog domain, so all its requirements shall be considered as High Priority.
```

### REVIEW-0233

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:60

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:60
- Section 13\.2\.1\.1 ADSP Peculiar Requirements \(under Section 13\.2\.1 ADSP integration\), paragraph 036 \(page 87\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The selected OTP memory has a data bit cut size of 640 bits with an 8-bit word size.
```

### REVIEW-0234

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:61

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:61
- Section 13\.2\.1\.1\.2 Requirements \(under Section 13\.2\.1\.1 ADSP Peculiar Requirements\), paragraph 034 \(page 89\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The same register also contain a SOFT_RESET bit used to trigger the corresponding soft reset routine.
```

### REVIEW-0235

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:62

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:62
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 044 \(page 99\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Port name Direction Type TOP CONNECTION rst_n input POR i_if_cs input CS for SPI interface o_if_cs_tud output Control for CS PAD.
```

### REVIEW-0236

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:63

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:63
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 044 \(page 99\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Port name Direction Type TOP CONNECTION rst_n input POR i_if_cs input CS for SPI interface o_if_cs_tud output Control for CS PAD.
```

### REVIEW-0237

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:64

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:64
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 026 \(page 99\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
i2c_hs_mode 1'b0 To activate HS I2C [DDS_STBIO1_8102] i2c_master_code 8'h00 Master code for HS I2C [DDS_STBIO1_8103] ser_mode "i2c_spi" To choose if the interface is SPI only, I2C only or both.
```

### REVIEW-0238

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:65

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:65
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 026 \(page 99\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
i2c_hs_mode 1'b0 To activate HS I2C [DDS_STBIO1_8102] i2c_master_code 8'h00 Master code for HS I2C [DDS_STBIO1_8103] ser_mode "i2c_spi" To choose if the interface is SPI only, I2C only or both.
```

### REVIEW-0239

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:66

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:66
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 003 \(page 100\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
i_if_sda_sdi_in input SDA/SDI from pad o_if_sda_sdi_en_n output SDA/SDI pad enable o_if_sda_sdi_out output SDA/SDI to pad o_ctrl_reg_7 output [7:0] 8 configuration bit set by local register (addr.
```

### REVIEW-0240

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:67

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:67
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 003 \(page 100\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
i_if_sda_sdi_in input SDA/SDI from pad o_if_sda_sdi_en_n output SDA/SDI pad enable o_if_sda_sdi_out output SDA/SDI to pad o_ctrl_reg_7 output [7:0] 8 configuration bit set by local register (addr.
```

### REVIEW-0241

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:68

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:68
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 004 \(page 101\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Pulse on AHB clock to inform system that AHB clock can be switched off o_ahb_error output Error on AHB side.
```

### REVIEW-0242

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:69

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:69
- Section 13\.2\.2 I2C\_SPI\_AHB integration \(under Section 13\.2 IPs\), paragraph 004 \(page 101\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Pulse on AHB clock to inform system that AHB clock can be switched off o_ahb_error output Error on AHB side.
```

### REVIEW-0243

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:70

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:70
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 005 \(page 109\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_9000] Description Sensor hub IP is an IP used to read up-to 4 external I2C devices.
```

### REVIEW-0244

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:71

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:71
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 003 \(page 110\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Input sys_clk of sensor hub shall be connected to 8MHz clock to generate I2C communications compliant with FM+ I2C standard.
```

### REVIEW-0245

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:72

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:72
- Section 13\.2\.3\.1 SensorHub Peculiar Requirements \(under Section 13\.2\.3 SensorHub integration\), paragraph 027 \(page 110\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
All the values shall be tested since MasterBlaze supports up-to 4 I2C targets connected to I2C network.
```

### REVIEW-0246

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:73

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:73
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 030 \(page 113\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89455449] [End] [DDS_STBIO1_89455232] Requirement: As default, the FIFO shall work in Unique FIFO Mode.
```

### REVIEW-0247

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:74

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:74
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 034 \(page 113\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89455232] [End] [DDS_STBIO1_89456975] Requirement: The user shall select the Multiple FIFO mode setting to 1 the first bit into the FIFO_CFG_MODE and 0 for the Unique FIFO mode.
```

### REVIEW-0248

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:75

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:75
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 039 \(page 113\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89456975] [End] [DDS_STBIO1_89457435] Requirement: The FIFO Controller shall have a 6 i_depth input of 8 bit to be used in Multiple FIFO Mode to define the depth of each subFIFOs.
```

### REVIEW-0249

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:76

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:76
- Section 13\.2\.4\.1 FIFO\_CTRL Peculiar Requirements \(under Section 13\.2\.4 FIFO\_CTRL integration\), paragraph 015 \(page 114\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[TO: IPOS_FIFO_CTRL_89457790] [End] [DDS_STBIO1_00000008] Requirement: If input signal HMASTER is set to 0 or 1, the FIFO Controller shall enter Memory mode.
```

### REVIEW-0250

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:77

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:77
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 015 \(page 121\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ca_stredl_bist_c_sif_reg_e n input BIST Enable for various types of data transfer (Bitmap, memory selection, programma ble algorithms) through serial interface.
```

### REVIEW-0251

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:78

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:78
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 015 \(page 121\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ca_stredl_bist_c_sif_reg_e n input BIST Enable for various types of data transfer (Bitmap, memory selection, programma ble algorithms) through serial interface.
```

### REVIEW-0252

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:79

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:79
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 008 \(page 127\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ca_stredl_bist_c_tst_gated clock input BIST Clock Gating Signal for the entire BIST.
```

### REVIEW-0253

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:80

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:80
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 008 \(page 127\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ca_stredl_bist_c_tst_gated clock input BIST Clock Gating Signal for the entire BIST.
```

### REVIEW-0254

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:81

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:81
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 014 \(page 127\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Used to force clock gating cell transparenc y in ATPG mode .
```

### REVIEW-0255

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:82

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:82
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 014 \(page 127\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Used to force clock gating cell transparenc y in ATPG mode .
```

### REVIEW-0256

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:83

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:83
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 029 \(page 127\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
allows to force reset synchronizin g circuit transparenc y in ATPG mode.
```

### REVIEW-0257

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:84

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:84
- Section 13\.3 ISPU integration \(under Section 13 Modules\), paragraph 029 \(page 127\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
allows to force reset synchronizin g circuit transparenc y in ATPG mode.
```

### REVIEW-0258

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:85

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:85
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 059 \(page 133\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The device is configurable/readable by the I2C/AHB bridge. This IP is in charge of take an I2C/SPI access and (eventually) transform it into an AHB transaction, to allow the configuration/reading of the device using the ISPU.
```

### REVIEW-0259

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:86

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:86
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 009 \(page 133\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The AFE_BLOCK registers are accessible by I2C/SPI direct access and AHB interface, while the others are only by AHB.
```

### REVIEW-0260

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:87

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:87
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 011 \(page 133\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers.
```

### REVIEW-0261

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:88

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:88
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 025 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
To enable AHB Access, it needs using I2C/SPI direct access mode, for: • First turn-on the LDO1V8 and the Fast-Ring Oscillator (set EN_LDO1V8 and EN_CLKF of VIREF_LDO1V8_CLK16M, see address in the Table 34).
```

### REVIEW-0262

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:89

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:89
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 031 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
ow it's possible to configure the registers that are mapped on AHB_Interface as explained in the following example: • Run an I2C/SPI transaction, with the type of AHB access word/byte, at the address 0x59 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0263

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:90

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:90
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 035 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI transaction, with the register address that you want to configure, at the address 0x50 (one of I2C/SPI Internal Configuration Registers), starting from the LSB. In other word, if you need to access at register VIREF_LDO1V8_CLK16M at AHB address
```

### REVIEW-0264

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:91

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:91
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 036 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In other word, if you need to access at register VIREF_LDO1V8_CLK16M at AHB address 0x000C_00CF, you have to perform four I2C/SPI accesses to write: o At address 0x50 0xCF o At address 0x51 0x00 o At address 0x52 0x0C o At address 0x53 → 0x00 • Run an I2C/SPI write, of the new data, at address 0x60 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0265

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:92

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:92
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address \(under Section 13\.4\.1 STBIO1 Register Map\), paragraph 046 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI read transition, with the number of byte that you read, at address 0x68 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0266

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:93

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:93
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 003 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The only registers that are accessible also by an I2C/SPI direct access, are the ones of the AFE BLOCK section.
```

### REVIEW-0267

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:94

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:94
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 006 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers (Table 24).
```

### REVIEW-0268

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:95

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:95
- Section 13\.4\.1 STBIO1 Register Map \(under Section 13\.4 STBIO1 Register Map\), paragraph 005 \(page 134\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
To reach a very Low-Power consumption, the AHB interface is disabled as default.
```

### REVIEW-0269

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:96

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:96
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 003 \(page 135\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI transaction with the data that you want to read, at address loaded into the previous step, at the address 0x70 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0270

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:97

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:97
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 003 \(page 135\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Run an I2C/SPI transaction with the data that you want to read, at address loaded into the previous step, at the address 0x70 (one of I2C/SPI Internal Configuration Registers).
```

### REVIEW-0271

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:98

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:98
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 006 \(page 135\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It's possible remap the whole AFE register map with AHB addresses column “AHB Start Address” of Table 34), included the AFE_BLOCK block: in this case each registers is accessible with own AHB address (AHB start address + offset) and the I2C/SPI access to these registers must follow the previous procedure.
```

### REVIEW-0272

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:99

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:99
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 006 \(page 135\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It's possible remap the whole AFE register map with AHB addresses column “AHB Start Address” of Table 34), included the AFE_BLOCK block: in this case each registers is accessible with own AHB address (AHB start address + offset) and the I2C/SPI access to these registers must follow the previous procedure.
```

### REVIEW-0273

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:100

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:100
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 012 \(page 135\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This procedure is useful when you are thinking of configuring the STBIO1 by ISPU (with a code previously charged in code memory), leaving to host interface (I2C/SPI) the rule to collect the data from FIFO after AFE sampling and processing phases.
```

### REVIEW-0274

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** named block text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:101

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:101
- Section 2 AFE\_BLOCK register R/W \-\> Read/Write the AFE\_BLOCK register with the address, paragraph 012 \(page 135\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This procedure is useful when you are thinking of configuring the STBIO1 by ISPU (with a code previously charged in code memory), leaving to host interface (I2C/SPI) the rule to collect the data from FIFO after AFE sampling and processing phases.
```

### REVIEW-0275

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:102

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:102
- Section 15\.2 Configuration Phase \(under Section 15 Measurement Cycle Examples\), paragraph 005 \(page 147\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The start and the end of a Measurement Cycle is selected by the writing of the dedicated register as described in following examples.
```

### REVIEW-0276

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:103

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:103
- Section 15\.2 Configuration Phase \(under Section 15 Measurement Cycle Examples\), paragraph 005 \(page 147\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The start and the end of a Measurement Cycle is selected by the writing of the dedicated register as described in following examples.
```

### REVIEW-0277

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:104

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:104
- Section 15\.3\.1 ECG Only \(under Section 15\.3 Measurement Cycle\), paragraph 004 \(page 148\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively.
```

### REVIEW-0278

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:105

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:105
- Section 15\.3\.1 ECG Only \(under Section 15\.3 Measurement Cycle\), paragraph 004 \(page 148\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively.
```

### REVIEW-0279

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:106

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:106
- Section 15\.3\.2 ECG and BIA \(under Section 15\.3 Measurement Cycle\), paragraph 007 \(page 150\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively and four averaged BIA data which are BIA_AC_P, BIA_DC_P, BIA_AC_Q and BIA_DC_Q.
```

### REVIEW-0280

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:107

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:107
- Section 15\.3\.2 ECG and BIA \(under Section 15\.3 Measurement Cycle\), paragraph 007 \(page 150\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively and four averaged BIA data which are BIA_AC_P, BIA_DC_P, BIA_AC_Q and BIA_DC_Q.
```

### REVIEW-0281

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:108

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:108
- Section 15\.3\.3 PPG Only \(under Section 15\.3 Measurement Cycle\), paragraph 006 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
This configuration generates each time slot, a number of PPG DATA according to user configuration.
```

### REVIEW-0282

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:109

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:109
- Section 15\.3\.3 PPG Only \(under Section 15\.3 Measurement Cycle\), paragraph 006 \(page 152\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
This configuration generates each time slot, a number of PPG DATA according to user configuration.
```

### REVIEW-0283

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:110

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:110
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 047 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
All user BIST control is done through the controller.
```

### REVIEW-0284

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:111

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:111
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 047 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
All user BIST control is done through the controller.
```

### REVIEW-0285

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:112

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:112
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 048 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
through the controller. The controller controls various testing and reporting activities of the memory test. It allows various mode selections and programs the pre-stored synthesized
```

### REVIEW-0286

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:113

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:113
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 049 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It allows various mode selections and programs the pre-stored synthesized algorithms instructions into collars attached to it.
```

### REVIEW-0287

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_candidate\_only

**Spiegazione:** candidate retained; not rendered in this overview

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:114

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:114
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 049 \(page 157\)

**audit_decision:** candidate\_only

**Estratto sorgente:**

```text
It allows various mode selections and programs the pre-stored synthesized algorithms instructions into collars attached to it.
```

### REVIEW-0288

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:115

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:115
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 059 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It includes a TAP controller, a 7-bit instruction register, three test data registers, and the bypass register.
```

### REVIEW-0289

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:116

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:116
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 059 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
It includes a TAP controller, a 7-bit instruction register, three test data registers, and the bypass register.
```

### REVIEW-0290

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:117

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:117
- Section 17\.2 Memory BIST Architecture \(under Section 17 BIST\), paragraph 037 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The BIST solution consists of memory-wrapper “collar” and common master “controller” and an IEEE 1149.1 compliant Test Access Port (TAP).
```

### REVIEW-0291

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:118

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:118
- Section 17\.2 Memory BIST Architecture \(under Section 17 BIST\), paragraph 037 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
The BIST solution consists of memory-wrapper “collar” and common master “controller” and an IEEE 1149.1 compliant Test Access Port (TAP).
```

### REVIEW-0292

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:119

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:119
- Section 17\.2\.1 MBIST Collar \(under Section 17\.2 Memory BIST Architecture\), paragraph 043 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
After testing it reports the execution status to the controller and manages all the BIST status, diagnosis, repair information and debug data. The collar also provides support for testing multiple
```

### REVIEW-0293

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:120

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:120
- Section 17\.2\.1 MBIST Collar \(under Section 17\.2 Memory BIST Architecture\), paragraph 043 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
After testing it reports the execution status to the controller and manages all the BIST status, diagnosis, repair information and debug data. The collar also provides support for testing multiple
```

### REVIEW-0294

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:121

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:121
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 052 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Main functionalities of controller are: • Mode management (RunBIST mode, Retention mode etc.)
```

### REVIEW-0295

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:122

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:122
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 052 \(page 157\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Main functionalities of controller are: • Mode management (RunBIST mode, Retention mode etc.)
```

### REVIEW-0296

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:123

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:123
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 005 \(page 158\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
In this configuration, there is only one controller for the entire chip. All associated collars are
```

### REVIEW-0297

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:124

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:124
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 010 \(page 158\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Bend: Indicates that all the activities of the test run of all Memories in the current BIST mode are complete • Bfail: Indicates bfail for a specific memory.
```

### REVIEW-0298

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:125

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:125
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 010 \(page 158\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Bend: Indicates that all the activities of the test run of all Memories in the current BIST mode are complete • Bfail: Indicates bfail for a specific memory.
```

### REVIEW-0299

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: no supported functional construction

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:126

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:126
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 017 \(page 158\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Tdo:TAP serial output Updated on falling edge of tck INPUT FROM PAD • Tck: TAP clock • Tdi: TAP serial input Sampled on rising edge of tck • Tms: TAP test mode select Sampled on rising edge of tck • Trstn: TAP reset INPUT FROM REGISTER • Memsafe (ADDRESS=0x3E, BIT=0x05): to globally deactivate the memory by making CSN high internally • Mem_atpg_mode (ADDRESS=0x3E, BIT=0x06): Used to constraint few memory inputs and improve controllability and observability.
```

### REVIEW-0300

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** raw/implementation text not eligible for direct narrative

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:127

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:127
- Section 17\.2\.3 Top Level Approach \(under Section 17\.2 Memory BIST Architecture\), paragraph 017 \(page 158\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Tdo:TAP serial output Updated on falling edge of tck INPUT FROM PAD • Tck: TAP clock • Tdi: TAP serial input Sampled on rising edge of tck • Tms: TAP test mode select Sampled on rising edge of tck • Trstn: TAP reset INPUT FROM REGISTER • Memsafe (ADDRESS=0x3E, BIT=0x05): to globally deactivate the memory by making CSN high internally • Mem_atpg_mode (ADDRESS=0x3E, BIT=0x06): Used to constraint few memory inputs and improve controllability and observability.
```

### REVIEW-0301

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:128

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:128
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 010 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_302] Requirement If MODE_CONFIG register is 0x00 the operative mode shall be functional.
```

### REVIEW-0302

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:129

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:129
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 014 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_303] Requirement If MODE_CONFIG register is 0x01 the operative mode shall be SCAN.
```

### REVIEW-0303

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:130

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:130
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 018 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_304] Requirement If MODE_CONFIG register is 0x04 the operative mode shall be BIST.
```

### REVIEW-0304

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:131

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:131
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 022 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_305] Requirement If MODE_CONFIG register is 0x08 the operative mode shall be DEBUG.
```

### REVIEW-0305

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:132

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:132
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 026 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_306] Requirement If MODE_CONFIG register is 0x10 the operative mode shall be ISPU_DEBUG.
```

### REVIEW-0306

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:133

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:133
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 030 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_307] Requirement If MODE_CONFIG register is 0x20 the operative mode shall be Bist MEMSAFE mode.
```

### REVIEW-0307

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** not a provenanced system/architecture descriptive record

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:134

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:134
- Section 13\.1\.2\.2 Requirements \(under Section 13\.1\.2 PAD Mux\), paragraph 034 \(page 59\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
[DDS_STBIO1_308] Requirement If MODE_CONFIG register is 0x40 the operative mode shall be Bist Bypass mode.
```

### REVIEW-0308

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: power qualifier requires explicit projection

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:167

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:167
- Stage 1 OCR power\-domain table/description \(PD\_TOP1V2\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOP1V2: Included block(s): ADSP,, multi_channel_fifo, i2c_spi_slave, main_controller_top, senshub_mst_i2c, pad_mux, pmu, stbio1_regmap, scan_out_mux, xbar_afe. Domain type: Always-On. Control mode: HW. Notes: Always active. • Function: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only). • Characteristics: Never powered down. • Control: Managed by hardware.
```

### REVIEW-0309

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** projection\_gap\: power qualifier requires explicit projection

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:168

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_system\_overview\_audit\.csv\:data\-record\:168
- Stage 1 OCR power\-domain table/description \(PD\_TOP1V2\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOP1V2: Included block(s): ADSP,, multi_channel_fifo, i2c_spi_slave, main_controller_top, senshub_mst_i2c, pad_mux, pmu, stbio1_regmap, scan_out_mux, xbar_afe. Domain type: Always-On. Control mode: HW. Notes: Always active. • Function: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only). • Characteristics: Never powered down. • Control: Managed by hardware.
```

### REVIEW-0310

**Documento:** SRS

**Posizione:** 0\.1 Table of contents \{\#01\-table\-of\-contents\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:1

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:85

**Estratto sorgente:**

```text
- [Assumptions and TBD](#assumptions-and-tbd)
```

### REVIEW-0311

**Documento:** SRS

**Posizione:** 3\.4 External Interfaces and System Boundaries \{\#34\-external\-interfaces\-and\-system\-boundaries\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:2

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:395

**Estratto sorgente:**

```text
The interfaces provide sensing input, measurement data exchange, serial communication, interrupt reporting and power supply roles. External versus internal placement is not specified for every interface.
```


**Contenuto supportato mantenuto:**

```text
The interfaces provide sensing input, measurement data exchange, serial communication, interrupt reporting and power supply roles.
```

### REVIEW-0312

**Documento:** SRS

**Posizione:** 3\.6 Power, Clock, and Reset Overview \{\#36\-power\-clock\-and\-reset\-overview\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:3

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:427

**Estratto sorgente:**

```text
State retention across system power transitions is not specified.
```

### REVIEW-0313

**Documento:** SRS

**Posizione:** 3\.6 Power, Clock, and Reset Overview \{\#36\-power\-clock\-and\-reset\-overview\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:4

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:439

**Estratto sorgente:**

```text
  - Top-level clock and reset coordination are not specified.
```

### REVIEW-0314

**Documento:** SRS

**Posizione:** 3\.7 Assumptions, Scope Limits, and Allocation Boundaries \{\#37\-assumptions\-scope\-limits\-and\-allocation\-boundaries\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:5

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:446

**Estratto sorgente:**

```text
  - Additional system-level assumptions are not described in the available descriptions.
```

### REVIEW-0315

**Documento:** SRS

**Posizione:** Assumptions \{\#assumptions\-and\-tbd\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:6

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:601

**Estratto sorgente:**

```text
## Assumptions and TBD {#assumptions-and-tbd}
```


**Contenuto supportato mantenuto:**

```text
## Assumptions {#assumptions}
```

### REVIEW-0316

**Documento:** SRS

**Posizione:** Assumptions \{\#assumptions\-and\-tbd\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:7

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:604

**Estratto sorgente:**

```text
- TBD-001: Unassigned requirements in traceability matrix need architectural owner review.
```

### REVIEW-0317

**Documento:** SRS

**Posizione:** 10\.1 Descriptive content review findings \{\#101\-descriptive\-content\-review\-findings\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:8

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:612

**Estratto sorgente:**

```text
- SRS_CATALOG_CLASSIFICATION_MISSING: IRQ logic
```

### REVIEW-0318

**Documento:** SRS

**Posizione:** 10\.1 Descriptive content review findings \{\#101\-descriptive\-content\-review\-findings\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:9

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:613

**Estratto sorgente:**

```text
- SRS_CATALOG_CLASSIFICATION_MISSING: BIST Controller
```

### REVIEW-0319

**Documento:** SRS

**Posizione:** 10\.1 Descriptive content review findings \{\#101\-descriptive\-content\-review\-findings\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:10

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:614

**Estratto sorgente:**

```text
- SRS_CATALOG_CLASSIFICATION_CONFLICT: PAD MUX
```

### REVIEW-0320

**Documento:** SRS

**Posizione:** 10\.1 Descriptive content review findings \{\#101\-descriptive\-content\-review\-findings\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:11

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:615

**Estratto sorgente:**

```text
- SRS_CATALOG_APPROVAL_MISSING: ISPU
```

### REVIEW-0321

**Documento:** SRS

**Posizione:** 10\.1 Descriptive content review findings \{\#101\-descriptive\-content\-review\-findings\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:12

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:616

**Estratto sorgente:**

```text
- SRS_POWER_VOLTAGE_UNRELIABLE: Stage 1 OCR power-domain table/description (PD_TOP3V3): 3A
```

### REVIEW-0322

**Documento:** SRS

**Posizione:** 10\.1 Descriptive content review findings \{\#101\-descriptive\-content\-review\-findings\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json\:omissions\:13

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_publication\_audit\.json
- system\_requirements\_specification\.md\:renderer\-input\-line\:617

**Estratto sorgente:**

```text
- SRS_POWER_NOTE_UNREADABLE: Stage 1 OCR power-domain table/description (PD_TOPIO): Always active 32 10.4
```

### REVIEW-0323

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json

**Classe del blocco:** descriptive\_review\_finding

**Spiegazione:** SRS\_CATALOG\_CLASSIFICATION\_MISSING\: IRQ logic

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- review\_findings\:1

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json
### REVIEW-0324

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json

**Classe del blocco:** descriptive\_review\_finding

**Spiegazione:** SRS\_CATALOG\_CLASSIFICATION\_MISSING\: BIST Controller

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- review\_findings\:2

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json
### REVIEW-0325

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json

**Classe del blocco:** descriptive\_review\_finding

**Spiegazione:** SRS\_CATALOG\_CLASSIFICATION\_CONFLICT\: PAD MUX

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- review\_findings\:3

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json
### REVIEW-0326

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json

**Classe del blocco:** descriptive\_review\_finding

**Spiegazione:** SRS\_CATALOG\_APPROVAL\_MISSING\: ISPU

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- review\_findings\:4

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json
### REVIEW-0327

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json

**Classe del blocco:** descriptive\_review\_finding

**Spiegazione:** SRS\_POWER\_VOLTAGE\_UNRELIABLE\: Stage 1 OCR power\-domain table/description \(PD\_TOP3V3\)\: 3A

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- review\_findings\:5

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json
### REVIEW-0328

**Documento:** SRS

**Posizione:** artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json

**Classe del blocco:** descriptive\_review\_finding

**Spiegazione:** SRS\_POWER\_NOTE\_UNREADABLE\: Stage 1 OCR power\-domain table/description \(PD\_TOPIO\)\: Always active 32 10\.4

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- review\_findings\:6

**Riferimenti sorgente:**

- artifacts/stage3\_srs/descriptive\_srs\_content\_audit\.json

## ARS

### REVIEW-0329

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:1

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:1
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0330

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:2

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:2
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0331

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:3

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:3
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0332

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:4

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:4
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0333

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:5

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:5
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0334

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:6

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:6
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0335

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:7

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:7
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0336

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:8

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:8
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0337

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:9

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:9
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0338

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:10

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:10
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0339

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:11

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:11
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0340

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:12

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:12
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 020 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 020 (page 34)
```

### REVIEW-0341

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:13

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:13
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0342

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:14

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:14
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0343

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:15

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:15
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0344

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:16

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:16
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0345

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:17

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:17
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0346

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:18

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:18
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0347

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:19

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:19
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0348

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:20

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:20
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0349

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:21

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:21
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0350

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:22

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:22
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 007 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 007 (page 130)
```

### REVIEW-0351

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:23

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:23
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 008 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 008 (page 130)
```

### REVIEW-0352

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:24

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:24
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 009 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 009 (page 130)
```

### REVIEW-0353

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:25

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:25
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 011 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 011 (page 130)
```

### REVIEW-0354

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:26

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:26
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 013 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 013 (page 130)
```

### REVIEW-0355

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:27

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:27
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 023 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 023 (page 131)
```

### REVIEW-0356

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:28

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:28
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 027 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 027 (page 131)
```

### REVIEW-0357

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:29

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:29
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 031 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 031 (page 131)
```

### REVIEW-0358

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:30

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:30
- Section 1 TIME SLOT LENGTH\: \(under Section 15\.3\.3 PPG Only\), paragraph 010 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 1 TIME SLOT LENGTH: (under Section 15.3.3 PPG Only), paragraph 010 (page 152)
```

### REVIEW-0359

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:31

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:31
- Section 3 SELECT DIVISION INDEX FOR CONFIGURED CHANNELS\: \(under Section 15\.3\.3 PPG Only\), paragraph 018 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 3 SELECT DIVISION INDEX FOR CONFIGURED CHANNELS: (under Section 15.3.3 PPG Only), paragraph 018 (page 152)
```

### REVIEW-0360

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:32

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:32
- Section 4 CONFIGURE ADC SAMPLING PERIOD\: \(under Section 15\.3\.3 PPG Only\), paragraph 022 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 4 CONFIGURE ADC SAMPLING PERIOD: (under Section 15.3.3 PPG Only), paragraph 022 (page 152)
```

### REVIEW-0361

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:33

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:33
- Section 2 SELECT CHANNEL\: \(under Section 15\.3\.3 PPG Only\), paragraph 014 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 2 SELECT CHANNEL: (under Section 15.3.3 PPG Only), paragraph 014 (page 152)
```

### REVIEW-0362

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:34

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:34
- Section 5 PPG FRAMES CONFIG\: \(under Section 15\.3\.3 PPG Only\), paragraph 026 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 5 PPG FRAMES CONFIG: (under Section 15.3.3 PPG Only), paragraph 026 (page 152)
```

### REVIEW-0363

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:35

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:35
- Section 6 SELECT OPERATIVE MODE\: \(under Section 15\.3\.3 PPG Only\), paragraph 008 \(page 153\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 6 SELECT OPERATIVE MODE: (under Section 15.3.3 PPG Only), paragraph 008 (page 153)
```

### REVIEW-0364

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:36

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:36
- Section 7 CHECK DATA\: \(under Section 15\.3\.3 PPG Only\), paragraph 011 \(page 153\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 7 CHECK DATA: (under Section 15.3.3 PPG Only), paragraph 011 (page 153)
```

### REVIEW-0365

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:37

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:37
- Section 18\.1 Scan mode \(under Section 18 Digital DFT\), paragraph 011 \(page 159\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.1 Scan mode (under Section 18 Digital DFT), paragraph 011 (page 159)
```

### REVIEW-0366

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:38

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:38
- Section 18\.2 Debug mode \(under Section 18 Digital DFT\), paragraph 024 \(page 159\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.2 Debug mode (under Section 18 Digital DFT), paragraph 024 (page 159)
```

### REVIEW-0367

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:39

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:39
- Section 18\.3 ADC TEST LOW NOISE \(under Section 18 Digital DFT\), paragraph 006 \(page 160\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 006 (page 160)
```

### REVIEW-0368

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:40

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:40
- Section 18\.3 ADC TEST LOW NOISE \(under Section 18 Digital DFT\), paragraph 023 \(page 160\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 023 (page 160)
```

### REVIEW-0369

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:41

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:41
- Section 18\.4 ADC TEST FAST \(under Section 18 Digital DFT\), paragraph 010 \(page 161\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.4 ADC TEST FAST (under Section 18 Digital DFT), paragraph 010 (page 161)
```

### REVIEW-0370

**Documento:** ARS

**Posizione:** artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:42

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_low\_power\_audit\.csv\:data\-record\:42
- Section 18\.5 BIST MODE \(under Section 18 Digital DFT\), paragraph 030 \(page 161\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.5 BIST MODE (under Section 18 Digital DFT), paragraph 030 (page 161)
```

### REVIEW-0371

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:2

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:2
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0372

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:3

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:3
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0373

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:5

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:5
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0374

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:6

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:6
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0375

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:8

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:8
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0376

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:9

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:9
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0377

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:10

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:10
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0378

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:11

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:11
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0379

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:14

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:14
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0380

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:15

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:15
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0381

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:16

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:16
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0382

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:18

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:18
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0383

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:19

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:19
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0384

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:20

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:20
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0385

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:21

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:21
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0386

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:22

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:22
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 007 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 007 (page 130)
```

### REVIEW-0387

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:23

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:23
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 008 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 008 (page 130)
```

### REVIEW-0388

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:24

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:24
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 009 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 009 (page 130)
```

### REVIEW-0389

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:25

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:25
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 011 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 011 (page 130)
```

### REVIEW-0390

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:26

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:26
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 013 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 013 (page 130)
```

### REVIEW-0391

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:27

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:27
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 023 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 023 (page 131)
```

### REVIEW-0392

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:28

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:28
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 027 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 027 (page 131)
```

### REVIEW-0393

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:29

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:29
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 031 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 031 (page 131)
```

### REVIEW-0394

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:36

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:36
- Section 7 CHECK DATA\: \(under Section 15\.3\.3 PPG Only\), paragraph 011 \(page 153\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 7 CHECK DATA: (under Section 15.3.3 PPG Only), paragraph 011 (page 153)
```

### REVIEW-0395

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:37

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:37
- Section 18\.1 Scan mode \(under Section 18 Digital DFT\), paragraph 011 \(page 159\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.1 Scan mode (under Section 18 Digital DFT), paragraph 011 (page 159)
```

### REVIEW-0396

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:38

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:38
- Section 18\.2 Debug mode \(under Section 18 Digital DFT\), paragraph 024 \(page 159\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.2 Debug mode (under Section 18 Digital DFT), paragraph 024 (page 159)
```

### REVIEW-0397

**Documento:** ARS

**Posizione:** Analog Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:42

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_summary\_audit\.csv\:data\-record\:42
- Section 18\.5 BIST MODE \(under Section 18 Digital DFT\), paragraph 030 \(page 161\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.5 BIST MODE (under Section 18 Digital DFT), paragraph 030 (page 161)
```

### REVIEW-0398

**Documento:** ARS

**Posizione:** 0\.1 Table of contents \{\#01\-table\-of\-contents\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_publication\_audit\.json\:omissions\:1

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_publication\_audit\.json
- analog\_requirements\_specification\.md\:renderer\-input\-line\:76

**Estratto sorgente:**

```text
- [8. Assumptions and TBD](#8-assumptions-and-tbd)
```


**Contenuto supportato mantenuto:**

```text
- [8.
```

### REVIEW-0399

**Documento:** ARS

**Posizione:** Table 3\. Section navigation index \{\#table\-3\-section\-navigation\-index\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_publication\_audit\.json\:omissions\:2

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_publication\_audit\.json
- analog\_requirements\_specification\.md\:renderer\-input\-line\:136

**Estratto sorgente:**

```text
| 8. Assumptions and TBD | 8 | [Jump](#8-assumptions-and-tbd) | Auto |
```


**Contenuto supportato mantenuto:**

```text
| 8. Assumptions | 8 |  | Auto |
```

### REVIEW-0400

**Documento:** ARS

**Posizione:** 8\. Assumptions \{\#8\-assumptions\-and\-tbd\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_publication\_audit\.json\:omissions\:3

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_publication\_audit\.json
- analog\_requirements\_specification\.md\:renderer\-input\-line\:402

**Estratto sorgente:**

```text
## 8. Assumptions and TBD {#8-assumptions-and-tbd}
```


**Contenuto supportato mantenuto:**

```text
## 8. Assumptions {#8-assumptions}
```

### REVIEW-0401

**Documento:** ARS

**Posizione:** 8\. Assumptions \{\#8\-assumptions\-and\-tbd\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage4\_ars/descriptive\_publication\_audit\.json\:omissions\:4

**Riferimenti sorgente:**

- artifacts/stage4\_ars/descriptive\_publication\_audit\.json
- analog\_requirements\_specification\.md\:renderer\-input\-line\:405

**Estratto sorgente:**

```text
- TBD-001: Unassigned requirements in ARS traceability matrix require architectural owner review.
```


## DRS

### REVIEW-0402

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:5

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:5
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ADC -> Main Controller (digital samples; sample cycle; digital pipeline input)
```

### REVIEW-0403

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:6

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:6
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Main Controller -> Smart FIFO (sample stream and FIFO mode control; FIFO enabled; stream/bypass/fifo mode routing)
```

### REVIEW-0404

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:7

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:7
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Smart FIFO -> IRQ logic (watermark/overrun/empty flags; FIFO status change; interrupt condition generation)
```

### REVIEW-0405

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:8

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:8
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Regmap -> Main Controller (configuration writes; register update; sample-rate/filter/mode setup)
```

### REVIEW-0406

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:9

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:9
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: SPI interface -> Regmap (SPI register transactions; host SPI access; SPI path to register map)
```

### REVIEW-0407

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:10

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:10
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C interface -> Regmap (I2C register transactions; host I2C access; I2C path to register map)
```

### REVIEW-0408

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:11

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:11
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Regmap -> SPI interface (register read response; SPI read; response serialization on SPI)
```

### REVIEW-0409

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:12

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:12
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Regmap -> I2C interface (register read response; I2C read; response serialization on I2C)
```

### REVIEW-0410

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:14

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:14
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: BIST Controller -> Regmap (self-test/calibration status; self-test command; status publication through registers)
```

### REVIEW-0411

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:15

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:15
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> SPI interface (SPI host transactions; SPI bus session; host boundary ingress)
```

### REVIEW-0412

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:16

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:16
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> I2C interface (I2C host transactions; I2C bus session; host boundary ingress)
```

### REVIEW-0413

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:17

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:17
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Main Controller -> Regmap (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0414

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:18

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:18
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Main Controller -> FIFO (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0415

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:19

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:19
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Main Controller -> ADSP (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0416

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:20

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:20
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ADSP -> Regmap (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0417

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:21

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:21
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ADSP -> SENSOR HUB (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0418

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:22

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:22
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ADSP -> FIFO (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0419

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:23

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:23
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> Regmap (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0420

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:24

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:24
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> SENSOR HUB (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0421

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:25

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:25
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> ISPU (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0422

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:26

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:26
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> FIFO (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0423

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:27

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:27
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> ADSP (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0424

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:28

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:28
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: SENSOR HUB -> FIFO (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0425

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:29

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:29
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU -> Regmap (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0426

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:30

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:30
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU -> SENSOR HUB (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0427

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:31

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:31
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU -> FIFO (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0428

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:32

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:32
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU -> ADSP (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0429

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:33

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:33
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU debug -> Regmap (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0430

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:34

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:34
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU debug -> SENSOR HUB (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0431

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:35

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:35
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU debug -> ISPU (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0432

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:36

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:36
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU debug -> FIFO (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0433

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:37

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:37
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU debug -> ADSP (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0434

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:38

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:38
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface SENSOR_ANALOG_INPUT owned by Sensor-Hub: Raw sensor-domain analog input
```

### REVIEW-0435

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:39

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:39
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface ADC_DATA owned by ADC: Digitized samples
```

### REVIEW-0436

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:40

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:40
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface FIFO_DATA owned by Smart FIFO: Buffered output samples
```

### REVIEW-0437

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:41

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:41
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface SERIAL_CLK owned by SPI interface: Serial clock input
```

### REVIEW-0438

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:42

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:42
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface SERIAL_SELECT owned by SPI interface: Serial frame/select input
```

### REVIEW-0439

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:43

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:43
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface SERIAL_DATA_IN owned by SPI interface: Serial data input
```

### REVIEW-0440

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:44

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:44
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface SERIAL_DATA_OUT owned by SPI interface: Serial data output
```

### REVIEW-0441

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:45

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:45
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface ALT_SERIAL_CLK owned by I2C interface: Alternate serial clock input
```

### REVIEW-0442

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:46

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:46
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface ALT_SERIAL_DATA owned by I2C interface: Alternate serial bidirectional data line
```

### REVIEW-0443

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:47

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:47
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface INT1 owned by IRQ logic: Primary interrupt output
```

### REVIEW-0444

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:48

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:48
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface INT2 owned by IRQ logic: Secondary interrupt output
```

### REVIEW-0445

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:51

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:51
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0446

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:52

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:52
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0447

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:53

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:53
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0448

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:54

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:54
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0449

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:55

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:55
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0450

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:56

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:56
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0451

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:57

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:57
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0452

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:58

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:58
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0453

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:59

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:59
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0454

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:60

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:60
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0455

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:61

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:61
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0456

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:62

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:62
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 020 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 020 (page 34)
```

### REVIEW-0457

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:63

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:63
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0458

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:64

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:64
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0459

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:65

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:65
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0460

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:66

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:66
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0461

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:67

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:67
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0462

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:68

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:68
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0463

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:69

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:69
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0464

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:70

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:70
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0465

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:71

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:71
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0466

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:72

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:72
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 007 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 007 (page 130)
```

### REVIEW-0467

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:73

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:73
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 008 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 008 (page 130)
```

### REVIEW-0468

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:74

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:74
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 009 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 009 (page 130)
```

### REVIEW-0469

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:75

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:75
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 011 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 011 (page 130)
```

### REVIEW-0470

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:76

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:76
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 013 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 013 (page 130)
```

### REVIEW-0471

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:77

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:77
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 023 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 023 (page 131)
```

### REVIEW-0472

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:78

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:78
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 027 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 027 (page 131)
```

### REVIEW-0473

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:79

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:79
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 031 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 031 (page 131)
```

### REVIEW-0474

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:80

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:80
- Section 1 TIME SLOT LENGTH\: \(under Section 15\.3\.3 PPG Only\), paragraph 010 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 1 TIME SLOT LENGTH: (under Section 15.3.3 PPG Only), paragraph 010 (page 152)
```

### REVIEW-0475

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:81

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:81
- Section 3 SELECT DIVISION INDEX FOR CONFIGURED CHANNELS\: \(under Section 15\.3\.3 PPG Only\), paragraph 018 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 3 SELECT DIVISION INDEX FOR CONFIGURED CHANNELS: (under Section 15.3.3 PPG Only), paragraph 018 (page 152)
```

### REVIEW-0476

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:82

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:82
- Section 4 CONFIGURE ADC SAMPLING PERIOD\: \(under Section 15\.3\.3 PPG Only\), paragraph 022 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 4 CONFIGURE ADC SAMPLING PERIOD: (under Section 15.3.3 PPG Only), paragraph 022 (page 152)
```

### REVIEW-0477

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:83

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:83
- Section 2 SELECT CHANNEL\: \(under Section 15\.3\.3 PPG Only\), paragraph 014 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 2 SELECT CHANNEL: (under Section 15.3.3 PPG Only), paragraph 014 (page 152)
```

### REVIEW-0478

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:84

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:84
- Section 5 PPG FRAMES CONFIG\: \(under Section 15\.3\.3 PPG Only\), paragraph 026 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 5 PPG FRAMES CONFIG: (under Section 15.3.3 PPG Only), paragraph 026 (page 152)
```

### REVIEW-0479

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:85

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:85
- Section 6 SELECT OPERATIVE MODE\: \(under Section 15\.3\.3 PPG Only\), paragraph 008 \(page 153\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 6 SELECT OPERATIVE MODE: (under Section 15.3.3 PPG Only), paragraph 008 (page 153)
```

### REVIEW-0480

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:86

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:86
- Section 7 CHECK DATA\: \(under Section 15\.3\.3 PPG Only\), paragraph 011 \(page 153\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 7 CHECK DATA: (under Section 15.3.3 PPG Only), paragraph 011 (page 153)
```

### REVIEW-0481

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:87

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:87
- Section 18\.1 Scan mode \(under Section 18 Digital DFT\), paragraph 011 \(page 159\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.1 Scan mode (under Section 18 Digital DFT), paragraph 011 (page 159)
```

### REVIEW-0482

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:88

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:88
- Section 18\.2 Debug mode \(under Section 18 Digital DFT\), paragraph 024 \(page 159\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.2 Debug mode (under Section 18 Digital DFT), paragraph 024 (page 159)
```

### REVIEW-0483

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:89

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:89
- Section 18\.3 ADC TEST LOW NOISE \(under Section 18 Digital DFT\), paragraph 006 \(page 160\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 006 (page 160)
```

### REVIEW-0484

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:90

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:90
- Section 18\.3 ADC TEST LOW NOISE \(under Section 18 Digital DFT\), paragraph 023 \(page 160\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 023 (page 160)
```

### REVIEW-0485

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:91

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:91
- Section 18\.4 ADC TEST FAST \(under Section 18 Digital DFT\), paragraph 010 \(page 161\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.4 ADC TEST FAST (under Section 18 Digital DFT), paragraph 010 (page 161)
```

### REVIEW-0486

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:92

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:92
- Section 18\.5 BIST MODE \(under Section 18 Digital DFT\), paragraph 030 \(page 161\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.5 BIST MODE (under Section 18 Digital DFT), paragraph 030 (page 161)
```

### REVIEW-0487

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:93

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:93
- Stage 1 OCR power\-domain table/description \(PD\_TOP1V2\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOP1V2: Included block(s): ADSP,, multi_channel_fifo, i2c_spi_slave, main_controller_top, senshub_mst_i2c, pad_mux, pmu, stbio1_regmap, scan_out_mux, xbar_afe. Domain type: Always-On. Control mode: HW. Notes: Always active. • Function: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only). • Characteristics: Never powered down. • Control: Managed by hardware.
```

### REVIEW-0488

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:94

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:94
- Stage 1 OCR power\-domain table/description \(PD\_STREDL\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_STREDL: Included block(s): STREDL. Domain type: Switchable. Control mode: SW. Notes: Can be powered down in idle. • Function: Powers the STREDL core and associated cache. • Characteristics: Can be powered down when STREDL is not in use. • Control: Managed via software (power management driver)(see 12.3.1)
```

### REVIEW-0489

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:95

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:95
- Stage 1 OCR power\-domain table/description \(PD\_TOP3V3\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOP3V3: Included block(s): H9A_MEM_OTP_ PUMP_85AL05_2. Domain type: Always-On. Voltage: 3A. Control mode: HW. Notes: Always active. • Function: power supply to the OTP memory block. • Characteristics: Never powered down. It provides 4.7V of power supply to the OTP memory block during programming (write) operations • Control: Managed by hardware.
```

### REVIEW-0490

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:96

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:96
- Stage 1 OCR power\-domain table/description \(PD\_TOPIO\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOPIO: Included block(s): level_shifter_sel. Domain type: Always-On. Control mode: HW. Notes: Always active 32 10.4.. • Function: Powers communication PAD • Characteristics: Never powered down. • Control: Managed by hardware.
```

### REVIEW-0491

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:100

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:100
- Section 5 STBIO1 toplevel overview, paragraph 004 \(page 12\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0492

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:101

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:101
- Stage 1 OCR page 12, lines 4\-5

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0493

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:102

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:102
- Stage 1 OCR page 12, lines 38\-40

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main purpose of ADSP is to reduce the computation workload on both ISPU and host processor, while saving power through the optimization of both hardware and algorithm.
```

### REVIEW-0494

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:103

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:103
- Stage 1 OCR page 12, lines 42\-45

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain. The data collected by sensor hub is accessible from the Advanced DSP and ISPU, for sensor fusion algorithm elaboration.
```

### REVIEW-0495

**Documento:** DRS

**Posizione:** artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv

**Classe del blocco:** audit\_rejected

**Spiegazione:** no configured low\-power topic match

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:104

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_low\_power\_audit\.csv\:data\-record\:104
- Stage 1 OCR page 13, lines 17\-18

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor Hub and Elaboration results). The depth of each Sub-FIFO is configurable by regmap. Each Sub-FIFO behavior as a Classic FIFO.
```

### REVIEW-0496

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:18

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:18
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv
- Interaction\: Main Controller \-\> FIFO \(XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source\-derived cell\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Main Controller -> FIFO (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0497

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:19

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:19
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv
- Interaction\: Main Controller \-\> ADSP \(XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source\-derived cell\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: Main Controller -> ADSP (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0498

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:23

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:23
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv
- Interaction\: I2C\_SPI\_AHB \-\> Regmap \(XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source\-derived cell\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> Regmap (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0499

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:24

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:24
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv
- Interaction\: I2C\_SPI\_AHB \-\> SENSOR HUB \(XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source\-derived cell\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> SENSOR HUB (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0500

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:25

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:25
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv
- Interaction\: I2C\_SPI\_AHB \-\> ISPU \(XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source\-derived cell\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> ISPU (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0501

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:26

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:26
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv
- Interaction\: I2C\_SPI\_AHB \-\> FIFO \(XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source\-derived cell\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> FIFO (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0502

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:27

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:27
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv
- Interaction\: I2C\_SPI\_AHB \-\> ADSP \(XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source\-derived cell\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: I2C_SPI_AHB -> ADSP (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0503

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:36

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:36
- artifacts/stage2\_mirco\_arc/interaction\_matrix\.csv
- Interaction\: ISPU debug \-\> FIFO \(XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source\-derived cell\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Interaction: ISPU debug -> FIFO (XBAR connection; XBAR matrix cell; XBAR Connection Matrix; source-derived cell)
```

### REVIEW-0504

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:40

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:40
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface FIFO\_DATA owned by Smart FIFO\: Buffered output samples

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface FIFO_DATA owned by Smart FIFO: Buffered output samples
```

### REVIEW-0505

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:42

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:42
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface SERIAL\_SELECT owned by SPI interface\: Serial frame/select input

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface SERIAL_SELECT owned by SPI interface: Serial frame/select input
```

### REVIEW-0506

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:43

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:43
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface SERIAL\_DATA\_IN owned by SPI interface\: Serial data input

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface SERIAL_DATA_IN owned by SPI interface: Serial data input
```

### REVIEW-0507

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:44

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:44
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface SERIAL\_DATA\_OUT owned by SPI interface\: Serial data output

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface SERIAL_DATA_OUT owned by SPI interface: Serial data output
```

### REVIEW-0508

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:45

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:45
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface ALT\_SERIAL\_CLK owned by I2C interface\: Alternate serial clock input

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface ALT_SERIAL_CLK owned by I2C interface: Alternate serial clock input
```

### REVIEW-0509

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:46

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:46
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface ALT\_SERIAL\_DATA owned by I2C interface\: Alternate serial bidirectional data line

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface ALT_SERIAL_DATA owned by I2C interface: Alternate serial bidirectional data line
```

### REVIEW-0510

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:47

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:47
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface INT1 owned by IRQ logic\: Primary interrupt output

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface INT1 owned by IRQ logic: Primary interrupt output
```

### REVIEW-0511

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:48

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:48
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface INT2 owned by IRQ logic\: Secondary interrupt output

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface INT2 owned by IRQ logic: Secondary interrupt output
```

### REVIEW-0512

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:49

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:49
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface VDD owned by PMU\: Core supply

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface VDD owned by PMU: Core supply
```

### REVIEW-0513

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:50

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:50
- artifacts/stage2\_mirco\_arc/interface\_catalog\.csv
- Approved interface VDD\_IO owned by PMU\: Digital IO supply

**audit_decision:** rejected

**Estratto sorgente:**

```text
Approved interface VDD_IO owned by PMU: Digital IO supply
```

### REVIEW-0514

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:51

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:51
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0515

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:52

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:52
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0516

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:53

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:53
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 017 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
```

### REVIEW-0517

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:54

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:54
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0518

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:55

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:55
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0519

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:56

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:56
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 018 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
```

### REVIEW-0520

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:57

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:57
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0521

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:58

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:58
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0522

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:59

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:59
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0523

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:60

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:60
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0524

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:61

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:61
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 019 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
```

### REVIEW-0525

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:62

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:62
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 020 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 020 (page 34)
```

### REVIEW-0526

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:63

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:63
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0527

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:64

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:64
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0528

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:65

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:65
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0529

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:66

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:66
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 021 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
```

### REVIEW-0530

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:67

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:67
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0531

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:68

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:68
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0532

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:69

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:69
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0533

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:70

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:70
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0534

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:71

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:71
- Section 11\.1 XBAR Connection Matrix \(under Section 11 Interconnect\), paragraph 022 \(page 34\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)
```

### REVIEW-0535

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:72

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:72
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 007 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 007 (page 130)
```

### REVIEW-0536

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:73

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:73
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 008 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 008 (page 130)
```

### REVIEW-0537

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:74

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:74
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 009 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 009 (page 130)
```

### REVIEW-0538

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:75

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:75
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 011 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 011 (page 130)
```

### REVIEW-0539

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:76

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:76
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 013 \(page 130\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 013 (page 130)
```

### REVIEW-0540

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:77

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:77
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 023 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 023 (page 131)
```

### REVIEW-0541

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:78

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:78
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 027 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 027 (page 131)
```

### REVIEW-0542

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:79

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:79
- Section 13\.3\.1 Requirements \(under Section 13\.3 ISPU integration\), paragraph 031 \(page 131\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 031 (page 131)
```

### REVIEW-0543

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:84

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:84
- Section 5 PPG FRAMES CONFIG\: \(under Section 15\.3\.3 PPG Only\), paragraph 026 \(page 152\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 5 PPG FRAMES CONFIG: (under Section 15.3.3 PPG Only), paragraph 026 (page 152)
```

### REVIEW-0544

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:85

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:85
- Section 6 SELECT OPERATIVE MODE\: \(under Section 15\.3\.3 PPG Only\), paragraph 008 \(page 153\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 6 SELECT OPERATIVE MODE: (under Section 15.3.3 PPG Only), paragraph 008 (page 153)
```

### REVIEW-0545

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:86

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:86
- Section 7 CHECK DATA\: \(under Section 15\.3\.3 PPG Only\), paragraph 011 \(page 153\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 7 CHECK DATA: (under Section 15.3.3 PPG Only), paragraph 011 (page 153)
```

### REVIEW-0546

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:87

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:87
- Section 18\.1 Scan mode \(under Section 18 Digital DFT\), paragraph 011 \(page 159\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.1 Scan mode (under Section 18 Digital DFT), paragraph 011 (page 159)
```

### REVIEW-0547

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:88

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:88
- Section 18\.2 Debug mode \(under Section 18 Digital DFT\), paragraph 024 \(page 159\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.2 Debug mode (under Section 18 Digital DFT), paragraph 024 (page 159)
```

### REVIEW-0548

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:89

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:89
- Section 18\.3 ADC TEST LOW NOISE \(under Section 18 Digital DFT\), paragraph 006 \(page 160\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 006 (page 160)
```

### REVIEW-0549

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:90

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:90
- Section 18\.3 ADC TEST LOW NOISE \(under Section 18 Digital DFT\), paragraph 023 \(page 160\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 023 (page 160)
```

### REVIEW-0550

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:91

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:91
- Section 18\.4 ADC TEST FAST \(under Section 18 Digital DFT\), paragraph 010 \(page 161\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.4 ADC TEST FAST (under Section 18 Digital DFT), paragraph 010 (page 161)
```

### REVIEW-0551

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:92

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:92
- Section 18\.5 BIST MODE \(under Section 18 Digital DFT\), paragraph 030 \(page 161\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Section 18.5 BIST MODE (under Section 18 Digital DFT), paragraph 030 (page 161)
```

### REVIEW-0552

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:93

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:93
- Stage 1 OCR power\-domain table/description \(PD\_TOP1V2\)
- PD\_TOP1V2\: Included block\(s\)\: ADSP,, multi\_channel\_fifo, i2c\_spi\_slave, main\_controller\_top, senshub\_mst\_i2c, pad\_mux, pmu, stbio1\_regmap, scan\_out\_mux, xbar\_afe\. Domain type\: Always\-On\. Control mode\: HW\. Notes\: Always active\. • Function\: Ensures continuity of critical functions \(Data Storage Mode, Sensor\-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only\)\. • Characteristics\: Never powered down\. • Control\: Managed by hardware\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOP1V2: Included block(s): ADSP,, multi_channel_fifo, i2c_spi_slave, main_controller_top, senshub_mst_i2c, pad_mux, pmu, stbio1_regmap, scan_out_mux, xbar_afe. Domain type: Always-On. Control mode: HW. Notes: Always active. • Function: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only). • Characteristics: Never powered down. • Control: Managed by hardware.
```

### REVIEW-0553

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:94

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:94
- Stage 1 OCR power\-domain table/description \(PD\_STREDL\)
- PD\_STREDL\: Included block\(s\)\: STREDL\. Domain type\: Switchable\. Control mode\: SW\. Notes\: Can be powered down in idle\. • Function\: Powers the STREDL core and associated cache\. • Characteristics\: Can be powered down when STREDL is not in use\. • Control\: Managed via software \(power management driver\)\(see 12\.3\.1\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_STREDL: Included block(s): STREDL. Domain type: Switchable. Control mode: SW. Notes: Can be powered down in idle. • Function: Powers the STREDL core and associated cache. • Characteristics: Can be powered down when STREDL is not in use. • Control: Managed via software (power management driver)(see 12.3.1)
```

### REVIEW-0554

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:95

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:95
- Stage 1 OCR power\-domain table/description \(PD\_TOP3V3\)
- PD\_TOP3V3\: Included block\(s\)\: H9A\_MEM\_OTP\_ PUMP\_85AL05\_2\. Domain type\: Always\-On\. Voltage\: 3A\. Control mode\: HW\. Notes\: Always active\. • Function\: power supply to the OTP memory block\. • Characteristics\: Never powered down\. It provides 4\.7V of power supply to the OTP memory block during programming \(write\) operations • Control\: Managed by hardware\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOP3V3: Included block(s): H9A_MEM_OTP_ PUMP_85AL05_2. Domain type: Always-On. Voltage: 3A. Control mode: HW. Notes: Always active. • Function: power supply to the OTP memory block. • Characteristics: Never powered down. It provides 4.7V of power supply to the OTP memory block during programming (write) operations • Control: Managed by hardware.
```

### REVIEW-0555

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** duplicate descriptive evidence

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:96

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:96
- Stage 1 OCR power\-domain table/description \(PD\_TOPIO\)
- PD\_TOPIO\: Included block\(s\)\: level\_shifter\_sel\. Domain type\: Always\-On\. Control mode\: HW\. Notes\: Always active 32 10\.4\.\. • Function\: Powers communication PAD • Characteristics\: Never powered down\. • Control\: Managed by hardware\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
PD_TOPIO: Included block(s): level_shifter_sel. Domain type: Always-On. Control mode: HW. Notes: Always active 32 10.4.. • Function: Powers communication PAD • Characteristics: Never powered down. • Control: Managed by hardware.
```

### REVIEW-0556

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:97

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:97
- Section 10\.1 Introduction \(under Section 10 Power Domains\), paragraph 031 \(page 31\)
- This document paragraph describes the Power Domain architecture implemented in the STBIO1\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
This document paragraph describes the Power Domain architecture implemented in the STBIO1.
```

### REVIEW-0557

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:98

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:98
- Section 10\.2 Definitions \(under Section 10 Power Domains\), paragraph 011 \(page 32\)
- Retention Domain\: Domain that retains register state even when the main logic is powered down\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Retention Domain: Domain that retains register state even when the main logic is powered down.
```

### REVIEW-0558

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:99

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:99
- Section 17\.2\.2 MBIST Controller \(under Section 17\.2 Memory BIST Architecture\), paragraph 052 \(page 157\)
- Main functionalities of controller are\: • Mode management \(RunBIST mode, Retention mode etc\.\)

**audit_decision:** rejected

**Estratto sorgente:**

```text
Main functionalities of controller are: • Mode management (RunBIST mode, Retention mode etc.)
```

### REVIEW-0559

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:100

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:100
- Stage 1 OCR page 12, lines 4\-5
- Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio\-impedance, EDA and PPG \(Photoplethysmography\) embedded in a single die\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.
```

### REVIEW-0560

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:101

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:101
- Stage 1 OCR page 12, lines 38\-40
- ADSP is an embedded IP able to elaborate ultra\-low\-power custom DSP functions\. The main purpose of ADSP is to reduce the computation workload on both ISPU and host processor, while saving power through the optimization of both hardware and algorithm\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
ADSP is an embedded IP able to elaborate ultra-low-power custom DSP functions. The main purpose of ADSP is to reduce the computation workload on both ISPU and host processor, while saving power through the optimization of both hardware and algorithm.
```

### REVIEW-0561

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:102

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:102
- Stage 1 OCR page 12, lines 42\-45
- Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain\. The data collected by sensor hub is accessible from the Advanced DSP and ISPU, for sensor fusion algorithm elaboration\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor hub IP can read external sensors by means of an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain. The data collected by sensor hub is accessible from the Advanced DSP and ISPU, for sensor fusion algorithm elaboration.
```

### REVIEW-0562

**Documento:** DRS

**Posizione:** Digital Main Functions

**Classe del blocco:** audit\_rejected

**Spiegazione:** topic output limit

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:103

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_summary\_audit\.csv\:data\-record\:103
- Stage 1 OCR page 13, lines 17\-18
- Sensor Hub and Elaboration results\)\. The depth of each Sub\-FIFO is configurable by regmap\. Each Sub\-FIFO behavior as a Classic FIFO\.

**audit_decision:** rejected

**Estratto sorgente:**

```text
Sensor Hub and Elaboration results). The depth of each Sub-FIFO is configurable by regmap. Each Sub-FIFO behavior as a Classic FIFO.
```

### REVIEW-0563

**Documento:** DRS

**Posizione:** \*\*Arbitration, control, and shared resources\*\* \{\#arbitration\-control\-and\-shared\-resources\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:1

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:354

**Estratto sorgente:**

```text
Priority between simultaneous resource requesters: need clarification.
```

### REVIEW-0564

**Documento:** DRS

**Posizione:** \*\*Sequencing and domain control\*\* \{\#sequencing\-and\-domain\-control\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:2

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:405

**Estratto sorgente:**

```text
Domain transition ordering and reset-release dependencies: need clarification.
```

### REVIEW-0565

**Documento:** DRS

**Posizione:** \*\*4\.1 Digital block list\*\* \{\#41\-digital\-block\-list\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:3

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:434

**Estratto sorgente:**

```text
| Sensor-Hub | Operate the Sensor Hub I2C master for external targets, including trigger/control, pad enable, data collection, and FIFO multi-mode coordination. | Detailed integration relationship: need clarification. |
```


**Contenuto supportato mantenuto:**

```text
| Sensor-Hub | Operate the Sensor Hub I2C master for external targets, including trigger/control, pad enable, data collection, and FIFO multi-mode coordination. |  |
```

### REVIEW-0566

**Documento:** DRS

**Posizione:** \*\*4\.1 Digital block list\*\* \{\#41\-digital\-block\-list\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:4

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:443

**Estratto sorgente:**

```text
| OTP | Provide the source-specified one-time-programmable memory interface used by ADSP boot, programming, and test routines. | Detailed integration relationship: need clarification. |
```


**Contenuto supportato mantenuto:**

```text
| OTP | Provide the source-specified one-time-programmable memory interface used by ADSP boot, programming, and test routines. |  |
```

### REVIEW-0567

**Documento:** DRS

**Posizione:** \*\*4\.1 Digital block list\*\* \{\#41\-digital\-block\-list\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:5

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:444

**Estratto sorgente:**

```text
| PAD MUX | Route source-specified functional, scan, BIST, debug, and ISPU-debug signals to and from device pads. | Detailed integration relationship: need clarification. |
```


**Contenuto supportato mantenuto:**

```text
| PAD MUX | Route source-specified functional, scan, BIST, debug, and ISPU-debug signals to and from device pads. |  |
```

### REVIEW-0568

**Documento:** DRS

**Posizione:** \*\*4\.1 Digital block list\*\* \{\#41\-digital\-block\-list\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:6

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:445

**Estratto sorgente:**

```text
| ISPU | An interrupt triggers ISPU wake-up. Local processing function: need clarification. | from I2C_SPI_AHB (XBAR connection); to Regmap (XBAR connection); to SENSOR HUB (XBAR connection); to FIFO (XBAR connection); to ADSP (XBAR connection); from ISPU debug (XBAR connection) |
```


**Contenuto supportato mantenuto:**

```text
| ISPU | An interrupt triggers ISPU wake-up. | from I2C_SPI_AHB (XBAR connection); to Regmap (XBAR connection); to SENSOR HUB (XBAR connection); to FIFO (XBAR connection); to ADSP (XBAR connection); from ISPU debug (XBAR connection) |
```

### REVIEW-0569

**Documento:** DRS

**Posizione:** \*\*4\.2 Arbitration, control, and shared resources\*\* \{\#42\-arbitration\-control\-and\-shared\-resources\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:7

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:458

**Estratto sorgente:**

```text
Register and memory access coordination: ADSP executes ADSP firmware for OTP boot/write/test and signal elaboration, using mapped program/data/register memory and soft-reset handling. Regmap implements the mapped AFE, system, and OTP registers, exposing configuration/status while enforcing reset and OTP write-protection rules. BIST Controller controls BIST operating modes and coordinates ADC/OTP test operations and their register-visible results. I2C_SPI_AHB accepts I2C/SPI accesses and translates them as needed into AHB transactions for device configuration and readback, including ISPU access. SPI interface provides SPI register transactions to Regmap. I2C interface provides I2C register transactions to Regmap. Regmap provides register read response to SPI interface and I2C interface. Concurrent-access ordering policy: need clarification.
```


**Contenuto supportato mantenuto:**

```text
Register and memory access coordination: ADSP executes ADSP firmware for OTP boot/write/test and signal elaboration, using mapped program/data/register memory and soft-reset handling. Regmap implements the mapped AFE, system, and OTP registers, exposing configuration/status while enforcing reset and OTP write-protection rules. BIST Controller controls BIST operating modes and coordinates ADC/OTP test operations and their register-visible results. I2C_SPI_AHB accepts I2C/SPI accesses and translates them as needed into AHB transactions for device configuration and readback, including ISPU access. SPI interface provides SPI register transactions to Regmap. I2C interface provides I2C register transactions to Regmap. Regmap provides register read response to SPI interface and I2C interface.
```

### REVIEW-0570

**Documento:** DRS

**Posizione:** \*\*4\.2 Arbitration, control, and shared resources\*\* \{\#42\-arbitration\-control\-and\-shared\-resources\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:8

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:502

**Estratto sorgente:**

```text
Flow control and backpressure: need clarification
```

### REVIEW-0571

**Documento:** DRS

**Posizione:** \*\*4\.2 Arbitration, control, and shared resources\*\* \{\#42\-arbitration\-control\-and\-shared\-resources\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:9

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:506

**Estratto sorgente:**

```text
Synchronization: need clarification
```

### REVIEW-0572

**Documento:** DRS

**Posizione:** \*\*4\.2 Arbitration, control, and shared resources\*\* \{\#42\-arbitration\-control\-and\-shared\-resources\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:10

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:510

**Estratto sorgente:**

```text
Latency and bandwidth: need clarification
```

### REVIEW-0573

**Documento:** DRS

**Posizione:** \*\*4\.2 Arbitration, control, and shared resources\*\* \{\#42\-arbitration\-control\-and\-shared\-resources\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:11

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:514

**Estratto sorgente:**

```text
Priority between simultaneous resource requesters: need clarification.
```

### REVIEW-0574

**Documento:** DRS

**Posizione:** \*\*4\.6 Digital performance requirements\*\* \{\#46\-digital\-performance\-requirements\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:12

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:559

**Estratto sorgente:**

```text
Reset connection DDS_STBIO1_2054: PMU.resetn_32k_main_ctrl -> Main Controller.i_rstn_sync_32; release/synchronization behavior: need clarification.
```


**Contenuto supportato mantenuto:**

```text
Reset connection DDS_STBIO1_2054: PMU.resetn_32k_main_ctrl -> Main Controller.i_rstn_sync_32;
```

### REVIEW-0575

**Documento:** DRS

**Posizione:** \*\*4\.6 Digital performance requirements\*\* \{\#46\-digital\-performance\-requirements\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:13

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:567

**Estratto sorgente:**

```text
| DDS_STBIO1_1024 | stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft | stbio1_top.dig_wrapper_LV.u_xbar_afe.hclk | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.clk_xbar_en \| stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_1024 | stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft | stbio1_top.dig_wrapper_LV.u_xbar_afe.hclk | 16 MHz |  |
```

### REVIEW-0576

**Documento:** DRS

**Posizione:** \*\*4\.6 Digital performance requirements\*\* \{\#46\-digital\-performance\-requirements\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:14

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:568

**Estratto sorgente:**

```text
| DDS_STBIO1_1023 | stbio1_top.dig_wrapper_LV.u_pmu.w_sh_clk | stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.sys_clk | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.i_en_sh_clk \| stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_1023 | stbio1_top.dig_wrapper_LV.u_pmu.w_sh_clk | stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.sys_clk | 16 MHz |  |
```

### REVIEW-0577

**Documento:** DRS

**Posizione:** \*\*4\.6 Digital performance requirements\*\* \{\#46\-digital\-performance\-requirements\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:15

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:569

**Estratto sorgente:**

```text
| DDS_STBIO1_2026 | stbio1_top.dig_wrapper_LV.u_pmu.clk_xbar | stbio1_top.dig_wrapper_LV.u_regmap_otp.hclk | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3 \| stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode \| stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3_reg \| stbio1_top.dig_wrapper_LV.u_pm u.clk_en_s3 \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_2026 | stbio1_top.dig_wrapper_LV.u_pmu.clk_xbar | stbio1_top.dig_wrapper_LV.u_regmap_otp.hclk | 16 MHz |  |
```

### REVIEW-0578

**Documento:** DRS

**Posizione:** \*\*4\.6 Digital performance requirements\*\* \{\#46\-digital\-performance\-requirements\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:16

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:571

**Estratto sorgente:**

```text
| DDS_STBIO1_1022 | stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft | stbio1_top.dig_wrapper_LV.u_ADSP.stmc_clk | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.adsp_run \| stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_1022 | stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft | stbio1_top.dig_wrapper_LV.u_ADSP.stmc_clk | 16 MHz |  |
```

### REVIEW-0579

**Documento:** DRS

**Posizione:** \*\*4\.6 Digital performance requirements\*\* \{\#46\-digital\-performance\-requirements\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:17

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:573

**Estratto sorgente:**

```text
| DDS_STBIO1_1026 | stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_16m | stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_16MHz | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.i_en_clk_16MHz_sleep \| stbio1_top.dig_wrapper_LV.u_pm u.scan_mode \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_1026 | stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_16m | stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_16MHz | 16 MHz |  |
```

### REVIEW-0580

**Documento:** DRS

**Posizione:** \*\*4\.6 Digital performance requirements\*\* \{\#46\-digital\-performance\-requirements\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:18

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:594

**Estratto sorgente:**

```text
Measured latency and cross-domain synchronization behavior: need clarification.
```

### REVIEW-0581

**Documento:** DRS

**Posizione:** \*\*4\.6 Digital performance requirements\*\* \{\#46\-digital\-performance\-requirements\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:19

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:598

**Estratto sorgente:**

```text
Clock-path endpoints requiring clarification: DDS_STBIO1_2024.
```

### REVIEW-0582

**Documento:** DRS

**Posizione:** \*\*4\.7 Clock and synchronization across domains\*\* \{\#47\-clock\-and\-synchronization\-across\-domains\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:20

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:603

**Estratto sorgente:**

```text
The clock network distributes 16 MHz clocks with and without clock gating; 32 kHz clocks without clock gating; 64 kHz clocks without clock gating. Incomplete source and destination clock labels: need clarification.
```


**Contenuto supportato mantenuto:**

```text
The clock network distributes 16 MHz clocks with and without clock gating; 32 kHz clocks without clock gating; 64 kHz clocks without clock gating.
```

### REVIEW-0583

**Documento:** DRS

**Posizione:** \*\*4\.7 Clock and synchronization across domains\*\* \{\#47\-clock\-and\-synchronization\-across\-domains\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:21

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:607

**Estratto sorgente:**

```text
Reset/synchronization-labelled connection DDS_STBIO1_2054: PMU.resetn_32k_main_ctrl -> Main Controller.i_rstn_sync_32; synchronization implementation: need clarification.
```


**Contenuto supportato mantenuto:**

```text
Reset/synchronization-labelled connection DDS_STBIO1_2054: PMU.resetn_32k_main_ctrl -> Main Controller.i_rstn_sync_32;
```

### REVIEW-0584

**Documento:** DRS

**Posizione:** \*\*4\.7 Clock and synchronization across domains\*\* \{\#47\-clock\-and\-synchronization\-across\-domains\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:22

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:619

**Estratto sorgente:**

```text
| DDS_STBIO1_1024 | stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft | stbio1_top.dig_wrapper_LV.u_xbar_afe.hclk | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.clk_xbar_en \| stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_1024 | stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft | stbio1_top.dig_wrapper_LV.u_xbar_afe.hclk | 16 MHz |  |
```

### REVIEW-0585

**Documento:** DRS

**Posizione:** \*\*4\.7 Clock and synchronization across domains\*\* \{\#47\-clock\-and\-synchronization\-across\-domains\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:23

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:620

**Estratto sorgente:**

```text
| DDS_STBIO1_1023 | stbio1_top.dig_wrapper_LV.u_pmu.w_sh_clk | stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.sys_clk | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.i_en_sh_clk \| stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_1023 | stbio1_top.dig_wrapper_LV.u_pmu.w_sh_clk | stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.sys_clk | 16 MHz |  |
```

### REVIEW-0586

**Documento:** DRS

**Posizione:** \*\*4\.7 Clock and synchronization across domains\*\* \{\#47\-clock\-and\-synchronization\-across\-domains\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:24

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:621

**Estratto sorgente:**

```text
| DDS_STBIO1_2026 | stbio1_top.dig_wrapper_LV.u_pmu.clk_xbar | stbio1_top.dig_wrapper_LV.u_regmap_otp.hclk | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3 \| stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode \| stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3_reg \| stbio1_top.dig_wrapper_LV.u_pm u.clk_en_s3 \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_2026 | stbio1_top.dig_wrapper_LV.u_pmu.clk_xbar | stbio1_top.dig_wrapper_LV.u_regmap_otp.hclk | 16 MHz |  |
```

### REVIEW-0587

**Documento:** DRS

**Posizione:** \*\*4\.7 Clock and synchronization across domains\*\* \{\#47\-clock\-and\-synchronization\-across\-domains\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:25

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:623

**Estratto sorgente:**

```text
| DDS_STBIO1_1022 | stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft | stbio1_top.dig_wrapper_LV.u_ADSP.stmc_clk | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.adsp_run \| stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_1022 | stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft | stbio1_top.dig_wrapper_LV.u_ADSP.stmc_clk | 16 MHz |  |
```

### REVIEW-0588

**Documento:** DRS

**Posizione:** \*\*4\.7 Clock and synchronization across domains\*\* \{\#47\-clock\-and\-synchronization\-across\-domains\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:26

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:624

**Estratto sorgente:**

```text
| DDS_STBIO1_2024 | need clarification | need clarification | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m2 \| stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode \| stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m2_reg \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_2024 |  |  | 16 MHz |  |
```

### REVIEW-0589

**Documento:** DRS

**Posizione:** \*\*4\.7 Clock and synchronization across domains\*\* \{\#47\-clock\-and\-synchronization\-across\-domains\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:27

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:627

**Estratto sorgente:**

```text
| DDS_STBIO1_1026 | stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_16m | stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_16MHz | 16 MHz | Gated; control expression: stbio1_top.dig_wrapper_LV.u_pm u.i_en_clk_16MHz_sleep \| stbio1_top.dig_wrapper_LV.u_pm u.scan_mode \| ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable; signal spelling: need clarification |
```


**Contenuto supportato mantenuto:**

```text
| DDS_STBIO1_1026 | stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_16m | stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_16MHz | 16 MHz |  |
```

### REVIEW-0590

**Documento:** DRS

**Posizione:** \*\*4\.7 Clock and synchronization across domains\*\* \{\#47\-clock\-and\-synchronization\-across\-domains\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:28

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:644

**Estratto sorgente:**

```text
Clock-domain crossing, reset-domain crossing, and measured interrupt response time: need clarification.
```

### REVIEW-0591

**Documento:** DRS

**Posizione:** \*\*8\. Assumptions\*\* \{\#8\-assumptions\}

**Classe del blocco:** review\_only\_or\_unsupported\_presentation

**Spiegazione:** The existing presentation path omitted review\-only or unsupported descriptive text; supported independent text was retained\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json\:omissions\:29

**Riferimenti sorgente:**

- artifacts/stage5\_drs/descriptive\_publication\_audit\.json
- digital\_requirements\_specification\.md\:renderer\-input\-line\:1088

**Estratto sorgente:**

```text
- TBD-001: Unassigned requirements in DRS traceability matrix require architectural owner review.
```


## Digital IPOS

### REVIEW-0592

**Documento:** Digital IPOS

**Posizione:** artifacts/stage6\_digital\_ipos

**Classe del blocco:** stage\_not\_executed

**Spiegazione:** No whole\-stage runner was recorded in this window\. Any verified block outputs are reported separately and do not complete the stage\. A valid\-empty allocation is not a generation or validation result\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- snap\-73c872b1307b6adb5eaf843e

**Riferimenti sorgente:**

- artifacts/orchestrator/workflow\_cli\_runs\.jsonl
### REVIEW-0593

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8104\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8104
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8104; offset 0\:76:**

```text
ser_mode "i2c_spi" To choose if the interface is SPI only, I2C only or both.
```

### REVIEW-0594

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8104\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8104
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8104; offset 77\:96:**

```text
Suggested : i2c_spi
```

### REVIEW-0595

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8102\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8102
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8102; offset 0\:35:**

```text
i2c_hs_mode 1'b0 To activate HS I2C
```

### REVIEW-0596

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported relative\-clause subject; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8004\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8004
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8004; offset 0\:299:**

```text
A double byte write access to the address 0x68-0x6f (with data that is the number of bytes that the master wants to read) shall start the data preload from AHB in order to have the internal fifo not empty when the read request will be done by the master. [TO: IPOS_I2C_SPI_AHB_0010] [Vpriority High]
```

### REVIEW-0597

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8103\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8103
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8103; offset 0\:44:**

```text
i2c_master_code 8'h00 Master code for HS I2C
```

### REVIEW-0598

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8100\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8100
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8100; offset 0\:33:**

```text
CONNECTION fifo_dpt 8 FIFO depth.
```

### REVIEW-0599

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8100\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8100
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8100; offset 34\:49:**

```text
Suggested val 8
```

### REVIEW-0600

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8105\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8105
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8105; offset 0\:27:**

```text
ip_version 8'haa IP version
```

### REVIEW-0601

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8101\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8101
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8101; offset 0\:129:**

```text
rd_to_max_val 6000 Time available between double byte write to communicate the number of bytes to be read and the following read.
```

### REVIEW-0602

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8101\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8101
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8101; offset 130\:201:**

```text
If timer expires the operation is aborted and proper flag is activated.
```

### REVIEW-0603

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8101\:clause\:3\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8101
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8101; offset 202\:221:**

```text
Suggested val. 1200
```

### REVIEW-0604

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8106\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8106
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8106; offset 0\:35:**

```text
i2c_dev_id 7'h5f I2C device address
```

### REVIEW-0605

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8002\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_8002
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:I2C\_SPI\_AHB\:DDS\_STBIO1\_8002; offset 0\:104:**

```text
The IP has a serial interface (I2C or SPI) and a parallel bus interface AHB. [TO: IPOS_I2C_SPI_AHB_0007]
```

### REVIEW-0606

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- I2C\_SPI\_AHB

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0607

**Documento:** Digital IPOS

**Posizione:** I2C\_SPI\_AHB\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported relative\-clause subject; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- I2C\_SPI\_AHB

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0608

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported relative\-clause subject; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_051\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_051
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_051; offset 142\:217:**

```text
This signal indicates the number of clock that o_ADC_start shall stay high.
```

### REVIEW-0609

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unbalanced source delimiters; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_107\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_107
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_107; offset 0\:183:**

```text
When in Measurement state, after the wait at least of the TX_ledset time related to the frame that is being executed. (TX_LEDSET_FRAME {n}]), the o_start_adc signal shall be set high.
```

### REVIEW-0610

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_094\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_094
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_094; offset 0\:123:**

```text
When only GSR is selected (NO ECG0 and PPG are selected), if i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] is greater than 0,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_094; offset 123\:329:**

```text
 the Device FSM shall go in SLEEP after the IDLE State and shall go back in Operative State only when the measurement shall be run or, in case of cds disabled, when the o_gsr_curr shall change its polarity.
```

### REVIEW-0611

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_052\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_052
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_052; offset 136\:301:**

```text
The o_end_cal_phases shall be set to 1 if i_do_calibration (bit 0 of ADC_CAL_CONFIG) is set to 0, otherwise shall be set to 0 until the end of the calibration phase.
```

### REVIEW-0612

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_011\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_011
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_011; offset 0\:165:**

```text
When the HC_EN (ECG_CTRL register [0]) is set to 0 and IMP_EN (IMP_CTRL register [0]) is set to 1 and ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL register [1]) is set to 1,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_011; offset 165\:317:**

```text
 ECG1 and ECG2 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall remain high
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_011; offset 340\:484:**

```text
 and the Device_FSM shall go to the WAIT_SU State, so main_controller_status_register (DEVICE_STATUS_REG register [2:0]) shall be equal to 0x03.
```

### REVIEW-0613

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_125\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_125
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_125; offset 0\:51:**

```text
When i_reset_ramp is high all output shall be down.
```

### REVIEW-0614

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_140\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_140
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_140; offset 0\:106:**

```text
Once the PPG Raw Data and PPG Noise reach the i_n_average_ppg value , depending on the ALC Mask bit value,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_140; offset 146\:832:**

```text
 and final results shall be computed as follow: I_N_Average_PPG Samples Result with ALC MASK=0 Result with ALC Mask=1 0 3= (N1+P+N2) (Acc_P-(Acc_N)/2) * 8 Acc_P*16 2 4= (N1+2P+N2) (Acc_P -(Acc_N)) * 4 Acc_P *8 4 8= (2N1+4P+2N2) (Acc_P -(Acc_N)) * 2 Acc_P *4 8 16= (4N1+8P+4N2) (Acc_P -(Acc_N)) Acc_P *2 16 32= (8N1+16P+8N2) (Acc_P -(Acc_N))/2 Acc_P 32 64= (16N1+32P+16N2) (Acc_P -(Acc_N))/4 Acc_P /2 64 128= (32N1+64P+32N2) (Acc_P -(Acc_N))/8 Acc_P /4 128 256= (64N1+128P+64N2) (Acc_P -(Acc_N))/16 Acc_P /8 Table 18: PPG Result Table Where PPG Raw Data is indicated as P and PPG Noise is indicated as N1 and N2, while Acc_P is the accumulated PPG data and Acc_N is the accumulated noise
```

### REVIEW-0615

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_103\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_103
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_103; offset 163\:174:**

```text
After that,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_103; offset 174\:233:**

```text
 the PPG FSM shall bring itself into the Rising_Ramp state.
```

### REVIEW-0616

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_108\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_108
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_108; offset 129\:140:**

```text
After that,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_108; offset 140\:200:**

```text
 the PPG_FSM shall bring itself into the Falling Ramp state.
```

### REVIEW-0617

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported relative\-clause subject; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_002\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_002
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_002; offset 0\:127:**

```text
The only registers that the user shall change after setting the mode_operation to 1 are the ones described in requirement 7096.
```

### REVIEW-0618

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5005\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5005
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5005; offset 0\:84:**

```text
If the user set a value greater than 1024 into ones of the m_channel (see req 5004),
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5005; offset 84\:198:**

```text
 the value shall clamp at 1024 (check the input i_m_ecg, i_m_bia, i_m_gsr or i_m_ppg into the main controller fsm)
```

### REVIEW-0619

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_8106\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_8106
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_8106; offset 0\:111:**

```text
If multiple frame is selected (i_frame_repetition in ppg_fsm greater than 0), when Tx Preset falls from 1 to 0,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_8106; offset 111\:228:**

```text
 the en_tx shall pass from 1 to 0 only during the last repetition (check that when o_end_ppg_fsm is set, en_tx is 0).
```

### REVIEW-0620

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_032\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_032
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_032; offset 0\:231:**

```text
When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) during each frame o_Txi_idac_VREF shall go from 0 to N_MAX (DIGITAL_RAMP_CONFIG_PARAM_1 register [3:0]).
```

### REVIEW-0621

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_032\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_032
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_032; offset 232\:241:**

```text
At first,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_032; offset 241\:359:**

```text
 o_Txi_idac_VREF shall be increase its value of N_START for next step o_Txi_idac_VREF shall be increase its value by 1
```

### REVIEW-0622

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_3127\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_3127
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_3127; offset 0\:31:**

```text
When ELAB_FSM is in BIA state ,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_3127; offset 31\:225:**

```text
 o_ADC_EN shall go high and 16 acquisitions are required (acquisitions described in section 5.4 ADC PHASE ) and then device shall go in SLEEP (DEVICE_STATUS_REG register [2:0] is equal to 0x05).
```

### REVIEW-0623

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_4090\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_4090
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_4090; offset 0\:31:**

```text
If i_rst_async_bia is set to 1,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_4090; offset 31\:100:**

```text
 the start-up phase shall restart but no clock shall stop if enabled.
```

### REVIEW-0624

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1143\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1143
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1143; offset 0\:314:**

```text
For GSR Operation, if i_en_cds is set 0, the behavior shall as described in Requirement 143, otherwise the o_write_enabled shall be asserted when i_end_of_coversion is set to 1 and i_n_average_ecg_bia_gsr is equal to their limit values when the measurement is done with o_gsr_curr_on set to 0 and o_gsr_on set to 1
```

### REVIEW-0625

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_138\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_138
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_138; offset 78\:107:**

```text
When the CDS mode is enabled,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_138; offset 107\:292:**

```text
 the average block shall perform a n average on 16 sample acquisition on GSR ON and 16 sample acquisition on GSR OFF, then shall perform a subtraction operation between the two results.
```

### REVIEW-0626

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:DDS\_STBIO1\_0117\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_0117
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:DDS\_STBIO1\_0117; offset 0\:62:**

```text
During the Configuration Phase (IDLE STATE of the Device_FSM),
```


**Frammento sorgente\: requirement\:Main Controller\:DDS\_STBIO1\_0117; offset 62\:242:**

```text
 the user shall be able to: • Configure Bio-Channel or Optical Channel, the ADC Calibration and then Start a measurement cycle. • Put the device in Debug-Mode. [TO: IPOS_MAIN_CTRL]
```

### REVIEW-0627

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:DDS\_STBIO1\_0124\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_0124
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:DDS\_STBIO1\_0124; offset 0\:163:**

```text
• To check data in unique FIFO (default config) the user shall check the first MSB which will have to be equal to the table in DATA TAG Table. [TO: IPOS_MAIN_CTRL]
```

### REVIEW-0628

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145; offset 0\:35:**

```text
The Frame shall work as follows: 1.
```

### REVIEW-0629

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145\:clause\:5\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145; offset 382\:783:**

```text
The final result shall be computed as follows: Number of times the Frame has been repeated Result 2 (Res_F_R1 + Res_F_R2)/2 4 (Res_F_R1 + Res_F_R2+Res_F_R3+Res_F_R4)/4 8 (Res_F_R1 + Res_F_R2+Res_F_R3+…..+Res_F_R8)/8 Table 20: Frame Repetitions Result Computation table Where Res_F_Rx stands for Result_frame_Repeated_times (Example: RES_F_R2 refers to the result of the second repetition of the frame.
```

### REVIEW-0630

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_017\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_017
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_017; offset 234\:348:**

```text
On the other hand, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 0, the O_IMP_CURINJ_PD shall remain high.
```

### REVIEW-0631

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_044\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_044
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_044; offset 0\:28:**

```text
When i_rstn is asserted low,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_044; offset 28\:106:**

```text
 all the output shall be set to 0, except for count_cap that shall be set to 9
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_044; offset 106\:153:**

```text
 and o_end_cal_phase that shall be set to high.
```

### REVIEW-0632

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_0152\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_0152
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_0152; offset 0\:33:**

```text
If the calibration has been done,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_0152; offset 33\:176:**

```text
 the ADC_error_caps values computed shall reset only if the POR signal is asserted or shall be overwritten if another calibration is performed.
```

### REVIEW-0633

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_128\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_128
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_128; offset 0\:200:**

```text
When ECG0 and BIA are selected 21 acquisitions shall be required (acquisitions described in section 5.4 ADC PHASE) and then device shall go in SLEEP (DEVICE_STATUS_REG register [2:0] is equal to 101).
```

### REVIEW-0634

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported conditional consequence marker; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_097\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_097
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_097; offset 0\:197:**

```text
When in Reset state, if the rstn_i is de-asserted , i_wave_velocity_mode is and the i_start_ppg_fsm is high, if i_ID_Frame is equal to 0 or two successively frame have two different i_rx_ch_frame ,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_097; offset 197\:250:**

```text
 then the PPG FSM shall go to ALC Compensation state.
```

### REVIEW-0635

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_078\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_078
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_078; offset 0\:28:**

```text
If i_su_hlt_dly is set to 0.
```

### REVIEW-0636

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_089\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_089
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_089; offset 0\:50:**

```text
If the en_gsr_cds [bit 3 of GSR_CTRL] is set High,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_089; offset 50\:226:**

```text
 the i_m_gsr shall define also in which time slot after the GSR_Curr_on falls from 1 to 0, an acquisition without current injection (o_gsr_curr_on set to 0) shall be performed.
```

### REVIEW-0637

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_018\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_018
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_018; offset 0\:263:**

```text
When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) signal is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1, 5ms after the falling of imp_curinj_pd and O_PD_IMP, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 1, O_CK_M,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_018; offset 263\:469:**

```text
 O_CK_P and O_CK_Q shall be generated from Clock generator block so they run at FREQ_BIA_CLK_m_p_q (EN_CHOP_FREQ_MOD_DEMOD register [4:3] ) and its values shall be chosen from 20kHz, 50kHz, 100kHz, 200kHz .
```

### REVIEW-0638

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported or incomplete predicate; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_018\:clause\:3\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_018
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_018; offset 582\:593:**

```text
After this,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_018; offset 593\:621:**

```text
 the clock shall always run.
```

### REVIEW-0639

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_036\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_036
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_036; offset 147\:352:**

```text
Furthermore, if no Bio -Channel operations are selected and more than 150us are left before the start of a new time slot, the o_pd_clkf (Digital Top signal) shall be set to 1, otherwise shall be left to 0.
```

### REVIEW-0640

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unbalanced source delimiters; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_134\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_134
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_134; offset 0\:294:**

```text
According to time diagram, when in RESET_PPG and ELAB_FSM is in PPG state during the first frame (i_id_frame=0) , shall be wait a configurable time PPG_START_UP_TIME (PPG_START_UP_TIME starting from when i_start_operation_ppg is set to 1 and at least 1 clock cycle after i_start_ppg is set to 1
```

### REVIEW-0641

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1136\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1136
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1136; offset 0\:188:**

```text
After the assertion of i_end_of_conversion a number of times equals to i_n_average_ecg_bia_gsr (in case of ECG, BIA and GSR) or i_n_average_ppg (in case of PPG without frame repetitions) ,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1136; offset 251\:281:**

```text
 and o_write_enable shall rise
```

### REVIEW-0642

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_126\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_126
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_126; offset 0\:21:**

```text
When ALC_COMP starts,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_126; offset 21\:158:**

```text
 o_BTIA_gain (2:0) shall be set at i_gain_start (PPG_ALC_CONFIG_PARAM_2 register [4:2]) and o_w_BTIA_ALC (8:0) shall be set at 100000000.
```

### REVIEW-0643

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_132\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_132
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_132; offset 0\:243:**

```text
After T1+T2 (PPG_ALC_CONFIG_PARAM_2 register [1:0]), if o_BTIA_gain (2:0) < i_gain_max_set (PPG_ALC_CONFIG_PARAM_2 register [7:5]), during ALC_COMPENSATION state of PPG fsm with o_end_compensation set to 0, o_BTIA_gain increase its value of 1.
```

### REVIEW-0644

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unbalanced source delimiters; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_132\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_132
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_132; offset 244\:374:**

```text
Instead, if o_BTIA_gain 2:0) >= i_gain_max_set (PPG_ALC_CONFIG_PARAM_2 register [7:5]), o_BTIA_gain shall remain at its old value.
```

### REVIEW-0645

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unbalanced source delimiters; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_004\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_004
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_004; offset 0\:250:**

```text
[Covers: DDS_STBIO1_0116] When the Device_FSM FSM is in BOOT State, that is DEVICE_STATUS_REG register [2:0]) == 0x01 (main_controller_status_register), it shall wait that the ADSP ends the BOOT Phase, checking when the i_quokka_boot_end is set high.
```

### REVIEW-0646

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unbalanced source delimiters; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_004\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_004
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_004; offset 251\:280:**

```text
When the BOOT Phase is ended,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_004; offset 280\:503:**

```text
 the Device_FSM FSM shall go to IDLE State, check that DEVICE_STATUS_REG register [2:0]) == 0x02, (main_controller_status_register), check that the w_en_ldo1v8 signal is set low and that the O_PD_CLKF signal is set to high.
```

### REVIEW-0647

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported relative\-clause subject; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_075\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_075
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_075; offset 0\:82:**

```text
The counter that defines the timing during the start-up phase shall work at 32KHz.
```

### REVIEW-0648

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_072\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_072
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_072; offset 0\:88:**

```text
When the i_hc_en is set to 1 and i_imp_en is set to 0 and i_n_ecg_channel is equal to 1,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_072; offset 88\:138:**

```text
 ECG0 shall be active so the o_pd_hc2 shall go low
```

### REVIEW-0649

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_053\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_053
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_053; offset 0\:51:**

```text
When the i_ADC_en_mc and i_adc_en_mask is set to 1,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_053; offset 51\:121:**

```text
 at least 160 clock cycles shall pass before the ADC is ready to work.
```

### REVIEW-0650

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_029\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_029
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_029; offset 0\:167:**

```text
When DEVICE_FSM FSM is in IDLE if PPG_SEL (DEVICE_CONFIG_CHANNEL [4]) is set to 1 and MODE_OPERATION (bit [1:0] on DEVICE_CONFIG_OPERATION register) is different to 0,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_029; offset 167\:291:**

```text
 the device shall go in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05)
```

### REVIEW-0651

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_4079\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_4079
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_4079; offset 0\:31:**

```text
If i_rst_async_ecg is set to 1,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_4079; offset 31\:100:**

```text
 the start-up phase shall restart but no clock shall stop if enabled.
```

### REVIEW-0652

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_021\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_021
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_021; offset 0\:259:**

```text
When DEVICE_FSM FSM is in WAIT_SU state, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1; 20ms after the falling of O_RST_IMP, if EN_CHOP_CLK_IMP (EN_CHOP_FREQ_MOD_DEMOD register [1]) is set to 1,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_021; offset 259\:370:**

```text
 O_CK_CHOP_IMP shall be generated from Clock generator block, so O_CK_CHOP_IMP shall be run at 10kHz frequency.
```

### REVIEW-0653

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_099\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_099
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_099; offset 154\:185:**

```text
This shall happen in OPERATIVE.
```

### REVIEW-0654

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_074\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_074
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_074; offset 0\:88:**

```text
When the i_hc_en is set to 1 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 3,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_074; offset 88\:153:**

```text
 ECG0- ECG1 and ECG2 shall be active so the o_pd_hc2 shall go low
```

### REVIEW-0655

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_038\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_038
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_038; offset 0\:80:**

```text
When the ELAB_FSM is in ECG State, the ADC_Mux (concatenation of {o_adc_mux_sel,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_038; offset 80\:235:**

```text
 o_adc_mux_bio_channel} on digital top) output shall be set equal to 001 and after 4 acquisitions (described in section 5.4 ADC PHASE) shall be set to 010.
```

### REVIEW-0656

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_038\:clause\:3\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_038
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_038; offset 336\:353:**

```text
In the ECG state.
```

### REVIEW-0657

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported relative\-clause subject; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5004\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5004
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5004; offset 0\:97:**

```text
The max value that the user shall use for every m_channel (m_ecg, m_bia, m_gsr and m_ppg) is 1024
```

### REVIEW-0658

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_093\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_093
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_093; offset 0\:316:**

```text
If en_gsr_cds is set high [bit 3 of GSR_CTRL] the GSR_SNS (acquisition with o_gsr_curr_on set to 1) and GSR_CDS (acquisition with o_gsr_curr_on set to 0) shall be sampled 16 times, then mediated to get one single value for each of them, and then the final result shall be the subtraction between GSR_SNS and GSR_CDS.
```

### REVIEW-0659

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_113\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_113
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_113; offset 138\:185:**

```text
After that, if there are no more frames to run,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_113; offset 185\:352:**

```text
 the PPG_FSM shall go into the Reset State, otherwise, if there are other frames to run and channel rx is not changed, the PPG_FSM shall go into the Rx_start_up phase.
```

### REVIEW-0660

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_3126\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_3126
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_3126; offset 0\:67:**

```text
When ELAB_FSM is in ECG state and EC0, ECG1 and ECG2 are selected ,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_3126; offset 67\:251:**

```text
 o_ADC_EN shall go high and15 acquisitions are required (acquisitions described in 5.4 ADC PHASE) and then device shall go in SLEEP (DEVICE_STATUS_REG register [2:0] is equal to 0x05).
```

### REVIEW-0661

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unbalanced source delimiters; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_008\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_008
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_008; offset 190\:289:**

```text
The value of the time_slot_data shall be referred to the start of the entire measurement cycle (for
```

### REVIEW-0662

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported or incomplete predicate; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_728\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_728
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_728; offset 0\:97:**

```text
At the end of ALC compensation, if ALC is not masked, o_w_BTIA_ALC relative to the running frame,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_728; offset 97\:179:**

```text
 shall be set to output system (check when i_end_of_compensation rise in PPG FSM).
```

### REVIEW-0663

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_088\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_088
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_088; offset 114\:170:**

```text
 following this formula: GSRdata = time_slot 2 ∗ m_gsr .
```

### REVIEW-0664

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_010\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_010
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_010; offset 0\:204:**

```text
[Covers: DDS_STBIO1_0119] When the FSM is in IDLE State, if ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is high, HC_EN (ECG_CTRL register [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 0,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_010; offset 204\:342:**

```text
 ECG0 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall go low
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_010; offset 342\:495:**

```text
 and the Device_FSM FSM shall go to the WAIT_SU State , so the main_controller_status_register (DEVICE_STATUS_REG register [2:0]) shall be equal to 0x03.
```

### REVIEW-0665

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unbalanced source delimiters; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_033\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_033
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_033; offset 0\:110:**

```text
When not in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) ,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_033; offset 110\:244:**

```text
 Device_FSM shall go back in IDLE only if the user turns off the MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0]) is set to 0).
```

### REVIEW-0666

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_073\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_073
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_073; offset 0\:88:**

```text
When the i_hc_en is set to 0 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 2,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_073; offset 88\:152:**

```text
 ECG1 and ECG2 shall be active so the o_pd_hc2 shall remain high
```

### REVIEW-0667

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2144\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2144
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2144; offset 0\:721:**

```text
[Covers: DDS_STBIO1_0124] [Covers: DDS_STBIO1_0142] The data written in FIFO shall have the following tag: DATA TYPE BIT: 23 - 20 BIT: 19 - 16 BIT: 15 - 0 PPG FRAME 0 0000 DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT PPG FRAME 1 0001 PPG FRAME 2 0010 PPG FRAME 3 0011 PPG FRAME 4 0100 PPG FRAME 5 0101 PPG FRAME 6 0110 PPG FRAME 7 0111 PPG FRAME 8 1000 PPG FRAME 9 1001 PPG FRAME 10 1010 PPG FRAME 11 1011 TIME SLOT DATA 1111 0000 DATA 16 BIT ECG0_AC 1100 0000 DATA 16 BIT ECG0_DC 1101 0000 DATA 16 BIT ECG1_AC 1100 0001 DATA 16 BIT ECG1_DC 1101 0001 DATA 16 BIT ECG2_AC 1100 0010 DATA 16 BIT ECG2_DC 1101 0010 DATA 16 BIT
```

### REVIEW-0668

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_077\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_077
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_077; offset 0\:73:**

```text
20ms after that the o_rst_hc2 is gone low, if i_clk_hlt_en is equal to 1,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_077; offset 73\:155:**

```text
 chopper_clock shall be generated and after another 10ms, o_rsti_hc2 shall go low.
```

### REVIEW-0669

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unresolved subject reference; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5015\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5015
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5015; offset 83\:132:**

```text
If the user wants to interrupt the WAIT_SU state,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_5015; offset 132\:213:**

```text
 it shall perform the Soft Reset procedure described in the DDS [DDS_STBIO1_1114]
```

### REVIEW-0670

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unresolved subject reference; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_7135\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_7135
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_7135; offset 0\:57:**

```text
If the ALC_COARSE (o_w_BTIA_ALC) result is equal to zero,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_7135; offset 57\:82:**

```text
 it shall be brought to 1
```

### REVIEW-0671

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unbalanced source delimiters; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_031\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_031
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_031; offset 0\:309:**

```text
When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x 05) o_ADC_start shall go high a number of times equal “2 ^ value indicated in regmap of FRAME_{n}_SAMPLES (FRAME_n_PARAMETERS_1 register [5:3]) for ALC and PPG both (2*(2^regmap_value).
```

### REVIEW-0672

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_6129\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_6129
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_6129; offset 0\:34:**

```text
When i_ALC_comp_start is set to 1,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_6129; offset 34\:146:**

```text
 the first rise of the o_comp_rx_ck shall happen at least after a T1+T_TIA_On time, both configurable by regmap.
```

### REVIEW-0673

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unbalanced source delimiters; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_101\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_101
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_101; offset 0\:26:**

```text
When in Rx_Start_Up state,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_101; offset 26\:174:**

```text
 the PPG_FSM shall stay in this state for the T_rx_set time (GENERAL_PPG_PARAMETERS_3 register [3:0])) and then go into the FIRST_ALC_SAMPLES state.
```

### REVIEW-0674

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_030\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_030
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_030; offset 0\:309:**

```text
When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) the device shall be execute a number of frames equal to N_PPG_FRAME (GENERAL_PPG_PARAMETERS_1 register [3:0]) (Check the i_id_frame shall increase until it’s equal to N_PPG_FRAME-1).
```

### REVIEW-0675

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_030\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_030
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_030; offset 310\:363:**

```text
At the beginning of each frame o_ADC_EN shall go high
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_030; offset 363\:451:**

```text
 and it shall go low when ALC_COMPENSATION is performed or at the end of the last frame.
```

### REVIEW-0676

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1105\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1105
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1105; offset 0\:108:**

```text
If no multiple frame is selected (i_frame_repetition in ppg_fsm set to 0), when Tx Preset falls from 1 to 0,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1105; offset 108\:147:**

```text
 also the en_tx shall pass from 1 to 0.
```

### REVIEW-0677

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unsupported or incomplete predicate; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_061\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_061
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_061; offset 0\:70:**

```text
When the i_data_out_adc is sampled, the 15 bit (MSB in little endian),
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_061; offset 70\:136:**

```text
 shall be negated in order to convert the input in Two Complement.
```

### REVIEW-0678

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** unresolved subject reference; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1116\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1116
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1116; offset 0\:47:**

```text
When the Ioff Calibration algorithm is enabled,
```


**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_1116; offset 47\:113:**

```text
 it shall be performed every time a new measurements cycle starts.
```

### REVIEW-0679

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_139\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_139
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_139; offset 0\:220:**

```text
When a PPG Raw data ( i_data_valid_ppg_adc set to 1) or a PPG_Noise (i_data_valid_noise_ppg_adc set to 1) data is sampled (i_end_of_conversion set to 1) the data shall be accumulated until i_n_average_ppg is not reached.
```

### REVIEW-0680

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive disposition

**Classe del blocco:** no\_supported\_claim

**Spiegazione:** The shared claim plan did not preserve this descriptive contribution\: unresolved\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145\:clause\:2\:meaning\:1

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**disposition:** unresolved

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145; offset 36\:97:**

```text
Select how many times a particular frame shall be repeated 2.
```

### REVIEW-0681

**Documento:** Digital IPOS

**Posizione:** Main Controller\: descriptive disposition

**Classe del blocco:** no\_supported\_claim

**Spiegazione:** The shared claim plan did not preserve this descriptive contribution\: unresolved\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145\:clause\:3\:meaning\:1

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**disposition:** unresolved

**Frammento sorgente\: requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_2145; offset 98\:211:**

```text
The result of each repetition shall be obtained as explained in [IPOS_STBIO1_MAIN_CONTROLLER_1 40] REQUIREMENT 3.
```

### REVIEW-0682

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:no\_supported\_claim

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0683

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported relative\-clause subject; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0684

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unbalanced source delimiters; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0685

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0686

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:ambiguous guard boundary; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0687

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0688

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported predicate grammar; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0689

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported conditional consequence marker; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0690

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported or incomplete predicate; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0691

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unresolved subject reference; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Main Controller

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0692

**Documento:** Digital IPOS

**Posizione:** Main Controller\: shared preflight

**Classe del blocco:** ipos\_source\_relationship\_changed\:requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_064

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Source\-model relationship needs review

**Riferimenti a requisiti o contesti:**

- requirement\:Main Controller\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_064

**Riferimenti sorgente:**

- approved requirement\:IPOS\_STBIO1\_MAIN\_CONTROLLER\_064
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv
### REVIEW-0693

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_302\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_302
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_302; offset 0\:100:**

```text
[DDS_STBIO1_302] Requirement If MODE_CONFIG register is 0x00 the operative mode shall be functional.
```

### REVIEW-0694

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** unsupported or incomplete predicate; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_394\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_394
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_394; offset 0\:126:**

```text
If O_DCCK_P_i changes its value from '1' to '0' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp,
```


**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_394; offset 126\:146:**

```text
 shall be set to '1'
```

### REVIEW-0695

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** unsupported or incomplete predicate; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_393\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_393
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_393; offset 0\:126:**

```text
If O_DCCK_N_i changes its value from '0' to '1' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp,
```


**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_393; offset 126\:146:**

```text
 shall be set to '1'
```

### REVIEW-0696

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_395\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_395
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_395; offset 0\:228:**

```text
The DCC feature consists of two stages that detect whether one of six electrode inputs is in the range 0 to 1.5V; thresholds have a 100mV step, and continuous current from 25nA to 200nA flows from the stages into the electrodes.
```

### REVIEW-0697

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_306\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_306
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_306; offset 0\:100:**

```text
[DDS_STBIO1_306] Requirement If MODE_CONFIG register is 0x10 the operative mode shall be ISPU_DEBUG.
```

### REVIEW-0698

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_308\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_308
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_308; offset 0\:106:**

```text
[DDS_STBIO1_308] Requirement If MODE_CONFIG register is 0x40 the operative mode shall be Bist Bypass mode.
```

### REVIEW-0699

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_307\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_307
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_307; offset 0\:107:**

```text
[DDS_STBIO1_307] Requirement If MODE_CONFIG register is 0x20 the operative mode shall be Bist MEMSAFE mode.
```

### REVIEW-0700

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_303\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_303
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_303; offset 0\:94:**

```text
[DDS_STBIO1_303] Requirement If MODE_CONFIG register is 0x01 the operative mode shall be SCAN.
```

### REVIEW-0701

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_305\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_305
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_305; offset 0\:95:**

```text
[DDS_STBIO1_305] Requirement If MODE_CONFIG register is 0x08 the operative mode shall be DEBUG.
```

### REVIEW-0702

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** unsupported or incomplete predicate; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_392\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_392
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_392; offset 0\:126:**

```text
If O_DCCK_P_i changes its value from '0' to '1' and DCCK_IRQ_MASK is set to '1', then irq_DCCK_IRQ_ST, output of u_regmap_otp,
```


**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_392; offset 126\:146:**

```text
 shall be set to '1'
```

### REVIEW-0703

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: descriptive claim preflight

**Classe del blocco:** ambiguous guard boundary; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PAD MUX\:DDS\_STBIO1\_304\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_304
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PAD MUX\:DDS\_STBIO1\_304; offset 0\:94:**

```text
[DDS_STBIO1_304] Requirement If MODE_CONFIG register is 0x04 the operative mode shall be BIST.
```

### REVIEW-0704

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:ambiguous guard boundary; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- PAD MUX

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0705

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported or incomplete predicate; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- PAD MUX

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0706

**Documento:** Digital IPOS

**Posizione:** PAD MUX\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- PAD MUX

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0707

**Documento:** Digital IPOS

**Posizione:** PMU\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PMU\:DDS\_STBIO1\_2052\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_2052
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PMU\:DDS\_STBIO1\_2052; offset 0\:36:**

```text
The stbio1_top.dig_wrapper_LV.u_pmu.
```

### REVIEW-0708

**Documento:** Digital IPOS

**Posizione:** PMU\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:PMU\:DDS\_STBIO1\_0114\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_0114
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:PMU\:DDS\_STBIO1\_0114; offset 0\:56:**

```text
At the release of the POR signal from the analog domain,
```


**Frammento sorgente\: requirement\:PMU\:DDS\_STBIO1\_0114; offset 56\:177:**

```text
 the PMU shall manage the turn-on of the LDO1V8 and starts clocks Start-Up Sequence (reported in PMU IPOS) [TO: IPOS_PMU]
```

### REVIEW-0709

**Documento:** Digital IPOS

**Posizione:** PMU\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- PMU

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0710

**Documento:** Digital IPOS

**Posizione:** PMU\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported predicate grammar; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- PMU

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0711

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3004\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3004
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3004; offset 0\:69:**

```text
0xCA000 SYSTEM_REGISTER 32 0xCA140 tst_main_reset_n, regmap_sw_resetn
```

### REVIEW-0712

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3006\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3006
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3006; offset 0\:70:**

```text
0xCD000 OTP (TRIMM REGS) 32 0xCD02F tst_main_reset_n, regmap_sw_resetn
```

### REVIEW-0713

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3002\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3002
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3002; offset 0\:47:**

```text
0xC9000 OTP REGISTER 8 0xC902C tst_main_reset_n
```

### REVIEW-0714

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3001\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3001
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3001; offset 0\:59:**

```text
0xC80EC RESERVED 0xC8FFF tst_main_reset_n, regmap_sw_resetn
```

### REVIEW-0715

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3005\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3005
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3005; offset 0\:59:**

```text
0xCA144 RESERVED 0xCCFFF tst_main_reset_n, regmap_sw_resetn
```

### REVIEW-0716

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3003\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3003
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3003; offset 0\:59:**

```text
0xC9030 RESERVED 0xC9FFF tst_main_reset_n, regmap_sw_resetn
```

### REVIEW-0717

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3000\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3000
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3000; offset 0\:52:**

```text
132 **Update-IR** Run-Test/Idle Select-DR-Scan 13.4.
```

### REVIEW-0718

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3000\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3000
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3000; offset 53\:80:**

```text
STBIO1 Register Map 13.4.1.
```

### REVIEW-0719

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3000\:clause\:3\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3000
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3000; offset 81\:161:**

```text
STBIO1 Register Map Here is described the list of registers in the register map.
```

### REVIEW-0720

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3000\:clause\:4\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3000
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3000; offset 162\:278:**

```text
The AFE_BLOCK registers are accessible by I2C/SPI direct access and AHB interface, while the others are only by AHB.
```

### REVIEW-0721

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3000\:clause\:5\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3000
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3000; offset 279\:437:**

```text
The I2C/SPI direct access mode is done by the HOST INTF port (I2C/SPI AHB) and the address of the AFE_BLOCK registers are arranged in 4 pages of 64 registers.
```

### REVIEW-0722

**Documento:** Digital IPOS

**Posizione:** Regmap\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Regmap\:DDS\_STBIO1\_3000\:clause\:6\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_3000
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Regmap\:DDS\_STBIO1\_3000; offset 438\:589:**

```text
BASE START ADDRESS ADDRESS BLOCK REGISTER WIDTH BASE END ADDRE VREF_TRIM SS RESET REQ_ID 0xC8000 AFE_BLOCK 8 0xC80EB tst_main_reset_n, regmap_sw_resetn
```

### REVIEW-0723

**Documento:** Digital IPOS

**Posizione:** Regmap\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Regmap

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0724

**Documento:** Digital IPOS

**Posizione:** Sensor\-Hub\: descriptive claim preflight

**Classe del blocco:** unsupported conditional consequence marker; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Sensor\-Hub\:DDS\_STBIO1\_9500\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_9500
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Sensor\-Hub\:DDS\_STBIO1\_9500; offset 0\:186:**

```text
[DDS_STBIO1_9500] Requirement In case also other sources that writes into FIFO are active, then sensor hub shall work always in multi-fifo mode fifo_mode input of sensor hub set to '1' .
```

### REVIEW-0725

**Documento:** Digital IPOS

**Posizione:** Sensor\-Hub\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Sensor\-Hub\:DDS\_STBIO1\_9027\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_9027
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Sensor\-Hub\:DDS\_STBIO1\_9027; offset 0\:188:**

```text
[DDS_STBIO1_9027] Requirement The bit 0 of SLAVE1_DEV_ADD, SLAVE2_DEV_ADD, SLAVE3_DEV_ADD registers shall be ignored: ONLY read operations towards I2C target 1, 2 and 3 shall be performed.
```

### REVIEW-0726

**Documento:** Digital IPOS

**Posizione:** Sensor\-Hub\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Sensor\-Hub\:DDS\_STBIO1\_9034\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_9034
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Sensor\-Hub\:DDS\_STBIO1\_9034; offset 0\:100:**

```text
The NACK_REGISTER register is reset every time a new I2C operation starts. [TO: IPOS_Senshub_MB_i2c]
```

### REVIEW-0727

**Documento:** Digital IPOS

**Posizione:** Sensor\-Hub\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported conditional consequence marker; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Sensor\-Hub

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0728

**Documento:** Digital IPOS

**Posizione:** Sensor\-Hub\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Sensor\-Hub

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0729

**Documento:** Digital IPOS

**Posizione:** Smart FIFO\: descriptive claim preflight

**Classe del blocco:** unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- requirement\:Smart FIFO\:DDS\_STBIO1\_00001199\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_00001199
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Smart FIFO\:DDS\_STBIO1\_00001199; offset 0\:22:**

```text
When in Multiple Fifo,
```


**Frammento sorgente\: requirement\:Smart FIFO\:DDS\_STBIO1\_00001199; offset 22\:306:**

```text
 the 6 sub-FIFO offset shall coincide with the following table : FIFO OFFSET DATA TYPE ECG FIFO OFFSET ECG0_AC, ECG0_DC BIA FIFO OFFSET BIA_AC_P, BIA_DC_P, BIA_AC_Q, BIA_DC_Q, ECG1_AC, ECG2_DC GSR FIFO OFFSET GSR, ECG1_DC, ECG2_AC PPG FIFO OFFSET PPG Table 31 : FIFO Offset Data Table
```

### REVIEW-0730

**Documento:** Digital IPOS

**Posizione:** Smart FIFO\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Smart FIFO\:DDS\_STBIO1\_89455449\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_89455449
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Smart FIFO\:DDS\_STBIO1\_89455449; offset 81\:150:**

```text
These two modes are mutually exclusive. [TO: IPOS_FIFO_CTRL_89455449]
```

### REVIEW-0731

**Documento:** Digital IPOS

**Posizione:** Smart FIFO\: descriptive claim preflight

**Classe del blocco:** unsupported predicate grammar; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Smart FIFO\:DDS\_STBIO1\_89456557\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_89456557
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Smart FIFO\:DDS\_STBIO1\_89456557; offset 0\:113:**

```text
The FIFO Controller shall be able to address 1.5 kbyte divided into 32-bit address. [TO: IPOS_FIFO_CTRL_89456557]
```

### REVIEW-0732

**Documento:** Digital IPOS

**Posizione:** Smart FIFO\: descriptive claim preflight

**Classe del blocco:** unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- requirement\:Smart FIFO\:DDS\_STBIO1\_89457790\:clause\:1\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_89457790
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Smart FIFO\:DDS\_STBIO1\_89457790; offset 0\:133:**

```text
The FIFO 6 memory locations to access each sub-FIFO in Multiple mode are obtained adding multiples of 256 to the memory base address.
```

### REVIEW-0733

**Documento:** Digital IPOS

**Posizione:** Smart FIFO\: descriptive claim preflight

**Classe del blocco:** unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** Shared interpretation left this context unresolved; dependent descriptive content cannot be accepted under the active contract\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- requirement\:Smart FIFO\:DDS\_STBIO1\_89457790\:clause\:2\:unresolved

**Riferimenti sorgente:**

- approved requirement\:DDS\_STBIO1\_89457790
- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- approved snapshot
- artifacts/stage2\_mirco\_arc/block\_inventory\.csv

**Frammento sorgente\: requirement\:Smart FIFO\:DDS\_STBIO1\_89457790; offset 134\:434:**

```text
Example: FIFO Memory Base Address = 0xC4000, then: FIFO 0 memory location 0xC4000 FIFO 1 memory location 0xC4100 FIFO 2 memory location 0xC4200 FIFO 3 memory location 0xC4300 FIFO 4 memory location 0xC4400 FIFO 5 memory location 0xC4500 Table 29: SUB FIFO Memory Address [TO: IPOS_FIFO_CTRL_89457790]
```

### REVIEW-0734

**Documento:** Digital IPOS

**Posizione:** Smart FIFO\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported structured/table/procedure evidence; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Structured evidence not sufficiently recoverable

**Riferimenti a requisiti o contesti:**

- Smart FIFO

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0735

**Documento:** Digital IPOS

**Posizione:** Smart FIFO\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported multi\-clause or non\-normative construction; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Smart FIFO

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py
### REVIEW-0736

**Documento:** Digital IPOS

**Posizione:** Smart FIFO\: shared preflight

**Classe del blocco:** descriptive\_synthesis\_unresolved\:unsupported predicate grammar; full source retained

**Spiegazione:** The existing shared preflight returned this finding; no override or source correction was applied\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- Smart FIFO

**Riferimenti sorgente:**

- C\:\\Users\\iannuzza\\LOCAL\_PROJ\\Github\_copilot\_proj\\Deterministic\_Reqs\_workflow\\data\\canonical\\canonical\_store\.sqlite
- scripts/workflow\_routing\.py

## Analog IPOS

### REVIEW-0737

**Documento:** Analog IPOS

**Posizione:** artifacts/stage7\_analog\_ipos

**Classe del blocco:** stage\_not\_executed

**Spiegazione:** No whole\-stage runner was recorded in this window\. Any verified block outputs are reported separately and do not complete the stage\. A valid\-empty allocation is not a generation or validation result\.

**Conclusione:** Need clarification

**Riferimenti a requisiti o contesti:**

- snap\-73c872b1307b6adb5eaf843e

**Riferimenti sorgente:**

- artifacts/orchestrator/workflow\_cli\_runs\.jsonl

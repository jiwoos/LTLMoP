# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)

CompileOptions:
convexify: True
parser: structured
symbolic: False
use_region_bit_encoding: True
synthesizer: jtlv
fastslow: False
decompose: True

CurrentConfigName:
tutorial

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
FindingNemo4.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
r4 = p8
r5 = p7
r6 = p6
r7 = p5
r12 = p11
r2 = p10
r10 = p13
r11 = p12
r3 = p9
r8 = p4
r9 = p3
others = p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38, p39
r1 = p14

Spec: # Specification in structured English
go to r1


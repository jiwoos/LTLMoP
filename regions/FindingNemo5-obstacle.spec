# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
camera_turn_on, 1

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
FindingNemo5-obstacle.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)
nemo_detect, 1


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
r12 = p23
r2 = p13
r5 = p31, p32
r3 = p12
r8 = p7
r6 = p60, p61, p62
r9 = p6
r7 = p8
others = p1, p2, p37, p38, p39, p40, p41, p42, p43, p44, p45, p46, p47, p48, p49, p50, p51, p52, p53, p54, p55, p56, p57, p58, p59
r11 = p24
r10 = p25
r4 = p11
r1 = p28, p29, p30

Spec: # Specification in structured English
if not camera_turn_on then go to r1
if not camera_turn_on then go to r3
if not camera_turn_on then go to r5
if not camera_turn_on then go to r8

if nemo_detect then do camera_turn_on
if not nemo_detect then do not camera_turn_on


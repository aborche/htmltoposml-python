""" ESC/POS Commands (Constants) """
"""  Corrected to Custom VPK-80  """
# Calculate motion units
# HMU=1/x (in), VMU=1/y
# HMU=25.4/x (mm), VMU=25.4/y (mm)
# HMU=0,1245 mm, VMU=0,06225 mm
# HMU=0,0049 in, VMU=0,0024 in
# VKP80ii - x=204, y=408
# Printing Area max = 576, if PAM=0 -> MAX
# left margin = PAM*HMU

# Feed control sequences
CTL_LF     = '\x0a'              # Print and line feed
CTL_FF     = '\x0c'              # Form feed
CTL_CR     = '\x0d'              # Carriage return
CTL_HT     = '\x09'              # Horizontal tab
CTL_VT     = '\x1b\x64\x04'      # Vertical tab
NUL	   = '\x00'

# Printer hardware
HW_INIT    = '\x1b\x40'          # Clear data in buffer and reset modes
HW_SELECT  = '\x1b\x3d\x01'      # Printer select

# Paper
PAPER_EJECT      = '\x1d\x65\x05' 	# Eject ticket
PAPER_TOTAL_CUT  = '\x1b\x69'		# Paper total cut
PAPER_FULL_CUT   = '\x1d\x56\x00' 	# Full cut paper
PAPER_FEED_CUT   = '\x1d\x56\x41' 	# Partial cut paper
PAPER_FINAL_EJECT = '\x1d\x65\x03\x0c'	# Final ticket cut and eject

# Text format   
TXT_SET_HT	 = '\x1b\x44'	  # Set horizontal tab positions
#
TXT_CONTROL	 = '\x1b\x21'	  # Control print modes
#
# \x08 - Bold on/off
# \x10 - Double height on/off
# \x20 - Double width on/off
# \x40 - Italic mode on/off
# \x80 - Underline mode on/off
#
TXT_DEFAULT	 = '\x1b\x21\x00' # Reset all text properties

#TXT_NORMALA      = '\x1b\x21\x00' # Character Set Font A !!!!! Do not use this for set font !!!!! Use TXT_FONT_A, TXT_FONT_B
#TXT_NORMALB      = '\x1b\x21\x01' # Character Set Font B !!!!! Do not use this for set font !!!!! Use TXT_FONT_A, TXT_FONT_B

TXT_UNDERL_OFF   = '\x1b\x2d\x00' # Underline OFF
TXT_UNDERL_ON    = '\x1b\x2d\x01' # Underline 1-dot ON
TXT_UNDERL2_ON   = '\x1b\x2d\x02' # Underline 2-dot ON

TXT_BOLD_OFF     = '\x1b\x45\x00' # Bold OFF
TXT_BOLD_ON      = '\x1b\x45\x01' # Bold ON

TXT_ITALIC_OFF	 = '\x1b\x34\x00' # Italic OFF
TXT_ITALIC_ON	 = '\x1b\x34\x01' # Italic OFF

TXT_FONT       	 = '\x1b\x4d'	  # Font select
TXT_FONT_A       = '\x1b\x4d\x00' # Font type A
TXT_FONT_B       = '\x1b\x4d\x01' # Font type B

TXT_ALIGN_LT     = '\x1b\x61\x00' # Left justification
TXT_ALIGN_CT     = '\x1b\x61\x01' # Centering
TXT_ALIGN_RT     = '\x1b\x61\x02' # Right justification

TXT_CPI_MODE0	 = '\x1b\xc1\x00'	 # Set/cancel cpi mode. Font A = 11 cpi, Font B = 15 cpi
TXT_CPI_MODE1	 = '\x1b\xc1\x01'	 # Set/cancel cpi mode. Font A = 15 cpi, Font B = 20 cpi
TXT_CPI_MODE2	 = '\x1b\xc1\x02'	 # Set/cancel cpi mode. Font A = 20 cpi, Font A = 15 cpi

TXT_SIZE_DEFAULT = '\x1d\x21\x00' # Reset character size

TXT_SIZE_CUSTOM  = '\x1d\x21'	# Custom character size
# Bits 0 to 3 - select character size height
# Bits 4 to 7 - select character size width
# 1 - x2 (10,01)
# 2 - x3 (20,02)
# 3 - x4 (30,03)
# 4 - x5 (40,04)
# 5 - x6 (50,05)
# 6 - x7 (60,06)
# 7 - x8 (70,07)

# change position
TXT_SET_RPOS	 = '\x1b\x5c'	 # Set relative horisontal position
TXT_SET_APOS	 = '\x1b\x24'	 # Set absolute horisontal print position

# change black/white mode
TXT_NEG_ON	 = '\x1d\x42\x01' # Turn black/white reverse mode
TXT_NEG_OFF	 = '\x1d\x42\x00' # Turn black/white normal mode

# change black/white mode
TXT_UPDOWN_ON	 = '\x0a\x1b\x7b\x01' # Turn up/down mode on
TXT_UPDOWN_OFF	 = '\x0a\x1b\x7b\x00' # Turn up/down mode off

# change rotate mode
TXT_ROTATE_ON	 = '\x1b\x56\x01' # Turn rotate mode on
TXT_ROTATE_OFF	 = '\x1b\x56\x00' # Turn rotate mode off

TXT_LMARGIN	 = '\x1d\x4c'	  # Set Left Margin
TXT_PWIDTH	 = '\x1d\x57'	  # Set printing area width

TXT_18LSP	 = '\x1b\x30'	  # Set 1/8 inch line spacing
TXT_16LSP	 = '\x1b\x32'	  # Set 1/6 inch line spacing
TXT_LSP		 = '\x1b\x33'	  # Set custom line spacing default=64


# Char code table
CHARCODE_PC437  = '\x1b\x74\x00' # USA: Standard Europe
CHARCODE_PC850  = '\x1b\x74\x02' # Multilingual
CHARCODE_PC860  = '\x1b\x74\x03' # Portuguese
CHARCODE_PC863  = '\x1b\x74\x04' # Canadian-French
CHARCODE_PC865  = '\x1b\x74\x05' # Nordic
CHARCODE_PC858  = '\x1b\x74\x13' # Euro 
CHARCODE_SPACE  = '\x1b\x74\xff' # Space Page

# Barcode format
BARCODE_TXT_OFF = '\x1d\x48\x00' # HRI barcode chars OFF
BARCODE_TXT_ABV = '\x1d\x48\x01' # HRI barcode chars above
BARCODE_TXT_BLW = '\x1d\x48\x02' # HRI barcode chars below
BARCODE_TXT_BTH = '\x1d\x48\x03' # HRI barcode chars both above and below

BARCODE_FONT_A  = '\x1d\x66\x00' # Font type A for HRI barcode chars
BARCODE_FONT_B  = '\x1d\x66\x01' # Font type B for HRI barcode chars

BARCODE_HEIGHT  = '\x1d\x68'	 #\xa2' # Barcode Height [1-255] default 162
BARCODE_WIDTH   = '\x1d\x77'	 #\x03' # Barcode Width  [2-6] default 3

BARCODE_UPC_A   = '\x1d\x6b\x00' # Barcode type UPC-A
BARCODE_UPC_E   = '\x1d\x6b\x01' # Barcode type UPC-E
BARCODE_EAN13   = '\x1d\x6b\x02' # Barcode type EAN13
BARCODE_EAN8    = '\x1d\x6b\x03' # Barcode type EAN8
BARCODE_CODE39  = '\x1d\x6b\x04' # Barcode type CODE39
BARCODE_ITF     = '\x1d\x6b\x05' # Barcode type ITF
BARCODE_CODABAR = '\x1d\x6b\x06' # Barcode type CODABAR
BARCODE_CODE93  = '\x1d\x6b\x07' # Barcode type CODE93
BARCODE_CODE32  = '\x1d\x6b\x20' # Barcode type CODE32
BARCODE_CODE128FSA = '\x1d\x6b\x08\x7b\x41'  # Barcode CODE128 Font Set A
BARCODE_CODE128FSB = '\x1d\x6b\x08\x7b\x42'  # Barcode CODE128 Font Set B
BARCODE_CODE128FSC = '\x1d\x6b\x08\x7b\x43'  # Barcode CODE128 Font Set C

BARCODE_FILTER_NUMBER = '0123456789'
BARCODE_FILTER_CODE39 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%+-./'
BARCODE_FILTER_CODABAR = '0123456789ABCD$+-./;'

# Print internal flash logo 608x862
P_LOGO1_PART = '\x1b\xfa\x01'	 # Print logo 1 
P_LOGO2_PART = '\x1b\xfa\x02'	 # Print logo 2

# Image format  
S_RASTER_N      = '\x1d\x76\x30\x00' # Set raster image normal size
S_RASTER_2W     = '\x1d\x76\x30\x01' # Set raster image double width
S_RASTER_2H     = '\x1d\x76\x30\x02' # Set raster image double height
S_RASTER_Q      = '\x1d\x76\x30\x03' # Set raster image quadruple

# Printing Density
PD_N50          = '\x1d\x7c\x00' # Printing Density -50%
PD_N37          = '\x1d\x7c\x01' # Printing Density -37.5%
PD_N25          = '\x1d\x7c\x02' # Printing Density -25%
PD_N12          = '\x1d\x7c\x03' # Printing Density -12.5%
PD_0            = '\x1d\x7c\x04' # Printing Density  0%
PD_P50          = '\x1d\x7c\x08' # Printing Density +50%
PD_P37          = '\x1d\x7c\x07' # Printing Density +37.5%
PD_P25          = '\x1d\x7c\x06' # Printing Density +25%
PD_P12          = '\x1d\x7c\x05' # Printing Density +12.5%

# Reserved
RESERVED	= [ '', '' ]

# Printer status
# \x10\x04\x01
PRINTER_BIT_0	= RESERVED
PRINTER_BIT_1	= RESERVED
PRINTER_BIT_2	= RESERVED
PRINTER_BIT_3	= [ 'Online', 'Offline' ]
PRINTER_BIT_4	= RESERVED
PRINTER_BIT_5	= RESERVED
PRINTER_BIT_6	= RESERVED
PRINTER_BIT_7	= RESERVED
PRINTER_STATUS_VKP80II	= [ PRINTER_BIT_0, PRINTER_BIT_1, PRINTER_BIT_2, PRINTER_BIT_3, PRINTER_BIT_4, PRINTER_BIT_5, PRINTER_BIT_6, PRINTER_BIT_7 ]
PRINTER_STATUS_VKP80III	= [ PRINTER_BIT_0, PRINTER_BIT_1, PRINTER_BIT_2, PRINTER_BIT_3, PRINTER_BIT_4, PRINTER_BIT_5, PRINTER_BIT_6, PRINTER_BIT_7 ]

# Offline status
# \x10\x04\x02
OFFLINE_BIT_0	= RESERVED
OFFLINE_BIT_1	= RESERVED
OFFLINE_BIT_2	= [ 'Cover closed', 'Cover opened' ]
OFFLINE_BIT_3	= [ 'Paper isnt fed by LINE FEED button', 'Paper is fed by LINE FEED button' ]
OFFLINE_BIT_4	= RESERVED
OFFLINE_BIT_5	= [ 'Paper present', 'Printing stop due the paper end' ]
OFFLINE_BIT_6	= [ 'No error', 'Error' ]
OFFLINE_BIT_7	= RESERVED
OFFLINE_STATUS_VKP80II	= [ OFFLINE_BIT_0, OFFLINE_BIT_1, OFFLINE_BIT_2, OFFLINE_BIT_3, OFFLINE_BIT_4, OFFLINE_BIT_5, OFFLINE_BIT_6, OFFLINE_BIT_7 ]
OFFLINE_STATUS_VKP80III	= [ OFFLINE_BIT_0, OFFLINE_BIT_1, OFFLINE_BIT_2, OFFLINE_BIT_3, OFFLINE_BIT_4, OFFLINE_BIT_5, OFFLINE_BIT_6, OFFLINE_BIT_7 ]

# Error status
# \x10\x04\x03
ERROR_BIT_0	= RESERVED
ERROR_BIT_1	= RESERVED
ERROR_BIT_2	= RESERVED
ERROR_BIT_3	= [ 'Cutter ok', 'Cutter error' ]
ERROR_BIT_4	= RESERVED
ERROR_BIT_5	= [ 'No unrecoverable error', 'Unrecoverable error' ]
ERROR_BIT_6	= [ 'No auto-recoverable error', 'Auto-recoverable error' ]
ERROR_BIT_7	= RESERVED
ERROR_STATUS_VKP80II	= [ ERROR_BIT_0, ERROR_BIT_1, ERROR_BIT_2, ERROR_BIT_3, ERROR_BIT_4, ERROR_BIT_5, ERROR_BIT_6, ERROR_BIT_7 ]
ERROR_STATUS_VKP80III	= [ ERROR_BIT_0, ERROR_BIT_1, ERROR_BIT_2, ERROR_BIT_3, ERROR_BIT_4, ERROR_BIT_5, ERROR_BIT_6, ERROR_BIT_7 ]

IGNORE_NEAR_END		= True
IGNORE_NEAR_END_MASK	= { 'ROLL': 0b11110011, 'PAPER': 0b10111011 }

# Paper roll sensor status
# \x10\x04\x04
ROLL_BIT_0	= RESERVED
ROLL_BIT_1	= RESERVED
# Error code \x0C
ROLL_BIT_2	= [ 'Paper present in abudance', 'Near paper end' ]
ROLL_BIT_3	= [ 'Paper present in abudance', 'Near paper end' ]
ROLL_BIT_4	= RESERVED
# Error code \x60
ROLL_BIT_5	= [ 'Paper present', 'Paper not present' ]
ROLL_BIT_6	= [ 'Paper present', 'Paper not present' ]
ROLL_BIT_7	= RESERVED
ROLL_STATUS_VKP80II	= [ ROLL_BIT_0, ROLL_BIT_1, ROLL_BIT_2, ROLL_BIT_3, ROLL_BIT_4, ROLL_BIT_5, ROLL_BIT_6, ROLL_BIT_7 ]
ROLL_STATUS_VKP80III	= [ ROLL_BIT_0, ROLL_BIT_1, ROLL_BIT_2, ROLL_BIT_3, ROLL_BIT_4, ROLL_BIT_5, ROLL_BIT_6, ROLL_BIT_7 ]

# Print status
# \x10\x04\x11
PRINT_BIT_0	= RESERVED
PRINT_BIT_1	= RESERVED
PRINT_BIT_2	= [ 'Paper drag motor off', 'Paper drag motor on' ]
PRINT_BIT_3	= [ 'Ejector motor off', 'Ejector motor on' ]
PRINT_BIT_4	= RESERVED
PRINT_BIT_5	= [ 'Paper present', 'Printing stop due to paper end' ]
PRINT_BIT_6	= RESERVED
PRINT_BIT_7	= RESERVED
PRINT_STATUS_VKP80II	= [ PRINT_BIT_0, PRINT_BIT_1, PRINT_BIT_2, RESERVED, PRINT_BIT_4, PRINT_BIT_5, PRINT_BIT_6, PRINT_BIT_7 ]
PRINT_STATUS_VKP80III	= [ PRINT_BIT_0, PRINT_BIT_1, PRINT_BIT_2, PRINT_BIT_3, PRINT_BIT_4, PRINT_BIT_5, PRINT_BIT_6, PRINT_BIT_7 ]

# Full Status decoder (From manual 1.60 for VKP80iii)
#
# 1Byte = \x10 (DLE)
# 2Byte = \x0F
# 3Byte = paper status
PAPER_BIT_0	= [ 'Paper present', 'Paper not present' ]
PAPER_BIT_1	= RESERVED
PAPER_BIT_2	= [ 'Paper present in abundance', 'Near paper end' ]
PAPER_BIT_3	= RESERVED
PAPER_BIT_4	= RESERVED
PAPER_BIT_5	= [ 'Ticket not present in output', 'Ticket present in output' ]
PAPER_BIT_6	= [ 'Not virtual paper end', 'Virtual Paper end' ]
PAPER_BIT_7	= [ 'Notch not found', 'Notch Found' ]
PAPER_STATUS_VKP80II	= [ PAPER_BIT_0, PAPER_BIT_1, PAPER_BIT_2, PAPER_BIT_3, PAPER_BIT_4, PAPER_BIT_5, PAPER_BIT_6, PAPER_BIT_7 ]
PAPER_STATUS_VKP80III	= [ PAPER_BIT_0, PAPER_BIT_1, PAPER_BIT_2, PAPER_BIT_3, PAPER_BIT_4, PAPER_BIT_5, PAPER_BIT_6, PAPER_BIT_7 ]

# 4Byte = User status
USER_BIT_0	= [ 'Cover closed', 'Cover opened' ]
USER_BIT_1	= [ 'Cover closed', 'Cover opened' ]
USER_BIT_2	= [ 'No spooling', 'Spooling' ]
USER_BIT_3	= [ 'Drag paper motor off', 'Drag paper motor on' ]
USER_BIT_4	= RESERVED
USER_BIT_5	= [ 'LF key released', 'LF key pressed' ]
USER_BIT_6	= [ 'FF key released', 'FF key pressed' ]
USER_BIT_7	= RESERVED
USER_STATUS_VKP80II	= [ USER_BIT_0, USER_BIT_1, USER_BIT_2, USER_BIT_3, USER_BIT_4, USER_BIT_5, USER_BIT_6, USER_BIT_7 ]
USER_STATUS_VKP80III	= [ USER_BIT_0, USER_BIT_1, USER_BIT_2, USER_BIT_3, USER_BIT_4, USER_BIT_5, USER_BIT_6, USER_BIT_7 ]

# 5Byte = Recoverable error status
RECOVER_BIT_0	= [ 'Head temperature ok', 'Head temperature error' ]
RECOVER_BIT_1	= [ 'No COM error', 'RS232 COM error' ]
RECOVER_BIT_2	= RESERVED
RECOVER_BIT_3	= [ 'Power supply voltage ok', 'Power supply voltage error' ]
RECOVER_BIT_4	= RESERVED
RECOVER_BIT_5	= [ 'Acknowledge command', 'Not acknowledge command error' ]
RECOVER_BIT_6	= [ 'Free paper path', 'Paper jam' ]
RECOVER_BIT_7	= RESERVED
RECOVER_STATUS_VKP80II	= [ RECOVER_BIT_0, RECOVER_BIT_1, RECOVER_BIT_2, RECOVER_BIT_3, RECOVER_BIT_4, RECOVER_BIT_5, RECOVER_BIT_6, RECOVER_BIT_7 ]
RECOVER_STATUS_VKP80III	= [ RECOVER_BIT_0, RECOVER_BIT_1, RECOVER_BIT_2, RECOVER_BIT_3, RECOVER_BIT_4, RECOVER_BIT_5, RECOVER_BIT_6, RECOVER_BIT_7 ]

# 6Byte = Unrecoverable error status
UNRECOVER_BIT_0	= [ 'Cutter ok', 'Cutter error' ]
UNRECOVER_BIT_1	= RESERVED
UNRECOVER_BIT_2	= [ 'RAM ok', 'RAM error' ]
UNRECOVER_BIT_3	= [ 'EEPROM ok', 'EEPROM error' ]
UNRECOVER_BIT_4	= RESERVED
UNRECOVER_BIT_5	= RESERVED
UNRECOVER_BIT_6 = [ 'Flash ok', 'Flash error' ]
UNRECOVER_BIT_7	= RESERVED
UNRECOVER_STATUS_VKP80II	= [ UNRECOVER_BIT_0, UNRECOVER_BIT_1, UNRECOVER_BIT_2, UNRECOVER_BIT_3, UNRECOVER_BIT_4, UNRECOVER_BIT_5, UNRECOVER_BIT_6, UNRECOVER_BIT_7 ]
UNRECOVER_STATUS_VKP80III	= [ UNRECOVER_BIT_0, UNRECOVER_BIT_1, UNRECOVER_BIT_2, RESERVED, UNRECOVER_BIT_4, UNRECOVER_BIT_5, RESERVED, UNRECOVER_BIT_7 ]

TYPEID_BIT_0	= [ '2-Byte character codes not supported', '2-Byte character code is supported' ]
TYPEID_BIT_1	= [ 'Autocutter not supplied', 'Autocutter supplied' ]
TYPEID_BIT_2	= [ 'Thermal paper w/o label', 'Thermal paper with label' ]
TYPEID_BIT_3	= RESERVED
TYPEID_BIT_4	= RESERVED
TYPEID_BIT_5	= RESERVED
TYPEID_BIT_6	= RESERVED
TYPEID_BIT_7	= RESERVED

TYPEID = [ TYPEID_BIT_0, TYPEID_BIT_1, TYPEID_BIT_2, TYPEID_BIT_3, TYPEID_BIT_4, TYPEID_BIT_5, TYPEID_BIT_6, TYPEID_BIT_7 ]
MODELS = { '\x5d': 'VKP80II', '\x95': 'VKP80II-EE', '\xb9': 'VK80', '\xff': 'VKP80III' }

STATUS_VKP80II	= { 'PRINTER': PRINTER_STATUS_VKP80II, 'OFFLINE': OFFLINE_STATUS_VKP80II, 'ERROR': ERROR_STATUS_VKP80II, 'ROLL': ROLL_STATUS_VKP80II, \
                    'PRINT': PRINT_STATUS_VKP80II, 'PAPER': PAPER_STATUS_VKP80II, 'USER': USER_STATUS_VKP80II, 'RECOVER': RECOVER_STATUS_VKP80II, 'UNRECOVER': UNRECOVER_STATUS_VKP80II }
STATUS_VKP80III	= { 'PRINTER': PRINTER_STATUS_VKP80III, 'OFFLINE': OFFLINE_STATUS_VKP80III, 'ERROR': ERROR_STATUS_VKP80III, 'ROLL': ROLL_STATUS_VKP80III, \
                    'PRINT': PRINT_STATUS_VKP80III, 'PAPER': PAPER_STATUS_VKP80III, 'USER': USER_STATUS_VKP80III, 'RECOVER': RECOVER_STATUS_VKP80III, 'UNRECOVER': UNRECOVER_STATUS_VKP80III }

GETSTATUS = { 'VKP80II': STATUS_VKP80II, 'VKP80II-EE': STATUS_VKP80II, 'VK80': STATUS_VKP80II, 'VKP80III': STATUS_VKP80III }

STARTTAG = {   'B': TXT_BOLD_ON, 'U': TXT_UNDERL_ON, 'U2': TXT_UNDERL2_ON, 'I': TXT_ITALIC_ON, 'CENTER': TXT_ALIGN_CT,  \
               'UPDOWN': TXT_UPDOWN_ON, 'ROTATE': TXT_ROTATE_ON, 'NEG': TXT_NEG_ON, \
               'BR': CTL_LF, 'TAB': CTL_HT, 'INIT': HW_INIT }
CLOSETAG = {  'B': TXT_BOLD_OFF, 'U': TXT_UNDERL_OFF, 'U2': TXT_UNDERL_OFF, 'I': TXT_ITALIC_OFF, 'FONT': TXT_DEFAULT, 'TEXT': TXT_SIZE_DEFAULT, \
               'CENTER': TXT_ALIGN_LT, 'UPDOWN': TXT_UPDOWN_OFF, 'ROTATE': TXT_ROTATE_OFF, 'NEG': TXT_NEG_OFF, \
               'BR': CTL_LF }

TXT_ALIGN = {  'LEFT': TXT_ALIGN_LT, 'CENTER': TXT_ALIGN_CT, 'RIGHT': TXT_ALIGN_RT }
TXT_SET	  = {  'HT' : TXT_SET_HT, 'CPI0': TXT_CPI_MODE0, 'CPI1': TXT_CPI_MODE1, 'CPI2': TXT_CPI_MODE2, 'LMARGIN': TXT_LMARGIN, 'PWIDTH': TXT_PWIDTH, 'RPOS': TXT_SET_RPOS, 'APOS': TXT_SET_APOS }

BARCODE   = {  'HEIGHT' : BARCODE_HEIGHT, 'WIDTH': BARCODE_WIDTH }
BARCODE_TXT  = { 'OFF': BARCODE_TXT_OFF, 'ABOVE': BARCODE_TXT_ABV, 'BELOW': BARCODE_TXT_BLW, 'BOTH': BARCODE_TXT_BTH}
BARCODE_FONT = { 'A': BARCODE_FONT_A, 'B': BARCODE_FONT_B }
BARCODE_TYPE = { 'UPC-A': BARCODE_UPC_A, 'UPC-E': BARCODE_UPC_E, 'EAN13': BARCODE_EAN13, 'EAN8': BARCODE_EAN8, 'CODE39': BARCODE_CODE39, 'ITF': BARCODE_ITF, 'CODABAR': BARCODE_CODABAR, \
                 'CODE93': BARCODE_CODE93, 'CODE32': BARCODE_CODE32, 'CODE128FSA': BARCODE_CODE128FSA, 'CODE128FSB': BARCODE_CODE128FSB, 'CODE128FSC': BARCODE_CODE128FSC }
BARCODESTRUCT = { 'WIDTH': 3, 'HEIGHT': 162, 'FONT': 'A', 'POS': 'BELOW' }
TXT_DEFAULTS  = { 'FONT': 'A', 'SIZE': '0x00', 'CPI': '1', 'ALIGN': 'LEFT', 'HT': 8, 'PD': 6, 'LS': '1_6',\
                  'LMARGIN': 0, 'PWIDTH': 576, 'ALIGNLF': 'ON' }


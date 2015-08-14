from hexToBase64           import test as test_hexToBase64
from fixedXOR              import test as test_fixedXOR
from singleByteXOR         import test as test_singleByteXOR
from detectSingleByteXOR   import test as test_detectSingleByteXOR
from repeatingKeyXOR       import test as test_repeatingKeyXOR
from breakRepeatingKeyXOR  import test as test_breakRepeatingKeyXOR
from PKCS7padding          import *
from detectECB             import test as test_detectECB
from ECBmode               import test as test_ECBmode
from CBCmode               import test as test_CBCmode
from ECB_CBCdetection      import test as test_ECB_CBCdetection
from ECB_cut_and_paste     import test as test_ECB_cut_and_paste
from CBCbitflipping_attack import test as test_CBCbitflipping_attack

# Current tests
test_hexToBase64()

# Test catalogue
"""
test_fixedXOR()
test_singleByteXOR()
test_detectSingleByteXOR()
test_repeatingKeyXOR()
test_breakRepeatingKeyXOR()
test_detectECB()
test_ECBmode()
test_CBCmode()
test_ECB_CBCdetection()
test_ECB_cut_and_paste()
test_CBCbitflipping_attack()
"""

# Ctrl + Shift + { Up|Down } to move tests. (in Sublime Text 3, anyway)
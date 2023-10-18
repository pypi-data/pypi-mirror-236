import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.fontregion import fontregion

def hardcodedfontregions(option: str) -> list[fontregion]:
    """
    This function provides some hard-coded fontregions
    for the purpose of unit-tests
    
    # Parameters: None
    option: str: standard, we return the fontregions that belong to pdfminer & SplitDoc.pdf. If you enter pymupdf, we adjust the frequency to that library (for the same document).
    # Returns: those fontregions.
    """
    
    # -------------------------------------------------------
    
    trueregions = [fontregion(), fontregion(), fontregion(), fontregion(), fontregion()]
    
    trueregions[0].set_left(15.705920000000006)
    trueregions[0].set_right(24.95527000000001)
    trueregions[0].set_value(17.135365000000007)
    trueregions[0].set_frequency(0.023157894736842106+0.06736842105263158)
    trueregions[0].set_cascadelevel(1)
    trueregions[0].set_isregular(False)
    
    trueregions[1].set_left(13.099285000000005)
    trueregions[1].set_right(15.705920000000006)
    trueregions[1].set_value(14.276475000000005)
    trueregions[1].set_frequency(0.07473684210526316)
    trueregions[1].set_cascadelevel(2)
    trueregions[1].set_isregular(False)
    
    trueregions[2].set_left(10.913075000000003)
    trueregions[2].set_right(13.099285000000005)
    trueregions[2].set_value(11.922095000000004)
    trueregions[2].set_frequency(0.05368421052631579)
    trueregions[2].set_cascadelevel(3)
    trueregions[2].set_isregular(False)
    
    trueregions[3].set_left(8.979120000000002)
    trueregions[3].set_right(10.913075000000003)
    trueregions[3].set_value(9.904055000000003)
    trueregions[3].set_frequency(0.7789473684210526)
    trueregions[3].set_cascadelevel(4)
    trueregions[3].set_isregular(True)
    
    trueregions[4].set_left(7.8019300000000005)
    trueregions[4].set_right(8.979120000000002)
    trueregions[4].set_value(8.054185000000002)
    trueregions[4].set_frequency(0.002105263157894737)
    trueregions[4].set_cascadelevel(5)
    trueregions[4].set_isregular(False)
    
    if (option=="pymupdf"):
        trueregions[0].set_frequency(0.017543859649122806+0.07017543859649122)
        trueregions[1].set_frequency(0.17543859649122806)
        trueregions[2].set_frequency(0.10526315789473684)
        trueregions[3].set_frequency(0.6140350877192983)
        trueregions[4].set_frequency(0.017543859649122806)
    
    return trueregions

def hardcodedfontregions_pdfminer_LineTest1() -> list[fontregion]:
    """
    This function provides some hard-coded fontregions
    for the purpose of unit-tests
    
    # Parameters: None
    # Returns: those fontregions.
    """
    
    # -------------------------------------------------------
    
    trueregions = []
    
    thisregion = fontregion()
    thisregion.set_left(17.993999999999993)
    thisregion.set_right(24.182)
    thisregion.set_value(23.909)
    thisregion.set_frequency(0.0013553578991952562)
    thisregion.set_cascadelevel(1)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(11.805999999999987)
    thisregion.set_right(17.993999999999993)
    thisregion.set_value(12.078999999999988)
    thisregion.set_frequency(0.8470139771283355)
    thisregion.set_cascadelevel(2)
    thisregion.set_isregular(True)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(10.804999999999986)
    thisregion.set_right(11.805999999999987)
    thisregion.set_value(11.532999999999987)
    thisregion.set_frequency(0.0015247776365946632)
    thisregion.set_cascadelevel(3)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(8.529999999999985)
    thisregion.set_right(10.804999999999986)
    thisregion.set_value(10.076999999999986)
    thisregion.set_frequency(0.14781872088098263)
    thisregion.set_cascadelevel(4)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(6.436999999999983)
    thisregion.set_right(8.529999999999985)
    thisregion.set_value(6.982999999999984)
    thisregion.set_frequency(0.0020330368487928843)
    thisregion.set_cascadelevel(5)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(5.617999999999983)
    thisregion.set_right(6.436999999999983)
    thisregion.set_value(5.890999999999983)
    thisregion.set_frequency(0.00025412960609911054)
    thisregion.set_cascadelevel(6)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)
    
    return trueregions

def hardcodedfontregions_pymupdf_LineTest1() -> list[fontregion]:
    """
    This function provides some hard-coded fontregions
    for the purpose of unit-tests
    
    # Parameters: None
    # Returns: those fontregions.
    """
    
    # -------------------------------------------------------
    
    trueregions = []
    
    thisregion = fontregion()
    thisregion.set_left(17.994000062942504)
    thisregion.set_right(24.18199999809265)
    thisregion.set_value(23.90900000095367)
    thisregion.set_frequency(0.03361344537815126)
    thisregion.set_cascadelevel(1)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(11.806000127792357)
    thisregion.set_right(17.994000062942504)
    thisregion.set_value(12.079000124931333)
    thisregion.set_frequency(0.6680672268907563)
    thisregion.set_cascadelevel(2)
    thisregion.set_isregular(True)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(10.805000138282775)
    thisregion.set_right(11.806000127792357)
    thisregion.set_value(11.533000130653381)
    thisregion.set_frequency(0.012605042016806723)
    thisregion.set_cascadelevel(3)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(8.530000162124633)
    thisregion.set_right(10.805000138282775)
    thisregion.set_value(10.07700014591217)
    thisregion.set_frequency(0.19747899159663865)
    thisregion.set_cascadelevel(4)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(6.437000184059143)
    thisregion.set_right(8.530000162124633)
    thisregion.set_value(6.983000178337098)
    thisregion.set_frequency(0.07563025210084033)
    thisregion.set_cascadelevel(5)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(5.618000192642212)
    thisregion.set_right(6.437000184059143)
    thisregion.set_value(5.891000189781189)
    thisregion.set_frequency(0.012605042016806723)
    thisregion.set_cascadelevel(6)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)
    
    return trueregions

def hardcodedfontregions_pdfminer_LineTest2() -> list[fontregion]:
    """
    This function provides some hard-coded fontregions
    for the purpose of unit-tests
    
    # Parameters: None
    # Returns: those fontregions.
    """
    
    # -------------------------------------------------------
    
    trueregions = []

    thisregion = fontregion()
    thisregion.set_left(14.962199999999989)
    thisregion.set_right(18.0996)
    thisregion.set_value(17.9502)
    thisregion.set_frequency(0.0038910505836575876)
    thisregion.set_cascadelevel(1)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(11.725199999999976)
    thisregion.set_right(14.962199999999989)
    thisregion.set_value(11.974199999999977)
    thisregion.set_frequency(0.9381755296152183)
    thisregion.set_cascadelevel(2)
    thisregion.set_isregular(True)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(9.78299999999997)
    thisregion.set_right(11.725199999999976)
    thisregion.set_value(11.476199999999976)
    thisregion.set_frequency(0.057392996108949414)
    thisregion.set_cascadelevel(3)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(7.940399999999963)
    thisregion.set_right(9.78299999999997)
    thisregion.set_value(8.089799999999963)
    thisregion.set_frequency(0.000540423692174665)
    thisregion.set_cascadelevel(4)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)
    
    return trueregions

def hardcodedfontregions_pymupdf_LineTest2() -> list[fontregion]:
    """
    This function provides some hard-coded fontregions
    for the purpose of unit-tests
    
    # Parameters: None
    # Returns: those fontregions.
    """
    
    # -------------------------------------------------------
    
    trueregions = []
    
    thisregion = fontregion()
    thisregion.set_left(14.932412427663806)
    thisregion.set_right(18.170421531796457)
    thisregion.set_value(17.914789234101775)
    thisregion.set_frequency(0.032520325203252036)
    thisregion.set_cascadelevel(1)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(11.694403323531152)
    thisregion.set_right(14.932412427663806)
    thisregion.set_value(11.950035621225835)
    thisregion.set_frequency(0.6910569105691057)
    thisregion.set_cascadelevel(2)
    thisregion.set_isregular(True)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(9.734555707871914)
    thisregion.set_right(11.694403323531152)
    thisregion.set_value(11.438771025836468)
    thisregion.set_frequency(0.1991869918699187)
    thisregion.set_cascadelevel(3)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(4.536698988080025)
    thisregion.set_right(9.734555707871914)
    thisregion.set_value(8.03034038990736)
    thisregion.set_frequency(0.02032520325203252)
    thisregion.set_cascadelevel(4)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    thisregion = fontregion()
    thisregion.set_left(0.7874252885580063)
    thisregion.set_right(4.536698988080025)
    thisregion.set_value(1.0430575862526894)
    thisregion.set_frequency(0.056910569105691054)
    thisregion.set_cascadelevel(5)
    thisregion.set_isregular(False)
    trueregions.append(thisregion)

    return trueregions

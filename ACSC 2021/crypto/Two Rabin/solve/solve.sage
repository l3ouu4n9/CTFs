from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from sage.matrix.matrix2 import Matrix


def resultant(f1, f2, var):
    return Matrix.determinant(f1.sylvester_matrix(f2, var))


flag1_len = 98
n = 105663510238670420757255989578978162666434740162415948750279893317701612062865075870926559751210244886747509597507458509604874043682717453885668881354391379276091832437791327382673554621542363370695590872213882821916016679451005257003326444660295787578301365987666679013861017982035560204259777436442969488099
B = 12408624070212894491872051808326026233625878902991556747856160971787460076467522269639429595067604541456868927539680514190186916845592948405088662144279471
c1 = 47149257341850631803344907793040624016460864394802627848277699824692112650262968210121452299581667376809654259561510658416826163949830223407035750286554940980726936799838074413937433800942520987785496915219844827204556044437125649495753599550708106983195864758161432571740109614959841908745488347057154186396
c2 = 38096143360064857625836039270668052307251843760085437365614169441559213241186400206703536344838144000472263634954875924378598171294646491844012132284477949793329427432803416979432652621257006572714223359085436237334735438682570204741205174909769464683299442221434350777366303691294099640097749346031264625862
flag2_len = 98
hard_c1 = 73091191827823774495468908722773206641492423784400072752465168109870542883199959598717050676487545742986091081315652284268136739187215026022065778742525832001516743913783423994796457270286069750481789982702001563824813913547627820131760747156379815528428547155422785084878636818919308472977926622234822351389
hard_c2 = 21303605284622657693928572452692917426184397648451262767916068031147685805357948196368866787751567262515163804299565902544134567172298465831142768549321228087238170761793574794991881327590118848547031077305045920819173332543516073028600540903504720606513570298252979409711977771956104783864344110894347670094


def pgcd(g1, g2):
    while g2:
        g1, g2 = g2, g1 % g2
    return g1.monic()


def solve1():
    k = bytes_to_long(pad(b"a" * flag1_len, 128)[flag1_len:])
    P = PolynomialRing(Zmod(n), "m1")
    m1 = P.gen()
    m2 = m1 * 2 ^ 240 + k
    f1 = m1 * (m1 + B) - c1
    f2 = m2 * (m2 + B) - c2

    g = pgcd(f1, f2)
    return long_to_bytes(-g.coefficients()[0])


def solve2():
    global t, x, m1, m2, f1, f2, g
    P = PolynomialRing(Zmod(n), "m1,x")
    m1, x = P.gens()
    m2 = m1 + x
    f1 = m1 * (m1 + B) - hard_c1
    f2 = m2 * (m2 + B) - hard_c2
    f = resultant(f1, f2, m1).univariate_polynomial()
    x = f.small_roots(X=2 ^ 240, epsilon=0.03)[1]

    P = PolynomialRing(Zmod(n), "m1")
    m1 = P.gen()
    m2 = m1 + x
    f1 = m1 * (m1 + B) - hard_c1
    f2 = m2 * (m2 + B) - hard_c2
    g = pgcd(f1, f2)
    return long_to_bytes(-g.coefficients()[0] >> 240)


print(solve1() + solve2())
# b'ACSC{Rabin_cryptosystem_was_published_in_January_1979_ed82c25b173f38624f7ba16247c31d04ca22d8652da4a1d701b0966ffa10a4d1_ec0c177f446964ca9595c187869312b2c0929671ca9b7f0a27e01621c90a9ac255_wow_GJ!!!}'
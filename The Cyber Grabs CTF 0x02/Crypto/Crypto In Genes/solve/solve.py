#!/usr/bin/python

from Crypto.Util.number import *
import binascii
import sympy
e = 4

n1 = 692702922043276259906263941037401186733141625675576868571798384917935315544202330759457707479004810252459325034768198619014779900480707997634085533778147578653657665645962032018447555836139672993505990335298784212777716417980519653234745817723310882213924846668325241173823620448954178950839800152199858724082915293960369939130624374536162805818262540715541499220104124399214362464060979657870454002103757377647660747664042052809845245544965006385467174367842460655042968960207082153766550393150729629412512217334036496815197998642885897516201922192194363968824782559173741616437855428311356171154571965225361838851591351272207206609790514774390700514911364046218560181172432858463829518042027648402101379949281692849249108651488116294430113117921458139664744596879343296244850605648651746908478877617579212790956890347430218572544191370155921764494430675368049305860252532855850227689308630560492199757050905480209238485818030933767516562349131086728882844487057919224383881784668330112202168429352345660098952524270821148131360589603861177692391799498291026230379229304871550172801834982650834651926428205507676264359624559894080471025627584445221836308854382855318775534018708623930574488786523653012564177593889637523508731906513
n2 = 750938775489164486891216849757683849998722482726786455316218745858782413408803024459356885289128396646920606055950611202262957405206036467742385161404945756454290778431291516117996721290788521267911828478990472754627194191374133299526619521212966960641130605417468089468957762373873107444927602183362059701284168148847667392618540193577589092314716768181220545009625590846414439474266179648039871610552488963125785829767477294399841335725782567060148437418923695637981342631127617764433030438632142164063609153669358659819100491696542035574411957295306307605137787966074183292321775733260444070974272001479899274634405728087514326189921561677317653936065336844477877653056967155233089544314937420783993018221300978937984579533777836317323444063226941675174354617529096521716519498882648840507506298670575544888580916026971486719266642427867608096308216337671066829865674792289998911862822116203621123916503522960393524279173522366731185956577831791360713862627617862383309857013014598757518471425857553600179536609201063908788472671918820216334015439532174201008257768491287288164938767671751080329760969320344470922951068834216765203585445750011903983930725322992235342895406163071778303814510897622261451784058814171849577355373677
n3 = 991903263345714502912347658341216313475511926180465898111347849896188569699893494932781061543813088194443196450636904785052308400860512053674190781828018614447128290916249524778883646744746931764768552569912006957166578934676647197151754427039760780153920449635198193629677203041736214227499344586588930810512807015272935330514075139237019666101907358032482838094969076612677608384510938155145611298149766839430524753664849679854572672426602441695885311753084818886930899215624987534576105383589423733421875671291942772200061859960007259289000293513481681946557830736474742635788398564067326197913244219592374897298079417938447056569169268181874224961794737244730426570836879114521324942850461754069803149319601492494987232303800360276029739917079319782204756609395052559948286415525405646796025243561028358944329210705098109761764370552798330162586699907859575084499711579529882345453487128626444734266582858538317829281802675974161404614064383260551907058882654702181930680321865664259728465639763175661194450975831392457111781760213396433986237388451477336638233480164829499943139934367604358100960590061570503659281107823342147112327515352080870130939733847367303498437960554775431096433183128873642054243119889151868804299614377

c1 = 372481517139015447540979668357575927057676783926957745711445356823047090958311776655519878016801301475514214865702779554289110283325653393982081197194092914725390490228591243303515926586774778293587076242281366245720831684540942456497498842237298336661363294406337288984146357296222832853385889236567600435150936330329621177117724069780814790699582830089496266527626008405388323542939563220419129982548670474670527734210810531507627117610406125817646142320605793922856933301160432099379965700764532505569291256418743762195707879820302476487474143654958919703046181377544583621488836637888457144809107786748871930461363895689923043200718513692543580696861371997520367571339640855464614925744539657038832060348781247779482864192344198258265296601062320671921648169901952882957673776558586837888096773647659683489270311367038002184790443756405977487522377096912071096067703308372130699186500631048803394201787416838528758928503163878696792847414230330552728817197040135940839747833309125648587594594087937543491508730080596903392911620971918472111268469448652002278874642019624454235414674041105207579601447654556870495387234467700463612998869336187622585867025775418667437758707478570842198721642993339573929699125254227502232495543884
c2 = 72538765779659742476126854921183100131803435877182395508470049959784008306205763571390572307620685566601476624665409657461377837520609889951785518177225338757535266201118291551745471232114577309378736940867947338522353970427991879244758304981304087429828476495310338103734207346901264049858484906234656996324295308071302675060823095020046913430706969053198047677829698387637556169436906011662552790420232038232070617096576646343744364507197741309792935815564843628318625835886945230327895877488918163595088521002472923617208067248769309372687274849332618193416498260948669000999198532174510098471758161438505942268176890634929964815834693546156199292845794826675809089893832223535805633670213407406996196633156750942442929843242362207598898589730446638053877163437054430837246375044517216578401296714592777874891913291412532524467857895023412724299749254225723408908948949230981823700713457747477729348620831415874984529285959748163219385761301431767021296894099479911440552509178334219931154171174979941867132431537241948438374405390271740218046451006347669013748248958741294389451582694815368583333091435718695733434949289915392260810183751122462893765477990769800869059375567882349982923396086110293046252868205210189437209904350
c3 = 215466543055247719556283404874151411763279968775340780393909900446509344154126970808933875107837972096501032489316445420625176702280098880565472739874263396386008186463937602135916130646435246603084579414343176151529169746864562689279140379355660436830777808300538785359153700700987083741288800637114662838384022573774421381740158310321655580672739546056582212935151503105778704703637540414433518109782261455205670485443329501171287554166092462162660646250181138749969193912764269777607150891545620702953618443179868809076277717616890879938864185781202476239788999281316363542978825537587989525929641372849354459983445919826231378298345471152422081753767672399655051775017996734029618876617971629502475926600962167666747342191375941348682235284940741134039466928231522207489202153781162899175233399012762809488279967440960065869096721499645015041517393212956430705634982688717775154184190440206320674223687280866153815369442560883483033081872471529592523625263523381994333858488392154498546556701857575028289296077238482527949432480309022895244065515968689834222272196954558755347041075486911104347359459504681050021304835356326459881591717493273344179377496641863311457416877227830456177383905093835136522491397171011779372481279432
                                                                             
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod / n_i
       
        sum += a_i * inverse(p, n_i) * p
       
    return sum % prod 
 
x = chinese_remainder([n1, n2, n3], [c1, c2, c3])

 
m = pow(sympy.E,  sympy.ln(x) / e )
 

 
print ""
 

 
try:
    print hex(int(m))[2:-1].decode('hex')
except:
    print "Supposedly odd length string..."
    print str("0"+ hex( int(m))[2:-1]).decode('hex')


# I have Crypto in my genes did you also have If yes Prove M3 one more time CGTCATGCTCTGCGACACGTCTAGTCGCTATCGACTAGAGCATAGTCGCATATCTCTGACTCGATGACGTGAGCGATGAGCGCTAGCTGATCGATGAGCGATATACATCTGTCTGTAGACAGATAGACAGAGTCGATGCTCTCAGTGCATCTGACTGCTCACTAGTCTACGCTCTGTCACTACGCTAGACTGCTAGCATGACGACGAGACGAGTACGTGCGTCGTACGTACGTACGTACGTACGTGCGCT
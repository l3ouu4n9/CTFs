#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes, inverse

n_1 = 18313667803478867336609004721464541537328973484305462826796382793855753159667702339443214415676107219128019719918729781240367765840170011546130583192904778311406642412055832301895834234050092458894891378245659415453668079516268277621821820816314253525389030994411875738859521385775378994318680298110895022910442167872459649446752807884859578440573460451717182770603357201261838877834565082113563029377616922987738400092690457439097525425733191455006127272117318175252557137776704423298751249687687982939242399995960217891670545776591917279437324424655966555374035972380565105603454122721599641307596329237684195317587

n_2 = 20194467459457647060586516996478370472351267218473917410062391619804366508155615598555934151439965040658239840971767337317396956926547783621869694734101324546348705982578129843495046800965472146299498824698092002656707267929600194580016819675385334043852783023251749457877096316831425135876783876607713235344100191162140401175616183217075255611260047339942560958156070307547443884997807476833178558920808584815204100121025788968550385803770908539890673979000205479656826535064665232908045866184941964720268186377486138453445647534884078844954199823059749774156922214595091852691529313493766002778666818883664405832403

n_3 = 28410407035821399633105602414308666083186296658943720122869492873011020714858272525924383333651592284428901214906611872460164447581815587883155804582069085992375163808745662275133491411336915996399762543519217523867565162464721135784726071214566835068379436095952306868321574023543552212709114558637219985795158790999008762464781584235742497782435874814916996914994622843458737648796476512273155699038887480170809464170867427859436811167822162365878701943537205202829629515767060354955288883378511576712085561459099352295975180411538002583505384685029771639657760193592641463091670959570110199839193007853012047792951

ct_1 = 4361068625491121585959284487341364298014917091167459186815285529598354735142456720602466259897053502006543584155650414108053083187715487460414552189153473176328972836654051104002438654670972840351138096724369732822616030793769716381154959736278166838792024300286881567007214354013293287163863182681969888796359513260199887574592768851482378233523702226160031879160962727499277063367162956148498154268271025542127905089334411348063974019724471911095717624141476012283069088544181538863919281957631181754200250370777952217187591480953121517810770662230820689692425877920149973485291740351240601042031554568416165653801

ct_2 = 7454119914503246454695225608366998910502362663575277057804461920278767763248677179908320434252341988720062910948247234833145541538721789767567216822524509307779250204983551429213791107932957166581434644890426988090302661172536864772938094552788386232242044947782405157429008368192073663951594129377676752306905041733416517122507652313240587554617250337508737466749142455332827859556080609592971327915921976414897414103328089640910405224692254001370474817181338600658683188149268215440111576616804026782469078580075278163035385301354208954742090806396419312598674668782737577467445931682124259183904307994197406247889

ct_3 = 475431757150415548038120878675026605258081422958849322189947529651864550511016854432752841608067858620795144603286556404827027829790131339932716728168413658428417455936312330389421287814427992302961543375036809563812960151703062899930161470602633031599828887098914730417799654684023064362771853376591221374617439483919394574339804160488928252982891682671342232959007865677713493662084854838321612782206385687329676060126776093320146302404930844788632687207893577657763961310494363939265885733023621969573701702862867184316968075660702024069750913111874157011920933780381567012981148057478008081618456449117864142394

ciphertexts = [(ct_1, n_1), (ct_2, n_2), (ct_3, n_3)]

def find_root(x,n=3):
    high = 1
    while(high ** n < x):
        high *= 2
    low = high // 2
    while(low < high):
        mid = (low + high) // 2
        if(low < mid and mid**n < x):
            low = mid
        elif(high > mid and mid ** n > x):
            high = mid
        else:
            return mid
    return mid + 1

def get_plaintext(ciphertexts):

    t0 = (ciphertexts[0][0] * (ciphertexts[1][1] * ciphertexts[2][1]) * inverse((ciphertexts[1][1] * ciphertexts[2][1]), ciphertexts[0][1]))
    t1 = (ciphertexts[1][0] * (ciphertexts[0][1] * ciphertexts[2][1]) * inverse((ciphertexts[0][1] * ciphertexts[2][1]), ciphertexts[1][1]))
    t2 = (ciphertexts[2][0] * (ciphertexts[0][1] * ciphertexts[1][1]) * inverse((ciphertexts[0][1] * ciphertexts[1][1]), ciphertexts[2][1]))
    
    c = (t0 + t1 + t2) % (ciphertexts[0][1] * ciphertexts[1][1] * ciphertexts[2][1])
    
    return find_root(c)

print(long_to_bytes(get_plaintext(ciphertexts)))

# That there is such a thing as raw, unalloyed, agendaless kindness. That it is possible to fall asleep during an anxiety attack. That concentrating on anything is very hard work. flag{infi_nite_jes_t}
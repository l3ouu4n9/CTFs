from Crypto.Util.number import long_to_bytes

n = 142793817321992828777925840162504083304079023834001118099549928854335392622287928254035247188624975743042449746066633491912316354241339908190889792327014012472372654378644158878787350693992259970146885854641856991605625756536504266728483088687985429310233421251081614258665472164668993082471923690196082829593
e1 = 82815162880874815458042429141267540989513396527359063805652845923737062346339641683097075730151688566721221542188377672708478777831586255213972947470222613130635483227797717393291856129771004300757155687587305350059401683671715424063527610425941387424425367153041852997937972925839362190900175155479532582934
c1 = 108072697038795075732704334514926058617161875495016327352871122917196026504758904760148391499245235850616838765611460630089577948665981247735905622903872682862860306107704253287284051312867625831877418240290183661755993649928399992531008191618616452091127799880839665225093055618092869662205901927957599941568
e2 = 84856171747859965508406237198459622554468224770252249975158471902036102010991476445962577679301719179079633469099994226630172251817358960347828156301869905575867853640850107406452911333646573296923235424617864473580743418995994067645338437540627399276292679100115018844287273293945121023787594592185295794983
c2 = 101960082023987498941061751761131381167414505957511290567652602520714324823481487410890478130601013005035303795327512367595187718926017321227779179404306882163521882309833982882201152721855538832465833869251505131262098978117904455226014402089126682222497271578420753565370375178303927777655414023662528363360
 

M = 2**512

B = Matrix(ZZ, [
    [M, M, -n],
    [0, M, e1],
    [0, 0, e2],
])

L = B.LLL()

v = Matrix(ZZ, L[0])
x = v * B**(-1)

d1, d2 = abs(x[0,1]), abs(x[0,2])

m1 = pow(c1, d1, n) * pow(c2, d2, n) % n
m2 = pow(c1, d2, n) * pow(c2, d1, n) % n

print(long_to_bytes(m1))
print(long_to_bytes(m2))
"""Independent checks for the integrated design parts and five general cases.

Selected numerical and physical claims are checked, not every qualitative argument.
All modeled quantities and records are hypothetical or synthetic.
"""
from pathlib import Path
import json,math,re
import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.stats import chi2

ROOT=Path(__file__).resolve().parents[1]
records=[]
def check(label,actual,expected,tol=1e-6):
    actual=np.asarray(actual);expected=np.asarray(expected)
    ok=bool(np.allclose(actual,expected,rtol=tol,atol=tol))
    records.append({'check':label,'passed':ok,'max_error':float(np.max(np.abs(actual-expected)))})
    assert ok,(label,actual,expected)

# Structural contracts connect each statement to its answer and navigation.
for folder in sorted((ROOT/'laboratories').iterdir()):
    q=(folder/'exercises.tex').read_text(encoding='utf-8')
    a=(folder/'exercise-solutions.tex').read_text(encoding='utf-8')
    assert re.findall(r'\\task\{(\d+)\}',q)==list('12345'),folder
    assert re.findall(r'\\task\{(\d+)\}',a)==list('12345'),folder
    assert q.count(r'\item ')==a.count(r'\answer ')==15,folder
    assert 'figures/physical-system.tikz' in q and 'figures/system-diagram.tikz' in q
    assert not re.search(r'Question \d|Questions \d|ten original|Ten original',q+a)
general=ROOT/'problem-sets/integrated-design'
q=(general/'exercises.tex').read_text(encoding='utf-8')
a=(general/'solutions.tex').read_text(encoding='utf-8')
assert re.findall(r'\\task\{(\d+)\}',q)==list('12345')
assert q.count(r'\item ')==a.count(r'\answer ')==30

# Heat capacity, finite energy and nonzero initial states.
check('01.1(c) competing conductance bounds',[45/3,900/45],[15,20])
check('01.1(c) alternatives',[15*45,20*3],[675,60])
thermal=solve_ivp(lambda t,z:[(40-15*z[0])/900,15*z[0]],(0,60),[0,0],
                  rtol=1e-11,atol=1e-12)
check('01.3(c) integrated energy balance',900*thermal.y[0,-1]+thermal.y[1,-1],2400)
check('01.3(c) stored energy',900*thermal.y[0,-1],2400*(1-math.exp(-1)))
warm=solve_ivp(lambda t,z:[(30-15*(z[0]-2))/900,(z[0]-z[1])/12],
              (0,120),[1,0],rtol=1e-11,atol=1e-12,dense_output=True)
t=np.linspace(0,120,61)
check('01.5(c) warm-start superposition',warm.sol(t),
      [4-3*np.exp(-t/60),4-15/4*np.exp(-t/60)-1/4*np.exp(-t/12)])

# Bilinear mixing: exact equilibrium versus linearization.
for eps in [.1,1.]:
    exact=120/(1+eps);linear=120*(1-eps)
    check(f'02.2(c) relative change error eps={eps}',abs(exact-linear)/exact,eps**2)
check('02.3(c) worst-source required flow',396/100,3.96)
check('02.3(c) robust concentration limits',np.array([324,396])/3.96,[81.818181818,100])
check('02.4(c) feasible feedback flow',.025*math.sqrt(16800),3.240370349)
check('02.5(c) liquid inventory',np.array([360,120])/3,[120,40])

# Base-excitation energy: compare differential energy to boundary-work identity.
for x,v,z,zd in [(0.002,.1,.001,.03),(-.01,-.2,.004,.4)]:
    acc=(-25.6*(v-zd)-3200*(x-z))/8
    derivative=8*v*acc+3200*(x-z)*(v-zd)
    power=-25.6*(v-zd)**2-(25.6*(v-zd)+3200*(x-z))*zd
    check('03.5(c) moving-boundary power identity',derivative,power)
check('03.4(c) incompatible frequency bounds',[math.sqrt(9.81/.003),40/math.sqrt(2)],
      [57.18391382,28.28427125])

# RLC energy and finite winding resistance.
check('04.3(c) winding-resistance boundary',(10/19)/(10+10/19),.05)
lower=(-10+math.sqrt(10**2+4*.01/.0001))/(2*.01)
upper=(10+math.sqrt(10**2+4*.01/.0001))/(2*.01)
check('04.4(b) edge identities',[math.sqrt(lower*upper),upper-lower],[1000,1000])

# Independent frequency crossings and pole geometry for the redesigned constraint.
R_design=.01*800
notch_mag=lambda w:abs((1-.01*.0001*w*w)/(1-.01*.0001*w*w+1j*R_design*.0001*w))
w_lo=brentq(lambda w:notch_mag(w)-1/math.sqrt(2),1e-6,999.)
w_hi=brentq(lambda w:notch_mag(w)-1/math.sqrt(2),1001.,10000.)
pole=np.roots([.01*.0001,R_design*.0001,1])[0]
check('04.4(c) requested bandwidth and resulting damping',
      [w_hi-w_lo,-pole.real/abs(pole)],[800,.4])

for t in [0,.0007,.002]:
    i=.2*math.cos(1000*t);v=2*math.sin(1000*t)
    check('04.2(c) total reactive energy',.5*.01*i*i+.5*.0001*v*v,.0002)
for i,v,u in [(.2,1,3),(-.3,2,-1)]:
    di=(u-10*i-v)/.01;dv=i/.0001
    check('04.5(c) port energy balance',.01*i*di+.0001*v*dv,u*i-10*i*i)

# Motor power and dynamic load-estimator bias.
omega=2.8;current=(.02*omega+.03)/.1
check('05.2(c) voltage-limited current',current,.86)
check('05.2(c) voltage-limited power',2*current,2*current**2+.02*omega**2+.03*omega)
check('05.4(c) coefficient reserve',.8*(51+102*.8),106.08)
for V,i,w,load in [(2,.3,1,.03),(1,-.1,-2,.02)]:
    di=(V-2*i-.1*w)/.02;dw=(.1*i-.02*w-load)/.01
    estimate=.05*V-.025*w
    check('05.5(c) dynamic estimator bias',estimate-load,.001*di+.01*dw)

# Root locus and time-scaled cancellation.
sb=(-8+2*math.sqrt(7))/3
check('06.2(c) remaining pole at breakaway',-8-2*sb,(-8-4*math.sqrt(7))/3)
check('06.4(c) symmetric gain uncertainty lower bound',84*(1-1/21),80)
check('06.5(c) scaled compensated boundary',960*.5**3,120)
check('06.5(c) factorization at boundary',
      np.polymul([1,8],[1,0,15]),[1,8,15,120])

# Exact loop magnitudes independently determine the new sensor crossover.
wc=math.sqrt((-9+math.sqrt(337))/2)
pm=math.pi/2-math.atan(wc/3)
check('07.2(c) remaining delay budget',(pm-math.pi/6)/wc-.19,.005328715)
ws=brentq(lambda w:abs(8/(1j*w*(1j*w+3)*(1+.1j*w)))-1,.1,4)
pms=math.pi/2-math.atan(ws/3)-math.atan(.1*ws)-.18*ws
check('07.4(c) sensor crossover and margin',[ws,math.degrees(pms)],[2.127567246,20.703065747])
assert 2*math.tan(pm/2)/wc>pm/wc
phi=math.atan(3)-math.radians(35)
alpha=(1-math.sin(phi))/(1+math.sin(phi));T=1/(3*math.sqrt(alpha))
K=3*math.sqrt(10*alpha);g=abs((1+3j/.006)/(1+3j/.03))
comp=lambda s:g*K*(1+T*s)/(1+alpha*T*s)*(1+s/.03)/(1+s/.006)
margin=180+np.angle(comp(3j)/(3j*(3j+1)),deg=True)
check('08.4(c) delayed retained margin',margin-math.degrees(.09*3),39.07179257)
check('08.5(c) high-frequency controller limit',abs(comp(1e10j)),g*K/(5*alpha))

check('08.1(c) omitted actuator lag at fixed crossover',
      [3*math.sqrt(10.9),90-math.degrees(math.atan(3)+math.atan(.3))],
      [9.9045444115,1.7357045889])

# Filter-state realization checked against the independently formed polynomial.
kp,ki,kd,tauf=25,24,7,.03
Af=np.array([[0,1,0,0],[-1-kp-kd/tauf,-2,kd/tauf,1],
             [1/tauf,0,-1/tauf,0],[-ki,0,0,0]])
check('09.2(c) filtered state characteristic polynomial',np.poly(Af),
      np.array([.03,1.06,9.78,26.72,24])/.03)
y,v,z,I=2,0,2,-20;requested=25*(3-y)+I-7*(y-z)/.03;u=2
check('09.3(c) saturated equilibrium derivatives',
      [v,-2*v-y+u,(y-z)/.03,24*(3-y)+8*(u-requested)],[0,0,0,0])
check('09.4(c) Euler local correction upper bounds',2/np.array([8,40]),[.25,.05])

# Physical thermal realization, integral augmentation and isolated observer bias.
A=np.array([[-.15,.05],[.05,-.10]]);B=np.array([[.1],[0]]);C=np.array([[0,1]])
physical=np.array([[-(1+.5)/10,.5/10],[.5/10,-(.5+.5)/10]])
check('10.1(c) thermal balance realization',physical,A)
Aa=np.block([[A,np.zeros((2,1))],[-C,np.zeros((1,1))]])
Ba=np.vstack([B,[[0.]]])
check('10.4(c) augmented controllability determinant',
      np.linalg.det(np.hstack([Ba,Aa@Ba,Aa@Aa@Ba])),-2.5e-6,tol=1e-12)
L=np.array([[11.1],[1.55]])
check('10.5(c) isolated observer bias',(-np.linalg.solve(A-L@C,L*.1)).ravel(),
      [.1484375,.0984375])

# Sampled PI: unit-circle frequency and exact intersample solution.
angle=math.acos((3*math.exp(-1.5)-1)/2)
check('11.3(c) marginal oscillation frequency',angle/.75,2.315817788)
for yk,uk in [(0,2),(2,-1)]:
    values=np.exp(-2*np.linspace(0,.5,51))*yk+(1-np.exp(-2*np.linspace(0,.5,51)))*uk
    assert min(values)>=min(values[0],values[-1])-1e-12
    assert max(values)<=max(values[0],values[-1])+1e-12

# Noise interval is conditional on a fixed perfect model and iid Gaussian errors.
check('12.3(c) conditional 95-percent RMSE interval',
      .015*np.sqrt(chi2.ppf([.025,.975],400)/400),[.01396052,.01603853])
check('12.4(c) robust reachable output',1.5*2-.2,2.8)
# Independent quadrature of a held input with a fractional delay.
h=.01;tau=4;theta=.604289;q=int(theta//h);delta=theta-q*h
aa=math.exp(-h/tau);bb=math.exp(-(h-delta)/tau)
for past,recent,yk in [(0,1,0),(-.6,1.1,.3)]:
    integrated=aa*yk+quad(lambda t:math.exp(-(h-t)/tau)*1.8*past/tau,0,delta)[0]
    integrated+=quad(lambda t:math.exp(-(h-t)/tau)*1.8*recent/tau,delta,h)[0]
    recurrence=aa*yk+1.8*((bb-aa)*past+(1-bb)*recent)
    check('12.5(c) fractional-delay exact update',recurrence,integrated,tol=1e-12)

# General case 1: nonlinear interacting tanks versus the analytic Jacobian.
areas=np.array([.02,.03]);k12=.004;k2=.003;qbar=.0012
def tank_rhs(h,inflow=qbar):
    cross=k12*np.sign(h[0]-h[1])*np.sqrt(abs(h[0]-h[1]))
    drain=k2*np.sqrt(h[1])
    return np.array([inflow-cross,cross-drain])/areas
eq=np.array([.25,.16]);check('G1(a) tank equilibrium',tank_rhs(eq),[0,0],tol=1e-12)
eps=1e-6
jac=np.column_stack([(tank_rhs(eq+eps*np.eye(2)[j])-tank_rhs(eq-eps*np.eye(2)[j]))/(2*eps) for j in range(2)])
At=np.array([[-1/3,1/3],[2/9,-25/72]]);Bt=np.array([[50],[0]])
check('G1(b) flow-law numerical Jacobian',jac,At)
check('G1(b) tank characteristic polynomial',np.poly(At),[1,49/72,1/24])
check('G1(b) tank DC gain',(-C@np.linalg.solve(At,Bt)).item(),800/3)
newq=.0013
nonlinear=solve_ivp(lambda t,h:tank_rhs(h,newq),(0,400),eq,rtol=1e-11,atol=1e-13)
check('G1(c) integrated nonlinear final height',nonlinear.y[1,-1],(newq/k2)**2)
exact=(newq/k2)**2-.16;local=800/3*.0001
check('G1(c) relative equilibrium-change error',(exact-local)/exact,.04)
A_pi=np.block([[At-Bt@C*.001,Bt*.0001],[-C,np.zeros((1,1))]])
check('G1(d) PI augmented polynomial',np.poly(A_pi),[1,49/72,1/24+1/90,1/900])
assert max(np.linalg.eigvals(A_pi).real)<0
check('G1(e) pump-limited level',(.0015/.003)**2,.25)
check('G1(e) required target inflow',.003*math.sqrt(.3),.001643167673)
check('G1(f) intertank flow reverses',int(tank_rhs([.16,.25])[0]>0),1)

# General cases 2--5: acceptance decisions and continuous/discrete distinctions.
def platform(zeta):
    w=40.;b=2*zeta*math.sqrt(8*3200)
    tr=(1j*b*w+3200)/(-8*w*w+1j*b*w+3200)
    return [abs(tr)*.5,abs(tr-1)*.5]
check('G2(b) nominal displacement and travel mm',platform(.08),[.174005,.662907],tol=2e-5)
check('G2(d) higher damping amplitudes mm',platform(.4),[.277471,.588235],tol=2e-5)
check('G3(c) full motor PI poles',np.sort(np.roots([.0002,.0204,.16,.3])),
      [-93.62653047,-5.41459798,-2.95887155])
check('G3(f) feasible steady command',.5*2+.6,1.6)
check('G4(c) ramp tracking error',1/(g*K),.041887,tol=1e-5)
check('G4(d) retained-margin delay limit',math.radians(margin-40)/3,.0845999)
Kf=np.array([[3,5.5]])
check('G5(b) feedback polynomial',np.poly(A-B@Kf),[1,.55,.07])
check('G5(d) disturbance offset',(-C@np.linalg.solve(A-B@Kf,[[0],[.01]])).item(),9/140)
sampled=[]
for h,expected in [(1,[.65653395,.81986179]),(10,[-1.716127,.13986156])]:
    Ad=expm(A*h);Bd=np.linalg.solve(A,(Ad-np.eye(2))@B)
    values=np.sort(np.linalg.eigvals(Ad-Bd@Kf).real)
    check(f'G5(e) held-feedback poles at {h} s',values,expected)
    sampled.append({'period':h,'eigenvalues':values.tolist()})
result={'laboratory_problems':60,'laboratory_parts':180,'general_problems':5,'general_parts':30,
        'checks':records,'numeric_checks':len(records),'passed':all(r['passed'] for r in records),
        'sampled_thermal_cases':sampled,
        'scope':'Selected integrated derivations, physical balances, feasibility and implementation claims; no experimental evidence.'}
(ROOT/'docs/integrated-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(f"{len(records)} integrated checks passed; 65 problems, 210 linked parts.")

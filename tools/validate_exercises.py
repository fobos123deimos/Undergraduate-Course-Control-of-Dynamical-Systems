"""Selected independent numerical checks for the derivations retained in the integrated problems.

These checks complement, rather than prove, the written derivations and qualitative
answers. No measured data are loaded or generated.
"""
from pathlib import Path
import json
import math
import re
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from scipy.optimize import minimize_scalar
from scipy.signal import cont2discrete, step, TransferFunction

ROOT=Path(__file__).resolve().parents[1]
exercise_map=json.loads((ROOT/'docs/exercise-map.json').read_text(encoding='utf-8'))
records=[]
def check(label,actual,expected,tolerance=1e-5):
    match=re.match(r"(\d+)\.(\d+)(.*)",label)
    if match:
        module,oldq=int(match[1]),int(match[2])
        entry=next(p for p in exercise_map["laboratories"][module-1]["problems"] if any(x["question"]==oldq for x in p["previous_original_questions"]))
        part=next(x["new_part"] for x in entry["previous_original_questions"] if x["question"]==oldq)
        label=f"{module:02d}.{entry['problem']}({part}){match[3]}"
    actual=np.asarray(actual)
    if np.iscomplexobj(actual):
        assert np.max(np.abs(actual.imag))<1e-10,(label,actual)
        actual=actual.real
    actual=actual.astype(float)
    expected=np.asarray(expected,dtype=float)
    error=float(np.max(np.abs(actual-expected)))
    ok=bool(np.allclose(actual,expected,rtol=tolerance,atol=tolerance))
    records.append({'check':label,'passed':ok,'maximum_absolute_error':error,
                    'actual':actual.tolist(),'expected':expected.tolist(),'tolerance':tolerance})
    if not ok: print('FAIL',label,actual,expected,flush=True)

folders=sorted((ROOT/'laboratories').iterdir())
assert len(folders)==12
for folder in folders:
    q=(folder/'exercises.tex').read_text(encoding='utf-8')
    a=(folder/'exercise-solutions.tex').read_text(encoding='utf-8')
    assert re.findall(r'\\task\{(\d+)\}',q)==list(map(str,range(1,6))),folder
    assert re.findall(r'\\task\{(\d+)\}',a)==list(map(str,range(1,6))),folder
    assert len(re.findall(r'\\answer\s',a))==15,folder
    assert not re.search(r'\bUFC\b|Wilkley|LAB_0|Lista_01',q+a),folder

# Thermal response: compare closed forms with integrated physical state equations.
tstar=15*math.log(5)
thermal=solve_ivp(lambda t,z:[(40-15*z[0])/900,(z[0]-z[1])/12],
                 (0,180),[0,0],rtol=1e-11,atol=1e-13,dense_output=True)
check('01.2 target time',thermal.sol(60*math.log(4))[0],2)
check('01.4 maximum sensor error',np.diff(thermal.sol(tstar))[0]*-1,(8/15)*5**(-.25))
opt=minimize_scalar(lambda t:-(thermal.sol(t)[0]-thermal.sol(t)[1]),bounds=(0,120),method='bounded')
check('01.4 critical time',opt.x,tstar)
check('01.6 cooling interval',60*math.log((16/3)*(1-math.exp(-1))),72.9180773)
nonzero=solve_ivp(lambda t,z:[(40-15*z[0])/900,(z[0]-z[1])/12],
                 (0,60),[1,0],rtol=1e-11,atol=1e-13)
check('01.9 nonzero initial response',nonzero.y[:,-1],
      [8/3-5/3*math.exp(-1),8/3-25/12*math.exp(-1)-7/12*math.exp(-5)])
check('01.10 inverse noise deviation',.02*math.sqrt(313),.35383612)

# Ventilation exact and local equilibria, feedback and positivity.
check('02.1 nominal equilibrium and time constant',[360/3,120/3],[120,40])
check('02.3 finite-step discrepancy',360/3.3-108,12/11)
check('02.4 threshold concentration',60+60*math.exp(-(20*math.log(4))/20),75)
check('02.5 constrained concentration',480/4,120)
check('02.6 uncertain equilibrium range',np.array([324,396])/3.6,[90,110])
check('02.7 local pole',-(3+120*.025)/120,-.05)
check('02.8 nonlinear equilibrium',math.sqrt(16800),129.614814)
check('02.9 PI poles',np.sort(np.roots([1,.05,.0004])),[-.04,-.01])
assert all(360/q+(c-360/q)*math.exp(-q*t/120)>=0
           for q in [.1,3,6] for c in [0,60,120] for t in [0,10,1000])

# Base excitation: evaluate complex transfer functions directly.
def trans(zeta,w,m=8,k=3200):
    b=2*zeta*math.sqrt(m*k)
    return (1j*b*w+k)/(-m*w*w+1j*b*w+k)
check('03.2 damping coefficients',2*np.array([.08,.4])*math.sqrt(8*3200),[25.6,128])
check('03.3 isolation boundary',[abs(trans(z,20*math.sqrt(2))) for z in [.08,.4]],[1,1])
check('03.4 resonance magnitudes',[abs(trans(z,20)) for z in [.08,.4]],[6.3295,1.6008],2e-5)
check('03.5 high-frequency magnitudes',[abs(trans(z,60)) for z in [.08,.4]],[.13841,.31130],1e-5)
check('03.6 relative travel mm',abs(trans(.08,40)-1)*.5,.66291)
check('03.7 payload ratios',[math.sqrt(3200/12),25.6/(2*math.sqrt(12*3200)),math.sqrt(6400/12)],
      [16.3299,.06532,23.0940],1e-5)
check('03.8 gravity requirements',[8*9.81/3200*1000,8*9.81/.003,math.sqrt(9.81/.003)],
      [24.525,26160,57.1839],1e-5)
delta=math.log(5/3)
check('03.9 decay-derived damper',16*delta/.32,25.541281)

# Passive notch: complex impedance versus pole/zero claims.
def notch(w,R=10,L=.01,C=.0001,rl=0):
    reactive=1j*w*L+1/(1j*w*C)
    return (rl+reactive)/(R+rl+reactive)
check('04.2 pole real parts',np.roots([1,1000,1e6]).real,[-500,-500])
check('04.3 resonance output',abs(notch(1000)),0)
check('04.3 reactive energies',[.5*.01*.2**2,.5*.0001*2**2],[.0002,.0002])
check('04.4 tolerance leakage',[abs(notch(1000,C=.00009)),abs(notch(1000,C=.00011))],[.1104315,.0905357])
check('04.6 reciprocal frequencies',[abs(notch(500)),abs(notch(2000))],[3/math.sqrt(13)]*2)
edges=1000*np.array([(math.sqrt(5)-1)/2,(math.sqrt(5)+1)/2])
check('04.7 half-power edges',[abs(notch(w)) for w in edges],[1/math.sqrt(2)]*2)
check('04.8 winding resistance',abs(notch(1000,rl=1)),1/11)
t=np.linspace(0,.025,501)
_,yy=step(TransferFunction([1,0,1e6],[1,1000,1e6]),T=t)
check('04.10 step response',yy,1-2/math.sqrt(3)*np.exp(-500*t)*np.sin(500*math.sqrt(3)*t))

# Motor: equilibria, power, state and stability checks.
check('05.2 actuator equilibrium',[2*1.3+.1*5,(2-.6)/.5],[3.1,2.8])
check('05.3 proportional balance',.8*(5-34/13),.5*(34/13)+.6)
check('05.4 PI equilibrium voltage',.5*5+.6,3.1)
for ki,stable in [(1.6,True),(150,False)]:
    assert bool(np.max(np.roots([.0002,.0204,.13,.1*ki]).real)<0)==stable
check('05.5 gain boundary',.0204*.13/.00002,132.6)
Am=np.array([[-100,-5],[10,-2]]);Bm=np.array([[50],[0]])
check('05.7 controllability determinant',np.linalg.det(np.hstack([Bm,Am@Bm])),25000)
check('05.8 load channel DC',-40/(1+.8*2),-200/13)
check('05.9 power conservation',3.1*1.3,2*1.3**2+.02*5**2+.03*5)
check('05.10 load estimate',.05*3.1-.025*5,.03)

# Root locus: direct roots and gain stationarity.
for gain,stable in [(5,True),(24,True),(95,True),(97,False),(-1,False)]:
    assert bool(max(np.roots([1,8,12,gain]).real)<0)==stable
sb=(-8+2*math.sqrt(7))/3
check('06.4 breakaway derivative',3*sb**2+16*sb+12,0)
check('06.4 gain',-sb*(sb+2)*(sb+6),5.0490425)
check('06.5 marginal polynomial',np.polymul([1,8],[1,0,12]),[1,8,12,96])
check('06.5 period',2*math.pi/math.sqrt(12),1.81379936)
check('06.6 ramp error',12/24,.5)
check('06.8 time-scaled boundary',96*.5**3,12)

# Delay and compensation: complex frequency response and rational roots.
wc=math.sqrt((-9+math.sqrt(337))/2);pm=math.pi/2-math.atan(wc/3)
check('07.2 crossover magnitude',abs(8/(1j*wc*(1j*wc+3))),1)
check('07.3 delay boundary',pm/wc,.437393891)
check('07.4 30-degree budget',(pm-math.pi/6)/wc,.195328715)
check('07.6 first-order Pade phase error',(wc*.3-2*math.atan(wc*.3/2))*180/math.pi,1.22800141)
check('07.8 uncertain delay margin',(pm-.18*wc)*180/math.pi,31.8997423)
wc4=math.sqrt((-9+math.sqrt(145))/2)
check('07.9 lower-gain boundary',(math.pi/2-math.atan(wc4/3))/wc4,.957491641)
phi=math.atan(3)-math.radians(35)
alpha=(1-math.sin(phi))/(1+math.sin(phi));T=1/(3*math.sqrt(alpha));K=3*math.sqrt(10*alpha)
lead=lambda s:K*(T*s+1)/(alpha*T*s+1)
G=lambda s:1/(s*(s+1))
check('08.4 normalized crossover',abs(lead(3j)*G(3j)),1)
check('08.4 lead gain',K,4.7750,2e-5)
check('08.5 ramp error',1/K,.20942,1e-5)
lag=lambda s:(1+s/.03)/(1+s/.006)
g=1/abs(lag(3j))
check('08.6 low-frequency gain',g*K,23.8739,1e-5)
phase_margin=180+np.angle(g*lead(3j)*lag(3j)*G(3j),deg=True)
check('08.7 final margin',phase_margin,54.541653,1e-5)
assert max(np.roots([alpha*T,1+alpha*T,1+K*T,K]).real)<0
check('08.10 delay boundary',math.radians(phase_margin)/3,.3173105)
check('08.10 retained-margin budget',math.radians(phase_margin-40)/3,.0845999)

# PID filtering, saturation and anti-windup arithmetic.
check('09.1 desired polynomial',np.poly([-2,-3,-4]),[1,9,26,24])
den=np.polyadd(np.polymul([.03,1,0],[1,2,1]),np.polyadd(np.polymul([25,24],[.03,1]),[7,0,0]))
check('09.4 filtered polynomial',den,[.03,1.06,9.78,26.72,24])
assert max(np.roots(den).real)<0
check('09.4 quartic inequality sides',[1.06*9.78*26.72,.03*26.72**2+1.06**2*24],
      [277.000896,48.385152])
check('09.6 back-calculation cancellation',24+8*(2-5),0)
check('09.7 integral increments',[24*.4*2,(24*.4-8*.5)*2],[19.2,11.2])
check('09.8 recovery improvement percent',100*(1-1.841207/9.756216),81.12786,1e-5)
check('09.9 local correction scales',[1/8,1/40],[.125,.025])

# Observer design: matrix properties independently from coefficient matching.
A=np.array([[-.15,.05],[.05,-.10]]);B=np.array([[.1],[0]]);C=np.array([[0,1]])
K=np.array([[3,5.5]]);L=np.array([[11.1],[1.55]])
check('10.1 open-loop poles',np.sort(np.linalg.eigvals(A)),[-.180901699,-.069098301])
check('10.2 controllability',np.linalg.det(np.hstack([B,A@B])),.0005)
check('10.2 observability',np.linalg.det(np.vstack([C,C@A])),-.05)
check('10.3 feedback poles',np.sort(np.linalg.eigvals(A-B@K)),[-.35,-.2])
check('10.4 prefilter',(-1/(C@np.linalg.solve(A-B@K,B))).item(),14)
check('10.4 equilibrium',-np.linalg.solve(A-B@K,B*14).ravel(),[2,1])
check('10.5 observer poles',np.sort(np.linalg.eigvals(A-L@C)),[-1,-.8])
check('10.7 disturbance offset',(-C@np.linalg.solve(A-B@K,np.array([[0],[.01]]))).item(),9/140)
check('10.8 noise DC gain',(-C@np.linalg.solve(A-L@C,L)).item(),.984375)
check('10.9 constrained reference',2/2.5,.8)

# Sampled controller: exact discretization and Jury region.
Ad,Bd,_,_,_=cont2discrete((np.array([[-2]]),np.array([[2]]),np.eye(1),np.zeros((1,1))),.5)
check('11.1 exact held-input coefficients',[Ad.item(),Bd.item()],[math.exp(-1),1-math.exp(-1)])
def matrix(h):
    a=math.exp(-2*h);b=1-a
    return np.array([[a-2*b,b],[-4*h,1]])
periods=[.05,.5,1]
radii=[max(abs(np.linalg.eigvals(matrix(h)))) for h in periods]
check('11.6 spectral radii',radii,[.893907,.606531,1.365534],1e-5)
for h in np.linspace(.001,.749,100):
    assert max(abs(np.linalg.eigvals(matrix(h))))<1
for h in np.linspace(.751,2,100):
    assert max(abs(np.linalg.eigvals(matrix(h))))>1
check('11.5 boundary radii',abs(np.linalg.eigvals(matrix(.75))),[1,1])
check('11.7 decay rates',[-math.log(radii[i])/periods[i] for i in [0,1]],[2.243,1],5e-4)
for h in periods:check(f'11.8 equilibrium at {h}',matrix(h)@np.ones(2)+np.array([2*(1-math.exp(-2*h)),4*h]),[1,1])
a=math.exp(-1);b=1-a;changed=np.array([[a-4*b,b],[-2,1]])
assert max(abs(np.linalg.eigvals(changed)))>1

# Synthetic identification: timing, conservation and tuning formulas.
check('12.1 one-time-constant response',3.6*(1-math.exp(-(6.6-2.6)/4)),3.6*(1-math.exp(-1)))
check('12.5 multistep equilibrium',1.8*sum([1,-.6,1.1,-.8]),1.26)
check('12.6 noise MSE',.015**2,.000225)
check('12.7 nominal PI',[4/(1.8*2.6),1/(1.8*2.6)],[100/117,25/117])
check('12.7 uncertain-delay PI',[4/(1.8*2.9),1/(1.8*2.9)],[200/261,50/261])
check('12.8 required efforts',[1/1.8,1.2/1.8],[5/9,2/3])
assert round(.6/.01)==60
y=np.zeros(62);commands=np.ones(62);a=math.exp(-.01/4)
for k in range(61):y[k+1]=a*y[k]+(1-a)*1.8*(commands[k-60] if k>=60 else 0)
check('12.9 delayed onset before sample 61',y[:61],np.zeros(61))
assert y[61]>0

result={'laboratories':12,'problems_per_laboratory':5,'total_laboratory_problems':60,
        'general_problems':5,'numeric_checks':len(records),'passed':all(x['passed'] for x in records),
        'scope':'Selected numerical claims and structural counts; not a formal proof of every written argument.',
        'checks':records}
(ROOT/'docs/exercise-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(f"{len(records)} numerical checks; 60 integrated laboratory problems and their worked parts; passed={result['passed']}",flush=True)
assert result['passed'],'See docs/exercise-validation.json'

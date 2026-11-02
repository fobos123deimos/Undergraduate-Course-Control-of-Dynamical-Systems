function result = run_lesson(number)
% Original hypothetical scenarios. All generated records are synthetic.
if exist('OCTAVE_VERSION','builtin'); pkg('load','control'); end
result=struct(); figure; hold on;
switch number
case 1
    time=linspace(0,420,4201); tau=60; sensor=12;
    physical=40/15*(1-exp(-time/tau));
    measured=40/15*(1-(tau*exp(-time/tau)-sensor*exp(-time/sensor))/(tau-sensor));
    model=tf(1/15,conv([tau,1],[sensor,1]));
    calculated=step(40*model,time);
    assert(max(abs(calculated(:)-measured(:)))<1e-8);
    plot(time,physical,time,measured,'--');
    result.tau=tau; result.final_rise=40/15;
case 2
    volume=120; source=360; nominal_flow=3; initial=120;
    time=linspace(0,240,2401);
    for fraction=[.1,1]
        change=nominal_flow*fraction; final=source/(nominal_flow+change);
        exact=final+(initial-final)*exp(-(nominal_flow+change)*time/volume);
        linear=initial-initial/nominal_flow*change*(1-exp(-nominal_flow*time/volume));
        plot(time,exact,time,linear,'--');
    end
    result.exact_final=[source/3.3,source/6]; result.linear_final=[108,0];
case 3
    mass=8; stiffness=3200; angular=logspace(-1,3,1000); natural=sqrt(stiffness/mass);
    for ratio=[.08,.4]
        damping=2*ratio*sqrt(mass*stiffness);
        model=tf([damping,stiffness],[mass,damping,stiffness]);
        assert(abs(abs(frequency_value(model,sqrt(2)*natural))-1)<1e-10);
        values=squeeze(freqresp(model,angular)); semilogx(angular,20*log10(abs(values)));
    end
    result.isolation_threshold=sqrt(2)*natural;
case 4
    inductance=.01; capacitance=100e-6; resistance=10; angular=logspace(1,5,1600);
    result.notches=zeros(1,3); index=0;
    for factor=[.9,1,1.1]
        index=index+1; c=capacitance*factor;
        model=tf([inductance*c,0,1],[inductance*c,resistance*c,1]);
        notch=1/sqrt(inductance*c); assert(abs(frequency_value(model,notch))<1e-10);
        values=squeeze(freqresp(model,angular)); semilogx(angular,20*log10(max(abs(values),1e-8)));
        result.notches(index)=notch;
    end
case 5
    denominator=conv([.02,2],[.01,.02]); denominator(end)=denominator(end)+.01;
    voltage=tf(.1,denominator); disturbance=tf([-.02,-2],denominator);
    controllers={tf(.8,1),tf([.8,1.6],[1,0])}; time=linspace(0,18,9001); load=.03*(time>=4);
    result.final_speed=zeros(1,2);
    for index=1:2
        controller=controllers{index}; closed=feedback(controller*voltage,1);
        disturbed=minreal(disturbance/(1+controller*voltage));
        speed=step(5*closed,time)+lsim(disturbed,load,time);
        assert(max(real(pole(closed)))<0); plot(time,speed);
        result.final_speed(index)=speed(end);
    end
    assert(abs(result.final_speed(1)-6.8/2.6)<1e-5);
    assert(abs(result.final_speed(2)-5)<1e-4);
case 6
    plant=tf(1,[1,8,12,0]); time=linspace(0,20,6001);
    for gain=[12,60,100]
        model=feedback(gain*plant,1);
        assert((max(real(pole(model)))<0)==(gain<96)); plot(time,step(model,time));
    end
    result.stable_interval=[0,96]; result.endpoints_excluded=true;
case 7
    loop=tf(8,[1,3,0]); crossover=sqrt((-9+sqrt(337))/2);
    nominal_margin=90-atan(crossover/3)*180/pi; time=linspace(0,12,4001);
    result.delay_budget=nominal_margin*pi/180/crossover;
    result.phase_margins=[];
    for delay=[0,.1,.3]
        approximation=delay_approximation(delay,5);
        [unused,phase_margin]=margin(loop*approximation);
        exact=nominal_margin-crossover*delay*180/pi;
        assert(abs(phase_margin-exact)<.02);
        plot(time,step(feedback(loop*approximation,1),time));
        result.phase_margins(end+1)=exact;
    end
case 8
    plant=tf(1,[1,1,0]); crossover=3;
    phase=angle(frequency_value(plant,crossover))*180/pi;
    needed=(55-180-phase)*pi/180; alpha=(1-sin(needed))/(1+sin(needed));
    lead_time=1/(crossover*sqrt(alpha)); gain=sqrt(alpha)/abs(frequency_value(plant,crossover));
    lead=tf(gain*[lead_time,1],[alpha*lead_time,1]); lag=tf([1/.03,1],[1/.006,1]);
    scale=1/abs(frequency_value(lead*lag*plant,crossover));
    controllers={lead,scale*lead*lag}; time=linspace(0,160,16001);
    result.margins=zeros(1,2); result.velocity_constants=zeros(1,2);
    for index=1:2
        controller=controllers{index}; [unused,phase_margin]=margin(controller*plant);
        result.margins(index)=phase_margin; result.velocity_constants(index)=dcgain(controller);
        model=feedback(controller*plant,1); assert(max(real(pole(model)))<0);
        output=lsim(model,time,time); plot(time,time(:)-output(:));
    end
    assert(abs(result.margins(1)-55)<1e-5);
    assert(result.margins(2)>54 && result.margins(2)<55);
case 9
    options=odeset('RelTol',1e-8,'AbsTol',1e-10,'MaxStep',.01);
    result.recovery_iae=zeros(1,2); index=0;
    for antiwindup=[0,8]
        index=index+1;
        [first_time,first]=ode45(@(t,x) saturated_pid(x,3,antiwindup),linspace(0,6,3001),zeros(4,1),options);
        [second_time,second]=ode45(@(t,x) saturated_pid(x,.2,antiwindup),linspace(6,12,3001),first(end,:)',options);
        plot([first_time;second_time(2:end)],[first(:,1);second(2:end,1)]);
        result.recovery_iae(index)=trapz(second_time,abs(.2-second(:,1)));
    end
    assert(result.recovery_iae(2)<result.recovery_iae(1));
case 10
    A=[-.15,.05;.05,-.10]; B=[.1;0]; C=[0,1];
    assert(rank(ctrb(A,B))==2 && rank(obsv(A,C))==2);
    K=place(A,B,[-.2,-.35]); observer=place(A',C',[-.8,-1])';
    prefilter=-1/(C*((A-B*K)\B));
    augmented=[A-B*K,B*K;zeros(2),A-observer*C]; inputs=[B*prefilter;zeros(2,1)];
    time=linspace(0,80,4001);
    output=lsim(ss(augmented,inputs,eye(4),zeros(4,1)),ones(size(time)),time,[.6;-.4;.6;-.4]);
    assert(abs(output(end,2)-1)<1e-5 && norm(output(end,3:4))<1e-8);
    plot(time,output(:,1:2)); result.K=K; result.L=observer; result.prefilter=prefilter;
case 11
    result.radii=zeros(1,3); index=0;
    for period=[.05,.5,1]
        index=index+1; a=exp(-2*period); b=1-a;
        matrix=[a-2*b,b;-4*period,1]; state=zeros(2,1); time=0:period:16; output=zeros(size(time));
        for sample=1:numel(time)
            output(sample)=state(1); state=matrix*state+[2*b;4*period];
        end
        radius=max(abs(eig(matrix))); assert((radius<1)==(period<.75));
        result.radii(index)=radius; plot(time,output,'.-');
    end
    result.first_boundary=.75;
case 12
    rng(2026,'twister'); time=0:.05:30; truth=[1.8,4,.6];
    training=delayed_step(time,truth,2,2)+.015*randn(size(time));
    objective=@(transformed) sum((delayed_step(time,exp(transformed),2,2)-training).^2);
    fitted=exp(fminsearch(objective,log([1,2,.2]),optimset('Display','off','MaxIter',2000,'TolX',1e-9,'TolFun',1e-10)));
    assert(all(abs(fitted-truth)./truth<.08));
    validation=zeros(size(time)); prediction=zeros(size(time));
    changes=[1,1;8,-.6;15,1.1;22,-.8];
    for index=1:4
        validation=validation+delayed_step(time,truth,changes(index,2),changes(index,1));
        prediction=prediction+delayed_step(time,fitted,changes(index,2),changes(index,1));
    end
    validation=validation+.015*randn(size(time)); rmse=sqrt(mean((prediction-validation).^2)); assert(rmse<.03);
    kp=fitted(2)/(fitted(1)*(2+fitted(3))); ki=kp/fitted(2);
    dt=.01; clock=0:dt:35; output=zeros(size(clock)); effort=zeros(size(clock)); integral=0; a=exp(-dt/4); lag=60;
    for sample=1:numel(clock)-1
        error_signal=1-output(sample); request=kp*error_signal+integral; effort(sample)=min(max(request,0),2);
        integral=integral+dt*(ki*error_signal+2*(effort(sample)-request));
        delayed=0; if sample>lag; delayed=effort(sample-lag); end
        disturbance=0; if clock(sample)>=15; disturbance=-.2; end
        output(sample+1)=a*output(sample)+(1-a)*(1.8*delayed+disturbance);
    end
    assert(abs(output(end)-1)<.01); plot(clock,output);
    result.estimated=fitted; result.validation_rmse=rmse; result.Kp=kp; result.Ki=ki;
otherwise
    error('Lesson number must be between 1 and 12.');
end
grid on; title(sprintf('Original lesson %02d - synthetic computation',number));
if any(number==[3,4]); xlabel('Angular frequency (rad/s)'); ylabel('Gain (dB)'); else; xlabel('Time (scenario units)'); ylabel('Scenario output'); end
fprintf('Lesson %02d completed.\n',number); disp(result);
end

function value=frequency_value(model,angular)
value=squeeze(freqresp(model,angular));
end

function model=delay_approximation(delay,order)
if delay==0; model=tf(1,1); return; end
coefficients=zeros(1,order+1);
for k=0:order
    coefficients(k+1)=factorial(2*order-k)*factorial(order)/(factorial(2*order)*factorial(k)*factorial(order-k))*delay^k;
end
model=tf(fliplr(coefficients.*((-1).^(0:order))),fliplr(coefficients));
end

function derivative=saturated_pid(state,reference,antiwindup)
error_signal=reference-state(1);
request=25*error_signal+state(3)-7*(state(1)-state(4))/.03;
effort=min(max(request,-2),2);
derivative=[state(2);effort-2*state(2)-state(1);24*error_signal+antiwindup*(effort-request);(state(1)-state(4))/.03];
end

function output=delayed_step(time,parameters,amplitude,start)
elapsed=max(time-start-parameters(3),0);
output=amplitude*parameters(1)*(1-exp(-elapsed/parameters(2)));
end

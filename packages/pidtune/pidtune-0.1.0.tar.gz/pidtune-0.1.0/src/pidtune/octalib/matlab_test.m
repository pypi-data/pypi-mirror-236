                % Run on execution start
version_info=ver("MATLAB");

ver("control")
ver("optim")
ver("symbolic")
unix("which python")

try
  if (version_info.Name=="MATLAB")
    fprintf("Running on Matlab\n")
  end
catch ME
  fprintf("Running on Octave\n")
  %% Octave load packages
  pkg load control
  pkg load symbolic
  pkg load optim
end

fprintf("Running initial module\n")

%clc;
clear;

%% Define
s=tf('s');

file_json_id = fopen("/tmp/tmpch7aylre/results.json", "wt");
fid=fopen("/tmp/tmpch7aylre/model_vs_initial_step_response.csv",'wt');

%% Global variables definition
global To vo Lo Ko ynorm unorm tnorm long tin tmax tu

%% Load data from thread cache
in_v1=[0.0; 0.1; 0.2; 0.3; 0.4; 0.5; 0.6; 0.7; 0.8; 0.9; 1.0; 1.1; 1.2; 1.3; 1.4; 1.5; 1.6; 1.7; 1.8; 1.9; 2.0; 2.1; 2.2; 2.3; 2.4; 2.5; 2.6; 2.7; 2.8; 2.9; 3.0; 3.1; 3.2; 3.3; 3.4; 3.5; 3.6; 3.7; 3.8; 3.9; 4.0; 4.1; 4.2; 4.3; 4.4; 4.5; 4.6; 4.7; 4.8; 4.9; 5.0; 5.1; 5.2; 5.3; 5.4; 5.5; 5.6; 5.7; 5.8; 5.9; 6.0; 6.1; 6.2; 6.3; 6.4; 6.5; 6.6; 6.7; 6.8; 6.9; 7.0; 7.1; 7.2; 7.3; 7.4; 7.5; 7.6; 7.7; 7.8; 7.9; 8.0; 8.1; 8.2; 8.3; 8.4; 8.5; 8.6; 8.7; 8.8; 8.9; 9.0; 9.1; 9.2; 9.3; 9.4; 9.5; 9.6; 9.7; 9.8; 9.9; 10.0; 10.1; 10.2; 10.3; 10.4; 10.5; 10.6; 10.7; 10.8; 10.9; 11.0; 11.1; 11.2; 11.3; 11.4; 11.5; 11.6; 11.7; 11.8; 11.9; 12.0; 12.1; 12.2; 12.3; 12.4; 12.5; 12.6; 12.7; 12.8; 12.9; 13.0; 13.1; 13.2; 13.3; 13.4; 13.5; 13.6; 13.7; 13.8; 13.9; 14.0; 14.1; 14.2; 14.3; 14.4; 14.5; 14.6; 14.7; 14.8; 14.9; 15.0; 15.1; 15.2; 15.3; 15.4; 15.5; 15.6; 15.7; 15.8; 15.9; 16.0; 16.1; 16.2; 16.3; 16.4; 16.5; 16.6; 16.7; 16.8; 16.9; 17.0; 17.1; 17.2; 17.3; 17.4; 17.5; 17.6; 17.7; 17.8; 17.9; 18.0; 18.1; 18.2; 18.3; 18.4; 18.5; 18.6; 18.7; 18.8; 18.9; 19.0; 19.1; 19.2; 19.3; 19.4; 19.5; 19.6; 19.7; 19.8; 19.9; 20.0; 20.1; 20.2; 20.3; 20.4; 20.5; 20.6; 20.7; 20.8; 20.9; 21.0; 21.1; 21.2; 21.3; 21.4; 21.5; 21.6; 21.7; 21.8; 21.9; 22.0; 22.1; 22.2; 22.3; 22.4; 22.5; 22.6; 22.7; 22.8; 22.9; 23.0; 23.1; 23.2; 23.3; 23.4; 23.5; 23.6; 23.7; 23.8; 23.9; 24.0; 24.1; 24.2; 24.3; 24.4; 24.5; 24.6; 24.7; 24.8; 24.9; 25.0; 25.1; 25.2; 25.3; 25.4; 25.5; 25.6; 25.7; 25.8; 25.9; 26.0; 26.1; 26.2; 26.3; 26.4; 26.5; 26.6; 26.7; 26.8; 26.9; 27.0; 27.1; 27.2; 27.3; 27.4; 27.5; 27.6; 27.7; 27.8; 27.9; 28.0; 28.1; 28.2; 28.3; 28.4; 28.5; 28.6; 28.7; 28.8; 28.9; 29.0; 29.1; 29.2; 29.3; 29.4; 29.5; 29.6; 29.7; 29.8; 29.9; 30.0];                                % time vector
in_v2=[50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 50.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0; 75.0];                                % control signal vector
in_v3=[60.520983; 60.280331; 60.033577; 60.157243; 59.68851; 60.758538; 60.026412; 60.803675; 60.118095; 60.389824; 59.353252; 59.686429; 60.55722; 59.714241; 60.258199; 59.83899; 59.939368; 59.396557; 59.431838; 60.440313; 59.979929; 59.642701; 59.657804; 60.38538; 59.974855; 60.229634; 60.177401; 60.338191; 60.179103; 59.400116; 60.167723; 60.503188; 60.325858; 58.93677; 59.877561; 59.855577; 60.142209; 59.771397; 59.999087; 60.718454; 60.37908; 60.119898; 59.587003; 59.968472; 60.066139; 59.75086; 59.849421; 60.185695; 60.696675; 58.906876; 59.508872; 60.502063; 60.26013; 59.878647; 60.185232; 59.562706; 59.543177; 60.142046; 60.67795; 60.334986; 59.772592; 60.395223; 59.887783; 59.673027; 59.797374; 59.720205; 59.897769; 60.238509; 59.505606; 60.131058; 60.47063; 60.018361; 60.2498; 59.892131; 60.794066; 60.275409; 59.015857; 59.801463; 58.928933; 60.141121; 59.793201; 59.829; 59.850552; 60.149418; 59.117692; 59.082876; 59.291087; 59.311799; 58.221394; 58.306518; 58.3889; 57.065282; 58.484211; 57.283179; 58.019741; 56.899562; 57.268282; 57.070257; 56.329669; 56.35129; 55.720744; 55.690579; 54.604446; 54.408505; 54.992558; 53.704752; 53.695537; 52.47739; 52.595932; 52.010789; 51.810188; 51.929521; 51.488946; 51.128141; 50.224514; 49.920911; 48.766397; 48.574985; 48.880928; 48.249689; 47.578398; 46.358905; 46.597222; 46.163155; 45.346211; 45.199388; 45.760579; 43.956408; 42.993022; 42.076468; 42.492577; 42.098107; 41.449292; 42.462144; 41.572413; 41.032267; 40.520786; 38.655971; 40.310112; 39.191957; 38.407381; 37.532003; 38.137828; 38.687477; 37.581938; 37.470096; 36.690764; 36.924373; 35.478924; 36.300829; 35.820285; 35.226605; 35.13048; 35.493619; 34.545733; 34.68606; 33.472481; 34.355276; 34.419884; 33.134055; 32.739114; 32.564604; 33.113458; 32.28231; 32.40226; 31.64715; 32.574589; 31.61735; 32.19785; 32.003067; 31.450061; 31.526076; 31.120026; 30.977531; 31.538847; 30.93221; 30.315629; 31.40502; 30.137657; 30.702081; 30.046092; 30.199087; 30.434971; 30.648894; 29.952956; 30.185167; 29.868504; 29.910865; 29.309161; 29.725447; 30.394297; 29.302252; 29.044691; 30.282972; 30.055327; 29.842682; 28.796601; 30.106797; 29.10772; 28.798775; 28.992924; 29.435292; 29.538119; 29.314621; 29.073554; 29.972462; 28.854996; 29.168981; 28.77708; 29.266568; 28.195742; 29.336625; 28.531224; 28.962124; 28.519003; 28.424692; 28.120142; 28.516835; 29.035021; 29.149443; 29.609945; 29.196321; 27.937576; 28.429241; 28.81756; 27.742915; 28.725404; 28.59282; 29.000249; 29.095284; 29.241897; 28.744062; 28.724157; 29.472195; 29.640306; 28.643579; 28.880105; 28.375517; 28.820656; 29.14227; 28.530895; 28.852045; 28.806661; 28.509017; 28.544525; 29.624354; 28.332512; 28.556953; 28.104727; 28.733044; 28.95148; 28.536759; 28.925121; 28.446184; 29.335515; 28.753184; 29.114054; 29.740112; 28.959778; 29.359339; 28.874476; 28.622533; 28.347843; 28.587837; 29.277205; 29.144354; 28.295318; 28.671346; 28.175752; 28.893647; 29.189439; 28.42147; 27.504875; 29.066523; 30.188772; 28.993996; 28.887465; 28.880749; 29.182641; 29.686828; 29.434864; 28.665476; 28.760326; 28.862594; 28.370122; 29.269879; 28.824364; 29.448161; 28.665139; 29.490061; 27.902307; 29.566422; 28.072213; 28.281127; 28.773427; 28.100437; 28.959594; 28.994808; 29.341284; 28.569866; 28.937852];                                % controled variable vector

                long=length(in_v3);                              % define the default length
m_long=floor(long/2);

%% Infer vectors
mid_line_v1 = abs((in_v1(end)-in_v1(1))/2);
mid_line_v2 = abs((in_v2(end)-in_v2(1))/2);
mid_line_v3 = abs((in_v3(end)-in_v3(1))/2);

diff_v1 = diff(in_v1(m_long:end))/mid_line_v1;
diff_v2 = diff(in_v2(m_long:end))/mid_line_v2;
diff_v3 = diff(in_v3(m_long:end))/mid_line_v3;

mean_v1 = mean(abs(diff_v1));
mean_v2 = mean(abs(diff_v2));
mean_v3 = mean(abs(diff_v3));

%% Find u(s) in signals columns
u_v1=false;
u_v2=false;
u_v3=false;

if max(diff_v1) < mean_v2 && max(diff_v1) < mean_v3
    fprintf('\tu(s) is vector 1\n');
    u_v1=true;
    u = in_v1;
elseif max(diff_v2) < mean_v1 && max(diff_v2) < mean_v3
    fprintf('\tu(s) is vector 2\n');
    u_v2=true;
    u = in_v2;
else
    fprintf('\tu(s) is vector 3\n');
    u_v3=true;
    u = in_v3;
end

%% Find t(s) in signals columns
t_v1=false;
t_v2=false;
t_v3=false;

if ~u_v1 && min(diff_v1) > min(diff_v2) && min(diff_v1) > min(diff_v3)
    fprintf('\tt(s) is vector 1\n');
    t_v1=true;
    t = in_v1;
elseif ~u_v2 && min(diff_v2) > min(diff_v1) && min(diff_v2) > min(diff_v3)
    fprintf('\tt(s) is vector 2\n');
    t_v2=true;
    t = in_v2;
else
    fprintf('\tt(s) is vector 3\n');
    t_v3=true;
    t = in_v3;
end

%% Find y(s) in signals columns

if ~u_v1 && ~t_v1
    fprintf('\ty(s) is vector 1\n');
    y = in_v1;
elseif ~u_v2 && ~t_v2
    fprintf('\ty(s) is vector 2\n');
    y = in_v2;
else
    fprintf('\ty(s) is vector 3\n');
    y = in_v3;
end

%% FIXME, fixed definitions
t = in_v1;
u = in_v2;
y = in_v3;%% Main execution
% The next program is able to generate the fractional model parameters
% compute previous variables and then get the final constants

fprintf('Optimal model is in process...\n')

%% Static gain processing
% Vectors in file need to keep same lenght
sample=7;                        % Get noise avernage value
Uo=mean(u(1:sample));            %
Uf=mean(u(long-sample+1:long));  %
Yo=mean(y(1:sample));            % Clean noise
Yf=mean(y(long-sample+1:long));
Ko=(Yf-Yo)/(Uf-Uo);              % Get controled process gain

% Parameters normalization

ynorm=(y-Yo)./(Yf-Yo);       % Controlled variable vector with normalized values
unorm=(u-Uo)./(Uf-Uo);       % Control signal vector with normalized values
tnorm=t-min(t);              % Normalized time vector
ymax=max(ynorm);             % Sampling from non zero 't'

% Get_step_time rutine
cont=1;
flagtin=0;
% Flag variable
while cont<long
    if unorm(cont+1)>unorm(cont) || unorm(cont+1)<unorm(cont)
        tin=tnorm(cont);
        flagtin=cont;        % Obtain the tin position in data vector
        cont=long;
    else
        cont=cont+1;
    end
end

fprintf('Check 0\n')
%% Initial values computation
% Default data for initial iteration

m1=1; % Temporal variables define
while m1<long
    % Get position of point over 63.2% of yinf
    if ynorm(m1)>0.632*ynorm(long)
        t63=tnorm(m1); % Time when 'y' is 63.2% of max(y)
        y63=ynorm(m1);
        m1=long;
    else
        m1=m1+1;
    end
end
fprintf('Check 1\n')
m2=1;
while m2<long
    % Get position of first point over 3% of yinf
    if ynorm(m2)>0.03*ynorm(long) && tnorm(m2)>tin
        t3=tnorm(m2); % Time when 'y' is 3% of max(y)
        y3=ynorm(m2);
        m2=long;
    else
        m2=m2+1;
    end
end

m3=1;
while m3<long
    % Get position of first point over 90% of yinf
    if ynorm(m3)>0.9*ynorm(long)
        t90=tnorm(m3); % Time when 'y' is 3% of max(y)
        y90=ynorm(m3);
        m3=long;
    else
        m3=m3+1;
    end
end

%% Fractional order initial value
fprintf('Check 2\n')
v=0;
tt=t63/t90;

% Overshoot when dynamic underdamped
Mp=(ymax-ynorm(long))/ynorm(long);

% Obtain fractional order (v) from previous results
if (ymax>ynorm(long))
    syms v;
    v1 = (1.4182+sqrt((-1.4182)^2 - 4*0.8032*(0.6115-Mp))) / (2*0.8032);
    v2 = (1.4182-sqrt((-1.4182)^2 - 4*0.8032*(0.6115-Mp))) / (2*0.8032);
    if isreal(v1) && isreal(v2)
        if (v1>=1 && v1<=3)
            v0=v1;
        else
            v0=v2;
        end
    end
elseif (tt>=0 && tt<0.4325)
    p=1; tx2=zeros(1,71);
    for x=0.3:0.01:1 %variacion orden fraccional
        tx=-0.1621*x^3+0.9351*x^2+-0.4089*x+0.0711;
        tx2(p)=tx;
        p=p+1;
    end
    [row_a,col_a]=find(tx2>=tt,1,'first');
    v0=0.3+0.01*(col_a-1);
else
    v0=1;
end
fprintf('Check 3\n')
% Obtain the times signal cross over 1
if v0>1.3 % Only compute this data when FT or MTE is introduced
    cont3=1;
    totalosc=0;
    while cont3<long
        if ynorm(cont3)<1 && ynorm(cont3+1)>1
            totalosc=totalosc+1;
            cont3=cont3+1;
        else
            cont3=cont3+1;
        end
    end
end

% L0 definition
L0=t3-tin;

%& Algorithm for L0 computation
% Get settling time
if v0>=1.1525
    ma=long;
    while ma>1
        if (ynorm(ma)>=1.05 || ynorm(ma)<=0.95)
            ta=tnorm(ma); % Settling time
            ya=ynorm(ma);
            ma=1;
        else
            ma=ma-1;
        end
    end
end
fprintf('Check 4\n')

if v0>=1.4349 && totalosc>=2
    % Oscillation time
    os=1; % Oscillation time need to be greater than one
    while os<long
        if ynorm(os)>=1
            tu1=tnorm(os);
            yu1=ynorm(os);
            temp1=os;
            os=long;
        else
            os=os+1;
        end
    end

    os=temp1;
    while os<long
        if ynorm(os)<=1
            tu2=tnorm(os);
            yu2=ynorm(os);
            os=long;
        else
            os=os+1;
        end
    end

    tu=tu2-tu1; % Obtain half period

    %::::::::::::::Condiciones para la asignación de T0::::::::::
    diff=0.05;
    tuT0=0;
    while tuT0<tu
        [zT0 pT0 kT0] =APC(1, v0, 0.001, 1000);
        MT0=zpk(zT0,pT0,kT0);
        MMT0=1/(diff*MT0+1);
        [yT0,tT0]=step(MMT0,tnorm);
        longT0=length(yT0);

        % tuT0 calculation
        os=1;
        while os<longT0
            if yT0(os)>=1
                tu1T0=t(os);
                yu1T0=y(os);
                temp1=os;
                os=longT0;
            else
                os=os+1;
            end
        end

        os=temp1;
        while os<longT0
            if yT0(os)<=1
                tu2T0=t(os);
                yu2T0=y(os);
                os=longT0;
            else
                os=os+1;
            end
        end

        tuT0=tu2T0-tu1T0; % half period

        % Verify condition
        if tu<=tuT0
            T0=diff;     % T0 definition
        else
            diff=0.05+diff;
        end
    end

else
    T0=(t63-(tin+L0))^v0;
end
fprintf('Check 5\n')

%% Get initial model form
fprintf("Computing initial model\n")

    % Model to use
    if v0<1
        [z0, p0, k0]=APC(1,-v0,0.001,1000);  % Approach
        Gmm=zpk(z0,p0,k0);
        Gmm=1/Gmm;
    else
        [z0, p0, k0]=APC(1,v0,0.001,1000);   % Approach
        Gmm=zpk(z0,p0,k0);
    end
    fprintf('Check 5.1\n')

    try
      if (version_info.Name=="MATLAB")
       Gm0 = 1*exp(-(L0+tin)*s)/(T0*Gmm+1);     % Define initial model for MATLAB
      end
    catch ME
      %% Octave PADE delay approximation
      [pade_num, pade_den] = padecoef(L0+tin,6);
      pade_delay=tf(pade_num,pade_den);
      Gm0 = pade_delay/(T0*Gmm+1);     % Define initial model
    end
fprintf('Check 5.2\n')

    Gm0
    ym0=step(Gm0,tnorm);                     % set tolerances
fprintf('Check 5.3\n')

    Tolf=trapz(tnorm,abs(ym0-ynorm))*1e-7;   % optimization (Tolx and Tolf).
fprintf('Check 5.4\n')

    Tolx=norm([T0 v0 L0])*1e-7;


%::::::::::::::::::::Optimización:::::::::::::::::::::::::::
fprintf('Check 6\n')

%se establecen las opciones para llevar a cabo la optiización
options = optimset('MaxIter', ...
                   200, ...
                   'MaxFunEvals', ...
                   1000, ...
                   'Algorithm', ...
                   'active-set', ...
                   'TolFun', ...
                   Tolf, ...
                   'TolX', ...
                   Tolx, ...
                   'Display', ...
                   'off');

x0 = [T0 v0 L0]; % Initial paramenters and optimization command with evaluation range
costfun = @(xns)f_IDFOM(xns, tnorm, ynorm, tin, flagtin, 1);

[xns,IAEns] = fmincon(costfun, ...
                      x0, ...
                      [], ...
                      [], ...
                      [], ...
                      [], ...
                      x0*(1-0.9), ...
                      x0*(1+0.9), ...
                      [], ...
                      options);

To=xns(1); % Time constant
vo=xns(2); % Fractional order
Lo=xns(3); % Dead time
fprintf('Check 7\n')

% Model:
tmax=max(tnorm);
if vo<1
   [zo, po, koo]=APC(1,-vo,0.001,1000);
   Gm= 1/zpk(zo,po,koo);
else
    [zo, po, koo]=APC(1,vo,0.001,1000);
    Gm= zpk(zo,po,koo);
end

try
  if (version_info.Name=="MATLAB")
    Gmo=Ko*exp(-(Lo+tin)*s)/(To*Gm+1); % Define the tf for MATLAB
  end
catch ME
  %% Octave PADE delay approximation
  [pade_num, pade_den] = padecoef(Lo+tin,18);
  pade_delay=tf(pade_num,pade_den);
  Gmo=Ko*pade_delay/(To*Gm+1);
end

fprintf('Check 8\n')

ym=step(Gmo,tnorm);

%% Print parameters
fprintf('Initial model paramenters:\n')
if (Ko/floor(Ko))~=1
    fprintf('  K\t= %4.2d\n',Ko)
else
    fprintf('  K\t= %4.1d\n',Ko)
end
if (Lo/floor(Lo))~=1
    fprintf('  L\t= %1.2d\n',Lo)
else
    fprintf('  L\t= %1.1d\n',Lo)
end
if vo==1
    fprintf('  v\t= %1.1d\n',vo)
else
    fprintf('  v\t= %1.2d\n',vo)
end
if (To/floor(To))~=1
    fprintf('  T\t= %1.2d\n',To)
else
    fprintf('  T\t= %1.1d\n',To)
end
fprintf('  IAE\t= %1.2d\n',IAEns)

fprintf('Fractional order model:\n')
fprintf('\t\t %1.2E*exp(-%1.2Es)\n',Ko,Lo)
fprintf('Gm(s)=\t----------------------------\n')
fprintf('\t\t\t%1.2Es^%1.2E+1 \n',To,vo)

%% Write optimal model in results cache file:
fprintf(file_json_id, '{\n');
fprintf(file_json_id, '\t"type": "fractional_model",\n');
fprintf(file_json_id, '\t"v": %.20f,\n', vo);
fprintf(file_json_id, '\t"T": %.20f,\n', To);
fprintf(file_json_id, '\t"K": %.20f,\n', Ko);
fprintf(file_json_id, '\t"L": %.20f,\n', Lo);
fprintf(file_json_id, '\t"IAE": %.20f\n', IAEns);
fprintf(file_json_id, '}\n');

% Save signals to file
out = [tnorm unorm ynorm ym/Ko];
% fprintf(fid,'time\tstep\tinitial\tmodel\n');
for i = 1:length(out)
    fprintf(fid,'%d\t%d\t%d\t%d\n',out(i,1),out(i,2),out(i,3),out(i,4));
end
fclose(fid);
fclose(file_json_id);

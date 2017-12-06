A = [];
b = [];
Aeq = [];
beq = [];
lb = [];
ub = [];
nonlcon = @unitdisk;
x0 = [1,0,0];
x = fmincon(@minError,x0,A,b,Aeq,beq,lb,ub,nonlcon)
masterfile='.\data\transform\masterlocal-2.csv';
slavefile='.\data\transform\slavelocal-2.csv';
M=csvread(masterfile);
S=csvread(slavefile);
m_g0=[0,0,1];
M=M(1:200,1:3)';
S=S(1:200,1:3);
y=cross(m_g0,x);
B=combine(x,y,m_g0);
T=B*M;
T=T';
[row,col]=size(T);
fontsize=10;
t=1:row;
figure(1);
subplot(3,1,1); hold on; set(gca, 'Fontname', 'Times New Roman','FontSize',fontsize)
plot(t,T(:,1),'r');
plot(t,S(:,1),'b');
ylabel('acc-x');
legend('device 1','device 2');
subplot(3,1,2); hold on; set(gca, 'Fontname', 'Times New Roman','FontSize',fontsize)
plot(t,T(:,2),'r');
plot(t,S(:,2),'b');
legend('device 1','device 2');
ylabel('acc-y');
subplot(3,1,3); hold on; set(gca, 'Fontname', 'Times New Roman','FontSize',fontsize)
plot(t,T(:,3),'r');
plot(t,S(:,3),'b');
legend('device 1','device 2');
xlabel('sample')
ylabel('acc-z')
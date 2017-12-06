function f=minError(x)
    masterfile='.\data\transform\masterlocal-2.csv';
    slavefile='.\data\transform\slavelocal-2.csv';
    M=csvread(masterfile);
    S=csvread(slavefile);
    m_g0=[0,0,1];
    m_g0=m_g0/norm(m_g0);
    M=M(1:200,1:3)';
    S=S(1:200,1:3)';
    y=cross(m_g0,x);
    B=combine(x,y);
    T=B*M;
    f=calcError(T,S);
end
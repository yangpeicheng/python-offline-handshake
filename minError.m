function f=minError(x,M,S)
    %masterfile='.\data\aligned\masterlocal-14.csv';
    %slavefile='.\data\aligned\slavelocal-14.csv';
    %M=csvread(masterfile);
    %S=csvread(slavefile);
    m_g0=[0,0,1];
    x=x/norm(x);
    %m_g0=m_g0/norm(m_g0);
    len=min(size(M,1),size(S,1));
    M=M(1:len,1:3)';
    S=S(1:len,1:3)';
    y=cross(m_g0,x);
    B=[x;y];
    T=B*M;
    f=calcError(T,S);
end
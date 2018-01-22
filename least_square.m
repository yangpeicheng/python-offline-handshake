function B=least_square(M,S,g)
    A = [];
    b = [];
    g=g/norm(g);
    Aeq = [];
    beq = [];
    lb = [];
    ub = [];
    nonlcon = @unitdisk;
    x0 = [0.707,0.707,0];
    %masterfile='.\data\aligned\masterlocal-14.csv';
    %slavefile='.\data\aligned\slavelocal-14.csv';
    x = fmincon(@(x)minError(x,M,S),x0,A,b,Aeq,beq,lb,ub,@(x)nonlcon(x,g));
    x=x/norm(x);
    m_g0=[0,0,1];
    y=cross(m_g0,x);
    B=[x;y/norm(y);m_g0];
   
end

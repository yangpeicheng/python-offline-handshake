for i=1:44
    i
    m=strcat('.\data\transform\masterlocal-',num2str(i),'.csv');
    s=strcat('.\data\transform\slavelocal-',num2str(i),'.csv');
    m_output=strcat('.\data\leastsquare\masterlocal-',num2str(i),'.csv');
    s_output=strcat('.\data\leastsquare\slavelocal-',num2str(i),'.csv');
    adaptive_train(m,s,m_output,s_output);
end



function compare(master_file1,master_file2,slave_file1,slave_file2)
%master_file1 开始对齐 master文件名
%slave_file1 开始对齐 slave文件名
%master_file2 自适应对齐 master文件名
%slave_file2 自适应对齐 slave文件名
    m_data1=csvread(master_file1);
    m_data2=csvread(master_file2);
    s_data1=csvread(slave_file1);
    s_data2=csvread(slave_file2);
    figure(1);
    [len1,col]=size(m_data1);
    [len2,col]=size(m_data2);
    t1=1:len1;
    t2=1:len2;
    
    fontsize=15;
    subplot(2,1,1);hold on; set(gca, 'Fontname', 'Times New Roman','FontSize',fontsize)
    plot(t1,m_data1(:,1),'r')
    plot(t1,s_data1(:,1),'b')
    legend('device 1','device 2');
    ylabel('beginning alignment');
    subplot(2,1,2);hold on; set(gca, 'Fontname', 'Times New Roman','FontSize',fontsize)
    
    plot(t2,m_data2(:,1),'r')
    plot(t2,s_data2(:,1),'b')
    ylabel('adaptive alignment');
    legend('device 1','device 2');
    
    
end

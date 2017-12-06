function plot3D( masterfile,slavefile )
%三维数据对比折线图
    M=csvread(masterfile);
    S=csvread(slavefile);
    Mx=M(:,1);
    My=M(:,2);
    Mz=M(:,3);
    Sx=S(:,1);
    Sy=S(:,2);
    Sz=S(:,3);
    [row,col]=size(M);
    fontsize=15;
    t=1:row;
    
    figure(1);
    figure('visible','off');
    
    subplot(3,1,1); hold on; set(gca, 'Fontname', 'Times New Roman','FontSize',fontsize)
    plot(t,Mx,'r');
    plot(t,Sx,'b');
    ylabel('acc-x');
    legend('device 1','device 2');
    subplot(3,1,2); hold on; set(gca, 'Fontname', 'Times New Roman','FontSize',fontsize)
    plot(t,My,'r');
    plot(t,Sy,'b');
    legend('device 1','device 2');
    ylabel('acc-y');
    subplot(3,1,3); hold on; set(gca, 'Fontname', 'Times New Roman','FontSize',fontsize)
    plot(t,Mz,'r');
    plot(t,Sz,'b');
    legend('device 1','device 2');
    xlabel('sample')
    ylabel('acc-z')
    %num=isstrprop(masterfile,'digit');
    %picturename=masterfile(num);
    %saveas(gcf,strcat('.\picture\',picturename,'.jpg'));
    %close(gcf);
end


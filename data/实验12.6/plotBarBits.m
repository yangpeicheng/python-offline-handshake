function plotBarBits(masterfile,slavefile,lab,varargin)
%masterfile Cartesian�ļ���
%slavefile Spherical�ļ���
%lab axis-label example:   [{'axis 1'};{'axis 2'};{'axis 3'}]
%varargin legend example:   'Cartesian','Spherical'
    M=csvread(masterfile);
    S=csvread(slavefile);
    tm=M(40:end,:);     %������������͹�������˳��
    ts=S(40:end,:);
    fM=[tm ;M(26:39,:)];
    fS=[ts ;S(26:39,:)];
    Mx=fM(:,1)';
    My=fM(:,2)';
    Mz=fM(:,3)';
    Sx=fS(:,1)';
    Sy=fS(:,2)';
    Sz=fS(:,3)';
    
    fontsize=5;
    
    figure(1);
    subplot(3,1,1);
    bar([Mx;Sx]','group');
    ylabel(lab{1});
    %ylabel('axis-1 axis-2');
    %ylabel('axis-1');
    legend(varargin)
    set(gca,'Fontsize',fontsize);
    subplot(3,1,2);
    bar([My;Sy]','group');
    ylabel(lab{2});
    %ylabel('axis1 axis-3');
    %ylabel('axis-2');
    legend(varargin)
    set(gca,'Fontsize',fontsize);
    subplot(3,1,3);
    bar([Mz;Sz]','group');
    ylabel(lab{3});
    %ylabel('axis-2 axis-3');
    %ylabel('axis-3');
    legend(varargin)
    set(gca,'Fontsize',fontsize);
end
    
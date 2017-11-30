function plotBar(masterfile,slavefile)

    M=csvread(masterfile);
    S=csvread(slavefile);
    tm=M(40:end,:)
    ts=M(40:end,:)
    fM=[tm ;M(26:39,:)];
    fS=[ts ;S(26:39,:)];
    Mx=fM(:,1)';
    My=fM(:,2)';
    Mz=fM(:,3)';
    Sx=fS(:,1)';
    Sy=fS(:,2)';
    Sz=fS(:,3)';
    
    figure(1);
    subplot(3,1,1);
    bar([Mx;Sx]','group');
    ylabel('len(bits)');
    %ylabel('axis-1');
    legend('Cartesian','Spherical')
    set(gca,'Fontsize',5);
    subplot(3,1,2);
    bar([My;Sy]','group');
    ylabel('len(bits)/len(data)');
    %ylabel('axis-2');
    legend('Cartesian','Spherical')
    set(gca,'Fontsize',5);
    subplot(3,1,3);
    bar([Mz;Sz]','group');
    ylabel('error/len(bits)');
    %ylabel('axis-3');
    legend('Cartesian','Spherical')
    set(gca,'Fontsize',5);
end
    
x=1:10;
y1 = 1:10;
y2 = y1;
y3 = y2;

figure(1);

subplot(3,1,1); hold on;
plot(x,y1);

subplot(3,1,2); hold on;
plot(x,y2);

subplot(3,1,3); hold on;  set(gca, 'Fontname', 'Times New Roman','FontSize',24)
plot(x,y3);
xlabel('x')
ylabel('y')
function error=calcError(A,B)
    A=A(1:2,:);
    B=B(1:2,:);
    m=A-B;
    e=m.*m;
    error=sum(e(:));
end



    
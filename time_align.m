function [m_s,s_s]=time_align(m,s)
    m_s=1;
    s_s=1;
    len=size(m,1);
    l=floor(len*4/9);
    cor=0;
    for i=1:len-l
        for j=1:len-l
            tcor=corr(m(i:i+l),s(j:j+l));
            if tcor>cor
                cor=tcor;
                m_s=i;
                s_s=j;
            end
        end
    end
end
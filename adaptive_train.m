function adaptive_train(mfile,sfile,m_output,s_output)
    M=csvread(mfile);
    S=csvread(sfile);
    %g=M(1,16:18);
    g=M(:,16:18);
    M=M(:,1:3);
    S=S(:,1:3);
    
    m_mean=[mean(M(:,1)),mean(M(:,2)),mean(M(:,3))];
    s_mean=[mean(S(:,1)),mean(S(:,2)),mean(S(:,3))];
    M_mean=repmat(m_mean,size(M,1),1);
    S_mean=repmat(s_mean,size(S,1),1);
    M=M-M_mean;
    S=S-S_mean;
    
    norm_m=[];
    norm_s=[];
    output_M=[];
    output_S=[];
    for i=1:size(M,1)
        norm_m=[norm_m;norm(M(i,:))];
    end
    for i=1:size(S,1)
        norm_s=[norm_s;norm(S(i,:))];
    end
    m_len=size(M,1);
    s_len=size(S,1);
    %plot3D(M(1:min(m_len,s_len),:),S(1:min(m_len,s_len),:));
   %{
    figure(1)
    tl=min(m_len,s_len);
    t=1:tl;
    subplot(2,1,1);
    plot(t,M(1:tl,3),'r');hold on;
    plot(t,S(1:tl,3),'b');hold on;
    %}
    
    m_index=1;
    s_index=1;
    k=2;
    first=true;
    while true
        if first
            train_size=100;
            interval=train_size;
            first=false;
        else
             train_size=20;
             interval=50;
        end
        master_end=m_index+train_size;
        slave_end=s_index+train_size;
        
        if master_end>=m_len ||slave_end>=s_len
            %l=min(max(master_end , m_len)-min(master_end , m_len),max(slave_end , s_len)-min(slave_end , s_len));
            break
        end
        
        %[m_start,s_start]=time_align(norm_m(m_index:master_end),norm_s(s_index:slave_end));
        [m_start,s_start]=time_align(M(m_index:master_end,3),S(s_index:slave_end,3));
        if abs(m_start-s_start)>2
            k=1;
            m_index=m_index+m_start;
            s_index=s_index+s_start;
        else
            k=k+1;
        end
        
        if m_index>m_len || s_index>s_len
            break
        end
        
        l=min([k*interval,m_len-m_index,s_len-s_index]);
        
        m_tmp_end=m_index+l-1;
        s_tmp_end=s_index+l-1;

        l=min(slave_end-s_index,master_end-m_index);
        B=least_square(M(m_index:m_index+l-1,:),S(s_index:s_index+l-1,:),g(m_index));
        B
        output_M=[output_M;M(m_index:m_tmp_end,:)*B'];
        output_S=[output_S;S(s_index:s_tmp_end,:)];
        m_index=m_tmp_end;
        s_index=s_tmp_end;
        
        
        
        
        %{
        m_train_end=min(m_index+train_size-1,len);
        s_train_end=min(s_index+train_size-1,len);
        m_end=min(m_index+interval-1,len);
        s_end=min(s_index+interval-1,len);
        [m_s,s_s]=time_align(norm_m(m_index:m_train_end),norm_s(s_index:s_train_end));
        m_s=m_index+m_s;
        s_s=s_index+s_s;
        l=min(m_end-m_s,s_end-s_s);
        m_end=m_s+l;
        s_end=s_s+l;
        B=least_square(M(m_s:m_end,:),S(s_s:s_end,:));
        output_M=[output_M;M(m_s:m_end,:)*B'];
        output_S=[output_S;S(s_s:s_end,:)];
        m_index=m_end;
        s_index=s_end;
        if m_end>=len || s_end>=len ||m_train_end>=len ||s_train_end>=len
            break
        end
        %}
    end
    
    %plot3D(output_M,output_S)
    %{
    norm_ms=[];
    norm_ss=[];
    for i=1:size(output_M,1)
        norm_ms=[norm_ms;norm(output_M(i,:))];
    end
    for i=1:size(output_S,1)
        norm_ss=[norm_ss;norm(output_S(i,:))];
    end
    tl=min(size(norm_ms,1),size(norm_ss,1));
    t=1:tl;
    subplot(2,1,2);
    plot(t,norm_ms(1:tl,:),'r');hold on;
    plot(t,norm_ss(1:tl,:),'b');hold on;
    %}
    corrcoef(output_M,output_S);
    csvwrite(m_output,output_M);
    csvwrite(s_output,output_S);
end
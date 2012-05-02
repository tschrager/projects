function leda_feng_init()
    defaults = {};
    pfbsperfft = 4;
    fftsperfftblock = 4;
    numfftsblocks=1;
    %numpfbs=pfbsperfft*numffts
    %numbiplexffts = numffts/4;

    fftsize=13;

    % Place ADC blocks
    adcsync=xInport('adcsync');
    %xBlock(struct('source','xps_library/quadc'), struct('adc_brd','0'),{},[adcdata_cell,{adcvalid},{adcsync}]);
    %xBlock(struct('source','xps_library/quadc'), struct('adc_brd','1'));
    
    
    const_fft_shift = xSignal;
    fft_shift_data = xSignal;
    fft_shift = xBlock(struct('source','xps_library/software register','name','fft_shift'), struct('io_dir','From Processor'));
    fft_shift.bindPort({const_fft_shift},{fft_shift_data})

    % Create each FFT stream
    for streamno = 0:numfftsblocks-1,
        fftinputdata_cell = cell(1,4);
        
        for fftnumber = 1:fftsperfftblock,
            adcdata_cell = cell( 1, 4 );
            adcdata_cell{1}=xInport();
            adcdata_cell{2}=xInport();
            adcdata_cell{3}=xInport();
            adcdata_cell{4}=xInport();
            
            fftsync = xSignal;
            fftinputdata_cell{fftnumber} = xSignal;
            currentPFBMux = xBlock(str2func('pfb_mux'),{});
            currentPFBMux.bindPort([{adcsync},adcdata_cell],struct('fftsync',fftsync,'fftinputdata',fftinputdata_cell(fftnumber)));

        end
        
        term_fft_sync=xOutport();
        fftout12 = xOutport();
        fftout34 = xOutport();
        term_of = xSignal;
        
        
        
        % Place a biplex FFT
        currentFFT = xBlock(struct('source','casper_library_ffts/fft_biplex_real_2x'), struct('FFTSize',fftsize));
        currentFFT.bindPort([{fftsync},{fft_shift_data},fftinputdata_cell],{term_fft_sync,fftout12,fftout34,term_of});
        


    end

end


function pfb_mux()
    pfbsperfft = 4;
    fftsperfftblock = 4;
    numfftsblocks=1;
    %numpfbs=pfbsperfft*numffts
    %numbiplexffts = numffts/4;

    fftsize=13;
    
    pfbsync = xSignal;
    fftsync = xOutport('fftsync');
    pfbdata_cell = cell( 1, 4 );
    delayed_pfbdata_cell = cell( 1, 4 );
    
    adcsync = xInport('adc_sync');
    adcdata_cell = cell(1,4);
    fftinputdata = xOutport('fftinputdata');

    % address counter for pfb data
    addresscount = xSignal;
    zero_cmp = xSignal;
    we_pfb = xSignal;
    xBlock('Counter',struct('n_bits',fftsize,'arith_type','Unsigned','cnt_type','Free Running','rst','On','en','Off'),{pfbsync},{addresscount});
    % counter for pfb multiplexor
    pfbcount = xSignal;
    xBlock('Counter',struct('n_bits',log2(pfbsperfft),'arith_type','Unsigned','cnt_type','Free Running','rst','On','en','Off'),{pfbsync},{pfbcount});
    xBlock('Constant',struct('const',1,'arith_type','Unsigned','n_bits',log2(pfbsperfft),'bin_pt',0), ...
           {},{zero_cmp} );
    xBlock('Delay',{},{pfbsync},{fftsync});
    
    xBlock('Relational',struct('mode','a=b','latency',0),{pfbcount,zero_cmp},{we_pfb});


    % Place PFB blocks and associated memory
    currentmulitplexor = xBlock('Mux',struct('inputs','4'));


    pfbdata_cell{1} = xSignal;
    delayed_pfbdata_cell{1} = pfbdata_cell{1};
    adcdata_cell{1} = xInport;
    xBlock(struct('source','casper_library_pfbs/pfb_fir_real'), ...
           struct('PFBSize',fftsize,'TotalTaps',4,'n_inputs',0), ...
           {adcsync,adcdata_cell{1}},struct('sync_out',pfbsync,'pol1_out1',pfbdata_cell{1}) );

    for i=2:pfbsperfft,
        pfbdata_cell{i} = xSignal;
        delayed_pfbdata_cell{i} = xSignal;
        terminate = xSignal;
        adcdata_cell{i} = xInport;
        xBlock(struct('source','casper_library_pfbs/pfb_fir_real'), struct('PFBSize',fftsize,'TotalTaps',4,'n_inputs',0),...
               {adcsync,adcdata_cell{i}}, ...
               struct('sync_out',terminate,'pol1_out1',pfbdata_cell{i}) );
        xBlock('Single Port RAM',struct('Depth',2^fftsize), ...
               struct('addr',addresscount,'data_in',pfbdata_cell{i},'we', we_pfb), ...
               {delayed_pfbdata_cell{i}} );
    end

    currentmulitplexor.bindPort([{pfbcount},delayed_pfbdata_cell],struct('y',fftinputdata));
    
end




% Place output blocks


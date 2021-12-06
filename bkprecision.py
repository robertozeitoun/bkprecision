import pyvisa, time
class Oscilloscope(object):
    '''A class for simplifying communication with BK Precision oscilloscopes.'''
    def __init__(self, ip):
        self.delay = 0.001
        rm = pyvisa.ResourceManager()
        try:
            print("Connecting to oscilloscope (IP {}).".format(ip))
            self.osc = rm.open_resource("TCPIP::{}::INSTR".format(ip),read_termination='\n')
            self.osc.chunk_size=20480
            self.osc.timeout=5000
            self.nchannels=2
            print(self.chdr('off'))
            print(self.wfsu(1,int(self.sanu(1)),0,0))
            print("Connected!!!")
            return
        except:
            print("Couldn't connect to oscilloscope.")
        
    def disconnect(self):
        """Close the resource manager connection."""
        self.osc.close()
        return("Connection finished.")

    # ACQUIRE_WAY
    def __acqw_get(self):
        '''Get configuration of ACQW - Acquire Way'''
        query_results = self.osc.query("ACQW?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def acqw(self, mode=None, times=None):
        '''Set configuration to ACQW - Acquire Way'''
        if mode is None:
            return(self.__acqw_get())
        else:
            try:
                if mode.upper() in ('PEAK_DETECT','SAMPLING','AVERAGE'):
                    if mode.upper() == 'AVERAGE':
                        if times in (4, 16, 32, 64, 128, 256):
                            self.osc.write("AVGA {}".format(times))
                            return("Success. Acquire Way set to {} with {} averages.".format(mode.upper(),times))
                        else:
                            raise Exception
                    else:
                        self.osc.write("ACQW {}".format(mode.upper()))
                        return("Success. Acquire Way set to {}.".format(mode.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid  input for ACQW - Acquire Way -> Use: mode=['PEAK_DETECT', 'SAMPLING' or 'AVERAGE']; for mode='AVERAGE', use: times=[4, 16, 32, 64, 128 or 256]")

    # ALL_STATUS?
    def alst(self):
        '''Get configuration of ALST? - All Status'''
        query_results = self.osc.query("ALST?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))

    # ARM_ACQUISITION
    def arm(self):
        '''Command ARM - Arm Acquisition'''
        return(self.osc.write("ARM"))

    # ATTENUATION
    def __attn_get(self, channel=None):
        '''Get configuration of ATTN - Attenuation'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:ATTN?".format(channel))
                    time.sleep(self.delay)
                    return(Oscilloscope.format_results(query_results))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for ATTN - Attenuation -> Use: channel=[1~{}]".format(self.nchannels))
    def attn(self, channel=None, value=None):
        '''Set configuration to ATTN - Attenuation'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__attn_get(set_channel)))
                return channel_list
            else:
                return self.__attn_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))) and value in(1,5,10,50,100,500,1000):
                    self.osc.write("C{}:ATTN {}".format(channel,value))
                    return("Success. Attenuation set to {}x on channel {}.".format(value,channel))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for ATTN - Attenuation -> Use: channel=[1 to {0}], value=[1, 5, 10, 50, 100, 500 or 1000]".format(str(self.nchannels)))

    # AUTO_SETUP
    def aset(self):
        '''Command ASET - Auto Setup'''
        return(self.osc.write("ASET"))

    # AUTO_TYPESET
    def __autts_get(self):
        '''Get configuration of AUTTS - Auto Typeset'''
        query_results = self.osc.query("AUTTS?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def autts(self, value=None):
        '''Set configuration to AUTTS - Auto Typeset'''
        if value is None:
            return(self.__autts_get())
        else:
            try:
                if value.upper() in ('SP','MP','RS','DRP','RC'):
                    self.osc.write("AUTTS {}".format(value))
                    return("Success. Auto Typeset set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for AUTTS - Auto Typeset -> Use:\n\
                    'SP' - means only one period to be displayed\n\
                    'MP' - means multiple periods to be displayed\n\
                    'RS' - means the waveform is triggered on the rise side\n\
                    'DRP'- means the waveform is triggered on the drop side\n\
                    'RC -  means to go back to the state before auto set \n")

    # AVERAGE_ACQUIRE
    def __avga_get(self):
        '''Get configuration of AVGA - Average Acquire'''
        query_results = self.osc.query("AVGA?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def avga(self, value=None):
        '''Set configuration to AVGA - Average Acquire'''
        if value is None:
            return(self.__avga_get())
        else:
            try:
                if value in (4, 16, 32, 64, 128, 256):
                    self.osc.write("AVGA {}".format(value))
                    return("Success. Average Acquire set to {}.".format(value))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for AVGA - Average Acquire -> Use: value=[4, 16, 32, 64, 128, 256]")

    # BANDWIDTH_LIMIT
    def __bwl_get(self, channel=None):
        '''Get configuration of BWL - BandWidth Limit'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:BWL?".format(channel))
                    time.sleep(self.delay)
                    return(Oscilloscope.format_results(query_results))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for BWL - BandWidth Limit -> Use: channel=[1~{}]".format(self.nchannels))
    def bwl(self, channel=None, value=None):
        '''Set configuration to BWL - BandWidth Limit'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__bwl_get(set_channel)))
                return channel_list
            else:
                return self.__bwl_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))) and value.upper() in('ON','OFF'):
                    self.osc.write("C{}:BWL {}".format(channel,value.upper()))
                    return("Success. BandWidth Limit set to {} on channel {}.".format(value.upper(),channel))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for BWL - BandWidth Limit -> Use: channel=[1 to {}], value=['ON' or 'OFF']".format(str(self.nchannels)))

    # BUZZER
    def __buzz_get(self):
        '''Get configuration of BUZZ - Buzzer'''
        query_results = self.osc.query("BUZZ?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def buzz(self, value=None):
        '''Set configuration to BUZZ - Buzzer'''
        if value is None:
            return(self.__buzz_get())
        else:
            try:
                if value.upper() in ('ON','OFF'):
                    self.osc.write("BUZZ {}".format(value.upper()))
                    return("Success. Buzzer set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for BUZZ - Buzzer -> Use: value=['ON' or 'OFF']")

    # *CAL?
    def _cal(self):
        '''Command *CAL? - Self-Calibration'''
        try:
            self.osc.timeout=60000
            self.osc.query("*CAL?")
            return("Success. Self-Calibration command performed.")
        except:
            raise Exception("Error. Self-Calibration command not performed.")
        finally:
            self.osc.timeout=5000

    # *CLS
    def _cls(self):
        '''Command CLS - Clear All Status Data Registers'''
        try:
            self.osc.write("*CLS")
            return("Success. Clear All Status Data Registers command performed.")
        except:
            raise Exception("Error. Clear All Status Data Registers command not performed.")
            
    # CMR?
    def cmr(self):
        '''Query CMR? - Command Error Register'''
        try:
            query_results=self.osc.query("CMR?")
            time.sleep(self.delay)
            return(Oscilloscope.format_results(query_results))
        except:
            raise Exception("Error. Command Error Register not performed.")

    # COMM_HEADER
    def __chdr_get(self):
        '''Get configuration of CHDR - Comm Header'''
        query_results = self.osc.query("CHDR?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def chdr(self, value=None):
        '''Set configuration to CHDR - Comm Header'''
        if value is None:
            return(self.__chdr_get())
        else:
            try:
                if value.upper() in ('OFF', 'SHORT', 'LONG'):
                    try:
                        self.osc.write("CHDR {}".format(value.upper()))
                        return("Success. Comm Header set to {}.".format(value.upper()))
                    except:
                        raise Exception("Failed to set CHDR - Comm Header.")
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for CHDR - Comm Header -> Use: 'OFF','SHORT' or 'LONG'")
   
    # COMM_NET
    def conet(self):
        '''Query CONET? - Commom Net'''
        try:
            query_results=self.osc.query("CONET?")
            time.sleep(self.delay)
            return(query_results.replace(',','.'))
        except:
            raise Exception("Failed. Commom Net query not performed.")
    
    # COUNTER
    def __coun_get(self):
        '''Get configuration of COUN - Cymometer Display'''
        query_results = self.osc.query("COUN?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def coun(self, value=None):
        '''Set configuration to COUN - Cymometer Display'''
        if value is None:
            return(self.__coun_get())
        else:
            try:
                if value.upper() in ('ON','OFF'):
                    self.osc.write("COUN {}".format(value.upper()))
                    return("Success. Cymometer Display set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for COUN - Cymometer Display -> Use: value=['ON' or 'OFF']")

    # COUPLING    
    def __cpl_get(self, channel=None):
        '''Get configuration of CPL - Coupling'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{0}:CPL?".format(str(channel)))
                    time.sleep(self.delay)
                    return(Oscilloscope.format_results(query_results))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for CPL - Coupling -> Use: channel=[1~{}]".format(self.nchannels))
    def cpl(self, channel=None, value=None):
        '''Set configuration to CPL - Coupling'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__cpl_get(set_channel)))
                return channel_list
            else:
                return self.__cpl_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))) and value.upper() in('A1M','D1M','GND'):
                    self.osc.write("C{}:CPL {}".format(channel,value.upper()))
                    return("Success. Coupling set to {} on channel {}.".format(value.upper(),channel))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for CPL - Coupling -> Use: channel=[1 to {}], value=['A1M', 'D1M' or 'GND']".format(self.nchannels))

    # CSV_SAVE
    def __csvs_get(self):
        '''Get configuration of CSVS - CSV Save'''
        query_results = self.osc.query("CSVS?")
        time.sleep(self.delay)
        return Oscilloscope.format_results(query_results)
    def csvs(self, dd=None, save=None):
        '''Set configuration to CSVS - CSV Save'''
        nones=0
        if dd is None:
            dd = 'MAX'
            nones+=1
        else:
            if dd.upper() not in  ('DIS','MAX'):
                raise Exception("Invalid input for CSV Save. Use: dd=['DIS' or 'MAX]")
        if save is None:
            save='OFF'
            nones+=1
        else:
            if save.upper() not in  ('ON','OFF'):
                raise Exception("Invalid input for CSV Save. Use: save=['ON' or 'OFF]")
        if nones == 2:
            return self.__csvs_get()
        else:
            try:
                self.osc.write("CSVS DD,{},SAVE,{}".format(dd.upper(),save.upper()))
                return("Success. CSV Save sets to DD={}, SAVE={}.".format(dd.upper(),save.upper()))
            except:
                raise Exception("Failed to set CSV Save.")

    # CURSOR_AUTO
    def crau(self):
        '''Command CRAU - Cursor Auto Mode'''
        try:
            self.osc.write("CRAU")
            return("Success. CRAU - Cursor Auto Mode command performed.")
        except:
            raise Exception("Error. CRAU - Cursor Auto Mode command not performed.")

    # CURSOR_MEASURE
    def __crms_get(self):
        '''Get configuration of CRMS - Cursor Measure'''
        query_results = self.osc.query("CRMS?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def crms(self, value=None):
        '''Set configuration to CRMS - Cursor Measure'''
        if value is None:
            return(self.__crms_get())
        else:
            try:
                if value.upper() in ('OFF', 'AUTO', 'VREL', 'HREL'): # VREL=MANUAL  HREL=TRACK
                    try:
                        self.osc.write("CRMS {}".format(value.upper()))
                        return("Success. Cursor Measure set to {}.".format(value.upper()))
                    except:
                        raise Exception("Failed to set CRMS - Cursor Measure.")
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for CRMS - Cursor Measure -> Use: 'OFF', 'AUTO', 'VREL'(manual) or 'HREL'(track)")

    # CURSOR_SET
    def __crst_get(self, channel=None):
        '''Get configuration of CRST - Cursor Set'''
        try:
            if channel is not None:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{0}:CRST? VREF, VDIF, TREF, TDIF, HREF, HDIF".format(str(channel)))
                    time.sleep(self.delay)
                    return "C{0}={1}".format(channel,Oscilloscope.format_results(query_results))
                else:
                    raise Exception
            else:
                raise Exception
        except:
            raise Exception("Invalid input for CRST - Cursor Set -> Use: channel=[1~{0}]".format(str(self.nchannels)))
    def crst(self, channel=None, vref=None, vdif=None, tref=None, tdif=None, href=None, hdif=None):
        '''Set configuration to CRST - Cursor Set'''
        if channel is None:
            if vref is None and vdif is None and tref is None and tdif is None and href is None and hdif is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append(self.__crst_get(set_channel))
                channel_list_string='\n'.join(channel_list)
                return channel_list_string
            else:
                raise Exception("Invalid input for CRST - Cursor Set -> Use: channel=[1~{0}]".format(str(self.nchannels)))
        else:
            current_values = self.__crst_get(channel).strip('C1234=[]').replace(" ","").replace("'","").split(',')
            nones=0        
            if vref is None:
                vref = float(current_values[0].split('=')[1])
                nones+=1
            else:
                if vref < -4.0 or vref > 4.0:
                    raise Exception("Invalid input for Cursor Set. Use: vref=[-4.0 ~ 4.0]")
            if vdif is None:
                vdif = float(current_values[1].split('=')[1])
                nones+=1
            else:
                if vdif < -4.0 or vdif > 4.0:
                    raise Exception("Invalid input for Cursor Set. Use: vdif=[-4.0 ~ 4.0]")
            if tref is None:
                tref = float(current_values[2].split('=')[1])
                nones+=1
            else:
                if tref < -8.0 or tref > 8.0:
                    raise Exception("Invalid input for Cursor Set. Use: tref=[-8.0 ~ 8.0]")
            if tdif is None:
                tdif = float(current_values[3].split('=')[1])
                nones+=1
            else:
                if tdif < -8.0 or tdif > 8.0:
                    raise Exception("Invalid input for Cursor Set. Use: tdif=[-8.0 ~ 8.0]")
            if href is None:
                href = float(current_values[4].split('=')[1])
                nones+=1
            else:
                if href < 0.1 or href > 15.9:
                    raise Exception("Invalid input for Cursor Set. Use: href=[0.1 ~ 15.9]")
            if hdif is None:
                hdif = float(current_values[5].split('=')[1])
                nones+=1
            else:
                if hdif < 0.1 or hdif > 15.9:
                    raise Exception("Invalid input for Cursor Set. Use: hdif=[0.1 ~ 15.9]")
            if nones == 6:
                return self.__crst_get(channel)
            else:
                try:
                    self.osc.write("MENU OFF;C{}:CRST VREF,{:.1f},VDIF,{:.1f},TREF,{:.1f},TDIF,{:.1f},HREF,{:.1f},HDIF,{:.1f}".format(channel,vref,vdif,tref,tdif,href,hdif))
                    return("Success. Cursor Set sets to VREF={:.1f}, VDIF={:.1f}, TREF={:.1f}, TDIF={:.1f}, HREF={:.1f}, HDIF={:.1f} on Channel {}.".format(vref,vdif,tref,tdif,href,hdif,channel))
                except:
                    raise Exception("Failed to set Cursor Set.")
            
    # CURSOR_VALUE?
    def __crva_get(self, channel=None, value=None):
        '''Get configuration of CRVA - Cursor Value'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:CRVA? {}".format(channel,value))
                    time.sleep(self.delay)
                    return "C{}={}".format(channel,query_results)
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for CRVA - Cursor Value -> Use: channel=[1~{}]".format(self.nchannels))
    def crva(self, channel=None, value=None):
        '''Set configuration to CRVA - Cursor Value'''
        if value is None:
            channel_list=[]
            if channel is None:
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append(self.__crva_get(set_channel,'HREL'))
                    channel_list.append(self.__crva_get(set_channel,'VREL'))
                return channel_list
            else:
                channel_list.append(self.__crva_get(channel,'HREL'))
                channel_list.append(self.__crva_get(channel,'VREL'))
                return channel_list
        else:
            try:
                if channel in (range(1,(self.nchannels+1))) and value.upper() in('HREL','VREL'):
                    return self.__crva_get(channel,value)
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for CRVA - Cursor Value -> Use: channel=[1 to {}], value=['HREL' or 'VREL']".format(self.nchannels))

    # CYMOMETER      
    def cymt(self):
        '''Query CYMT - Cymometer'''
        query_results = self.osc.query("CYMT?")
        time.sleep(self.delay)
        return Oscilloscope.format_results(query_results)
            
    # DDR?
    def ddr(self):
        '''Query DDR? - Device Dependent Register'''
        query_results = self.osc.query("DDR?")
        time.sleep(self.delay)
        return Oscilloscope.format_results(query_results)

    # DEFINE
    def __defm_get(self):
        '''Get configuration of DEF - Mathematical Expression'''
        query_results = self.osc.query("DEF?")
        time.sleep(self.delay)
        return(query_results)
    def defm(self, oper=None, sourceA=None, sourceB=None):
        '''Set configuration to DEF - Mathematical Expression'''
        if oper is None:
            return(self.__defm_get())
        else:
            if oper.upper() in ('+','-','*','/'):
                if sourceA in (range(1,(self.nchannels+1))) and sourceB in (range(1,(self.nchannels+1))):
                    self.osc.write("DEF EQN,'C{}{}C{}'".format(sourceA,oper,sourceB))
                    return("Success. Mathematical Expression equation set to 'C{}{}C{}'.".format(sourceA,oper,sourceB))
                else:
                    raise Exception("Invalid input for DEF - Mathematical Expression -> Use: oper=['+', '-', '*' or '/'], sourceA=[1 to {0}], sourceB=[1 to {0}]".format(self.nchannels))
            elif oper.upper() == 'FFT':
                if sourceA in (range(1,(self.nchannels+1))):
                    self.osc.write("DEF EQN,'{}(C{})'".format(oper.upper(),sourceA))
                    return("Success. Mathematical Expression equation set to '{}(C{})'.".format(oper.upper(),sourceA))
                else:
                    raise Exception("Invalid input for DEF - Mathematical Expression -> Use: oper=['FFT'], sourceA=[1 to {0}]".format(self.nchannels))
            else:
                raise Exception("Invalid input for DEF - Mathematical Expression -> Use: oper=['+', '-', '*', '/' or 'FFT']")

    # DELETE_FILE
    def delf(self, file=None):
        '''Command DELF - Delete File'''
        if file is not None:
            self.osc.write("DELF DISK,UDSK,FILE,'{}'".format(file.upper()))
            return("Success. Deleted file {}".format(file.upper()))
        else:
            raise Exception("Invalid input for DELF - Delete File -> Use: file='/{DIRECTORY_NAME}/{FILE_NAME}'")

    # DIRECTORY
    def __dir_get(self, path=None):
        '''Get configuration of DIR - Directory'''
        if path is None:
            return(self.osc.query("DIR? DISK,UDSK"))
        if path.upper().find('/') != -1:
            self.osc.write("DIR? DISK,UDSK,'{}'".format(path.upper()))
            query_results=self.osc.read_raw()
            time.sleep(self.delay)
            if query_results==b'':
                raise Exception("Directory {} not found".format(path))
            else:
                return(self.osc.query("DIR? DISK,UDSK,'{}'".format(path.upper())))
        else:
            raise Exception("Invalid input for DIR - Directory -> Use: path=['/' or '/{DIRECTORY_NAME}']")
    def dir(self, path=None, action=None):
        '''Set configuration to DIR - Directory'''
        if action is None:
            if path is None:
                return self.__dir_get()
            else:
                return self.__dir_get(path.upper())
        else:
            try:
                if action.upper() in ('CREATE','DELETE'):
                    if path is not None:
                        if path.find('/') != -1:
                            self.osc.write("DIR DISK,UDSK,ACTION,{},'{}'".format(action.upper(),path.upper()))
                            return("Success. Directory sets {} -> {}".format(action.upper(),path.upper()))
                        else:
                            raise Exception
                    else:
                        raise Exception
                else:
                    raise Exception("Invalid input for DIR - Directory -> Use: path=['/' or '/{DIRECTORY_NAME}'], action=['CREATE' or 'DELETE']")
            except:
                raise Exception("Failed to set Directory.")

    # DOT_JOIN
    def __dtjn_get(self):
        '''Get configuration of DTJN - Dot Join'''
        query_results = self.osc.query("DTJN?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def dtjn(self, value=None):
        '''Set configuration to DTJN - Dot Join'''
        if value is None:
            return(self.__dtjn_get())
        else:
            try:
                if value.upper() in ('ON','OFF'):
                    self.osc.write("DTJN {}".format(value.upper()))
                    return("Success. Dot Join set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for DTJN - Dot Join -> Use: value=['ON' or 'OFF']")

    # *ESE
    def __ese_get(self):
        '''Query from *ESE Command'''
        query_results = self.osc.query("*ESE?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def _ese(self, value=None):
        '''Command for *ESE Command'''
        if value is None:
            return(self.__ese_get())
        else:
            try:
                if value in range(0,256):
                    self.osc.write("*ESE {}".format(value))
                    return("Success. *ESE Command set to {}.".format(value))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for *ESE Command -> Use: value=[0 to 255]")

    # *ESR?
    def _esr(self):
        '''Query from *ESR Command'''
        query_results = self.osc.query("*ESR?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))

    # EXR?
    def exr(self):
        '''Query from EXR? Command'''
        query_results = self.osc.query("EXR?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))

    # FFT_FULLSCREEN
    def __fftf_get(self):
        '''Get configuration of FFTF - FFT Fullscreen'''
        query_results = self.osc.query("FFTF?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def fftf(self, value=None):
        '''Set configuration to FFTF - FFT Fullscreen'''
        if value is None:
            return(self.__fftf_get())
        else:
            try:
                if value.upper() in ('ON', 'OFF'):
                    try:
                        self.osc.write("FFTF {}".format(value.upper()))
                        return("Success. FFT Fullscreen set to {}.".format(value.upper()))
                    except:
                        raise Exception("Failed to set FFTF - FFT Fullscreen.")
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for FFTF - FFT Fullscreen -> Use: 'ON' or 'OFF'")

    # FFT_SCALE
    def __ffts_get(self):
        '''Get configuration of FFTS - FFT Scale'''
        query_results = self.osc.query("FFTS?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def ffts(self, value=None):
        '''Set configuration to FFTS - FFT Scale'''
        if value is None:
            return(self.__ffts_get())
        else:
            try:
                if value.upper() in ('DBVRMS', 'VRMS'):
                    try:
                        self.osc.write("FFTS {}".format(value.upper()))
                        return("Success. FFT Scale set to {}.".format(value.upper()))
                    except:
                        raise Exception("Failed to set FFTS - FFT Scale.")
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for FFTS - FFT Scale -> Use: 'DBVRMS' or 'VRMS'")

    # FFT_WINDOW
    def __fftw_get(self):
        '''Get configuration of FFTW - FFT Window'''
        query_results = self.osc.query("FFTW?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def fftw(self, value=None):
        '''Set configuration to FFTW - FFT Window'''
        if value is None:
            return(self.__fftw_get())
        else:
            try:
                if value.upper() in ('RECT', 'BLAC', 'HANN', 'HAMM'):
                    try:
                        self.osc.write("FFTW {}".format(value.upper()))
                        return("Success. FFT Window set to {}.".format(value.upper()))
                    except:
                        raise Exception("Failed to set FFTW - FFT Window.")
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for FFTW - FFT Window -> Use: 'RECT', 'BLAC', 'HANN' or 'HAMM'")

    # FFT_ZOOM
    def __fftz_get(self):
        '''Get configuration of FFTZ - FFT Zoom'''
        query_results = self.osc.query("FFTZ?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def fftz(self, value=None):
        '''Set configuration to FFTZ - FFT Zoom'''
        if value is None:
            return(self.__fftz_get())
        else:
            try:
                if value in (1,2,5,10):
                    try:
                        self.osc.write("FFTZ {}".format(value))
                        return("Success. FFT Zoom set to {}x.".format(value))
                    except:
                        raise Exception("Failed to set FFTZ - FFT Zoom.")
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for FFTZ - FFT Zoom -> Use: 1, 2, 5 or 10")

    # FILENAME
    def __flnm_get(self, ftype=None):
        '''Get configuration of FLNM - File Name'''
        query_results = self.osc.query("FLNM? TYPE,{}".format(ftype.upper()))
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def flnm(self, ftype=None, fname=None):
        '''Set configuration to FLNM - File Name'''
        ftype_avalible=['C1','C2','TA','TB','SETUP','HCOPY']
        if fname is None:
            if ftype is None:
                ftypes=[]
                for ft in ftype_avalible:
                    ftypes.append(self.__flnm_get(ft))
                return(ftypes)
            else:
                if ftype.upper() in ftype_avalible:
                    return(self.__flnm_get(ftype.upper()))
                else:
                    raise Exception("Invalid input for FLNM - File Name -> Use: ftype=['C1','C2','TA','TB','SETUP' or 'HCOPY']")
        else:
            try:
                if ftype.upper() in ftype_avalible:
                    if len(fname.upper()) <= 8:
                        self.osc.write("FLNM TYPE,{},FILE,'{}'".format(ftype.upper(),fname.upper()))
                        return("Success. File Name for Type {} set to {}".format(ftype.upper(),fname.upper()))
                    else:
                        raise Exception
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for FLNM - File Name -> Use: ftype=['C1','C2','TA','TB','SETUP' or 'HCOPY'], fname='{DOS_FILENAME}'")
 
    # FILS_SET
    def __filts_get(self, channel=None):
        '''Get configuration of FILT - Filter Set'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:FILTS?".format(channel))
                    time.sleep(self.delay)
                    return(query_results)
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for FILTS - Filter Set -> Use: channel=[1~{}]".format(self.nchannels))
    def filts(self, channel=None, ftype=None, upplimit=None, lowlimit=None):
        '''Set configuration to FILTS - Filter Set'''
        if ftype is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__filts_get(set_channel)))
                return(channel_list)
            else:
                return(self.__filts_get(channel))
        else:
            tdiv=self.tdiv(True)
            for freq in self.__filts_limits():
                if freq[0].find(tdiv)==0:
                    upplimitmax=self.__indiscret_convert(self.__std(freq[2]),'HZ')
                    lowlimitmin=self.__indiscret_convert(self.__std(freq[3]),'HZ')
                    break
            upplimitmaxdisconv=self.__discret_convert(upplimitmax,'Hz',3)
            lowlimitmindisconv=self.__discret_convert(lowlimitmin,'Hz',3)
            if ftype.upper() in ('LP','HP','BP','BR'):
                if channel in (range(1,(self.nchannels+1))):
                    if ftype.upper() == 'LP': 
                        if upplimit is not None:
                            if type(upplimit) is str:
                                upplimitindconv=self.__indiscret_convert(self.__std(upplimit.upper()),'HZ')
                            else:
                                upplimitindconv=upplimit
                            upplimitdisconv=self.__discret_convert(upplimitindconv,'Hz',3)
                            if upplimitindconv <= upplimitmax and upplimitindconv >= lowlimitmin:
                                upplimit=upplimitdisconv
                                self.osc.write("C{}:FILTS TYPE,{},UPPLIMIT,{}".format(channel,ftype.upper(),upplimit))
                                message_success = "Success. Filter Set set to {} with Upplimit {} on channel {}.".format(ftype.upper(),upplimit,channel)
                            else:
                                raise Exception ("Invalid input for FILTS - Filter Set -> upplimit value shoud be between {} and {}".format(lowlimitmindisconv,upplimitmaxdisconv))    
                        else:
                            raise Exception ("Invalid input for FILTS - Filter Set -> for ftype LP: use upplimit='value[M,K]Hz'")
                    elif ftype.upper() == 'HP':
                        if upplimit is not None or lowlimit is not None:
                            if upplimit is not None and lowlimit is None: 
                                lowlimit = upplimit
                            if type(lowlimit) is str:
                                lowlimitindconv=self.__indiscret_convert(self.__std(lowlimit.upper()),'HZ')
                            else:
                                lowlimitindconv=lowlimit
                            lowlimitdisconv=self.__discret_convert(lowlimitindconv,'Hz',3)
                            if lowlimitindconv <= upplimitmax and lowlimitindconv >= lowlimitmin:
                                lowlimit=lowlimitdisconv
                                self.osc.write("C{}:FILTS TYPE,{},LOWLIMIT,{}".format(channel,ftype.upper(),lowlimit))
                                message_success = "Success. Filter Set set to {} with Lowlimit {} on channel {}.".format(ftype.upper(),lowlimit,channel)
                            else:
                                raise Exception ("Invalid input for FILTS - Filter Set -> lowlimit value shoud be between {} and {}".format(lowlimitmindisconv,upplimitmaxdisconv))    
                        else:
                            raise Exception ("Invalid input for FILTS - Filter Set -> for ftype HP: use lowlimit='value[M,K]Hz'")
                    elif ftype.upper() in ('BP','BR'):
                        if upplimit is not None and lowlimit is not None: 
                            if type(upplimit) is str:
                                upplimitindconv=self.__indiscret_convert(self.__std(upplimit.upper()),'HZ')
                            else:
                                upplimitindconv=upplimit
                            upplimitdisconv=self.__discret_convert(upplimitindconv,'Hz',3)
                            if type(lowlimit) is str:
                                lowlimitindconv=self.__indiscret_convert(self.__std(lowlimit.upper()),'HZ')
                            else:
                                lowlimitindconv=lowlimit
                            lowlimitdisconv=self.__discret_convert(lowlimitindconv,'Hz',3)
                            if upplimitindconv > upplimitmax or upplimitindconv < lowlimitmin:
                                raise Exception ("Invalid input for FILTS - Filter Set -> upplimit value shoud be between {} and {}".format(lowlimitmindisconv,upplimitmaxdisconv))    
                            if lowlimitindconv > upplimitmax and lowlimitindconv < lowlimitmin:
                                raise Exception ("Invalid input for FILTS - Filter Set -> lowlimit value shoud be between {} and {}".format(lowlimitmindisconv,upplimitmaxdisconv))    
                            if upplimitindconv >= (lowlimitindconv + lowlimitmin):                               
                                upplimit=upplimitdisconv
                                lowlimit=lowlimitdisconv
                                self.osc.write("C{}:FILTS TYPE,{},UPPLIMIT,{},LOWLIMIT,{}".format(channel,ftype.upper(),upplimit,lowlimit))
                                message_success = "Success. Filter Set set to {} with Upplimit {} and Lowlimit {} on channel {}.".format(ftype.upper(),upplimit,lowlimit,channel)
                            else:
                                raise Exception ("Invalid input for FILTS - Filter Set -> the diff between upplimit and lowlimit values must be at least {}".format(lowlimitmindisconv))    
                        else:
                            raise Exception ("Invalid input for FILTS - Filter Set -> for ftype BP or BR: use upplimit='value[M,K]Hz', lowlimit='value[M,K]Hz'")
                    else:
                        raise Exception ("Invalid input for FILTS - Filter Set -> Use: ftype=['LP','HP','BP' or 'BR']")
                else:
                    raise Exception("Invalid input for FILTS - Filter Set -> Use: channel=[1~{}]".format(self.nchannels))
            else:
                raise Exception("Invalid input for FILTS - Filter Set -> Use: \n\
                                channel=[1 to {}]\n\
                                ftype=['LP','HP','BP' or 'BR']\n\
                                \tfor ftype LP: use upplimit='value[M,K]Hz'\n\
                                \tfor ftype HP: use lowlimit='value[M,K]Hz'\n\
                                \tfor ftype BP or BR: use upplimit='value[M,K]Hz', lowlimit='value[M,K]Hz'\n\
                                ".format(str(self.nchannels)))
            self.tdiv(self.tdiv())
            return message_success
    def __filts_limits(self):
        return(\
        # TDIV     TDIV float  UPPLIMIT   LOWLIMIT
        [['2.50ns', '2.5e-09', '245.0MHz', '5.000MHz'],\
        ['5ns'    , '5e-09'  , '245.0MHz', '5.000MHz'],\
        ['10ns'   , '1e-08'  , '245.0MHz', '5.000MHz'],\
        ['25ns'   , '2.5e-08', '245.0MHz', '5.000MHz'],\
        ['50ns'   , '5e-08'  , '245.0MHz', '5.000MHz'],\
        ['100ns'  , '1e-07'  , '245.0MHz', '5.000MHz'],\
        ['250ns'  , '2.5e-07', '245.0MHz', '5.000MHz'],\
        ['500ns'  , '5e-07'  , '122.5MHz', '2.500MHz'],\
        ['1us'    , '1e-06'  , '122.5MHz', '2.500MHz'],\
        ['2.50us' , '2.5e-06', '49.00MHz', '1.000MHz'],\
        ['5us'    , '5e-06'  , '49.00MHz', '1.000MHz'],\
        ['10us'   , '1e-05'  , '49.00MHz', '1.000MHz'],\
        ['25us'   , '2.5e-05', '12.25MHz', '250.0KHz'],\
        ['50us'   , '5e-05'  , '6.125MHz', '125.0KHz'],\
        ['100us'  , '0.0001' , '2.450MHz', '50.00KHz'],\
        ['250us'  , '0.00025', '1.225MHz', '25.00KHz'],\
        ['500us'  , '0.0005' , '612.5KHz', '12.50KHz'],\
        ['1ms'    , '0.001'  , '245.0KHz', '5.000KHz'],\
        ['2.50ms' , '0.0025' , '122.5KHz', '2.500KHz'],\
        ['5ms'    , '0.005'  , '61.25KHz', '1.250KHz'],\
        ['10ms'   , '0.01'   , '24.50KHz', '500.00Hz'],\
        ['25ms'   , '0.025'  , '12.25KHz', '250.00Hz'],\
        ['50ms'   , '0.05'   , '6.125KHz', '125.00Hz'],\
        ['100ms'  , '0.1'    , '12.25KHz', '250.00Hz'],\
        ['250ms'  , '0.25'   , '4.900KHz', '100.00Hz'],\
        ['500ms'  , '0.5'    , '2.450KHz', '50.000Hz'],\
        ['1s'     , '1.0'    , '1.225KHz', '25.000Hz'],\
        ['2.50s'  , '2.5'    , '490.00Hz', '10.000Hz'],\
        ['5s'     , '5.0'    , '245.00Hz', '5.0000Hz'],\
        ['10s'    , '10.0'   , '122.50Hz', '2.5000Hz'],\
        ['25s'    , '25.0'   , '49.000Hz', '1.0000Hz'],\
        ['50s'    , '50.0'   , '24.500Hz', '0.5000Hz']])

    # FILTER
    def __filt_get(self, channel=None):
        '''Get configuration of FILT - Filter'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:FILT?".format(channel))
                    time.sleep(self.delay)
                    return(Oscilloscope.format_results(query_results))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for FILT - Filter -> Use: channel=[1~{}]".format(self.nchannels))
    def filt(self, channel=None, value=None):
        '''Set configuration to FILT - Filter'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__filt_get(set_channel)))
                return channel_list
            else:
                return self.__filt_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))) and value.upper() in('ON','OFF'):
                    self.osc.write("C{}:FILT {}".format(channel,value.upper()))
                    return("Success. Filter set to {} on channel {}.".format(channel,value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for FILT - Filter -> Use: channel=[1 to {}], value=['ON' or 'OFF']".format(self.nchannels))

    # FORCE_TRIGGER
    def frtr(self):
        '''Command FRTR - Force Trigger'''
        return(self.osc.write("FRTR"))

    # FORMAT_VDISK
    def fvdisk(self):
        '''Query from FVDISK Query'''
        return( self.osc.query("FVDISK?"))

    # GET_CSV
    def gcsv(self, dd=None, save=None):
        '''Query from GCSV - Get CSV'''
        chunk=self.osc.chunk_size
        self.osc.chunk_size = 1024*1024
        nones=0
        if dd is None:
            dd = 'DIS'
            nones+=1
        else:
            if dd.upper() not in  ('DIS','MAX'):
                raise Exception("Invalid input for Get CSV. Use: dd=['DIS' or 'MAX]")
        if save is None:
            save='OFF'
            nones+=1
        else:
            if save.upper() not in  ('ON','OFF'):
                raise Exception("Invalid input for Get CSV. Use: save=['ON' or 'OFF]")
        try:
            csv_data=self.osc.query("GCSV? DD,{},SAVE,{}".format(dd.upper(),save.upper()))
            self.osc.chunk_size = chunk
            return(csv_data)
        except:
            raise Exception("Error. Failed to Get CSV.")

    # GRID_DISPLAY
    def __grds_get(self):
        '''Get configuration of GRDS - Grid Display'''
        query_results = self.osc.query("GRDS?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def grds(self, value=None):
        '''Set configuration to GRDS - Grid Display'''
        if value is None:
            return(self.__grds_get())
        else:
            try:
                if value.upper() in ('FULL','HALF','OFF'):
                    self.osc.write("GRDS {}".format(value.upper()))
                    return("Success. Grid Display set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for GRDS - Grid Display -> Use: value=['FULL','HALF' or 'OFF']")

    # *IDN?
    def _idn(self):
        '''Query *IDN? - Identification'''
        query_results = self.osc.query("*IDN?")
        time.sleep(self.delay)
        return(query_results.split(','))

    # INR?
    def inr(self):
        '''Query INR? - Internal Register'''
        query_results = self.osc.query("INR?")
        time.sleep(self.delay)
        return(int(query_results))

    # INTENSITY
    def __ints_get(self):
        '''Get configuration of INTS - Intensity Trace and Grid'''
        query_results = self.osc.query("INTS?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def ints(self, trace=None, grid=None):
        '''Set configuration to INTS - Intensity Trace and Grid'''
        if trace is None and grid is None:
            return(self.__ints_get())
        else:
            try:
                if trace in range(30,101) and grid in range(0,101):
                    self.osc.write("INTS TRACE,{},GRID,{}".format(trace,grid))
                    return("Success. Intensity Trace and Grid set to TRACE={}% and GRID={}%.".format(trace,grid))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for INTS - Intensity Trace and Grid -> Use: trace=[ 30 ~ 100 ], grid=[ 0 ~ 100 ]")

    # INTERLEAVED
    def __ilvd_get(self):
        '''Get configuration of ILVD - Interleaved'''
        query_results = self.osc.query("ILVD?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def ilvd(self, value=None):
        '''Set configuration to ILVD - Interleaved'''
        if value is None:
            return(self.__ilvd_get())
        else:
            try:
                if value.upper() in ('ON','OFF'):
                    self.osc.write("ILVD {}".format(value.upper()))
                    return("Success. Interleaved set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for ILVD - Interleaved -> Use: value=['ON' or 'OFF']")

    # INVERT_SET
    def __invs_get(self, channel=None):
        '''Get configuration of INVS - Invert Set'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:INVS?".format(channel))
                    time.sleep(self.delay)
                    return(Oscilloscope.format_results(query_results))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for INVS - Invert Set -> Use: channel=[1~{0}]".format(self.nchannels))
    def invs(self, channel=None, value=None):
        '''Set configuration to INVS - Invert Set'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__invs_get(set_channel)))
                return channel_list
            else:
                return self.__invs_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))) and value.upper() in('ON','OFF'):
                    self.osc.write("C{}:INVS {}".format(channel,value.upper()))
                    return("Success. Invert Set set to {} on channel {}.".format(value.upper(),channel))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for INVS - Invert Set -> Use: channel=[1 to {}], value=['ON' or 'OFF']".format(self.nchannels))

    # LOCK
    def __lock_get(self):
        '''Get configuration of LOCK - Lock Keyboard'''
        query_results = self.osc.query("LOCK?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def lock(self, value=None):
        '''Set configuration to LOCK - Lock Keyboard'''
        if value is None:
            return(self.__lock_get())
        else:
            try:
                if value.upper() in ('ON','OFF'):
                    if value.upper() == 'ON':
                        self.osc.write("LOCK {}".format(value.upper()))
                    else:
                        self.osc.write("FRTR;LOCK {}".format(value.upper()))
                    return("Success. Lock Keyboard set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for LOCK - Lock Keyboard -> Use: value=['ON' or 'OFF']")

    # MATH_VERT_DIV
    def __mtvd_get(self):
        '''Get configuration of MTVD - Mathematical Verical Division'''
        query_results = self.osc.query("MTVD?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def mtvd(self, value=None):
        '''Set configuration to MTVD - Mathematical Verical Division'''
        if value is None:
            return(self.__mtvd_get())
        else:
            try:
                value=self.__std(value)
                if value in ('1pV','2pV','5pV','10pV','20pV','50pV','100pV','200pV','500pV',
                             '1uV','2uV','5uV','10uV','20uV','50uV','100uV','200uV','500uV',
                             '1mV','2mV','5mV','10mV','20mV','50mV','100mV','200mV','500mV',
                             '1V','2V','5V','10V','20V','50V','100V'):
                    self.osc.write("MTVD {}".format(value.upper()))
                    return("Success. Mathematical Verical Division set to {}.".format(self.__std(value)))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for MTVD - Mathematical Verical Division -> Use: value=[1,2,5,10,20,50,100,200,500pV ~ 100V]")

    # MATH_VERT_POS
    def __mtvp_get(self):
        '''Get configuration of MTVP - Mathematical Verical Position'''
        query_results = self.osc.query("MTVP?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def mtvp(self, value=None):
        '''Set configuration to MTVP - Mathematical Verical Position'''
        if value is None:
            return(self.__mtvp_get())
        else:
            try:
                if value in range(-230, 231):
                    self.osc.write("MTVP {}".format(value))
                    return("Success. Mathematical Verical Position set to {}.".format(value))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for MTVP - Mathematical Verical Position -> Use: value=[-230 up to 230]")

    # MEASURE_DELAY
    def mead(self, value=None, channel1=None, channel2=None):
        '''Query from MEAD - Measure Delay'''
        if channel2 is None:
            channel2=2    
        if channel1 is None:
            channel1=1 
        if value is None:
            allvalues=[]
            for value_one in ('PHA','FRR','FRF','FFR','FFF','LRR','LRF','LFR','LFF'):
                allvalues.append(Oscilloscope.format_results(self.osc.query("C{}-C{}:MEAD? {}".format(channel1,channel2,value_one))))
            return(allvalues)
        else:
            try:
                if value.upper() in ('PHA','FRR','FRF','FFR','FFF','LRR','LRF','LFR','LFF'):
                    return(Oscilloscope.format_results(self.osc.query("C{}-C{}:MEAD? {}".format(channel1,channel2,value))))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for MEAD - Measure Delay -> Use: value=['PHA','FRR','FRF','FFR','FFF','LRR','LRF','LFR','LFF'], channel1=[1 ~ {0}], channel2=[1 ~ {0}]".format(self.nchannels))

    # MENU
    def __menu_get(self):
        '''Get configuration of MENU - Menu Display'''
        query_results = self.osc.query("MENU?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def menu(self, value=None):
        '''Set configuration to MENU - Menu Display'''
        if value is None:
            return(self.__menu_get())
        else:
            try:
                if value.upper() in ('ON','OFF'):
                    self.osc.write("MENU {}".format(value.upper()))
                    time.sleep(0.1)
                    return("Success. Menu Display set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for MENU - Menu Display -> Use: value=['ON' or 'OFF']")

    #OFFSET
    def __ofst_get(self, channel=None):
        '''Get value of OFST - Offset'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:OFST?".format(channel))
                    time.sleep(self.delay)
                    return float(query_results)
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for OFST - Offset -> Use: channel=[1~{}]".format(self.nchannels))
    def ofst(self, channel=None, value=None):
        '''Set value of OFST - Offset'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__ofst_get(set_channel)))
                return channel_list
            else:
                return self.__ofst_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    vdiv=self.vdiv(channel)
                    if vdiv > 0.2:
                        offset_max_neg=-40.00
                        offset_max_pos=40.00
                    else:
                        offset_max_neg=-1.60
                        offset_max_pos=1.60
                    if type(value) is str:
                        value=self.__indiscret_convert(self.__std(value),'v')    
                    if value >= offset_max_neg and value <= offset_max_pos:
                        self.osc.write("C{}:OFST {}".format(channel,value))
                        return("Success. Offset set to {} on channel {}.".format(value,channel))
                    else:
                        raise Exception
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for OFST - Offset -> Use: channel=[1 to {}], value=[{:.2f}V ~ {:.2f}V]".format(self.nchannels,offset_max_neg,offset_max_pos))

    # *OPC
    def __opc_get(self):
        '''Query from *OPC - Operation Complete'''
        query_results = self.osc.query("*OPC?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def _opc(self, value=None):
        '''Command for *OPC - Operation Complete'''
        if value is None:
            return(self.__opc_get())
        else:
            try:
                if value == 1:
                    self.osc.write("*OPC")
                    return("Success. Operation Complete set to {}.".format(value))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for *OPC - Operation Complete -> Use: value=[1]")

    # *OPT
    def _opt(self):
        '''Query from *OPT? Query'''
        query_results = self.osc.query("*OPT?")
        time.sleep(self.delay)
        return(query_results)

    # PANEL_SETUP
    def pnsu(self, file=None, action=None):
        '''Command for PNSU - Panel Setup Command'''
        if file is not None:
            if type(file) is str and str(file).upper().find('.SET') != -1:
                if action is not None:
                    if action.upper() == "SAVE":
                        self.osc.write("PNSU?")
                        data=self.osc.read_raw()
                        try:
                            with open(file.upper(),'wb') as f:
                                f.write(data)
                            return("Success. Panel Setup Command save to file: {}.".format(file.upper()))
                        except:
                            raise Exception("Error. Panel Setup Command save to file {} not possible.".format(file.upper()))
                    elif action.upper() == "RECALL":
                        try:
                            pnsu=bytes("PNSU ","ascii")
                            with open(file.upper(),'rb') as f:
                                data=f.read()
                            self.osc.write_raw(pnsu+data)
                            self.run()
                            return("Success. Panel Setup Command recall from file: {}.".format(file.upper()))
                        except:
                            raise Exception("Error. Panel Setup Command recall from file {} not possible.".format(file.upper()))
                    else:
                        raise Exception("Invalid input for PNSU - Panel Setup Command -> Use: action=['SAVE' or 'RECALL']")
                else:
                    raise Exception("Invalid input for PNSU - Panel Setup Command -> Use: action=['SAVE' or 'RECALL']")
            else:
                raise Exception
        else: 
            raise Exception("Invalid input for PNSU - Panel Setup Command -> Use: file='{/DIRECTORY/}{DOS_FILENAME.SET}'")

    # PARAMETER_CLR
    def pacl(self):
        '''Command for PACL - Parameter Clear Pass/Fail test Counter'''
        try:
            self.osc.write("PACL")
            return("Success. Parameter Clear Pass/Fail test Counter.")
        except:
            raise Exception("Error. PACL - Parameter Clear Pass/Fail test Counter.")

    # PARAMETER_VALUE?
    def __pava_get(self, channel=None, param=None):
        '''Query from PAVA - Parameter Value'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:PAVA? {}".format(channel,param))
                    time.sleep(0.02)
                    if param.upper() == 'ALL':
                        return(Oscilloscope.format_results(query_results))
                    else:
                        return(query_results.split(',')[1])
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for PAVA - Parameter Value -> Use: channel=[1~{0}]".format(str(self.nchannels)))
    def __pava_param_units(self, param):
        '''Units of parameter to PAVA - Parameter Value'''
        parameter_units={'PKPK':'V','MAX':'V','MIN':'V','AMPL':'V','TOP':'V','BASE':'V','CMEAN':'V','MEAN':'V','RMS':'V','CRMS':'V',
                         'OVSN':'%','FPRE':'%','OVSP':'%','RPRE':'%',
                         'FREQ':'Hz',
                         'PER':'s','PWID':'s','NWID':'s','RISE':'s','FALL':'s','WID':'s',
                         'DUTY':'%','NDUTY':'%'}
        for par in parameter_units.keys():
            if param.upper() == par:
                return parameter_units[par]
        return("Error. Parameter key not found.")
    def pava(self, channel=None, param=None, discret=False):
        '''Select parameter to PAVA - Parameter Value'''
        if param is None or param is True:
            if param is True:
                discret=True
            param='ALL'
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{0}={1}".format(set_channel,self.__pava_get(set_channel,param)))
                return(channel_list)
            else:
                data_all=self.__pava_get(channel,param)
                if discret:
                    data_discret=[]
                    for d in data_all:
                        value=self.__discret_convert(float(d.split('=')[1]),self.__pava_param_units(d.split('=')[0]))
                        data_discret.append("{}={}".format(d.split('=')[0],value))
                    return(data_discret)
                else:
                    return(data_all)
        else:
            data_all=self.__pava_get(channel,'ALL')
            for d in data_all:
                if param.upper() == d.split('=')[0]:    
                    if discret:
                        return self.__discret_convert(float(d.split('=')[1]),self.__pava_param_units(d.split('=')[0]))
                    else:
                        return float(d.split('=')[1])
            return("Error. Parameter not found.")

    # PEAK_DETECT
    def __pdet_get(self):
        '''Get configuration of PDET - Peak Detect'''
        query_results = self.osc.query("PDET?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def pdet(self, value=None):
        '''Set configuration to PDET - Peak Detect'''
        if value is None:
            return(self.__pdet_get())
        else:
            try:
                if value.upper() in ('ON','OFF'):
                    self.osc.write("PDET {0}".format(value.upper()))
                    return("Success. Peak Detect to {0}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for PDET - Peak Detect -> Use: value=['ON' or 'OFF']")

    # PERSIST
    def __pers_get(self):
        '''Get configuration of PERS - Persistence Display'''
        query_results = self.osc.query("PERS?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def pers(self, value=None):
        '''Set configuration to PERS - Persistence Display'''
        if value is None:
            return(self.__pers_get())
        else:
            try:
                if value.upper() in ('ON', 'OFF'):
                    try:
                        self.osc.write("PERS {0}".format(value.upper()))
                        return("Success. Persistence Display set to {0}.".format(value.upper()))
                    except:
                        raise Exception("Failed to set Persistence Display.")
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for PERS - Persistence Display -> Use: 'ON' or 'OFF'")

    # PERSIST_SETUP
    def __pesu_get(self):
        '''Get configuration of PESU - Persistence Display Setup'''
        query_results = self.osc.query("PESU?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def pesu(self, value=None):
        '''Set configuration to PESU - Persistence Display Setup'''
        if value is None:
            return(self.__pesu_get())
        else:
            try:
                if type(value) is int:
                    if value in (1,2,5):
                        try:
                            self.osc.write("PESU {0}".format(value))
                            return("Success. Persistence Display Setup set to {0}s.".format(value))
                        except:
                            raise Exception("Failed to set Persistence Display Setup.")
                    else:
                        raise Exception
                elif type(value) is str:
                    if value.upper() in ('OFF','INFINITE'):
                        try:
                            self.osc.write("PESU {0}".format(value.upper()))
                            return("Success. Persistence Display Setup set to {0}.".format(value.upper()))
                        except:
                            raise Exception("Failed to set Persistence Display Setup.")
                    else:
                        raise Exception
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for PESU - Persistence Display Setup -> Use: value=['OFF', 1, 2, 5 or 'INFINITE']")

    # PF_CONTROL
    def __pfct_get(self):
        '''Get configuration of PFCT - Pass/Fail Controls'''
        query_results = self.osc.query("PFCT?")
        time.sleep(self.delay)
        return(query_results)
    def pfct(self, trace=None, control=None, output=None, outputstop=None):
        '''Set configuration to PFCT - Pass/Fail Controls'''
        if trace is None and control is None and output is None and outputstop is None:
            return(Oscilloscope.format_results(self.__pfct_get()))
        else:
            try:
                previous_data=self.__pfct_get()
                if outputstop is None:
                    outputstop=previous_data.split(',')[7]
                if output is None:
                    output=previous_data.split(',')[5]
                if control is None:
                    control=previous_data.split(',')[3]
                if trace is None:
                    trace=previous_data.split(',')[1]
                if type(trace) is str:
                    trace=int(trace.upper().strip('C'))
                if trace in range(1,(self.nchannels+1)):
                    self.osc.write("PFCT TRACE,C{},CONTROL,{},OUTPUT,{},OUTPUTSTOP,{}".format(trace,control.upper(),output.upper(),outputstop.upper()))
                    return("Success. PFCT - Pass/Fail Controls set to TRACE=C{}, CONTROL={}, OUTPUT={}, OUTPUTSTOP={}.".format(trace,control.upper(),output.upper(),outputstop.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for PFCT - Pass/Fail Controls -> Use: trace=[1 to {}], control=['START' or 'STOP'], output=['FAIL' or 'PASS'], outputstop=['ON' or 'OFF']".format(self.nchannels))

    # PF_CREATEM
    def pfcm(self):
        '''Command for PFCM - Pass/Fail Create Mask'''
        try:
            self.osc.write("PFCM")
            return("Success. Pass/Fail Create Mask.")
        except:
            raise Exception("Invalid input for PFCM - Pass/Fail Create Mask")

    # PF_DATADIS
    def pfdd(self):
        '''Query from PFDD - Pass/Fail Data Display'''
        query_results = self.osc.query("PFDD?").replace('PASS',',PASS')
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))

    # PF_DISPLAY
    def __pfds_get(self):
        '''Get configuration of PFDS - Pass/Fail Display'''
        query_results = self.osc.query("PFDS?")
        time.sleep(self.delay)
        return(query_results)
    def pfds(self, test=None, display=None):
        '''Set configuration to PFDS - Pass/Fail Display'''
        if test is None and display is None:
            return(Oscilloscope.format_results(self.__pfds_get()))
        else:
            try:
                previous_data=self.__pfds_get()
                if test is None:
                    test=(Oscilloscope.format_results(previous_data.split(',')[1]))
                if display is None:
                    display=(Oscilloscope.format_results(previous_data.split(',')[3]))
                if test.upper() in ('ON','OFF') and display.upper() in ('ON','OFF'):
                    self.osc.write("PFDS TEST,{},DISPLAY,{}".format(test.upper(),display.upper()))
                    return("Success. Pass/Fail Display set to TEST={} and DISPLAY={}.".format(test.upper(),display.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for PFDS - Pass/Fail Display -> Use: test=['ON' or 'OFF'], display=['ON' or 'OFF']")

    # PF_SAVELOAD
    def pfsl(self, location=None, action=None):
        '''Command for PFSL - Pass/Fail Save Load'''
        try:
            if location is None or action is None: 
                raise Exception
            else:
                if location.upper() in ('IN','EX') and action.upper() in ('SAVE','LOAD'):
                    self.osc.write("PFSL LOCATION,{},ACTION,{}".format(location.upper(),action.upper()))
                    return("Success. PFSL - Pass/Fail Save Load set to LOCATION={} and ACTION={}.".format(location.upper(),action.upper()))
                else:
                    raise Exception
        except:
            raise Exception("Invalid input for PFSL - Pass/Fail Save Load -> Use: location=['IN' or 'EX'], action=['SAVE' or 'LOAD']")

    # PF_SET
    def __pfst_get(self):
        '''Get configuration of PFST - Pass/Fail Set Mask'''
        query_results = self.osc.query("PFST?")
        time.sleep(self.delay)
        return(query_results)
    def pfst(self, xmask=None, ymask=None):
        '''Set configuration to PFST - Pass/Fail Set Mask'''
        if xmask is None and ymask is None:
            return(Oscilloscope.format_results(self.__pfst_get()))
        else:
            try:
                previous_data=self.__pfst_get()
                if xmask is None:
                    xmask=float(previous_data.split(',')[1].strip('DIV'))
                if ymask is None:
                    ymask=float(previous_data.split(',')[3].strip('DIV'))
                if xmask >= 0.04 and xmask <=4 and ymask >= 0.04 and ymask <=4:
                    xmask=0.04*int(xmask/0.04)
                    ymask=0.04*int(ymask/0.04)
                    self.osc.write("PFST XMASK,{},YMASK,{}".format(xmask,ymask))
                    return("Success. PFST - Pass/Fail Set Mask set to XMASK={}DIV and YMASK={}DIV.".format(xmask,ymask))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for PFST - Pass/Fail Set Mask -> Use: xmask=[0.04 ~ 4.0], ymask=[0.04 ~ 4.0]")

    # *RCL
    def _rcl(self, value=None):
        '''Command for *RCL - Recall Panel Setup Command'''
        try:
            if value is not None:
                if value in range(1,21):
                    self.osc.write("*RCL {}".format(value))
                    return("Success. Recall Panel Setup Command set to memory {}.".format(value))
                else:
                    raise Exception
            else: 
                raise Exception
        except:
            raise Exception("Invalid input for *RCL - Recall Panel Setup Command -> Use: value=[1 to 20]")

    # RCPN
    def rcpn(self, file=None):
        '''Command for RCPN - Recall Panel Command'''
        try:
            if file is not None:
                if type(file) is str and str(file).upper().find('.SET') != -1:
                    self.osc.write("RCPN DISK,UDSK,FILE,'{}'".format(file.upper()))
                    return("Success. Recall Panel Command read from UDSK by FILE {}.".format(file.upper()))
                else:
                    raise Exception
            else: 
                raise Exception
        except:
            raise Exception("Invalid input for RCPN - Recall Panel Command -> Use: file='/{DIRECTORY}/{DOS_FILENAME.SET}'")
    
    # *RST
    def _rst(self):
        '''Command RST - Reset'''
        return(self.osc.write("*RST"))

    # RUN
    def run(self):
        '''Command RUN - Run execution'''
        return(self.osc.write("RUN"))

    # SAMPLE_NUM
    def sanu(self, channel=None):
        '''Query value from SANU - Sample Unit'''
        if channel is None:
            channel_list = []
            for set_channel in (range(1,(self.nchannels+1))):
                channel_list.append("C{}={}".format(set_channel,self.osc.query("SANU? C{}".format(set_channel))))
            return channel_list
        else:
            if channel in (range(1,(self.nchannels+1))):
                return(float(self.osc.query("SANU? C{}".format(str(channel)))))
            else:
                raise Exception("Invalid input for SANU - Sample Unit -> Use: channel=[1~{}]".format(str(self.nchannels)))

    # SAMPLE_RATE
    def sara(self):
        '''Query value from SARA - Sample Rate'''
        query_results = self.osc.query("SARA?")
        time.sleep(self.delay)
        sara_unit = {'G':1E9,'M':1E6,'K':1E3}
        for unit in sara_unit.keys():
            if query_results.find(unit) !=-1:
                sara_value = query_results.split(unit)
                sara_value = float(sara_value[0])*sara_unit[unit]
                break
        return float(sara_value)

    # SAMPLE_STATUS
    def sast(self):
        '''Query configuration from SAST - Sample Status'''
        query_results = self.osc.query("SAST?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))

    # *SAV
    def _sav(self, value=None):
        '''Command for *SAV - Save Panel Setup Command'''
        try:
            if value is not None:
                if value in range(1,21):
                    self.osc.write("*SAV {}".format(value))
                    return("Success. Save Panel Setup Command set to memory {}.".format(value))
                else:
                    raise Exception
            else: 
                raise Exception
        except:
            raise Exception("Invalid input for *SAV - Save Panel Setup Command -> Use: value=[1 to 20]")

    # SCREEN_DUMP
    def scdp(self):
        '''Command SCDP - Screen Dump'''
        chunk=self.osc.chunk_size
        self.osc.chunk_size = 1024*1024
        self.osc.write("SCDP")
        image=self.osc.read_raw()
        self.osc.chunk_size = chunk
        return(image)

    #SCREEN_SAVE
    def __scsv_get(self):
        '''Get configuration of SCSV - Screen Save'''
        query_results = self.osc.query("SCSV?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def scsv(self, value=None):
        '''Set configuration to SCSV - Screen Save'''
        if value is None:
            return(self.__scsv_get())
        else:
            try:
                if value.upper() in ('YES','NO'):
                    self.osc.write("SCSV {0}".format(value.upper()))
                    return("Success. Screen Save set to {0}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for SCSV - Screen Save -> Use: value=['YES' or 'NO']")

    # SETTO%50
    def set50(self):
        '''Command SET50 - Set at 50% of trigger level'''
        return(self.osc.write("SET50"))
    
    # SINXX_SAMPLE
    def __sxsa_get(self):
        '''Get configuration of SXSA - Sinx/X Sample'''
        query_results = self.osc.query("SXSA?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def sxsa(self, value=None):
        '''Set configuration to SXSA - Sinx/X Sample'''
        if value is None:
            return(self.__sxsa_get())
        else:
            try:
                if value.upper() in ('ON','OFF'):
                    self.osc.write("SXSA {}".format(value.upper()))
                    return("Success. Sinx/X Sample set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for SXSA - Sinx/X Sample -> Use: value=['ON' or 'OFF']")

    # SKEW
    def __skew_get(self, channel=None):
        '''Get configuration of SKEW - Skew Command'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:SKEW?".format(channel))
                    time.sleep(self.delay)
                    return(Oscilloscope.format_results(query_results))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for SKEW - Skew Command -> Use: channel=[1~{}]".format(self.nchannels))
    def skew(self, channel=None, value=None):
        '''Set configuration to SKEW - Skew Command'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__skew_get(set_channel)))
                return channel_list
            else:
                return self.__skew_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    if type(value) is str or type(value) is float:
                        if type(value) is str:
                            value=self.__indiscret_convert(self.__std(value))*1e9
                        if value >= -100.0 and value <= 100.0:
                            self.osc.write("C{}:SKEW {}".format(channel,value))
                            return("Success. Skew Command set to {}ns on channel {}.".format(value,channel))
                        else:
                            raise Exception
                    elif value in range(-100,101):
                        self.osc.write("C{}:SKEW {}".format(channel,value))
                        return("Success. Skew Command set to {}ns on channel {}.".format(value,channel))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for SKEW - Skew Command -> Use: channel=[1 to {}], value=[-100 to 100]ns".format(self.nchannels))

    # *SRE
    def __sre_get(self):
        '''Query from *SRE - Service Request Enable'''
        query_results = self.osc.query("*SRE?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def _sre(self, value=None):
        '''Command for *SRE - Service Request Enable'''
        if value is None:
            return(self.__sre_get())
        else:
            try:
                if value in range(0,256):
                    self.osc.write("*SRE {}".format(value))
                    return("Success. Service Request Enable set to {0}.".format(value))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for *SRE - Service Request Enable -> Use: value=[0 to 255]")

    # *STB?
    def _stb(self):
        '''Query *STB? - Status Register'''
        query_results = self.osc.query("*STB?")
        time.sleep(self.delay)
        return(int(query_results))
    
    # STOP
    def stop(self):
        '''Command STOP - Stop Acquisition'''
        return(self.osc.write("STOP"))

    # STORE
    def sto(self, trace=None, dest=None):
        '''Command for STO - Store'''
        try:
            if trace.upper() in ('C1','C2','TA','TB','ALL_DISPLAYED') and dest.upper() in ('M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','UDSK'):
                self.osc.write("STO {},{}".format(trace.upper(),dest.upper()))
                return("Success. Store set trace {} to memory {}.".format(trace.upper(),dest.upper()))
            else: 
                raise Exception
        except:
            raise Exception("Invalid input for STO - Store -> Use: trace=['C1','C2','TA','TB' or 'ALL_DISPLAYED'], dest=['M1' ~ 'M10' or 'UDSK']")

    # STORE_PANEL
    def stpn(self, file=None):
        '''Command for STPN - Store Panel Command'''
        try:
            if file is not None:
                if type(file) is str and str(file).upper().find('.SET') != -1:
                    self.osc.write("STPN DISK,UDSK,FILE,'{}'".format(file.upper()))
                    return("Success. Store Panel Command save to UDSK on FILE {}.".format(file.upper()))
                else:
                    raise Exception
            else: 
                raise Exception
        except:
            raise Exception("Invalid input for STPN - Store Panel Command -> Use: file='/{DIRECTORY}/{DOS_FILENAME.SET}'")

    # STORE_SETUP
    def __stst_get(self):
        '''Query from STST - Store Setup'''
        query_results = self.osc.query("STST?")
        time.sleep(self.delay)
        return(query_results)
    def stst(self, trace=None, dest=None):
        '''Command for STST - Store Setup'''
        if trace is None and dest is None:
            return(self.__stst_get())
        else:
            try:
                if trace.upper() in ('C1','C2','ALL_DISPLAYED') and dest.upper() in ('M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','UDSK'):
                    self.osc.write("STST {},{}".format(trace.upper(),dest.upper()))
                    return("Success. Store Status set trace {} to memory {}.".format(trace.upper(),dest.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for STO - Store -> Use: trace=['C1','C2' or 'ALL_DISPLAYED'], dest=['M1' ~ 'M10' or 'UDSK']")

    # TEMPLATE
    def tmpl(self):
        '''Query TMPL - Template'''
        query_results = self.osc.query("TMPL?")
        time.sleep(self.delay)
        return(query_results)


    # TIME_DIV
    def __tdiv_get(self, discret=False):
        '''Get value of TDIV - Time Div'''
        query_results = self.osc.query("TDIV?")
        time.sleep(self.delay)
        if discret:
            return self.__discret_convert(float(query_results))
        else:
            return float(query_results)
    def tdiv(self, value=None):
        '''Set value of TDIV - Time Div'''
        if value is None:
            return self.__tdiv_get()
        else:
            try:
                if type(value) is str:
                    if value in ('2.5ns','5ns', '10ns', '25ns', '50ns', '100ns', '250ns', '500ns', '1us', '2.5us', '5us', '10us', '25us',
                                '50us', '100us', '250us', '500us', '1ms', '2.5ms', '5ms', '10ms', '25ms', '50ms', '100ms', '250ms',
                                '500ms', '1s', '2.5s', '5s', '10s', '25s', '50s'):
                        self.osc.write("TDIV {}".format(value))
                        return("Success. Time Div to {}.".format(value))
                    else:
                        raise Exception
                elif value is True:
                     return self.__tdiv_get(True)
                else:
                    if value >= 2.50E-9 and value <= 50:
                        self.osc.write("TDIV {}".format(value))
                        return("Success. Time Div to {}.".format(value))
                    else:
                        raise Exception
            except:
                raise Exception("Invalid input for TDIV - Time Div -> Use:\n \
                                value=['2.5ns','5ns', '10ns', '25ns', '50ns', '100ns', '250ns', '500ns',\n\
                                '1us', '2.5us', '5us', '10us', '25us', '50us', '100us', '250us', '500us',\n\
                                '1ms', '2.5ms', '5ms', '10ms', '25ms', '50ms', '100ms', '250ms', '500ms',\n\
                                '1s', '2.5s', '5s', '10s', '25s', '50s']")

    # TRACE
    def __tra_get(self, channel=None):
        '''Get configuration of TRA - Trace'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:TRA?".format(channel))
                    time.sleep(self.delay)
                    return(Oscilloscope.format_results(query_results))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for TRA - Trace -> Use: channel=[1~{}]".format(self.nchannels))
    def tra(self, channel=None, value=None):
        '''Set configuration to TRA - Trace'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__tra_get(set_channel)))
                return channel_list
            else:
                return self.__tra_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))) and value.upper() in('ON','OFF'):
                    self.osc.write("C{}:TRA {}".format(channel,value.upper()))
                    return("Success. Trace set to {} on channel {}.".format(channel,str(value.upper())))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for TRA - Trace -> Use: channel=[1 to {}], value=['ON' or 'OFF']".format(self.nchannels))

    # *TRG
    def _trg(self):
        '''Command *TRG - Trigger'''
        return(self.osc.write("*TRG"))

    # TRIG_COUPLING
    def __trcp_get(self):
        '''Get configuration of TRCP - Trigger Coupling'''
        return(self.osc.query("TRCP?"))
    def trcp(self, value=None):
        '''Set configuration to TRCP - Trigger Coupling'''
        if value is None:
            return self.__trcp_get()
        else:
            try:
                if value.upper() in('AC','DC','HFREJ','LFREJ'):
                    self.osc.write("TRCP {}".format(value.upper()))
                    return("Success. Trigger Coupling set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for TRCP - Trigger Coupling -> Use: value=['AC','DC','HFREJ' or 'LFREJ']")

    #TRIG_DELAY
    def __trdl_get(self):
        '''Get configuration of TRDL - Trigger Delay'''
        query_results = self.osc.query("TRDL?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results).lower())
    def trdl(self, value=None):
        '''Set configuration to TRDL - Trigger Delay'''
        if value is None:
            return(self.__trdl_get())
        else:
            try:
                if type(value) is str:
                    value=self.__indiscret_convert(self.__std(value))
                if self.__trdl_onlimits(value):
                    self.osc.write("TRDL {}".format(value))
                    return("Success. Trigger Delay set to {}.".format(self.__discret_convert(value)))
                else:
                    minmax=self.__trdl_onlimits(value,True)
                    min=self.__discret_convert(minmax[0])
                    max=self.__discret_convert(minmax[1])

                    raise Exception(min,max)
            except:
                raise Exception("Invalid input for TRDL - Trigger Delay -> Use: values=[ between {} and {} ]".format(min,max))
    def __trdl_onlimits(self, value=None, range=False):
        tdiv=self.__discret_convert(self.tdiv())
        for trdl_limits in self.__trdl_limits():
            if trdl_limits[0].find(tdiv) == 0:
                break
        if range:
            return(trdl_limits[1],trdl_limits[2]) 
        else:
            if value >= trdl_limits[1] and value <= trdl_limits[2]:
                return True
            else:
                return False
    def __trdl_limits(self):
        return(\
        # TDIV       MIN(Seg)      MAX(Seg)
        [['2.50ns', -4.31160e-06, 3.47550e-07],\
        ['5ns'   , -7.12350e-06, 6.95100e-07],\
        ['10ns'  , -1.05704e-05, 1.39020e-06],\
        ['25ns'  , -1.48945e-05, 3.47540e-06],\
        ['50ns'  , -1.72459e-05, 6.95100e-06],\
        ['100ns' , -2.04799e-05, 1.39019e-05],\
        ['250ns' , -1.97399e-05, 3.47550e-05],\
        ['500ns' , -3.94799e-05, 6.95100e-05],\
        ['1us'   , -4.09599e-05, 0.000139020],\
        ['2.50us' , -0.000102400, 0.000347550],\
        ['5us'   , -0.000102400, 0.000695100],\
        ['10us'  , -0.000102400, 0.001390200],\
        ['25us'  , -0.000406500, 0.003475500],\
        ['50us'  , -0.000813000, 0.006951001],\
        ['100us' , -0.002048000, 0.013902000],\
        ['250us' , -0.004065000, 0.034755000],\
        ['500us' , -0.008130000, 0.069510000],\
        ['1ms'   , -0.020479990, 0.139020000],\
        ['2.50ms' , -0.040650000, 0.347550000],\
        ['5ms'   , -0.081300000, 0.695100000],\
        ['10ms'  , -0.204800000, 1.390200000],\
        ['25ms'  , -0.406500000, 3.475500000],\
        ['50ms'  , -0.813000000, 6.951001000],\
        ['100ms' , -0.800000000, 0.800000000],\
        ['250ms' , -2.000000000, 2.000000000],\
        ['500ms' , -4.000000000, 4.000000000],\
        ['1s'    , -8.000000000, 8.000000000],\
        ['2.50s'  , -20.00000000, 20.00000000],\
        ['5s'    , -40.00000000, 40.00000000],\
        ['10s'   , -80.00000000, 80.00000000],\
        ['25s'   , -200.0000000, 200.0000000],\
        ['50s'   , -400.0000000, 400.0000000]])

    # TRIG_LEVEL
    def __trlv_get(self, channel=None):
        '''Get configuration of TRLV - Trigger Level'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:TRLV?".format(channel))
                elif channel.upper() in ('EX', 'EX5'):
                    query_results = self.osc.query("{}:TRLV?".format(channel))
                else:
                    raise Exception
                time.sleep(self.delay)
                return(Oscilloscope.format_results(query_results))
            except:
                raise Exception("Invalid input for TRLV - Trigger Level -> Use: channel=[1 to {}, 'EX' or 'EX5']".format(self.nchannels))
    def trlv(self, channel=None, value=None):
        '''Set configuration to TRLV - Trigger Level'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__trlv_get(set_channel)))
                for set_channel in ('EX', 'EX5'):
                    channel_list.append("{}={}".format(set_channel,self.__trlv_get(set_channel)))
                return channel_list
            else:
                return self.__trlv_get(channel)
        else:
            if type(value) is str:
                value=self.__indiscret_convert(self.__std(value),'V')
            valuemin=-(self.vdiv(channel)*6)-self.ofst(channel)
            valuemax=self.vdiv(channel)*6-self.ofst(channel)
            if self.ofst(channel) > 0:
                valuemin=-(self.vdiv(channel)*6)
            elif self.ofst(channel) < 0:
                valuemax=self.vdiv(channel)*6
            if value >= valuemin and value <= valuemax:
                if channel in (range(1,(self.nchannels+1))):
                    self.osc.write("C{}:TRLV {}".format(channel,value))
                    return("Success. Trigger Level set to {} on channel {}.".format(self.__discret_convert(value,'V'),channel))
                elif channel.upper() in ('EX', 'EX5'):
                    self.osc.write("{}:TRLV {}".format(channel.upper(),value))
                    return("Success. Trigger Level set to {} on channel {}.".format(self.__discret_convert(value,'V'),channel.upper()))
                else:
                    raise Exception("Invalid input for TRLV - Trigger Level -> Use: channel=[1 to {}, 'EX' or 'EX5'], value=[-6DIV * volt/div to +6DIV volt/div]".format(self.nchannels))
            else:
                raise Exception("Invalid input for TRLV - Trigger Level -> Use: value=[{}V to {}V]".format(valuemin,valuemax))

    # TRIG_MODE
    def __trmd_get(self):
        '''Get configuration of TRMD - Trigger Mode'''
        query_results = self.osc.query("TRMD?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def trmd(self, value=None):
        '''Set configuration to TRMD - Trigger Mode'''
        if value is None:
            return(self.__trmd_get())
        else:
            try:
                if value.upper() in ('AUTO','NORM','SINGLE','STOP'):
                    self.osc.write("TRMD {}".format(value.upper()))
                    return("Success. Trigger Mode set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for TRDM - Trigger Mode -> Use values=['AUTO','NORM','SINGLE' or 'STOP']")

    # TRIG_SELECT
    def __trse_get(self, trigger=None):
        '''Get configuration of TRSE - Trigger Select'''
        if trigger is None:
            query_results = self.osc.query("TRSE?")
        else:
            self.osc.write("TRSE {}".format(trigger.upper()))
            query_results = self.osc.query("TRSE?")
        return(query_results)
    def trse(self, trigger=None, source=None, ht=None, hv=None, sync=None, line=None, char=None, pol=None, vert=None):
        '''Set configuration to TRSE - Trigger Select'''
        if trigger is None:
            return self.__trse_get()
        else:
            if trigger.upper() in ('EDGE','GLIT','SLEW','TV'):
                if trigger.upper() == 'EDGE':
                    if source is not None:
                        if ht is not None:
                            hv=ht    
                        ht='TI'
                        try:
                            if type(source) is int:
                                if source in (range(1,(self.nchannels+1))):
                                    source="C{}".format(source)
                                else:
                                    raise Exception 
                            elif type(source) is str:
                                if source.upper() in ('EX', 'EX5', 'LINE'):
                                    source="{}".format(source.upper())
                                else:
                                    raise Exception
                            else:
                                raise Exception
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: source=[1 to {0}, 'EX', 'EX5' or 'LINE']".format(self.nchannels))
                        try:
                            if hv is not None:
                                if type(hv) is str:
                                    if self.__indiscret_convert(self.__std(hv)) >= self.__indiscret_convert('100nS') and self.__indiscret_convert(self.__std(hv)) <= self.__indiscret_convert('1.5S'):
                                        pass
                                    else:
                                        raise Exception
                                elif type(hv) is int or type(hv) is float:
                                    if float(hv) >= 100e-9 and float(hv) <= 1.5:
                                        hv=self.__discret_convert(hv)
                                    else:
                                        raise Exception
                            else:
                                hv=self.__trse_get(trigger).split(',')[-1]
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: hv=[between '100ns' and '1.5s']")
                        self.osc.write("TRSE {},SR,{},HT,{},HV,{}".format(trigger.upper(),source.upper(),ht,hv.upper()))
                        return("Success. Trigger Select set to Trigger={}, Source={}, HT={}, HV={}.".format(trigger.upper(),source.upper(),ht,hv.upper()))
                    else:
                        return self.__trse_get(trigger)
                elif trigger.upper() == 'GLIT':
                    if source is not None:
                        try:
                            if type(source) is int:
                                if source in (range(1,(self.nchannels+1))):
                                    source="C{}".format(source)
                                else:
                                    raise Exception 
                            elif type(source) is str:
                                if source.upper() in ('EX', 'EX5'):
                                    source="{}".format(source.upper())
                                else:
                                    raise Exception
                            else:
                                raise Exception
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: source=[1 to {0}, 'EX' or 'EX5']".format(self.nchannels))
                        try:
                            if ht is not None:
                                if ht.upper() not in ('PS', 'PL', 'PE'):
                                    raise Exception
                            else:
                                ht=self.__trse_get(trigger).split(',')[-3]
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: ht=['PS', 'PL' or 'PE']".format(self.nchannels))
                        try:
                            if hv is not None:
                                if type(hv) is str:
                                    if self.__indiscret_convert(self.__std(hv)) < self.__indiscret_convert('20nS') or self.__indiscret_convert(self.__std(hv)) > self.__indiscret_convert('10S'):
                                        raise Exception
                                elif type(hv) is int or type(hv) is float:
                                    if float(hv) >= 20e-9 and float(hv) <= 10:
                                        hv=self.__discret_convert(hv)
                                    else:
                                        raise Exception
                            else:
                                hv=self.__trse_get(trigger).split(',')[-1]
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: hv=[between '20ns' and '10s']")
                        self.osc.write("TRSE {},SR,{},HT,{},HV,{}".format(trigger.upper(),source.upper(),ht.upper(),hv.upper()))
                        return("Success. Trigger Select set to Trigger={}, Source={}, HT={}, HV={}.".format(trigger.upper(),source.upper(),ht.upper(),hv.upper()))
                    else:
                        return self.__trse_get(trigger)
                elif trigger.upper() == 'SLEW':
                    if source is not None:
                        try:
                            if type(source) is int:
                                if source in (range(1,(self.nchannels+1))):
                                    source="C{}".format(source)
                                else:
                                    raise Exception 
                            elif type(source) is str:
                                if source.upper() in ('EX', 'EX5'):
                                    source="{}".format(source.upper())
                                else:
                                    raise Exception
                            else:
                                raise Exception
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: source=[1 to {0}, 'EX' or 'EX5']".format(self.nchannels))
                        if ht is not None:
                            if ht.upper() in ('UP', 'DOWN', 'BOTH'):
                                vert=ht
                        if vert is not None:
                            try:
                                if vert.upper() not in ('UP', 'DOWN', 'BOTH'):
                                        raise Exception
                                else:
                                    self.osc.write("TRSE {},SR,{},VERT,{}".format(trigger.upper(),source.upper(),vert.upper()))
                                    return("Success. Trigger Select set to Trigger={}, Source={}, Vert={}".format(trigger.upper(),source.upper(),vert.upper()))
                            except:
                                raise Exception("Invalid input for TRSE - Trigger Select -> Use: vert=['UP', 'DOWN' or 'BOTH']")
                        try:
                            if ht is not None:
                                if ht.upper() not in ('IS', 'IL', 'IE'):
                                    raise Exception
                            else:
                                ht=self.__trse_get(trigger).split(',')[-3]
                                return(ht)
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: ht=['IS', 'IL' or 'IE']")
                        try:
                            if hv is not None:
                                if type(hv) is str:
                                    if self.__indiscret_convert(self.__std(hv)) < self.__indiscret_convert('20nS') or self.__indiscret_convert(self.__std(hv)) > self.__indiscret_convert('10S'):
                                        raise Exception
                                elif type(hv) is int or type(hv) is float:
                                    if float(hv) >= 20e-9 and float(hv) <= 10:
                                        hv=self.__discret_convert(hv)
                                    else:
                                        raise Exception
                            else:
                                hv=self.__trse_get(trigger).split(',')[-1]
                                return(hv)
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: hv=[between '20ns' and '10s']")
                        self.osc.write("TRSE {},SR,{},HT,{},HV,{},".format(trigger.upper(),source.upper(),ht.upper(),hv.upper()))
                        return("Success. Trigger Select set to Trigger={}, Source={}, HT={}, HV={}.".format(trigger.upper(),source.upper(),ht.upper(),hv.upper()))
                    else:
                        return self.__trse_get(trigger)
                elif trigger.upper() == 'TV':
                    if source is not None:
                        try:
                            if type(source) is int:
                                if source in (range(1,(self.nchannels+1))):
                                    source="C{}".format(source)
                                else:
                                    raise Exception 
                            elif type(source) is str:
                                if source.upper() in ('EX', 'EX5'):
                                    source="{}".format(source.upper())
                                else:
                                    raise Exception
                            else:
                                raise Exception
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: source=[1 to {0}, 'EX' or 'EX5']".format(self.nchannels))
                        try:
                            if ht is not None:
                                if ht.upper() not in ('NTSC', 'PALSEC'):
                                    raise Exception
                                else:
                                    char=ht
                            elif char is not None:
                                if char.upper() not in ('NTSC', 'PALSEC'):
                                    raise Exception
                            else:                           
                                char=self.__trse_get(trigger).split(',')[4]
                                return char
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: ['NTSC' or 'PALSEC'] or char=['NTSC' or 'PALSEC']")
                        try:
                            if hv is not None:
                                if hv.upper() not in ('PO','NE'):
                                    raise Exception
                                else:
                                    pol=hv
                            elif pol is not None:
                                if pol.upper() not in ('PO', 'NE'):
                                    raise Exception
                            else:
                                pol=self.__trse_get(trigger).split(',')[6]
                                return pol
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: hv=['PO' or 'NE']")
                        try:
                            if sync is not None:
                                if sync.upper() not in ('AL','LN','OF','EF'):
                                    raise Exception
                            else:
                                sync=self.__trse_get(trigger).split(',')[8]
                                return sync
                        except:
                            raise Exception("Invalid input for TRSE - Trigger Select -> Use: sync=['AL','LN','OF' or 'EF']")
                        if line is not None:
                            try:
                                if sync.upper() != 'LN':
                                    raise Exception
                            except:
                                raise Exception("Invalid input for TRSE - Trigger Select -> LINE only valid from SYNC=LN")
                            try:
                                if char.upper() == 'NTSC':
                                    if line not in range(1,526):
                                        raise Exception
                            except:
                                raise Exception("Invalid input for TRSE - Trigger Select -> LINE must be between 1 and 525 for CHAR=NTSC")
                            try:
                                if char.upper() == 'PALSEC':
                                    if line not in range(1,626):
                                        raise Exception
                            except:
                                raise Exception("Invalid input for TRSE - Trigger Select -> LINE must be between 1 and 625 for CHAR=PALSEC")
                            self.osc.write("TRSE {},SR,{},CHAR,{},POL,{},SYNC,{},LINE,{}".format(trigger.upper(),source.upper(),char.upper(),pol.upper(),sync.upper(),line))
                            return("Success. Trigger Select set to Trigger={}, Source={}, CHAR={}, POL={}, SYNC={}, LINE={}.".format(trigger.upper(),source.upper(),char.upper(),pol.upper(),sync.upper(),line))
                        else:
                            try:
                                if sync.upper() == 'LN':
                                    self.osc.write("TRSE {},SYNC,LN".format(trigger.upper()))
                                    if self.__trse_get(trigger).split(',')[8] == 'LN':
                                        return(self.__trse_get(trigger).split(',')[10])
                                    else:
                                        raise Exception
                                else:
                                    self.osc.write("TRSE {},SR,{},CHAR,{},POL,{},SYNC,{}".format(trigger.upper(),source.upper(),char.upper(),pol.upper(),sync.upper()))
                                    return("Success. Trigger Select set to Trigger={}, Source={}, CHAR={}, POL={}, SYNC={}.".format(trigger.upper(),source.upper(),char.upper(),pol.upper(),sync.upper()))
                            except:
                                raise Exception("Invalid input for TRSE - Trigger Select -> LINE must be between: 1 and 525 for CHAR=NTSC or 1 and 625 for CHAR=PALSEC")
                    else:
                        return self.__trse_get(trigger)
            else:
                raise Exception("Invalid input for TRSE - Trigger Select -> Use: trigger=['EDGE','GLIT','SLEW','TV']")

    # TRIG_SLOPE
    def __trsl_get(self):
        '''Get configuration of TRSL - Trigger Slope'''
        return(self.osc.query("TRSL?"))
    def trsl(self, value=None):
        '''Set configuration to TRSL - Trigger Slope'''
        if value is None:
            return self.__trsl_get()
        else:
            try:
                if value.upper() in ('POS','NEG','WINDOW'):
                    self.osc.write("TRSL {}".format(value.upper()))
                    return("Success. Trigger Slope set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for TRSL - Trigger Slope -> Use: value=['POS','NEG' or 'WINDOW']")

    # UNIT
    def __unit_get(self, channel=None):
        '''Get configuration of UNIT - Unit'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:UNIT?".format(channel))
                    time.sleep(self.delay)
                    return(Oscilloscope.format_results(query_results))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for UNIT - Unit -> Use: channel=[1~{}]".format(self.nchannels))
    def unit(self, channel=None, value=None):
        '''Set configuration to UNIT - Unit'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__unit_get(set_channel)))
                return channel_list
            else:
                return self.__unit_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))) and value.upper() in('A','V'):
                    self.osc.write("C{}:UNIT {}".format(channel,value.upper()))
                    return("Success. Unit set to {} on channel {}.".format(value.upper(),channel))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for UNIT - Unit -> Use: channel=[1 to {}], value=['A' or 'V']".format(self.nchannels))

    # VERTICAL
    def __vtcl_get(self, channel=None):
        '''Get configuration of VTCL - Vertical Control'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:VTCL?".format(channel))
                    time.sleep(self.delay)
                    highpos_LVL=str(float(query_results.split(',')[0])*self.vdiv(channel)/50)+'V'
                    lowpos_LVL=str(float(query_results.split(',')[1])*self.vdiv(channel)/50)+'V'
                    return(highpos_LVL,lowpos_LVL)
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for VTCL - Vertical Control -> Use: channel=[1~{}]".format(self.nchannels))
    def vtcl(self, channel=None, value=None, vert=None):
        '''Set configuration to VTCL - Vertical Control'''
        value_discret=None
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__vtcl_get(set_channel)))
                return channel_list
            else:
                return self.__vtcl_get(channel)
        else:
            if channel in (range(1,(self.nchannels+1))):
                if type(value) is str:
                    value_discret=value
                    value_from_str=self.__indiscret_convert(self.__std(value),'V')
                    value_min=-(self.vdiv(channel)/50)*100
                    value_max=(self.vdiv(channel)/50)*100
                    if value_from_str >= value_min and value_from_str <= value_max:
                        value=int((value_from_str/self.vdiv(channel))*50)
                    else:
                        raise Exception("Invalid input for VTCL - Vertical Control -> The value must be between {}V and {}V".format(value_min,value_max))
                elif type(value) is float:
                    print("is float")
                    value_discret=self.__discret_convert(value,'V')
                    value_min=-(self.vdiv(channel)/50)*100
                    value_max=(self.vdiv(channel)/50)*100
                    if value >= value_min and value <= value_max:
                        value=int((value/self.vdiv(channel))*50)
                    else:
                        raise Exception("Invalid input ({}) for VTCL - Vertical Control -> The value must be between {} and {}".format(value,value_min,value_max))
            try:
                if channel in (range(1,(self.nchannels+1))) and value in range(-100,101):
                    if vert is not None:
                        if value_discret is None:
                            # value_discret=str(value)+"pts"
                            value_discret=self.__discret_convert(value*self.vdiv(channel)/50,'V')
                        if vert.upper() in ('UP', 'DOWN', 'BOTH'):
                            self.trse('slew',channel,vert=vert.upper())
                        else:
                            raise Exception
                        self.osc.write("C{}:VTCL {}".format(channel,value))
                        return("Success. Vertical Control set to {} pts ({}) on channel {} in vert {}.".format(value,value_discret,channel,vert.upper()))
                    else:
                        raise Exception
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for VTCL - Vertical Control -> Use: channel=[1 to {}], value=[-100 up to 100], vert=['UP','DOWN' or 'BOTH']".format(self.nchannels))

    # VOLT_DIV
    def __vdiv_get(self, channel=None):
        '''Get value of VDIV - Volt Div'''
        if channel is not None:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    query_results = self.osc.query("C{}:VDIV?".format(channel))
                    time.sleep(self.delay)
                    return float(query_results)
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for VDIV - Volt Div -> Use: channel=[1~{}]".format(self.nchannels))
    def vdiv(self, channel=None, value=None):
        '''Set value of VDIV - Volt Div'''
        if value is None:
            if channel is None:
                channel_list=[]
                for set_channel in (range(1,(self.nchannels+1))):
                    channel_list.append("C{}={}".format(set_channel,self.__vdiv_get(set_channel)))
                return channel_list
            else:
                return self.__vdiv_get(channel)
        else:
            try:
                if channel in (range(1,(self.nchannels+1))):
                    if type(value) is str:
                        value=self.__std(value)
                        if value in ('2mV', '5mV', '10mV', '20mV', '50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', '10V'):
                            self.osc.write("C{}:VDIV {}".format(channel,value))
                            return("Success. Volt Div to {} on channel {}.".format(value,channel))
                        else:
                            raise Exception
                    else:
                        if value >= 0.002 and value <= 10:
                            self.osc.write("C{}:VDIV {}".format(channel,value))
                            return("Success. Volt Div to {}V on channel {}.".format(value,channel))
                        else:
                            raise Exception
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for VDIV - Volt Div -> Use: channel=[1 to {}], value=['2mV', '5mV', '10mV', '20mV', '50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V' or '10V']".format(self.nchannels))

    # WAIT
    def wait(self, time=None):
        '''Command WAIT - Wait complete acquisition'''
        if time is None:
            return(self.osc.write("WAIT".format(time)))
        else:
            return(self.osc.write("WAIT {}".format(time)))

    # WAVEFORM
    def wf(self, channel=None):
        '''Get data of WF - Waveform'''
        if channel in (range(1,(self.nchannels+1))):
            VDIV=self.vdiv(channel)
            OFST=self.ofst(channel)
            TDIV=self.tdiv()
            SARA=self.sara()
            try:
                self.osc.write("C{}:WF? DAT2".format(channel))
                recv = self.osc.read_raw()[15:-2]
                volt_value = []
                for data in recv:
                    if data > 127:
                        data = data - 255
                    volt_value.append(data)
                time_value = []
                for idx in range(0,len(volt_value)):
                    volt_value[idx] = volt_value[idx] / 25 * VDIV - OFST
                    time_data = -( (TDIV) * 14 / 2 ) + idx * (1/SARA)
                    time_value.append(time_data)
                return(time_value, volt_value)
            except:
                raise Exception("Failed to get WF - Waveform.")
        else:
            raise Exception("Invalid input for WF - Waveform -> Use: channel=[1 to {}]".format(self.nchannels))

    # WAVEFORM_SETUP
    def __wfsu_get(self):
        '''Get configuration of WFSU - Waveform Setup'''
        query_results = self.osc.query("WFSU?")
        time.sleep(self.delay)
        return Oscilloscope.format_results(query_results)
    def wfsu(self, sp=None, np=None, fp=None, sn=None):
        '''Set configuration to WFSU - Waveform Setup'''
        nones=0        
        if sp is None:
            sp = self.__wfsu_get()[0].split('=')[1]
            nones+=1
        else:
            if sp not in range(1,51):
                raise Exception("Invalid input for WFSU - Waveform Setup -> Use: sp=[1~50]")
        if np is None:
            np = self.__wfsu_get()[1].split('=')[1]
            nones+=1
        else:
            if np not in range(0,int(self.sanu(1))+1):
                raise Exception("Invalid input for WFSU - Waveform Setup -> Use: np=[0~{}]".format(int(self.sanu(1))))
        if fp is None:
            fp = self.__wfsu_get()[2].split('=')[1]
            nones+=1
        else:
            if fp not in range(0,20001):
                raise Exception("Invalid input for WFSU - Waveform Setup -> Use: fp=[0~20000]")
        if sn is None:
            sn = self.__wfsu_get()[3].split('=')[1]
            nones+=1
        else:
            if sn not in range(0,1001):
                raise Exception("Invalid input for WFSU - Waveform Setup -> Use: sn=[0~1000]")
        if nones == 4:
            return self.__wfsu_get()
        else:
            try:
                self.osc.write("WFSU SP,{},NP,{},FP,{},SN,{}".format(sp,np,fp,sn))
                return("Success. Waveform Setup sets to SP={}, NP={}, FP={}, SN={}.".format(sp,np,fp,sn))
            except:
                raise Exception("Failed to set Waveform Setup.")

    # XY_DISPLAY
    def __xyds_get(self):
        '''Get configuration of XYDS - XY Display'''
        query_results = self.osc.query("XYDS?")
        time.sleep(self.delay)
        return(Oscilloscope.format_results(query_results))
    def xyds(self, value=None):
        '''Set configuration to XYDS - XY Display'''
        if value is None:
            return(self.__xyds_get())
        else:
            try:
                if value.upper() in ('ON','OFF'):
                    if value.upper() == 'ON':
                        value_inv='off'
                    else:
                        value_inv='on'
                    self.osc.write("XYDS {}".format(value_inv.upper()))
                    return("Success. XY Display set to {}.".format(value.upper()))
                else:
                    raise Exception
            except:
                raise Exception("Invalid input for XYDS - XY Display -> Use: value=['ON' or 'OFF']")

    # UTILS FUNCTIONS
    @staticmethod
    def format_results(query_results):
        prepare_results=[]
        lenght_field=query_results.split(',')
        if len(lenght_field) > 1:
            keys_results=query_results.split(',')[0:len(query_results):2]
            values_results=query_results.split(',')[1:len(query_results):2]
            for results in range(0,len(keys_results)):
                prepare_results.append("{}={}".format(str(keys_results[results]).upper(),values_results[results]))
            return prepare_results
        else:
            try:
                return int(lenght_field[0])
            except:
                return str(lenght_field[0]).upper()

    def __discret_convert(self, value=None, unit='s', dp=2):
        if value >= 0:
            signal=''
        else:
            signal='-'
        value=abs(value)
        if unit not in ('%'):
            if value >= 1e24:
                # yotta
                value = value * 1e-24
                unit='Y'+unit
            elif value >= 1e21:
                # zetta
                value = value * 1e-21
                unit='Z'+unit
            elif value >= 1e18:
                # exa
                value = value * 1e-18
                unit='E'+unit
            elif value >= 1e15:
                # peta
                value = value * 1e-15
                unit='P'+unit
            elif value >= 1e12:
                # tera
                value = value * 1e-12
                unit='T'+unit
            elif value >= 1e9:
                # giga
                value = value * 1e-9
                unit='G'+unit
            elif value >= 1e6:
                # mega
                value = value * 1e-6
                unit='M'+unit
            elif value >= 1e3:
                # kilo
                value = value * 1e-3
                unit='K'+unit
            elif value >= 1e-0:
                # base
                value = value * 1e0
                unit=unit
            elif value >= 1e-3:
                # mili
                value = value * 1e3
                unit='m'+unit
            elif value >= 1e-6:
                # micro
                value = value * 1e6
                unit='u'+unit
            elif value >= 1e-9:
                # nano
                value = value * 1e9
                unit='n'+unit
            elif value >= 1e-12:
                # pico
                value = value * 1e12
                unit='p'+unit
            elif value >= 1e-15:
                # femto
                value = value * 1e15
                unit='f'+unit
            elif value >= 1e-18:
                # atto
                value = value * 1e18
                unit='a'+unit
            elif value >= 1e-21:
                # zepto
                value = value * 1e21
                unit='z'+unit
            elif value >= 1e-24:
                # yocto
                value = value * 1e24
                unit='y'+unit
        if dp == 2:
            if value % 1 > 0.0000001:
                return "{}{:.2f}{}".format(signal,float(value),unit)
            else:
                return "{}{}{}".format(signal,int(value),unit)
        elif dp == 3:
            if unit == 'mHz':
                unit='Hz'
                value=value/1000
            value_str="{:.4f}".format(float(value))
            if len(unit) == 3:
                value_str=value_str[0:5]
            else:
                value_str=value_str[0:6]
            return "{}{}{}".format(signal,value_str,unit)
        else:
            return "{}{}{}".format(signal,int(value),unit)

    def __indiscret_convert(self, value, unit='s'):
        unit=unit.upper()
        mult={'Y':1e24,'Z':1e21,'E':1e18,'P':1e15,'T':1e12,'G':1e9,'M':1e6,'K':1e3,'m':1e-3,'u':1e-6,'n':1e-9,'p':1e-12,'f':1e-15,'a':1e-18,'z':1e-21,'y':1e-24}
        mixunit=[]
        mixvalue=[]
        for mix in mult.keys():
            mixunit.append(mix+unit)
            mixvalue.append(mult[mix])
        multunit=dict(zip(mixunit,mixvalue))
        for mu in multunit.keys():
            if value.find(mu) != -1:
                valueconvert=float(value.split(mu)[0]) * multunit[mu]
                break
            valueconvert=value.split(unit)[0]
        return(float(valueconvert))

    def __std(self, value):
        valueval=value[0:len(value)-1]
        valueunit=value[-1].upper()
        return(valueval+valueunit)



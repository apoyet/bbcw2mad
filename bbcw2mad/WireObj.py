import numpy as np 
from pprint import pprint

class WireObj():
    '''
    This class is used to define a wire as an object. 
    Each wire compensator and its attribute will therefore be an instance of 
    this class. 
    '''
    
    def __init__(self, name, current, s_pos, x_pos, y_pos, nb, mad_inst, sequence, x_co=0, y_co=0, switch=0, sigx = (2*1e-3)/6, sigy = (2*1e-3)/6):
        self.name = name
        self.current = current
        self.s_pos = s_pos
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.nb = nb
        self.mad_inst = mad_inst
        self.sequence = sequence
        self.x_co = x_co
        self.y_co = y_co
        self.switch = switch
        self.sigx = sigx
        self.sigy = sigy
        self.xma = self.x_pos + self.x_co
        self.yma = self.y_pos + self.y_co
    
    # Print all attribute
    def describe(self):
        pprint(vars(self))
    
    # Modify/Add Attributes
    
    def update_transverse_position(self, x_w, y_w):
        '''
        Updates the transverse beam-wire distance of the considered wire.
        
        Args:
            x_w, y_w: floats, new transverse coordinates of the wire [in m]
        '''
        self.x_pos = x_w
        self.y_pos = y_w
        
    # Act on the wire in MADX
    def define_in_mad(self):
        '''
        Define the wire as element in its madx instance. 
        '''
        self.mad_inst.input(f'''
        ! Input current
        I_{self.name} := {self.current};
        I_{self.name}_N := on_{self.name}*{self.current}/(qelect*clight*{self.nb});
        ! Input position
        xma_{self.name} := {self.x_pos};
        yma_{self.name} := {self.y_pos};
        {self.name}: beambeam, charge:=-I_{self.name}_N, sigx={self.sigx}, sigy={self.sigy}, xma:=xma_{self.name}, yma:=yma_{self.name}, bbshape=1, bbdir=-1;
        ''')    
        
    def install_in_sequence(self):
        '''
        Install the wire in its sequence.
        ''' 
        self.mad_inst.input(f'''
        print, text="<<<< Installation of the wire {self.name} in sequence {self.sequence} >>>>>";
        use, sequence = {self.sequence};
        seqedit, sequence = {self.sequence};
        flatten;
        install, element={self.name}, at={self.s_pos};
        flatten;
        endedit;
        print, text="<<<< Installation done >>>>>";
        ''')
    
    def get_closed_orbit(self):
        '''
        Get the closed orbit and update the corresponding xma/yma of the bb element in madx.
        '''
        twiss_table = self.mad_inst.table.twiss_after_machine_tuning.dframe()
        #Update closed orbit at wire location 
        self.x_co = twiss_table.loc[self.name]['x']
        self.y_co = twiss_table.loc[self.name]['y']
        #New xma/yma
        self.xma = self.x_pos + self.x_co
        self.yma = self.y_pos + self.y_co
        #Input in mad
        self.mad_inst.input(f'''
        xma_{self.name} := {self.xma};
        yma_{self.name} := {self.yma};
        ''')
        
    def switch_wire(self, on=True):
        '''
        Switches the wire on/off
        Args:
            on: bool, set to True to turn it on
        '''
        if on:
            self.mad_inst.input(f'''on_{self.name}=1;''')
        else:
            self.mad_inst.input(f'''on_{self.name}=0;''')
    
    def print_lense(self):
        self.mad_inst.input(f'''
        system, "sed -i '$d' bb_lenses.dat"; ! removes last line: NEXT
        !! Print out the beam beam wire compensator lenses
        !option,-echo, -info;
        assign, echo=bb_lenses.dat;
        printf, text="{self.name} 0 %f %f %f %f %f", value= ({self.sigx})^2*1e6, ({self.sigx})^2*1e6, 1.0*({self.x_pos})*1e3, 1.0*({self.y_pos})*1e3, {self.name}->charge;
        print, text="NEXT";
        assign, echo=terminal;
        ''')

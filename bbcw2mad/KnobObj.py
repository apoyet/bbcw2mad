class KnobObj():
    '''
    A class containing the knobs compensating the tune shifts induced by the wires. 
    It assumes the configuration of LHC Run 3.
    '''
    def __init__(self,mad_inst):
        self.mad_inst = mad_inst
    
    def define_q4_ir1_knob(self, wire_ir1):
        '''
        Defines the know of the Q4 quadrupoles located in IR1.
        Args:
            wire_ir1: WireObj, one of the wires located in IR1
        '''
        kq4_r1_0 = self.mad_inst.eval('kq4.r1b1')
        kq4_l1_0 = self.mad_inst.eval('kq4.l1b1')
        self.mad_inst.input(f'''
        kq4.l1b1 := -5.339518293867958e-12*(on_{wire_ir1.name}*I_{wire_ir1.name}/{wire_ir1.y_pos**2}) + ({kq4_l1_0});
        kq4.r1b1 := -1.4733791126352925e-12*(on_{wire_ir1.name}*I_{wire_ir1.name}/{wire_ir1.y_pos**2}) + ({kq4_r1_0});
        ''')
    
    def define_q4_ir5_knob(self, wire_ir5):
        '''
        Defines the know of the Q4 quadrupoles located in IR5.
        Args:
            wire_ir5: WireObj, one of the wires located in IR5
        '''
        kq4_r5_0 = self.mad_inst.eval('kq4.r5b1')
        kq4_l5_0 = self.mad_inst.eval('kq4.l5b1')
        self.mad_inst.input(f'''
        kq4.l5b1 := 5.271370021700931e-12*(on_{wire_ir5.name}*I_{wire_ir5.name}/{wire_ir5.x_pos**2}) + ({kq4_l5_0});
        kq4.r5b1 := 1.3545529526911738e-12*(on_{wire_ir5.name}*I_{wire_ir5.name}/{wire_ir5.x_pos**2}) + ({kq4_r5_0});
        ''')

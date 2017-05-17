"""Performs Volatility Calculations based on data from FieldsDaily.py

** Run:
    py FieldsDaily.py first!

Indicators:
    VDelta: VIX-VXST
    Roll Yield: (VX1/VIX)-1
    Contango: (VX2/VX1)-1
    Contango Roll: (VX2/VIX)-1
    VRatio: VXV/VIX
    VXV Roll: (VXV/VX2)-1
    VCO (VIX Contango Oscillator): VIX - 45 + 1000 ((VXV2/VX1)-1)
    
    ----------------
    VTRO (VIX Term Roll Oscillator): 
        MA(3) of 
        (
        1000 *
        (
        (21/84) *
        (VIX/VXST - 1) +
        ((84 - T1 - T2) / 84) *
        (VX1/VIX - 1) +
        (T2/84) *
        (VX2/VX1 - 1) +
        (T1/84) *
        (VXV/VX2 - 1)
        )
        )

Returns: A file that displays the indicators provided in this class.
"""

"""Import all at top of module."""
import pandas as pd
import time

"""Read data from the file FieldsDaily produces."""
class TermStructureIndicators:
    def __init__(self):
        self.data = get_file()
        self.v_deltas = pd.Series(name='VDelta')
        self.roll_yields = pd.Series(name='Roll Yield')
        self.contangos = pd.Series(name='Contango')
        self.contango_rolls = pd.Series(name='Contango Roll')
        self.v_ratios = pd.Series(name='VRatio')
        self.vxv_rolls = pd.Series(name='VXV Roll')
        self.vcos = pd.Series(name='VCO (VIX Contango Oscillator)')
        self.total_fields = 7
        pass

    def print_data(self):
        print('{}'.format(self.data))
        pass

    def calculate_indicators(self):
        """Calculates indicators, making a Series for each in self.
        
        """
        for index, row in self.data.iterrows():
            self.v_deltas.set_value(index, self.v_delta(row['CBOE/VIX'], row['CBOE/VXST']))
            self.write_single_to_file(self.v_deltas, 'v_deltas')
            self.roll_yields.set_value(index, self.roll_yield(row['CHRIS/CBOE_VX1'], row['CBOE/VIX']))
            self.write_single_to_file(self.roll_yields, 'roll_yields')
            self.contangos.set_value(index, self.contango(row['CHRIS/CBOE_VX2'], row['CHRIS/CBOE_VX1']))
            self.write_single_to_file(self.contangos, 'contangos')
            self.contango_rolls.set_value(index, self.contango_roll(row['CHRIS/CBOE_VX2'], row['CBOE/VIX']))
            self.write_single_to_file(self.contango_rolls, 'contango_rolls')
            self.v_ratios.set_value(index, self.v_ratio(row['CBOE/VXV'], row['CBOE/VIX']))
            self.write_single_to_file(self.v_ratios, 'v_ratios')
            self.vxv_rolls.set_value(index, self.vxv_roll(row['CBOE/VXV'], row['CHRIS/CBOE_VX2']))
            self.write_single_to_file(self.vxv_rolls, 'vxv_rolls')
            self.vcos.set_value(index, self.vix_contango_oscillator(row['CBOE/VIX'], row['CHRIS/CBOE_VX2'], row['CHRIS/CBOE_VX1']))
            self.write_single_to_file(self.vcos, 'vcos')
            pass
        pass

    def v_delta(self, vix, vxst):
        return vix - vxst

    def roll_yield(self, vx1, vix):
        return (vx1/vix) - 1

    def contango(self, vx2, vx1):
        return (vx2/vx1) - 1

    def contango_roll(self, vx2, vix):
        return (vx2/vix) - 1

    def v_ratio(self, vxv, vix):
        return vxv / vix

    def vxv_roll(self, vxv, vx2):
        return (vxv/vx2) - 1

    def vix_contango_oscillator(self, vix, vx2, vx1):
        return (vix - 45 + 1000) * ((vx2 / vx1) - 1)

    def check_data_lengths(self):
        """Checks the lengths of each Series produced by indicator calculation.
        
        """
        print (self.v_deltas.size)
        print (self.roll_yields.size)
        print (self.contangos.size)
        print (self.contango_rolls.size)
        print (self.v_ratios.size)
        print (self.vxv_rolls.size)
        print (self.vcos.size)
        pass

    def combine_data(self):
        """Combines original data with calculated indicators.
        
        """
        self.data = pd.merge(self.data,
                             pd.DataFrame(self.v_deltas),
                             how='inner',
                             left_index=True,
                             right_index=True
                             )

        self.data = pd.merge(self.data,
                             pd.DataFrame(self.roll_yields),
                             how='inner',
                             left_index=True,
                             right_index=True
                             )

        self.data = pd.merge(self.data,
                             pd.DataFrame(self.contangos),
                             how='inner',
                             left_index=True,
                             right_index=True
                             )

        self.data = pd.merge(self.data,
                             pd.DataFrame(self.contango_rolls),
                             how='inner',
                             left_index=True,
                             right_index=True
                             )

        self.data = pd.merge(self.data,
                             pd.DataFrame(self.v_ratios),
                             how='inner',
                             left_index=True,
                             right_index=True
                             )

        self.data = pd.merge(self.data,
                             pd.DataFrame(self.vxv_rolls),
                             how='inner',
                             left_index=True,
                             right_index=True
                             )

        self.data = pd.merge(self.data,
                             pd.DataFrame(self.vcos),
                             how='inner',
                             left_index=True,
                             right_index=True
                             )
        pass

    def write_single_to_file(self, data, name):
        """Writes index data to CSV and Excel files ('./data/[timestr]_[name].csv').
        
        """
        time_str = time.strftime('%Y%m%d')
        data.to_csv('./data/' + time_str + name + '.csv', index=True)
        pass

    def write_to_files(self):
        """Writes data to CSV and Excel files ('./data').
        
        """
        print ('Writing to files..')
        time_str = time.strftime('%Y%m%d')
        self.data.to_csv('./data/' + time_str + '_term_structure_indicators.csv', index=True)
        #self.complete_data.to_excel('./data/' + time_str + '_fields_daily.xlsx', sheet_name='Fields Daily', index=True)
        print ('Complete!')
        pass

    pass

def get_file():
    """Read data from file provided by FieldsDaily.py.
    
    """
    time_str = time.strftime('%Y%m%d')
    dailies = pd.read_csv('./data/' + str(time_str) + '_fields_daily.csv')
    return dailies
    pass

indicators = TermStructureIndicators()
indicators.calculate_indicators()
indicators.combine_data()
indicators.write_to_files()

# scales.py functions
# ======
# scale_is_negative
# scale_is_divergent
# get_color_scale
# get_color_mapping
# get_color
# get_shape_scale
# get_frequency_scale
# get_shape
# get_frequency


import pytest
import numpy as np
import matplotlib.cm as cm

from vizent import scales

def test_scale_is_negative():

    values = (-1,0,1,2)
    assert scales.scale_is_negative(values) == False

    values = (-5,-3,-1,-10)
    assert scales.scale_is_negative(values) == True

    values = (0,)
    assert scales.scale_is_negative(values) == False

    values = (1,2,3,4,5)
    assert scales.scale_is_negative(values) == False


def test_scale_is_divergent():

    values = (-1,0,1,2)
    assert scales.scale_is_divergent(values) == True

    values = (-5,-3,-1,-10)
    assert scales.scale_is_divergent(values) == False

    values = (0,)
    assert scales.scale_is_divergent(values) == False

    values = (1,2,3,4,5)
    assert scales.scale_is_divergent(values) == False


def test_get_scale_bounds():

    values = (-1,0,1,2,3,4)
    max_val = None
    min_val = None
    scale_spread = None
    min_val, scale_spread = scales.get_scale_bounds(values, min_val, 
                                                    max_val, scale_spread)
    assert min_val == -1
    assert scale_spread == 5

    max_val = 5
    min_val = None
    scale_spread = None
    min_val, scale_spread = scales.get_scale_bounds(values, min_val, 
                                                    max_val, scale_spread)
    assert min_val == -1
    assert scale_spread == 6

    max_val = 5
    min_val = -5
    scale_spread = None
    min_val, scale_spread = scales.get_scale_bounds(values, min_val, 
                                                    max_val, scale_spread)
    assert min_val == -5
    assert scale_spread == 10

    max_val = 5
    min_val = None
    scale_spread = 8
    min_val, scale_spread = scales.get_scale_bounds(values, min_val, 
                                                    max_val, scale_spread)
    assert min_val == -3
    assert scale_spread == 8

    max_val = -5
    min_val = 5
    scale_spread = 10
    with pytest.raises(ValueError):
        min_val, scale_spread = scales.get_scale_bounds(values, min_val, 
                                                        max_val, scale_spread)



class TestColorScale:

    def setup_method(self):
        self.values =  (-2, 0, 1, 3, 5)
        self.max_val = 10
        self.min_val = -10
        self.n_colors = 4
        self.scale_spread = None

        self.scale_vals = scales.get_color_scale(self.values, self.max_val, 
                                                 self.min_val, self.n_colors, 
                                                 self.scale_spread)
    
    def test_get_color_scale(self):
    

        # Test we receive the right number of colors
        assert len(self.scale_vals) == self.n_colors

        # Check extreme values
        assert self.scale_vals[0] == self.min_val
        assert self.scale_vals[-1] == self.max_val

        # Check intervals are equal
        dif = [np.round(self.scale_vals[i+1] - self.scale_vals[i], 5) 
                for i in range(len(self.scale_vals)-1)]
        assert len(set(dif)) == 1


    def test_get_color_mapping(self):

        # metoffice colormap returns None
        mapping = scales.get_color_mapping(self.scale_vals, 'metoffice')
        assert mapping is None

        mapping = scales.get_color_mapping(self.scale_vals, 'autumn')
        assert type(mapping) == cm.ScalarMappable
        assert mapping.get_cmap().name == 'autumn'
        assert mapping.get_clim()[0] == self.min_val
        assert mapping.get_clim()[1] == self.max_val 

        mapping = scales.get_color_mapping(self.scale_vals, 
                                           'nonexistent_colormap')
        assert type(mapping) == cm.ScalarMappable
        assert mapping.get_cmap().name == 'viridis'
        assert mapping.get_clim()[0] == self.min_val
        assert mapping.get_clim()[1] == self.max_val


    def test_get_color(self):

        color = scales.get_color(29, 'metoffice', None)
        assert color == (0.9490196078431372, 0.4, 0.2196078431372549)

        color = scales.get_color(-36, 'metoffice', None)
        assert color == (0.0, 0.01568627450980392, 0.07450980392156863)

        with pytest.raises(IndexError):
            scales.get_color(40, 'metoffice', None)

        mapping = scales.get_color_mapping(self.scale_vals, 'autumn')
        color = scales.get_color(0.5, 'autumn', mapping)
        assert len(color) == 4

    

def test_get_shape_scale():

    values = (-7, -3, 0, 4, 5)
    max_val = None
    min_val = None
    n_shapes = 5
    scale_diverges = True
    scale_spread = None

    scale_vals = scales.get_shape_scale(values, max_val, min_val, n_shapes, 
                                 scale_diverges, scale_spread)

    assert scale_vals[0] == -7
    assert scale_vals[-1] == 7
    
    # same number of shapes on either side of 0
    assert len(scale_vals) == 2 * n_shapes - 1 
    
    # Check intervals are equal
    dif = [np.round(scale_vals[i+1] - scale_vals[i], 5) 
           for i in range(len(scale_vals)-1)]
    assert len(set(dif)) == 1


    values = (-9, -8.5, -3, -1)
    min_val = -12
    max_val = None
    n_shapes = 5
    scale_diverges = None
    scale_spread = None

    scale_vals = scales.get_shape_scale(values, max_val, min_val, n_shapes, 
                                 scale_diverges, scale_spread)

    assert scale_vals[0] == -12
    assert scale_vals[-1] == 0
    assert len(scale_vals) == n_shapes

    # Check intervals are equal
    dif = [np.round(scale_vals[i+1] - scale_vals[i], 5) 
           for i in range(len(scale_vals)-1)]
    assert len(set(dif)) == 1


    values = (4,6,7,10,15,21,35,39)
    max_val = 50
    min_val = 1
    n_shapes = 8
    scale_diverges = None
    scale_spread = None

    scale_vals = scales.get_shape_scale(values, max_val, min_val, n_shapes, 
                                 scale_diverges, scale_spread)

    assert scale_vals[0] == 1
    assert scale_vals[-1] == 50
    assert len(scale_vals) == 7

    # Check intervals are equal
    dif = [np.round(scale_vals[i+1] - scale_vals[i], 5) 
           for i in range(len(scale_vals)-1)]
    assert len(set(dif)) == 1

    
class TestFrequencyScale:

    def setup_method(self):

        self.values =  (-2, 0, 1, 3, 5)
        self.max_val = 10
        self.min_val = -10
        self.n_shapes = 4
        self.scale_spread = None
        self.scale_diverges = True

        self.scale_vals = scales.get_shape_scale(self.values, self.max_val, 
                                                 self.min_val, self.n_shapes, 
                                                 self.scale_diverges,
                                                 self.scale_spread)
        
        self.frequency_scale = scales.get_frequency_scale(self.scale_vals, 
                                                     self.scale_diverges)  
    
    def test_get_frequency_scale(self):

              
        assert self.frequency_scale == [12, 6, 3, 0, 3, 6, 12]


    def test_get_shape(self):
        for v in self.scale_vals:
            shape = scales.get_shape(v, shape_pos='saw', 
                                 divergent=self.scale_diverges, 
                                 shape_neg='sine')
            if v > 0:
                assert shape == 'saw'
            else:
                assert shape == 'sine'


    def test_get_frequency(self):

        d = {k:v for k, v in zip(self.scale_vals, self.frequency_scale)}
        for v in self.scale_vals:
            freq = scales.get_frequency(v, self.scale_vals, 
                                        self.frequency_scale, 
                                        interval_type="limit")
            
            assert d[v] == freq


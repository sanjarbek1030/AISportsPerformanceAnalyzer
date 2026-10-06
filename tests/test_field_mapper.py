from field_mapper import FieldMapper
def test_mapper():
    m=FieldMapper(105,68,[[0,0],[100,0],[100,100],[0,100]])
    x,y=m.image_to_field(50,50); assert 52<x<53 and 33<y<35

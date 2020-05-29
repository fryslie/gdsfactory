import pp
from pp.components.waveguide import waveguide


@pp.autoname
def dbr_cell(w1=0.5, w2=0.6, l1=0.2, l2=0.4, waveguide_function=waveguide):
    c = pp.Component()
    c1 = c << waveguide_function(length=l1, width=w1)
    c2 = c << waveguide_function(length=l2, width=w2)
    c2.connect(port="W0", destination=c1.ports["E0"])
    c.add_port("W0", port=c1.ports["W0"])
    c.add_port("E0", port=c2.ports["E0"])
    return c


@pp.autoname
def dbr(w1=0.5, w2=0.6, l1=0.2, l2=0.3, n=10, waveguide_function=waveguide):
    """ Distributed Bragg Reflector

           l1      l2
        <-----><-------->
                _________
        _______|

          w1       w2       ...  n times
        _______
               |_________
    """
    c = pp.Component()
    cell = dbr_cell(w1=w1, w2=w2, l1=l1, l2=l2, waveguide_function=waveguide_function)
    c.add_array(device=cell, columns=n, rows=1, spacing=(l1 + l2, 100))
    c.add_port("W0", port=cell.ports["W0"])
    p1 = c.add_port("E0", port=cell.ports["E0"])
    p1.midpoint = [(l1 + l2) * n, 0]
    return c


if __name__ == "__main__":
    c = dbr(w1=0.5, w2=0.6, l1=0.2, l2=0.3, n=10, with_pins=True)
    pp.show(c)

import h3
from fastkml import kml, styles
from pygeoif.geometry import Polygon

style = styles.Style(
    id="default",
    styles=[
        styles.PolyStyle(
            color="ff0000ff",
            color_mode="random",
            fill=0,
            outline=1,
        )
    ],
)

def get_polygon(cell):
    boundary = h3.cell_to_boundary(cell)
    boundary = [(point[1], point[0]) for point in boundary]

    p = kml.Placemark(ns, cell, cell, cell, style_url="#default")
    p.geometry = Polygon(boundary)
    return p

# Resolution: 9 = 0.2 nmi
# Resolution: 8 = 0.5 nmi
# Resolution: 7 = 1.3 nmi
# ...
# Resolution: 2 = 180 nmi
# Resolution: 1 = 468 nmi

k = kml.KML()
ns = "{http://www.opengis.net/kml/2.2}"

d = kml.Document(ns, "Demo", "Demo", "Demonstrate H3")
d.append_style(style)
k.append(d)

f = kml.Folder(ns, "demo-01", "demo-01", "Hierarchy")
d.append(f)

lat, lng = 39.758949, -84.191605
index_cell = h3.latlng_to_cell(lat, lng, 2)
f.append(get_polygon(index_cell))

grid = h3.grid_disk(index_cell, 1)
for cell in grid:
    f.append(get_polygon(cell))

subcells = h3.cell_to_children(index_cell, 3)
for cell in subcells:
    f.append(get_polygon(cell))

print(k.to_string(prettyprint=True))

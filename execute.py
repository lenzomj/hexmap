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

k = kml.KML()
ns = "{http://www.opengis.net/kml/2.2}"

d = kml.Document(ns, "docid", "doc name", "doc description")
d.append_style(style)
k.append(d)

f = kml.Folder(ns, "fid", "f name", "f description")
d.append(f)

# Resolution: 9 = 0.2 nmi
# Resolution: 8 = 0.5 nmi
# Resolution: 7 = 1.3 nmi
# ...
# Resolution: 2 = 180 nmi
# Resolution: 1 = 468 nmi

def get_polygon(cell):
    # index = h3.h3_to_string(cell)
    boundary = h3.cell_to_boundary(cell)
    boundary = [(point[1], point[0]) for point in boundary]

    p = kml.Placemark(ns, cell, cell, "Hex", style_url="#default")
    p.geometry = Polygon(boundary)
    return p


lat, lng = 39.758949, -84.191605
cell = h3.latlng_to_cell(lat, lng, 2)
f.append(get_polygon(cell))

grid = h3.grid_disk(cell, 1)
for unit in grid:
    f.append(get_polygon(unit))

print(k.to_string(prettyprint=True))

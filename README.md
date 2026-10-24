# BakeBuild Parametric Cookie Cutter Trio

Three original parametric 3D-printable cookie cutters modeled with OpenCascade (`build123d`), each within the 100x100x100mm build volume with a 3.0mm ergonomic press lip and 0.9mm tapered cutting blade.

1. `cutter_1_benzene_ring.step` (76.0 x 65.8 x 18 mm): hexagonal chemistry benzene ring cutter with internal bond stamp ribs.
2. `cutter_2_octagram_star.step` (90.4 x 90.4 x 18 mm): 8-pointed compass star cookie cutter.
3. `cutter_3_erlenmeyer_flask.step` (78.0 x 87.0 x 18 mm): laboratory Erlenmeyer flask cookie cutter.
4. `bakebuild_3_cookie_cutters_set.step`: combined 3-cutter assembly STEP file, laid out 95 mm apart for display (267 mm wide, so print the single cutters).

Sizes above are measured from the STEP files by `tools/inspect_cad.py`. The blade is designed at 0.9 mm; the thinnest wall measured in the plan sections is 0.41 mm (cutter 2), 0.77 mm (cutter 3) and 0.78 mm (cutter 1).

## Interactive inspector

`index.html` is a static page (3D viewer, plan view, measurements, downloads) served by GitHub Pages. To run it locally, serve the folder with `python3 -m http.server` and open `http://localhost:8000/`.

![BakeBuild CAD Render](./bakebuild_cutters_cad.png)

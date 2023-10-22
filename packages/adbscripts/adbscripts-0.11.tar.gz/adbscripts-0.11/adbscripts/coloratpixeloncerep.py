coloratpixelrep=r"""
widthheight=()
get_width_height widthheight
screen_width="${widthheight[0]}"
screen_height="${widthheight[1]}"
allrgbresults=()
x_coordinate=%s
y_coordinate=%s
while true; do
  get_rgb_value_at_coords $x_coordinate $y_coordinate "$screen_width" allrgbresults
  echo "${allrgbresults[0]},${allrgbresults[1]},${allrgbresults[2]},${allrgbresults[3]},${allrgbresults[4]}"
  unset allrgbresults
done
"""

coloratpixelonce=r"""
widthheight=()
get_width_height widthheight
screen_width="${widthheight[0]}"
screen_height="${widthheight[1]}"
allrgbresults=()
x_coordinate=%s
y_coordinate=%s
while true; do
  get_rgb_value_at_coords $x_coordinate $y_coordinate "$screen_width" allrgbresults
  echo "${allrgbresults[0]},${allrgbresults[1]},${allrgbresults[2]},${allrgbresults[3]},${allrgbresults[4]}"
  unset allrgbresults
done
"""
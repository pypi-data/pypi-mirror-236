getpixelcolor=r"""#!/bin/bash
get_width_height() {
    local -n stringarraywidthheight=$1
    stringarraywidthheight=()
    screen_width=$(wm size | grep -oE '[0-9]+x[0-9]+$')
    stringarraywidthheight=()
    dlim="x"
    splitstringdelim stringarraywidthheight "$screen_width" "$dlim"
    #echo "${stringarraywidthheight[0]}"
    #echo "${stringarraywidthheight[1]}"
}

splitstringdelim() {
    local -n stringarray="$1"
    inputstring=$2
    sep=$3
    allfilessplit=$(tr "$sep" '\r' <<<"$inputstring")
    array=($(echo $allfilessplit | sed 's/\r/\n/g'))
    for l in "${array[@]}"; do
        stringarray+=("$l")
    done
}

get_rgb_value_at_coords() {
    x_coord="$1"
    y_coord="$2"
    screen_width="$3"
    local -n rgbresults="$4"

    color_depth_bytes=4
    offset_bytes=$(((y_coord * screen_width + x_coord) * color_depth_bytes))
    offset_bytes=$((offset_bytes - color_depth_bytes))
    screencap /sdcard/dumpdata.tmp
    rgbdata=$(hexdump -n 4 -s $offset_bytes -e '"%07.8_Ad\n"' -e'4/1 "%d "" "' /sdcard/dumpdata.tmp)
    IFS=" " read -r r g b alpha offset_dec <<<"$rgbdata"
    coldepth=$((screen_width * color_depth_bytes))
    y=$((offset_dec / coldepth))
    x=$((offset_dec % coldepth))
    x=$((x / color_depth_bytes))
    rgbresults[0]="$x"
    rgbresults[1]="$y"
    rgbresults[2]="$r"
    rgbresults[3]="$g"
    rgbresults[4]="$b"
    rm -f /sdcard/dumpdata.tmp
    
}"""


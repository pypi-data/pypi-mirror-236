uiautomatorscriptbasis= r"""
while true; do
    outputuidump=$(uiautomator dump 2>&1 >/dev/null)
    if [ -n "$outputuidump" ]; then
        continue
    fi
    parse_uiautomator
    if [ "$print_csv" -gt 0 ]; then
        echo "$ALL_COLUMNS"
        for row in "${INDEX_ARRAY[@]}"; do
            for column in "${COLUMNS[@]}"; do
                indexarray=$((row + column))
                echo -n "\"${array_elements[indexarray]}\""
                if [ "$column" != "$ARRAY_MAX_INDEX" ]; then
                    echo -n ","
                fi
            done
            echo ""
        done
    fi
    unset INDEX_ARRAY
    unset array_elements
    sleep SLEEPTIME_REPLACE
done        
        """

uiautomatorscript=r"""
#!/bin/bash
INDEX=0
TEXT=1
RESOURCE_ID=2
CLASS=3
PACKAGE=4
CONTENT_DESC=5
CHECKABLE=6
CHECKED=7
CLICKABLE=8
ENABLED=9
FOCUSABLE=10
FOCUSED=11
SCROLLABLE=12
LONG_CLICKABLE=13
PASSWORD=14
SELECTED=15
BOUNDS=16
STARTX=17
ENDX=18
STARTY=19
ENDY=20
CENTER_X=21
CENTER_Y=22
AREA=23
WIDTH=24
HEIGHT=25
ARRAY_WIDTH=26
ARRAY_MAX_INDEX=$((ARRAY_WIDTH - 1))
COLUMNS=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25)
NAMESCOLUMNS=(INDEX TEXT RESOURCE_ID CLASS PACKAGE CONTENT_DESC CHECKABLE CHECKED CLICKABLE ENABLED FOCUSABLE FOCUSED SCROLLABLE LONG_CLICKABLE PASSWORD SELECTED BOUNDS STARTX ENDX STARTY ENDY CENTER_X CENTER_Y AREA WIDTH HEIGHT)
ALL_COLUMNS="INDEX,TEXT,RESOURCE_ID,CLASS,PACKAGE,CONTENT_DESC,CHECKABLE,CHECKED,CLICKABLE,ENABLED,FOCUSABLE,FOCUSED,SCROLLABLE,LONG_CLICKABLE,PASSWORD,SELECTED,BOUNDS,STARTX,ENDX,STARTY,ENDY,CENTER_X,CENTER_Y,AREA,WIDTH,HEIGHT"
array_elements=()
INDEX_ARRAY=()
print_csv=PRINT_CSV_REPLACE
defaultval="DEFAULTVALUE_REPLACE"

trim() {
    local var="$1"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}
parse_uiautomator() {
    grep -o -E '<([A-Za-z_:]|[^\x00-\x7F])([A-Za-z0-9_:.-]|[^\x00-\x7F])*([ \n\t\r]+([A-Za-z_:]|[^\x00-\x7F])([A-Za-z0-9_:.-]|[^\x00-\x7F])*([ \n\t\r]+)?=([ \n\t\r]+)?("[^<"]*"|'\''[^<'\'']*'\''))*([ \n\t\r]+)?/?>?' /sdcard/window_dump.xml | grep -o -E '([a-zA-Z0-9\-]+)=(("[^"]*")|('\''[^'\'']*'\''))' | awk '{ printf "\"AAAA%sQQQQ", $1, ""} END { print "\n" }' | sed 's/QQQQ"AAAA/\nQQQQAAAA/g' | sed 's/AAAAindex=/\nQQQQAAAANEWELEMENT="EE"\nQQQQAAAAindex=/g' >/sdcard/outputui.txt
    file_contents=$(<"/sdcard/outputui.txt")
    j=0
    i=0
    while IFS= read -r line0; do
        keyx=$(echo "$line0" | sed -n -E 's/QQQQAAAA([^=]+)=\"([^\"]*)\"?/\1/p')
        if [ "$keyx" = "boundsQQQQ" ]; then
            keyx="bounds"
        fi
        valx=$(echo "$line0" | sed -n -E 's/QQQQAAAA([^=]+)=\"([^\"]*)\"?/\2/p')
        valx=$(trim "$valx")
        if [ "$valx" = "" ]; then
            valx="$defaultval"
        fi
        if [ "$keyx" = "NEWELEMENT" ]; then
            iar=$((j * ARRAY_WIDTH))
            INDEX_ARRAY+=("$iar")
            j=$((j + 1))
            i=$((j - 1))
            array_elements[$((i * $((ARRAY_WIDTH)) + $((INDEX))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((TEXT))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((RESOURCE_ID))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CLASS))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((PACKAGE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CONTENT_DESC))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CHECKABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CHECKED))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENABLED))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((FOCUSED))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((SCROLLABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((PASSWORD))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((SELECTED))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((BOUNDS))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((STARTX))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENDX))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((STARTY))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENDY))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((AREA))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((WIDTH))))]="$defaultval"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$defaultval"
        fi
        if [ "$keyx" = "index" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((INDEX))))]="$valx"
        fi
        if [ "$keyx" = "text" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((TEXT))))]="$valx"
        fi
        if [ "$keyx" = "resource-id" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((RESOURCE_ID))))]="$valx"
        fi
        if [ "$keyx" = "class" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CLASS))))]="$valx"
        fi
        if [ "$keyx" = "package" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((PACKAGE))))]="$valx"
        fi
        if [ "$keyx" = "content-desc" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CONTENT_DESC))))]="$valx"
        fi
        if [ "$keyx" = "checkable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CHECKABLE))))]="$valx"
        fi
        if [ "$keyx" = "checked" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CHECKED))))]="$valx"
        fi
        if [ "$keyx" = "clickable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$valx"
        fi
        if [ "$keyx" = "enabled" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENABLED))))]="$valx"
        fi
        if [ "$keyx" = "focusable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$valx"
        fi
        if [ "$keyx" = "focused" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((FOCUSED))))]="$valx"
        fi
        if [ "$keyx" = "scrollable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((SCROLLABLE))))]="$valx"
        fi
        if [ "$keyx" = "long-clickable" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$valx"
        fi
        if [ "$keyx" = "password" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((PASSWORD))))]="$valx"
        fi
        if [ "$keyx" = "selected" ]; then
            array_elements[$((i * $((ARRAY_WIDTH)) + $((SELECTED))))]="$valx"
        fi
        if [ "$keyx" = "bounds" ]; then
            lxa2y=$(echo "$valx" | sed -n -E 's/[^0-9]*\[([0-9]+),([0-9]+)\]\[([0-9]+),([0-9]+)\][^0-9]*/\1 \2 \3 \4/p' || echo "0 0 0 0")
            array_elements[$((i * $((ARRAY_WIDTH)) + $((BOUNDS))))]="$lxa2y"
            IFS=" " read -r startxtmp startytmp endxtmp endytmp <<<"$lxa2y"
            widthx=$((endxtmp - startxtmp))
            heighty=$((endytmp - startytmp))
            area=$((widthx * heighty))
            centerx=$((widthx / 2 + startxtmp))
            centery=$((heighty / 2 + startytmp))
            array_elements[$((i * $((ARRAY_WIDTH)) + $((STARTX))))]="$startxtmp"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENDX))))]="$endxtmp"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((STARTY))))]="$startytmp"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((ENDY))))]="$endytmp"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$centerx"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$centery"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((AREA))))]="$area"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((WIDTH))))]="$widthx"
            array_elements[$((i * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$heighty"
        fi
    done <<<"$file_contents"
}
ADD_TO_SCRIPT_REPLACE
"""
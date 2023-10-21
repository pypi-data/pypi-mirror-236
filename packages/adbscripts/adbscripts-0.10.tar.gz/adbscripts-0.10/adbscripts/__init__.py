import base64
import functools
import importlib
import io
import os
import platform
import subprocess
import sys
from collections import deque
from time import sleep, time
import kthread

bashscript_chrome_download=r"""
0#!/bin/bash
fileout="/sdcard/dumpsys_output.txt"
filex="/sdcard/filenames_output.txt"
filenamesmatch="/sdcard/match_filenames.txt"
rm -f "$fileout"
rm -f "$filex"
rm -f "$filenamesmatch"
with_class=1
with_mid=1
with_hashcode=1
with_elementid=1
with_visibility=1
with_focusable=1
with_enabled=1
with_drawn=1
with_scrollbars_horizontal=1
with_scrollbars_vertical=1
with_clickable=1
with_long_clickable=1
with_context_clickable=1
with_pflag_is_root_namespace=1
with_pflag_focused=1
with_pflag_selected=1
with_pflag_prepressed=1
with_pflag_hovered=1
with_pflag_activated=1
with_pflag_invalidated=1
with_pflag_dirty_mask=1
stripline=1
defaultval="null"
print_csv=0
only_active=1
IS_ACTIVE=0
ELEMENT_INDEX=1
START_X=2
START_Y=3
CENTER_X=4
CENTER_Y=5
AREA=6
END_X=7
END_Y=8
WIDTH=9
HEIGHT=10
START_X_RELATIVE=11
START_Y_RELATIVE=12
END_X_RELATIVE=13
END_Y_RELATIVE=14
PARENTSINDEX=15
ELEMENT_ID=16
MID=17
HASHCODE=18
VISIBILITY=19
FOCUSABLE=20
ENABLED=21
DRAWN=22
SCROLLBARS_HORIZONTAL=23
SCROLLBARS_VERTICAL=24
CLICKABLE=25
LONG_CLICKABLE=26
CONTEXT_CLICKABLE=27
CLASSNAME=28
PFLAG_IS_ROOT_NAMESPACE=29
PFLAG_FOCUSED=30
PFLAG_SELECTED=31
PFLAG_PREPRESSED=32
PFLAG_HOVERED=33
PFLAG_ACTIVATED=34
PFLAG_INVALIDATED=35
PFLAG_DIRTY_MASK=36
LINE_STRIPPED=37
ARRAY_WIDTH=38
ARRAY_MAX_INDEX=$((ARRAY_WIDTH - 1))
INDEX_ARRAY=()
array_elements=()
COLUMNS=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37)
NAMESCOLUMNS=(IS_ACTIVE ELEMENT_INDEX START_X START_Y CENTER_X CENTER_Y AREA END_X END_Y WIDTH HEIGHT START_X_RELATIVE START_Y_RELATIVE END_X_RELATIVE END_Y_RELATIVE PARENTSINDEX ELEMENT_ID MID HASHCODE VISIBILITY FOCUSABLE ENABLED DRAWN SCROLLBARS_HORIZONTAL SCROLLBARS_VERTICAL CLICKABLE LONG_CLICKABLE CONTEXT_CLICKABLE CLASSNAME PFLAG_IS_ROOT_NAMESPACE PFLAG_FOCUSED PFLAG_SELECTED PFLAG_PREPRESSED PFLAG_HOVERED PFLAG_ACTIVATED PFLAG_INVALIDATED PFLAG_DIRTY_MASK LINE_STRIPPED)
ALL_COLUMNS="IS_ACTIVE,ELEMENT_INDEX,START_X,START_Y,CENTER_X,CENTER_Y,AREA,END_X,END_Y,WIDTH,HEIGHT,START_X_RELATIVE,START_Y_RELATIVE,END_X_RELATIVE,END_Y_RELATIVE,PARENTSINDEX,ELEMENT_ID,MID,HASHCODE,VISIBILITY,FOCUSABLE,ENABLED,DRAWN,SCROLLBARS_HORIZONTAL,SCROLLBARS_VERTICAL,CLICKABLE,LONG_CLICKABLE,CONTEXT_CLICKABLE,CLASSNAME,PFLAG_IS_ROOT_NAMESPACE,PFLAG_FOCUSED,PFLAG_SELECTED,PFLAG_PREPRESSED,PFLAG_HOVERED,PFLAG_ACTIVATED,PFLAG_INVALIDATED,PFLAG_DIRTY_MASK,LINE_STRIPPED"
process_matches() {
    rm -f "$fileout"
    rm -f "$filex"
    rm -f "$filenamesmatch"
    dumpsys activity top -c >"$fileout"
    awk '/View Hierarchy:/ {
        output = $0
        next
    }
    output {
        output = output "\n" $0
    }
    /Looper/ {
        if (output) {
            # Process and print each match separately
            # print "Match found:"
            print output
            # Save each match to a separate file
            match_file = "/sdcard/match_" NR ".txt"
            print output > match_file
            close(match_file)
            # Save the filename to a separate file
            print match_file > "/sdcard/match_filenames.txt"
            output = ""
        }
    }' "$fileout" >"$filex"
}
trim() {
    local var="$1"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    var="${var//\"/}"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo "$var"
}
process_result() {
    resultx="$1"
    groups=("$resultx")
    classname=''
    defaultvalue="$2"
    if [ -z "$resultx" ]; then
        classname="$defaultvalue"
    else
        for group in "${groups[@]}"; do
            classname="${classname} ${group}"
        done
    fi
    classnamestriped=$(trim "$classname")
    if [ "$classnamestriped" = "" ]; then
        classnamestriped="$defaultval"
    fi
    echo "$classnamestriped"
}
execute_all() {
    process_matches
    match_filenames_names=()
    filecounter=0
    while IFS= read -r filename; do
        match_filenames_names+=("$filename")
        filecounter=$((filecounter + 1))
        sed -i '1,2d' "$filename"
        sed -i '$d' "$filename"
    done <"$filenamesmatch"
    filecountermain=0
    isactivemainwindow=0
    element_index=0
    for file in "${match_filenames_names[@]}"; do
        filecountermain=$((filecountermain + 1))
        if [ "$only_active" -gt 0 ]; then
            if [ "$filecountermain" -lt "$filecounter" ]; then
                rm -f "$file"
                continue
            fi
        fi
        if [ "$filecountermain" -ge "$filecounter" ]; then
            isactivemainwindow=$((isactivemainwindow + 1))
        fi
        file_len=$(wc -l <"$file")
        file_contents=$(<"$file")
        rm -f "$file"
        output_array_coords=()
        output_array_lines=()
        output_array_index=()
        output_array_coords_start_x=()
        output_array_coords_start_y=()
        output_array_coords_end_x=()
        output_array_coords_end_y=()
        output_array_count=()
        output_array_index_rev=()
        output_array_coords_rev=()
        output_array_lines_rev=()
        output_array_coords_start_x_rev=()
        output_array_coords_start_y_rev=()
        output_array_coords_end_x_rev=()
        output_array_coords_end_y_rev=()
        output_array_count_rev=()
        i=0
        j="$file_len"
        while IFS= read -r line0; do
            j=$((j - 1))
            line0="${line0%?} "
            lxa=$(echo "$line0" | awk '{ for (i=1; i<=NF; i++) if ($i ~ /^[0-9,-]+$/) print $i }' || echo "0 0 0 0")
            lxa2=$(echo "$lxa" | sed -n -E 's/[^0-9]*([0-9]+)[^0-9]+([0-9]+)[^0-9]+([0-9]+)[^0-9]+([0-9]+)[^0-9]*/\1 \2 \3 \4/p' || echo "0 0 0 0")
            string0="$line0"
            count0="${#string0}"
            string0="${string0#"${string0%%[![:space:]]*}"}"
            count0=$((count0 - ${#string0}))
            output_array_coords+=("$lxa2")
            output_array_lines+=("$string0")
            output_array_index+=("$i")
            output_array_count+=("$count0")
            output_array_index_rev+=("$j")
            IFS=" " read -r startx_temp1 starty_temp1 endx1 endy1 <<<"$lxa2"
            output_array_coords_start_x+=("$startx_temp1")
            output_array_coords_start_y+=("$starty_temp1")
            output_array_coords_end_x+=("$endx1")
            output_array_coords_end_y+=("$endy1")
            i=$((i + 1))
        done <<<"$file_contents"
        for element in "${output_array_index_rev[@]}"; do
            output_array_coords_rev+=("${output_array_coords[element]}")
            output_array_lines_rev+=("${output_array_lines[element]}")
            output_array_coords_start_x_rev+=("${output_array_coords_start_x[element]}")
            output_array_coords_start_y_rev+=("${output_array_coords_start_y[element]}")
            output_array_coords_end_x_rev+=("${output_array_coords_end_x[element]}")
            output_array_coords_end_y_rev+=("${output_array_coords_end_y[element]}")
            output_array_count_rev+=("${output_array_count[element]}")
        done
        indexrevcounter=0
        reversecounterchecker=$((file_len - 1))
        resultmid="$defaultval"
        result_visibility="$defaultval"
        result_focusable="$defaultval"
        result_enabled="$defaultval"
        result_drawn="$defaultval"
        result_scrollbars_horizontal="$defaultval"
        result_scrollbars_vertical="$defaultval"
        result_clickable="$defaultval"
        result_long_clickable="$defaultval"
        result_context_clickable="$defaultval"
        resultclass="$defaultval"
        result_pflag_is_root_namespace="$defaultval"
        result_pflag_focused="$defaultval"
        result_pflag_selected="$defaultval"
        result_pflag_prepressed="$defaultval"
        result_pflag_hovered="$defaultval"
        result_pflag_activated="$defaultval"
        result_pflag_invalidated="$defaultval"
        result_pflag_dirty_mask="$defaultval"
        for element in "${output_array_index[@]}"; do
            line0="${output_array_lines[element]}"
            startx0="${output_array_coords_start_x[element]}"
            starty0="${output_array_coords_start_y[element]}"
            count0="${output_array_count[element]}"
            indexrevcounter=$((indexrevcounter - indexrevcounter))
            parents='|'
            for element1 in "${output_array_index[@]}"; do
                indexrev="${output_array_index_rev[element1]}"
                indexrevcounter=$((indexrevcounter + 1))
                if [ "$indexrev" -lt "$element" ]; then
                    startx1="${output_array_coords_start_x_rev[element1]}"
                    starty1="${output_array_coords_start_y_rev[element1]}"
                    endx1="${output_array_coords_end_x_rev[element1]}"
                    endy1="${output_array_coords_end_y_rev[element1]}"
                    count1="${output_array_count_rev[element1]}"
                    if [ "$count1" -lt "$count0" ]; then
                        parents="${parents}${indexrev}|"
                        count0=$((count1 + 0))
                        startx0=$((startx0 + startx1))
                        starty0=$((starty0 + starty1))
                    fi
                fi
                if [ "$indexrevcounter" -eq "$reversecounterchecker" ]; then
                    relativexstart="${output_array_coords_start_x[element]}"
                    relativeystart="${output_array_coords_start_y[element]}"
                    relativexend="${output_array_coords_end_x[element]}"
                    relativeyend="${output_array_coords_end_y[element]}"
                    relativexend=$((relativexend - relativexstart))
                    relativeyend=$((relativeyend - relativeystart))
                    absxend=$((startx0 + relativexend))
                    absyend=$((starty0 + relativeyend))
                    width=$((absxend - startx0))
                    height=$((absyend - starty0))
                    area=$((width * height))
                    centerx=$((width / 2 + startx0))
                    centery=$((height / 2 + starty0))
                    relativexend="${output_array_coords_end_x[element]}"
                    relativeyend="${output_array_coords_end_y[element]}"
                    if [ "$with_class" -gt 0 ]; then
                        classsearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*([^[:space:]]+)\{.*/\1/p')
                        resultclass=$(process_result "$classsearch" "$defaultval")
                    fi
                    if [ "$with_mid" -gt 0 ]; then
                        midsearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*[^[:space:]]+\{([a-fA-F0-9]+)[[:space:]]+.*/\1/p')
                        resultmid=$(process_result "$midsearch" "$defaultval")
                    fi
                    if [ "$with_hashcode" -gt 0 ]; then
                        hashcodesearch=$(echo "$line0" | sed -n -E 's/^[^#]+[[:space:]]+#([a-f0-9]+)[[:space:]]+.*/\1/p')
                        resulthashcode=$(process_result "$hashcodesearch" "$defaultval")
                    fi
                    if [ "$with_elementid" -gt 0 ]; then
                        elementidsearch=$(echo "$line0" | sed -n -E 's/^[^:]+[[:space:]]+([^[:space:]]+:[^[:space:]]+)\}?.*/\1/p')
                        resultelementid=$(process_result "$elementidsearch" "$defaultval")
                    fi
                    execute_first_flag=$((with_visibility + with_focusable + with_enabled + with_drawn + with_scrollbars_horizontal + with_scrollbars_vertical + with_clickable + with_long_clickable + with_context_clickable))
                    if [ "$execute_first_flag" -gt 0 ]; then
                        firstimesearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*[^[:space:]]+\{[a-fA-F0-9]+[[:space:]]+([A-Z.]{8,9})[[:space:]]+.*/\1/p')
                    fi
                    if [ "$with_visibility" -gt 0 ]; then
                        visibility_search=$"${firstimesearch:0:1}"
                        if [ "$visibility_search" = "." ]; then
                            visibility_search="$defaultval"
                        fi
                        result_visibility="$visibility_search"
                    fi
                    if [ "$with_focusable" -gt 0 ]; then
                        focusable_search=$"${firstimesearch:1:1}"
                        if [ "$focusable_search" = "." ]; then
                            focusable_search="$defaultval"
                        fi
                        result_focusable="$focusable_search"
                    fi
                    if [ "$with_enabled" -gt 0 ]; then
                        enabled_search=$"${firstimesearch:2:1}"
                        if [ "$enabled_search" = "." ]; then
                            enabled_search="$defaultval"
                        fi
                        result_enabled="$enabled_search"
                    fi
                    if [ "$with_drawn" -gt 0 ]; then
                        drawn_search=$"${firstimesearch:3:1}"
                        if [ "$drawn_search" = "." ]; then
                            drawn_search="$defaultval"
                        fi
                        result_drawn="$drawn_search"
                    fi
                    if [ "$with_scrollbars_horizontal" -gt 0 ]; then
                        scrollbars_horizontal_search=$"${firstimesearch:4:1}"
                        if [ "$scrollbars_horizontal_search" = "." ]; then
                            scrollbars_horizontal_search="$defaultval"
                        fi
                        result_scrollbars_horizontal="$scrollbars_horizontal_search"
                    fi
                    if [ "$with_scrollbars_vertical" -gt 0 ]; then
                        scrollbars_vertical_search=$"${firstimesearch:5:1}"
                        if [ "$scrollbars_vertical_search" = "." ]; then
                            scrollbars_vertical_search="$defaultval"
                        fi
                        result_scrollbars_vertical="$scrollbars_vertical_search"
                    fi
                    if [ "$with_clickable" -gt 0 ]; then
                        clickable_search=$"${firstimesearch:6:1}"
                        if [ "$clickable_search" = "." ]; then
                            clickable_search="$defaultval"
                        fi
                        result_clickable="$clickable_search"
                    fi
                    if [ "$with_long_clickable" -gt 0 ]; then
                        long_clickable_search=$"${firstimesearch:7:1}"
                        if [ "$long_clickable_search" = "." ]; then
                            long_clickable_search="$defaultval"
                        fi
                        result_long_clickable="$long_clickable_search"
                    fi
                    if [ "$with_context_clickable" -gt 0 ]; then
                        if [ ${#firstimesearch} -gt 8 ]; then
                            context_clickable_search=$"${firstimesearch:8:1}"
                            if [ "$context_clickable_search" = "." ]; then
                                context_clickable_search="$defaultval"
                                result_context_clickable="$context_clickable_search"
                            fi
                        fi
                    fi
                    execute_second_flag=$((with_pflag_is_root_namespace + with_pflag_focused + with_pflag_selected + with_pflag_prepressed + with_pflag_hovered + with_pflag_activated + with_pflag_invalidated + with_pflag_dirty_mask))
                    if [ "$execute_second_flag" -gt 0 ]; then
                        secondtimesearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*[^[:space:]]+\{[a-fA-F0-9]+[[:space:]]+[A-Z.]{8,9}[[:space:]]+([A-Z.]{8}).*/\1/p')
                    fi
                    if [ "$with_pflag_is_root_namespace" -gt 0 ]; then
                        pflag_is_root_namespace_search=$"${secondtimesearch:0:1}"
                        if [ "$pflag_is_root_namespace_search" = "." ]; then
                            pflag_is_root_namespace_search="$defaultval"
                        fi
                        result_pflag_is_root_namespace="$pflag_is_root_namespace_search"
                    fi
                    if [ "$with_pflag_focused" -gt 0 ]; then
                        pflag_focused_search=$"${secondtimesearch:1:1}"
                        if [ "$pflag_focused_search" = "." ]; then
                            pflag_focused_search="$defaultval"
                        fi
                        result_pflag_focused="$pflag_focused_search"
                    fi
                    if [ "$with_pflag_selected" -gt 0 ]; then
                        pflag_selected_search=$"${secondtimesearch:2:1}"
                        if [ "$pflag_selected_search" = "." ]; then
                            pflag_selected_search="$defaultval"
                        fi
                        result_pflag_selected="$pflag_selected_search"
                    fi
                    if [ "$with_pflag_prepressed" -gt 0 ]; then
                        pflag_prepressed_search=$"${secondtimesearch:3:1}"
                        if [ "$pflag_prepressed_search" = "." ]; then
                            pflag_prepressed_search="$defaultval"
                        fi
                        result_pflag_prepressed="$pflag_prepressed_search"
                    fi
                    if [ "$with_pflag_hovered" -gt 0 ]; then
                        pflag_hovered_search=$"${secondtimesearch:4:1}"
                        if [ "$pflag_hovered_search" = "." ]; then
                            pflag_hovered_search="$defaultval"
                        fi
                        result_pflag_hovered="$pflag_hovered_search"
                    fi
                    if [ "$with_pflag_activated" -gt 0 ]; then
                        pflag_activated_search=$"${secondtimesearch:5:1}"
                        if [ "$pflag_activated_search" = "." ]; then
                            pflag_activated_search="$defaultval"
                        fi
                        result_pflag_activated="$pflag_activated_search"
                    fi
                    if [ "$with_pflag_invalidated" -gt 0 ]; then
                        pflag_invalidated_search=$"${secondtimesearch:6:1}"
                        if [ "$pflag_invalidated_search" = "." ]; then
                            pflag_invalidated_search="$defaultval"
                        fi
                        result_pflag_invalidated="$pflag_invalidated_search"
                    fi
                    if [ "$with_pflag_dirty_mask" -gt 0 ]; then
                        pflag_dirty_mask_search=$"${secondtimesearch:7:1}"
                        if [ "$pflag_dirty_mask_search" = "." ]; then
                            pflag_dirty_mask_search="$defaultval"
                        fi
                        result_pflag_dirty_mask="$pflag_dirty_mask_search"
                    fi
                    if [ "$stripline" -gt 0 ]; then
                        #line0stripped=$(echo "$line0" | tr -d '[:space:]|')
                        line0stripped=$(trim "$line0")
                    else
                        line0stripped="$line0"
                    fi
                    INDEX_ARRAY+=($((element_index * ARRAY_WIDTH)))
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((IS_ACTIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_INDEX))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((AREA))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((WIDTH))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PARENTSINDEX))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_ID))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((MID))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HASHCODE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((VISIBILITY))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ENABLED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((DRAWN))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_HORIZONTAL))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_VERTICAL))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CONTEXT_CLICKABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLASSNAME))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_IS_ROOT_NAMESPACE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_FOCUSED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_SELECTED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_PREPRESSED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_HOVERED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_ACTIVATED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_INVALIDATED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_DIRTY_MASK))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LINE_STRIPPED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((IS_ACTIVE))))]=1
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_INDEX))))]="$element"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X))))]="$startx0"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y))))]="$starty0"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$centerx"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$centery"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((AREA))))]="$area"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X))))]="$absxend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y))))]="$absyend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((WIDTH))))]="$width"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$height"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X_RELATIVE))))]="$relativexstart"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y_RELATIVE))))]="$relativeystart"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X_RELATIVE))))]="$relativexend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y_RELATIVE))))]="$relativeyend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PARENTSINDEX))))]="$parents"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_ID))))]="$resultelementid"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((MID))))]="$resultmid"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HASHCODE))))]="$resulthashcode"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((VISIBILITY))))]="$result_visibility"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$result_focusable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ENABLED))))]="$result_enabled"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((DRAWN))))]="$result_drawn"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_HORIZONTAL))))]="$result_scrollbars_horizontal"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_VERTICAL))))]="$result_scrollbars_vertical"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$result_clickable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$result_long_clickable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CONTEXT_CLICKABLE))))]="$result_context_clickable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLASSNAME))))]="$resultclass"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_IS_ROOT_NAMESPACE))))]="$result_pflag_is_root_namespace"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_FOCUSED))))]="$result_pflag_focused"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_SELECTED))))]="$result_pflag_selected"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_PREPRESSED))))]="$result_pflag_prepressed"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_HOVERED))))]="$result_pflag_hovered"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_ACTIVATED))))]="$result_pflag_activated"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_INVALIDATED))))]="$result_pflag_invalidated"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_DIRTY_MASK))))]="$result_pflag_dirty_mask"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LINE_STRIPPED))))]="$line0stripped"
                    element_index=$((element_index + 1))
                fi
            done
        done
    done
}

splitlines() {
    local -n stringarrayx="$1"
    inputstring=$2
    while IFS= read -r line; do
        stringarrayx+=("$line")
    done <<<"$inputstring"
}

get_unique_and_common_strings() {
    local -n file1_array="$1"
    local -n file2_array="$2"
    local -n unique_to_file1="$3"
    local -n unique_to_file2="$4"
    local -n in_file1_and_file2="$5"
    for path1 in "${file1_array[@]}"; do
        found=false
        for path2 in "${file2_array[@]}"; do
            if [ "$path1" = "$path2" ]; then
                found=true
                in_file1_and_file2+=("$path1")
                break
            fi
        done
        if [ "$found" = false ]; then
            unique_to_file1+=("$path1")
        fi
    done
    for path1 in "${file2_array[@]}"; do
        found=false
        for path2 in "${file1_array[@]}"; do
            if [ "$path1" = "$path2" ]; then
                found=true
                break
            fi
        done
        if [ "$found" = false ]; then
            unique_to_file2+=("$path1")
        fi
    done
}
tap_on_item() {
    for row in "${INDEX_ARRAY[@]}"; do
        for column in "${COLUMNS[@]}"; do
            indexarray=$((row + column))
            active_column="${NAMESCOLUMNS[column]}"
            if [ "$active_column" = "$1" ]; then
                if [ "${array_elements[indexarray]}" = "$2" ]; then
                    centerx="${array_elements[$((row + CENTER_X))]}"
                    centery="${array_elements[$((row + CENTER_Y))]}"
                    input tap "$centerx" "$centery"
                fi
            fi
        done
    done
}

unique1=()
unique2=()
commo=()
oldstrings=()
newstrings=()
while true; do
    unset oldstrings
    unset newstrings
    unset unique1
    unset unique2
    unset commo
    unset INDEX_ARRAY
    unset array_elements
    execute_all
    lstmp1=$(ls -1 /sdcard/Download/*.*)
    splitlines oldstrings "$lstmp1"
    tap_on_item "ELEMENT_ID" "app:id/positive_button"
    tap_on_item "ELEMENT_ID" "app:id/save_offline_button"
    sleep 1
    lstmp2=$(ls -1 /sdcard/Download/*.*)
    splitlines newstrings "$lstmp2"
    get_unique_and_common_strings oldstrings newstrings unique1 unique2 commo
    for liney in "${unique2[@]}"; do
        cat "$liney"
        rm -f "$liney"
    done
done
"""


iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
    from ctypes import wintypes
    import ctypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    kernel32 = windll.kernel32

    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.LPWSTR,
        wintypes.DWORD,
    ]
    _GetShortPathNameW.restype = wintypes.DWORD

else:
    invisibledict = {}

try:
    pd = importlib.__import__("pandas")
except Exception:
    pass



def get_script_activities(
    print_csv=1,
    defaultvalue="null",
    sleeptime=1,
    addtoscript="",
    stripline=1,
    with_class=1,
    with_mid=1,
    with_hashcode=1,
    with_elementid=1,
    with_visibility=1,
    with_focusable=1,
    with_enabled=1,
    with_drawn=1,
    with_scrollbars_horizontal=1,
    with_scrollbars_vertical=1,
    with_clickable=1,
    with_long_clickable=1,
    with_context_clickable=1,
    with_pflag_is_root_namespace=1,
    with_pflag_focused=1,
    with_pflag_selected=1,
    with_pflag_prepressed=1,
    with_pflag_hovered=1,
    with_pflag_activated=1,
    with_pflag_invalidated=1,
    with_pflag_dirty_mask=1,
):
    if addtoscript:
        addtoscript = "\n".join(
            [x.replace("\t", "    ") for x in addtoscript.splitlines()]
        )
    else:
        """
        while true; do
            execute_all
            if [ "$print_csv" -gt 0 ]; then
                echo "$ALL_COLUMNS"
                for row in "${INDEX_ARRAY[@]}"; do
                    #echo "----------------------------"
                    for column in "${COLUMNS[@]}"; do
                        indexarray=$((row + column))
                        #echo -n "$row ${NAMESCOLUMNS[column]}"
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
    return (
        r"""
#!/bin/bash
fileout="/sdcard/dumpsys_output.txt"
filex="/sdcard/filenames_output.txt"
filenamesmatch="/sdcard/match_filenames.txt"
rm -f "$fileout"
rm -f "$filex"
rm -f "$filenamesmatch"
with_class=WITH_CLASS_REPLACE
with_mid=WITH_MID_REPLACE
with_hashcode=WITH_HASHCODE_REPLACE
with_elementid=WITH_ELEMENTID_REPLACE
with_visibility=WITH_VISIBILITY_REPLACE
with_focusable=WITH_FOCUSABLE_REPLACE
with_enabled=WITH_ENABLED_REPLACE
with_drawn=WITH_DRAWN_REPLACE
with_scrollbars_horizontal=WITH_SCROLLBARS_HORIZONTAL_REPLACE
with_scrollbars_vertical=WITH_SCROLLBARS_VERTICAL_REPLACE
with_clickable=WITH_CLICKABLE_REPLACE
with_long_clickable=WITH_LONG_CLICKABLE_REPLACE
with_context_clickable=WITH_CONTEXT_CLICKABLE_REPLACE
with_pflag_is_root_namespace=WITH_PFLAG_IS_ROOT_NAMESPACE_REPLACE
with_pflag_focused=WITH_PFLAG_FOCUSED_REPLACE
with_pflag_selected=WITH_PFLAG_SELECTED_REPLACE
with_pflag_prepressed=WITH_PFLAG_PREPRESSED_REPLACE
with_pflag_hovered=WITH_PFLAG_HOVERED_REPLACE
with_pflag_activated=WITH_PFLAG_ACTIVATED_REPLACE
with_pflag_invalidated=WITH_PFLAG_INVALIDATED_REPLACE
with_pflag_dirty_mask=WITH_PFLAG_DIRTY_MASK_REPLACE
stripline=STRIPLINE_REPLACE
defaultval="DEFAULTVALUE_REPLACE"
print_csv=PRINT_CSV_REPLACE

only_active=1

IS_ACTIVE=0
ELEMENT_INDEX=1
START_X=2
START_Y=3
CENTER_X=4
CENTER_Y=5
AREA=6
END_X=7
END_Y=8
WIDTH=9
HEIGHT=10
START_X_RELATIVE=11
START_Y_RELATIVE=12
END_X_RELATIVE=13
END_Y_RELATIVE=14
PARENTSINDEX=15
ELEMENT_ID=16
MID=17
HASHCODE=18
VISIBILITY=19
FOCUSABLE=20
ENABLED=21
DRAWN=22
SCROLLBARS_HORIZONTAL=23
SCROLLBARS_VERTICAL=24
CLICKABLE=25
LONG_CLICKABLE=26
CONTEXT_CLICKABLE=27
CLASSNAME=28
PFLAG_IS_ROOT_NAMESPACE=29
PFLAG_FOCUSED=30
PFLAG_SELECTED=31
PFLAG_PREPRESSED=32
PFLAG_HOVERED=33
PFLAG_ACTIVATED=34
PFLAG_INVALIDATED=35
PFLAG_DIRTY_MASK=36
LINE_STRIPPED=37
ARRAY_WIDTH=38
ARRAY_MAX_INDEX=$((ARRAY_WIDTH - 1))
INDEX_ARRAY=()
array_elements=()
COLUMNS=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37)
NAMESCOLUMNS=(IS_ACTIVE ELEMENT_INDEX START_X START_Y CENTER_X CENTER_Y AREA END_X END_Y WIDTH HEIGHT START_X_RELATIVE START_Y_RELATIVE END_X_RELATIVE END_Y_RELATIVE PARENTSINDEX ELEMENT_ID MID HASHCODE VISIBILITY FOCUSABLE ENABLED DRAWN SCROLLBARS_HORIZONTAL SCROLLBARS_VERTICAL CLICKABLE LONG_CLICKABLE CONTEXT_CLICKABLE CLASSNAME PFLAG_IS_ROOT_NAMESPACE PFLAG_FOCUSED PFLAG_SELECTED PFLAG_PREPRESSED PFLAG_HOVERED PFLAG_ACTIVATED PFLAG_INVALIDATED PFLAG_DIRTY_MASK LINE_STRIPPED)
ALL_COLUMNS="IS_ACTIVE,ELEMENT_INDEX,START_X,START_Y,CENTER_X,CENTER_Y,AREA,END_X,END_Y,WIDTH,HEIGHT,START_X_RELATIVE,START_Y_RELATIVE,END_X_RELATIVE,END_Y_RELATIVE,PARENTSINDEX,ELEMENT_ID,MID,HASHCODE,VISIBILITY,FOCUSABLE,ENABLED,DRAWN,SCROLLBARS_HORIZONTAL,SCROLLBARS_VERTICAL,CLICKABLE,LONG_CLICKABLE,CONTEXT_CLICKABLE,CLASSNAME,PFLAG_IS_ROOT_NAMESPACE,PFLAG_FOCUSED,PFLAG_SELECTED,PFLAG_PREPRESSED,PFLAG_HOVERED,PFLAG_ACTIVATED,PFLAG_INVALIDATED,PFLAG_DIRTY_MASK,LINE_STRIPPED"
process_matches() {
    rm -f "$fileout"
    rm -f "$filex"
    rm -f "$filenamesmatch"
    dumpsys activity top -c >"$fileout"
    awk '/View Hierarchy:/ {
        output = $0
        next
    }
    output {
        output = output "\n" $0
    }
    /Looper/ {
        if (output) {
            # Process and print each match separately
            # print "Match found:"
            print output

            # Save each match to a separate file
            match_file = "/sdcard/match_" NR ".txt"
            print output > match_file
            close(match_file)

            # Save the filename to a separate file
            print match_file > "/sdcard/match_filenames.txt"

            output = ""
        }
    }' "$fileout" >"$filex"
}

trim() {
    local var="$1"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    var="${var//\"/}"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo "$var"
}

process_result() {
    resultx="$1"
    groups=("$resultx")
    classname=''
    defaultvalue="$2"
    if [ -z "$resultx" ]; then
        classname="$defaultvalue"
    else
        for group in "${groups[@]}"; do
            classname="${classname} ${group}"
        done
    fi
    classnamestriped=$(trim "$classname")
    if [ "$classnamestriped" = "" ]; then
        classnamestriped="$defaultval"
    fi
    echo "$classnamestriped"
}
execute_all() {
    process_matches
    match_filenames_names=()
    filecounter=0
    while IFS= read -r filename; do
        match_filenames_names+=("$filename")
        filecounter=$((filecounter + 1))
        sed -i '1,2d' "$filename"
        sed -i '$d' "$filename"
    done <"$filenamesmatch"
    filecountermain=0
    isactivemainwindow=0
    element_index=0
    for file in "${match_filenames_names[@]}"; do
        filecountermain=$((filecountermain + 1))
        if [ "$only_active" -gt 0 ]; then
            if [ "$filecountermain" -lt "$filecounter" ]; then
                rm -f "$file"
                continue
            fi
        fi
        if [ "$filecountermain" -ge "$filecounter" ]; then
            isactivemainwindow=$((isactivemainwindow + 1))
        fi
        file_len=$(wc -l <"$file")
        file_contents=$(<"$file")
        rm -f "$file"
        output_array_coords=()
        output_array_lines=()
        output_array_index=()
        output_array_coords_start_x=()
        output_array_coords_start_y=()
        output_array_coords_end_x=()
        output_array_coords_end_y=()
        output_array_count=()
        output_array_index_rev=()
        output_array_coords_rev=()
        output_array_lines_rev=()
        output_array_coords_start_x_rev=()
        output_array_coords_start_y_rev=()
        output_array_coords_end_x_rev=()
        output_array_coords_end_y_rev=()
        output_array_count_rev=()
        i=0
        j="$file_len"
        while IFS= read -r line0; do
            j=$((j - 1))
            line0="${line0%?} "
            lxa=$(echo "$line0" | awk '{ for (i=1; i<=NF; i++) if ($i ~ /^[0-9,-]+$/) print $i }' || echo "0 0 0 0")
            lxa2=$(echo "$lxa" | sed -n -E 's/[^0-9]*([0-9]+)[^0-9]+([0-9]+)[^0-9]+([0-9]+)[^0-9]+([0-9]+)[^0-9]*/\1 \2 \3 \4/p' || echo "0 0 0 0")
            string0="$line0"
            count0="${#string0}"
            string0="${string0#"${string0%%[![:space:]]*}"}"
            count0=$((count0 - ${#string0}))
            output_array_coords+=("$lxa2")
            output_array_lines+=("$string0")
            output_array_index+=("$i")
            output_array_count+=("$count0")
            output_array_index_rev+=("$j")
            IFS=" " read -r startx_temp1 starty_temp1 endx1 endy1 <<<"$lxa2"
            output_array_coords_start_x+=("$startx_temp1")
            output_array_coords_start_y+=("$starty_temp1")
            output_array_coords_end_x+=("$endx1")
            output_array_coords_end_y+=("$endy1")
            i=$((i + 1))
        done <<<"$file_contents"
        for element in "${output_array_index_rev[@]}"; do
            output_array_coords_rev+=("${output_array_coords[element]}")
            output_array_lines_rev+=("${output_array_lines[element]}")
            output_array_coords_start_x_rev+=("${output_array_coords_start_x[element]}")
            output_array_coords_start_y_rev+=("${output_array_coords_start_y[element]}")
            output_array_coords_end_x_rev+=("${output_array_coords_end_x[element]}")
            output_array_coords_end_y_rev+=("${output_array_coords_end_y[element]}")
            output_array_count_rev+=("${output_array_count[element]}")
        done
        indexrevcounter=0
        reversecounterchecker=$((file_len - 1))
        resultmid="$defaultval"
        result_visibility="$defaultval"
        result_focusable="$defaultval"
        result_enabled="$defaultval"
        result_drawn="$defaultval"
        result_scrollbars_horizontal="$defaultval"
        result_scrollbars_vertical="$defaultval"
        result_clickable="$defaultval"
        result_long_clickable="$defaultval"
        result_context_clickable="$defaultval"
        resultclass="$defaultval"
        result_pflag_is_root_namespace="$defaultval"
        result_pflag_focused="$defaultval"
        result_pflag_selected="$defaultval"
        result_pflag_prepressed="$defaultval"
        result_pflag_hovered="$defaultval"
        result_pflag_activated="$defaultval"
        result_pflag_invalidated="$defaultval"
        result_pflag_dirty_mask="$defaultval"
        for element in "${output_array_index[@]}"; do
            line0="${output_array_lines[element]}"
            startx0="${output_array_coords_start_x[element]}"
            starty0="${output_array_coords_start_y[element]}"
            count0="${output_array_count[element]}"
            indexrevcounter=$((indexrevcounter - indexrevcounter))
            parents='|'
            for element1 in "${output_array_index[@]}"; do
                indexrev="${output_array_index_rev[element1]}"
                indexrevcounter=$((indexrevcounter + 1))
                if [ "$indexrev" -lt "$element" ]; then
                    startx1="${output_array_coords_start_x_rev[element1]}"
                    starty1="${output_array_coords_start_y_rev[element1]}"
                    endx1="${output_array_coords_end_x_rev[element1]}"
                    endy1="${output_array_coords_end_y_rev[element1]}"
                    count1="${output_array_count_rev[element1]}"
                    if [ "$count1" -lt "$count0" ]; then
                        parents="${parents}${indexrev}|"
                        count0=$((count1 + 0))
                        startx0=$((startx0 + startx1))
                        starty0=$((starty0 + starty1))
                    fi
                fi
                if [ "$indexrevcounter" -eq "$reversecounterchecker" ]; then
                    relativexstart="${output_array_coords_start_x[element]}"
                    relativeystart="${output_array_coords_start_y[element]}"
                    relativexend="${output_array_coords_end_x[element]}"
                    relativeyend="${output_array_coords_end_y[element]}"
                    relativexend=$((relativexend - relativexstart))
                    relativeyend=$((relativeyend - relativeystart))
                    absxend=$((startx0 + relativexend))
                    absyend=$((starty0 + relativeyend))
                    width=$((absxend - startx0))
                    height=$((absyend - starty0))
                    area=$((width * height))
                    centerx=$((width / 2 + startx0))
                    centery=$((height / 2 + starty0))
                    relativexend="${output_array_coords_end_x[element]}"
                    relativeyend="${output_array_coords_end_y[element]}"
                    if [ "$with_class" -gt 0 ]; then
                        classsearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*([^[:space:]]+)\{.*/\1/p')
                        resultclass=$(process_result "$classsearch" "$defaultval")
                    fi
                    if [ "$with_mid" -gt 0 ]; then
                        midsearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*[^[:space:]]+\{([a-fA-F0-9]+)[[:space:]]+.*/\1/p')
                        resultmid=$(process_result "$midsearch" "$defaultval")
                    fi
                    if [ "$with_hashcode" -gt 0 ]; then
                        hashcodesearch=$(echo "$line0" | sed -n -E 's/^[^#]+[[:space:]]+#([a-f0-9]+)[[:space:]]+.*/\1/p')
                        resulthashcode=$(process_result "$hashcodesearch" "$defaultval")
                    fi
                    if [ "$with_elementid" -gt 0 ]; then
                        elementidsearch=$(echo "$line0" | sed -n -E 's/^[^:]+[[:space:]]+([^[:space:]]+:[^[:space:]]+)\}?.*/\1/p')
                        resultelementid=$(process_result "$elementidsearch" "$defaultval")
                    fi
                    execute_first_flag=$((with_visibility + with_focusable + with_enabled + with_drawn + with_scrollbars_horizontal + with_scrollbars_vertical + with_clickable + with_long_clickable + with_context_clickable))
                    if [ "$execute_first_flag" -gt 0 ]; then
                        firstimesearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*[^[:space:]]+\{[a-fA-F0-9]+[[:space:]]+([A-Z.]{8,9})[[:space:]]+.*/\1/p')
                    fi
                    if [ "$with_visibility" -gt 0 ]; then
                        visibility_search=$"${firstimesearch:0:1}"
                        if [ "$visibility_search" = "." ]; then
                            visibility_search="$defaultval"
                        fi

                        result_visibility="$visibility_search"
                    fi
                    if [ "$with_focusable" -gt 0 ]; then
                        focusable_search=$"${firstimesearch:1:1}"
                        if [ "$focusable_search" = "." ]; then
                            focusable_search="$defaultval"
                        fi

                        result_focusable="$focusable_search"
                    fi
                    if [ "$with_enabled" -gt 0 ]; then
                        enabled_search=$"${firstimesearch:2:1}"
                        if [ "$enabled_search" = "." ]; then
                            enabled_search="$defaultval"
                        fi

                        result_enabled="$enabled_search"
                    fi
                    if [ "$with_drawn" -gt 0 ]; then
                        drawn_search=$"${firstimesearch:3:1}"
                        if [ "$drawn_search" = "." ]; then
                            drawn_search="$defaultval"
                        fi

                        result_drawn="$drawn_search"
                    fi
                    if [ "$with_scrollbars_horizontal" -gt 0 ]; then
                        scrollbars_horizontal_search=$"${firstimesearch:4:1}"
                        if [ "$scrollbars_horizontal_search" = "." ]; then
                            scrollbars_horizontal_search="$defaultval"
                        fi

                        result_scrollbars_horizontal="$scrollbars_horizontal_search"
                    fi
                    if [ "$with_scrollbars_vertical" -gt 0 ]; then
                        scrollbars_vertical_search=$"${firstimesearch:5:1}"
                        if [ "$scrollbars_vertical_search" = "." ]; then
                            scrollbars_vertical_search="$defaultval"
                        fi

                        result_scrollbars_vertical="$scrollbars_vertical_search"
                    fi
                    if [ "$with_clickable" -gt 0 ]; then
                        clickable_search=$"${firstimesearch:6:1}"
                        if [ "$clickable_search" = "." ]; then
                            clickable_search="$defaultval"
                        fi

                        result_clickable="$clickable_search"
                    fi
                    if [ "$with_long_clickable" -gt 0 ]; then
                        long_clickable_search=$"${firstimesearch:7:1}"
                        if [ "$long_clickable_search" = "." ]; then
                            long_clickable_search="$defaultval"
                        fi

                        result_long_clickable="$long_clickable_search"
                    fi
                    if [ "$with_context_clickable" -gt 0 ]; then
                        if [ ${#firstimesearch} -gt 8 ]; then
                            context_clickable_search=$"${firstimesearch:8:1}"
                            if [ "$context_clickable_search" = "." ]; then
                                context_clickable_search="$defaultval"
                                result_context_clickable="$context_clickable_search"

                            fi
                        fi
                    fi
                    execute_second_flag=$((with_pflag_is_root_namespace + with_pflag_focused + with_pflag_selected + with_pflag_prepressed + with_pflag_hovered + with_pflag_activated + with_pflag_invalidated + with_pflag_dirty_mask))
                    if [ "$execute_second_flag" -gt 0 ]; then
                        secondtimesearch=$(echo "$line0" | sed -n -E 's/^[[:space:]]*[^[:space:]]+\{[a-fA-F0-9]+[[:space:]]+[A-Z.]{8,9}[[:space:]]+([A-Z.]{8}).*/\1/p')
                    fi
                    if [ "$with_pflag_is_root_namespace" -gt 0 ]; then
                        pflag_is_root_namespace_search=$"${secondtimesearch:0:1}"
                        if [ "$pflag_is_root_namespace_search" = "." ]; then
                            pflag_is_root_namespace_search="$defaultval"
                        fi

                        result_pflag_is_root_namespace="$pflag_is_root_namespace_search"
                    fi
                    if [ "$with_pflag_focused" -gt 0 ]; then
                        pflag_focused_search=$"${secondtimesearch:1:1}"
                        if [ "$pflag_focused_search" = "." ]; then
                            pflag_focused_search="$defaultval"
                        fi

                        result_pflag_focused="$pflag_focused_search"
                    fi
                    if [ "$with_pflag_selected" -gt 0 ]; then
                        pflag_selected_search=$"${secondtimesearch:2:1}"
                        if [ "$pflag_selected_search" = "." ]; then
                            pflag_selected_search="$defaultval"
                        fi

                        result_pflag_selected="$pflag_selected_search"
                    fi
                    if [ "$with_pflag_prepressed" -gt 0 ]; then
                        pflag_prepressed_search=$"${secondtimesearch:3:1}"
                        if [ "$pflag_prepressed_search" = "." ]; then
                            pflag_prepressed_search="$defaultval"
                        fi

                        result_pflag_prepressed="$pflag_prepressed_search"
                    fi
                    if [ "$with_pflag_hovered" -gt 0 ]; then
                        pflag_hovered_search=$"${secondtimesearch:4:1}"
                        if [ "$pflag_hovered_search" = "." ]; then
                            pflag_hovered_search="$defaultval"
                        fi

                        result_pflag_hovered="$pflag_hovered_search"
                    fi
                    if [ "$with_pflag_activated" -gt 0 ]; then
                        pflag_activated_search=$"${secondtimesearch:5:1}"
                        if [ "$pflag_activated_search" = "." ]; then
                            pflag_activated_search="$defaultval"
                        fi

                        result_pflag_activated="$pflag_activated_search"
                    fi
                    if [ "$with_pflag_invalidated" -gt 0 ]; then
                        pflag_invalidated_search=$"${secondtimesearch:6:1}"
                        if [ "$pflag_invalidated_search" = "." ]; then
                            pflag_invalidated_search="$defaultval"
                        fi

                        result_pflag_invalidated="$pflag_invalidated_search"
                    fi
                    if [ "$with_pflag_dirty_mask" -gt 0 ]; then
                        pflag_dirty_mask_search=$"${secondtimesearch:7:1}"
                        if [ "$pflag_dirty_mask_search" = "." ]; then
                            pflag_dirty_mask_search="$defaultval"
                        fi

                        result_pflag_dirty_mask="$pflag_dirty_mask_search"
                    fi
                    if [ "$stripline" -gt 0 ]; then
                        #line0stripped=$(echo "$line0" | tr -d '[:space:]|')
                        line0stripped=$(trim "$line0")
                    else
                        line0stripped="$line0"
                    fi
                    INDEX_ARRAY+=($((element_index * ARRAY_WIDTH)))
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((IS_ACTIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_INDEX))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((AREA))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((WIDTH))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y_RELATIVE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PARENTSINDEX))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_ID))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((MID))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HASHCODE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((VISIBILITY))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ENABLED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((DRAWN))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_HORIZONTAL))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_VERTICAL))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CONTEXT_CLICKABLE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLASSNAME))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_IS_ROOT_NAMESPACE))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_FOCUSED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_SELECTED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_PREPRESSED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_HOVERED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_ACTIVATED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_INVALIDATED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_DIRTY_MASK))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LINE_STRIPPED))))]="$defaultval"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((IS_ACTIVE))))]=1
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_INDEX))))]="$element"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X))))]="$startx0"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y))))]="$starty0"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_X))))]="$centerx"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CENTER_Y))))]="$centery"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((AREA))))]="$area"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X))))]="$absxend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y))))]="$absyend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((WIDTH))))]="$width"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HEIGHT))))]="$height"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_X_RELATIVE))))]="$relativexstart"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((START_Y_RELATIVE))))]="$relativeystart"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_X_RELATIVE))))]="$relativexend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((END_Y_RELATIVE))))]="$relativeyend"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PARENTSINDEX))))]="$parents"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ELEMENT_ID))))]="$resultelementid"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((MID))))]="$resultmid"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((HASHCODE))))]="$resulthashcode"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((VISIBILITY))))]="$result_visibility"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((FOCUSABLE))))]="$result_focusable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((ENABLED))))]="$result_enabled"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((DRAWN))))]="$result_drawn"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_HORIZONTAL))))]="$result_scrollbars_horizontal"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((SCROLLBARS_VERTICAL))))]="$result_scrollbars_vertical"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLICKABLE))))]="$result_clickable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LONG_CLICKABLE))))]="$result_long_clickable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CONTEXT_CLICKABLE))))]="$result_context_clickable"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((CLASSNAME))))]="$resultclass"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_IS_ROOT_NAMESPACE))))]="$result_pflag_is_root_namespace"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_FOCUSED))))]="$result_pflag_focused"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_SELECTED))))]="$result_pflag_selected"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_PREPRESSED))))]="$result_pflag_prepressed"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_HOVERED))))]="$result_pflag_hovered"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_ACTIVATED))))]="$result_pflag_activated"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_INVALIDATED))))]="$result_pflag_invalidated"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((PFLAG_DIRTY_MASK))))]="$result_pflag_dirty_mask"
                    array_elements[$((element_index * $((ARRAY_WIDTH)) + $((LINE_STRIPPED))))]="$line0stripped"
                    element_index=$((element_index + 1))
                fi
            done
        done
    done
}
ADD_TO_SCRIPT_REPLACE

""".replace(
            "ADD_TO_SCRIPT_REPLACE", str(addtoscript)
        )
        .replace("WITH_CLASS_REPLACE", str(with_class))
        .replace("WITH_MID_REPLACE", str(with_mid))
        .replace("WITH_HASHCODE_REPLACE", str(with_hashcode))
        .replace("WITH_ELEMENTID_REPLACE", str(with_elementid))
        .replace("WITH_VISIBILITY_REPLACE", str(with_visibility))
        .replace("WITH_FOCUSABLE_REPLACE", str(with_focusable))
        .replace("WITH_ENABLED_REPLACE", str(with_enabled))
        .replace("WITH_DRAWN_REPLACE", str(with_drawn))
        .replace("WITH_SCROLLBARS_HORIZONTAL_REPLACE", str(with_scrollbars_horizontal))
        .replace("WITH_SCROLLBARS_VERTICAL_REPLACE", str(with_scrollbars_vertical))
        .replace("WITH_CLICKABLE_REPLACE", str(with_clickable))
        .replace("WITH_LONG_CLICKABLE_REPLACE", str(with_long_clickable))
        .replace("WITH_CONTEXT_CLICKABLE_REPLACE", str(with_context_clickable))
        .replace(
            "WITH_PFLAG_IS_ROOT_NAMESPACE_REPLACE", str(with_pflag_is_root_namespace)
        )
        .replace("WITH_PFLAG_FOCUSED_REPLACE", str(with_pflag_focused))
        .replace("WITH_PFLAG_SELECTED_REPLACE", str(with_pflag_selected))
        .replace("WITH_PFLAG_PREPRESSED_REPLACE", str(with_pflag_prepressed))
        .replace("WITH_PFLAG_HOVERED_REPLACE", str(with_pflag_hovered))
        .replace("WITH_PFLAG_ACTIVATED_REPLACE", str(with_pflag_activated))
        .replace("WITH_PFLAG_INVALIDATED_REPLACE", str(with_pflag_invalidated))
        .replace("WITH_PFLAG_DIRTY_MASK_REPLACE", str(with_pflag_dirty_mask))
        .replace("STRIPLINE_REPLACE", str(stripline))
        .replace("PRINT_CSV_REPLACE", str(int(print_csv)))
        .replace("DEFAULTVALUE_REPLACE", str(defaultvalue))
        .replace("SLEEPTIME_REPLACE", str(sleeptime))
    )


def get_script_uiautomator(
    print_csv=1,
    defaultvalue="null",
    sleeptime=1,
    addtoscript="",
):
    if addtoscript:
        addtoscript = "\n".join(
            [x.replace("\t", "    ") for x in addtoscript.splitlines()]
        )
    else:
        addtoscript = r"""
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
    return (
        r"""
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
""".replace("ADD_TO_SCRIPT_REPLACE", str(addtoscript)).replace("PRINT_CSV_REPLACE", str(int(print_csv)))
        .replace("DEFAULTVALUE_REPLACE", str(defaultvalue))
        .replace("SLEEPTIME_REPLACE", str(sleeptime))

    )


@functools.cache
def get_short_path_name(long_name):
    if not iswindows:
        return long_name
    try:
        if not os.path.exists(long_name):
            return long_name

        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        pa = output_buf.value
        return pa if os.path.exists(pa) else long_name
    except Exception:
        return long_name


def _format_command(
    adbpath,
    serial_number,
    cmd,
    su=False,
    use_busybox=False,
    errors="strict",
    use_short_adb_path=True,
    add_exit=True,
):
    wholecommand = [get_short_path_name(adbpath) if use_short_adb_path else adbpath]
    nolimitcommand = []
    print(cmd)

    base64_command = base64.standard_b64encode(cmd.encode("utf-8", errors)).decode(
        "utf-8", errors
    )
    base64_command = "'" + base64_command + "'"
    if serial_number:
        wholecommand.extend(["-s", serial_number])
    wholecommand.extend(["shell"])
    if su:
        wholecommand.extend(["su", "--"])

    nolimitcommand.extend(["echo", base64_command, "|"])
    if use_busybox:
        nolimitcommand.extend(["busybox"])
    nolimitcommand.extend(["base64", "-d", "|", "sh"])

    exit_u = "\nexit\n"
    exit_b = b"\nexit\n"
    if not add_exit:
        exit_u = ""
        exit_b = b""

    nolimitcommand_no_bytes = " ".join(nolimitcommand) + exit_u
    nolimitcommand_bytes = " ".join(nolimitcommand).encode("utf-8", errors) + exit_b
    return nolimitcommand_no_bytes, nolimitcommand_bytes, wholecommand


def killproc(pid):
    return subprocess.Popen(f"taskkill /F /PID {pid} /T", **invisibledict)


def kill_subproc(p, t=()):
    try:
        p.stdin.close()
    except Exception:
        pass
    try:
        p.stdout.close()
    except Exception:
        pass
    try:
        p.stderr.close()
    except Exception:
        pass
    try:
        _ = killproc(p.pid)
    except Exception:
        pass
    if t:
        for tt in t:
            try:
                tt.kill()
            except Exception:
                pass


class AdbCapture:
    def __init__(self, adb_path, device_serial, capture_buffer=100, use_busybox=False):
        self.adbpath = get_short_path_name(adb_path)
        self.adb_path = adb_path
        self.device_serial = device_serial
        self.use_busybox = use_busybox
        self.captured_stdout = deque([], capture_buffer)
        self.captured_stderr = deque([], capture_buffer)
        self.columncheck = [
            "INDEX,TEXT,RESOURCE_ID,CLASS,PACKAGE,CONTENT_DESC,CHECKABLE,CHECKED,CLICKABLE,ENABLED,FOCUSABLE,FOCUSED,SCROLLABLE,LONG_CLICKABLE,PASSWORD,SELECTED,BOUNDS,STARTX,ENDX,STARTY,ENDY,CENTER_X,CENTER_Y,AREA,WIDTH,HEIGHT",
            "IS_ACTIVE,ELEMENT_INDEX,START_X,START_Y,CENTER_X,CENTER_Y,AREA,END_X,END_Y,WIDTH,HEIGHT,START_X_RELATIVE,START_Y_RELATIVE,END_X_RELATIVE,END_Y_RELATIVE,PARENTSINDEX,ELEMENT_ID,MID,HASHCODE,VISIBILITY,FOCUSABLE,ENABLED,DRAWN,SCROLLBARS_HORIZONTAL,SCROLLBARS_VERTICAL,CLICKABLE,LONG_CLICKABLE,CONTEXT_CLICKABLE,CLASSNAME,PFLAG_IS_ROOT_NAMESPACE,PFLAG_FOCUSED,PFLAG_SELECTED,PFLAG_PREPRESSED,PFLAG_HOVERED,PFLAG_ACTIVATED,PFLAG_INVALIDATED,PFLAG_DIRTY_MASK,LINE_STRIPPED",
        ]
        self.stop_capturing = False
        self.subproc = None
        self.stdout_thread_list = None
        self.stderr_thread_list = None

    def kill_csv_capture(self):
        self.stop_capturing = True
        sleep(2)
        try:
            subprocess.Popen(f"taskkill /F /PID {self.subproc.pid} /T", **invisibledict)
        except Exception:
            pass
        kill_subproc(self.subproc, (self.stdout_thread_list, self.stderr_thread_list))
        return self

    def get_one_csv_uiautomator(self, defaultvalue="null", convert_to_pandas=True):
        return self._get_one_csv(
            use_uiautomator=True,
            defaultvalue=defaultvalue,
            convert_to_pandas=convert_to_pandas,
        )

    def get_one_csv_activities(
        self,
        defaultvalue="null",
        convert_to_pandas=True,
        stripline=0,
        with_class=0,
        with_mid=0,
        with_hashcode=0,
        with_elementid=0,
        with_visibility=0,
        with_focusable=0,
        with_enabled=0,
        with_drawn=0,
        with_scrollbars_horizontal=0,
        with_scrollbars_vertical=0,
        with_clickable=0,
        with_long_clickable=0,
        with_context_clickable=0,
        with_pflag_is_root_namespace=0,
        with_pflag_focused=0,
        with_pflag_selected=0,
        with_pflag_prepressed=0,
        with_pflag_hovered=0,
        with_pflag_activated=0,
        with_pflag_invalidated=0,
        with_pflag_dirty_mask=0,
    ):
        return self._get_one_csv(
            use_uiautomator=False,
            defaultvalue=defaultvalue,
            convert_to_pandas=convert_to_pandas,
            stripline=int(stripline),
            with_class=int(with_class),
            with_mid=int(with_mid),
            with_hashcode=int(with_hashcode),
            with_elementid=int(with_elementid),
            with_visibility=int(with_visibility),
            with_focusable=int(with_focusable),
            with_enabled=int(with_enabled),
            with_drawn=int(with_drawn),
            with_scrollbars_horizontal=int(with_scrollbars_horizontal),
            with_scrollbars_vertical=int(with_scrollbars_vertical),
            with_clickable=int(with_clickable),
            with_long_clickable=int(with_long_clickable),
            with_context_clickable=int(with_context_clickable),
            with_pflag_is_root_namespace=int(with_pflag_is_root_namespace),
            with_pflag_focused=int(with_pflag_focused),
            with_pflag_selected=int(with_pflag_selected),
            with_pflag_prepressed=int(with_pflag_prepressed),
            with_pflag_hovered=int(with_pflag_hovered),
            with_pflag_activated=int(with_pflag_activated),
            with_pflag_invalidated=int(with_pflag_invalidated),
            with_pflag_dirty_mask=int(with_pflag_dirty_mask),
        )

    def _get_one_csv(
        self,
        use_uiautomator,
        defaultvalue="null",
        convert_to_pandas=True,
        stripline=0,
        with_class=0,
        with_mid=0,
        with_hashcode=0,
        with_elementid=0,
        with_visibility=0,
        with_focusable=0,
        with_enabled=0,
        with_drawn=0,
        with_scrollbars_horizontal=0,
        with_scrollbars_vertical=0,
        with_clickable=0,
        with_long_clickable=0,
        with_context_clickable=0,
        with_pflag_is_root_namespace=0,
        with_pflag_focused=0,
        with_pflag_selected=0,
        with_pflag_prepressed=0,
        with_pflag_hovered=0,
        with_pflag_activated=0,
        with_pflag_invalidated=0,
        with_pflag_dirty_mask=0,
    ):
        addtoscript_activities = r"""
while true; do
    execute_all
    if [ "$print_csv" -gt 0 ]; then
        echo "$ALL_COLUMNS"
        for row in "${INDEX_ARRAY[@]}"; do
            #echo "----------------------------"
            for column in "${COLUMNS[@]}"; do
                indexarray=$((row + column))
                #echo -n "$row ${NAMESCOLUMNS[column]}"
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
    exit
done        
        """
        add_to_scripts_uiautomator=r"""
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
    exit
done        
"""

        if use_uiautomator:
            scri = get_script_uiautomator(
                print_csv=1,
                defaultvalue=defaultvalue,
                sleeptime=0.00001,
                addtoscript=add_to_scripts_uiautomator,
            )
        else:
            scri = get_script_activities(
                print_csv=1,
                defaultvalue=defaultvalue,
                sleeptime=0.0000001,
                addtoscript=addtoscript_activities,
                stripline=int(stripline),
                with_class=int(with_class),
                with_mid=int(with_mid),
                with_hashcode=int(with_hashcode),
                with_elementid=int(with_elementid),
                with_visibility=int(with_visibility),
                with_focusable=int(with_focusable),
                with_enabled=int(with_enabled),
                with_drawn=int(with_drawn),
                with_scrollbars_horizontal=int(with_scrollbars_horizontal),
                with_scrollbars_vertical=int(with_scrollbars_vertical),
                with_clickable=int(with_clickable),
                with_long_clickable=int(with_long_clickable),
                with_context_clickable=int(with_context_clickable),
                with_pflag_is_root_namespace=int(with_pflag_is_root_namespace),
                with_pflag_focused=int(with_pflag_focused),
                with_pflag_selected=int(with_pflag_selected),
                with_pflag_prepressed=int(with_pflag_prepressed),
                with_pflag_hovered=int(with_pflag_hovered),
                with_pflag_activated=int(with_pflag_activated),
                with_pflag_invalidated=int(with_pflag_invalidated),
                with_pflag_dirty_mask=int(with_pflag_dirty_mask),
            )

        nolimitcommand_no_bytes, nolimitcommand_bytes, wholecommand = _format_command(
            adbpath=self.adbpath,
            serial_number=self.device_serial,
            cmd=scri,
            su=False,
            use_busybox=self.use_busybox,
            errors="strict",
            use_short_adb_path=True,
            add_exit=True,
        )
        print(nolimitcommand_no_bytes)
        self.subproc = subprocess.run(
            wholecommand, input=nolimitcommand_bytes, capture_output=True
        )
        if convert_to_pandas:
            try:
                return pd.read_csv(
                    io.StringIO(self.subproc.stdout.decode("utf-8", "backslashreplace"))
                ), self.subproc.stderr.decode("utf-8", "backslashreplace")
            except Exception as fe:
                print(fe)
                return self.subproc.stdout.decode(
                    "utf-8", "backslashreplace"
                ), self.subproc.stderr.decode("utf-8", "backslashreplace")

    def _start_capturing_csv(
        self,
        print_csv=1,
        defaultvalue="null",
        sleeptime=1,
        addtoscript="",
        clear_temp_lines=True,
        print_stdout=True,
        print_stderr=True,
        add_exit=False,
        use_uiautomator=True,
            reset_buffer=True,
        stripline=0,
        with_class=0,
        with_mid=0,
        with_hashcode=0,
        with_elementid=0,
        with_visibility=0,
        with_focusable=0,
        with_enabled=0,
        with_drawn=0,
        with_scrollbars_horizontal=0,
        with_scrollbars_vertical=0,
        with_clickable=0,
        with_long_clickable=0,
        with_context_clickable=0,
        with_pflag_is_root_namespace=0,
        with_pflag_focused=0,
        with_pflag_selected=0,
        with_pflag_prepressed=0,
        with_pflag_hovered=0,
        with_pflag_activated=0,
        with_pflag_invalidated=0,
        with_pflag_dirty_mask=0,
        **kwargs,
    ):
        self.stop_capturing = False
        if use_uiautomator:
            scri = get_script_uiautomator(
                print_csv=print_csv,
                defaultvalue=defaultvalue,
                sleeptime=sleeptime,
                addtoscript=addtoscript,
            )
        else:
            scri = get_script_activities(
                print_csv=print_csv,
                defaultvalue=defaultvalue,
                sleeptime=sleeptime,
                addtoscript=addtoscript,
                stripline=int(stripline),
                with_class=int(with_class),
                with_mid=int(with_mid),
                with_hashcode=int(with_hashcode),
                with_elementid=int(with_elementid),
                with_visibility=int(with_visibility),
                with_focusable=int(with_focusable),
                with_enabled=int(with_enabled),
                with_drawn=int(with_drawn),
                with_scrollbars_horizontal=int(with_scrollbars_horizontal),
                with_scrollbars_vertical=int(with_scrollbars_vertical),
                with_clickable=int(with_clickable),
                with_long_clickable=int(with_long_clickable),
                with_context_clickable=int(with_context_clickable),
                with_pflag_is_root_namespace=int(with_pflag_is_root_namespace),
                with_pflag_focused=int(with_pflag_focused),
                with_pflag_selected=int(with_pflag_selected),
                with_pflag_prepressed=int(with_pflag_prepressed),
                with_pflag_hovered=int(with_pflag_hovered),
                with_pflag_activated=int(with_pflag_activated),
                with_pflag_invalidated=int(with_pflag_invalidated),
                with_pflag_dirty_mask=int(with_pflag_dirty_mask),
            )

        self.execute_shell_script(
            script=scri,
            su=False,
            add_exit=add_exit,
            print_stderr=print_stderr,
            reset_buffer=reset_buffer,
            print_stdout=print_stdout,
            clear_temp_lines_for_csv=True,
        )

        return self

    def execute_shell_script(
        self,
            script,
        su=False,
        add_exit=True,
        print_stderr=True,
        reset_buffer=True,
        print_stdout=True,
        clear_temp_lines_for_csv=False,
    ):
        self.stop_capturing = False
        stdoutlist = []
        if reset_buffer:
            self.captured_stderr.clear()
            self.captured_stdout.clear()

        def read_stderr_thread():
            while not self.stop_capturing:
                try:
                    for q in iter(self.subproc.stderr.readline, b""):
                        if self.stop_capturing:
                            break
                        deco = q.decode("utf-8", "backslashreplace").strip()
                        self.captured_stderr.append(deco)
                        if print_stderr:
                            sys.stderr.write(f"{deco}\n")
                except Exception:
                    sleep(.1)
                    pass

        def read_stdout_thread():
            while not self.stop_capturing:
                try:
                    for q in iter(self.subproc.stdout.readline, b""):
                        if self.stop_capturing:
                            break
                        deco = q.decode("utf-8", "backslashreplace").strip()
                        if not deco:
                            continue
                        if "," in deco and deco not in self.columncheck:
                            if not deco.startswith("ERROR"):
                                stdoutlist.append(deco)
                                if print_stdout:
                                    print(f"{deco}")

                        else:
                            joining = "\n".join(stdoutlist)
                            if joining:
                                self.captured_stdout.append(joining)
                                if clear_temp_lines_for_csv:
                                    stdoutlist.clear()
                            stdoutlist.append(deco)
                except Exception as fe:
                    print(fe)
                    sleep(.1)

        if "#!/bin/bash" not in script:
            script = "#!/bin/bash\n" + script
        nolimitcommand_no_bytes, nolimitcommand_bytes, wholecommand = _format_command(
            adbpath=self.adbpath,
            serial_number=self.device_serial,
            cmd=script,
            su=su,
            use_busybox=self.use_busybox,
            errors="strict",
            use_short_adb_path=True,
            add_exit=add_exit,
        )

        self.subproc = subprocess.Popen(
            wholecommand,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **invisibledict,
        )

        self.subproc.stdin.write(nolimitcommand_bytes)
        self.subproc.stdin.close()
        self.stdout_thread_list = kthread.KThread(
            target=read_stdout_thread, name=f"read_stdout_thread{time()}"
        )
        self.stderr_thread_list = kthread.KThread(
            target=read_stderr_thread, name=f"read_stderr_thread{time()}"
        )
        self.stdout_thread_list.start()
        self.stderr_thread_list.start()

    def start_capturing_csv_uiautomator(
        self,
        print_csv=1,
        defaultvalue="null",
        sleeptime=1,
        addtoscript="",
        print_stdout=True,
        print_stderr=True,
        add_exit=False,
        clear_temp_lines=True,
        **kwargs,
    ):
        return self._start_capturing_csv(
            print_csv=print_csv,
            defaultvalue=defaultvalue,
            sleeptime=sleeptime,
            addtoscript=addtoscript,
            print_stdout=print_stdout,
            print_stderr=print_stderr,
            add_exit=add_exit,
            use_uiautomator=True,
            clear_temp_lines=clear_temp_lines,
            **kwargs,
        )

    def start_capturing_csv_activities(
        self,
        print_csv=1,
        defaultvalue="null",
        sleeptime=1,
        addtoscript="",
        print_stdout=True,
        print_stderr=True,
        add_exit=False,
        clear_temp_lines=True,
        stripline=0,
        with_class=0,
        with_mid=0,
        with_hashcode=0,
        with_elementid=0,
        with_visibility=0,
        with_focusable=0,
        with_enabled=0,
        with_drawn=0,
        with_scrollbars_horizontal=0,
        with_scrollbars_vertical=0,
        with_clickable=0,
        with_long_clickable=0,
        with_context_clickable=0,
        with_pflag_is_root_namespace=0,
        with_pflag_focused=0,
        with_pflag_selected=0,
        with_pflag_prepressed=0,
        with_pflag_hovered=0,
        with_pflag_activated=0,
        with_pflag_invalidated=0,
        with_pflag_dirty_mask=0,
        **kwargs,
    ):
        return self._start_capturing_csv(
            print_csv=print_csv,
            defaultvalue=defaultvalue,
            sleeptime=sleeptime,
            addtoscript=addtoscript,
            print_stdout=print_stdout,
            print_stderr=print_stderr,
            add_exit=add_exit,
            use_uiautomator=False,
            stripline=int(stripline),
            with_class=int(with_class),
            with_mid=int(with_mid),
            with_hashcode=int(with_hashcode),
            with_elementid=int(with_elementid),
            with_visibility=int(with_visibility),
            with_focusable=int(with_focusable),
            with_enabled=int(with_enabled),
            with_drawn=int(with_drawn),
            with_scrollbars_horizontal=int(with_scrollbars_horizontal),
            with_scrollbars_vertical=int(with_scrollbars_vertical),
            with_clickable=int(with_clickable),
            with_long_clickable=int(with_long_clickable),
            with_context_clickable=int(with_context_clickable),
            with_pflag_is_root_namespace=int(with_pflag_is_root_namespace),
            with_pflag_focused=int(with_pflag_focused),
            with_pflag_selected=int(with_pflag_selected),
            with_pflag_prepressed=int(with_pflag_prepressed),
            with_pflag_hovered=int(with_pflag_hovered),
            with_pflag_activated=int(with_pflag_activated),
            with_pflag_invalidated=int(with_pflag_invalidated),
            with_pflag_dirty_mask=int(with_pflag_dirty_mask),
            clear_temp_lines=clear_temp_lines,
            **kwargs,
        )

    def connect_to_device(
        self,
        **kwargs,
    ):
        p = subprocess.run(
            f"{self.adbpath} connect {self.device_serial}",
            capture_output=True,
            **kwargs,
            **invisibledict,
        )
        stdout = p.stdout.splitlines()
        stderr = p.stderr.splitlines()
        return stdout, stderr

    def open_adb_shell(self):
        subprocess.run(
            f'start cmd /k "{self.adbpath}" -s {self.device_serial} shell', shell=True
        )


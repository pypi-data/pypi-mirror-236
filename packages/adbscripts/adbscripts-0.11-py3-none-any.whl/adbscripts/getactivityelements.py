activityelementsbasic=r"""
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

activityelements=r"""
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

"""
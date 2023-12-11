#!/bin/bash

log_file="$HOME/Downloads/log.txt"
output_log="$HOME/Downloads/output_log.txt"
search_line_start=63
#search_line_end=69 - nu sunt suficiente linii pt a scrie tot cuvantul
search_line_end=72
replacement_word="AUTOMATION"

if [ ! -f "$log_file" ]; then
  echo "Error: log.txt not found in the Downloads folder."
        exit 1
fi


echo "LOG OF WORD REPLACEMENTS" > "$output_log"
echo "------------------------" >> "$output_log"

letters=($(echo "$replacement_word" | sed 's/./& /g'))

sed -n "${search_line_start},${search_line_end}p" "$log_file" | \
awk '{if (NF >= 6) {print $6}}' | \
while read -r original_word; do
        sed -i "$search_line_start s/${original_word}/${letters[0]}/" "$log_file"
        echo "'${original_word}' was replaced with the letter '${letters[0]}'." >> "$output_log"
        letters=("${letters[@]:1}")
        ((search_line_start++))
        if [ ${search_line_start} -gt ${search_line_end} ]; then
                break
        fi
done

echo "Replacement was complete! Check '$output_log' for details!"
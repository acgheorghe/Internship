#!/bin/bash

if [ "$#" -lt 2 ]; then
        echo "Usage: $0 <search_string> <filename1> [<filename2 ...]"
        exit 1
fi

search_string="$1"
shift

for file in "$@"; do
        if [ -f "$file" ]; then
                echo "Occurrences of '$search_string' in '$file':"
                grep -n "$search_string" "$file" | while IFS=: read -r line_number content; do
                        echo "Line '$line_number': '$content'"
                done
        else
                echo "Error: File '$file' not found."
        fi
done

#!/bin/bash

if [ "$#" -ne 2 ]; then
        echo "Usage: $0 <search_string> <filename>"
        exit 1
fi

search_string="$1"
filename="$2"

if [ ! -f "$filename" ]; then
        echo "Error: File '$filename' not found."
        exit 1
fi

count=$(grep -o "$search_string" "$filename" | wc -l)

echo "The string '$search_string' occurs '$count' times in the file $filename "

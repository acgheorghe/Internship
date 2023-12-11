#!/bin/bash

input_file="$HOME/Downloads/bashcrc.txt"
output_file="$HOME/Downloads/bashcrc"

if [ ! -e "$input_file" ] || [ ! -e "$output_file" ]; then
        echo "Error: One or both of the bascrc files do not exist in the specified folder"
        exit 1
fi


declare -A key_value_pairs

while IFS='=' read -r key value ; do
        key_value_pairs["$key"]=$value

done < <(grep '=' "$input_file")



for key in "${!key_value_pairs[@]}"; do
        sed -i "/^[[:space:]]*#/!s/$key=.*$/$key=${key_value_pairs[$key]//\//\\/}/" "$output_file"
        echo "Updated $key in $output_file"
done

echo "Done"

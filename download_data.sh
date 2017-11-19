#!/bin/bash

files=(
  wipo_field
  wipo
  patent
  uspatentcitation

  # assignee
  # patent_assignee
  # cpc_current
  # cpc_group
  # cpc_subgroup
  # cpc_subsection
)

function download {
  file=$1".zip"
  echo downloading $file

  wget -N "http://www.patentsview.org/data/20170808/"$file

  echo uziping $file
  unzip -o $file
  rm $file
}

mkdir -p data
cd data

for f in "${files[@]}"
do
  download $f
done


exit

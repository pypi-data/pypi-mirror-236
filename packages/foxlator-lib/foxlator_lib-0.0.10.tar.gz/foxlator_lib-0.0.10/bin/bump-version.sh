#!/bin/bash

config_file="./pyproject.toml"
version=$(grep 'version.*=' ${config_file} | cut -d = -f2 | tr -d '"')
echo "$ - current version:" $version

get_part() {
    echo $(echo $version | cut -d . -f$1)
}

apply_version() {
    echo "$ - new version is:" $1
    version=$1
    sed -i -e "s/\(version = \"\)[^\"]*\"/\1$1\"/" $config_file
}

if [ "$1" = '--patch' ]; then
    echo "$ - bumping patch"
    n=$(get_part 3)
    apply_version "$(get_part 1).$(get_part 2).$(($n + 1))"
elif [ "$1" = '--minor' ]; then
    echo "$ - bumping minor version"
    n=$(echo $version | cut -d . -f2)
    apply_version "$(get_part 1).$(($n + 1)).0"
elif [ "$1" = '--major' ]; then
    echo "$ - bumping major version"
    n=$(echo $version | cut -d . -f1)
    apply_version "$(($n + 1)).0.0"
else
    echo "$ - invalid argument!"
    exit -1
fi

git add $config_file
git commit -m "Build notification - "$version
git push

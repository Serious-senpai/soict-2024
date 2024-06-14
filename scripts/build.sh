g++ --version

#! https://stackoverflow.com/a/246128
SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
ROOT_DIR=$(realpath $SCRIPT_DIR/..)

echo "Got root of directory: $ROOT_DIR"

params="-O3 -Wall -I src/include -std=c++20"
if [ "$1" == "debug" ]
then
    params="$params -g -D DEBUG"
    echo "Building in debug mode"
else
    params="$params -O3"
fi

mkdir -p build result
g++ $params $ROOT_DIR/src/main.cpp -o $ROOT_DIR/build/main.exe

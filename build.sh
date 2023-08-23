#!/usr/bin/env bash

SINGULARITY=${SINGULARITY:-"$(which singularity)"}
IMAGE_BASE_NAME="PEpiTA"

# must be build.def for this image to be buildable on Rivanna
IMG=$IMAGE_BASE_NAME.sif

if [ -w $IMG ]; then
	echo "Overwrite $IMG? y/n"
	read ANSWER
	case $ANSWER in
		[yY]) rm $IMG;;
	        [nN]) echo 'Cancelling'; exit 1;;
	esac
fi

echo "Building $IMG"
echo sudo "${SINGULARITY}" build output_image.sif build.def
sudo "${SINGULARITY}" build output_image.sif build.def && mv output_image.sif $IMG
echo "Build Complete.  Image in `realpath $IMG`"

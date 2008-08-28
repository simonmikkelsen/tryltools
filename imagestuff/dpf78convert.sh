#!/bin/sh

if [ $# = 0 -o "$1" = "-h" -o "$1" = "--help" ]
then
	echo "Usage: $0 files"
	cat <<EODESC
       Converts pictures to be used for a Lumatron digital picture frame
       model DPF-78.

       ORIGINALS ARE OVER WRITTEN WITHOUT WARNING.
       Use only this script on copies!
       
       Requirements: convert command from imagemagick

       Official resolution (from the manual): 1440x234
       More probable resolution: 440x234
       Aspect ratio: 16:9

       Challenges:

       Resizing: The picture frame will add black bars so an image will have
       the 4:3 aspect ratio. Then it will rescale it to be in the 16:9 ratio.
       That problem is solved by this script by outputting a 4:3 picture that
       will have the proper aspect ratio when scaled to 16:9.

       Aspect ratio: Most pictures are not in 16:9 and its a pain to crop
       them all by hand. This is solved by the script in this way:
       Depending on a prefix in the image name, the script will take different
       parts of the image and use that, e.g. the top, the middle, bottom etc.
       Use the following:
       t - top
       s - sky, between top and middle.
       m - middle	
       w - water, between middle and bottom.
       b - bottom
       images without prefix are ignored. 
       The originals are assumed to be in 4:3 aspect ratio. If not the
       prefixes will produce slightly different results than expected.

       TODO:
          The picture frame does not show files resized with this script
          in full screen. Open the pictures in The Gimp, save them and
          close, and then they show perfectly. Don't ask why but find
          a solution.

          The script was made for a max with resolution of 1440 which it
          has appeared to be too high. Recalculate everyting to fit into
          440.

          Only overwrite copies if a switch is given - else make new file.
       
          Don't just ignore pictures without prefix.

       License: GPLv3
       Author: Simon Mikkelsen, http://mikkelsen.tv/simon/
EODESC
	exit 0
fi

ls $* | while read f
do
	case "$f" in
		t*)
			y=0 ;;
		m*)
			# 720 - 540
			y=180 ;;
		b*)
			# 1440 - 1080
			y=360 ;;
		s*)
			y=90 ;;
		w*)
			y=270 ;;
		*)
			y=None ;;
	esac

	if [ $y != None ]
	then
		# Convert
		# ! means ignore aspect ratio: Force this exact resolution.
		# -quality is the compression. This don't have to be more.
		convert -quality 65 -resize '1440x1440!' -crop "1440x1080+0+$y" "$f" "$f" 
	fi
done


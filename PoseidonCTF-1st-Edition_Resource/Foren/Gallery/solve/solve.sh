while read line; do
	steghide extract -sf Wallpaper_HD_19756487Ef4.jpg -p $line 2>/dev/null
done < 123-Garbage.txt

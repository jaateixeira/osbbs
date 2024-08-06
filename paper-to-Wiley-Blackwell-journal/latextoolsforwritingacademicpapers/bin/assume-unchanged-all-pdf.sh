echo "updating git index to assume all pdf-files in this folder as unchanged"
git update-index --verbose --assume-unchange *.pdf
echo "DONE"

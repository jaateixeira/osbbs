echo "updating git index to assume all pdf-files in this folder as unchanged"
git update-index --verbose --assume-unchange *.docx
git update-index --verbose --assume-unchange *.doc
echo "DONE"

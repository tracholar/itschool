python download.py -f php.txt
python download.py -f html.txt
python download.py -f cshap.txt
python download.py -f bash.txt
python download.py -f android.txt

mv *.md ../article
cd ../article
git add .
git commit -m 'update file'
git push origin master


echo "Running The Game..."
for ((i=1; i<=100; i++))
do
    python Game.py -ge 100 -gp 10 -gr 10 -u 0.0,10.0 -p 0
done
echo "Running The Game..."
for ((i=1; i<=100; i++))
do
    python Game.py -ge 100 -gp 10 -gr 0 -u 0.0,1.0 -p 50
done
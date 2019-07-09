"""
Calculating lottery odds - and looking at the woman who won 
multiple times on potentially badly designed game

for k choices out of n balls, we have *combination* formula of

   n!
-------
k!(n-k)!



"""
import functools
import sys
import locale
locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')


@functools.lru_cache()
def factorial(n):
    """ """
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def chances(n=55, k=6):
    factn = factorial(n)
    factk = factorial(k)
    factn_k = factorial(n-k)
    chance = factn/(factk*factn_k)
    chancef = locale.format_string("%d", chance, grouping=True)
    msg = "Picking {} balls from {} is a 1/{} chance"
    print(msg.format(k,n,chancef))

if __name__ == '__main__':
    try:
        n = sys.argv[1:][0]
        k = sys.argv[1:][1]
    except:
        print("lottery.py n k")
        sys.exit()
    chances(int(n),int(k))
    

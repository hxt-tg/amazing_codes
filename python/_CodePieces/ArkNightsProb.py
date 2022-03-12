import matplotlib.pyplot as plt
import numpy as np

MAX_TIMES = 300
P = np.hstack((np.ones(50)*0.02, np.arange(0.02, 1.00+1e-7, 0.02), [1.0]*300))

def plot_total_p(times, p_arr, label):
    xa = np.array(list(range(1, times + 1)))
    total_p = np.array([1-np.prod((1-p_arr)[:x]) for x in xa])
    plt.plot(xa, total_p, label=f'{label}')    
    
plot_total_p(300, P * 0.7, 'Any')
plot_total_p(300, P * 0.7 * 0.5, 'Specific')
plt.legend()
plt.show()

## --- 

from random import random
from numpy.random import choice
from tqdm import tqdm

class Pool:
    NOT_SIX = 0
    SIX_UP_1 = 1
    SIX_UP_2 = 2
    SIX_OTHER = 3
    
    def __init__(self, finite=False, double_up=True):
        self.finite = finite
        self.double_up = double_up
        self.cu_times = 0  # Cumulative
        self.p6 = 0.02
        self.p6_dist = {
            # finite, double_up
            (True, True): (0.7*0.5, 0.7*0.5, 0.3),
            (True, False): (0.7, 0, 0.3),
            (False, True): (0.5*0.5, 0.5*0.5, 0.5),
            (False, False): (0.5, 0, 0.5),
        }[(self.finite, self.double_up)]
        
    @property
    def pa(self):
        """Probability array"""
        return [1-self.p6] + [self.p6 * p for p in self.p6_dist]
    
    def reset(self):
        self.cu_times = 0
        self.p6 = 0.02
    
    def draw(self):
        result = choice(4, p=self.pa)
        self.cu_times += 1
        if result != Pool.NOT_SIX:
            self.reset()
        if self.cu_times >= 50:
            self.p6 = min(self.p6 + 0.02, 1.0)
        return result
    
    def count(self, cond=lambda x: x != Pool.NOT_SIX):
        self.reset()
        cnt = 0
        while True:
            r = self.draw()
            cnt += 1
            if cond(r): break
        return cnt
    
    def count_any_6(self):
        return self.count()
    
    def count_any_up(self):
        return self.count(cond=lambda x: x == Pool.SIX_UP_1 or x == Pool.SIX_UP_2)
    
    def count_specific(self):
        return self.count(cond=lambda x: x == Pool.SIX_UP_1)
    
    def count_double_up(self):
        if not self.double_up: return 0
        self.reset()
        cnt = 0
        up_6 = 0
        
        while True:
            r = self.draw()
            cnt += 1
            if r == Pool.SIX_UP_1 or r == Pool.SIX_UP_2:
                up_6 |= r
                if up_6 == 3:
                    break
        return cnt


# 轮换池单UP(50%)
pool = Pool(double_up=False)
print(pool.pa)
roll = np.sort(np.array([pool.count_any_up() for _ in tqdm(range(2000))]))
p = np.array(range(roll.shape[0]))/float(roll.shape[0])
plt.plot(roll, p, label='single_up')
plt.xlim([0, 300])
plt.legend()
plt.title('Normal single UP')
plt.show()


# 限定池双UP(70%)
pool = Pool(finite=True)
print(pool.pa)
roll = np.sort(np.array([pool.count_any_up() for _ in tqdm(range(2000))]))
p = np.array(range(roll.shape[0]))/float(roll.shape[0])
plt.plot(roll, p, label='any_up')
roll = np.sort(np.array([pool.count_specific() for _ in tqdm(range(2000))]))
p = np.array(range(roll.shape[0]))/float(roll.shape[0])
plt.plot(roll, p, label='specific')
roll = np.sort(np.array([pool.count_double_up() for _ in tqdm(range(2000))]))
p = np.array(range(roll.shape[0]))/float(roll.shape[0])
plt.plot(roll, p, label='double_up')
plt.xlim([0, 300])
plt.legend()
plt.title('Finite double up')
plt.show()


# 轮换池双UP(50%)
pool = Pool()
print(pool.pa)
roll = np.sort(np.array([pool.count_any_up() for _ in tqdm(range(2000))]))
p = np.array(range(roll.shape[0]))/float(roll.shape[0])
plt.plot(roll, p, label='any_up')
roll = np.sort(np.array([pool.count_specific() for _ in tqdm(range(2000))]))
p = np.array(range(roll.shape[0]))/float(roll.shape[0])
plt.plot(roll, p, label='specific')
roll = np.sort(np.array([pool.count_double_up() for _ in tqdm(range(2000))]))
p = np.array(range(roll.shape[0]))/float(roll.shape[0])
plt.plot(roll, p, label='double_up')
plt.xlim([0, 300])
plt.legend()
plt.title('Normal double up')
plt.show()

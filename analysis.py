import matplotlib.pyplot as plt

algos = [
    'AES',
    'Blowfish',
    'tripleDES',
    'RSA',
]

sizes = [
    'very-short',
    'short',
    'medium',
    'long',
    'very-long'
]

data = {}

for algo in algos:
    data[algo] = {}
    for size in sizes:
        with open('./data/{}_{}.txt'.format(algo, size)) as f:
            data[algo][size] = [float(line.rstrip()) for line in f]


def plot_aes_long():
    with open('./data/AES_long.txt') as f:
        data = [float(line.rstrip()) for line in f]
        
    x = [i for i in range(0, 1000)]
    # plt.plot(data)
    plt.scatter(x=x, y=data)
    plt.ylabel('execution time')
    plt.xlabel('Attempt #')
    # plt.show()

    import numpy as np
    from scipy.signal import savgol_filter
    from scipy.optimize import curve_fit
    yhat = savgol_filter(data, 51, 3)

    # plt.plot(x,y)
    plt.plot(x, yhat, color='red')

    # 1024 characters (long)
    plt.legend(['AES (Savitzky-Golay)', 'AES'])
    plt.show()


def plot_aes_long_fit():
    with open('./data/AES_long.txt') as f:
        data = [float(line.rstrip()) for line in f]
        
    x = [i for i in range(0, 1000)]
    plt.scatter(x=x, y=data)
    plt.ylabel('execution time')
    plt.xlabel('Attempt #')

    from scipy.optimize import curve_fit

    # plt.plot(x,y)
    # plt.plot(x, yhat, color='red')

    import numpy as np

    # fitted a polynomial of degree 10                                          # funny note, actually looks like Savitzky-Golay,
    z = np.polyfit(x, data, 20)
    f = np.poly1d(z)
    x_new = np.linspace(x[0], x[-1], 1000)
    y_new = f(x_new)
    plt.plot(x,data,'o', x_new, y_new)
    plt.xlim([x[0]-1, x[-1] + 1 ])

    # 1024 characters (long)
    plt.legend(['AES', 'curve fit'])
    
    from sklearn.metrics import r2_score
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
    # a pretty bad r^2 score. Coefficient of determination
    print(r2_score(data, y_new))

    less_than_10_ms = []
    less_than_10_ms_count = 0
    for i in data:
        if i < 10:
            less_than_10_ms.append(i)
            less_than_10_ms_count += 1
    # 71% of data is faster than 10 ms, but the random deviations make it noisy
    print(less_than_10_ms_count)

    plt.show()


def plot_aes_long_fit_10():
    with open('./data/AES_long.txt') as f:
        data = [float(line.rstrip()) for line in f]
    
    less_than_10_ms = []
    less_than_10_ms_count = 0
    for i in data:
        # 5 ms or faster
        if i < 5:
            less_than_10_ms.append(i)
            less_than_10_ms_count += 1
    data = less_than_10_ms
    print("Faster than 5 ms:", less_than_10_ms_count)

    x = [i for i in range(0, len(data))]
    plt.scatter(x=x, y=data)
    plt.ylabel('execution time')
    plt.xlabel('Attempt #')
    import numpy as np
    z = np.polyfit(x, data, 20)
    f = np.poly1d(z)
    x_new = np.linspace(x[0], x[-1], len(data))
    y_new = f(x_new)
    plt.plot(x,data,'o', x_new, y_new)
    plt.xlim([x[0]-1, x[-1] + 1 ])

    plt.legend(['AES', 'curve fit'])
    
    from sklearn.metrics import r2_score
    print(r2_score(data, y_new))
    plt.show()



def plot_symmetric():
    aes = [sum(data['AES'][i])/1000 for i in data['AES']]
    blowfish = [sum(data['Blowfish'][i])/1000 for i in data['Blowfish']]
    tripleDES = [sum(data['tripleDES'][i])/1000 for i in data['tripleDES']]
    rsa = [sum(data['RSA'][i])/5 for i in data['RSA']]

    x = [1,2,3,4,5]
    x_names = [16,64, 256, 1024, 4096]
    # print(aes)
    plt.plot(x, aes, linestyle='--')
    plt.plot(x, blowfish, linestyle=':')
    plt.plot(x, tripleDES)
    plt.xticks(x, x_names)
    plt.ylabel('Average execution time (ms)')
    plt.xlabel('Initial message length (characters)')
    plt.legend(['AES', 'Blowfish', 'tripleDES'])
    plt.show()



def plot_all():
    aes = [sum(data['AES'][i])/1000 for i in data['AES']]
    blowfish = [sum(data['Blowfish'][i])/1000 for i in data['Blowfish']]
    tripleDES = [sum(data['tripleDES'][i])/1000 for i in data['tripleDES']]
    rsa = [sum(data['RSA'][i])/5 for i in data['RSA']]

    x = [1,2,3,4,5]
    x_names = [16,64, 256, 1024, 4096]
    # print(aes)
    plt.scatter(x, aes)
    # plt.plot(x, aes, linestyle='--')
    # plt.scatter(x, blowfish)
    # plt.plot(x, blowfish, linestyle=':')
    # plt.scatter(x, tripleDES)
    # plt.plot(x, tripleDES)
    plt.scatter(x, rsa)
    # plt.plot(x, rsa, linestyle='-.')
    plt.xticks(x, x_names)
    plt.ylabel('Average execution time (ms)')
    plt.xlabel('Initial message length (characters)')
    # plt.legend(['AES', 'Blowfish', 'tripleDES', 'RSA'])
    plt.legend(['AES', 'RSA'])
    plt.show()



def calculate_table(algo):
    import statistics
    aes = [sum(data['AES'][i])/1000 for i in data['AES']]
    blowfish = [sum(data['Blowfish'][i])/1000 for i in data['Blowfish']]
    tripleDES = [sum(data['tripleDES'][i])/1000 for i in data['tripleDES']]
    rsa = [sum(data['RSA'][i])/5 for i in data['RSA']]

    results = []

    for size in sizes:
        average = round(statistics.mean(data[algo][size]), 3)
        median = round(statistics.median(data[algo][size]), 3)
        stdev = round(statistics.stdev(data[algo][size]), 3)
        results.append([average, median, stdev])

    print(''.ljust(12), 'mean ', 'med  ', 'stdev')
    for index, size in enumerate(sizes):
        print(size.ljust(12),
            str(results[index][0]).ljust(5),
            str(results[index][1]).ljust(5),
            str(results[index][2]).ljust(5)
        )
    return results


# plot_aes_long()
plot_aes_long_fit()
# plot_aes_long_fit_10()
# plot_all()
# calculate_table('RSA')
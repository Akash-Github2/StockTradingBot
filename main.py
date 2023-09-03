import stock_scaper as ss

def main():
    # ss.storePrices()
    priceMap = ss.loadPrices()
    print(len(priceMap))

if __name__ == '__main__':
    main()

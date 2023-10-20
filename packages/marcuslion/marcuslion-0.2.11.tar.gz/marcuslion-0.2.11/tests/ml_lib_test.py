from src.marcuslion import *

if __name__ == '__main__':
    try:
        ml_help()

        df = ml_providers()
        print(df.head(10))

        df = ml_search("bike", "kaggle,usgov")
        print(df.head(3))
        print(df.tail(3))

    except Exception as e:
        print("Exception ", e)

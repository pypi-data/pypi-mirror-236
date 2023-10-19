from src.marcuslion import ml_help
from src.marcuslion import ml_addone
from src.marcuslion import ml_search

if __name__ == '__main__':
    try:
        ml_help()

        print(ml_addone(3))

        df = ml_search("bike", "kaggle,usgov")
        print(df.head(3))
        print(df.tail(3))

    except Exception as e:
        # print(e, '|', e.errno, '|', e.value, '|', e.args)
        print("Exception ", e)

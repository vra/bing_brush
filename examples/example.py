from bing_brush import BingBrush

def main():
    brush = BingBrush(
        cookie='/path/to/cookie.txt'
        verbose=False,
    )

    brush.process(
        prompt='a cute panda eating bamboos',
    )

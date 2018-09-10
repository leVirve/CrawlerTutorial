# 批踢踢爬蟲: PTT-parser

## 特色

* 一行指令下載看板內的所有文章及圖片

    ```bash
    ptt meta --board Movie --filepath ../sample.json --num 100
    ```

* 可程式化的 API 提供更靈活的操作

    ```python
    def get_metadata():
        # 取得文章列表基本資訊
        board = ptt.Board('Soft_Job')
        meta = board.get_meta(num=20)

        assert len(meta) == 20

        for m in meta:
            print(f'推文數: {m.push} ',
                f'標記: {m.mark} ',
                f'標題: {m.title} ',
                f'日期: {m.date} ',
                f'作者: {m.author} ',
                f'連結: {m.link} ',
                f'文章檔案編號: {m.filename} ',
                )

    def get_after_metadata():
        # 取得特定文章後的幾篇資訊
        board = ptt.Board('Movie')
        meta = board.get_meta(num=20)
        meta = board.get_meta(num=5, after_filename='M.1536559731.A.AE2')

        assert len(meta) == 5


    def get_post_content():
        # 取得完整文章資訊
        board = ptt.Board('Movie')
        meta = board.get_meta(num=1)

        post = board.get_post(link=meta[0].link)
        print(dir(post))
    ```

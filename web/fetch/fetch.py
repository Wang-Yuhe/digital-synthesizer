from playwright.sync_api import sync_playwright


def scrape_dom_html(url: str, output_file: str):
    """
    打开网页，抓取 JS 渲染后的完整 HTML 内容（等价于检查面板里的 DOM），并保存到输出文件。
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # 等待页面加载完成（含 JS 动态渲染）
        page.wait_for_load_state("networkidle")

        # 获取整个渲染后的 HTML 内容
        html = page.content()

        # 写入到文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"页面 HTML 内容已保存到 {output_file}")
        browser.close()


if __name__ == "__main__":
    url = "https://www.aoqiv.com/studio/"
    output_file = "dom_dump.txt"
    scrape_dom_html(url, output_file)

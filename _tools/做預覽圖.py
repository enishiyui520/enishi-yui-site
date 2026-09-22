# -*- coding: utf-8 -*-
"""重做社群預覽圖 assets/og.png（1200x630，Telegram／LINE／X／FB 分享連結時出現的那張）。

既有產線調查：本 repo 沒有做 og.png 的程式（7/3 那張是手做後直接 commit），
全機也沒有緣結專用的預覽圖產線；所以這支是新建。直接吃網站自己的素材
（assets/logo.png、assets/bg-poster.jpg）和網站同一組字型，換 LOGO 或背景之後重跑這支就會跟著變。

用法：python _tools/做預覽圖.py
"""
import pathlib
from playwright.sync_api import sync_playwright

站 = pathlib.Path(__file__).resolve().parent.parent
輸出 = 站 / "assets" / "og.png"

HTML = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@700;800&family=Zen+Maru+Gothic:wght@500;700&family=Klee+One:wght@600&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:1200px;height:630px;overflow:hidden;background:#fbf3ea;}
  .bg{position:absolute;inset:0;background:url("BG") 0% 42%/1200px auto no-repeat;}
  .wash{position:absolute;inset:0;background:linear-gradient(to right,
      rgba(251,243,234,0) 0%, rgba(251,243,234,0) 40%, rgba(251,243,234,.82) 58%, rgba(251,243,234,.96) 72%);}
  .card{position:absolute;left:684px;top:0;width:470px;height:630px;
      display:flex;flex-direction:column;align-items:center;justify-content:center;color:#5a444c;}
  .eyebrow{font-family:"Klee One";font-size:22px;letter-spacing:.34em;color:#a9772b;margin-bottom:14px;padding-left:.34em;}
  .logo{width:360px;height:auto;display:block;}
  .furi{font-family:"Shippori Mincho";font-weight:700;font-size:21px;letter-spacing:1.05em;color:#8a7079;margin:12px 0 22px;padding-left:1.05em;}
  .tag{font-family:"Zen Maru Gothic";font-weight:700;font-size:25px;letter-spacing:.04em;}
  .tag .r{color:#e0455a;}
  .rule{width:300px;height:2px;background:#e0455a;opacity:.55;margin:22px 0 16px;}
  .links{font-family:"Zen Maru Gothic";font-weight:500;font-size:20px;color:#a9772b;letter-spacing:.06em;}
</style></head><body>
<div class="bg"></div><div class="wash"></div>
<div class="card">
  <div class="eyebrow">縁結びの神様</div>
  <img class="logo" src="LOGO">
  <div class="furi">えにしゆい</div>
  <div class="tag">日本來的<span class="r">結緣神社</span>・實習神 <span class="r">♪</span></div>
  <div class="tag" style="margin-top:6px">幫你繫起好<span class="r">緣分</span></div>
  <div class="rule"></div>
  <div class="links">YouTube ・ Discord ・ X @enishi_yui</div>
</div>
</body></html>"""


def main():
    html = (HTML.replace("BG", (站 / "assets" / "bg-poster.jpg").as_uri())
                .replace("LOGO", (站 / "assets" / "logo.png").as_uri()))
    暫存 = 站 / "_tools" / "_og_render.html"
    暫存.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1200, "height": 630})
            pg.goto(暫存.as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            # 每一行字用它自己的字型、自己的文字檢查（CJK 字型按字切包，只會載到用得到的字）
            缺字型 = pg.evaluate("""[...document.querySelectorAll('.card div')]
                .filter(e => e.textContent.trim())
                .filter(e => { const s = getComputedStyle(e);
                    return !document.fonts.check(s.fontWeight + ' 20px ' + s.fontFamily, e.textContent); })
                .map(e => getComputedStyle(e).fontFamily + '：' + e.textContent.trim())""")
            if 缺字型:
                raise SystemExit(f"字型沒載到（沒網路？）：{缺字型}，不出圖")
            pg.screenshot(path=str(輸出))
            b.close()
    finally:
        暫存.unlink(missing_ok=True)
    print(f"已輸出 {輸出}")


if __name__ == "__main__":
    main()

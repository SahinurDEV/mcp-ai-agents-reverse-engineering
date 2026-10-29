#!/workspace/venv-pw/bin/python
"""Drive the MCP Inspector Web UI in a real Chrome window for lecture 3.3.

  inspector_tour.py serve        start Chrome (headed) and wait for steps
  inspector_tour.py STEP         ask the running tour to perform STEP
Steps: connect, tools, resources, prompts, close. Every click is a real UI click.
"""
import asyncio, os, re, sys, time
from pathlib import Path
from playwright.async_api import async_playwright

CTL = Path("/tmp/inspector_tour.step")
LOG = Path("/tmp/insp_web.log")
HEADLESS = os.environ.get("HEADLESS") == "1"

async def slow_type(loc, text):
    await loc.click(); await loc.press_sequentially(text, delay=120)

async def step(pg, name):
    if name == "connect":
        await pg.locator(".mantine-Switch-track").first.click()
        await pg.wait_for_timeout(2500)
    elif name == "tools":
        await pg.get_by_text("Tools", exact=True).first.click(); await pg.wait_for_timeout(1500)
        await pg.get_by_text("add", exact=True).first.click(); await pg.wait_for_timeout(1500)
        await slow_type(pg.get_by_role("textbox", name="A", exact=True), "2"); await slow_type(pg.get_by_role("textbox", name="B", exact=True), "40")
        await pg.wait_for_timeout(800)
        await pg.get_by_role("button", name="Execute Tool").click(); await pg.wait_for_timeout(2000)
    elif name == "resources":
        await pg.get_by_text("Resources", exact=True).first.click(); await pg.wait_for_timeout(2000)
        await pg.get_by_role("button", name="index", exact=True).click(); await pg.wait_for_timeout(3000)
        await pg.get_by_role("button", name="note", exact=True).click(); await pg.wait_for_timeout(1500)
        await slow_type(pg.locator("input[placeholder*='name' i]").first, "ghidra"); await pg.wait_for_timeout(500)
        btns = pg.locator("button").filter(has_text=re.compile("read|fetch|get|load|subscribe", re.I))
        print("res buttons", await btns.all_inner_texts(), file=sys.stderr)
        await btns.first.click(); await pg.wait_for_timeout(2000)
    elif name == "prompts":
        await pg.get_by_text("Prompts", exact=True).first.click(); await pg.wait_for_timeout(1500)
        await pg.locator("button").filter(has_text="summarize_note").first.click(); await pg.wait_for_timeout(1500)
        await slow_type(pg.locator("input[placeholder='Enter name...']"), "mcp"); await pg.wait_for_timeout(500)
        await pg.get_by_role("button", name="Get Prompt").click(); await pg.wait_for_timeout(2000)

async def serve():
    url = None
    for _ in range(60):
        m = re.search(r"http://127\.0\.0\.1:6274\?\S+", LOG.read_text() if LOG.exists() else "")
        if m: url = m.group(0); break
        time.sleep(0.5)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=HEADLESS,
            args=["--window-position=0,0", "--window-size=1920,1109", "--no-first-run",
                  "--disable-infobars", "--app=" + url])
        ctx = b.contexts[0] if b.contexts else await b.new_context(no_viewport=True)
        pg = ctx.pages[0] if ctx.pages else await ctx.new_page()
        if pg.url in ("about:blank", ""): await pg.goto(url)
        await pg.wait_for_timeout(2500)
        CTL.write_text("")
        while True:
            s = CTL.read_text().strip() if CTL.exists() else ""
            if s:
                CTL.write_text("")
                if s == "close": break
                try: await step(pg, s)
                except Exception as e: print("step failed", s, e, file=sys.stderr)
                if HEADLESS: await pg.screenshot(path=f"/tmp/v2f/tour_{s}.png")
                Path(f"/tmp/inspector_tour.{s}.done").write_text("ok")
            await asyncio.sleep(0.2)
        await b.close()

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "serve":
        asyncio.run(serve())
    else:
        Path(f"/tmp/inspector_tour.{a}.done").unlink(missing_ok=True)
        CTL.write_text(a)
        for _ in range(200):
            if a == "close" or Path(f"/tmp/inspector_tour.{a}.done").exists(): break
            time.sleep(0.1)

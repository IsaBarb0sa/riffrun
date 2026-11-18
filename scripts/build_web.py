"""Empacota a variante web sem alterar os assets do jogo desktop."""
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from imageio_ffmpeg import get_ffmpeg_exe


PROJECT_DIR = Path(__file__).resolve().parent.parent
BUILD_DIR = PROJECT_DIR / "build"
WEB_DIR = BUILD_DIR / "web"
WEB_PAGE_CUSTOMIZATION = Path(__file__).with_name("web_page.html")


def build():
    BUILD_DIR.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=BUILD_DIR) as temporary:
        app = Path(temporary) / "riffrun"
        app.mkdir()
        shutil.copy2(PROJECT_DIR / "main.py", app)
        shutil.copytree(PROJECT_DIR / "riffrun", app / "riffrun",
                        ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(PROJECT_DIR / "assets", app / "assets",
                        ignore=shutil.ignore_patterns("*.wav"))

        ffmpeg = get_ffmpeg_exe()
        for source in sorted((PROJECT_DIR / "assets" / "sounds" / "sfx").glob("*.wav")):
            target = (app / source.relative_to(PROJECT_DIR)).with_suffix(".ogg")
            subprocess.run([
                ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error",
                "-i", str(source), "-c:a", "libvorbis", "-q:a", "5", str(target),
            ], check=True)

        subprocess.run([
            sys.executable, "-m", "pygbag", "--build", "--no_opt",
            "--PYBUILD", "3.12",
            "--app_name", "Riff Run", "--title", "Riff Run",
            "--package", "io.github.nelicearaujo.riffrun", str(app),
        ], cwd=PROJECT_DIR, check=True)

        generated = app / "build" / "web"
        index = generated / "index.html"
        if not index.is_file() or not any(generated.glob("*.apk")):
            raise RuntimeError("O Pygbag não gerou o HTML e o pacote do jogo.")
        page = index.read_text(encoding="utf-8")
        if "</body>" not in page:
            raise RuntimeError("O HTML do Pygbag não contém a seção esperada para os controles.")
        customization = WEB_PAGE_CUSTOMIZATION.read_text(encoding="utf-8")
        index.write_text(page.replace("</body>", customization + "\n</body>", 1), encoding="utf-8")
        shutil.copytree(generated, WEB_DIR, dirs_exist_ok=True)

    print(f"Build web disponível em {WEB_DIR}")


if __name__ == "__main__":
    build()

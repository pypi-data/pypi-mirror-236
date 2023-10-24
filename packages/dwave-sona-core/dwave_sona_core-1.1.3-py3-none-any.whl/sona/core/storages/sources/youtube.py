from .base import SourceBase

try:
    import yt_dlp
except ImportError:
    pass


class YoutubeSource(SourceBase):
    ydl_opts = {
        "outtmpl": f"{str(SourceBase.tmp_dir)}/%(title)s",
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "lossless",
            }
        ],
    }

    @classmethod
    def download(cls, file):
        cls.tmp_dir.mkdir(parents=True, exist_ok=True)
        with yt_dlp.YoutubeDL(cls.ydl_opts) as ydl:
            info = ydl.extract_info(file.path, download=True)
            filepath = ydl.prepare_filename(info)
            return file.mutate(path=filepath + ".wav")

    @classmethod
    def verify(cls, file):
        return file.path and file.path.startswith("https://www.youtube.com/")

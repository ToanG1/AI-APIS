from youtube_transcript_api import YouTubeTranscriptApi
from models.subtitleResponse import subtitleResponse


def getYoutubeSubtitles(video_id):
    return subtitleResponse(200, "Get subtitles successfully", YouTubeTranscriptApi.get_transcript(video_id))
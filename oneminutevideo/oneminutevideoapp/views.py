from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import sys, os
from django.conf import settings
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from os import listdir
from os.path import isfile, join
import subprocess

class VideoCreateView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        try:              
            print("================================")
            print(self.request.data)
            data = self.request.data      
            print(data['name'])   
            print("================================")   
            print(data['file'])   
            print("================================")   
            print(data['audio']) 
            path = default_storage.save("video_files/" + data['name'], ContentFile(data['file'].read()))
            print(path)
            file_name = path.split('/')[1]
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            muted_video_path = os.path.join(settings.MEDIA_ROOT, "no_audio_videos" , file_name)
            subprocess.call(['ffmpeg', '-i', tmp_file, "-c" , "copy" , "-an" , muted_video_path])
            print(tmp_file)
            audio_path = os.path.join(settings.MEDIA_ROOT, "audio_files" , data['audio'])
            combine_audio_video = os.path.join(settings.MEDIA_ROOT, "final_videos" , file_name)
            subprocess.call(['ffmpeg', '-i', muted_video_path, "-i" , audio_path, "-c:v" , "copy" , "-c:a" , "aac" , combine_audio_video])
            res = "http://localhost:8000/media/final_videos/" + file_name            
            return Response({'path': res})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})

class AudioGetView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            path = os.path.join(settings.MEDIA_ROOT, "audio_files")
            print(path)
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]            
            return Response({'audios_file_list':onlyfiles})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer
from base.models import Room


@api_view(['GET'])
def getRoutes(request): 

    routes=[
        'GET /api',
        'GET /api/rooms', 
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request): 

    rooms=Room.objects.all()
    #response cannot return a python objects, we need to serialize it
   
    serializer=RoomSerializer(rooms,many=True)
   
    return Response(serializer.data)

@api_view(['GET'])

def getRoom(request,pk): 

    room=Room.objects.get(id=pk)
    #response cannot return a python objects, we need to serialize it
   
    serializer=RoomSerializer(room)
   
    return Response(serializer.data)
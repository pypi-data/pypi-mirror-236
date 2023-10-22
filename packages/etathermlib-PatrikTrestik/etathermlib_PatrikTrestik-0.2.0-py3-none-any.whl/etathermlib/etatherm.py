from __future__ import annotations
from datetime import datetime, timedelta
import socket
import time
import asyncio


class Etatherm:
    _responseDelay=4

    def __init__(self, host: str, port:int):
        self._host=host
        self._port=port
        self._socket=None
        self._params=None

    def __getHeader(self, a:int,j:int):
        return b'\x10\x01'+a.to_bytes(1,'big')+j.to_bytes(1,'big')

    def __getAddrRead(self, addr:bytes, cnt:int):
        n=cnt//2 - 1
        n=n%16
        b=(n << 4)+8
        return addr+b.to_bytes(1,'big')

    def __getAddrWrite(self, addr:bytes, cnt:int):
        n=cnt-1
        n=n%16
        b=(n << 4)+0x0c
        return addr+b.to_bytes(1,'big')

    def __getDelay(self):
        return (self._responseDelay//2).to_bytes(1,'big')

    def __getCRC(self, payload: bytes):
        s=0
        x=0
        for b in payload:
            s=b + s
            x=b ^ x
        return (s%256).to_bytes(1,'big') + (x%256).to_bytes(1,'big')

    def __checkHeader(self, data: bytes, a: int, j:int):
        while data[0:1]==b'\xff':
            data=data[1:]

        h=data[:2]
        if h!=b'\x10\x17':
            return (None, False)
        da=data[2:3]
        dj=data[3:4]
        if int.from_bytes(da,'little')!=a or int.from_bytes(dj,'little')!=j:
            return (None, False)
        return (data,True)

    def __checkTail(self, data):
        s1=data[-4:-3]
        s2=data[-3:-2]
        if s1!=b'\x00' and s2!=b'\x00':
            return (None, False)
        addxor=data[-2:]
        crc=self.__getCRC(data[:-2])
        if crc!=addxor:
            return (None, False)
        return (data[4:-4], True)

    async def __sendReadRequest(self, a:int, j:int, addr: bytes, count: int) -> tuple[bytes, str | None]:
        retr=3
        error=None
        while retr>0:
            retr-=1
            reader, writer =await self.__getSocket()
            try:
                out_bytes=self.__getHeader(a,j)+self.__getAddrRead(addr,count)+self.__getDelay()
                out_bytes=out_bytes+self.__getCRC(out_bytes) +b'\xff\xff'
                writer.write(out_bytes)
                await asyncio.wait_for(writer.drain(), 5)
                data = await asyncio.wait_for(reader.read(1024), 5)
                error = None
                break
            except TimeoutError as e:
                error= "Timeout"
            except ConnectionResetError as e:
                self.__closeSocket()
                error= "No connection"
        if error!=None:
            return (None, error)

        (data, ok)=self.__checkHeader(data, a, j)
        if not ok:
            return (None, 'Bad header')
        (data, ok)=self.__checkTail(data)
        if not ok:
            return (None,'Bad checksum')
        return (data, None)

    async def __sendWriteRequest(self, a:int, j:int, addr: bytes, data: bytes)->(bool, str):
        retr=3
        error=None
        while retr>0:
            retr-=1
            reader, writer =await self.__getSocket()
            try:
                out_bytes=self.__getHeader(a,j)+self.__getAddrWrite(addr,len(data))+data
                out_bytes=out_bytes+self.__getCRC(out_bytes) +b'\xff\xff'
                writer.write(out_bytes)
                await asyncio.wait_for(writer.drain(), 5)
                data = await asyncio.wait_for(reader.read(1024), 5)
                error = None
                break
            except TimeoutError as e:
                error= "Timeout"
            except ConnectionResetError as e:
                self.__closeSocket()
                error= "No connection"
        if error!=None:
            return (False, error)

        (data, ok)=self.__checkHeader(data, a, j)
        if not ok:
            return (False,'Bad header')
        (data, ok)=self.__checkTail(data)
        if not ok:
            return (False,'Bad checksum')
        if data!=b'\x00\x00':
            return (False,'Bad response')
        return (True, None)

    async def __readParams(self) -> None:
        start=0x1100
        nameStart=0x1030
        res={}
        for pos in range(1,17): 
            addr=start+(pos-1)*0x10
            (params, error)=await self.__sendReadRequest(0,1, addr.to_bytes(2,'big'), 4)
            if params==None:
                res[pos]=(False, "<timeout>", 5, 1)
                continue
            used=params[0] & 0x07
            used=not (used==0)
            shift = params[2] & 0x3F
            shift = shift-(64*(shift//32))
            step=(params[2] & 0xc0) >> 6
            step=step+1
            if used:
                addr=nameStart+(pos-1)*8
                (name, error)=await self.__sendReadRequest(0,1, addr.to_bytes(2,'big'), 8)
                if name==None:
                    name=b''
                end=name.find(b'\x00')
                if end!=-1:
                    name=name[:end]
                name=name.decode("1250")
            else:
                name=""
            res[pos]={'used':used, 'name':name, 'shift':shift, 'step':step }
        self._params=res

    async def getParameters(self)->(dict[int,dict[str,str]]|None):
        if self._params==None:
            await self.__readParams()
        if self._params==None:
            return None
        res={pos:{'name': p['name'],'min':(1+p['shift'])*p['step'], 'max':(30+p['shift'])*p['step']} for pos,p in self._params.items() if p['used']}
        self.__closeSocket()
        return res

    async def getCurrentTemperatures(self)-> (dict[int,int] | None):
        (data, error)=await self.__sendReadRequest(0,1, b'\x00\x60', 16)
        if self._params==None:
            await self.__readParams()
        if data==None or len(data)!=16 or self._params==None:
            return None
        res={}
        for pos in range(1,17):
            b=data[pos-1]
            position=self._params[pos]
            if position['used']:
                res[pos]= (b+position['shift'])*position['step']
        self.__closeSocket()
        return res
    
    def __getTOY(self, time:datetime)->int:
        return (time.minute // 15)+(time.hour*4)+(time.day*32*4)+(time.month*32*32*4)

    async def setTemporaryTemperature(self, pos:int, temperature: int, duration: int=120)-> bool:
        start=0x1100
        addr=start+(pos-1)*0x10+0x03
        
        if self._params==None:
            await self.__readParams()
        position=self._params[pos]
        temp=temperature//position['step']-position['shift'] & 0x1f
        now = datetime.now()
        start=self.__getTOY(now-timedelta(minutes=0))
        end=self.__getTOY(now+timedelta(minutes=duration+1))
        data=bytes([temp])+start.to_bytes(2,'big')+end.to_bytes(2,'big')
        (success, error)=await self.__sendWriteRequest(0,1, addr.to_bytes(2,'big'), data)

        if not success:
            return False
        return True

    async def getRequiredTemperatures(self) -> (dict[int,int] | None):
        (data, error)=await self.__sendReadRequest(0,1, b'\x00\x70', 16)
        if self._params==None:
            await self.__readParams()
        if data==None or len(data)!=16 or self._params==None:
            return None
        res={}
        for pos in range(1,17):
            b=data[pos-1] & 0x1f
            position=self._params[pos]
            if position['used']:
                res[pos]= (b+position['shift'])*position['step']
        self.__closeSocket()
        return res

    async def __getSocket(self):
        if self._socket==None:
            self._socket = await asyncio.open_connection(self._host, self._port)
        return self._socket

    def __closeSocket(self):
        if self._socket!=None:
            self._socket[1].close()
            self._socket=None







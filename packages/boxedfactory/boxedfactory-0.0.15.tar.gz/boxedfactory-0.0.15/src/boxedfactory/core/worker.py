import time
from threading import Thread
from enum import IntEnum

class LogKind:
    Information = "Information"
    Alert = "Alert"
    Error = "Error"
    Warning = "Warning"
    Success = "Success"

class WorkerLog:
    def __init__(self, title:str, kind:LogKind = LogKind.Information, detail:str = None) -> None:
        self.epoch:float = time.time()
        self.kind = kind
        self.title = title
        self.detail = detail or ''

class WorkerStatus(IntEnum):
    Stopped = 1
    Stopping = 2
    Paused = 3
    Active = 4

class Worker(Thread):
    def __init__(self, interval:float = 1000, log_size:int = 100) -> None:
        Thread.__init__(self)
        self.log_size = log_size
        self.logs:list[WorkerLog] = []
        self.status:WorkerStatus = WorkerStatus.Stopped
        self.interval = self.set_interval(interval)
        self.current:str = ''
        self.steps = 0
        self.step = 0
        self.meta:dict = dict()

    def log(self, title, kind:LogKind = LogKind.Information, detail:str = None):
        while len(self.logs) > self.log_size:
            self.logs.pop()
        self.logs.append(WorkerLog(title, kind, detail))

    def start(self) -> None:
        if self.status == WorkerStatus.Stopped:
            self.status = WorkerStatus.Active
            self.log("Started", LogKind.Success)
            return super().start()

    def set_interval(self, interval:float):
        self.interval = max(10, min(0.1, interval))
        return self.interval

    def run(self) -> None:
        while self.status not in [WorkerStatus.Stopped, WorkerStatus.Stopping]:
            if self.status != WorkerStatus.Paused:
                self.main_event_loop()
            time.sleep(self.interval)
        self.status = WorkerStatus.Stopped

    def main_event_loop(self):
        raise NotImplemented()

    def set_pause(self, paused:bool = True):
        if paused and self.status != WorkerStatus.Paused:
            self.status = WorkerStatus.Paused
            self.log("Paused", LogKind.Success)
        elif not paused and self.status == WorkerStatus.Paused:
            self.status = WorkerStatus.Active
            self.log("Resumed", LogKind.Success)

    def pause(self):
        return self.set_pause(True)

    def resume(self):
        return self.set_pause(False)

    def stop(self, retries:int = 3):
        if self.status in [WorkerStatus.Stopped, WorkerStatus.Stopping]:
            return
        self.status = WorkerStatus.Stopping
        while self.is_alive() and retries > 0:
            self.join(1000)
            retries -= 1
        if self.is_alive():
            self.log("Failed stop", LogKind.Error)
            self.status = WorkerStatus.Active
        else:
            self.log("Success stop", LogKind.Success)
            self.status = WorkerStatus.Stopped
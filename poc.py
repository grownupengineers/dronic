__DRONIC_STAGES_METHODS__ = dict()

def dronic_stage(func):
    __DRONIC_STAGES_METHODS__[func.__qualname__] = func
    return func

class DronicJob(object):

    def __init__(self, name: str, author: str):
        self.__jobname__ = name
        self.__author = author

    @property
    def name(self):
        return self.__jobname__

    @name.setter
    def name(self,value:str):
        self.__jobname__ = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self,value:str):
        self.__author = value

    def run(self,*args,**kwargs):

        import datetime                 

        # report = {
        #     'name' : self.__jobname__,
        #     'author' : self.__author,
        #     'startdate' : datetime.datetime.now(),
        #     'stages' : [],
        #     'result' : 'started'
        # }

        for k,_ in __DRONIC_STAGES_METHODS__.items():
            
            if not k.startswith(type(self).__qualname__):
                continue

            function = k.replace(f"{type(self).__qualname__}.","")
            
            x = self.__getattribute__(function)

            if type(x) == type(self.__init__): 
                before = datetime.datetime.now()                     
                __DRONIC_STAGES_METHODS__[k](self,*args,**kwargs)
                after = datetime.datetime.now()
                
                print ("Elapsed Time = {0}".format(after-before))              

class DronicScheduler(object):

    def __init__(self):
        self.__scheduled_jobs__ = []
        pass

    def load(self, url: str):
        pass

    def schedule(self, job: DronicJob, instances=1):
        pass

    def stop(self, id):
        pass

    def force_stop(self, id):
        pass

    def pause(self, id):
        pass

class Job1(DronicJob):

    @dronic_stage
    def checkout(self):
        print("Job 1 - Checkout Code!")

    @dronic_stage
    def pullimages(self):
        print("Job 1 - Pull images!")

class Job2(DronicJob):

    @dronic_stage
    def checkout(self):
        print("Job 2 - Checkout Code!")

    @dronic_stage
    def pullimages(self):
        print("Job 2 - Pull images!")

job1 = Job1("i","a")
job2 = Job2("i","a")

job1.run()
job2.run()

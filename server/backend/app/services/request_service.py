import datetime
from app import db, app
from app.models.request import Request, RequestState

class RequestService:
    @staticmethod
    def newRequest(master_id: str, worker_id: str):
        """Add or update new entry in request db

        Args:
            master_id (str): client_id of master from which request is comming
            worker_id (str): client_if of worker to which request will be shared

        Raises:
            Exception: Database Error
        """
        try:
            request = Request.query.filter_by(worker_id=worker_id, master_id=master_id).first()
            
            # create new request
            if request == None:
                request = Request(worker_id=worker_id, master_id=master_id,
                                state=RequestState.CREATED, state_update_time=datetime.datetime.now())
                db.session.add(request)
            # update previous request
            else:
                # only update request if its status is created of rejected
                if request.state == RequestState.CREATED or request.state == RequestState.REJECTED:
                    request.state = RequestState.CREATED
                    request.state_update_time = datetime.datetime.now()
    
            db.session.commit()

        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")

    @staticmethod
    def getMasterRequests(master_id: str)-> list[dict]:
        """Returns all request created by master

        Args:
            master_id (str): client_id of master

        Raises:
            Exception: _description_

        Returns:
            list[dict]: list of dict contaning worker_id(client_id) and state of request
        """
        try:
            result = Request.query.filter_by(master_id=master_id).with_entities(Request.worker_id, Request.state).all()
            result = [{'worker_id':row[0], 'state': row[1].name} for row in result]
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
        
        return result

    @staticmethod
    def getWorkerRequests(worker_id: str)-> list[dict]:
        """Returns all request recived by a worker

        Args:
            worker_id (str): client_id of worker

        Raises:
            Exception: _description_

        Returns:
            list[dict]: list of dict contaning master_id(client_id) and state of request
        """
        try:
            result = Request.query.filter_by(worker_id=worker_id).with_entities(Request.master_id, Request.state).all()
            result = [{'master_id':row[0], 'state': row[1].name} for row in result]
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
        
        return result


    @staticmethod
    def rejectComputeRequest(master_id, worker_id):
        """Reject Compute request from master

        Args:
            master_id (_type_): client_id of master
            worker_id (_type_): client_id of worker

        Raises:
            Exception: raise exception on error
        """
        try:
            Request.query.filter_by(
                master_id=master_id, 
                worker_id=worker_id).update(
                    dict(
                        state_update_time = datetime.datetime.now(),
                        state = RequestState.REJECTED
                    ))
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")

    
    @staticmethod
    def acceptComputeRequest(master_id, worker_id):
        """Accept Compute request from master

        Args:
            master_id (_type_): client_id of master
            worker_id (_type_): client_id of worker

        Raises:
            Exception: raise exception on error
        """
        try:
            result = Request.query.filter_by(
                master_id=master_id, 
                worker_id=worker_id).update(
                    dict(
                        state_update_time = datetime.datetime.now(),
                        state = RequestState.ACCEPTED
                    ))
            db.session.commit()
            
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
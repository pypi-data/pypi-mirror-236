_E='service'
_D='POST'
_C='message'
_B='error'
_A='status'
import json
from localstack.http import Request,Response,route
from.manager import SnapshotManager
class StateResource:
	'\n    Internal endpoints to trigger state management operations.\n    ';service_state_manager:0
	def __init__(A,service_state_manager):A.service_state_manager=service_state_manager
	@route('/_localstack/state/<service>/load',methods=[_D])
	def load_service_state(self,_,service):
		try:self.service_state_manager.load(service)
		except Exception as A:return Response(json.dumps({_A:_B,_C:str(A)}),status=500)
	@route('/_localstack/state/<service>/save',methods=[_D])
	def save_service_state(self,_,service):
		try:self.service_state_manager.save(service)
		except Exception as A:return Response(json.dumps({_B:_B,_C:str(A)}),status=500)
	@route('/_localstack/state/load',methods=[_D])
	def load_multiple_service_states(self,_):
		A=self;D=A.service_state_manager.service_sorter.sort_services(list(A.service_state_manager.tracker.keys()))
		def B():
			'\n            Iterates through services and loads their state one by one. The generator streams the responses\n            back to the client as a chunked response, where each load operation is one JSON line.\n            '
			for B in D:
				try:A.service_state_manager.load(B);C={_E:B,_A:'ok'}
				except Exception as E:C={_E:B,_A:_B,_C:f"{E}"}
				yield json.dumps(C)+'\n'
		return Response(response=B())
	@route('/_localstack/state/save',methods=[_D])
	def save_multiple_service_states(self,_):
		C=self.service_state_manager.service_manager.values()
		def A():
			'\n            Iterates through services and saves their state one by one. The generator streams the responses\n            to the client as a chunked response, where each save operation is one JSON line.\n            '
			for D in C:
				A=D.name()
				try:self.service_state_manager.save(A);B={_E:A,_A:'ok'}
				except Exception as E:B={_E:A,_A:_B,_C:f"{E}"}
				yield json.dumps(B)+'\n'
		return Response(response=A())